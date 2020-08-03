import os
from ListManager import ListManager
from Manga import Manga
from scrappers.LireScanScrapper import LireScanScrapper


liste_manager = ListManager()

for entry in liste_manager.lirescan_list:
    manga = Manga(entry["name"], entry["url"], entry["last_chapter"])
    # check if manga dir exist, if not, creates it
    dir_name = './images/'+manga.dir_name+'/'
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)

    for url in manga.url:
        site = url.split('/')[2].split('.')[1]
        if site == "lirescan":
            scrapper = LireScanScrapper(manga, url)
            scrapper.cycleChapter(manga.dir_name)
            liste_manager.updateLastChapter(manga, scrapper.previous_chapter)
