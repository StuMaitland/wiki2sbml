import requests
from bs4 import BeautifulSoup
import urllib

##Configuration options
wikiUrl = ("wiki.factorio.com")
wikiPath = ""
categoryPageTitle = "Items"


class CraftRecipe():
    def __init__(self, title):
        self.title = title
        self.time = 0
        self.ingredients = {}
        self.wikientry = ""

    def makerecipetext(self):
        string = ""
        for key, value in self.ingredients.iteritems():
            string = string + str(value) + key.lower() + "+"
        string = string[:-1]  # Remove last superfluous + sign
        string = string + "->" + self.title.lower()
        string = string.replace(" ", "")
        return string


def getlistofpages(wikiUrl, wikiPath, categoryPageTitle):
    correctpages = []
    r = requests.get("http://" + wikiUrl + wikiPath + "/api.php?action=parse&format=json&page=" + categoryPageTitle,
                     verify=False)
    print("the server responded with " + r.reason)
    pagejson = r.json()
    # returns list as default, get first item of list
    listofpages = pagejson['parse']['links']
    for page in listofpages:
        outputtitle = ""
        if categoryPageTitle not in page['*']:
            # remove any internationalised links e.g. foo/fr

            outputtitle = str(page['*'])
            # Title Case
            # outputtitle=outputtitle.title()
            outputtitle = outputtitle.replace(" ", "+")
            # url encode to detect page
            # outputtitle=urllib.quote_plus(outputtitle)
            correctpages.append(outputtitle)
    return correctpages


def extractwikicode(listofpages):
    wikicode = []
    concatTitles = []
    orderedtitles = []

    for i in range(abs(len(listofpages) / 50)):
        # avoid the rate limit in the next step, group concatenated titles in groups of 50
        thisgroupoftitles = listofpages[i * 50:i * 50 + 50]
        concatTitles.append("|".join(thisgroupoftitles))

    for pageGroup in concatTitles:
        print(concatTitles)
        r = requests.get(
            "http://" + wikiUrl + wikiPath + "/api.php?action=query&prop=revisions&rvprop=content&format=json&titles=" + pageGroup,
            verify=False)

        # This is a ridiculous way to navigate the json tree, there must be a better way
        # Until then:
        ## By default this returns multiple queries, for multiple pages.
        ## Iterate over each page returned in the result
        for page, title in zip(r.json()['query']['pages'].values(), thisgroupoftitles):
            # Get the most recent revision, all text
            try:
                wikicode.append(page['revisions'][0]['*'].encode('ascii', 'ignore'))
                orderedtitles.append(page['title'])
            except:
                print(page, page['title'])

    return wikicode, orderedtitles


def exportwikicode(code, pagetitles):
    with open("wikicode" + ".txt", 'w') as f:
        for item, title in zip(code, pagetitles):
            f.write(title.encode('ascii', 'ignore') + "\n")
            f.write(item.encode('ascii', 'ignore'))


def extractrecipe(page, title):
    x = CraftRecipe(title)
    r = page.split("\n")
    print(r)
    print("")
    for line in r:
        if "input" in line:
            print("input in line")
            x.wikientry = line
            try:
                formula = line.split("=")[1]
            except:
                print("error at: " + title + ". The content was: " + line)
            for unit in formula.split("+"):
                if "time" in unit.lower():
                    try:
                        x.time = int(unit.split(",")[1])
                    except:
                        x.time = 1
                else:
                    try:
                        x.ingredients[unit.split(",")[0]] = unit.split(",")[1]
                    except:
                        # single ingredient amount is not split by ","
                        x.ingredients[unit.split(",")[0]] = 1
        if x.ingredients:
            return x
        else:
            return x


listofpages = getlistofpages(wikiUrl, wikiPath, categoryPageTitle)

wikicode, orderedtitles = extractwikicode(listofpages)

allitems = []

for page, title in zip(wikicode, orderedtitles):
    allitems.append(extractrecipe(page, title))
badtitles = []
for item in allitems:
    if item.wikientry == "":
        # Change Title Case to First letter case
        badtitles.append(item.title.lower().capitalize().replace(" ", "+"))

wikicode, orderedtitles = extractwikicode(badtitles)
for page, title in zip(wikicode, orderedtitles):
    allitems.append(extractrecipe(page, title))

for item in allitems:
    print()
    item.makerecipetext()
print("")
exportwikicode(wikicode, orderedtitles)