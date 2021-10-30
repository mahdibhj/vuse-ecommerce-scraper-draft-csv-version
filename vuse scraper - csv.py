import threading
from selenium import webdriver
from time import sleep
import pandas as pd
from selenium.common.exceptions import NoSuchWindowException
import requests
from bs4 import BeautifulSoup
import random
import xlrd
import os
import openpyxl
from datetime import datetime

########################################################################################################
########################################################################################################

def scrape_180smoke_products():
    sleep(5)
    erp_list = []
    out_of_stock_names=[]
    out_of_stock_links=[]
    out_of_stock_titles=[]
    stock_description_list=[]
    product_price_list = []

    products_pages_list = ['https://www.180smoke.ca/vype-bat-british-american-tobacco?order=name-asc','https://www.180smoke.ca/vype-bat-british-american-tobacco?order=name-asc&page=2']
    website_erp = '52710523'
    for website in products_pages_list:
        ### CONTAINERS ###


        web_driver=webdriver.Chrome()
        web_driver.get(website)
        print('180 smoke start now')
        web_driver.find_element_by_xpath("//*[@id='state']/option[text()='{}']".format("Quebec")).click()
        web_driver.find_element_by_xpath("//*[@id='month']/option[text()='{}']".format("January")).click()
        web_driver.find_element_by_xpath('//*[@id="day"]/option[text()="{}"]'.format("15")).click()
        web_driver.find_element_by_xpath("//*[@id='year']/option[text()='{}']".format("1970")).click()
        web_driver.find_element_by_xpath("//*[@id='__next']/div/div/section/div[2]/div/form/div[2]/div/button").click()

        products_list=[]

        sleep(5)
        products_links= web_driver.find_elements_by_class_name('product-list--card.card.h-100.border-0.card')

        for link in products_links:
            link2=link.find_elements_by_tag_name('a')
            for link3 in link2:
                product=link3.get_attribute('href')
                products_list.append(product)
        #print(len(products_list))
        #print(products_list[-52:-22])

        for product_link in products_list:
            web_driver.get(product_link)
            #web_driver.get('https://www.180smoke.ca/vuse-vype-epod-vpro-watermelon-cartridges-2pk')
            sleep(5)
            try:
                page_title = web_driver.find_element_by_class_name('page-product-view--title').text
                page_price = web_driver.find_element_by_class_name('page-product-view--price-final').text
                #print('canvape' + str(page_title) + '-'+str(page_price) )
                disabled_products = web_driver.find_elements_by_class_name('page-product-view--info-options--radio.page-product-view--info-options--radio--disabled.form-check')
                #stock_label_1 = web_driver.find_element_by_xpath('//*[@id="data-product-option-0"]/option[1]').get_attribute('outerHTML')
                #print('disabled element found')
                #print(disabled_products)
                for prod in disabled_products:
                    #print(prod.get_attribute('value'))
                    #print(prod.get_attribute('outerHTML'))
                    out_of_stock_titles.append(web_driver.find_element_by_class_name('page-product-view--title').text)
                    product_price_list.append(page_price)
                    out_of_stock_links.append(product_link)
                    out_of_stock_names.append( str(prod.get_attribute('outerHTML'))[:-14].split('>')[-1] )
                    stock_description_list.append('Out of stock')
                    erp_list.append(website_erp)

            except:
                #print('disabled not found')
                pass

            try:
                page_title = web_driver.find_element_by_class_name('page-product-view--title').text
                page_price = web_driver.find_element_by_class_name('page-product-view--price-final').text
                #print('canvape' + str(page_title) + '-'+str(page_price) )
                #print(web_driver.find_element_by_class_name('page-product-view--title').text)
                disabled_products = web_driver.find_elements_by_class_name('page-product-view--info-options--radio.form-check')
                #stock_label_1 = web_driver.find_element_by_xpath('//*[@id="data-product-option-0"]/option[1]').get_attribute('outerHTML')
                #print('enabled element found')
                #print(disabled_products)
                for prod in disabled_products:
                    if 'disabled' not in str(prod.get_attribute('outerHTML')):
                        #print(prod.get_attribute('value'))
                        #print(prod.get_attribute('outerHTML'))
                        out_of_stock_titles.append(web_driver.find_element_by_class_name('page-product-view--title').text)
                        out_of_stock_links.append(product_link)
                        product_price_list.append(page_price)
                        out_of_stock_names.append( str(prod.get_attribute('outerHTML'))[:-14].split('>')[-1] )
                        stock_description_list.append('In stock')
                        erp_list.append(website_erp)
            except:
                #print('enabled not found')
                pass

            df = pd.DataFrame({'ERP':erp_list,'product link':out_of_stock_links ,'product title':out_of_stock_titles ,'product type':out_of_stock_names, 'product price':product_price_list ,'stock description':stock_description_list })
            #print(df )
            if len(df)>0:
                df.to_csv('output/180 smoke stock.csv',index=False)
            else:
                print('180 Smoke Dataframe lenght is 0')
    print('180smoke finished')

########################################################################################################
########################################################################################################

def scrape_canvape_products():
    sleep(10)

    erp_list=[]
    out_of_stock_names=[]
    out_of_stock_links=[]
    out_of_stock_titles=[]
    stock_description_list=[]
    product_price_list=[]


    products_pages_list = ['https://www.canvape.com/Vuse-Canada-ePod-s/2373.htm?searching=Y&sort=7&cat=2373&show=40&page=1']
    website_erp = '53604123'
    for website in products_pages_list:

        web_driver=webdriver.Chrome()
        web_driver.get(website)
        print('canvape start now')

        sleep(5)
        #web_driver.find_element_by_xpath("//*[@id='state']/option[text()='{}']".format("Quebec")).click()

        #web_driver.find_element_by_xpath('//*[@id="month_field"]/option[text()="{}"]'.format(" January")).click()
        #web_driver.find_element_by_xpath('//*[@id="date_field"]/option[text()="{}"]'.format(" 15")).click()
        web_driver.find_element_by_xpath('//*[@id="year_field"]/option[text()="{}"]'.format(" 1970")).click()
        #web_driver.find_elements_by_tag_name('select')[-1].click()
        #web_driver.find_element_by_xpath('//*[@id="preview_img"]/div[1]/section/div/div[3]/div[1]/button').click()
        web_driver.find_element_by_class_name('agree_btn.btn_verified').click()
        products_list=[]

        sleep(5)
        products_links= web_driver.find_elements_by_class_name('grid-product__content')

        for link in products_links:
            link2=link.find_elements_by_tag_name('a')
            for link3 in link2:
                product=link3.get_attribute('href')
                products_list.append(product)
        #print(len(products_list))
        #print(products_list[-52:-22])





        for product_link in products_list:
            web_driver.get(product_link)
            #web_driver.get('https://www.180smoke.ca/vuse-vype-epod-vpro-watermelon-cartridges-2pk')
            sleep(5)



            try:
                page_title = web_driver.find_element_by_class_name('h2.product-single__title').text
                page_price = web_driver.find_element_by_class_name('product__price').text
                #print('canvape' + str(page_title) + '-'+str(page_price) )
                product_veriety = web_driver.find_elements_by_class_name('variant-input')
                #stock_label_1 = web_driver.find_element_by_xpath('//*[@id="data-product-option-0"]/option[1]').get_attribute('outerHTML')
                #print('Variants found')
                #print(product_veriety)
                for prod in product_veriety:
                    #print(prod.get_attribute('value'))
                    #print(prod.get_attribute('outerHTML'))
                    out_of_stock_titles.append(page_title)
                    out_of_stock_links.append(product_link)
                    out_of_stock_names.append( prod.get_attribute('value') )
                    product_price_list.append(page_price)
                    erp_list.append(website_erp)

                    if 'disabled' in str(prod.get_attribute('outerHTML')):
                        stock_description_list.append('Out of stock')
                    else:
                        stock_description_list.append('In stock')

            except:
                #print('infos not found')
                pass




            df = pd.DataFrame({'ERP':erp_list,'product link':out_of_stock_links ,'product title':out_of_stock_titles ,'product type':out_of_stock_names, 'product price':product_price_list ,'stock description':stock_description_list})
            #print(df )
            if len(df)>0:
                df.to_csv('output/canvape stock.csv',index=False)
            else:
                print('Canvape Dataframe lenght is 0')
    print('canvape finished')

########################################################################################################
########################################################################################################

