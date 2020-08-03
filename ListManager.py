import json
import os


class ListManager():
    '''
    An object used to manage the list of tracked mangas to download
    '''

    mangas_list = {}
    lirescan_list = []

    def __init__(self):
        with open('mangas_list.json', 'r+') as json_file:
            self.mangas_list = json.load(json_file)
            for manga in self.mangas_list["lirescan"]:
                self.lirescan_list.append(manga)

    def addManga(self, manga):
        # Adds a manga to the list variable using a Manga() object
        new_manga = {}
        new_manga["name"] = manga.name
        new_manga["dir_name"] = manga.dir_name
        new_manga["url"] = manga.url
        new_manga["last_chapter"] = manga.chapter
        is_already_added = False
        for i in self.lirescan_list:
            if manga.name == i["name"]:
                print('Vous suivez déjà ce manga')
                is_already_added = True
                break
        if not is_already_added:
            self.lirescan_list.append(new_manga)
            self.mangas_list["lirescan"] = self.lirescan_list
        self.updateFile(self.mangas_list)

    def updateFile(self, mangas_list):
        # Write the modification to the file tracking all the mangas
        with open('mangas_list.json', 'w') as json_file:
            json.dump(self.mangas_list, json_file)

    def updateLastChapter(self, manga, chapter):
        # Just increment the last chapter downloaded var of the current manga
        for i in self.lirescan_list:
            if i["name"] == manga.name:
                i["last_chapter"] = chapter
                self.mangas_list["lirescan"] = self.lirescan_list
                self.updateFile(self.mangas_list)
                break
