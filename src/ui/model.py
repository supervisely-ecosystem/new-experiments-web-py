import os

import src.sly_functions as f
import src.sly_globals as g
import supervisely as sly

# from src.ui.augmentations import augmentations_editor
from src.ui.export_weights import onnx_checkbox, tesorrt_checkbox
from src.ui.hyperparameters import hyperparameters_editor
from src.ui.train import change_experiment_name, experiment_name_input
from supervisely.app.widgets import (
    Container,
    FastTable,
    Field,
    Image,
    NotificationBox,
    RadioCard,
    Select,
    Text,
)
from supervisely.io.json import load_json_file

# model
models = load_json_file("src/data/models.json")
filtered_models = {}
for model_json in models:
    for key in model_json:
        if isinstance(model_json[key], (int, float)):
            model_json[key] = str(model_json[key])

    arch_type = model_json.get("meta", {}).get("arch_type", "other")
    task_type = model_json.get("meta", {}).get("task_type", model_json.get("task_type", "other"))

    if task_type not in filtered_models:
        filtered_models[task_type] = {}
    if arch_type not in filtered_models[task_type]:
        filtered_models[task_type][arch_type] = []
    filtered_models[task_type][arch_type].append(model_json)

sorted_filtered_models = {
    task: {arch: models for arch, models in sorted(archs.items())}
    for task, archs in sorted(filtered_models.items())
}
# model_arch_selector = Select(
#     items=[Select.Item("no models", disabled=True)], widget_id="model_arch_selector"
# )
# columns = [
#     "Architecture",
#     "Framework",
#     "Description",
#     "Best mAP",
#     "Models",
#     "Year",
#     "Real-time",
#     "Export to",
# ]
# columns_options = [
#     {},
#     {},
#     {},
#     {"tooltip": "Best mAP achieved"},
#     {},
#     {"tooltip": "Year of release or last update"},
#     {"tooltip": "Real time inference"},
#     {"tooltip": "Available export formats"},
# ]
# arch_selector_table = FastTable(
#     columns=columns,
#     columns_options=columns_options,
#     show_header=False,
#     widget_id="arch_selector_fast_table",
# )
# arch_selector_text = Text("", status="success", widget_id="arch_selector_text")
# arch_selector_text.hide()

items = [
    RadioCard.Item(
        title="All models",
        content=Image(
            url="https://demo.supervisely.com/img/images-v2-light-dark.121c868.png",
            widget_id="all_models_image",
        ),
        description="Explore all models for selected task type. Sort or filter them by architecture, metric or other parameters in the table below.",
        # img="https://demo.supervisely.com/img/images-v2-light-dark.121c868.png",
        tag="ALL MODELS",
        tag_icon="zmdi-apps",
        disabled=False,
    ),
    RadioCard.Item(
        title="YOLO",
        content=Image(
            url="https://demo.supervisely.com/img/images-v1.ce5de12.png", widget_id="yolo_image"
        ),
        description="Explore YOLO models for selected task type. Sort or filter them by architecture, metric or other parameters in the table below.",
        # description_content=Text("This is content of item 2", status="info"),
        # img="https://demo.supervisely.com/img/images-v1.ce5de12.png",
        tag="YOLO",
        tag_icon="zmdi-apps",
        disabled=False,
    ),
    RadioCard.Item(
        title="DEIM",
        content=Image(
            url="https://demo.supervisely.com/img/images-v1.ce5de12.png", widget_id="deim_image"
        ),
        description="Explore DETR models for selected task type. Sort or filter them by architecture, metric or other parameters in the table below.",
        # img="https://demo.supervisely.com/img/images-v1.ce5de12.png",
        tag="DEIM",
        tag_icon="zmdi-apps",
        disabled=False,
    ),
    RadioCard.Item(
        title="RT-DETRv2",
        content=Image(
            url="https://demo.supervisely.com/img/images-v1.ce5de12.png",
            widget_id="rt_detrv2_image",
        ),
        description="Explore RT-DETRv2 models for selected task type. Sort or filter them by architecture, metric or other parameters in the table below.",
        # img="https://demo.supervisely.com/img/images-v1.ce5de12.png",
        tag="RT-DETRv2",
        tag_icon="zmdi-apps",
        disabled=False,
    ),
    RadioCard.Item(
        title="Recommendations",
        content=Image(
            url="https://demo.supervisely.com/img/images-v1.ce5de12.png",
            widget_id="recommendations_image",
        ),
        description="Description",
        # img="https://demo.supervisely.com/img/images-v1.ce5de12.png",
        tag="RECOMMENDATIONS",
        tag_icon="zmdi-apps",
        disabled=True,
        disabled_text="Comming soon...",
    ),
]
radio_card = RadioCard(items=items, widget_id="radio_card", items_width=140)
radio_card_container = Container(
    [radio_card],
    widget_id="radio_card_container",
    style="margin-top: 20px; margin-bottom: 20px;",
)

