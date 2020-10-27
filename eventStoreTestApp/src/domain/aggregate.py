import uuid
import requests
from src import CONFIG


class Aggregate:

    def __init__(self):
        self.aggregate_id = uuid.uuid4()
        self.version = 0

    def apply_event_effects_to_aggregate(self, event_json):
        pass

    def raise_event(self, event):
        event.execute()

    """
    def subscribe(self, stream, group):
        request = requests.put(f"{CONFIG.EVENTSTORE_SUBSCRIPTION_URL}/{stream}/{group}",
                               data={"startFrom": "0",
                                     "resolveLinktos": "false"})
    """

    def load_up(self):
        version = self.version
        while True:
            request = requests.get(f"{CONFIG.EVENTSTORE_STREAM_URL}/{self.aggregate_id}/{version}",
                                   headers={"Accept": "application/vnd.eventstore.atom+json"})
            if request.status_code == 200:
                self.apply_event_effects_to_aggregate(request.json())
                version += 1
            else:
                break
        self.version = version
