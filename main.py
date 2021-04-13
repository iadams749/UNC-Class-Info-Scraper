from bs4 import BeautifulSoup
from subjectObj import *
from classObj import *
import requests
import csv


source = requests.get('https://catalog.unc.edu/courses/').text

soup = BeautifulSoup(source, 'lxml')

#Creating the xml file for the subjects and abbreviations to be written to
csv_file = open('cms_subject_scrape.csv', 'w')

csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Full name','Abbreviation'])

test = soup.find('div', id='atozindex')



subjects = []

#Creating the subjects and writing their name and abbreviation to an xml file
for list in test.find_all('ul'):
    for line in list.find_all('li'):
        subjects.append(SubjectObj(line.a.text.split('(')[0],line.a.text.split('(')[1].split(")")[0],f'{line.a.get("href").split("/")[2]}/'))
        csv_writer.writerow([line.a.text,line.a.text.split('(')[1].split(")")[0]])

csv_file.close()

csv_file1 = open('cms_class_scrape.csv', 'w')

csv_writer = csv.writer(csv_file1)
csv_writer.writerow(['Abbreviation','Number','Full Title','Raw Credits','Min Credits','Max Credits','Has Credit Range','Gen-Eds','Full Description'])

# subjects[0].getClasses(csv_writer)
# csv_writer.writerow([])
# subjects[1].getClasses(csv_writer)
# csv_writer.writerow([])
# subjects[2].getClasses(csv_writer)
# csv_writer.writerow([])

for sub in subjects:
    sub.getClasses(csv_writer)
    csv_writer.writerow([])


csv_file1.close()