models_table_notification = NotificationBox(
    title="List of models in the table below depends on selected task type and architecture",
    description=(
        "If you want to see list of available models for another computer vision task, "
        "please, go back to task type & training classes step and change task type"
    ),
    widget_id="models_table_notification",
)
arch_selector_cont = Field(
    content=Container(
        # arch_selector_text
        [radio_card_container, models_table_notification],
        widget_id="arch_selector_container",
    ),
    widget_id="arch_selector_field",
    title="Model for training",
    # description="Select a architecture from the table below",
)
columns = ["Model name", "Size (pixels)", "mAP", "Params (M)", "FLOPs (B)"]
max_map = 0
for task, archs in sorted_filtered_models.items():
    for arch, models in archs.items():
        for model_dict in models:
            max_map = max(max_map, f.get_map(model_dict, task))
columns_options = [
    {},
    {"postfix": "px", "tooltip": "Input image size"},
    {"maxValue": max_map, "tooltip": "Mean Average Precision (mAP)"},
    {"postfix": "M", "tooltip": "Number of parameters (M)"},
    {"postfix": "B", "tooltip": "Number of FLOPs (B)"},
]
model_selector_table = FastTable(
    columns=columns, columns_options=columns_options, widget_id="model_selector_table"
)
# model_selector_table.hide()
model_selector_text = Text("", status="success", widget_id="model_selector_text")
model_selector_text.hide()
# model_selector_btn = Button(text="Confirm", widget_id="model_selector_button")

model_selector_cont = Container(
    [model_selector_table, model_selector_text],
    widget_id="model_selector_container",
)
model_selector_cont = Field(
    content=model_selector_cont,
    widget_id="model_selector_field",
    title="",
    description="Select a model for training",
)
model_selector_section = Container(
    [
        arch_selector_cont,
        model_selector_cont,
        # model_selector_btn,
    ],
    widget_id="model_selector_section",
)

# frameworks_info = f.update_arch_selector_table(g.cv_task)
# arch_selector_table.read_pandas(frameworks_info)


@radio_card.value_changed
def handle_radio_card_change(idx: int):
    mode = items[idx].tag
    data = f.update_model_selector(mode, g.cv_task, sorted_filtered_models)
    model_selector_table.read_pandas(data)


@model_selector_table.row_click
def on_model_selector_row_click(event: FastTable.ClickedRow):
    row = event.row
    g.selected_model = row[0]
    model_selector_text.text = f"Selected model {row[0]}"
    model_selector_text.show()

    g.selected_arch = f.get_architecture_name(g.selected_model, sorted_filtered_models, g.cv_task)
    available_formats = f.get_export_formats(g.selected_model, sorted_filtered_models, g.cv_task)
    onnx_checkbox.uncheck()
    g.export_to_onnx = False
    tesorrt_checkbox.uncheck()
    g.export_to_tensorrt = False
    onnx_checkbox.hide()
    tesorrt_checkbox.hide()
    if available_formats:
        if "onnx" in available_formats:
            onnx_checkbox.show()
        if "tensorrt" in available_formats:
            tesorrt_checkbox.show()

    # check for saved hyperparameters
    remote_dir = f"/new_experiments_settings/{g.cv_task}/{g.selected_arch}/"
    aug_file = "augmentations.yaml"
    hyper_file = "hyperparameters.yaml"
    # train_file = "training_params.yaml"

    for path, editor in [
        # (aug_file, augmentations_editor),
        (hyper_file, hyperparameters_editor),
        # (train_file, training_params_editor),
    ]:
        remote_path = os.path.join(remote_dir, path)
        default_path = f"src/data/{g.selected_arch}/{path}"
        if g.api.storage.exists(
            team_id=g.team_id,
            remote_path=remote_path,
        ):
            g.api.storage.download(team_id=g.team_id, remote_path=remote_path, local_save_path=path)
            with open(path, "r") as fr:
                content = fr.read()
                editor.set_text(content, language_mode="yaml")
        elif sly.fs.file_exists(default_path):
            with open(default_path, "r") as fr:
                content = fr.read()
                editor.set_text(content, language_mode="yaml")
        else:
            sly.logger.warning(f"File {path} not found in {remote_dir} or {default_path}.")
            editor.set_text("", language_mode="yaml")

    if g.selected_project:
        experiment_name = f"{g.selected_project.name}_{g.selected_model}"
        experiment_name_input.set_value(experiment_name)
        change_experiment_name.text = experiment_name
