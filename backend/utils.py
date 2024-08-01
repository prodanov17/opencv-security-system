import json


def load_config(filename):
    with open(filename, 'r') as file:
        config = json.load(file)
    return config


def resolve_storage(storage_name):
    if storage_name == 'LocalStorage':
        from storage.local_storage import LocalStorage
        return LocalStorage()
    else:
        raise ValueError(f"Unknown storage method: {storage_name}")


def resolve_notification(notification_name):
    if notification_name == 'SmsToNotification':
        from notification.smsto_notification import SmsToNotification
        return SmsToNotification()
    elif notification_name == 'DummyNotification':
        from notification.dummy_notification import DummyNotification
        return DummyNotification()
    elif notification_name == 'PushoverNotification':
        from notification.pushover import PushoverNotification
        return PushoverNotification()
    else:
        raise ValueError(f"Unknown notification method: {notification_name}")
