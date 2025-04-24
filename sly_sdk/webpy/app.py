import asyncio
import enum
import json
import tarfile
import time
from typing import List, NamedTuple, Optional
from fastapi import FastAPI
import numpy as np
from sly_sdk.sly_logger import logger


def get_or_create_event_loop():
    """
    Get the current event loop or create a new one if it doesn't exist.
    Works for different Python versions and contexts.

    :return: Event loop
    :rtype: asyncio.AbstractEventLoop
    """
    import asyncio

    try:
        # Preferred method for asynchronous context (Python 3.7+)
        return asyncio.get_running_loop()
    except RuntimeError:
        # If the loop is not running, get the current one or create a new one (Python 3.8 and 3.9)
        try:
            return asyncio.get_event_loop()
        except RuntimeError:
            # For Python 3.10+ or if the call occurs outside of an active loop context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop


def await_async(coro):
    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(coro)
    return res


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        local = kwargs.pop("__local__", False)
        if local is False:
            if cls not in cls._instances:
                cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            return cls._instances[cls]
        else:
            return super(Singleton, cls).__call__(*args, **kwargs)


class Field(str, enum.Enum):
    STATE = "state"
    DATA = "data"
    CONTEXT = "context"


class FigureInfo(NamedTuple):
    id: int
    class_id: int
    updated_at: str
    created_at: str
    entity_id: int
    object_id: int
    project_id: int
    dataset_id: int
    frame_index: int
    geometry_type: str
    geometry: dict
    geometry_meta: dict
    tags: list
    meta: dict
    area: str
    priority: Optional[int] = None
    version: int = 0

    def clone(self, **kwargs):
        return self._replace(**kwargs)


class FigureObj:
    attr_name = {
        "id": "id",
        "class_id": "classId",
        "updated_at": "updatedAt",
        "created_at": "createdAt",
        "object_id": "objectId",
        "geometry_type": "_geometryType",
        "tags": "tags",
        "meta": "meta",
        "area": "area",
        "priority": "priority",
        "version": "version",
    }

    def __init__(self, js_obj):
        self._js_obj = js_obj
        self._id = None

    @property
    def figure_info(self):
        return FigureInfo(
            id=self.id,
            object_id=self.object_id,
            class_id=self.class_id,
            updated_at=self.updated_at,
            created_at=self.created_at,
            entity_id=None,
            project_id=None,
            dataset_id=None,
            frame_index=None,
            geometry_type=self.geometry_type,
            geometry=self.geometry,
            geometry_meta=None,
            tags=self.tags,
            meta=self.meta,
            area=self.area,
            priority=self.priority,
            version=self.version,
        )

    def _get_property(self, name, default=object()):
        js_name = self.attr_name.get(name, name)
        if hasattr(self._js_obj, js_name):
            return getattr(self._js_obj, js_name)
        else:
            if default is object():
                raise KeyError(f"Attribute '{name}' is not found")
            return default

    def __getattr__(self, name):
        return self._get_property(name)

    @property
    def id(self):
        if self._id is None:
            self._id = self._get_property("id")
        return self._id

    @property
    def object_id(self):
        return self._get_property("object_id", None)

    @property
    def class_id(self):
        return self._get_property("class_id", None)

    @property
    def updated_at(self):
        return self._get_property("updated_at", None)

    @property
    def created_at(self):
        return self._get_property("created_at", None)

    @property
    def geometry_type(self):
        return self._get_property("geometry_type", None)

    @property
    def geometry(self):
        if self.geometry_type != "bitmap":
            raise ValueError(f"Unsupported geometry type: {self.geometry_type}")
        _, alpha = get_figure_data(self._js_obj)
        offset = (self._js_obj._geometry._main.offset.x, self._js_obj._geometry._main.offset.y)
        return {"data": alpha, "origin": offset}

    @property
    def geometry_version(self):
        return self._js_obj._geometry._main.version

    @property
    def tags(self):
        return js_to_py(self._get_property("tags", None))

    @property
    def meta(self):
        return js_to_py(self._get_property("meta", None))

    @property
    def area(self):
        return self._get_property("area", None)

    @property
    def priority(self):
        return self._get_property("priority", None)

    @property
    def version(self):
        return self._get_property("version", None)


