from selenium import webdriver
import requests
import xlsxwriter
import copy

# webdriver setup path
browser = webdriver.Chrome(executable_path="C:\\Users\\Shubham\\Downloads\\chromedriver_win32\\chromedriver.exe")

browser.get("https://www.game.tv/")
browser.maximize_window()

# to get number of required links(number of game tiles)
links = browser.find_elements_by_xpath('//*[@id="game_list"]/ul/li')

result = []
glist = []

# to find if status code of url and find tournament count if url is giving 200 response

for i in range(1,len(links)+1):
    try:
        game = browser.find_element_by_xpath('//*[@id="game_list"]/ul/li['+str(i)+']/a')
        request = requests.head(game.get_attribute('href'))
        
        if(request.status_code!=200):
            glist.clear()
            glist.append(str(browser.find_element_by_xpath('//*[@id="game_list"]/ul/li[1]/a/figcaption').text).replace(' Tournaments',''))
            glist.append(game.get_attribute('href'))
            glist.append(request.status_code)
        else:
            game.click()
            url = browser.current_url
            glist.clear()
            glist.append(str(browser.find_element_by_xpath('/html/body/div/section[1]/div[2]/div/div/div[1]/h1').text).replace(' Tournaments','') )
            glist.append(browser.current_url)
            glist.append(requests.head(url).status_code)
            glist.append(browser.find_element_by_xpath('/html/body/div/section[2]/div/div[1]/h2/span').text)
        result.append(copy.deepcopy(glist))
        browser.back()
    except:
        print(i)

#list to excel conversion using xlswriter module.

row0 = ['Game Name','Page URL', 'Page Status','Tournament count']
with xlsxwriter.Workbook('test.xlsx') as workbook:
    worksheet = workbook.add_worksheet()
    worksheet.write_row(0, 0, row0)
    for row_num, data in enumerate(result):
        worksheet.write_row(row_num+1, 0, data)

browser.quit()