def scrape_in2vapes_products():
    sleep(15)

    erp_list=[]
    out_of_stock_names=[]
    out_of_stock_links=[]
    out_of_stock_titles=[]
    stock_description_list=[]
    product_price_list=[]

    products_pages_list = ['https://in2vapes.com/collections/vuse']
    website_erp = 'in2vapes erp'
    for website in products_pages_list:

        web_driver=webdriver.Chrome()
        web_driver.get(website)
        print('in2vapes start now')
        sleep(5)
        #web_driver.find_element_by_xpath("//*[@id='state']/option[text()='{}']".format("Quebec")).click()

        #web_driver.find_element_by_xpath('//*[@id="bouncer_datepicker_month"]/option[text()="{}"]'.format("January")).click()
        #web_driver.find_element_by_xpath('//*[@id="bouncer_datepicker_day"]/option[text()="{}"]'.format("15")).click()
        web_driver.find_element_by_xpath('//*[@id="bouncer_datepicker_year"]/option[text()="{}"]'.format("1970")).click()
        web_driver.find_element_by_xpath('//*[@id="bouncer_modal_submit"]').click()

        products_list=[]

        sleep(5)
        products_links= web_driver.find_elements_by_class_name('three.columns')

        for link in products_links:
            link2=link.find_elements_by_tag_name('a')
            for link3 in link2:
                product=link3.get_attribute('href')
                products_list.append(product)
        #print(len(products_list))
        #print(products_list[-52:-22])





        for product_link in products_list:



            web_driver.get(product_link)
            #web_driver.get('https://in2vapes.com/collections/vuse/products/citrus-gin-vuse-epod')
            sleep(5)
            #print(product_title + '=' + product_price)

            if product_link == 'https://in2vapes.com/collections/vuse/products/vuse-epod-device':
                try:
                    product_title = str(web_driver.find_element_by_class_name('product_name').text)
                    product_price =  str(web_driver.find_element_by_class_name('money').text)
                    products_varieties = web_driver.find_elements_by_class_name('single-option-selector')[0]
                    #stock_label_1 = web_driver.find_element_by_xpath('//*[@id="data-product-option-0"]/option[1]').get_attribute('outerHTML')
                    #print('product variety found')
                    #print(product_link)
                    #print(products_varieties)
                    varieties_options = products_varieties.find_elements_by_tag_name('option')
                    for option in varieties_options:
                        sleep(1)
                        option_text = str(option.get_attribute('value'))
                        #print(option_text)
                        option.click()
                        #web_driver.find_element_by_xpath('//*[@id="product-select-4839627128929productproduct-template-option-1"]/option[text()="{}"]'.format(option_text)).click()
                        sleep(2)
                        sold_out_element = str(web_driver.find_element_by_class_name('notify_form').get_attribute('outerHTML') )
                        #print('Sold out element found')
                        #print(sold_out_element)
                        sleep(2)

                        sold_out_title= web_driver.find_element_by_xpath('//*[@id="shopify-section-product-template"]/div/div[2]/div[1]/div/div[2]/p/span[1]').get_attribute('outerHTML')
                        #print(str(sold_out_title))
                        #if ('display:none' in sold_out_element) or ('display: none' in sold_out_element):
                        if 'Sold Out' in str(sold_out_title)  :

                            #print('OUT OF STOCK')

                            erp_list.append(website_erp)
                            product_price_list.append(product_price)
                            out_of_stock_titles.append(product_title)
                            out_of_stock_links.append(product_link)
                            out_of_stock_names.append(option_text)
                            stock_description_list.append('Out of stock')
                        else:
                            #print('IN STOCK')
                            erp_list.append(website_erp)
                            product_price_list.append(product_price)
                            out_of_stock_titles.append(product_title)
                            out_of_stock_links.append(product_link)
                            out_of_stock_names.append(option_text)
                            stock_description_list.append('In stock')

                except:
                    #print('disabled not found')
                    pass


            else:

                try:
                    product_title = str(web_driver.find_element_by_class_name('product_name').text)
                    product_price =  str(web_driver.find_element_by_class_name('money').text)
                    products_varieties = web_driver.find_elements_by_class_name('single-option-selector')[1]
                    #stock_label_1 = web_driver.find_element_by_xpath('//*[@id="data-product-option-0"]/option[1]').get_attribute('outerHTML')
                    #print('product variety found')
                    #print(product_link)
                    #print(products_varieties)
                    varieties_options = products_varieties.find_elements_by_tag_name('option')
                    for option in varieties_options:
                        sleep(1)
                        option_text = str(option.get_attribute('value'))
                        #print(option_text)
                        option.click()
                        #web_driver.find_element_by_xpath('//*[@id="product-select-4839627128929productproduct-template-option-1"]/option[text()="{}"]'.format(option_text)).click()
                        sleep(2)
                        sold_out_element = str(web_driver.find_element_by_class_name('notify_form').get_attribute('outerHTML') )
                        #print('Sold out element found')
                        #print(sold_out_element)
                        sleep(2)

                        sold_out_title= web_driver.find_element_by_xpath('//*[@id="shopify-section-product-template"]/div/div[2]/div[1]/div/div[2]/p/span[1]').get_attribute('outerHTML')
                        #print(str(sold_out_title))
                        #if ('display:none' in sold_out_element) or ('display: none' in sold_out_element):
                        if 'Sold Out' in str(sold_out_title)  :

                            #print('OUT OF STOCK')

                            erp_list.append(website_erp)
                            product_price_list.append(product_price)
                            out_of_stock_titles.append(product_title)
                            out_of_stock_links.append(product_link)
                            out_of_stock_names.append(option_text)
                            stock_description_list.append('Out of stock')
                        else:
                            #print('IN STOCK')
                            erp_list.append(website_erp)
                            product_price_list.append(product_price)
                            out_of_stock_titles.append(product_title)
                            out_of_stock_links.append(product_link)
                            out_of_stock_names.append(option_text)
                            stock_description_list.append('In stock')

                except:
                    #print('disabled not found')
                    pass




            fat_pandas_df = pd.DataFrame({'ERP':erp_list,'product link':out_of_stock_links ,'product title':out_of_stock_titles ,'product type':out_of_stock_names , 'product price':product_price_list ,'stock description':stock_description_list})
            #print(fat_pandas_df )
            if len(fat_pandas_df)>0:
                fat_pandas_df.to_csv('output/in2vapes stock.csv',index=False)
            else:
                #pass
                print('in2vapes Dataframe lenght is 0')
    print('in2vapes finished')

########################################################################################################
########################################################################################################