def get_figure_data(js_figure):
    t = time.perf_counter()
    img_data_obj = js_figure._geometry._main.getPixels()
    logger.debug(f"getPixels time: {(time.perf_counter() - t) * 1000:.4f} ms")

    t = time.perf_counter()
    py_arr_data = img_data_obj.data.to_py()
    logger.debug(f"to_py time: {(time.perf_counter() - t) * 1000:.4f} ms")

    t = time.perf_counter()
    img_data = np.array(py_arr_data, dtype=np.uint8).reshape(
        img_data_obj.height, img_data_obj.width, 4
    )
    logger.debug(f"np.array time: {(time.perf_counter() - t) * 1000:.4f} ms")

    rgb = img_data[:, :, :3]
    alpha = img_data[:, :, 3]
    return rgb, alpha


def put_img_to_figure(js_figure, img_data: np.ndarray):
    from js import ImageData
    from pyodide.ffi import create_proxy

    height, width = img_data.shape[:2]
    img_data = img_data.flatten().astype(np.uint8)
    pixels_proxy = create_proxy(img_data)
    pixels_buf = pixels_proxy.getBuffer("u8clamped")
    new_img_data = ImageData.new(pixels_buf.data, width, height)

    try:
        js_figure._geometry._main.setImageData(new_img_data)
    except Exception as e:
        raise e
    finally:
        pixels_proxy.destroy()
        pixels_buf.release()


def py_to_js(obj):
    from pyodide.ffi import to_js
    from js import Object

    if isinstance(obj, dict):
        js_obj = Object()
        for key, value in obj.items():
            setattr(js_obj, key, py_to_js(value))
        return js_obj
    elif isinstance(obj, list):
        return [py_to_js(item) for item in obj]
    else:
        return to_js(obj)


def js_to_py(obj):
    if obj is None:
        return None
    return obj.to_py()


