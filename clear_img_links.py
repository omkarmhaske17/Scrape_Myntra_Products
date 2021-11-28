from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import os
import errno



product_links_list = list()

# Iterating over all pages to get all products links
for i in range(1, 37): # you can change range of for loop based on number of pages + 1
    driver = webdriver.Chrome(
        "F:\\Ignis Tech Solutions\\venv\\chromedriver.exe")
    main_url = "https://www.myntra.com/women-shrugs?p="
    url = f"{main_url}{i}"
    driver.get(url)
    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')
    for li in soup.find_all(class_='product-base'):
        links = li.a.get('href')
        product_links_list.append(links)

print(len(product_links_list))

x = 0
for url in product_links_list: # opening product links one by one
    x += 1
    driver = webdriver.Chrome("F:\\Ignis Tech Solutions\\venv\\chromedriver.exe")
    driver.get(url)
    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')
    img_list = list()
    img_links = list()

    # getting raw links as strigs with some kind of attributes and many more
    for a in soup.find_all('div', attrs={'class', 'image-grid-imageContainer'}):
        img = a.find('div', attrs={'class': 'image-grid-image'})
        # print(img)
        img_list.append(str(img))
        break
    # print(img_list)

    # clearing string and getting images links
    for items in img_list:
        repl = items.replace(
            '''<div class="image-grid-image" style='background-image: url("''', "")
        rep = repl.replace('''");'></div>''', "")
        # print(rep)
        img_links.append(rep)
    #print(img_links)

    # downloads all images product by product but without giving proper name i.e image1,image2,..etc
    for link in img_links:
        with open(f"F:\\Ignis Tech Solutions\\venv\\images\\image{x}.jpg", 'wb') as f:
            # print(link)
            image = requests.get(link)
            f.write(image.content)
            print("writing...")

    driver.close()