def scrape_dragonvape_products():
    sleep(20)

    erp_list=[]
    out_of_stock_names=[]
    out_of_stock_links=[]
    out_of_stock_titles=[]
    stock_description_list=[]
    product_price_list=[]

    products_pages_list = ['https://dragonvape.ca/collections/vuse-vype-replacement-pods-dragon-vape?sort_by=title-ascending']
    website_erp = 'dragonvape erp'
    for website in products_pages_list:



        web_driver=webdriver.Chrome()
        web_driver.get(website)
        print('dragonvape start now')

        sleep(5)



        #web_driver.find_element_by_xpath("//*[@id='state']/option[text()='{}']".format("Quebec")).click()

        #web_driver.find_element_by_xpath('//*[@id="month_field"]/option[text()="{}"]'.format(" January")).click()
        #web_driver.find_element_by_xpath('//*[@id="date_field"]/option[text()="{}"]'.format(" 15")).click()
        web_driver.find_element_by_xpath('//*[@id="bouncer_datepicker_year"]/option[text()="{}"]'.format("1970")).click()
        #web_driver.find_elements_by_tag_name('select')[-1].click()
        #web_driver.find_element_by_xpath('//*[@id="preview_img"]/div[1]/section/div/div[3]/div[1]/button').click()
        web_driver.find_element_by_class_name('button-enter.btn.styled-submit.spb-buttonfont.spb-buttontextcolor.spb-buttonbackground').click()
        products_list=[]

        sleep(2)
        web_driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(2)
        products_links= web_driver.find_elements_by_class_name('tt-image-box')

        for link in products_links:
            link2=link.find_elements_by_tag_name('a')[-1]
            #for link3 in link2:
            product=link2.get_attribute('href')
            products_list.append(product)
        #print(len(products_list))
        #print(products_list)


        for product_link in products_list:
            #print(product_link)
            web_driver.get(product_link)
            #web_driver.get('https://www.180smoke.ca/vuse-vype-epod-vpro-watermelon-cartridges-2pk')
            sleep(5)





            try:
                page_title = web_driver.find_element_by_xpath('//*[@id="shopify-section-product-template"]/div[1]/div[2]/div/div[2]/div/h1').text
                product_price = web_driver.find_element_by_xpath('//*[@id="shopify-section-product-template"]/div[1]/div[2]/div/div[2]/div/div[3]/span[1]').text
                #print('dragon vape :'+page_title + '=' + product_price)
                product_veriety = web_driver.find_element_by_xpath('//*[@id="shopify-section-product-template"]/div[1]/div[2]/div/div[2]/div/div[5]/div/div[2]/div/select').find_elements_by_tag_name('option')
                #stock_label_1 = web_driver.find_element_by_xpath('//*[@id="data-product-option-0"]/option[1]').get_attribute('outerHTML')
                #print('Variants found')
                #print(product_veriety)

                variety_list_reference=['1.6%','3%','5%']
                variety_list=[]
                for prod in product_veriety:
                    #print(prod.text)
                    variety_list.append(prod.text)


                #print(prod.get_attribute('outerHTML'))


                for variety_element in variety_list_reference:
                    if variety_element not in variety_list :
                        erp_list.append(website_erp)
                        product_price_list.append(product_price)
                        out_of_stock_titles.append(page_title)
                        out_of_stock_links.append(product_link)
                        out_of_stock_names.append(variety_element)

                        stock_description_list.append('Out of stock')
                        #print('OUT OF STOCK')
                    else:
                        erp_list.append(website_erp)
                        product_price_list.append(product_price)
                        out_of_stock_titles.append(page_title)
                        out_of_stock_links.append(product_link)
                        out_of_stock_names.append(variety_element)

                        stock_description_list.append('In stock')
                        #print('IN STOCK')

            except:
                #print('infos not found')
                pass




            fat_pandas_df = pd.DataFrame({'ERP':erp_list,'product link':out_of_stock_links ,'product title':out_of_stock_titles ,'product type':out_of_stock_names , 'product price':product_price_list ,'stock description':stock_description_list})
            #print(fat_pandas_df )
            if len(fat_pandas_df)>0:
                fat_pandas_df.to_csv('output/dragonvape stock.csv',index=False)
            else:
                print('dragonvape Dataframe lenght is 0')
    print('dragonvape finished')

########################################################################################################
########################################################################################################

def scrape_hazetownvapes_products():
    sleep(25)

    erp_list=[]
    out_of_stock_names=[]
    out_of_stock_links=[]
    out_of_stock_titles=[]
    stock_description_list=[]
    product_price_list=[]

    products_pages_list = ['https://hazetownvapes.com/collections/vuse-alto-pods-vype-epod?sort_by=title-ascending']
    website_erp = 'hazetownvapes erp'
    for website in products_pages_list:

        web_driver=webdriver.Chrome()
        web_driver.get(website)
        print('hazetownvapes start now')

        web_driver.find_element_by_xpath('//*[@id="submit_birthdate"]').click()

        products_list=[]

        sleep(5)
        products_links= web_driver.find_element_by_class_name('product-collection.products-grid.row').find_elements_by_class_name('inner.product-item')

        for link in products_links:
            link2=link.find_elements_by_tag_name('a')
            for link3 in link2:
                product=link3.get_attribute('href')
                if(product not in products_list) and ('https' in str(product)) :
                    products_list.append(product)
        #print(len(products_list))
        #print(products_list)
        #print(products_list[-52:-22])

        for product_link in products_list:
            web_driver.get(product_link)
            #web_driver.get('https://www.180smoke.ca/vuse-vype-epod-vpro-watermelon-cartridges-2pk')
            sleep(5)

            try:
                try:
                    close_popup = web_driver.find_element_by_class_name('CloseButton__ButtonElement-sc-79mh24-0.eptNMg.ascutney-CloseButton.ascutney-close.ascutney-ClosePosition--top-right').click()
                except:
                    pass
                product_title= str(web_driver.find_elements_by_tag_name('h1')[-1].find_element_by_tag_name('span').get_attribute('outerHTML'))[6:-7].replace('\n','')
                product_price = web_driver.find_element_by_class_name('product-shop.desktop.col-md-6.left-vertical-moreview.vertical-moreview').find_element_by_class_name('prices').find_element_by_tag_name('span').text
                #print('Welcome to product page')
                #print(product_link)
                #print(product_title)
                #print('price: '+product_price)

                product_variety = web_driver.find_element_by_class_name('swatch.device-finish.swatch-0').find_elements_by_xpath('//div[contains(@class,"swatch-element")]')
                #stock_label_1 = web_driver.find_element_by_xpath('//*[@id="data-product-option-0"]/option[1]').get_attribute('outerHTML')
                #print('product variety found')
                #print(len(product_variety))
                #print(product_variety)
                #print(product_variety)
                for prod in product_variety:
                    sleep(1)
                    try:
                        close_popup = web_driver.find_element_by_class_name('CloseButton__ButtonElement-sc-79mh24-0.eptNMg.ascutney-CloseButton.ascutney-close.ascutney-ClosePosition--top-right').click()
                    except:
                        pass
                    #print('PRINT VARIETY N')
                    #prod = prod_0.find_element_by_class_name('bgImg')
                    #print(prod.get_attribute('data-value'))
                    #print(prod.get_attribute('outerHTML'))
                    #print('CLICK ON VARIETY')
                    #####################################################################################################
                    #####################################################################################################
                    prod.click()
                    #print('Variety clicked')
                    erp_list.append(website_erp)
                    product_price_list.append(product_price)
                    out_of_stock_titles.append(product_title.replace('  ',''))
                    out_of_stock_links.append(product_link)
                    out_of_stock_names.append(str(prod.get_attribute('data-value')))
                    if 'soldout' in str(prod.get_attribute('outerHTML')) :
                        stock_description_list.append('Out of stock')
                        #print('OUT OF STOCK')
                    else:
                        stock_description_list.append('In stock')
                        #print('IN STOCK')

            except:
                #print('disabled not found')
                sleep(1)
                pass



            df = pd.DataFrame({'ERP':erp_list,'product link':out_of_stock_links ,'product title':out_of_stock_titles ,'product type':out_of_stock_names , 'product price':product_price_list ,'stock description':stock_description_list})
            #print(df)
            #print(out_of_stock_titles)
            if len(df)>0:
                df.to_csv('output/hazetownvapes stock.csv',index=False)
            else:
                #pass
                print('hazetownvapes Dataframe lenght is 0')
    print('hazetownvapes finished')

########################################################################################################
########################################################################################################

