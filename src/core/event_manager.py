class EventManager:
    """
    Gestionnaire d'événements pour le robot.
    """

    def __init__(self):
        self.events = []

    def trigger(self, event_name, data=None):
        self.events.append((event_name, data))

    def get_events(self):
        events = self.events[:]
        self.events.clear()
        return events