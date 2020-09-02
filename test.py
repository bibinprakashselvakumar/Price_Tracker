from selenium import webdriver


name = 'ps4 games'
currency = '₹'
MIN_PRICE = '1000'
MAX_PRICE = '2000'
filters = {
    'min': MIN_PRICE,
    'max': MAX_PRICE
}
base_url = "https://www.amazon.in"


def get_chrome_web_driver(options):
    return webdriver.Chrome('./chromedriver.exe', options=options)


def get_web_driver_options():
    return webdriver.ChromeOptions()


def set_browser_as_incognito(options):
    options.add_argument('--incognito')


