import json
import re
from time import sleep

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from tqdm import tqdm


def make_driver():
    """Creates headless Firefox WebDriver instance."""
    firefox_options = Options()
    firefox_options.add_argument('-headless')
    return Firefox(options=firefox_options)


driver = make_driver()
page = "https://www.ycombinator.com/companies"


def get_page_source():
    """Returns the source of the current page."""
    driver.get(page)


def click_see_all_options():
    """Clicks 'See all options' button to load checkboxes for all batches."""
    sleep(3)
    see_all_options = driver.find_element(By.LINK_TEXT, 'See all options')
    see_all_options.click()


def compile_batches():
    """Returns elements of checkboxes from all batches."""
    pattern = re.compile(r'^(W|S|IK)[012]')
    bx = driver.find_elements(By.XPATH, '//label')
    for element in bx:
        if pattern.match(element.text):
            yield element


def scroll_to_bottom():
    """Scrolls to the bottom of the page."""

    # get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # scroll down to bottom
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # wait to load page
        sleep(3)

        # calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def fetch_url_paths():
    """Returns a generator with url paths for all companies."""
    # contains 'companies' but not 'founders'
    elements = driver.find_elements(
        By.XPATH, ('//a[contains(@href,"/companies/") and not(contains(@href,"founders"))]'))
    for url in elements:
        yield url.get_attribute('href')


def write_urls_to_file(ul: list):
    """Appends a list of company urls to a file."""
    with open('./scrapy-project/ycombinator/start_urls.txt', 'w') as f:
        json.dump(ul, f)


def yc_links_extractor():
    """Run the main script to write all start urls to a file."""
    print(f"Attempting to scrape links from {page}.")
    get_page_source()
    click_see_all_options()
    # compile an array of batches (checkbox elements)
    batches = compile_batches()
    ulist = []

    for b in tqdm(list(batches)):
        # filter companies
        b.click()

        # scroll down to load all companies
        scroll_to_bottom()

        # fetch links and append them to ulist
        urls = [u for u in fetch_url_paths()]
        ulist.extend(urls)

        # uncheck the batch checkbox
        b.click()
    
    write_urls_to_file(ulist)
    driver.quit()


if __name__ == '__main__':
    yc_links_extractor()
