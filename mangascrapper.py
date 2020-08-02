import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import requests
import os
from urllib.parse import urlparse
import re
from Notifier import Notifier

# instantiate a chrome options object so you can set the size and headless preference
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(chrome_options=chrome_options,
                          executable_path='./chromedriver')
driver.get('https://www.lirescan.me/my-hero-academia-lecture-en-ligne/279/')
time.sleep(1)
is_last_chapter = False

notifier = Notifier()

# TODO put these var in a separated file to make adding mangas possible
manga_name = "my_hero_academia_"
previous_chapter = 275

while is_last_chapter == False:

    # locating the chapter selector
    chapter_selector = Select(driver.find_element_by_name('chapitres'))
    options = chapter_selector.options
    if int(options[0].text) == previous_chapter:
        is_last_chapter = True
    else:

        # finding the next chapter not downloaded
        for i in reversed(options):
            if int(i.text) > previous_chapter:
                previous_chapter = int(i.text)
                chapter = i.text
                i.click()
                break

        # getting the correct number of pages in the chapter
        page_select = driver.find_elements_by_class_name(
            'page-link')
        for i in range(len(page_select)):
            if page_select[i].text == 'Suiv':
                nb_pages = page_select[i-1].text
                break

        # checking if the image is png or jpg
        src = driver.find_element_by_id(
            'image_scan').get_attribute('src')
        parsed = urlparse(src)
        root, ext = os.path.splitext(parsed.path)

        # TODO Add the verifiaction on US version
        # checking if the images are correctly named. This is to prevent downloading us version of scan
        image_checker = root.rsplit('/', 6)[6]
        if re.search(r'^\d\d', image_checker):
            print('test')

            # creating the dir to put the images sorted by chapters
            dir_name = './images/my-hero-academia/'+chapter+'/'
            if not os.path.isdir(dir_name):
                os.mkdir(dir_name)

            # getting the generic link to the asset
            src = driver.find_element_by_id(
                'image_scan').get_attribute('src').rsplit('/', 1)[0]

            # downloading all the pages for the chapter
            page = 0
            for i in range(int(nb_pages)+1):
                page_nb = "%02d" % page
                picture_name = manga_name+chapter+"_"+str(page)+ext

                # preventing missnamed files on the website (ie : 00.png instead of 01.png)
                response = requests.get(src+'/'+page_nb+ext)
                if response.status_code == 200:
                    with open(dir_name+picture_name, "wb") as f:
                        f.write(requests.get(src+'/'+page_nb+ext).content)
                page += 1
            notifier.prepare(manga_name)
print('pas de nouveau chapitres')
