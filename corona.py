from bs4 import BeautifulSoup
import pandas
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

url = "https://www.gov.pl/web/koronawirus/wykaz-zarazen-koronawirusem-sars-cov-2"

driver = webdriver.Chrome() # create a new Chrome session
driver.get(url)
#time.sleep(6) #waiting 6 seconds

if driver.find_element_by_xpath("//*[@id='cookies-info']/div/button"):
    driver.find_element_by_xpath("//*[@id='cookies-info']/div/button").click()

python_button2 = driver.find_element_by_xpath("//*[@id='js-pagination-rows']/a[2]")
python_button2.click() #click more items on the page

soup=BeautifulSoup(driver.page_source,"html.parser") #take html code by BS

driver.quit() #close browser

table=soup.find("table")
all=table.find_all("tr")

l = []
i = 0
total1 = 0
total2 = 0
for item in all:
    i+=1

    if item.find("th") is not None:
        title1 = item.find_all("th")[0].text
        title2 = item.find_all("th")[1].text
        title3 = item.find_all("th")[2].text

    if item.find("td") is not None:
        d={}
        d[title1]=item.find_all("td")[0].text
        d[title2]=int(item.find_all("td")[1].text)
        total1 = total1 + d[title2]
        if item.find_all("td")[2].text == '':
            d[title3]=0
        else:
            d[title3]=int(item.find_all("td")[2].text)
        total2= total2 + d[title3]
        l.append(d)

total11={title1: 'Suma', title2: total1, title3: total2}
l.append(total11)

df=pandas.DataFrame(l)
df['Śmiertelność [%]'] = round(df['Liczba zgonów']*100/df['Liczba'],2)

df.to_excel(r"output.xlsx", index = False, header=True)
print(df)
