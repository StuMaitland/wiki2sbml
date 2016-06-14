import requests
from bs4 import BeautifulSoup
import urllib

##Configuration options
wikiUrl=("wiki.factorio.com")
wikiPath=""
categoryPageTitle="Items"


def getlistofpages(wikiUrl,wikiPath,categoryPageTitle):

    r=requests.get("http://"+wikiUrl+wikiPath+"/api.php?action=parse&format=json&page="+categoryPageTitle,verify=False)
    print "the server responded with " + r.reason
    pagejson= r.json()
    #returns list as default, get first item of list
    listofpages = pagejson['parse']['links']
    for page in listofpages:
        if categoryPageTitle in page['*']:
            #remove any internationalised links e.g. foo/fr
            page['*']=""
        else:
            #url encode to detect page
            page['*']=str(urllib.quote_plus(page['*']))

    return listofpages

def exportwikicode(code):
    with open("wikicode" + ".txt",'w') as f:
        for item in code:
            f.write(item.encode('ascii','ignore'))



listofpages=getlistofpages(wikiUrl,wikiPath,categoryPageTitle)
x=[]

for page in listofpages:
    r=requests.get("http://"+wikiUrl+wikiPath+"/api.php?action=query&prop=revisions&rvprop=content&format=json&titles="+page['*'],verify=False)
    print page['*']
    try:
        # This is a ridiculous way to navigate the json tree, there must be a better way
        # Until then:
        ## By default this returns multiple queries, for multiple pages.
        ## Since only one page will be returned, but its indexed by key: pageid, get the first value 
        ## Get the most recent revision, all text
        x.append( r.json()['query']['pages'].values()[0]['revisions'][0]['*'])
    except:
        continue
exportwikicode(x)
print ""
