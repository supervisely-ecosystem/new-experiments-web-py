from typing import List

from sly_sdk.webpy.app import StateJson
from sly_sdk.app.widgets.widget import Widget


class Stepper(Widget):
    def __init__(
        self,
        titles: List = None,
        widgets: List = None,
        active_step: int = 1,
        widget_id: str = None,
    ):
        if widgets is None:
            widgets = []
        if titles is None:
            titles = []
        self.titles = titles
        if len(titles) == 0:
            titles = ['' for x in range(len(widgets))]
        self.content = list(zip(titles, widgets))
        self.active_step = active_step
        super().__init__(widget_id=widget_id)

    def get_json_data(self):
        return None

    def get_json_state(self):
        return {'active_step': self.active_step}
    
    def set_active_step(self, value: int):
        self.active_step = value
        StateJson()[self.widget_id]["active_step"] = self.active_step
        StateJson().send_changes()

    def get_active_step(self) -> str:
        return StateJson()[self.widget_id]["active_step"]
