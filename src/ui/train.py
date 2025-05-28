import os
import threading

import yaml

import src.sly_functions as f
import src.sly_globals as g
import supervisely as sly

# from src.ui.augmentations import augmentations_editor, augmentations_mode
from src.ui.hyperparameters import hyperparameters_editor
from src.ui.train_val_split import collections_split, random_split, train_ds, val_ds
from supervisely._utils import abs_url
from supervisely.app.widgets import (
    Button,
    Container,
    Empty,
    Field,
    Flexbox,
    Input,
    Text,
)
from supervisely.sly_logger import logger

# train
experiments_utl = abs_url("nn/experiments")
info = f"""
    After you press the button below, the training task will be created and started on the selected GPU agent.<br>
    You can open the training session in the workspace tasks page and monitor the training process.<br>
    Once the training is finished, all the results (including the trained model) will be saved in Team Files for future use.<br>
    All experiments are available in the <a href="{experiments_utl}" target="_blank">Experiments</a> page. Trained models are saved in the Team Files and can be used for inference (in serving apps).
"""
train_text = Text(text=info, widget_id="train_text", status="info", font_size=12)
change_experiment_name = Button(
    "Experiment name",
    icon="zmdi zmdi-edit",
    plain=True,
    button_type="text",
    # button_size="mini",
    icon_gap=0,
    widget_id="change_experiment_name_button",
)
experiment_name_input = Input(
    placeholder="Experiment name", widget_id="experiment_name_input", icon="edit"
)
experiment_name_input.hide()
experiment_name_save_btn = Button(
    text="Save",
    widget_id="experiment_name_save_button",
    button_type="text",
    icon="zmdi zmdi-save",
    icon_gap=0,
    button_size="mini",
    style="margin-left: 10px",
)
experiment_name_save_btn.hide()
train_btn = Button(text="Train", widget_id="train_button", button_type="success")
experiment_name_controls_box = Flexbox(
    widgets=[
        experiment_name_input,
        experiment_name_save_btn,
        change_experiment_name,
        Empty(style="width: 70%", widget_id="experiment_name_empty"),
    ],
    widget_id="train_controls_box",
)
train_status_text = Text("", widget_id="train_status_text", status="info")
train_status_text.hide()

experiment_name_field = Field(
    title="Experiment name:",
    # description="You can change the experiment name before starting training",
    content=experiment_name_controls_box,
    widget_id="experiment_name_field",
)

train_section_cont = Container(
    widgets=[train_text, experiment_name_field, train_btn, train_status_text],
    widget_id="train_section_cont",
)
train_section = Field(
    content=train_section_cont,
    widget_id="train_section_field",
    title="Train",
)


# def prepare_augmentations():
#     train_status_text.set("Preparing augmentations...", status="info")
#     aug_mode = augmentations_mode.get_value()
#     if aug_mode == "predefined":
#         augmentations_text = augmentations_editor.get_value()
#     elif aug_mode == "none":
#         augmentations_text = ""
#     elif aug_mode == "custom":
#         augmentations_text = ""
#         # will run ML Pipelines app, generate temp project and after that will replace selected prject
#         module_info = g.api.app.get_ecosystem_module_info(slug=g.ML_PIPELINES_SLUG)
#         params = {
#             "project_id": g.selected_project_id,
#             "slyProjectId": g.selected_project_id,
#             "slyProjectName": g.selected_project.name,
#             "pipelineTemplate": g.pipeline_templates.get(g.cv_task),
#         }

#         session = f.start_app_with_params(
#             api=g.api,
#             agent_id=g.selected_gpu,
#             module_id=module_info.id,
#             params=params,
#         )
#         if session is None:
#             logger.error("ML Pipelines app is not ready for API calls")
#             return augmentations_text
#         g.api.app.send_request(session.task_id, "run_pipeline", {})
#         g.api.app.stop(session.task_id)
#         task_info = g.api.task.get_info_by_id(session.task_id) or {}
#         new_project_id = task_info.get("meta", {}).get("output", {}).get("project", {}).get("id")
#         logger.info(f"New project id: {new_project_id}")
#         # if new_project_id is not None:
#         #     # train_datasets = train_ds.get_selected_ids()
#         #     # val_datasets = val_ds.get_selected_ids()
#         #     from supervisely.nn.active_learning.utils.project import (
#         #         create_dataset_mapping,
#         #     )

#         #     src_tree = g.api.dataset.get_tree(g.selected_project_id)
#         #     dst_tree = g.api.dataset.get_tree(new_project_id)

