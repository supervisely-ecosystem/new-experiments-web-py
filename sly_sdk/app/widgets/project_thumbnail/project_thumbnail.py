from sly_sdk._utils import abs_url, is_debug_with_sly_net, is_development
from sly_sdk.app.widgets.widget import Widget
from sly_sdk.webpy.app import DataJson
from sly_sdk.api.project_api import ProjectInfo


class ProjectThumbnail(Widget):
    def __init__(
        self,
        info: ProjectInfo = None,
        widget_id: str = None,
        remove_margins: bool = False,
        description: str = None,
    ):
        self._info: ProjectInfo = None
        self._id: int = None
        self._name: str = None
        self._description: str = description
        self._url: str = None
        self._image_preview_url: str = None
        self._remove_margins: bool = remove_margins
        self._set_info(info, description=description)

        super().__init__(widget_id=widget_id)

    def get_json_data(self):
        return {
            "id": self._id,
            "name": self._name,
            "description": self._description,
            "url": self._url,
            "image_preview_url": self._image_preview_url,
            "removeMargins": self._remove_margins,
        }

    def get_json_state(self):
        return None

    def _set_info(self, info: ProjectInfo = None, description: str = None):
        if info is None:
            return
        self._info = info
        self._id = info.id
        self._name = info.name
        if description is not None:
            self._description = description
        else:
            self._description = f"{info.items_count} {info.type} in project"

        self._url = f"/projects/{info.id}/datasets"
        if is_development() or is_debug_with_sly_net():
            self._url = abs_url(self._url)

        self._image_preview_url = info.image_preview_url
        if is_development() or is_debug_with_sly_net():
            self._image_preview_url = abs_url(self._image_preview_url)

    def set(self, info: ProjectInfo):
        self._set_info(info)
        self.update_data()
        DataJson().send_changes()
