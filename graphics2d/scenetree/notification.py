

class Notification:
    """
    Small helper class to represent unique notifications.

    Giving a notification a name might help with debugging, but has no other
    purpose and provides no additional functionality.
    """
    notification_id = 0

    def __init__(self, name, *args):
        """
        name will be stored with the instance. additional args are used
        to document the signal callback arguments and will be ignored.
        """
        Notification.notification_id += 1
        self.notification_id = Notification.notification_id
        self.name = name

    def __repr__(self):
        return f"<notification {self.name}>"


def listen(item: 'SceneItem', notification: 'Notification', callback):
        """
        Binds a listener callback to a notification from a scene item

        The callback's first parameter is the SceneItem.
        """
        #TODO: We should probably use weakrefs for the callbacks!
        if not notification in item.listeners:
            item.listeners[notification] = []
        item.listeners[notification].append(callback)