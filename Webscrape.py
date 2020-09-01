from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.wait
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup as bs
import csv
from itertools import zip_longest

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get("https://yocket.in/universities")
while True:
    try:
        button = selenium.webdriver.support.wait.WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Load More')))
        button.click()
        time.sleep(30)
    except Exception as e:
        print(e)
        break

html = browser.page_source.encode('utf-8')

all_uni_fees_lst = []
all_uni_fees_lst_final = []
all_uni_fees_lst_final1 = []

soup = bs(html, 'lxml')

all_uni_names = soup.find_all("p", class_="lead text-center card-top-head")
all_uni_names_lst = []
all_uni_names_lst_final = []
for i in all_uni_names:
    # print(i.text)
    new_string = i.text.replace("\n", "")
    all_uni_names_lst.append(new_string)

all_uni_location = soup.find_all("p", class_="text-center card-bottom-text")
# location
all_uni_location_lst_final1 = []
all_uni_location_lst = []
all_uni_location_lst_final = []
all_uni_lst_private_public = []
for i in all_uni_location:
    new_string = i.text.replace("\n", "")
    all_uni_location_lst.append(new_string)
for string in all_uni_location_lst:
    new_string = " ".join(string.split())
    all_uni_location_lst_final.append(new_string)

all_uni_fees = soup.find_all("p", class_="card-icon-text")
# fees
for i in all_uni_fees:
    # print(i.text)
    all_uni_fees_lst.append(i.text)
all_uni_fees_lst.pop(0)
for string in all_uni_fees_lst:
    # new_string = string.replace("\n","")
    # new_string1 = new_string.replace("\t","")
    new_string2 = string.replace("Tuition", "")
    new_string3 = new_string2.replace("*", "")
    new_string4 = " ".join(new_string3.split())
    all_uni_fees_lst_final.append(new_string4)
for i in all_uni_fees_lst_final[1::3]:
    all_uni_fees_lst_final1.append(i)

# private_public
for i in all_uni_fees_lst_final[0::3]:
    all_uni_lst_private_public.append(i)

# print(all_uni_names_lst)
# print(all_uni_fees_lst_final1)

# print(all_uni_lst_private_public)
for i in all_uni_location_lst_final:
    split_string = i.split(",")
    all_uni_location_lst_final1.append(split_string)

region = list(item[0] for item in all_uni_location_lst_final1)
country = list(item[1] for item in all_uni_location_lst_final1)


d = [all_uni_names_lst, all_uni_fees_lst_final1, region, country, all_uni_lst_private_public]
export_data = zip_longest(*d, fillvalue='')
with open('Uni.csv', 'w', encoding='utf-8', newline='') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(("Name", "Fees", "Region", "Country", "Type"))
    wr.writerows(export_data)
myfile.close()
