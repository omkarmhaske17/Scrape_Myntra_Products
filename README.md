# Scrape_Myntra_Products
Data Scraping of myntra.com products(category:shrugs) 

clear_img_links.py file can download all images when run but without product name i.e it can store images names as image1,image2,image3,...,etc
main.py file can write csv file with [Brand Name,	Product Name,	MRP Price,	Sales Price, Product Attributes,	Product Description,	Product Size Chart] columns.
main.py file has one class with name Myntra_products and 3 other functions named getLinks(), getProductInfo(), write_to_csv() respectively.
