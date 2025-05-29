import time
from typing import List, Tuple, Union

import pandas as pd

from supervisely.api.api import Api
from supervisely.io.env import server_address as env_server_address
from supervisely.io.env import workspace_id
from supervisely.io.json import load_json_file
from supervisely.sly_logger import logger


def get_train_val_collections_ids(
    api: Api,
    project_id: int,
    use_prefix: bool = False,
) -> Tuple[List[int], List[int]]:
    all_collections = api.entities_collection.get_list(project_id)
    train_collections = []
    val_collections = []
    for collection in all_collections:
        if use_prefix:
            if collection.name.startswith("train"):
                train_collections.append(collection.id)
            elif collection.name.startswith("val"):
                val_collections.append(collection.id)
        else:
            if collection.name.lower() == "train":
                train_collections.append(collection.id)
            elif collection.name.lower() == "val":
                val_collections.append(collection.id)
    return train_collections, val_collections


def is_digit(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def update_nav_bar(clicked_btn, all_btns):
    for btn in all_btns:
        btn.plain = True
        btn.button_type = "text"
    clicked_btn.plain = False
    clicked_btn.button_type = "info"


def get_map(model_dict, task_type):
    if model_dict.get("mAP") is not None:
        return float(model_dict["mAP"])
    else:
        if task_type == "object detection":
            return float(model_dict.get("mAP (box)"))
        else:
            return float(model_dict.get("mAP (mask)"))


def update_model_selector(selected_arch: Union[str, List], task_type: str, all_models: dict):
    # if selected_arch in all_models[task_type]:
    table_data = []
    if selected_arch == "ALL MODELS":
        selected_arch = list(all_models[task_type].keys())
    if isinstance(selected_arch, str):
        selected_arch = [selected_arch]
    for arch in selected_arch:
        if arch in all_models[task_type]:
            for model in all_models[task_type][arch]:
                _map = get_map(model, task_type)
                row = [
                    model["model_name"],
                    model.get("Size (pixels)", "-"),
                    _map,
                    model.get("params (M)", "-"),
                    model.get("FLOPs (B)", "-"),
                ]
                table_data.append(row)
    columns = ["Model name", "Size (pixels)", "mAP", "Params (M)", "FLOPs (B)"]
    data = pd.DataFrame(data=table_data, columns=columns)
    return data


def _init_api(app=None):
    from supervisely._utils import running_in_webpy_app
    from supervisely.api.api import Api

    if running_in_webpy_app():
        # If running in a webpy app, use the app's API
        if app is None:
            raise ValueError("app parameter must be provided when running in a webpy app")
        try:
            server_address = app.get_server_address()
        except Exception as e:
            logger.warning("Failed to get server address, using environment variable instead")
            server_address = env_server_address(raise_not_found=False)
        api_token = app.get_api_token()
        api = Api(server_address, api_token, ignore_task_id=True)
    else:
        api = Api.from_env()
    return api


def get_classes_text(selected_classes: list):
    text = (
        f"Selected class{'' if len(selected_classes) == 1 else 'es'}: {selected_classes}"
        if len(selected_classes) > 0
        else ""
    )
    return text


def update_training_data(api: Api):
    projects = api.project.get_list(
        workspace_id=workspace_id(),
        filters=[{"field": "type", "operator": "=", "value": "images"}],
        fields=["imagesCount"],
    )
    # sort by updated_at
    data = []
    for p in projects:
        data.append([p.id, p.name, p.images_count, "-"])

    columns = ["ID", "Project name", "Images count", "Classes"]
    all_projects = pd.DataFrame(data=data, columns=columns)
    # all_table.read_pandas(all_projects)

    sorted_projects = sorted(
        projects,
        key=lambda p: p.updated_at,
        reverse=True,
    )
    recent_projects = sorted_projects[:5]
    data = []
    for p in recent_projects:
        data.append([p.id, p.name, p.images_count, "-"])
    recent_projects = pd.DataFrame(data=data, columns=columns)
    # recent_table.read_pandas(recent_projects)
    return all_projects, recent_projects


def get_architecture_name(model_name: str, all_models: dict, task_type: str):
    for arch, models in all_models[task_type].items():
        for model in models:
            if model["model_name"] == model_name:
                return arch
    return None


def get_export_formats(model_name: str, all_models: dict, task_type: str):
    json_path = "src/data/frameworks.json"
    frameworks_info = load_json_file(json_path)
    arch = get_architecture_name(model_name, all_models, task_type)
    export_formats = ["PyTorch"]
    for info in frameworks_info:
        if task_type not in info["tasks"]:
            continue
        if info["name"] == arch:
            if info.get("onnx"):
                export_formats.append("onnx")
            if info.get("tensorrt"):
                export_formats.append("tensorrt")
            break
    return export_formats


def update_arch_selector_table(task_type: str):
    json_path = "src/data/frameworks.json"
    frameworks_info = load_json_file(json_path)

    table_data = []
    for info in frameworks_info:
        if task_type not in info["tasks"]:
            continue
        export_formats = ["PyTorch"]
        if info.get("onnx"):
            export_formats.append("ONNX")
        if info.get("tensorrt"):
            export_formats.append("TensorRT")

        row = [
            info["name"],
            "YOLO",
            "some description",
            info["tasks"][task_type]["metric"],
            info["tasks"][task_type]["models"],
            info["released"],
            "+" if info["real_time"] else "-",
            ", ".join(export_formats),
        ]
        table_data.append(row)
    columns = [
        "Architecture",
        "Framework",
        "Description",
        "Best mAP",
        "Models",
        "Year",
        "Real-time",
        "Export to",
    ]
    data = pd.DataFrame(data=table_data, columns=columns)
    return data


def start_app_with_params(
    api: Api,
    agent_id: int,
    module_id: int,
    params: dict,
):
    session = api.app.start(
        agent_id=agent_id,
        module_id=module_id,
        workspace_id=workspace_id(),
        params=params,
        app_version="test-solutions-branch",
        is_branch=True,
    )
    try:
        api.app.wait(session.task_id, target_status=api.task.Status.STARTED)
    except Exception as e:
        logger.error("Failed to start app", exc_info=e)
        return
    ready = api.app.wait_until_ready_for_api_calls(session.task_id)
    return session if ready else None