class _PatchableJson(dict):
    def __init__(self, field: Field, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._field = field
        self._linked_obj = None

    def raise_for_key(self, key: str):
        if key in self:
            raise KeyError(f"Key {key} already exists in {self._field}")

    def __update(self, js_obj):
        self.update(js_obj.to_py())

    def link(self, js_obj):
        self._linked_obj = js_obj
        self.__update(js_obj)

    def send_changes(self):
        if self._linked_obj is None:
            return

        for key, value in self.items():
            setattr(self._linked_obj, key, py_to_js(value))


class StateJson(_PatchableJson, metaclass=Singleton):
    def __init__(self, *args, **kwargs):
        super().__init__(Field.STATE, *args, **kwargs)


class DataJson(_PatchableJson, metaclass=Singleton):
    def __init__(self, *args, **kwargs):
        super().__init__(Field.DATA, *args, **kwargs)


class MainServer(metaclass=Singleton):
    def __init__(self):
        self._server = FastAPI()

    def get_server(self) -> FastAPI:
        return self._server


# SDK code
class WebPyApplication(metaclass=Singleton):
    class Event:
        endpoint = None

        @staticmethod
        def from_json(data):
            type = data["type"]
            payload = data["payload"]
            for name, value in WebPyApplication.Event.__dict__.items():
                if hasattr(value, "endpoint") and value.endpoint == type:
                    return value.from_json(payload)
            raise ValueError(f"Unknown event type: {type}")

        class FigureGeometryChanged:
            endpoint = "figures/figureGeometryUpdated"

            def __init__(self, figure_id):
                self.figure_id = figure_id

            @classmethod
            def from_json(cls, data):
                figure_id = data["figureId"]
                return cls(figure_id)

        class FigureGeometrySaved:
            endpoint = "figures/commitFigureGeometryToServer"

            def __init__(self, figure_id):
                self.figure_id = figure_id

            @classmethod
            def from_json(cls, data):
                figure_id = data["figureId"]
                return cls(figure_id)

    def __init__(self, layout=None):
        if layout is None:
            from sly_sdk.app.widgets import Text

            layout = Text("", widget_id="__epmty_layout__")
        self.layout = layout
        self._run_f = None
        self._widgets_n = 0
        self.is_inited = False
        self.events = None

    def __init_state(self):
        from js import slyApp

        self._slyApp = slyApp
        app = slyApp.app
        app = getattr(app, "$children")[0]  # <- based on template
        self._state = app.state
        self._data = app.data
        self._context = app.context  # ??
        self._store = slyApp.store  # <- Labeling tool store (image, classes, objects, etc)

        StateJson().link(self._state)
        DataJson().link(self._data)

        self.is_inited = True

    # Labeling tool data access
    def get_server_address(self):
        from js import window

        server_address = f"{window.location.protocol}//{window.location.host}/"
        return server_address

    def get_api_token(self):
        return self._context.apiToken

    def get_team_id(self):
        return self._context.teamId

    def get_current_image_id(self):
        views = self.get_ordered_initialized_views()
        if not views:
            return None
        return views[0].data.videoId

    def get_current_image(self):
        image_id = self.get_current_image_id()
        if image_id is None:
            return None
        return self.get_image_data_by_id(image_id)

    def get_image_by_id(self, image_id):
        return getattr(self._store.state.videos.all, str(image_id))

    def get_image_data_by_id(self, image_id):
        cur_img = self.get_image_by_id(image_id)
        img_src = cur_img.sources[0]
        img_cvs = img_src.imageData
        img_ctx = img_cvs.getContext("2d")
        img_data = img_ctx.getImageData(0, 0, img_cvs.width, img_cvs.height).data
        py_arr_data = img_data.to_py()
        img_arr = np.array(py_arr_data, dtype=np.uint8).reshape((img_cvs.height, img_cvs.width, 4))
        return img_arr

    def get_view_by_id(self, view_id):
        return getattr(self._store.state.views.all, str(view_id))

    def set_view_image_data(self, view_id, img_np):
        import js
        from js import ImageData
        from pyodide.ffi import create_proxy, to_js

        height, width = img_np.shape[:2]

        print(f"View id: {view_id}")
        cur_view = self.get_view_by_id(view_id)
        cur_view_override_source = {
            "offset": { "x": 0, "y": 0, "z": 0 },
            "width": width,
            "height": height,
            "type": 1, # 1 canvas, 2 nrrd
            "imageData": None,
            "visible": True,
            "version": 1,
        }

        if hasattr(cur_view.data, "overrideSource") and cur_view.data.overrideSource is not None:
            cur_view_override_source["version"] = cur_view.data.overrideSource.version

            if cur_view_override_source["type"] == cur_view.data.overrideSource.type:
                cur_view_override_source["imageData"] = cur_view.data.overrideSource.imageData
                cur_view_override_source["imageData"].width = width
                cur_view_override_source["imageData"].height = height

        if cur_view_override_source["imageData"] is None:
            cur_view_override_source["imageData"] = js.document.createElement("canvas")
            cur_view_override_source["imageData"].width = width
            cur_view_override_source["imageData"].height = height

        img_ctx = cur_view_override_source["imageData"].getContext("2d")
        new_img_data = img_np.flatten().astype(np.uint8)

        pixels_proxy = create_proxy(new_img_data)
        pixels_buf = pixels_proxy.getBuffer("u8clamped")
        new_img_data = ImageData.new(pixels_buf.data, width, height)

        img_ctx.putImageData(new_img_data, 0, 0)
        cur_view_override_source["version"] += 1

        view_update_obj = {
            "viewId": view_id,
            "data": {
                "overrideSourceEnabled": True,
                "overrideSource": cur_view_override_source,
            },
        }

        self._store.dispatch("views/updateViewData", to_js(view_update_obj, dict_converter=js.Object.fromEntries))

    def get_ordered_initialized_views(self) -> List[FigureObj]:
        from pyodide.webloop import PyodideFuture

        js_views = self._store.getters.as_object_map()["views/orderedInitializedViews"]
        if isinstance(js_views, PyodideFuture):
            js_views = await_async(js_views)

        return js_views

    def update_scene_settings(self, settings):
        import js
        from pyodide.ffi import to_js

        self._store.dispatch("settings/updateSceneSettings", to_js(settings, dict_converter=js.Object.fromEntries))

    def create_views(self, rows, cols, image_ids, force_recreate=False, opts={}):
        settings = {
            "autoSelectViewOnHover": False,
            "customImagesLayout": {
                "rows": rows,
                "cols": cols,
                **opts,
            }
        }

        views = self.get_ordered_initialized_views()

        if force_recreate or len(views) != rows * cols:
            self.update_scene_settings(settings)
            self.create_group_views(image_ids)
            return

        self.update_scene_settings(settings)

    def create_group_views(self, image_ids: List[int]):
        import js
        from pyodide.ffi import to_js

        images = [self.get_image_by_id(image_id) for image_id in image_ids]
        entities = {"entities": images, "checkFiguresSynchronization": False}
        self._store.dispatch("views/createGroupViews", to_js(entities, dict_converter=js.Object.fromEntries))

    def _get_js_figures(self, ids=None):
        js_figures = self._store.getters.as_object_map()["figures/figuresList"]
        if ids is not None:
            js_figures = [f for f in js_figures if f.id in ids]
        return js_figures

    def get_figures(self, ids=None) -> List[FigureObj]:
        js_figures = self._get_js_figures(ids)
        return [FigureObj(f) for f in js_figures]

    def get_figure_by_id(self, figure_id: int):
        figures = self.get_figures(ids=[figure_id])
        if len(figures) == 0:
            return None
        return figures[0]

    def get_selected_figure(self) -> FigureObj:
        from pyodide.webloop import PyodideFuture

        js_figure = self._store.getters.as_object_map()["figures/currentFigure"]
        if isinstance(js_figure, PyodideFuture):
            js_figure = await_async(js_figure)
        if js_figure is None:
            return None
        return FigureObj(js_figure)

    def get_figure_geometry_version(self, figure_id):
        js_figures = self._get_js_figures(ids=[figure_id])
        if len(js_figures) == 0:
            return None
        js_figure = js_figures[0]
        return js_figure.geometry._main.version

    def get_current_view_figures(self) -> List[FigureObj]:
        from pyodide.webloop import PyodideFuture

        js_figures = self._store.getters.as_object_map()["figures/currentViewFigures"]
        if isinstance(js_figures, PyodideFuture):
            js_figures = await_async(js_figures)

        figures: List[FigureInfo] = []
        for js_figure in js_figures:
            if js_figure._geometryType != "bitmap":
                logger.warning(
                    f"Only bitmaps supported at the moment, skipping object #{js_figure.id}"
                )
                continue
            figures.append(FigureObj(js_figure))
        return figures

    def update_figure_geometry(self, figure: FigureObj, geometry):
        import js
        from pyodide.ffi import to_js

        self._store.dispatch("figures/figureGeometryBeforeUpdate", figure.id)
        img = np.stack([geometry] * 4, axis=-1)
        t = time.perf_counter()
        put_img_to_figure(figure._js_obj, img)
        logger.debug(f"put_img_to_figure time: {(time.perf_counter() - t) * 1000:.4f} ms")
        new_version = figure._js_obj.geometry._main.version + 1
        self._store.dispatch(
            "figures/updateGeometryInFigure",
            to_js(
                {
                    "figureId": figure.id,
                    "commit": True,
                    "data": {
                        "version": new_version,
                    },
                },
                dict_converter=js.Object.fromEntries,
            ),
        )
        return figure

    @property
    def state(self):
        if not self.is_inited:
            self.__init_state()
        StateJson().link(self._state)
        return StateJson()

    @property
    def data(self):
        if not self.is_inited:
            self.__init_state()
        DataJson().link(self._data)
        return DataJson()

    def render(
        self, main_script_path: str, src_dir: str, app_dir: str, requirements_path: str = None
    ):
        import json
        import os
        from pathlib import Path
        import supervisely as sly
        from supervisely.app.content import DataJson, StateJson
        from fastapi.staticfiles import StaticFiles
        from fastapi.routing import Mount

        app_dir = Path(app_dir)
        # read requirements
        reqs = Path("sly_sdk/requirements.txt").read_text().splitlines()
        if requirements_path is not None:
            reqs.extend(Path(requirements_path).read_text().splitlines())
        # Temp

        # init events handlers
        events = None
        if self.events is not None:
            events = list(self.events.keys())
        context = {
            "__webpy_script__": "__webpy_script__.py",
            "pyodide_requirements": reqs,
            "events_subscribed": events,
        }

        # render index.html
        app = sly.Application(layout=self.layout)
        index = app.render(context)
        index = index.replace("post('/", "runPythonScript('/")
        os.makedirs(app_dir, exist_ok=True)
        with open(app_dir / "index.html", "w") as f:
            f.write(index)

        # save State and Data
        StateJson()["app_initializing"] = True
        json.dump(StateJson(), open(app_dir / "state.json", "w"))
        json.dump(DataJson(), open(app_dir / "data.json", "w"))

        # generate entrypoint for script
        main_module = ".".join(main_script_path.split("/"))
        if main_module.endswith(".py"):
            main_module = main_module[:-3]
        with open(app_dir / "__webpy_script__.py", "w") as f:
            f.write(
                f"""
try:
    import supervisely
except ImportError:
    import sys

    import sly_sdk as supervisely

    sys.modules["supervisely"] = supervisely

from {main_module} import app

app.run"""
            )

        # Save SDK
        with tarfile.open(app_dir / "sly_sdk.tar", "w") as tar:
            tar.add(
                "sly_sdk",
                arcname="sly_sdk",
                filter=lambda tarinfo: (
                    None
                    if "__pycache__" in tarinfo.name or tarinfo.name.endswith(".pyc")
                    else tarinfo
                ),
            )

        # Copy src
        with tarfile.open(app_dir / "src.tar", "w") as tar:
            tar.add(
                src_dir,
                arcname=src_dir,
                filter=lambda tarinfo: (
                    None
                    if "__pycache__" in tarinfo.name or tarinfo.name.endswith(".pyc")
                    else tarinfo
                ),
            )

        # Save static
        server = app.get_server()
        for route in server.routes:
            if route.path == "/sly":
                route: Mount
                for route in route.routes:
                    if route.path == "/css" and isinstance(route.app, StaticFiles):
                        source_dir = route.app.directory
                        for root, _, files in os.walk(source_dir):
                            rel_path = Path(root).relative_to(source_dir)
                            for file in files:
                                if file.endswith(("css", "js", "html")):
                                    sly.fs.copy_file(
                                        Path(root, file), app_dir / Path("sly/css", rel_path, file)
                                    )

    def event(self, event: Event):
        def wrapper(f):
            if self.events is None:
                self.events = {}
            self.events[event.endpoint] = f
            return f

        return wrapper

    def _get_handler(self, *args, **kwargs):
        if len(args) != 1:
            return None, None
        arg = args[0]
        handlers = kwargs.get("widgets_handlers", {})

        if handlers is not None and isinstance(arg, str) and arg in handlers:
            return handlers[arg], []

        handlers = kwargs.get("event_handlers", {})
        if handlers is not None:
            try:
                if isinstance(arg, str):
                    arg = json.loads(arg)
                event_type = arg["type"]
                event_payload = arg["payload"]
            except Exception as e:
                pass
            else:
                if event_type in handlers:
                    return handlers[event_type], [
                        WebPyApplication.Event.from_json(
                            {"type": event_type, "payload": event_payload}
                        )
                    ]
        return None, None

    def _run_handler(self, f, *args, **kwargs):
        import inspect

        if inspect.iscoroutinefunction(f):
            loop = get_or_create_event_loop()
            return loop.run_until_complete(f(*args, **kwargs))
        return f(*args, **kwargs)

    def run(self, *args, **kwargs):
        t = time.perf_counter()
        try:
            from fastapi.routing import APIRoute

            state = self.state
            if state.get("app_initializing", False) == True:
                state["app_initializing"] = False
                state.send_changes()
            self.data  # to init StateJson and DataJson

            # import js
            # js.console.log(self._store.getters.as_object_map())

            server = MainServer().get_server()
            widget_handlers = {}
            for route in server.router.routes:
                if isinstance(route, APIRoute):
                    widget_handlers[route.path] = route.endpoint

            handler, handler_args = self._get_handler(
                *args, widgets_handlers=widget_handlers, event_handlers=self.events, **kwargs
            )
            if handler is not None:
                logger.debug("Prepare time: %.4f ms", time.perf_counter() - t)
                logger.info(f"handler called: {handler.__name__}")
                t = time.perf_counter()
                result = self._run_handler(handler, *handler_args)
                logger.debug("function_time: %.4f ms", time.perf_counter() - t)
                return result
            if self._run_f is None:
                logger.warning("Unknown command")
            logger.debug("Prepare time: %.4f ms", time.perf_counter() - t)
            t = time.perf_counter()
            if self._run_f is None:
                logger.error("main function is not set")
                return
            result = self._run_f(*args, **kwargs)
            logger.debug("function_time: %.4f ms", time.perf_counter() - t)
            return result
        except Exception as e:
            logger.error(f"Unexpected error in app.run(): {e}", exc_info=True)

    def run_function(self, f):
        self._run_f = f
        return f