def scrape_vapesbyenushi_products():
    sleep(30)

    erp_list = []
    out_of_stock_names=[]
    out_of_stock_links=[]
    out_of_stock_titles=[]
    stock_description_list=[]
    product_price_list = []

    products_pages_list = ['https://www.vapesbyenushi.com/vuse/']
    website_erp = 'vapesbyenushi erp'
    for website in products_pages_list:
        ### CONTAINERS ###


        web_driver=webdriver.Chrome()
        web_driver.get(website)
        print('vapesbyenushi start now')

        sleep(3)
        try:
            webdriver.find_element_by_xpath('//*[@id="en_US"]/tbody/tr[7]/td/table/tbody/tr/td/div/form/input[1]').click()
        except:
            pass


        #web_driver.find_element_by_xpath('//*[@id="AgeVerifycSelect"]/option[text()="{}"]'.format("Quebec")).click()
        web_driver.find_element_by_xpath('//*[@id="bmonth"]').send_keys("01")
        web_driver.find_element_by_xpath('//*[@id="bday"]').send_keys("15")
        web_driver.find_element_by_xpath('//*[@id="byear"]').send_keys("1970")
        #web_driver.find_element_by_xpath('/html/body/div[1]/div[4]/form/input[1]').click()



        products_list=[]

        sleep(5)
        products_divs= web_driver.find_elements_by_class_name('ProductImage.QuickView')
        #wc_session = HTMLSession()
        #products_divs = wc_session.get(website).html.find('div.product-small.box')



        for divs in products_divs:
            #print(divs)
            a_tag = divs.find_elements_by_tag_name('a')
            for  a_tag_element in a_tag :
                product=a_tag_element.get_attribute('href')
                #if '/product' in str(product):
                products_list.append(product)
        #print(len(products_list))
        #print(products_list)


        final_products_link_list = []
        final_products_variety_link_list = []
        final_out_of_stock_list = []
        out_of_stock_container = []
        for product_link in products_list:
            #print(product_link)
            try:
                web_driver.get(product_link)
                #web_driver.get('https://vapevine.ca/buy/vuse-canada-golden-tobacco-pods/')
                sleep(5)
                product_first_name = web_driver.find_element_by_xpath('//*[@id="LayoutColumn1"]/div[2]/div/h1').text
                #print(product_first_name)
                try:


                    variety_elements = web_driver.find_element_by_class_name('productOptionViewRadio').find_elements_by_class_name('radio')
                    variety_names = web_driver.find_element_by_class_name('productOptionViewRadio').find_elements_by_class_name('name')
                    #print('names found')
                    #print(str(len(variety_names)),'  ',str(len(variety_elements)) )
                    #print(variety_names)


                    for i in range(len(variety_elements)):
                        element=variety_elements[i]
                        pdt_name=variety_names[i].text
                        if 'Out of stock' in pdt_name:
                            pdt_name=pdt_name[-15]
                        #print(pdt_name)
                        element.click()
                        nicotine_variety = (web_driver.find_elements_by_class_name('productOptionViewRadio'))[-1].find_elements_by_class_name('radio')
                        nicotine_variety_names = web_driver.find_elements_by_class_name('productOptionViewRadio')[-1].find_elements_by_class_name('name')
                        product_price = web_driver.find_element_by_class_name('ProductPrice.VariationProductPrice').text
                        #print('Price: ' + product_price)
                        for i in range(len(nicotine_variety)):
                            nicotine_element=nicotine_variety[i]
                            nicotine_pdt_name=nicotine_variety_names[i].text
                            #print(nicotine_element)
                            #print(nicotine_pdt_name)
                            if 'Out of stock' in nicotine_pdt_name :

                                final_out_of_stock = str(pdt_name)+' '+str(nicotine_pdt_name)
                                final_page_title = str(product_first_name)+' '+str(pdt_name)
                                final_variety_str = str(nicotine_pdt_name)[:-15]
                                #print(final_out_of_stock)
                                if str(final_out_of_stock) not in out_of_stock_container:
                                    final_products_variety_link_list.append(nicotine_pdt_name)
                                    final_out_of_stock_list.append(product_first_name+' ' +pdt_name)
                                    final_products_link_list.append(product_link)
                                    out_of_stock_container.append(product_first_name+' '+str(final_out_of_stock))


                                    erp_list.append(website_erp)
                                    out_of_stock_names.append(final_variety_str)
                                    out_of_stock_links.append(product_link)
                                    out_of_stock_titles.append(final_page_title)
                                    stock_description_list.append('Out of stock')
                                    product_price_list.append(product_price)

                            else:
                                final_out_of_stock = str(pdt_name)+' '+str(nicotine_pdt_name)
                                final_page_title = str(product_first_name)+' '+str(pdt_name)
                                final_variety_str = str(nicotine_pdt_name)
                                #print(final_out_of_stock)
                                if str(final_out_of_stock) not in out_of_stock_container:
                                    final_products_variety_link_list.append(nicotine_pdt_name)
                                    final_out_of_stock_list.append(product_first_name+' ' +pdt_name)
                                    final_products_link_list.append(product_link)
                                    out_of_stock_container.append(product_first_name+' '+str(final_out_of_stock))


                                    erp_list.append(website_erp)
                                    out_of_stock_names.append(final_variety_str)
                                    out_of_stock_links.append(product_link)
                                    out_of_stock_titles.append(final_page_title)
                                    stock_description_list.append('In stock')
                                    product_price_list.append(product_price)




                        sleep(3)

                        #print('NO')
                except:
                    pass
            except:
                pass



            vapevine_df = pd.DataFrame({'ERP':erp_list,'product link':out_of_stock_links ,'product title':out_of_stock_titles ,'product type':out_of_stock_names, 'product price':product_price_list ,'stock description':stock_description_list})
            #print(vapevine_df )
            if len(vapevine_df)>0:
                vapevine_df.to_csv('output/vapesbyenushi stock.csv',index=False)
            else:
                print('vapesbyenushi Dataframe lenght is 0')
    print('vapesbyenushi finished')

########################################################################################################
########################################################################################################

def scrape_vapevine_products():
    sleep(35)

    erp_list = []
    out_of_stock_names=[]
    out_of_stock_links=[]
    out_of_stock_titles=[]
    stock_description_list=[]
    product_price_list = []
    products_pages_list = ['https://vapevine.ca/product/vuse-canada-pods/']
    website_erp = 'vapevine erp'
    for website in products_pages_list:
        web_driver=webdriver.Chrome()
        web_driver.get(website)
        print('vapevine start now')
        sleep(5)
        try:
            webdriver.find_element_by_xpath('//*[@id="en_US"]/tbody/tr[7]/td/table/tbody/tr/td/div/form/input[1]').click()
        except:
            pass

        #web_driver.find_element_by_xpath("//*[@id='province-in-canada']/option[text()='{}']".format("Quebec")).click()
        web_driver.find_element_by_xpath('//*[@id="age-gate-m"]').send_keys("01")
        web_driver.find_element_by_xpath('//*[@id="age-gate-d"]').send_keys("15")
        web_driver.find_element_by_xpath('//*[@id="age-gate-y"]').send_keys("1970")
        web_driver.find_element_by_xpath('/html/body/div[1]/div[4]/form/input[1]').click()



        products_list=[]

        sleep(5)
        products_links= web_driver.find_elements_by_class_name('woocommerce-LoopProduct-link.woocommerce-loop-product__link')
        #wc_session = HTMLSession()
        #products_links = wc_session.get(website).html.find('div.product-small.box')


        for link in products_links:
            #print(link)
            product=link.get_attribute('href')
            #if '/product' in str(product):
            products_list.append(product)
        #print(len(products_list))
        #print(products_list)

        for product_link in products_list:
            #print(product_link)
            try:
                web_driver.get(product_link)
                #web_driver.get('https://vapevine.ca/buy/vuse-canada-golden-tobacco-pods/')
                sleep(5)

                try:
                    page_title = web_driver.find_element_by_class_name('product_title.entry-title').text
                    page_price = web_driver.find_element_by_class_name('product_infos').find_element_by_class_name('price').find_element_by_class_name('woocommerce-Price-amount.amount').find_element_by_tag_name('bdi').text
                    #print(page_title+'  '+page_price)
                    stock_label_elements = web_driver.find_elements_by_class_name('attached')
                    #print('disabled element found')
                    #print(stock_label_elements)
                    for element in stock_label_elements:
                        if 'disabled' in str(element.get_attribute('outerHTML')):

                            #print('out of stock in : ',product_link)
                            erp_list.append(website_erp)
                            out_of_stock_names.append(element.get_attribute('value'))
                            out_of_stock_links.append(product_link)
                            out_of_stock_titles.append(page_title)
                            stock_description_list.append('Out of stock')
                            product_price_list.append(page_price)
                        else:

                            #print('in stock in : ',product_link)
                            erp_list.append(website_erp)
                            out_of_stock_names.append(element.get_attribute('value'))
                            out_of_stock_links.append(product_link)
                            out_of_stock_titles.append(page_title)
                            stock_description_list.append('In stock')
                            product_price_list.append(page_price)


                        #print('NO')
                except:
                    pass
            except:
                pass



            vapevine_df = pd.DataFrame({'ERP':erp_list,'product link':out_of_stock_links ,'product title':out_of_stock_titles ,'product type':out_of_stock_names, 'product price':product_price_list ,'stock description':stock_description_list})
            #print(vapevine_df )
            if len(vapevine_df)>0:
                vapevine_df.to_csv('output/vapevine stock.csv',index=False)
            else:
                print('vapevine DataFrame lenght is 0')
    print('vapevine finished')

########################################################################################################
########################################################################################################

