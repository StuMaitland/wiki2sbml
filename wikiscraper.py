import mwclient
import requests
from bs4 import BeautifulSoup

##Configuration options
wikiUrl=("wiki.factorio.com")
wikiPath=""
categoryPageTitle="Items"

def getlistoflinks(wikiUrl,wikiPath,categoryPageTitle):
    r=requests.get("http://"+wikiUrl+wikiPath+"/api.php?action=parse&format=json&page="+categoryPageTitle,verify=False)
    print "the server responded with " + r.reason
    pagejson= r.json()
    #returns list as default, get first item of list
    listoflinks = pagejson['parse']['links']

    return listoflinks

listoflinks=getlistoflinks(wikiUrl,wikiPath,categoryPageTitle)