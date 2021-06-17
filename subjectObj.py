import string

from bs4 import BeautifulSoup
from classObj import *
import requests

class SubjectObj:

    #Holds to top level URL
    mainURL = 'https://catalog.unc.edu/courses/'

    def __init__(self, name, abb, href):
        self.name = name
        self.abbreviation = abb
        self.href = href
        self.classes = []

    def __str__(self):
        return f'{self.name}({self.abbreviation}) {self.href}'

    def getClasses(self,csv_writer):

        #Opens the subject page and gets the soup from it
        newUrl = self.mainURL + self.href
        page = requests.get(newUrl).text
        subjectHTML = BeautifulSoup(page,'lxml')

        #List holding the course blocks
        courseblocks = []
        for cb in subjectHTML.find_all('div', class_='courseblock'):
            courseblocks.append(cb)


        #Loop that creates the classObj's
        for cb in courseblocks:
            courseBlockTitle = cb.find('p',class_='courseblocktitle').strong.text.strip()
            courseBlockTitleParts = courseBlockTitle.split('.')

            self.prepTitleBlock(courseBlockTitleParts)

            #Holds the abbreviation for the class
            abb = self.getGetAbb(courseBlockTitleParts)

            #Holds the number for the class
            num = self.getNum(courseBlockTitleParts)

            #Holds the full title for the class
            fullTitle = self.getFullTitle(courseBlockTitleParts)

            #Holds the raw credits for the class
            rawCreds = self.getRawCreds(courseBlockTitleParts)

            #Gets all of the course descriptions
            courseBlockDesc = cb.find('p',class_='courseblockdesc')

            #Holds the description of the class
            rawDesc = self.getRawClassDesc(courseBlockDesc)

            #Creates the classObj for each class
            a = ClassObj()
            a.setRawCredits(rawCreds)
            a.setAbbreviation(abb)
            a.setNumber(num)
            a.setFullTitle(fullTitle)
            a.setDesc(rawDesc)
            self.csvWrite(a,csv_writer)
            #print(a)



    #Preps the courseblockTitleParts array and handles the various formats in the titles of the classes
    def prepTitleBlock(self,courseBlockTitleParts):

        # Handling the M.F.A Classes
        if (len(courseBlockTitleParts) == 7):
            courseBlockTitleParts[
                1] = f'{courseBlockTitleParts[1]}.{courseBlockTitleParts[2]}.{courseBlockTitleParts[3]}.{courseBlockTitleParts[4]}'
            courseBlockTitleParts.remove(courseBlockTitleParts[2])
            courseBlockTitleParts.remove(courseBlockTitleParts[2])
            courseBlockTitleParts.remove(courseBlockTitleParts[2])

        # Handling of the classes with M.A. and Ph.D in their titles
        if (len(courseBlockTitleParts) == 6 and (courseBlockTitleParts[1] == '  M' or courseBlockTitleParts[2] == 'D')):
            courseBlockTitleParts[
                1] = f'{courseBlockTitleParts[1]}.{courseBlockTitleParts[2]}. {courseBlockTitleParts[3]}'
            courseBlockTitleParts.remove(courseBlockTitleParts[2])
            courseBlockTitleParts.remove(courseBlockTitleParts[2])

        subjectsWithPeriodInTitle = ['ENGL', 'ARTH', 'GERM', 'HPM', 'HIST', 'INLS']

        #Handling of the classes with a period in the class title
        if (len(courseBlockTitleParts) == 5 and (courseBlockTitleParts[0][:4] in subjectsWithPeriodInTitle or courseBlockTitleParts[0][:3] in subjectsWithPeriodInTitle) and not('  0' in courseBlockTitleParts or '  1' in courseBlockTitleParts)):
            courseBlockTitleParts[1] = f'{courseBlockTitleParts[1]}.{courseBlockTitleParts[2]}'
            courseBlockTitleParts.remove(courseBlockTitleParts[2])

        # Handling of the classes with half credit-hour classes
        if (len(courseBlockTitleParts) == 5 and (courseBlockTitleParts[0][:4] != 'ARCH')):
            courseBlockTitleParts[-2] = f'{courseBlockTitleParts[-3]}.{courseBlockTitleParts[-2]}'
            courseBlockTitleParts.remove(courseBlockTitleParts[-3])

        # Handling of the first weird ARCH class
        if (len(courseBlockTitleParts) == 5):
            courseBlockTitleParts[0] = courseBlockTitleParts[0] + courseBlockTitleParts[1]
            courseBlockTitleParts.remove(courseBlockTitleParts[1])

    #Returns the abbreviation of the subject
    def getGetAbb(self,courseBlockTitleParts):
        return courseBlockTitleParts[0].split('\xa0')[0]

    #Returns the number of the class
    def getNum(self,courseBlockTitleParts):
        num = courseBlockTitleParts[0].split('\xa0')[1]

        # try:
        #     num = num.replace("H", "")
        #     num = num.replace("L", "")
        #     num = num.replace("B", "")
        #     num = num.replace("A", "")
        #     num = num.replace("C", "")
        #     num = num.replace("I", "")
        #     num = num.replace("P", "")
        #
        # except:
        #     print('Missing H/L Argument')
        #
        # try:
        #     num = int(num)
        # except:
        #     num = 0
        #     print('Problem with num assignment')

        return num

    #Returns the full title of the class
    def getFullTitle(self,courseBlockTitleParts):
        return courseBlockTitleParts[1].strip()

    #Returns the raw credits string of the class
    def getRawCreds(self,courseBlockTitleParts):
        return float(courseBlockTitleParts[-2].strip(string.ascii_letters).replace('-',''))

    #Returns the class description
    def getRawClassDesc(self,courseBlockDesc):
        return courseBlockDesc.text.strip()

    def csvWrite(self,a,csv_writer):
        csv_writer.writerow([a.abb,a.number,a.fullTitle,a.rawCredits,a.minCredits,a.maxCredits,a.hasCreditRange,a.genEds,a.desc])
