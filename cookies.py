import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

sandboxCookie = '13313828369.9061'
ASPXAUTH = '27AB4CB33313E5F4F7744E8FEAB47C946497DD3739EA9FCECFB4ED16BD9633560086CCCEA68160C30F659B1290F2AA520' \
           'A8D3C877024D9D36AC5D31786CF5DAE8C58C6E2F36D243966F2571C1AC3E5FAC985866F6E9237CB5B37787B982DD94295' \
           '69DCC7A9B869AF9179FE42F6D886C7C1B6FD71B2449F24DCE290A4B43692FB7D0A9DD9C3CD33C67ECFF1C123C74DCF28272' \
           '424356766D5A2E16CE058FFF936FDAD7ABB6BDBD5FF31F4284DF40B81E25AE6DA814686107DE910565F52AAE02F31C77ECC' \
           'DB3D43D781C5EDD056F4E81E880540A6254BFEC6C065A5627C58CCDCDDA63E00C5BA2CA1EFAE9CC779BA8832'

login_url = 'https://canvas.nus.edu.sg/login/saml/103'
timeout = 10

def get_video_cookies():
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(login_url)
    try:
        element_present = EC.presence_of_element_located((By.ID, 'userInput'))
        print('Waiting for login...')
        WebDriverWait(driver, timeout=timeout).until(element_present)
    except:
        print('Timed out waiting for page to load')
    finally:
        print('Login page loaded')
        username_input = driver.find_element(By.ID, 'userInput')
        print('Please type in your NUS Net ID:')
        NUS_NET_ID = input()
        print('Please type in your password:')
        PASSWORD = input()
        print('Logging in, please wait for a while...')
        username_input.send_keys(NUS_NET_ID)
        username_submit_btn = driver.find_element(By.ID, 'userNameFormSubmit')
        username_submit_btn.click()

        password_input = driver.find_element(By.ID, 'password')
        signin_btn = driver.find_element(By.ID, 'signIn')
        password_input.send_keys(PASSWORD)
        signin_btn.click()

        application_present = EC.presence_of_element_located((By.ID, 'application'))
        WebDriverWait(driver, timeout=timeout).until(application_present)

        dashboard_app = driver.find_element(By.CLASS_NAME, 'ic-DashboardCard__box__container')
        dashboard_children = dashboard_app.find_elements(By.XPATH, './*')
        if len(dashboard_children) == 0:
            print('No modules enrolled')
            exit(-1)

        modules_dict = {}
        for module in dashboard_children:
            module_name = module.get_attribute('aria-label')
            modules_dict[module_name] = module

        # print out modules
        print('Your enrolled modules:')
        for m in list(modules_dict.keys()):
            print(m)

        # input target course number
        print('Please type in your target module number:')
        TARGET_MODULE = input()
        print('Getting cookies...')
        target_module_ele = None
        for k, v in modules_dict.items():
            if TARGET_MODULE in k:
                target_module_ele = v
                break
        if target_module_ele is None:
            print('Target module name invalid')
            exit(-1)

        # check and close prompt window
        click_finished = False
        try :
            target_module_ele.click()
            click_finished = True
        except :
            close_prompt = driver.find_element(By.ID, 'btnClosePrompt')
            close_prompt.click()
        finally:
            if not click_finished:
                target_module_ele.click()

        panopto_element = driver.find_element(By.CLASS_NAME, 'context_external_tool_128')
        panopto_element.click()

        time.sleep(1)
        tool_content_frame = driver.find_element(By.ID, 'tool_content')
        driver.switch_to.frame(tool_content_frame)
        video_content_element = driver.find_element(By.CLASS_NAME, 'subfolder-wrapper')
        video_content_element.click()

        all_cookies = driver.get_cookies()
        cookies_dict = {}
        for cookie in all_cookies:
            cookies_dict[cookie['name']] = cookie['value']
        return cookies_dict


