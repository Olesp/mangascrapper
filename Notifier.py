from notifypy import Notify


class Notifier():

    notification = Notify()

    def send(self, title, content, icon=None):
        # TODO add the code to send the notification to the user when a new entry is passed
        self.notification.title = title
        self.notification.message = content
        if icon != None:
            self.notification.icon = icon
        self.notification.send()

    def prepare(self, manga):
        title = 'Manga Scrapper'
        content = 'Un nouveau chaptire de '+manga + \
            ' a été téléchargé. Cliquez ici pour ouvrir'
        self.send(title, content)
