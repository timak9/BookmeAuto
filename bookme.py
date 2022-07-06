from datetime import datetime,timedelta
from time import sleep
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


def get_text(driver, element):
    return driver.execute_script("""
    return jQuery(arguments[0]).contents().filter(function() {
        return this.nodeType == Node.TEXT_NODE;
    }).text();
    """, element)

options = Options()
options.add_argument(r"--user-data-dir=C:/webdrivers")
options.add_argument(r'--profile-directory=Profile 3')
#driver = webdriver.Chrome(executable_path=r'C:/webdrivers/chromedriver.exe', options=options)

#format of firstHour : 10:30
#format of the day: YYYY-MM-DD
#rid the number of the room
#sid the number of the building
#For the both need to take in the url of the reservation in bookme

def firstReservation(options,day,firstHour,rid,sid):
    driver = webdriver.Chrome(executable_path=r'C:/webdrivers/chromedriver.exe', options=options)
    hour = firstHour.split(":")[0]
    minute = firstHour.split(":")[1]
    timeEnd = newHour(firstHour)
    timeEnd = newHour(timeEnd)
    hourEnd = timeEnd.split(":")[0]
    minuteEnd = timeEnd.split(":")[1]
    driver.get("https://bookme.technion.ac.il/booked/Web/reservation.php?rid="+rid+"&sid="+sid+"&rd="+day+"&sd="+day+"%20"+hour+"%3A"+minute+"%3A00&ed="+day+"%20"+hourEnd+"%3A"+minuteEnd+"%3A00")
    sleep(5)
    element = driver.find_element(By.ID,"reservationTitle")
    element2 = driver.find_element(By.CLASS_NAME,"save")
    element.send_keys("automatic")
    sleep(3)
    element2.click()
    sleep(5)
    elememt3 = driver.find_element(By.ID,"reference-number")
    newId = get_text(driver,elememt3).split(" ")[-1]
    sleep(3)
    driver.quit()
    return "https://bookme.technion.ac.il/booked/Web/reservation.php?rn="+newId

def newHour(lastHour):
    hourInt = int(lastHour.split(":")[0])
    minutesInt = int(lastHour.split(":")[1])
    if (minutesInt>0):
        hourInt+=1
        minutesInt=0
    else:
        minutesInt+=30
    if minutesInt == 0:
        minutes = "00"
    else:
        minutes = "30"
    if hourInt>10:
        hour = str(hourInt)
    else:
        hour = "0"+str(hourInt)
    return hour+":"+minutes

def reservationRepeat(options,url,hour):
    driver = webdriver.Chrome(executable_path=r'C:/webdrivers/chromedriver.exe', options=options)
    driver.get(url)
    sleep(5)
    element = driver.find_element(By.ID,"EndPeriod")
    select = Select(element)
    print("test"+hour)
    select.select_by_value(hour+":00")
    sleep(5)
    element2 = driver.find_element(By.CLASS_NAME,"save")
    element2.click()
    driver.quit()

def doOneReservation(options,day,firstHour,rid,sid):
    time1 = datetime.strptime(firstHour+' '+day, "%H:%M %Y-%m-%d")
    print(time1 - datetime.now())
    while (time1 - datetime.now() >  timedelta(days=5, hours=23)):
        print(time1 - datetime.now())
        sleep(10)
    newUrl = firstReservation(options, day, firstHour, rid, sid)
    firstHour = newHour(firstHour)
    firstHour = newHour(firstHour)
    for _ in range(4):
        sleep(1800)
        firstHour = newHour(firstHour)
        reservationRepeat(options, newUrl, firstHour)

def doReservation(options,numberRepetition=1):
    day = input("Insert a day, in format YYYY-MM-DD")
    firstHour = input("Insert a hour in format HH:MM")
    rid = input("insert the rid (write in the url, in format XXXX")
    sid = input("insert the sid (write in the url, in format XXX")
    for _ in range(numberRepetition):
        doOneReservation(options,day,firstHour,rid,sid)
        time1 = datetime.strptime(day, "%Y-%m-%d")
        time1 += timedelta(days=1)
        day = time1.strftime("%Y-%m-%d")

doReservation(options)