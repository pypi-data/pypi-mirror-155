import select
import socket
import threading
import time

import pycurl

# Debug shortcut
dprint = lambda x: None

# Merging ideas from:
#   https://github.com/pycurl/pycurl/blob/master/examples/multi-socket_action-select.py
#   https://github.com/fsbs/aiocurl

Auth = {
    "BASIC": pycurl.HTTPAUTH_BASIC,
    "DIGEST": pycurl.HTTPAUTH_DIGEST,
    "DIGEST_IE": pycurl.HTTPAUTH_DIGEST_IE,
    "BEARER": pycurl.XOAUTH2_BEARER,
    "NEGOTIATE": pycurl.HTTPAUTH_NEGOTIATE,
    "NTLM": pycurl.HTTPAUTH_NTLM,
    "NTLM_WB": pycurl.HTTPAUTH_NTLM_WB,
    "ANY": pycurl.HTTPAUTH_ANY,
    "ANYSAFE": pycurl.HTTPAUTH_ANYSAFE
}

def sanitized(msg):
    lower = msg.lower()
    if "authorization: " in lower or "authenticate: " in lower:
        spl = msg.split(" ")
        if len(spl) > 2 or "authorization: " in lower:
            m = ""
            for i in range(len(spl)):
                if i < len(spl)-1:
                    m += spl[i] + " "
                else:
                    m += "sanitized len(%d)" % len(spl[i])
            return m
    return msg

class Curl:
    # Data
    easy = None
    sock_fd = None

    # Request info
    method = None
    proxy = False
    size = None

    # Status
    done = False
    errstr = ""

    def __init__(self, url, method = "GET", request_version = "HTTP/1.1"):
        """
        Initialize curl instance

        method = GET, POST, PUT, CONNECT, etc.
        request_version = HTTP/1.0, HTTP/1.1, etc.
        """
        dprint("New curl instance")
        self.easy = pycurl.Curl()

        self._setup(url, method, request_version)

    def _setup(self, url, method = "GET", request_version = "HTTP/1.1"):
        dprint("%s %s using %s" % (method, url, request_version))

        # Ignore environment variables
        self.easy.setopt(pycurl.PROXY, "")
        self.easy.setopt(pycurl.NOPROXY, "")
        self.easy.setopt(pycurl.TIMEOUT, 5)

        # Set HTTP method
        self.method = method
        if method == "CONNECT":
            self.easy.setopt(pycurl.CONNECT_ONLY, True)

            # We want libcurl to make a simple HTTP connection to auth
            # with the upstream proxy and let client establish SSL
            if "://" not in url:
                url = "http://" + url
        elif method == "GET":
            self.easy.setopt(pycurl.HTTPGET, True)
        elif method == "HEAD":
            self.easy.setopt(pycurl.NOBODY, True)
        elif method == "POST":
            self.easy.setopt(pycurl.POST, True)
        elif method == "PUT":
            self.easy.setopt(pycurl.UPLOAD, True)
        elif method in ["PATCH", "DELETE"]:
            self.easy.setopt(pycurl.CUSTOMREQUEST, method)
        else:
            dprint("Unknown method: " + method)
            self.easy.setopt(pycurl.CUSTOMREQUEST, method)

        self.easy.setopt(pycurl.URL, url)

        # Set HTTP version to use
        version = request_version.split("/")[1].replace(".", "_")
        self.easy.setopt(pycurl.HTTP_VERSION, getattr(pycurl, "CURL_HTTP_VERSION_" + version))

    def reset(self, url, method = "GET", request_version = "HTTP/1.1"):
        "Reuse existing curl instance for another request"
        dprint("Resetting curl")
        self.easy.reset()
        self.sock_fd = None
        self.proxy = False
        self.size = None
        self.done = False
        self.errstr = ""

        self._setup(url, method, request_version)

    def is_connect(self):
        return self.method == "CONNECT"

    def is_upload(self):
        return self.method in ["PUT", "POST", "PATCH"]

    def get_response(self):
        return self.easy.getinfo(pycurl.RESPONSE_CODE)

    def set_proxy(self, proxy = "", noproxy = None, user = None, password = None, auth = "ANY"):
        "Set proxy options"
        self.proxy = True
        self.easy.setopt(pycurl.PROXY, proxy)
        if noproxy is not None:
            self.easy.setopt(pycurl.NOPROXY, noproxy)
        if user is not None:
            self.easy.setopt(pycurl.PROXYUSERNAME, user)
        if password is not None:
            self.easy.setopt(pycurl.PROXYPASSWORD, password)
        if auth is not None:
            self.easy.setopt(pycurl.PROXYAUTH, Auth[auth])

    def set_headers(self, xheaders):
        "Set headers to send"
        headers = []
        for header in xheaders:
            if not self.proxy and header.lower().startswith("proxy-"):
                dprint("Skipping header =!> %s: %s" % (header, xheaders[header]))
                continue
            if header.lower() == "content-length" and self.is_upload():
                self.size = int(xheaders[header])
                headers.append("Transfer-Encoding:")
            headers.append("%s: %s" % (header, xheaders[header]))

        if len(headers) != 0:
            self.easy.setopt(pycurl.HTTPHEADER, headers)

    def set_verbose(self, enable = True):
        "Set verbose mode"
        self.easy.setopt(pycurl.VERBOSE, enable)

    def _debug_callback(self, type, msg):
        if type == pycurl.INFOTYPE_TEXT:
            prefix = "Curl info: "
        elif type == pycurl.INFOTYPE_HEADER_IN:
            prefix = "Received header <= "
        elif type == pycurl.INFOTYPE_HEADER_OUT:
            prefix = "Sent header => "
        else:
            return
        msg = msg.decode("utf-8").strip()
        if "\r\n" in msg:
            for m in msg.split("\r\n"):
                if len(m) != 0:
                    dprint(prefix + sanitized(m))
        else:
            if len(msg) != 0:
                dprint(prefix + sanitized(msg))

    def set_debug(self, enable = True):
        "Enable debug output"
        self.set_verbose(enable)
        if enable:
            self.easy.setopt(pycurl.DEBUGFUNCTION, self._debug_callback)
        else:
            self.easy.setopt(pycurl.DEBUGFUNCTION, None)

    def _read_callback(self, size):
        dprint("Reading data")
        data = ""
        if self.size is not None:
            if self.size > size:
                self.size -= size
                data = self.read_from.read(size)
            else:
                size = self.size
                self.size = None
                data = self.read_from.read(size)
        return data

    def bridge(self, read_from = None, write_to = None):
        """
        Bridge curl reads/writes to fds specified

        read_from should be open("rb")
        write_to should be open("wb")
        """
        dprint("Bridging")
        if read_from is not None:
            self.read_from = read_from
            self.easy.setopt(pycurl.READFUNCTION, self._read_callback)

        if write_to is not None:
            self.easy.setopt(pycurl.WRITEDATA, write_to)
            self.easy.setopt(pycurl.WRITEHEADER, write_to)

            # Turn off transfer decoding - let client do it
            self.easy.setopt(pycurl.HTTP_TRANSFER_DECODING, False)

