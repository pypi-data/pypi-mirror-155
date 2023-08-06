import json as _json, requests, urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_s = requests.Session()
_s.local_endpoint = None
_s.tls = None

def init_api_remote(ip, key):
    _s.headers = {"authorization" : str(key)}
    
    if not "http://" in ip and not "https://" in ip:
        ip = "https://" + ip
    
    if ip[-1] == "/":
        ip = ip[:-1]
        
    _s.local_endpoint = ip
    return ping()

def ping(timeout=5):
    if not _s.local_endpoint: return False
    try:
        resp = _s.post(_s.local_endpoint, timeout=timeout, verify=False)
        response = _json.loads(resp.text)
        if "error" in response:
            raise Exception("bad key")
        else:
            return response["status"] == "ok"
        
    except requests.Timeout:
        return False
    
    except requests.ConnectionError:
        return False
    
class Session:
    
    def __init__(self):
        if not _s.local_endpoint:
            raise Exception("please init api with 'init_api' or 'init_api_remote'")
            
        if ping():
            response = _json.loads(_s.post(_s.local_endpoint+"/session/new", verify=False).text)
            if response["success"]:
                self.id = response["session-id"]
            else:
                raise Exception(_json.dumps(response))
        else:
            raise Exception("tls api is not currently activated")

        self.headers = {
            "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
        }
        
        self.pheaders = ["method", "authority", "scheme", "path"]
        self.navigator = "chrome" # "chrome" or "firefox"
        self.cookies = {}
        
        self.proxies = "" #depreciated -> use session.proxy instead
        self.proxy = "" #http://username:password@hostname.com:443
    
        
    def call(self, path, information={}):
        resp = _s.post(_s.local_endpoint+path+"?sid="+str(self.id), json=information, verify=False)
        return _json.loads(resp.text)
        
    def get_cookies(self, domain):
        return self.call("/session/cookies", information={
                    "domain" : domain
            })
    
    def close(self):
        result = self.call("/session/close")
    
        if not result["success"]:
            settingsErr = result["error"]
            raise Exception("error : %s" % settingsErr)
        else:
            return True
        
    def keep_alive(self):
        result = self.call("/session/keep-alive")
    
        if not result["success"]:
            settingsErr = result["error"]
            raise Exception("error : %s" % settingsErr)
        else:
            return True
            
    def apply_ja3(self, ja3 : str, specifications={}):
        '''
        Parameters : 
            ja3 : str
            curves : list (optional)
            specifications : dict (optional)

        Raises:
            Exception if an invalid ja3 string is given.
        
        Returns:
            True
            
        Specifications:
            You can specify any extensions details
            
            key : string -> extension id
            value : list -> list of values (string or integer)
            
            Example:
                specifications = {
                    "13" : [1027, 1283, 1539, 2052, 2053, 2054, 1025, 1281, 1537, 515, 513], #algorithm signatures
                    "16" : ["h2", "http/1.1"],                                               #ALPN
                    "34" : [1027, 1283, 1539, 515],                                          #delegated credentials
                    "43" : [771, 770, 769, 769],                                             #supported versions
                    "51" : [29, 23],                                                         #key share
                    "17513" : ["h2"]                                                         #application settings
                }
                
                *for any GREASE value, please set -1                
                **if no or not enough specifications are specified, the default values will be taken for the missing specifications (based on navigator's presets')
        '''
        result = self.call("/session/tls/ja3", {
                "ja3" : ja3,
                "specifications" : specifications,
                "navigator" : self.navigator
            })
        
        
        if not result["success"]:
            ja3err = result["error"]
            raise Exception("JA3 error : %s" % ja3err)
        else:
            return True
        
    def apply_http2_settings(self, settings : list):
        '''
        Parameters : 
            settings : list   

        Raises:
            Exception if invalid settings are given.

        Returns:
            True (everything is alright)
        
        • Example : 
            [
                {
                    "name": "HEADER_TABLE_SIZE",
                    "value": 65536
                },
                {
                    "name": "INITIAL_WINDOW_SIZE",
                    "value": 131072
                },
                {
                    "name": "MAX_FRAME_SIZE",
                    "value": 16384
                }
            ]
    
        • Valid settings' name for HTTP/2 request : 
            - HEADER_TABLE_SIZE
            - ENABLE_PUSH
            - MAX_CONCURRENT_STREAMS
            - INITIAL_WINDOW_SIZE
            - MAX_FRAME_SIZE
            - MAX_HEADER_LIST_SIZE
            - WINDOWS_UPDATE (only for flow-control)
            
        • More information about all HTTP2 SETTINGS : https://httpwg.org/specs/rfc7540.html#SETTINGS
        '''
        result = self.call("/session/http2/settings", {
                "settings" : settings
            })
        
        if not result["success"]:
            settingsErr = result["error"]
            raise Exception("SETTINGS error : %s" % settingsErr)
        else:
            return True
    
    def apply_windows_update(self, value : int):
        '''
        Parameters : 
            value : int (The legal range for the increment to the flow-control window is 1 to 2^31-1 (2,147,483,647) octets)

        Raises:
            Exception if invalid value is given.

        Returns:
            True (everything is alright)
        
        • More information about WINDOWS_UPDATE : https://httpwg.org/specs/rfc7540.html#WINDOW_UPDATE
        '''
        if value >= 1 and value <= 2**31-1:
            result = self.call("/session/http2/windows-update", {
                    "value" : value
                })
            
            if not result["success"]:
                error = result["error"]
                raise Exception("WINDOWS_UPDATE error : %s" % error)
            else:
                return True
        else:
            raise Exception(
                "WINDOWS_UPDATE error : The legal range for the increment to the flow-control window is 1 to 2^31-1 (2,147,483,647) octets")
    
    def apply_stream_priorities(self, streams : list):
        '''
        Parameters : 
            streams : list
        ----------
        Raises:
            Exception if invalid streams are given.
        ----------
        Returns:
            True (everything is alright)
        
        • Example : 
            [
                {
                    "stream-id": 3,
                    "stream-param": {
                        "weight": 200
                    }
                },
                {
                    "stream-id": 5,
                    "stream-param": {
                        "weight": 100
                    }
                },
                {
                    "stream-id": 7,
                    "stream-param": {
                        "weight": 0
                    }
                },
                {
                    "stream-id": 9,
                    "stream-param": {
                        "weight": 0,
                        "stream-dep" : 7
                    }
                },
                {
                    "stream-id": 11,
                    "stream-param": {
                        "weight": 0,
                        "stream-dep" : 3
                    }
                },
                {
                    "stream-id": 13,
                    "stream-param": {
                        "weight": 240
                    }
                }
            ]
                
        • stream param key value : 
            - stream-id : int
            - stream-param : dict
            - weight : int
            - stream-dep : int
            - exclusive : bool
            
        • More information about stream priorities : https://httpwg.org/specs/rfc7540.html#PRIORITY
        '''
        
        result = self.call("/session/http2/stream-priorities", {
            "streams" : streams
        })
                
        if not result["success"]:
            streamErr = result["error"]
            raise Exception("Streams error : %s" % streamErr)
        else:
            return True
    
    def get(self, url, data="", json={}, timeout=30, allow_redirects=True, server_push=False, verify=True, headers={}, proxies=""):
        return self.send(
            "GET", 
            url, 
            data=data, 
            json=json, 
            timeout=timeout, 
            allow_redirects=allow_redirects, 
            server_push=server_push,
            verify=verify,
            headers=headers,
            proxies=proxies,
        )

    def post(self, url, data="", json={}, timeout=30, allow_redirects=True, server_push=False, verify=True, headers={}, proxies=""):
        return self.send(
            "POST", 
            url, 
            data=data, 
            json=json, 
            timeout=timeout, 
            allow_redirects=allow_redirects, 
            server_push=server_push,
            verify=verify,
            headers=headers,
            proxies=proxies,
        )    
    
    def patch(self, url, data="", json={}, timeout=30, allow_redirects=True, server_push=False, verify=True, headers={}, proxies=""):
        return self.send(
            "PATCH", 
            url, 
            data=data, 
            json=json, 
            timeout=timeout, 
            allow_redirects=allow_redirects, 
            server_push=server_push,
            verify=verify,
            headers=headers,
            proxies=proxies,
        )    
    
    def option(self, url, data="", json={}, timeout=30, allow_redirects=True, server_push=False, verify=True, headers={}, proxies=""):
        return self.send(
            "OPTION", 
            url, 
            data=data, 
            json=json, 
            timeout=timeout, 
            allow_redirects=allow_redirects, 
            server_push=server_push,
            verify=verify,
            headers=headers,
            proxies=proxies,
        )    
    
    def put(self, url, data="", json={}, timeout=30, allow_redirects=True, server_push=False, verify=True, headers={}, proxies=""):
        return self.send(
            "PUT", 
            url, 
            data=data, 
            json=json, 
            timeout=timeout, 
            allow_redirects=allow_redirects, 
            server_push=server_push,
            verify=verify,
            headers=headers,
            proxies=proxies,
        )    
    
    
    def delete(self, url, data="", json={}, timeout=30, allow_redirects=True, server_push=False, verify=True, headers={}, proxies=""):
        return self.send(
            "DELETE", 
            url, 
            data=data, 
            json=json, 
            timeout=timeout, 
            allow_redirects=allow_redirects, 
            server_push=server_push,
            verify=verify,
            headers=headers,
            proxies=proxies,
        )    
    
    def send(self, method, url, data="", json={}, timeout=30, allow_redirects=True, server_push=False, verify=True, headers={}, proxies=""):
        if json != {}:
            data = _json.dumps(json)
            headers["Content-Type"] = "application/json"    
        
        information = {
            "method" : method,
            "url" : url,
            "data" : data,
            "pheader" : self.pheaders,
            "header" : {str(key): str(value) for key, value in headers.items()} or {key : value for key, value in self.headers.items()},
            "header-order" : [str(key) for key in headers.keys()] or [str(key) for key in self.headers.keys()],
            "proxy" : proxies or self.proxy or self.proxies,
            "navigator" : self.navigator,
            "timeout" : timeout,
            "allow-redirect" : allow_redirects,
            "server-push" : server_push,
            "verify" : verify
            }
        
        result = self.call("/session/request", information)
        response = self.Response(result)
        
        if "server-push" in result and result["server-push"] != None:            
            response.server_push = [self.Response(element) for element in result["server-push"]]
        else:
            response.server_push = []
        
        self.update(response)
        return response
        
        
    def update(self, response):        
        for key, value in response.cookies.items():
            self.cookies[key] = value
    
    class Response:
        
        def __init__(self, response):
            self.response = response
                        
            if "error" in self.response:
                error = self.response["error"]
                if "timeout" in error:
                    raise TimeoutError(error)
                else:
                    raise Exception(error)


                
            self.status_code = self.response["status_code"]
            
            if "id" in self.response:
                self.id = self.response["id"]
            
            if self.status_code == 0:
                error = self.response["body"]
                raise Exception("An error occurred : %s" % error)
                
            self.cookies = self.response["cookies"]
            self.url = self.response["url"]
            self.headers = self.response["headers"]
            self.text = self.response["body"]

        def __repr__(self):
            return "status : " + str(self.status_code)
        