def scrape_ftpanda_products():
    sleep(40)

    erp_list=[]
    out_of_stock_names=[]
    out_of_stock_links=[]
    out_of_stock_titles=[]
    stock_description_list=[]
    product_price_list=[]


    products_pages_list = ['https://fatpanda.ca/collections/vuse-pods']
    website_erp = 'fatpandas erp'
    for website in products_pages_list:



        web_driver=webdriver.Chrome()
        web_driver.get(website)

        sleep(3)
        try:
            webdriver.find_element_by_xpath('//*[@id="en_US"]/tbody/tr[7]/td/table/tbody/tr/td/div/form/input[1]').click()
        except:
            pass


        web_driver.find_element_by_xpath("//*[@id='province-in-canada']/option[text()='{}']".format("Quebec")).click()
        web_driver.find_element_by_xpath("//*[@id='age_verfication_modal']/div/div/div[2]/div/div[4]/div[1]/input").send_keys("01")
        web_driver.find_element_by_xpath('//*[@id="age_verfication_modal"]/div/div/div[2]/div/div[4]/div[2]/input').send_keys("15")
        web_driver.find_element_by_xpath('//*[@id="age_verfication_modal"]/div/div/div[2]/div/div[4]/div[3]/input').send_keys("1970")
        web_driver.find_element_by_xpath('//*[@id="age_verfication_modal"]/div/div/div[2]/div/div[5]/button').click()



        products_list=[]

        sleep(5)
        products_links= web_driver.find_elements_by_class_name('productitem--image-link')
        for link in products_links:
            product=link.get_attribute('href')
            products_list.append(product)
        #print(len(products_list))
        #print(products_list)

        for product_link in products_list:
            web_driver.get(product_link)
            sleep(5)

            try:
                page_title = web_driver.find_element_by_xpath('//*[@id="shopify-section-static-product"]/section/article/div[2]/div[1]/h1').text
                page_price = web_driver.find_element_by_class_name('product--price').find_element_by_class_name('price--main').find_element_by_class_name('money').text
                #print(page_title+'  '+page_price)

                stock_label_element_1 = web_driver.find_element_by_xpath('//*[@id="data-product-option-0"]/option[1]')
                stock_label_1 = web_driver.find_element_by_xpath('//*[@id="data-product-option-0"]/option[1]').get_attribute('outerHTML')


                if 'disabled' in str(stock_label_1):
                    #print(stock_label_1)
                    #out_of_stock_names.append(stock_label_element_1.get_attribute('value'))
                    #out_of_stock_links.append(product_link)
                    #print('out of stock in : ',product_link)
                    erp_list.append(website_erp)
                    out_of_stock_names.append(stock_label_element_1.get_attribute('value'))
                    out_of_stock_links.append(product_link)
                    out_of_stock_titles.append(page_title)
                    stock_description_list.append('Out of stock')
                    product_price_list.append(page_price)


                else:
                    #print('in stock in : ',product_link)
                    erp_list.append(website_erp)
                    out_of_stock_names.append(stock_label_element_1.get_attribute('value'))
                    out_of_stock_links.append(product_link)
                    out_of_stock_titles.append(page_title)
                    stock_description_list.append('In stock')
                    product_price_list.append(page_price)

                    #print('NO')
            except:
                pass


            try:
                stock_label_2_element = web_driver.find_element_by_xpath('//*[@id="data-product-option-0"]/option[2]')
                stock_label_2 = web_driver.find_element_by_xpath('//*[@id="data-product-option-0"]/option[2]').get_attribute('outerHTML')
                if 'disabled' in str(stock_label_2):
                    #print('out of stock in : ',product_link)
                    erp_list.append(website_erp)
                    out_of_stock_names.append(stock_label_2_element.get_attribute('value'))
                    out_of_stock_links.append(product_link)
                    out_of_stock_titles.append(page_title)
                    stock_description_list.append('Out of stock')
                    product_price_list.append(page_price)

                else:
                    #print('in stock in : ',product_link)
                    erp_list.append(website_erp)
                    out_of_stock_names.append(stock_label_2_element.get_attribute('value'))
                    out_of_stock_links.append(product_link)
                    out_of_stock_titles.append(page_title)
                    stock_description_list.append('In stock')
                    product_price_list.append(page_price)

                    #print('NO')

            except:
                pass

            try:
                stock_label_3_element = web_driver.find_element_by_xpath('//*[@id="data-product-option-0"]/option[3]')
                stock_label_3 = web_driver.find_element_by_xpath('//*[@id="data-product-option-0"]/option[3]').get_attribute('outerHTML')
                #stock_label_4 = web_driver.find_element_by_xpath('//*[@id="data-product-option-0"]/option[4]').get_attribute('outerHTML')
                if 'disabled' in str(stock_label_3):
                    #print('out of stock in : ',product_link)
                    erp_list.append(website_erp)
                    out_of_stock_names.append(stock_label_3_element.get_attribute('value'))
                    out_of_stock_links.append(product_link)
                    out_of_stock_titles.append(page_title)
                    stock_description_list.append('Out of stock')
                    product_price_list.append(page_price)
                else:
                    #print('in stock in : ',product_link)
                    erp_list.append(website_erp)
                    out_of_stock_names.append(stock_label_3_element.get_attribute('value'))
                    out_of_stock_links.append(product_link)
                    out_of_stock_titles.append(page_title)
                    stock_description_list.append('In stock')
                    product_price_list.append(page_price)
                    #print('NO')
            except:
                pass


            try:
                stock_label_4_element = web_driver.find_element_by_xpath('//*[@id="data-product-option-0"]/option[4]')
                stock_label_4 = web_driver.find_element_by_xpath('//*[@id="data-product-option-0"]/option[4]').get_attribute('outerHTML')
                #stock_label_4 = web_driver.find_element_by_xpath('//*[@id="data-product-option-0"]/option[4]').get_attribute('outerHTML')
                if 'disabled' in str(stock_label_4):
                    #print('out of stock in : ',product_link)
                    erp_list.append(website_erp)
                    out_of_stock_names.append(stock_label_4_element.get_attribute('value'))
                    out_of_stock_links.append(product_link)
                    out_of_stock_titles.append(page_title)
                    stock_description_list.append('Out of stock')
                    product_price_list.append(page_price)
                else:
                    #print('in stock in : ',product_link)
                    erp_list.append(website_erp)
                    out_of_stock_names.append(stock_label_4_element.get_attribute('value'))
                    out_of_stock_links.append(product_link)
                    out_of_stock_titles.append(page_title)
                    stock_description_list.append('In stock')
                    product_price_list.append(page_price)
                    #print('NO')
            except:
                pass


            try:
                stock_label_5_element = web_driver.find_element_by_xpath('//*[@id="data-product-option-0"]/option[5]')
                stock_label_5 = web_driver.find_element_by_xpath('//*[@id="data-product-option-0"]/option[5]').get_attribute('outerHTML')
                #stock_label_4 = web_driver.find_element_by_xpath('//*[@id="data-product-option-0"]/option[4]').get_attribute('outerHTML')
                if 'disabled' in str(stock_label_5):
                    #print('out of stock in : ',product_link)
                    erp_list.append(website_erp)
                    out_of_stock_names.append(stock_label_5_element.get_attribute('value'))
                    out_of_stock_links.append(product_link)
                    out_of_stock_titles.append(page_title)
                    stock_description_list.append('Out of stock')
                    product_price_list.append(page_price)
                else:
                    #print('in stock in : ',product_link)
                    erp_list.append(website_erp)
                    out_of_stock_names.append(stock_label_5_element.get_attribute('value'))
                    out_of_stock_links.append(product_link)
                    out_of_stock_titles.append(page_title)
                    stock_description_list.append('In stock')
                    product_price_list.append(page_price)
                    #print('NO')
            except:
                pass


            try:
                stock_label_6_element = web_driver.find_element_by_xpath('//*[@id="data-product-option-0"]/option[6]')
                stock_label_6 = web_driver.find_element_by_xpath('//*[@id="data-product-option-0"]/option[6]').get_attribute('outerHTML')
                #stock_label_4 = web_driver.find_element_by_xpath('//*[@id="data-product-option-0"]/option[4]').get_attribute('outerHTML')
                if 'disabled' in str(stock_label_6):
                    #print('out of stock in : ',product_link)
                    erp_list.append(website_erp)
                    out_of_stock_names.append(stock_label_6_element.get_attribute('value'))
                    out_of_stock_links.append(product_link)
                    out_of_stock_titles.append(page_title)
                    stock_description_list.append('Out of stock')
                    product_price_list.append(page_price)
                else:
                    #print('in stock in : ',product_link)
                    erp_list.append(website_erp)
                    out_of_stock_names.append(stock_label_6_element.get_attribute('value'))
                    out_of_stock_links.append(product_link)
                    out_of_stock_titles.append(page_title)
                    stock_description_list.append('In stock')
                    product_price_list.append(page_price)
                    #print('NO')
            except:
                pass





            fat_pandas_df = pd.DataFrame({'ERP':erp_list,'product link':out_of_stock_links ,'product title':out_of_stock_titles ,'product type':out_of_stock_names, 'product price':product_price_list ,'stock description':stock_description_list})
            #print(fat_pandas_df )
            if len(fat_pandas_df)>0:
                fat_pandas_df.to_csv('output/Fat Pandas stock.csv',index=False)
    print('ftpanda finished')

