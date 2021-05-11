# WebScraping for CoWin Website, using chrome driver.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from time import sleep, time
from pathlib import Path
from playsound import playsound
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


isOneTimeSetupComplete = True
state_identifier = "mat-option-36"
district_identifier = "mat-option-53"
check_in_x_seconds = 20
your_phone_number = "9830212422"

userState = input("Your State: ").lower()
userDistrict = input("Your District: ").lower()

def setup():
    print("Warning: Application is still in beta, if any errors occur report in github page")
    # file_settings = Path("settings.txt")
    if not isOneTimeSetupComplete:
        print("Error: Application not setup correctly!")
        quit()
    if os.path.exists("./settings.txt"):
        with open('settings.txt', 'r') as file:
            email = file.readlines()
    else:
        print("\nWelcome, this application is only for educational purposes and should not be misused to hamper the services of Co-Win website.\nFurther more, I am not responsible for any problem if to occur on your behalf of running this application!\n\n")
        email = input("\nPlease type your e-mail:  ")
        with open('settings.txt', 'w') as file:
            file.write(email)
    
    return email

def select_state(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(ec.presence_of_element_located((By.ID, "mat-select-0")))
    driver.find_element_by_id('mat-select-0').click()
    # state = wait.until(ec.presence_of_element_located((By.XPATH, f"//mat-option[@id='{state_identifier}']")))
    # state.click()
    wait.until(ec.presence_of_element_located((By.ID, "cdk-overlay-0")))
    stateList = driver.find_elements_by_xpath("//div[@id='cdk-overlay-0']/div/div/mat-option/span")
    for state in stateList:
        if state.text.lower() == userState.lower():
            state.click()
            break
    return

def select_district(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(ec.presence_of_element_located((By.ID, "mat-select-2")))
    driver.find_element_by_id('mat-select-2').click()
    # district = wait.until(ec.presence_of_element_located((By.XPATH, f"//mat-option[@id='{district_identifier}']")))
    # district.click()
    wait.until(ec.presence_of_element_located((By.ID, "cdk-overlay-1")))
    districtList = driver.find_elements_by_xpath("//div[@id='cdk-overlay-1']/div/div/mat-option/span")
    for district in districtList:
        if district.text.lower() == userDistrict.lower():
            district.click()
            break
    return

def find_vaccines(driver):
    wait = WebDriverWait(driver, 20)
    query = "//div[contains(@class, 'mat-main-field') and contains(@class, 'center-main-field')]/mat-selection-list/div[contains(@class, 'ng-star-inserted')]"
    vaccine_rows = wait.until(ec.presence_of_all_elements_located((By.XPATH, query)))
    all_vaccine_info = []
    for i in range(len(vaccine_rows)):
        vaccine_center = driver.find_elements_by_xpath(query)[i]
        vaccine_center_name = vaccine_center.find_elements_by_xpath("//h5[@class='center-name-title']")[i].text
        vaccine_slot_avail_ul = vaccine_center.find_elements_by_xpath("//ul[@class='slot-available-wrap']")[i]
        vaccine_slot_li = vaccine_slot_avail_ul.find_elements_by_tag_name("li")
        vaccine_info_about_slots = []
        for vaccine_slot in vaccine_slot_li:
            vaccine_info_about_slots.append(vaccine_slot.find_element_by_tag_name("a").text)

        final_info_grabbed = f"      >>> Vaccine Centre: {vaccine_center_name} -> Info(+7) "
        for vaccine_slot in vaccine_info_about_slots:
            final_info_grabbed += vaccine_slot + " "
        all_vaccine_info.append((vaccine_center_name, vaccine_info_about_slots))
        print(final_info_grabbed)
    return all_vaccine_info

def check_vaccines(driver, vaccine_info):
    list_of_vaccines = []
    for i in range(len(vaccine_info)):
        for x in range(len(vaccine_info[i][1])):
            vaccine_info_fetched_text = vaccine_info[i][1][x]
            txt = "" + vaccine_info_fetched_text
            if vaccine_info_fetched_text == "NA" or vaccine_info_fetched_text == "Booked":
                continue
            elif txt.isnumeric():
                list_of_vaccines.append(i)
                break;
    return list_of_vaccines

def PlayAlarm():
    if (vaccine_found == True):
        playsound('./alarm.mp3')
        while (True):
            sleep(0.17)
            playsound('./alarm.mp3')

email = setup()
sleep(1)

vaccine_found = False

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# options.add_argument("--user-data-dir=C:/users/Documents/CoWinBot")
options.add_argument("--profile-directory=Default")
# options.add_argument(r'--profile-directory="1"')
driver = webdriver.Chrome(r"./dependencies/chromedriver.exe", options=options)
driver.maximize_window
driver.get(r'https://www.cowin.gov.in/')
driver.execute_script("window.open('" + "https://messages.google.com/web/authentication" + "', '_blank')")
sleep(1)
driver.execute_script("window.open('" + "https://selfregistration.cowin.gov.in/" + "', '_blank')")
sleep(1)

def OpenMessages():
    driver.switch_to.window(driver.window_handles[2])
    print("\n>> Waiting for authentication from Google Messages")
    while(driver.current_url != r"https://messages.google.com/web/conversations"):
        print(">> Waiting for authentication from Google Messages (Retrying..)")
        sleep(10)

    return

def GetOTP():
    driver.switch_to.window(driver.window_handles[2])
    driver.get('https://messages.google.com/web/conversations')
    sleep(15)
    wait = WebDriverWait(driver, 30)
    wait.until(ec.presence_of_all_elements_located((By.TAG_NAME, r"mws-conversation-list-item")))
    msg_container = driver.find_elements_by_tag_name(r"mws-conversation-list-item")[0]
    msg_container.find_element_by_tag_name("a").click()
    query = "//div[contains(@class, 'text-msg') and contains(@class, 'ng-star-inserted')]"
    print(">> Found OTP!")
    driver.get('https://messages.google.com/web/conversations')
    wait.until(ec.presence_of_all_elements_located((By.TAG_NAME, r"mws-conversation-list-item")))
    msg_container = driver.find_elements_by_tag_name(r"mws-conversation-list-item")[0]
    msg_container.find_element_by_tag_name("a").click()
    wait.until(ec.presence_of_all_elements_located((By.XPATH, query)))
    all_msg_txt = driver.find_elements_by_xpath(query)

    unfiltered_OTP = all_msg_txt[len(all_msg_txt)-1].text
    OTP = []
    for word in unfiltered_OTP:
        if word.isdigit():
            OTP.append(int(word))
    OTP.pop()
    print(">> Received OTP")
    return OTP

def SendOTP():
    driver.switch_to.window(driver.window_handles[1])
    driver.get('https://selfregistration.cowin.gov.in/')
    sleep(3)
    wait = WebDriverWait(driver, 20)
    wait.until(ec.presence_of_element_located((By.ID, "mat-input-0")))
    box = driver.find_element_by_id("mat-input-0")
    for n in your_phone_number:
        box.send_keys(n)
        sleep(.3)
    wait.until(ec.presence_of_element_located((By.TAG_NAME, "ion-button")))
    button = driver.find_element_by_tag_name("ion-button")
    button.click()
    wait.until(ec.presence_of_element_located((By.ID, "mat-input-1")))
    sleep(10)
    print(">> Waiting for OTP")

    return

def TryPuttinOTP(OTP):
    print(">> Now trying to put OTP")
    driver.switch_to.window(driver.window_handles[1])
    sleep(3)
    wait = WebDriverWait(driver, 30)
    wait.until(ec.presence_of_element_located((By.ID, "mat-input-1")))
    box = driver.find_element_by_id("mat-input-1")
    for char in OTP:
        box.send_keys(char)
        sleep(.6)
    sleep(1)
    wait.until(ec.presence_of_element_located((By.TAG_NAME, "ion-button")))
    button = driver.find_element_by_tag_name("ion-button")
    button.click()
    sleep(5)
    if(driver.current_url == "https://selfregistration.cowin.gov.in/dashboard"):
        print(">> Successfully Logged in!")
        return True

    return False

def SwitchToDistrict():
    sleep(1)
    driver.find_element_by_class_name(r'status-switch').click()
    sleep(1)

    return

def GoBackToMainPage():
    driver.get("https://selfregistration.cowin.gov.in/dashboard")
    return

def Logout():
    wait.until(ec.presence_of_element_located((By.XPATH, "//ul[contains(@class, 'navigation') and contains(@class, 'logout-text')]")))
    driver.find_element_by_xpath("//ul[contains(@class, 'navigation') and contains(@class, 'logout-text')]/li").click()
    driver.get('https://messages.google.com/web/authentication')
    return

def Login():
    OpenMessages()
    driver.switch_to.window(driver.window_handles[2])
    SendOTP()
    OTP = GetOTP()
    TryPuttinOTP(OTP)
    sleep(1)

counting_entries = 1;

while(vaccine_found == False):
    if driver.current_url != "https://selfregistration.cowin.gov.in/dashboard":
        print(">> User is logged out!    Trying to log back in 10 seconds...")
        sleep(10)
        Login()
    wait = WebDriverWait(driver, 30)
    print("\n>> Fetching fresh set of slots:")
    counting_entries+=1
    wait.until(ec.presence_of_element_located((By.CLASS_NAME, "btnlist")))
    button_appointment_schedule = driver.find_element_by_class_name("btnlist").find_element_by_xpath("//li/a")
    button_appointment_schedule.click()
    wait.until(ec.presence_of_element_located((By.CLASS_NAME, "register-btn")))
    button_appointment_schedule = driver.find_element_by_class_name("register-btn")
    button_appointment_schedule.click()
    SwitchToDistrict()
    select_state(driver)
    sleep(.5)
    select_district(driver)
    driver.find_elements_by_tag_name("ion-button")[1].click()
    wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, "form-check")))
    sleep(1)
    driver.find_elements_by_class_name("form-check")[0].click()
    vaccine_info = find_vaccines(driver)
    list_of_vaccines_index = check_vaccines(driver, vaccine_info)
    if len(list_of_vaccines_index) > 0:
        vaccine_found = True
        print("\n\n\nFound vaccine(s)!!!!")
        for index in list_of_vaccines_index:
            print("      >>> " + vaccine_info[index][0])
        vaccine_found = True
        PlayAlarm()
    else:
        print(f"Vaccine not found!     " + f"Retrying in {check_in_x_seconds} seconds..\n")
        sleep(1)
        GoBackToMainPage()
        # if(counting_entries % 6 == 0):
        #     Logout()
        sleep(check_in_x_seconds)
