import re


class Manga():
    '''
    This object is just here to provide manga informations as the script goes on in order to download each pages
    '''

    name = ""
    url = []
    chapter = 0
    dir_name = ""

    def __init__(self, name, url, chapter=0):
        self.name = name
        self.url = url
        self.chapter = chapter
        dir_name = name.lower()
        dir_name = re.sub('[^A-Za-z0-9]+', ' ', dir_name)
        dir_name = dir_name.split(' ')
        dir_name = '-'.join(dir_name)
        self.dir_name = dir_name