########################################################################################################
########################################################################################################

def scrape_vapemeet_products():
    sleep(45)

    erp_list = []
    out_of_stock_names=[]
    out_of_stock_links=[]
    out_of_stock_titles=[]
    stock_description_list=[]
    product_price_list = []

    products_pages_list = ['https://vapemeet.ca/collections/vuse-epods']
    website_erp = 'vapemeet erp'
    for website in products_pages_list:



        web_driver=webdriver.Chrome()
        web_driver.get(website)
        print('vapemeet start now')
        sleep(5)

        #web_driver.find_element_by_xpath("//*[@id='state']/option[text()='{}']".format("Quebec")).click()

        web_driver.find_element_by_xpath('//*[@id="new_modal"]/div[1]/div/div[4]/input[1]').send_keys("11")
        web_driver.find_element_by_xpath('//*[@id="new_modal"]/div[1]/div/div[4]/input[2]').send_keys("11")
        web_driver.find_element_by_xpath('//*[@id="new_modal"]/div[1]/div/div[4]/input[3]').send_keys("1970")
        #web_driver.find_element_by_xpath('//*[@id="preview_img"]/div[1]/section/div/div[3]/div[1]/button').click()
        web_driver.find_element_by_xpath('//*[@id="bouncer_modal_actions"]/button[1]').click()
        products_list=[]

        sleep(2)
        web_driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(5)
        products_links= web_driver.find_elements_by_class_name('image__container.product__imageContainer')

        for link in products_links:
            link2=link.find_element_by_tag_name('a')
            #for link3 in link2:
            product=link2.get_attribute('href')
            products_list.append(product)
        #print(len(products_list))
        #print(products_list)


        for product_link in products_list:
            #print(product_link)
            web_driver.get(product_link)
            #web_driver.get('https://www.180smoke.ca/vuse-vype-epod-vpro-watermelon-cartridges-2pk')
            sleep(4)

            try:
                page_title = str(web_driver.find_element_by_xpath('//*[@id="shopify-section-product__main"]/section/div/div/div[2]/div[1]/h1').text).split('\n')[0]
                try:
                    page_price = web_driver.find_element_by_xpath('//*[@id="shopify-section-product__main"]/section/div/div/div[2]/div[1]/p/span[1]/span/span').text
                except:
                    page_price = 'No price in web page'
                #print(page_title)
                product_veriety = web_driver.find_element_by_class_name('single-option-selector').find_elements_by_tag_name('option')
                #stock_label_1 = web_driver.find_element_by_xpath('//*[@id="data-product-option-0"]/option[1]').get_attribute('outerHTML')
                #print('Variants found')
                #print(len(product_veriety))
                if len(product_veriety)>1:
                    for prod in product_veriety:
                        try:
                            prod.click()
                            #print('prod clicked')
                            #print(prod.get_attribute('outerHTML'))
                            out_of_stock_titles.append(page_title)
                            #print('out_of_stock_titles')
                            #print(len(out_of_stock_titles))
                            out_of_stock_links.append(product_link)
                            #print('out_of_stock_links')
                            #print(len(out_of_stock_links))
                            out_of_stock_names.append(prod.text)
                            #print('out_of_stock_names')
                            #print(len(out_of_stock_names))
                            erp_list.append(website_erp)
                            product_price_list.append(page_price)
                            try:
                                sold_out_button = str(web_driver.find_element_by_class_name('button.ajax-submit.action_button.button--add-to-cart').get_attribute('outerHTML') )
                                #print('sold out button found')
                                #print(sold_out_button)
                                if 'disabled' in sold_out_button :
                                    stock_description_list.append('Out of stock')
                                    #print('OUT OF STOCK')
                                else:
                                    stock_description_list.append('In stock')
                                    #print('IN STOCK')
                            except:
                                sold_out_button = str(web_driver.find_element_by_class_name('button--add-to-cart.sold_product.disabled').get_attribute('outerHTML') )
                                #print('sold out button found v2')
                                stock_description_list.append('Out of stock')
                        except:
                            pass
                else:
                    pass



            except:
                try:
                    page_title = str(web_driver.find_element_by_xpath('//*[@id="shopify-section-product__main"]/section/div/div/div[2]/div[1]/h1').text).split('\n')[0]
                    try:
                        page_price = web_driver.find_element_by_xpath('//*[@id="shopify-section-product__main"]/section/div/div/div[2]/div[1]/p/span[1]/span/span').text
                    except:
                        page_price = 'No price in web page'

                    #print(prod.text)
                    #print(prod.get_attribute('outerHTML'))
                    out_of_stock_titles.append(page_title)
                    #print(len(out_of_stock_titles))
                    out_of_stock_links.append(product_link)
                    product_price_list.append(page_price)
                    erp_list.append(website_erp)
                    #print(len(out_of_stock_links))
                    description_text = str(web_driver.find_element_by_class_name('description.content.has-padding-top').get_attribute('outerHTML'))
                    #print('description text')
                    #print(description_text)
                    if ('1.6' in description_text) or ('16mg' in description_text):
                        out_of_stock_names.append('18mg/mL')
                    elif ('34mg' in description_text) or ('3%' in description_text):
                        out_of_stock_names.append('34mg/mL')
                    elif ('5%' in description_text) or ('57mg' in description_text):
                        out_of_stock_names.append('57mg/mL')
                    else:
                        out_of_stock_names.append('Error extracting from pdt description')

                    #print(len(out_of_stock_names))
                    stock_description_list.append('In stock')
                    #print('extracted from pdt description IN STOCK')
                except:
                    pass






            fat_pandas_df = pd.DataFrame({'ERP':erp_list,'product link':out_of_stock_links ,'product title':out_of_stock_titles ,'product type':out_of_stock_names,'product price':product_price_list ,'stock description':stock_description_list})
            #print(fat_pandas_df )
            if len(fat_pandas_df)>0:
                fat_pandas_df.to_csv('output/vapemeet stock.csv',index=False)
            else:
                print('Dataframe lenght is 0')
    print('vapemeet finished')

########################################################################################################
########################################################################################################

