import requests
from bs4 import BeautifulSoup
import urllib
import math

##Configuration options
wikiUrl = ("wiki.factorio.com")
wikiPath = ""
categoryPageTitle = "Items"

modelTitle = "Factorio End Game"
richness = 200
startParameters = {
    "coal" : 100000000 * richness,
    "ironore" : 100000000 * richness,
    "copperore" : 100000000 * richness,
    "oil" : 100000000 * richness,
    "stone" : 100000000 * richness,
    "water" : 100000000000000 * richness,
    "wood" : 10000000000 * richness
}


class CraftRecipe():
    def __init__(self, title):
        self.title = title
        self.time = 0
        self.ingredients = {}
        self.wikientry = ""

    def makeRecipeText(self):

        #Recipe is made up of 3 parts:
        #   Title line
        #   Reaction specification
        #   Rate law
        try:
            titleLine = '@r={0}Crafting "{1} Crafting"'.format(self.title.replace(" ", ""), self.title)
        except:
            print(self.title)
        reaction =""
        for key, value in self.ingredients.items():
            sanitizedKey=""
            sanitizedKey = key.lower().replace(" ", "").replace("-","")
            # Add the item prefixed by its stoichiometry i.e. 2steel
            if sanitizedKey:
                reaction += str(value).replace(" ", "") + sanitizedKey + " + "
        reaction = reaction[:-3]  # Remove last superfluous + sign
        reaction += " -> " + self.title.lower().replace(" ", "")
        reaction = reaction.replace("\n","")
        reaction = reaction.replace("\\n", "") #Escaped characters \\n sneak in from the wiki entry. Remove those

        if self.time > 0:
            rateLaw = "rate{0} : rate{0}={1}".format(self.title.replace(" ", ""),(1.0/self.time))

            recipe= titleLine + "\n" + reaction + "\n" + rateLaw

            return recipe
        else:
            return ""
            #return "#Error with recipe: " + self.title + " : " + self.wikientry + str(len(self.wikientry))


def GetListOfPages(wikiUrl, wikiPath, categoryPageTitle):
    correctPages = []
    r = requests.get("http://" + wikiUrl + wikiPath + "/api.php?action=parse&format=json&page=" + categoryPageTitle,
                     verify=False)
    print("the server responded with " + r.reason)
    pagejson = r.json()
    # returns list as default, get first item of list
    listOfPages = pagejson['parse']['links']
    for page in listOfPages:
        outputTitle = ""
        if categoryPageTitle not in page['*']:
            # remove any internationalised links e.g. foo/fr

            outputTitle = str(page['*'])
            # Title Case
            outputTitle = outputTitle.replace(" ", "+")
            # url encode to detect page
            correctPages.append(outputTitle.lower())
    return correctPages


def extractWikiCode(listofpages):
    for page in listofpages:
        page.replace(" ", "+")
    wikiCode = []
    concatTitles = []
    orderedTitles = []

    # avoid the rate limit in the next step, group concatenated titles in groups of 50
    if len(listofpages)>1:
        for i in range(math.ceil(len(listofpages) / 50)):
            thisGroupOfTitles = listofpages[i * 50:i * 50 + 50]
            concatTitles.append("|".join(thisGroupOfTitles))

    else:
        concatTitles = listofpages

    for pageGroup in concatTitles:
        r = requests.get(
            "http://" + wikiUrl + wikiPath + "/api.php?action=query&prop=revisions&rvprop=content&format=json&titles=" + pageGroup,
            verify=False)
        print(pageGroup)

        # This is a ridiculous way to navigate the json tree, there must be a better way
        # Until then:
        ## By default this returns multiple queries, for multiple pages.
        ## Iterate over each page returned in the result
        for page, title in zip(r.json()['query']['pages'].values(), thisGroupOfTitles):
            # Get the most recent revision, all text
            try:
                wikiCode.append(page['revisions'][0]['*'])
                orderedTitles.append(page['title'])
            except:
                print("error1: ", page, page['title'])

    return wikiCode, orderedTitles


def exportWikiCode(code, pagetitles):
    with open("wikicode" + ".txt", 'w') as f:
        for item, title in zip(code, pagetitles):
            f.write(str(title) + "\n")
            f.write(str(item))


def extractRecipe(page, title):
    newItem = CraftRecipe(title)
    stringPage=str(page)
    r = stringPage.split("|")
    for section in r:
        if section[-2:] == "\n":
            section = section[:-2]
        if "input" in section:
            newItem.wikientry = section
            try:
                formula = section.split("=")[1]
            except:
                formula=""
                print("error2: " + section)

            for unit in formula.split("+"):
                if "time" in unit.lower():

                    try:
                        newItem.time = int(unit.split(",")[1])
                    except:
                        newItem.time = 1
                else:
                    try:
                        newItem.ingredients[unit.split(",")[0]] = unit.split(",")[1]

                    except:
                        # single ingredient amount is not split by ","
                        newItem.ingredients[unit.split(",")[0]] = 1

    return newItem


ListOfPages = GetListOfPages(wikiUrl, wikiPath, categoryPageTitle)

WikiCode, orderedTitles = extractWikiCode(ListOfPages)

AllTheItems = []

for page, title in zip(WikiCode, orderedTitles):
    AllTheItems.append(extractRecipe(page, title))
badtitles = []
for item in AllTheItems:
    if item.wikientry == "":
        # Change Title Case to First letter case
        #print(item.title)
        badtitles.append(item.title.title().replace(" ", "+"))

wikiCode, orderedTitles = extractWikiCode(badtitles)
for page, title in zip(wikiCode, orderedTitles):
    AllTheItems.append(extractRecipe(page, title))

completeRecipes=[]
for item in AllTheItems:
    completeRecipes.append(item.makeRecipeText())

with open("misc.mod") as myfile:
    content = myfile.read()


#Clear the file before appending all the recipes and other model information
with open ("recipes.mod", "w") as myfile:
    pass
    myfile.write('@model:3.1.1={0} "{1}" \n'.format(modelTitle.replace(" ", ""),modelTitle))
    myfile.write('@compartments\n   cell=1\n')

    myfile.write('@species\n')
    for key, value in startParameters.items():
        myfile.write('  cell:{0}={1}\n'.format(key,value))

    myfile.write('@reactions\n')
    myfile.write(content)


for reaction in completeRecipes:
    with open("recipes.mod", 'a') as myfile:
        myfile.write(reaction)
        myfile.write("\n\n")

