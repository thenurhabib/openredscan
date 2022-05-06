#!/usr/bin python3

from ssl import Purpose


reset='\033[0m'
bold='\033[01m'
disable='\033[02m'
underline='\033[04m'
reverse='\033[07m'
strikethrough='\033[09m'
invisible='\033[08m'
black='\033[30m'
red='\033[31m'
green='\033[32m'
orange='\033[33m'
blue='\033[34m'
purple='\033[35m'
cyan='\033[36m'
lightgrey='\033[37m'
darkgrey='\033[90m'
lightred='\033[91m'
lightgreen='\033[92m'
yellow='\033[93m'
lightblue='\033[94m'
pink='\033[95m'
lightcyan='\033[96m'

def bannerFunc():
    print(f"""{bold}{red}

 __   __   ___       __   ___  __   __   __            
/  \ |__) |__  |\ | |__) |__  |  \ /__` /  `  /\  |\ | 
\__/ |    |___ | \| |  \ |___ |__/ .__/ \__, /~~\ | \|
{purple}
Multifunctional Open Redirection Vulnerability Scanner
{reset}
~ by {cyan}{bold}@thenurhabib{reset}\n""")

