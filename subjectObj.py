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

    def getClasses(self):

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
            abb = courseBlockTitleParts[0].split('\xa0')[0]

            #Holds the number for the class
            num = courseBlockTitleParts[0].split('\xa0')[1]


            try:
                num = num.replace("H","")
                num = num.replace("L", "")
                num = num.replace("B", "")
                num = num.replace("A", "")
                num = num.replace("C", "")
                num = num.replace("I", "")
                num = num.replace("P", "")

            except:
                print('Missing H/L Argument')

            try:
                num = int(num)
            except:
                num = 94
                print('We got a problem aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')

            #Holds the full title for the class
            fullTitle = courseBlockTitleParts[1].strip()

            #Holds the raw credits for the class
            rawCreds = float(courseBlockTitleParts[-2].strip(string.ascii_letters).replace('-',''))

            #Gets all of the course descriptions
            courseBlockDesc = cb.find('p',class_='courseblockdesc')
            #print(courseBlockDesc.text.strip())

            #Holds the description of the class
            desc = courseBlockDesc.text.strip().replace('Grading status: Letter grade','')

            #Creates the classObj for each class
            a = ClassObj()
            a.setRawCredits(rawCreds)
            a.setAbbreviation(abb)
            a.setNumber(num)
            a.setFullTitle(fullTitle)
            print(a)


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

        #halfCreditSubjects = ['BUSI', 'BBSP', 'AMST', 'BIOS', 'CBPH', 'CHEM', 'PLAN', 'COMP', 'CMPL', 'DRAM', 'ENVR', 'EPID']

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