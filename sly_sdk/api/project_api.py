# coding: utf-8
"""create/download/update :class:`Project<supervisely.project.project.Project>`"""

# docs
from __future__ import annotations

from typing import Dict, NamedTuple, Optional

from supervisely._utils import abs_url, compress_image_url, is_development
from supervisely.api.module_api import (
    ApiField,
    CloneableModuleApi,
    RemoveableModuleApi,
    UpdateableModule,
)
from supervisely.project.project_meta import ProjectMetaJsonFields as MetaJsonF
from supervisely.project.project_settings import (
    ProjectSettings,
    ProjectSettingsJsonFields,
)
from supervisely.project.project_type import ProjectType


class ProjectNotFound(Exception):
    """ """

    pass


class ExpectedProjectTypeMismatch(Exception):
    """ """

    pass


class ProjectInfo(NamedTuple):
    """ """

    id: int
    name: str
    description: str
    size: int
    readme: str
    workspace_id: int
    images_count: int  # for compatibility with existing code
    items_count: int
    datasets_count: int
    created_at: str
    updated_at: str
    type: str
    reference_image_url: str
    custom_data: dict
    backup_archive: dict
    team_id: int
    settings: dict
    import_settings: dict
    version: dict
    created_by_id: int

    @property
    def image_preview_url(self):
        if self.type in [str(ProjectType.POINT_CLOUDS), str(ProjectType.POINT_CLOUD_EPISODES)]:
            res = "https://user-images.githubusercontent.com/12828725/199022135-4161917c-05f8-4681-9dc1-b5e10ee8bb0f.png"
        else:
            res = self.reference_image_url
            if is_development():
                res = abs_url(res)
            res = compress_image_url(url=res, height=200)
        return res

    @property
    def url(self):
        res = f"projects/{self.id}/datasets"
        if is_development():
            res = abs_url(res)
        return res


