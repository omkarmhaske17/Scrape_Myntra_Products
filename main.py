from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os
import requests
import errno


class Myntra_products:

    def __init__(self):
        self.driver = webdriver.Chrome(
            "F:\\Ignis Tech Solutions\\venv\\chromedriver.exe")
        self.product_brand_name = []
        self.product_name = []
        self.product_mrp_price = []
        self.product_sls_price = []

    def getLinks(self):

        self.product_links_list = list()

        for i in range(2, 3):  # you can change range of for loop based on number of pages + 1

            # Iterating over all pages to get all products links
            main_url = "https://www.myntra.com/women-shrugs?p="
            url = f"{main_url}{i}"
            self.driver.get(url)
            src = self.driver.page_source
            soup = BeautifulSoup(src, 'lxml')
            for li in soup.find_all(class_='product-base'):
                links = li.a.get('href')
                self.product_links_list.append(links)

        print("Total Products Are:", len(self.product_links_list))

        return self.product_links_list

    def getProductInfo(self):

        img_attrs_list = list()
        img_links = list()
        self.image_name_list = list()
        self.sizes_all_list = list()
        sizes_list = list()
        sizes_dict = {}
        self.product_desc = list()
        self.product_sizechart = list()

        x = 0
        
        for items in self.product_links_list:

            x += 1
            print(f"getting all info {x}/{len(self.product_links_list)}")
            self.driver.get("https://www.myntra.com/"+items)
            src = self.driver.page_source
            soup = BeautifulSoup(src, 'lxml')
            try:
                # This is for getting product brand name, product name, MRP and Sales Price, Size
                for a in soup.find_all('div', attrs={'class': 'pdp-description-container'}):
                    bname = a.find('h1', attrs={'class': 'pdp-title'})
                    self.pname = a.find('h1', attrs={'class': 'pdp-name'})
                    mrp = a.find('span', attrs={'class': 'pdp-mrp'})
                    sls = a.find('span', attrs={'class': 'pdp-price'})
                    img = a.find('div', attrs={'class': 'image-grid-image'})
                    print(img)

                    # print(mrp.text)

                    self.product_brand_name.append(bname.text)
                    self.product_name.append(self.pname.text)
                    if (sls and mrp != None):
                        sls_temp = sls.text
                        sls_int = sls_temp.replace("Rs. ", "")

                        mrp_temp = mrp.text
                        mrp_int = mrp_temp.replace("Rs. ", "")

                        sls_int = int(sls_int)
                        if sls_int < 500:
                            new_sls = sls_int * 0.28
                        elif sls_int >= 500 and sls_int <= 1000:
                            new_sls = sls_int * 0.42
                        elif sls_int >= 2000:
                            new_sls = sls_int * 0.55
                        elif sls_int >= 3000:
                            new_sls = sls_int * 0.60
                        elif sls_int >= 5000:
                            new_sls = sls_int * 0.72
                        elif sls_int >= 10000:
                            new_sls = sls_int * 0.78

                        self.product_mrp_price.append(int(mrp_int))
                        self.product_sls_price.append(round(new_sls))

                    else:
                        self.product_mrp_price.append(0)
                        self.product_sls_price.append(0)
            except:
                self.product_brand_name.append(0)
                self.product_name.append(0)
                self.product_mrp_price.append(0)
                self.product_sls_price.append(0)
                continue

            # This is for size atributes
            sizes_list.clear()
            sizes_dict.clear()
            for a in soup.find_all('div', attrs={'class': 'size-buttons-tipAndBtnContainer'}):
                size_name = a.find(
                    'p', attrs={'class': 'size-buttons-unified-size'})
                # print(size_name.text)
                if size_name != None:
                    sizes_list.append(size_name.text)
                else:
                    sizes_list.append(0)
            # print(sizes_list)
            sizes_dict['size'] = sizes_list.copy()
            # print(sizes_dict)
            self.sizes_all_list.append(sizes_dict.copy())
            # print(self.sizes_all_list)

            # # This is for getting product images link
            # for a in soup.find_all('div', attrs={'class', 'image-grid-imageContainer'}):
            #     img = a.find('div', attrs={'class': 'image-grid-image'})
            #     # print(img)
            #     img_attrs_list.append(str(img))
            #     break
            # #print(len(img_attrs_list))

            # #  clearing string and getting product images links
            # for items_img in img_attrs_list:
            #     repl = items_img.replace(
            #         '''<div class="image-grid-image" style='background-image: url("''', "")
            #     rep = repl.replace('''");'></div>''', "")
            #     # print(rep)
            #     img_links.append(rep)
            # # print(len(img_links))

            # # This is for creating folder for storing product images
            # foldername = f"F:/Ignis Tech Solutions/venv/ProductsImages1/"
            # if not os.path.exists(os.path.dirname(foldername)):
            #     try:
            #         os.makedirs(os.path.dirname(foldername))
            #     except OSError as e:  # Guard against race condition
            #         if e.errno != errno.EEXIST:
            #             raise
            # # This is for writing images to folder
            # for link in img_links:
            #     print(link)
            #     try:
            #         with open(f"F:\\Ignis Tech Solutions\\venv\\ProductsImages1\\{self.pname.text}-image1.jpg", 'wb') as f:
            #             # print(link)
            #             image = requests.get(link)
            #             f.write(image.content)
            #         break
            #     except:
            #         continue
            # print(f"saved successfully...{self.pname.text}.jpg")

            # This is for product description
            try:
                for dsc in soup.find_all('div', attrs={'class': 'pdp-productDescriptorsContainer'}):
                    if dsc != None:
                        self.product_desc.append(dsc)
                    else:
                        self.product_desc.append(0)
            except:
                self.product_desc.append(0)
                continue

            # This is for size chart
            try:
                btn = self.driver.find_element_by_class_name(
                    'size-buttons-show-size-chart')
                btn.click()
                page = self.driver.page_source
                page_soup = BeautifulSoup(page, 'lxml')
                chrt = page_soup.find(
                    'div', attrs={'class': 'sizeChartWeb-info'})
                if chrt != None:
                    self.product_sizechart.append(chrt)
                else:
                    self.product_sizechart.append(0)
            except:
                self.product_sizechart.append(0)
                continue

            # This is for getting all images names
            # for names in self.product_name:
            #     self.image_name_list.append(f"ProductsImages\\{names}-image1.jpg")
            # print(len(self.image_name_list))

            # print("brand name:",len(self.product_brand_name))
            # print("product name:",len(self.product_name))
            # print("sales price:",len(self.product_sls_price))
            # print("MRP price:",len(self.product_mrp_price))
            # print("desc:",len(self.product_desc))
            # print("sizechart:",len(self.product_sizechart))
            # print("sizes:",len(self.sizes_all_list))
            # print("image names:",len(self.image_name_list))

    def write_to_csv(self):
        print("writing to csv....")
        df = pd.DataFrame({'Brand Name': self.product_brand_name, 'Product Name': self.product_name,
                           'MRP Price': self.product_mrp_price, 'Sales Price': self.product_sls_price,
                           # 'Images': self.image_name_list,
                           'Product Attributes': self.sizes_all_list,
                           'Product Description': self.product_desc,
                           'Product Size Chart': self.product_sizechart})
        # df.transpose()
        df.to_csv('product_info_list.csv', index=False, encoding='utf-8')
        print("completed.")
        self.driver.close()


m = Myntra_products()
m.getLinks()
m.getProductInfo()
m.write_to_csv()
