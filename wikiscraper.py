import requests
from bs4 import BeautifulSoup
import urllib

##Configuration options
wikiUrl=("wiki.factorio.com")
wikiPath=""
categoryPageTitle="Items"


def getlistofpages(wikiUrl,wikiPath,categoryPageTitle):
    correctpages=[]
    r=requests.get("http://"+wikiUrl+wikiPath+"/api.php?action=parse&format=json&page="+categoryPageTitle,verify=False)
    print "the server responded with " + r.reason
    pagejson= r.json()
    #returns list as default, get first item of list
    listofpages = pagejson['parse']['links']
    for page in listofpages:
        if categoryPageTitle not in page['*']:
            #remove any internationalised links e.g. foo/fr
            #url encode to detect page
            correctpages.append(str(urllib.quote_plus(page['*'])))
    return correctpages

def exportwikicode(code):
    with open("wikicode" + ".txt",'w') as f:
        for item in code:
            f.write(item.encode('ascii','ignore'))



listofpages=getlistofpages(wikiUrl,wikiPath,categoryPageTitle)
x=[]
concatTitles=[]

for i in range(abs(len(listofpages)/50)):
    #avoid the rate limit in the next step, group concatenated titles in groups of 50
    concatTitles.append("|".join(listofpages[i*50:i*50+50]))
print concatTitles

for pageGroup in concatTitles:
    r=requests.get("http://"+wikiUrl+wikiPath+"/api.php?action=query&prop=revisions&rvprop=content&format=json&titles="+pageGroup,verify=False)
    print ""
    try:
        # This is a ridiculous way to navigate the json tree, there must be a better way
        # Until then:
        ## By default this returns multiple queries, for multiple pages.
        ## Since only one page will be returned, but its indexed by key: pageid, get the first value 
        ## Get the most recent revision, all text
        #r.json()['query']['pages'].values()[0]['revisions'][0]['*']
        for page in r.json()['query']['pages'].values():
            x.append( page['revisions'][0]['*'])
    except:
        print "error"
exportwikicode(x)
print ""
