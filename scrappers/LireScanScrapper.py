import time
import re
import os
import requests
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from Notifier import Notifier

# Notifier to notify the user when a new chapter of a manga is downloaded
notifier = Notifier()


class LireScanScrapper():

    is_last_chapter = False
    driver = ""
    previous_chapter = 0
    name = ""
    options = ""

    def __init__(self, manga, url):

        # instantiate a chrome options object so you can set the size and headless preference
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")

        self.driver = webdriver.Chrome(
            chrome_options=chrome_options,
            executable_path='./chromedriver')
        self.driver.get(url)
        time.sleep(1)
        self.name = manga.name
        self.previous_chapter = manga.chapter

    def checkLastChapter(self):
        # locating the chapter selector
        chapter_selector = Select(
            self.driver.find_element_by_name('chapitres'))
        options = chapter_selector.options
        # TODO ajouter une vérifiaction pour l'élément avertissant que c'est une version US et skip le chapitre si c'est le cas
        if int(options[0].text) == self.previous_chapter:
            self.is_last_chapter = True
            return False
        else:
            self.options = options
            return True

    def cycleChapter(self, dir_name):
        while self.checkLastChapter():
            # finding the next chapter not downloaded
            for i in reversed(self.options):
                if int(i.text) > self.previous_chapter:
                    self.previous_chapter = int(i.text)
                    chapter = i.text
                    i.click()
                    time.sleep(1)
                    break
            self.downloadPages(chapter, dir_name)
            notifier.prepare(self.name)

    def downloadPages(self, chapter, dir_name):
        # getting the correct number of pages in the chapter
        page_select = self.driver.find_elements_by_class_name(
            'page-link')
        for i in range(len(page_select)):
            if page_select[i].text == 'Suiv':
                nb_pages = page_select[i-1].text
                break

        # checking if the image is png or jpg
        src = self.driver.find_element_by_id(
            'image_scan').get_attribute('src')
        parsed = urlparse(src)
        root, ext = os.path.splitext(parsed.path)

        # checking if the images are correctly named.
        image_checker = root.rsplit('/', 6)[6]
        if re.search(r'^\d\d', image_checker):

            # creating the dir to put the images sorted by chapters
            dir_name = './images/'+dir_name+'/'+chapter+'/'
            if not os.path.isdir(dir_name):
                os.mkdir(dir_name)

            # getting the generic link to the asset
            src = self.driver.find_element_by_id(
                'image_scan').get_attribute('src').rsplit('/', 1)[0]
            # downloading all the pages for the chapter
            page = 0
            for i in range(int(nb_pages)+1):
                page_nb = "%02d" % page
                picture_name = self.name+chapter+"_"+str(page)+ext

                # preventing missnamed files on the website (ie : 00.png instead of 01.png)
                response = requests.get(src+'/'+page_nb+ext)
                if response.status_code == 200:
                    with open(dir_name+picture_name, "wb") as f:
                        f.write(requests.get(src+'/'+page_nb+ext).content)

                page += 1
