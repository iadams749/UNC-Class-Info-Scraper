from bs4 import BeautifulSoup
from subjectObj import *
from classObj import *
import requests
import csv


source = requests.get('https://catalog.unc.edu/courses/').text

soup = BeautifulSoup(source, 'lxml')

# csv_file = open('cms_scrape.csv', 'w')
#
# csv_writer = csv.writer(csv_file)
# csv_writer.writerow(['full name','abbreviation'])

test = soup.find('div', id='atozindex')



subjects = []

for list in test.find_all('ul'):
    for line in list.find_all('li'):
        subjects.append(SubjectObj(line.a.text.split('(')[0],line.a.text.split('(')[1].split(")")[0],f'{line.a.get("href").split("/")[2]}/'))
        #csv_writer.writerow([line.a.text,line.a.text.split('(')[1].split(")")[0]])

# subjects[65].getClasses()

for sub in subjects:
    sub.getClasses()
