#!/usr/bin python3

import re
import json
import datetime
from cgitb import reset
from plugins.banner import *
from urllib.parse import unquote
from core.features import requesterFunc


dorks = [
            '.*\?next=.*',
            '.*\?url=.*',
            '.*\?target=.*',
            '.*\?rurl=.*',
            '.*\/dest=.*',
            '.*\/destination=.*',
            '.*\?redir=.*',
            '.*\?redirect_uri=.*',
            '.*\?return=.*',
            '.*\?return_path.*',
            '.*\/cgi-bin\/redirect\.cgi\?.*',
            '.*\?checkout_url=.*',
            '.*\?image_url=.*',
            '.*\/out\?.*',
            '.*\?continue=.*',
            '.*\?view=.*',
            '.*\/redirect\/.*',
            '.*\?go=.*',
            '.*\?redirect=.*',
            '.*\?externallink=.*',
            '.*\?nextURL=.*'
        ]

urls = []
matchedURLs = []
def getAllURLsFunc(url, path):

    file = open(path,"w", encoding='utf-8')
    fetcher(url)

    for url in urls:
        match = re.search("|".join(dorks), url, re.IGNORECASE)
        try:
            print(f"{bold}{green} {match.group()}{reset}")
            matchedURLs.append(match.group())
        except AttributeError:
            continue 

    if len(matchedURLs) > 0:
        for matches in matchedURLs:
            file.write(f"{matches}\n")

    else:
        print(f"{bold}{red}No URLs found.{reset}")

def fetcher(url):
        currentDate = datetime.date.today().year
        fromdate = currentDate - 2
        result = requesterFunc(f"https://web.archive.org/cdx/search/cdx?url={url}*&output=json&collapse=urlkey&filter=statuscode:200&limit=1000from={fromdate}&to={currentDate}", False)
        jsonOutput = json.loads(result.text)

        for output in range(1, 1000, 1):
            urls.append(unquote(jsonOutput[output][2]))