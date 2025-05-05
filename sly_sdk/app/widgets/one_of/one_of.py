from typing import Dict
from sly_sdk.app.widgets.widget import Widget, ConditionalWidget


class OneOf(Widget):
    def __init__(
        self,
        conditional_widget: ConditionalWidget,
        widget_id: str = None,
    ):
        self._conditional_widget = conditional_widget
        super().__init__(widget_id=widget_id)

    def get_json_data(self) -> Dict:
        return {}

    def get_json_state(self) -> Dict:
        return {}
