import pandas
from selenium import webdriver
import pyautogui, time, random


header = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
         'Chrome/88.0.4324.150 Safari/537.36 '


def proxyAuth(username, password):
    time.sleep(2)
    pyautogui.typewrite(username, interval=0.2)
    pyautogui.press('tab')
    pyautogui.typewrite(password, interval=0.2)
    pyautogui.press('enter')


def watch(links, watchType, proxyIp, proxyLogin, proxyPassword):
    option = webdriver.ChromeOptions()
    option.add_argument(f"--user-agent={header}")
    capabilities = webdriver.DesiredCapabilities().CHROME
    capabilities['acceptSslCerts'] = True
    option.add_argument(f"--proxy-server={proxyIp}")
    driver = webdriver.Chrome(options=option, desired_capabilities=capabilities)
    
    driver.get("https://www.youtube.com/")
    proxyAuth(proxyLogin, proxyPassword)
    time.sleep(0.5)
    
    for l in range(len(links)):
        link = random.choice(links)
        
        driver.get(link + '//videos')
        index = links.index(link)
        links.pop(index)
        numberOfVideos = random.randint(3, 4)
        if (watchType[index]) == 'channel':
            print('Watch type -', watchType[index])
            videoLinks = []
            videos = driver.find_elements_by_xpath('//*[@id="items"]/ytd-grid-video-renderer')
            for v in videos:
                videoLinks.append(v.find_element_by_xpath('.//div[1]/ytd-thumbnail/a').get_attribute('href'))
            for videoWatch in range(numberOfVideos):
                driver.get(videoLinks[random.randint(0, len(videoLinks) - 1)])
                print("Watching video", videoWatch + 1)
                time.sleep(6)
                checkAds(driver)
                
                duration = driver.find_element_by_class_name("ytp-time-duration").get_attribute('innerHTML')
                duration = duration.split(":")
                duration = int(duration[0]) * 60 + int(duration[1])
                duration = round(duration * round(random.uniform(0.5, 0.9), 2), 0)
                checkTime = int(duration/6)
                print('\tI will watch video during', duration, 'seconds')
                for c in range(checkTime):
                    time.sleep(6)
                    checkAdsDuring(driver)
                
                pauseDuration = random.randint(5, 10)
                driver.back()
                time.sleep(pauseDuration)
        elif (watchType[index]) == 'recommendation':
            print('Watch type -',watchType[index])
            videoLinks = []
            videos = driver.find_elements_by_xpath('//*[@id="items"]/ytd-grid-video-renderer')
            for v in videos:
                videoLinks.append(v.find_element_by_xpath('.//div[1]/ytd-thumbnail/a').get_attribute('href'))
            driver.get(videoLinks[random.randint(0, len(videoLinks) - 1)])

            for videoWatch in range(numberOfVideos):
                videoLinks.clear()
                channelName = driver.find_element_by_xpath('//*[@id="text"]/a').text
                videos = driver.find_elements_by_xpath('//*[@id="items"]/ytd-compact-video-renderer')
                for v in videos:
                    if v.find_element_by_xpath('.//*[@id="text"]').text == channelName:
                        videoLinks.append(v.find_element_by_xpath('.//div[1]/ytd-thumbnail/a').get_attribute('href'))
                driver.get(videoLinks[random.randint(0, len(videoLinks)-1)])
                print("Watching video", videoWatch + 1)
                time.sleep(6)
                checkAds(driver)
                duration = driver.find_element_by_class_name("ytp-time-duration").get_attribute('innerHTML')
                duration = duration.split(":")
                duration = int(duration[0]) * 60 + int(duration[1])
                duration = (round(duration * round(random.uniform(0.5, 0.9), 2), 0))
                checkTime = int(duration / 6)
                print('\tI will watch video during', duration, 'seconds')
                for c in range(checkTime):
                    time.sleep(6)
                    checkAdsDuring(driver)
                
                pauseDuration = random.randint(5, 10)
                time.sleep(pauseDuration)
    time.sleep(2)
    driver.quit()