def scrape_digitalimports_products():
    sleep(50)

    erp_list = []
    out_of_stock_names=[]
    out_of_stock_links=[]
    out_of_stock_titles=[]
    stock_description_list=[]
    product_price_list = []

    products_pages_list = ['https://www.digitalimports.ca/category_s/2662.htm?searching=Y&sort=7&cat=2662&show=30&page=1']
    website_erp = 'digitalimports erp'
    for website in products_pages_list:



        web_driver=webdriver.Chrome()
        web_driver.get(website)
        print('digitalimports start now')
        sleep(5)
        #web_driver.find_element_by_xpath("//*[@id='state']/option[text()='{}']".format("Quebec")).click()
        web_driver.find_element_by_id('AVenterLink').click()

        products_list=[]
        #sleep(2)
        #web_driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(5)
        products_links= web_driver.find_elements_by_class_name('productnamecolor.colors_productname')
        #print(len(products_links))
        for link in products_links:
            #link2=link.find_element_by_tag_name('a')
            #for link3 in link2:
            product=link.get_attribute('href')
            products_list.append(product)
        #print(len(products_list))
        #print(products_list)


        for product_link in products_list:
            #print(product_link)

            if 'combo' not in str(product_link) :
                web_driver.get(product_link)
                #web_driver.get('https://www.180smoke.ca/vuse-vype-epod-vpro-watermelon-cartridges-2pk')
                sleep(4)

                try:
                    page_title = web_driver.find_element_by_xpath('//*[@id="v65-product-parent"]/tbody/tr[1]/td/font/span').text
                    #print(page_title)
                    page_price = web_driver.find_element_by_xpath('//*[@id="v65-product-parent"]/tbody/tr[2]/td[2]/table[1]/tbody/tr/td/table/tbody/tr[2]/td[2]/table/tbody/tr[1]/td[1]/div/table/tbody/tr/td/font/div/b/span').text
                    #print(page_price)

                    product_veriety = web_driver.find_element_by_xpath('//*[@id="options_table"]/tbody/tr/td[3]/select').find_elements_by_tag_name('option')
                    if 'DEVICE' in str(page_title):
                        #stock_label_1 = web_driver.find_element_by_xpath('//*[@id="data-product-option-0"]/option[1]').get_attribute('outerHTML')
                        #print('Variants found')
                        #print(product_veriety)
                        variety_list_reference=['Black','Gold','Graphite','Rose Gold','Silver']
                        variety_list=[]
                        for prod in product_veriety:
                            variety_list.append(prod.text)

                        for variety_element in variety_list_reference:
                            if variety_element not in variety_list :
                                #print('1')
                                erp_list.append(website_erp)
                                product_price_list.append(page_price)
                                out_of_stock_titles.append(page_title)
                                out_of_stock_links.append(product_link)
                                out_of_stock_names.append(variety_element)
                                stock_description_list.append('Out of stock')
                                #print(len(erp_list),len(product_price_list),len(out_of_stock_titles),len(out_of_stock_links),len(out_of_stock_names),len(stock_description_list))
                                #print('OUT OF STOCK')
                            else:
                                #print('2')
                                erp_list.append(website_erp)
                                product_price_list.append(page_price)
                                out_of_stock_titles.append(page_title)
                                out_of_stock_links.append(product_link)
                                out_of_stock_names.append(variety_element)
                                stock_description_list.append('In stock')
                                #print(len(erp_list),len(product_price_list),len(out_of_stock_titles),len(out_of_stock_links),len(out_of_stock_names),len(stock_description_list))
                                #print('IN STOCK')

                    else:
                        variety_list_reference=['1.6%','3%','5%']
                        variety_list=[]
                        for prod in product_veriety:
                            variety_list.append(prod.text)


                        for variety_element in variety_list_reference:
                            if variety_element not in variety_list :
                                #print('3')
                                erp_list.append(website_erp)
                                product_price_list.append(page_price)
                                out_of_stock_titles.append(page_title)
                                out_of_stock_links.append(product_link)
                                out_of_stock_names.append(variety_element)
                                stock_description_list.append('Out of stock')
                                #print(len(erp_list),len(product_price_list),len(out_of_stock_titles),len(out_of_stock_links),len(out_of_stock_names),len(stock_description_list))
                                #print('OUT OF STOCK')
                            else:
                                #print('4')
                                erp_list.append(website_erp)
                                product_price_list.append(page_price)
                                out_of_stock_titles.append(page_title)
                                out_of_stock_links.append(product_link)
                                out_of_stock_names.append(variety_element)
                                stock_description_list.append('In stock')
                                #print(len(erp_list),len(product_price_list),len(out_of_stock_titles),len(out_of_stock_links),len(out_of_stock_names),len(stock_description_list))
                                #print('IN STOCK')

                except:
                    print('digitalimports product infos not found')
                    pass


                #print('5')
                #print(len(erp_list),len(product_price_list),len(out_of_stock_titles),len(out_of_stock_links),len(out_of_stock_names),len(stock_description_list))
                df = pd.DataFrame({'ERP':erp_list,'product link':out_of_stock_links ,'product title':out_of_stock_titles ,'product type':out_of_stock_names, 'product price':product_price_list ,'stock description':stock_description_list})
                #print(df )
                if len(df)>0:
                    df.to_csv('output/digitalimports stock.csv',index=False)
                else:
                    print('Digitalimports Dataframe lenght is 0')
    print('digitalimports finished')

########################################################################################################
########################################################################################################

