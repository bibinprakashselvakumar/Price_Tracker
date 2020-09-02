import json
from datetime import datetime

from selenium.webdriver.common.keys import Keys

from price_tracker.test import (
    get_web_driver_options,
    set_browser_as_incognito,
    get_chrome_web_driver,
    name,
    filters,
    base_url,
    currency
)


class generate_report:
    def __init__(self, file_name, filters, base_link, currency, data):
        self.data = data
        self.file_name = file_name
        self.filters = filters
        self.base_link = base_link
        self.currency = currency
        sorted(data, key=lambda k: k['price'])
        report = {
            'title': self.file_name,
            'date': self.get_now(),
            'best_item': self.get_best_item(),
            'products': self.data
        }
        print("Creating Report")
        try:
            filname = file_name + '.json'
            f = open(filname, 'w+')
            json.dump(report, f)
            f.close()
        except Exception as e:
            print(e)
            print("Unable to create the Report")
        print("Done")

    def get_now(self):
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")

    def get_best_item(self):
        try:
            return sorted(data, key=lambda k: k['price'])[0]
        except Exception as e:
            print(e)
            print("Error Sorting items")
            return None


class amazon_api:
    def __init__(self, search_term, filters, base_url, currency):
        self.search_term = search_term
        self.base_url = base_url
        options = get_web_driver_options()
        set_browser_as_incognito(options)
        self.driver = get_chrome_web_driver(options)
        self.currency = currency
        self.price_filter = f"&i=videogames&rh=n%3A976460031%2Cp_36%3A{filters['min']}00-{filters['max']}00"

    def run(self):
        print("Starting script...")
        print(f"Looking for {self.search_term}...")
        links = self.get_product_links()
        if not links:
            print("Scraping Ended...")
            self.driver.quit()
            return
        print(f"Got {len(links)} links...")
        print("Getting info about games...")
        products = self.get_products_info(links)
        print(f"Got info for {len(products)} products...")
        self.driver.quit()
        return products

    def get_products_info(self, links):
        asins = self.get_asins(links)
        products = []
        i = 1
        for asin in asins:
            product = self.get_single_product_info(asin, i)
            if product:
                products.append(product)
            i += 1
        return products

    def get_single_product_info(self, asin, i):
        print(f"{i} Product ID: {asin} => Getting Info...")
        product_short_url = self.base_url + '/dp/' + asin
        self.driver.get(f'{product_short_url}')
        title = self.get_title()
        seller = self.get_seller()
        price = self.get_price()
        if title and seller and price:
            product_info = {
                'asin': asin,
                'url': product_short_url,
                'title': title,
                'seller': seller,
                'price': price
            }
            return product_info
        return None

    def get_title(self):
        return self.driver.find_element_by_id("productTitle").text

    def get_seller(self):
        return self.driver.find_element_by_id("sellerProfileTriggerId").text

    def get_price(self):
        price = self.driver.find_element_by_id("priceblock_ourprice").text.strip()
        p1 = price.replace(',', '')
        if p1.find('.'):
            return float(p1)
        else:
            p2 = p1 + '.00'
            return float(p2)

    def get_asins(self, links):
        return [self.get_asin(link) for link in links]

    def get_asin(self, product_link):
        return product_link.split("/ref")[0].split("/dp/")[1]

    def get_product_links(self):
        self.driver.get(self.base_url)
        element = self.driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
        element.send_keys(self.search_term)
        element.send_keys(Keys.ENTER)
        self.driver.get(f'{self.driver.current_url}{self.price_filter}')
        result_list = self.driver.find_elements_by_class_name('s-result-list')
        links = []
        try:
            results = result_list[1].find_elements_by_xpath('//div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div['
                                                            '1]/h2/a')
            links = [link.get_attribute('href') for link in results]
            return links
        except Exception as e:
            print("Didn't find any product...")
            print(e)
            return links


if __name__ == '__main__':
    amazon = amazon_api(name, filters, base_url, currency)
    data = amazon.run()
    generate_report(name, filters, base_url, currency, data)