def getLinks():
    readExcel = pandas.read_excel('data.xlsx', sheet_name='data')
    readExcel = readExcel.fillna('nan')
    linksTemp = readExcel['Links'].tolist()
    links = []
    for i in linksTemp:
        if i != 'nan':
            links.append(i)
    return links


def getWatchType():
    readExcel = pandas.read_excel('data.xlsx', sheet_name='data')
    readExcel = readExcel.fillna('nan')
    loginsTemp = readExcel['WatchType'].tolist()
    watchType = []
    for i in loginsTemp:
        if i != 'nan':
            watchType.append(i)
    return watchType


def getProxy():
    readExcel = pandas.read_excel('data.xlsx', sheet_name='data')
    readExcel = readExcel.fillna('nan')
    proxyTemp = readExcel['Proxy'].tolist()
    proxy = []
    for i in proxyTemp:
        if i != 'nan':
            proxy.append(i)
    proxyLoginTemp = readExcel['proxyLogin'].tolist()
    proxyLogin = []
    for i in proxyLoginTemp:
        if i != 'nan':
            proxyLogin.append(i)
    proxyPasswordTemp = readExcel['proxyPassword'].tolist()
    proxyPassword = []
    for i in proxyPasswordTemp:
        if i != 'nan':
            proxyPassword.append(i)
    return proxy, proxyLogin, proxyPassword


def checkAds(driver):
    playButtn = driver.find_element_by_class_name("ytp-cued-thumbnail-overlay")
    if playButtn.get_attribute('style') != 'display: none;':
        driver.find_element_by_class_name('ytp-large-play-button').click()
    ads = driver.find_elements_by_class_name("ytp-ad-text")
    time.sleep(0.5)
    if len(ads) != 0:
        time.sleep(6)
        elements = driver.find_elements_by_class_name("ytp-ad-text")
        for element in elements:
            if ('Пропустити' in element.text) or ('Skip' in element.text) or ('Пропустить' in element.text):
                element.click()
                print('\tAds skipped')
            elif ('после' in element.text) or ('після' in element.text) or ('after' in element.text):
                print('\tWaiting')
                adsDuration = driver.find_element_by_class_name("ytp-time-duration").get_attribute(
                    'innerHTML').split(":")
                time.sleep(int(adsDuration[0]) * 60 + int(adsDuration[1]))
        time.sleep(1)
        checkAds(driver)


def checkAdsDuring(driver):
    print('\tChecking ads...')
    playButtn = driver.find_element_by_class_name("ytp-cued-thumbnail-overlay")
    if playButtn.get_attribute('style') != 'display: none;':
        driver.find_element_by_class_name('ytp-large-play-button').click()
    ads = driver.find_elements_by_class_name("ytp-ad-text")
    if len(ads) != 0:
        elements = driver.find_elements_by_class_name("ytp-ad-text")
        for element in elements:
            if ('Пропустити' in element.text) or ('Skip' in element.text) or ('Пропустить' in element.text):
                element.click()
                print('\tAds skipped')
            elif ('после' in element.text) or ('після' in element.text) or ('after' in element.text):
                print('\tWaiting')
                adsDuration = driver.find_element_by_class_name("ytp-time-duration").get_attribute(
                    'innerHTML').split(":")
                time.sleep(int(adsDuration[0]) * 60 + int(adsDuration[1]))
        checkAds(driver)
        

def randomWatch():
    links = getLinks()
    watchType = getWatchType()
    proxyIp = getProxy()[0]
    proxyLogin = getProxy()[1]
    proxyPassword = getProxy()[2]
    
    for acc in range(len(proxyIp)):
        watch(links, watchType, proxyIp[acc], proxyLogin[acc], proxyPassword[acc])
        print('Endded for', acc+1, 'proxy')
    print('Watching completed')
    

if __name__ == '__main__':
    randomWatch()
