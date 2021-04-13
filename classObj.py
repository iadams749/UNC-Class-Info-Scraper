class ClassObj:
    def __init__(self):
        self.fullTitle = 'Class Full Title'
        self.number = 1
        self.hasHonors = False
        self.isLab = True
        self.abb = 'AAAA'
        self.rawCredits = 0.0
        self.minCredits = 0.0
        self.maxCredits = 0.0
        self.hasCreditRange = False
        self.desc = 'This is a class'
        self.genEds = []


    def setFullTitle(self, title):
        self.fullTitle = title

    def setNumber(self,num):
        self.number = num

    def setAbbreviation(self,abb):
        self.abb = abb

    #Sets the raw credits and determines in the min and max credits
    def setRawCredits(self,num):
        self.rawCredits = num

        if(num/10.0 <= 1.0 and num % 0.5 == 0):
            self.hasCreditRange = False
            self.maxCredits = num
            self.minCredits = num
            return

        if(num % 0.5 != 0):
            number1 = str(num)
            min = float(number1[:3])
            max = float(number1[3:])
            self.minCredits = min
            self.maxCredits = max
            self.hasCreditRange = True
            return

        if(str(num)[2] == '.'):
            number1 = str(num)
            min = float(number1[:1])
            max = float(number1[1:])
            self.minCredits = min
            self.maxCredits = max
            self.hasCreditRange = True
            return

        number = str(num)
        min = float(number[:1])
        max = float(number[1:])

        self.minCredits = min
        self.maxCredits = max
        self.hasCreditRange = True

    def setDesc(self,desc):

        #Make sure all of the sentences are seperated and pretty
        descParts = desc.split('.')
        descParts.remove(descParts[-1])

        desc = ''

        for d in descParts:
            desc = desc+(d.strip())+'. '

        descParts2 = desc.split('eS')

        if(len(descParts2) > 1):
            desc = descParts2[0]+'e. S'+descParts2[1]

        self.desc = desc

        descParts3 = desc.split('Gen Ed:')
        if(len(descParts3) > 1):
            parts = descParts3[1].split('.')
            eds = parts[0]
            edsList = eds.split(',')
            for e in edsList:
                self.genEds.append(e.strip())




    def setRequisites(self,req):
        self.reqisites = req

    def setGenEds(self,gens):
        self.genEds = gens

    def setHasCreditRange(self,bool):
        self.hasCreditRange = bool

    def __str__(self):
        return f'{self.abb} {self.number} {self.fullTitle} {self.minCredits} {self.maxCredits} \n {self.desc} \n {self.genEds}'