class ProjectApi(CloneableModuleApi, UpdateableModule, RemoveableModuleApi):
    """
    API for working with :class:`Project<supervisely.project.project.Project>`. :class:`ProjectApi<ProjectApi>` object is immutable.

    :param api: API connection to the server
    :type api: Api
    :Usage example:

     .. code-block:: python

        import os
        from dotenv import load_dotenv

        import supervisely as sly

        # Load secrets and create API object from .env file (recommended)
        # Learn more here: https://developer.supervisely.com/getting-started/basics-of-authentication
        if sly.is_development():
            load_dotenv(os.path.expanduser("~/supervisely.env"))
        api = sly.Api.from_env()

        # Pass values into the API constructor (optional, not recommended)
        # api = sly.Api(server_address="https://app.supervise.ly", token="4r47N...xaTatb")

        project_id = 1951
        project_info = api.project.get_info_by_id(project_id)
    """

    @staticmethod
    def info_sequence():
        """
        NamedTuple ProjectInfo with API Fields containing information about Project.

        :Example:

         .. code-block:: python

            ProjectInfo(id=999,
                        name='Cat_breeds',
                        description='',
                        size='861069',
                        readme='',
                        workspace_id=58,
                        images_count=10,
                        items_count=10,
                        datasets_count=2,
                        created_at='2020-11-17T17:44:28.158Z',
                        updated_at='2021-03-01T10:51:57.545Z',
                        type='images',
                        reference_image_url='http://app.supervise.ly/h5un6l2bnaz1vj8a9qgms4-public/images/original/...jpg',
                        custom_data={},
                        backup_archive={},
                        team_id=2,
                        import_settings={}
                        version={'id': 260, 'version': 3}
                        )
        """
        return [
            ApiField.ID,
            ApiField.NAME,
            ApiField.DESCRIPTION,
            ApiField.SIZE,
            ApiField.README,
            ApiField.WORKSPACE_ID,
            ApiField.IMAGES_COUNT,  # for compatibility with existing code
            ApiField.ITEMS_COUNT,
            ApiField.DATASETS_COUNT,
            ApiField.CREATED_AT,
            ApiField.UPDATED_AT,
            ApiField.TYPE,
            ApiField.REFERENCE_IMAGE_URL,
            ApiField.CUSTOM_DATA,
            ApiField.BACKUP_ARCHIVE,
            ApiField.TEAM_ID,
            ApiField.SETTINGS,
            ApiField.IMPORT_SETTINGS,
            ApiField.VERSION,
            ApiField.CREATED_BY_ID,
        ]

    @staticmethod
    def info_tuple_name():
        """
        NamedTuple name - **ProjectInfo**.
        """
        return "ProjectInfo"

    def __init__(self, api):
        from supervisely.project.data_version import DataVersion

        CloneableModuleApi.__init__(self, api)
        UpdateableModule.__init__(self, api)
        self.version = DataVersion(api)

    def get_info_by_id(
        self,
        id: int,
        expected_type: Optional[str] = None,
        raise_error: Optional[bool] = False,
    ) -> ProjectInfo:
        """
        Get Project information by ID.

        :param id: Project ID in Supervisely.
        :type id: int
        :param expected_type: Expected ProjectType.
        :type expected_type: ProjectType, optional
        :param raise_error: If True raise error if given name is missing in the Project, otherwise skips missing names.
        :type raise_error: bool, optional
        :raises: Error if type of project is not None and != expected type
        :return: Information about Project. See :class:`info_sequence<info_sequence>`
        :rtype: :class:`ProjectInfo`
        :Usage example:

         .. code-block:: python

            import supervisely as sly

            project_id = 1951

            os.environ['SERVER_ADDRESS'] = 'https://app.supervisely.com'
            os.environ['API_TOKEN'] = 'Your Supervisely API Token'
            api = sly.Api.from_env()

            project_info = api.project.get_info_by_id(project_id)
            print(project_info)
            # Output: ProjectInfo(id=861,
            #                     name='fruits_annotated',
            #                     description='',
            #                     size='22172241',
            #                     readme='',
            #                     workspace_id=58,
            #                     images_count=6,
            #                     items_count=6,
            #                     datasets_count=1,
            #                     created_at='2020-11-09T18:21:32.356Z',
            #                     updated_at='2020-11-09T18:21:32.356Z',
            #                     type='images',
            #                     reference_image_url='http://78.46.75.100:38585/h5un6l2bnaz1vj8a9qgms4-public/images/original/...jpg',
            #                     custom_data={},
            #                     backup_archive={},
            #                     import_settings={}
            #                   )


        """
        info = self._get_info_by_id(id, "projects.info")
        self._check_project_info(info, id=id, expected_type=expected_type, raise_error=raise_error)
        return info

    def _check_project_info(
        self,
        info,
        id: Optional[int] = None,
        name: Optional[str] = None,
        expected_type=None,
        raise_error=False,
    ):
        """
        Checks if a project exists with a given id and type of project == expected type
        :param info: project metadata information
        :param id: int
        :param name: str
        :param expected_type: type of data we expext to get info
        :param raise_error: bool
        """
        if raise_error is False:
            return

        str_id = ""
        if id is not None:
            str_id += "id: {!r} ".format(id)
        if name is not None:
            str_id += "name: {!r}".format(name)

        if info is None:
            raise ProjectNotFound("Project {} not found".format(str_id))
        if expected_type is not None and info.type != str(expected_type):
            raise ExpectedProjectTypeMismatch(
                "Project {!r} has type {!r}, but expected type is {!r}".format(
                    str_id, info.type, expected_type
                )
            )

    def get_meta(self, id: int, with_settings: bool = False) -> Dict:
        """
        Get ProjectMeta by Project ID.

        :param id: Project ID in Supervisely.
        :type id: int
        :param with_settings: Add settings field to the meta. By default False.
        :type with_settings: bool

        :return: ProjectMeta dict
        :rtype: :class:`dict`
        :Usage example:

         .. code-block:: python

            import supervisely as sly

            os.environ['SERVER_ADDRESS'] = 'https://app.supervisely.com'
            os.environ['API_TOKEN'] = 'Your Supervisely API Token'
            api = sly.Api.from_env()

            project_meta = api.project.get_meta(project_id)
            print(project_meta)
            # Output: {
            #     "classes":[
            #         {
            #             "id":22310,
            #             "title":"kiwi",
            #             "shape":"bitmap",
            #             "hotkey":"",
            #             "color":"#FF0000"
            #         },
            #         {
            #             "id":22309,
            #             "title":"lemon",
            #             "shape":"bitmap",
            #             "hotkey":"",
            #             "color":"#51C6AA"
            #         }
            #     ],
            #     "tags":[],
            #     "projectType":"images"
            # }
        """
        json_response = self._api.post("projects.meta", {"id": id}).json()

        if with_settings is True:
            json_settings = self.get_settings(id)
            mtag_name = None

            if json_settings.get("groupImagesByTagId") is not None:
                for tag in json_response["tags"]:
                    if tag["id"] == json_settings["groupImagesByTagId"]:
                        mtag_name = tag["name"]
                        break

            json_response[MetaJsonF.PROJECT_SETTINGS] = ProjectSettings(
                multiview_enabled=json_settings.get("groupImages", False),
                multiview_tag_name=mtag_name,
                multiview_tag_id=json_settings.get("groupImagesByTagId"),
                multiview_is_synced=json_settings.get("groupImagesSync", False),
                labeling_interface=json_settings.get(ProjectSettingsJsonFields.LABELING_INTERFACE),
            ).to_json()

        return json_response

    def _convert_json_info(self, info: dict, skip_missing=True) -> ProjectInfo:
        """ """
        res = super()._convert_json_info(info, skip_missing=skip_missing)
        if res.reference_image_url is not None:
            res = res._replace(reference_image_url=res.reference_image_url)
        if res.items_count is None:
            res = res._replace(items_count=res.images_count)
        return ProjectInfo(**res._asdict())

    def url(self, id: int) -> str:
        """
        Get Project URL by ID.

        :param id: Project ID in Supervisely.
        :type id: int
        :return: Project URL
        :rtype: :class:`str`
        :Usage example:

         .. code-block:: python

            import supervisely as sly

            project_id = 1951

            os.environ['SERVER_ADDRESS'] = 'https://app.supervisely.com'
            os.environ['API_TOKEN'] = 'Your Supervisely API Token'
            api = sly.Api.from_env()

            project_url = api.project.url(project_id)
            print(project_url)
            # Output: http://supervise.ly/projects/1951/datasets
        """
        res = f"projects/{id}/datasets"
        if is_development():
            res = abs_url(res)
        return res

    def get_settings(self, id: int) -> Dict[str, str]:
        info = self._get_info_by_id(id, "projects.info")
        return info.settings