class MCurl:
    _multi = None
    _rlist = None
    _wlist = None
    _handles = None
    _last = None
    _socks = None
    _lock = None

    def __init__(self, debug_print = None):
        "Initialize multi interface"
        global dprint
        if debug_print is not None:
            dprint = debug_print

        self._multi = pycurl.CurlMulti()

        # Set a callback for registering or unregistering socket events.
        self._multi.setopt(pycurl.M_SOCKETFUNCTION, self._socket_callback)

        # Set a callback for scheduling or cancelling timeout actions.
        self._multi.setopt(pycurl.M_TIMERFUNCTION, self._timer_callback)

        # Init
        self._rlist = []
        self._wlist = []
        self._handles = {}
        self._socks = {}
        self._lock = threading.Lock()

    def setopt(self, option, value):
        "Configure multi options"
        if option in (pycurl.M_SOCKETFUNCTION, pycurl.M_TIMERFUNCTION):
            raise Exception('callback option reserved for the event loop')
        self._multi.setopt(option, value)

    # Callbacks

    def _socket_callback(self, ev_bitmask, sock_fd, multi, data):
        # libcurl socket callback: add/remove actions for socket events
        if ev_bitmask & pycurl.POLL_IN or ev_bitmask & pycurl.POLL_INOUT:
            dprint("Read sock_fd %d" % sock_fd)
            if sock_fd not in self._rlist:
                self._rlist.append(sock_fd)

        if ev_bitmask & pycurl.POLL_OUT or ev_bitmask & pycurl.POLL_INOUT:
            dprint("Write sock_fd %d" % sock_fd)
            if sock_fd not in self._wlist:
                self._wlist.append(sock_fd)

        if ev_bitmask & pycurl.POLL_REMOVE:
            dprint("Remove sock_fd %d" % sock_fd)
            if sock_fd in self._rlist:
                self._rlist.remove(sock_fd)
            if sock_fd in self._wlist:
                self._wlist.remove(sock_fd)

    def _timer_callback(self, timeout_ms):
        # libcurl timer callback: schedule/cancel a timeout action
        #dprint("timeout = %d" % timeout_ms)
        if timeout_ms == -1:
            self._timer = None
        else:
            self._timer = timeout_ms / 1000.0

    def _socket_action(self, sock_fd, ev_bitmask):
        # Event loop callback: act on ready sockets or timeouts
        #dprint("mask = %d, sock_fd = %d" % (ev_bitmask, sock_fd))
        status, handle_count = self._multi.socket_action(sock_fd, ev_bitmask)

        # Check if any handles have finished.
        if handle_count != len(self._handles):
            self._update_transfers()

    def _update_transfers(self):
        # Mark finished handles as done
        more_info, succ_handles, fail_handles = self._multi.info_read()

        for easy in succ_handles:
            self._handles[easy].done = True

        for easy, errno, errmsg in fail_handles:
            curl = self._handles[easy]
            curl.done = True
            curl.errstr += str(errno) + ": " + errmsg + "; "
            # if curl.sock_fd is not None:
            #     if curl.sock_fd in self._rlist:
            #         self._rlist.remove(curl.sock_fd)
            #     if curl.sock_fd in self._wlist:
            #         self._wlist.remove(curl.sock_fd)

        if more_info:
            self._update_transfers()

    def _assign_sock_callback(self, sock_fd, purpose):
        # Associate new socket with last handle added
        dprint("sock_fd = %d" % sock_fd)
        if sock_fd not in self._socks:
            self._last.sock_fd = sock_fd
            self._socks[sock_fd] = self._last
            self._last = None

        return pycurl.E_OK

    # Adding to multi

    def _add_handle(self, curl: Curl):
        # Add a handle
        dprint("Add handle")
        if curl.easy not in self._handles:
            self._handles[curl.easy] = curl
            if curl.is_connect():
                # Need to know socket assigned for CONNECT since used later in select()
                self._last = curl
                curl.easy.setopt(pycurl.SOCKOPTFUNCTION, self._assign_sock_callback)
            self._multi.add_handle(curl.easy)
            dprint("Added handle")
        else:
            dprint("Active handle")

    def add(self, curl: Curl):
        """
        Add a Curl handle to perform

        Waits until multi instance is ready to add a handle
        """
        while True:
            with self._lock:
                dprint("Handles = %d, socks = %d" % (len(self._handles), len(self._socks)))
                dprint("Rlist = %s, wlist = %s" % (self._rlist, self._wlist))
                if len(self._handles) > len(self._socks):
                    dprint("Multi not ready for new curl")
                else:
                    self._add_handle(curl)
                    break
            self.perform()
            time.sleep(0.01)

    # Removing from multi

    def _remove_handle(self, curl: Curl, errstr = ""):
        # Remove a handle and set status
        if curl.easy not in self._handles:
            return

        if curl.done == False:
            curl.done = True

        if len(errstr) != 0:
            curl.errstr += errstr + "; "

        dprint("Remove handle: " + curl.errstr)
        if len(curl.errstr) == 0:
            self._multi.remove_handle(curl.easy)
        if curl.is_connect() and curl.sock_fd is not None:
            self._socks.pop(curl.sock_fd)
        self._handles.pop(curl.easy)

    def remove(self, curl: Curl):
        "Remove a Curl handle once done"
        with self._lock:
            self._remove_handle(curl)

    def stop(self, curl: Curl):
        "Stop a running curl handle and remove"
        with self._lock:
            self._remove_handle(curl, errstr = "Stopped")

    # Executing multi

    def perform(self):
        "Perform all tasks in the multi instance"
        with self._lock:
            rready, wready, xready = select.select(self._rlist, self._wlist, set(self._rlist) | set(self._wlist), self._timer)

            if len(rready) == 0 and len(wready) == 0 and len(xready) == 0:
                #dprint("No activity")
                self._socket_action(pycurl.SOCKET_TIMEOUT, 0)
            else:
                for sock_fd in rready:
                    #dprint("Ready to read sock_fd %d" % sock_fd)
                    self._socket_action(sock_fd, pycurl.CSELECT_IN)
                for sock_fd in wready:
                    #dprint("Ready to write sock_fd %d" % sock_fd)
                    self._socket_action(sock_fd, pycurl.CSELECT_OUT)
                for sock_fd in xready:
                    #dprint("Error sock_fd %d" % sock_fd)
                    self._socket_action(sock_fd, pycurl.CSELECT_ERR)


    def do(self, curl: Curl):
        "Add a Curl handle and peform until completion"
        self.add(curl)
        while True:
            if curl.done:
                break
            self.perform()
            time.sleep(0.01)
        return len(curl.errstr) == 0

    def select(self, curl: Curl, client, idle = 30):
        "Run select loop between client and curl"
        # TODO figure out if IPv6 or IPv4
        if curl.sock_fd is None:
            # Reusing a CONNECT!?
            dprint("sock_fd is None")
            return

        curl_sock = socket.fromfd(curl.sock_fd, socket.AF_INET, socket.SOCK_STREAM)

        # sockets will be removed from these lists, when they are
        # detected as closed by remote host; wlist contains sockets
        # only when data has to be written
        rlist = [client, curl_sock]
        wlist = []

        # data to be written to client connection and proxy socket
        cl = 0
        cs = 0
        cdata = []
        sdata = []
        max_idle = time.time() + idle
        while (rlist or wlist):
            (ins, outs, exs) = select.select(rlist, wlist, rlist, idle)
            if exs:
                break
            if ins:
                for i in ins:
                    if i is curl_sock:
                        out = client
                        wdata = cdata
                        source = "proxy"
                    else:
                        out = curl_sock
                        wdata = sdata
                        source = "client"

                    data = i.recv(4096)
                    if data:
                        cl += len(data)
                        # Prepare data to send it later in outs section
                        wdata.append(data)
                        if out not in outs:
                            outs.append(out)
                        max_idle = time.time() + idle
                    else:
                        # No data means connection closed by remote host
                        dprint("Connection closed by %s" % source)
                        # Because tunnel is closed on one end there is
                        # no need to read from both ends
                        del rlist[:]
                        # Do not write anymore to the closed end
                        if i in wlist:
                            wlist.remove(i)
                        if i in outs:
                            outs.remove(i)
            if outs:
                for o in outs:
                    if o is curl_sock:
                        wdata = sdata
                    else:
                        wdata = cdata
                    data = wdata[0]
                    # socket.send() may sending only a part of the data
                    # (as documentation says). To ensure sending all data
                    bsnt = o.send(data)
                    if bsnt > 0:
                        if bsnt < len(data):
                            # Not all data was sent; store data not
                            # sent and ensure select() get's it when
                            # the socket can be written again
                            wdata[0] = data[bsnt:]
                            if o not in wlist:
                                wlist.append(o)
                        else:
                            wdata.pop(0)
                            if not data and o in wlist:
                                wlist.remove(o)
                        cs += bsnt
                    else:
                        dprint("No data sent")
                max_idle = time.time() + idle
            if max_idle < time.time():
                # No data in timeout seconds
                dprint("Proxy connection timeout")
                break

        # After serving the proxy tunnel it could not be used for samething else.
        # A proxy doesn't really know, when a proxy tunnnel isn't needed any
        # more (there is no content length for data). So servings will be ended
        # either after timeout seconds without data transfer or when at least
        # one side closes the connection. Close both proxy and client
        # connection if still open.
        dprint("%d bytes read, %d bytes written" % (cl, cs))

        dprint("DONE")

    # Cleanup multi

    def close(self):
        "Stop any running transfers and close this multi handle"
        dprint("Closing multi")
        for easy in tuple(self._handles):
            self.stop(self._handles[easy])
        self._multi.close()

def tester(multi, url):
    curl = Curl(url)
    curl.set_debug()
    multi.do(curl)
    multi.remove(curl)

if __name__ == "__main__":
    import debug
    dbg = debug.Debug("test.log", "w")
    dprint = dbg.get_print()

    multi = MCurl()

    urls = ["http://www.google.com"]

    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
        futures = {executor.submit(tester, multi, url): url for url in urls}
        for future in concurrent.futures.as_completed(futures):
            url = futures[future]
            print("Done: " + url)

    multi.close()