def scrape_allyoucanvape_products():

    erp_list = []
    out_of_stock_names=[]
    out_of_stock_links=[]
    out_of_stock_titles=[]
    stock_description_list=[]
    product_price_list = []

    products_pages_list = ['https://www.allyoucanvape.ca/collections/vype-products-free-shipping']
    website_erp = 'AYCV erp'
    for website in products_pages_list:



        web_driver=webdriver.Chrome()
        web_driver.get(website)
        print('AllYouCanVape start now')
        sleep(5)

        web_driver.find_element_by_xpath('//*[@id="year"]/option[text()="{}"]'.format("""
            1970
          """)).click()
        web_driver.find_element_by_class_name('agp__birthdayType__button.agp__button').click()

        products_list=[]
        #sleep(2)
        #web_driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        products_divs= web_driver.find_elements_by_class_name('productitem--image-link')
        #wc_session = HTMLSession()
        #products_divs = wc_session.get(website).html.find('div.product-small.box')

        for divs in products_divs:
            #print('div treatment')
            product = divs.get_attribute('href')
            products_list.append(product)

        #print('products list length')
        #print(len(products_list))


        final_products_link_list = []
        final_products_variety_link_list = []
        final_out_of_stock_list = []
        out_of_stock_container = []
        for product_link in products_list:

            try:
                web_driver.get(product_link)
                #print(product_link)
                sleep(5)
                try:
                    web_driver.find_element_by_xpath('//*[@id="year"]/option[text()="{}"]'.format("""
                        1970
                      """)).click()
                    web_driver.find_element_by_class_name('agp__birthdayType__button.agp__button').click()
                    #print('closed')
                except:
                    pass
                sleep(5)


                if 'pods' in str(product_link):
                    #print('pods start')
                    product_first_name = web_driver.find_element_by_xpath('//*[@id="shopify-section-static-product"]/section[1]/article/div[2]/div[1]/h1').text
                    #print('pods Product first name: '+product_first_name)
                    try:
                        variety_elements = web_driver.find_element_by_xpath('//*[@id="product_form_4519574568995"]/div[1]/div[1]/div/select').find_elements_by_tag_name('option')
                        #print(str(len(variety_elements)) +' varieties found')
                        variety_names = web_driver.find_element_by_xpath('//*[@id="product_form_4519574568995"]/div[1]/div[1]/div/select').find_elements_by_tag_name('option')
                        #print('names found')
                        #print(str(len(variety_names)),'  ',str(len(variety_elements)) )
                        #print('variety names found')
                        #print(variety_names)

                        ##########################################################################################

                        for i in range(len(variety_elements)):
                            element=variety_elements[i]
                            pdt_name=variety_names[i].text
                            #if 'disabled' in str(element.get_attribute('outerHTML')) :
                            #    pdt_name=pdt_name[-15]
                            #print(pdt_name)
                            try:
                                element.click()
                                nicotine_variety = web_driver.find_element_by_xpath('//*[@id="product_form_4519574568995"]/div[1]/div[2]/div/select').find_elements_by_tag_name('option')
                                nicotine_variety_names = web_driver.find_element_by_xpath('//*[@id="product_form_4519574568995"]/div[1]/div[2]/div/select').find_elements_by_tag_name('option')
                                #print('nicotine variety names found')
                                product_price = web_driver.find_element_by_class_name('product--price').find_element_by_class_name('price--main').find_element_by_class_name('money').text
                                #print('Price: ' + product_price)
                                for i in range(len(nicotine_variety)):
                                    nicotine_element=nicotine_variety[i]
                                    nicotine_pdt_name=nicotine_variety_names[i].text
                                    #print(nicotine_element)
                                    #print(nicotine_pdt_name)
                                    if 'disabled' in str(nicotine_element.get_attribute('outerHTML')):
                                        #print('disabled found 1')
                                        final_out_of_stock = str(pdt_name)+' '+str(nicotine_pdt_name)
                                        final_page_title = str(product_first_name)+' '+str(pdt_name)
                                        final_variety_str = str(nicotine_pdt_name)
                                        #print(final_out_of_stock)
                                        if str(final_out_of_stock) not in out_of_stock_container:
                                            final_products_variety_link_list.append(nicotine_pdt_name)
                                            final_out_of_stock_list.append(product_first_name+' ' +pdt_name)
                                            final_products_link_list.append(product_link)
                                            out_of_stock_container.append(product_first_name+' '+str(final_out_of_stock))


                                            erp_list.append(website_erp)
                                            out_of_stock_names.append(final_variety_str)
                                            out_of_stock_links.append(product_link)
                                            out_of_stock_titles.append(final_page_title)
                                            stock_description_list.append('Out of stock')
                                            product_price_list.append(product_price)

                                    else:
                                        #print('no disabled')
                                        final_out_of_stock = str(pdt_name)+' '+str(nicotine_pdt_name)
                                        final_page_title = str(product_first_name)+' '+str(pdt_name)
                                        final_variety_str = str(nicotine_pdt_name)
                                        #print(final_out_of_stock)
                                        if str(final_out_of_stock) not in out_of_stock_container:
                                            final_products_variety_link_list.append(nicotine_pdt_name)
                                            final_out_of_stock_list.append(product_first_name+' ' +pdt_name)
                                            final_products_link_list.append(product_link)
                                            out_of_stock_container.append(product_first_name+' '+str(final_out_of_stock))


                                            erp_list.append(website_erp)
                                            out_of_stock_names.append(final_variety_str)
                                            out_of_stock_links.append(product_link)
                                            out_of_stock_titles.append(final_page_title)
                                            stock_description_list.append('In stock')
                                            product_price_list.append(product_price)


                                sleep(3)
                            except:
                                print('AYCV PBLM!')

                            #print('NO')
                    except:
                        pass





                elif 'device-kit' in str(product_link):
                    #print('device start')
                    product_first_name = web_driver.find_element_by_xpath('//*[@id="shopify-section-static-product"]/section[1]/article/div[2]/div[1]/h1').text
                    product_price = web_driver.find_element_by_class_name('product--price').find_element_by_class_name('price--main').find_element_by_class_name('money').text
                    #print('device Product first name: '+product_first_name)
                    #print('Product first name in device kit: '+product_first_name+' price: '+product_price)
                    try:
                        variety_elements = web_driver.find_element_by_xpath('//*[@id="product_form_4519499169827"]/div[1]/div/div/select').find_elements_by_tag_name('option')
                        #print(str(len(variety_elements)) +' varieties found')
                        variety_names    = web_driver.find_element_by_xpath('//*[@id="product_form_4519499169827"]/div[1]/div/div/select').find_elements_by_tag_name('option')
                        #print('names found')
                        #print(str(len(variety_names)),'  ',str(len(variety_elements)) )
                        #print('variety names found in device kit')
                        for i in range(len(variety_elements)):
                            element=variety_elements[i]
                            pdt_name=variety_names[i].text
                            #print(pdt_name)
                            if 'disabled' in str(element.get_attribute('outerHTML')):
                                #final_products_variety_link_list.append(pdt_name)
                                #final_out_of_stock_list.append(product_first_name)
                                #final_products_link_list.append(product_link)
                                #print('device out of stock')
                                erp_list.append(website_erp)
                                out_of_stock_names.append(pdt_name)
                                out_of_stock_links.append(product_link)
                                out_of_stock_titles.append(product_first_name)
                                stock_description_list.append('Out of stock')
                                product_price_list.append(product_price)
                            else:
                                #print('device in stock')
                                erp_list.append(website_erp)
                                out_of_stock_names.append(pdt_name)
                                out_of_stock_links.append(product_link)
                                out_of_stock_titles.append(product_first_name)
                                stock_description_list.append('In stock')
                                product_price_list.append(product_price)
                    except:
                        pass

                elif 'engraving' in str(product_link):
                    #print('engraving start')
                    product_first_name = web_driver.find_element_by_xpath('//*[@id="shopify-section-static-product"]/section[1]/article/div[2]/div[1]/h1').text
                    product_price = web_driver.find_element_by_class_name('product--price').find_element_by_class_name('price--main').find_element_by_class_name('money').text
                    #print('Product first name in engraving device: '+product_first_name+' price: '+product_price)
                    try:
                        variety_elements = web_driver.find_element_by_xpath('//*[@id="product_form_4562843893795"]/div[1]/div/div/select').find_elements_by_tag_name('option')
                        #print(str(len(variety_elements)) +' varieties found')
                        variety_names    = web_driver.find_element_by_xpath('//*[@id="product_form_4562843893795"]/div[1]/div/div/select').find_elements_by_tag_name('option')
                        #print('names found')
                        #print(str(len(variety_names)),'  ',str(len(variety_elements)) )
                        #print('variety names found in device kit')
                        for i in range(len(variety_elements)):
                            element=variety_elements[i]
                            pdt_name=variety_names[i].text
                            #print(pdt_name)
                            if 'disabled' in str(element.get_attribute('outerHTML')):
                                #final_products_variety_link_list.append(pdt_name)
                                #final_out_of_stock_list.append(product_first_name)
                                #final_products_link_list.append(product_link)
                                #print('device out of stock')
                                erp_list.append(website_erp)
                                out_of_stock_names.append(pdt_name)
                                out_of_stock_links.append(product_link)
                                out_of_stock_titles.append(product_first_name)
                                stock_description_list.append('Out of stock')
                                product_price_list.append(product_price)
                            else:
                                #print('device in stock')
                                erp_list.append(website_erp)
                                out_of_stock_names.append(pdt_name)
                                out_of_stock_links.append(product_link)
                                out_of_stock_titles.append(product_first_name)
                                stock_description_list.append('In stock')
                                product_price_list.append(product_price)
                    except:
                        pass

                elif '2-kit' in str(product_link):
                    #print('2-kit start')
                    product_first_name = web_driver.find_element_by_xpath('//*[@id="shopify-section-static-product"]/section[1]/article/div[2]/div[1]/h1').text
                    product_price = web_driver.find_element_by_class_name('product--price').find_element_by_class_name('price--main').find_element_by_class_name('money').text

                    #print('Product first name in 2-kit: '+product_first_name+' price: '+product_price)
                    try:
                        variety_elements = web_driver.find_element_by_xpath('//*[@id="product_form_6549494235171"]/div[1]/div/div/select').find_elements_by_tag_name('option')
                        #print(str(len(variety_elements)) +' varieties found')
                        variety_names    = web_driver.find_element_by_xpath('//*[@id="product_form_6549494235171"]/div[1]/div/div/select').find_elements_by_tag_name('option')
                        #print('names found')
                        #print(str(len(variety_names)),'  ',str(len(variety_elements)) )
                        #print('variety names found in device kit')
                        for i in range(len(variety_elements)):
                            element=variety_elements[i]
                            pdt_name=variety_names[i].text
                            #print(pdt_name)
                            if 'disabled' in str(element.get_attribute('outerHTML')):
                                #final_products_variety_link_list.append(pdt_name)
                                #final_out_of_stock_list.append(product_first_name)
                                #final_products_link_list.append(product_link)
                                #print('device out of stock')
                                erp_list.append(website_erp)
                                out_of_stock_names.append(pdt_name)
                                out_of_stock_links.append(product_link)
                                out_of_stock_titles.append(product_first_name)
                                stock_description_list.append('Out of stock')
                                product_price_list.append(product_price)
                            else:
                                #print('device in stock')
                                erp_list.append(website_erp)
                                out_of_stock_names.append(pdt_name)
                                out_of_stock_links.append(product_link)
                                out_of_stock_titles.append(product_first_name)
                                stock_description_list.append('In stock')
                                product_price_list.append(product_price)
                    except:
                        pass


                else:
                    pass
                    #print('key word not found in link allyoucanvape')


            except:
                pass


            #print('5')
            #print(len(erp_list),len(product_price_list),len(out_of_stock_titles),len(out_of_stock_links),len(out_of_stock_names),len(stock_description_list))
            df = pd.DataFrame({'ERP':erp_list,'product link':out_of_stock_links ,'product title':out_of_stock_titles ,'product type':out_of_stock_names, 'product price':product_price_list ,'stock description':stock_description_list})
            #print(df )
            if len(df)>0:
                df.to_csv('output/allyoucanvape stock.csv',index=False)
            else:
                print('AYCV Dataframe lenght is 0')
    print('AllYouCanVape finished')

########################################################################################################
########################################################################################################



########################################################################################################
########################################################################################################



print('threading will start now')

t1  = threading.Thread(target=scrape_180smoke_products)
t2  = threading.Thread(target=scrape_canvape_products)
t3  = threading.Thread(target=scrape_in2vapes_products)
t4  = threading.Thread(target=scrape_dragonvape_products)
t5  = threading.Thread(target=scrape_hazetownvapes_products)
t6  = threading.Thread(target=scrape_vapesbyenushi_products)
t7  = threading.Thread(target=scrape_vapevine_products)
t8  = threading.Thread(target=scrape_ftpanda_products)
t9  = threading.Thread(target=scrape_vapemeet_products)
t10 = threading.Thread(target=scrape_digitalimports_products)
t11 = threading.Thread(target=scrape_allyoucanvape_products)

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
t7.start()
t8.start()
t9.start()
t10.start()
t11.start()

t1.join()
t2.join()
t3.join()
t4.join()
t5.join()
t6.join()
t7.join()
t8.join()
t9.join()
t10.join()
t11.join()
