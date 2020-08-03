from notifypy import Notify


class Notifier():

    notification = Notify()

    def send(self, title, content, icon=None):
        self.notification.title = title
        self.notification.message = content
        if icon != None:
            self.notification.icon = icon
        self.notification.send()

    def prepare(self, name):
        title = 'Manga Scrapper'
        content = 'Un nouveau chaptire de '+name + \
            ' a été téléchargé. Cliquez ici pour ouvrir'
        self.send(title, content)
