from notification.notification import Notification


class DummyNotification(Notification):
    def notify(self, message):
        print(message)
