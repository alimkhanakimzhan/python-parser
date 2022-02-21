from selenium import webdriver
import time
import csv
import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
)

mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE aitu_students")
selecteddb=mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="aitu_students"
)

mycursor = selecteddb.cursor()
#mycursor.execute("CREATE TABLE students_db (name varchar(255), surname varchar(255), patronymic varchar(255), IIN varchar(12), gpa float, course int(11))")


fDELAY = 10
sDELAY = 10
studDELAY = 5
COUNT = 551
start_index = 480
COURSE = 2

log = 'user' #user`s login
passw = 'password' #user`s password


driver = webdriver.Chrome('./chromedriver')
driver.get('https://platonus.astanait.edu.kz/index')

driver.find_element_by_id("login_input").send_keys(log)
driver.find_element_by_id("pass_input").send_keys(passw)
driver.find_element_by_id("Submit1").click() #
time.sleep(fDELAY)

driver.get(f'https://platonus.astanait.edu.kz/template.html#/students?page=0&countInPart={COUNT}&facultyID=0&gender=0&year=0&cafedraID=0&professionID=0&specializationID=0&sGroupID=0&course={COURSE}&studyFormID=0&departmentID=0&state=1&academic_mobility=0&studyLanguageID=0&paymentFormID=0&militaryID=0&conditionally_enrolled=2&degreeID=0&grantTypeID=0&professionTypeID=0&centerTrainingDirectionsID=0')
time.sleep(sDELAY)
links=driver.find_elements_by_tag_name("a")
student_links=[]
for lnk in links:
    if lnk.get_attribute('href') != None:
        if  lnk.get_attribute('href').startswith('https://platonus.astanait.edu.kz/template.html#/student/'):
            student_links.append(lnk.get_attribute('href'))

for n, s in enumerate(student_links):
    if n>start_index:
        driver.get(s)
        time.sleep(studDELAY)
        try:
            student = []
            student.append(driver.find_element_by_tag_name("h3").text.split(' (GPA (за весь период обучения): ')[0].split(' ')[0])
            student.append(driver.find_element_by_tag_name("h3").text.split(' (GPA (за весь период обучения): ')[0].split(' ')[1])
            try:
                student.append(driver.find_element_by_tag_name("h3").text.split(' (GPA (за весь период обучения): ')[0].split(' ')[2])
            except:
                student.append("")
            student.append(driver.find_element_by_tag_name("h3").text.split(' (GPA (за весь период обучения): ')[1].split(', Статус: Обучающийся)')[0])
            student.append(driver.find_element_by_name('iin').get_attribute('value'))
            student.append(driver.find_element_by_name('birthDate').get_attribute('value'))
            try:
                mycursor.execute ("insert into students_db (name, surname, patronymic, IIN, gpa, course) values ('{name}','{surname}','{patronymic}','{IIN}', '{gpa}','{course}')".format(name=student[1], surname=student[0], patronymic=student[2], IIN=student[4], gpa=student[3], course=COURSE))
                selecteddb.commit()
                print(n, " is ", student)
            except:
                print(student, ' already exists in table')
        except:
            print('Cathed exception')
