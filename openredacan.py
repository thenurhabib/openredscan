#!/usr/bin/env python3

import re
import random
import requests
import warnings
import argparse
from plugins.banner import *
from bs4 import BeautifulSoup
from core.bug import crlfScanFunc
from payload.payload import sourcesSinks
from core.gatherurls import getAllURLsFunc
from core.features import requesterFunc, multitest

# Ignore Wornings
warnings.filterwarnings('ignore')

# Print Banner
bannerFunc()

# Arguments
parser = argparse.ArgumentParser(usage="Help Menu")
parser.add_argument('-u', help='Domain Name.', dest="url")
parser.add_argument('-l', help='Multiple targets. (Ex: domains.txt)', dest='path')
parser.add_argument('-crlf', help='Scan CRLF Injection.',action='store_true', dest='crlf')
parser.add_argument('-p', help='Use payloads file.',dest="payload", default="text/payloads.txt")
parser.add_argument('--proxy', help='use proxy',action='store_true', dest='proxy')
parser.add_argument('--wayback', help='fetch URLs from waybackmachine',action="store_true", dest='waybacks')
args = parser.parse_args()

url = args.url


if ((args.payload != "text/payloads.txt") and (args.crlf or args.waybacks)):
    print(f"{bold}{red} '-p' can't be used with '-crlf' or '--wayback'{reset}")
    quit()

if not (args.url or args.path):
    print(f"{orange}No arguments, Run -h for help{reset}")

if not args.crlf and not args.waybacks:
    try:
        file = open(args.payload, encoding='utf-8').read().splitlines()
    except FileNotFoundError:
        print(f"{bold}{red}Payload file not found{reset}")
        exit()

if args.path:
    try:
        urls = open(args.path, encoding='utf-8').read().splitlines()
    except FileNotFoundError:
        print(f"{bold}{red}Target file not found{reset}")
        quit()


def analyze(url):
    multiTestCall = multitest(url, file)
    print(f'{bold}{orange}[~] Payload Type :{reset}{blue} Infusing payloads\n{reset}')
    if type(multiTestCall) == tuple:
        for params in multiTestCall[0]:
            testingBreak = request(multiTestCall[1], params)
            if testingBreak:
                break
    else:
        for url in multiTestCall:
            testingBreak = request(url)
            if testingBreak:
                break

def request(URI, params=''):
    try:
        page = requesterFunc(URI, args.proxy, params)
    except requests.exceptions.Timeout:
        print(f"[Timeout] {url}")
        return True
    except requests.exceptions.ConnectionError:
        print(f"{bold}{red}Connection Error{reset}")
        return True

    funcBreak = check(page, page.request.url)
    if funcBreak:
        return True


def check(requestsObjectVar, finalURL):
    payload = "|".join([re.escape(i) for i in file])
    redirectCodes = [red for red in range(300, 311, 1)]
    errorCodes = [error for error in range(400, 411, 1)]
    soup = BeautifulSoup(requestsObjectVar.text, 'html.parser')
    google = re.search(payload, str(soup.find_all("script")), re.IGNORECASE)
    metas = str(soup.find_all('meta'))
    searchMetaTagVar = re.search(payload, metas, re.IGNORECASE)

 
    escapedSourcesSinks = [re.escape(SnS) for SnS in sourcesSinks]
    sourcesMatch = list(dict.fromkeys(re.findall(
        "|".join(escapedSourcesSinks), str(soup))))

    if requestsObjectVar.status_code in redirectCodes:
        if searchMetaTagVar and "http-equiv=\"refresh\"" in metas:
            print(f"{bold}{green}Meta Tag Redirection{reset}")
            return True

        else:
            print(f"{bold}{green}[~] Header Based Redirection :{reset}{purple}{finalURL} {requestsObjectVar.headers['Location']}\n")

    elif requestsObjectVar.status_code == 200:
        if google:
            print(f"{bold}{green}[~] Javascript Based Redirection{reset}" )
            if sourcesMatch != None:
                print(f"{bold}{green}Potentially Vulnerable Source/Sink(s) Found: %s" % (" ".join(sourcesMatch)))
            return True

        if searchMetaTagVar and "http-equiv=\"refresh\"" in str(requestsObjectVar.text):
            print(f"{bold}{green}Meta Tag Redirection{reset}")
            return True

        elif "http-equiv=\"refresh\"" in str(requestsObjectVar.text) and not searchMetaTagVar:
            print(f"{bold}{red}The page is only getting refreshed.{reset}")
            return True

    elif requestsObjectVar.status_code in errorCodes:
        print(f"{bold}{red} {finalURL} {orange} {requestsObjectVar.status_code}{reset}")

    else:
        print(f"{bold}{red} Found nothing :: {finalURL}")


try:
    if args.url:
        if args.crlf and not args.waybacks:
            crlfScanFunc(url, args.proxy)

        elif args.waybacks and not args.crlf:
            print(f"{bold}{orange}Getting URLs from waybackmachine{reset}")
            getAllURLsFunc(url, "wayback_data.txt")

        elif not (args.crlf and args.waybacks):
            analyze(url)

    elif args.path:
        if args.crlf and not args.waybacks:
            for url in urls:
                print(f"{bold}{orange}Target: {url}")
                crlfScanFunc(url, args.proxy)
                print("\n")

        elif args.waybacks and not args.crlf:
            print(f"{bold}{orange}Getting URLs from waybackmachine")
            for url in urls:
                print(f"{bold}{orange}URL: {url}")
                getAllURLsFunc(url, f"wayback_{random.randint(0, 1000)}.txt")
                print("\n")

        elif not (args.crlf and args.waybacks):
            for url in urls:
                print(f"{bold}{orange}Target: {blue}{url}{reset}")
                analyze(url)
                print("\n")

except KeyboardInterrupt:
    print("\nKeyboard Interrupt Detected. Exiting...")
    exit()