#         #     src_to_dst_map, _ = create_dataset_mapping(src_tree, dst_tree)
#         #     new_train_datasets = [src_to_dst_map[d] for d in train_datasets if d in src_to_dst_map]
#         #     new_val_datasets = [src_to_dst_map[d] for d in val_datasets if d in src_to_dst_map]

#         #     select_project(new_project_id, g.selected_classes, new_train_datasets, new_val_datasets)
#     else:
#         raise ValueError(f"Not supported augmentations mode: {aug_mode}")
#     return augmentations_text


@train_btn.click
def start_training():
    train_btn.disable()
    if g.selected_model is None:
        sly.logger.error("Model is not selected")
        return
    train_status_text.show()
    # augmentations = prepare_augmentations()
    train_status_text.set("Configuring training parameters...", status="info")
    split_method = g.selected_split_method
    train_val_splits = {"method": split_method}
    experiment_name = experiment_name_input.get_value()
    if split_method == "random":
        train_val_splits["split"] = "train"
        train_val_splits["percent"] = random_split.get_train_split_percent()
    elif split_method == "collections":
        train_val_splits["train_collections"] = collections_split.get_train_collections_ids()
        train_val_splits["val_collections"] = collections_split.get_val_collections_ids()
    elif split_method == "datasets":
        train_val_splits["train_datasets"] = train_ds.get_selected_ids()
        train_val_splits["val_datasets"] = val_ds.get_selected_ids()
    else:
        raise ValueError(f"Not supported split method: {split_method}")

    hyperparameters = hyperparameters_editor.get_value()
    # training_params = training_params_editor.get_value()

    # all_hyperparameters = augmentations + "\n\n" + hyperparameters
    all_hyperparameters = hyperparameters

    app_state = {
        "train_val_split": train_val_splits,
        "classes": g.selected_classes,
        "model": {
            "source": sly.nn.ModelSource.PRETRAINED,
            "model_name": g.selected_model,
        },
        "hyperparameters": all_hyperparameters,
        "options": {
            "model_benchmark": {
                "enable": g.run_evaluation,
                "speed_test": g.run_speed_test,
            },
            "cache_project": g.cache_project,
            "export": {"ONNXRuntime": g.export_to_onnx, "TensorRT": g.export_to_tensorrt},
        },
        "experiment_name": experiment_name,
    }

    train_status_text.set("Starting training app...", status="info")
    slug = g.framework2slug.get(g.selected_arch)
    if slug is None:
        raise ValueError(f"Not supported framework: {g.selected_arch}")

    module_info = g.api.app.get_ecosystem_module_info(slug=slug)
    params = {"state": {"project_id": g.selected_project_id, "slyProjectId": g.selected_project_id}}
    session = f.start_app_with_params(
        api=g.api,
        agent_id=g.selected_gpu,
        module_id=module_info.id,
        params=params,
    )
    if session is None:
        train_status_text.set("Failed to start training app", status="error")
        return
    # g.api.app.send_request(session.task_id, "train_from_api", {"app_state": app_state})

    train_status_text.set("Saving hyperparameters in Team Files...", status="info")
    if g.save_hyperparameters:
        remote_dir = f"/new_experiments_settings/{g.cv_task}/{g.selected_arch}/"
        aug_file = "augmentations.yaml"
        hyper_file = "hyperparameters.yaml"
        # train_file = "training_params.yaml"

        for path, data in [
            # (aug_file, augmentations),
            (hyper_file, hyperparameters),
            # (train_file, training_params),
        ]:
            if yaml.safe_load(data) is None:
                continue
            with open(path, "w") as fr:
                fr.write(data)
            g.api.storage.upload(
                team_id=g.team_id,
                src=path,
                dst=os.path.join(remote_dir, path),
            )

    train_status_text.set("Starting training...", status="info")
    g.api.app.send_request(
        session.task_id, "train_from_api", {"app_state": app_state, "wait": False}
    )
    train_status_text.set("Training started. You can close this window.", status="success")
    # g.api.app.stop(session.task_id)
    return session.task_id


@change_experiment_name.click
def on_change_experiment_name_click():
    experiment_name_input.show()
    experiment_name_input.set_value(change_experiment_name.text)
    experiment_name_save_btn.show()
    change_experiment_name.hide()


@experiment_name_save_btn.click
def on_experiment_name_save_btn_click():
    experiment_name = experiment_name_input.get_value()
    if not experiment_name:
        sly.logger.error("Experiment name is empty")
        return
    g.experiment_name_changed = True
    change_experiment_name.text = experiment_name
    change_experiment_name.show()
    experiment_name_input.hide()
    experiment_name_save_btn.hide()
