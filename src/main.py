import pandas as pd

from supervisely.annotation.obj_class import ObjClass
from supervisely.webpy.app import WebPyApplication
from supervisely.app.widgets import (
    Button,
    Card,
    # ClassesListSelector,
    Container,
    # Editor,
    # FastTable,
    # OneOf,
    # RadioGroup,
    # Select,
    # SelectCudaDevice,
    # Sidebar,
    # Text,
)
from supervisely.io.json import load_json_file

# initial setup
has_augmentations = True
has_hyperparameters = True
projects = None


# # left nav bar
# def get_navbar_btn(text):
#     widget_id = f"{text.lower()}_left_navbar_btn"
#     return Button(text, "text", "mini", True, False, widget_id=widget_id)


# start = get_navbar_btn("START")
# cv_task = get_navbar_btn("CV TASK")
# training_data = get_navbar_btn("TRAINING DATA")
# classes = get_navbar_btn("CLASSES")
# train_val_split = get_navbar_btn("TRAIN / VAL SPLIT")
# augmentations = get_navbar_btn("AUGMENTATIONS")
# model = get_navbar_btn("MODEL")
# hyperparameters = get_navbar_btn("HYPERPARAMETERS")
# gpu = get_navbar_btn("GPU")
# train = get_navbar_btn("TRAIN")
# navbar_btns = [
#     # start,
#     cv_task,
#     training_data,
#     classes,
#     train_val_split,
#     augmentations,
#     model,
#     hyperparameters,
#     gpu,
#     train,
# ]


# left_nav_bar = Container(
#     widgets=navbar_btns,
#     widget_id="left_nav_bar",
# )

# # start
# start_btn = Button(button_size="small", text="Start", widget_id="start_button")
# start_section_cont = Container(widgets=[start_btn], widget_id="start_section_cont")
# start_section = Card(
#     content=start_section_cont,
#     collapsable=True,
#     title="Start",
#     description="Click to create a new experiment",
#     widget_id="start_section",
# )

# # cv task
# cv_task_radio = RadioGroup(
#     items=[
#         RadioGroup.Item("object detection", "Object Detection"),
#         RadioGroup.Item("instance segmentation", "Instance Segmentation"),
#     ],
#     widget_id="cv_task_radio",
# )
# cv_task_btn = Button(text="Select", widget_id="cv_task_button")
# cv_task_section_cont = Container([cv_task_radio, cv_task_btn], widget_id="cv_task_container")
# cv_task_section = Card(
#     content=cv_task_section_cont,
#     collapsable=True,
#     title="CV Task",
#     description="Select a CV task",
#     widget_id="cv_task_section",
# )

# # training data
# data = []

# columns = ["ID", "Updated At", "Project name", "Items count"]
# columns_options = [
#     {},
#     {"tooltip": "Last update"},
#     {},
#     {"postfix": "images", "tooltip": "Total number of images in the project"},
# ]
# dataframe = pd.DataFrame(data=data, columns=columns)
# training_data_table = FastTable(
#     data=data,
#     columns=columns,
#     columns_options=columns_options,
#     widget_id="training_data_table",
# )
# training_data_text = Text("", status="success", widget_id="training_data_text")
# training_data_text.hide()
# training_data_section_cont = Container(
#     [training_data_table, training_data_text],
#     widget_id="training_data_container",
# )
# training_data_section = Card(
#     content=training_data_section_cont,
#     collapsable=True,
#     title="Training data",
#     description="Select a project with training data",
#     widget_id="training_data_section",
# )

# # classes
# classes_list_selector = ClassesListSelector(
#     # classes=obj_classes,
#     multiple=True,
#     widget_id="classes_list_selector",
# )
# classes_list_selector_btn = Button(text="Select Classes", widget_id="classes_list_selector_button")
# classes_list_selector_section_cont = Container(
#     [classes_list_selector, classes_list_selector_btn],
#     widget_id="classes_list_selector_container",
# )
# classes_list_selector_section = Card(
#     content=classes_list_selector_section_cont,
#     widget_id="classes_list_selector_card",
#     collapsable=True,
#     title="Classes",
#     description="Select classes for training",
# )

# # train/val split
# train_val_split_radio = RadioGroup(
#     items=[
#         RadioGroup.Item("random", "Random"),
#         RadioGroup.Item("collections", "Based on collections"),
#         RadioGroup.Item("datasets", "Based on datasets"),
#     ],
#     widget_id="train_val_split_radio",
# )
# train_val_split_btn = Button(text="Select", widget_id="train_val_split_button")
# train_val_split_section_cont = Container(
#     [train_val_split_radio, train_val_split_btn],
#     widget_id="train_val_split_container",
# )
# train_val_split_section = Card(
#     content=train_val_split_section_cont,
#     collapsable=True,
#     title="Train / Val split",
#     description="Select a train/val split method",
#     widget_id="train_val_split_section",
# )

# # augmentations
# augmentations_editor = Editor(language_mode="yaml", widget_id="augmentations_editor")
# augmentations_btn = Button(text="Select", widget_id="augmentations_button")
# augmentations_section_cont = Container(
#     [augmentations_editor, augmentations_btn],
#     widget_id="augmentations_container",
# )
# augmentations_section = Card(
#     content=augmentations_section_cont,
#     collapsable=True,
#     title="Augmentations",
#     description="Select augmentations for training",
#     widget_id="augmentations_section",
# )

# # model
# models = load_json_file("src/models.json")
# filtered_models = {}
# for model_json in models:
#     for key in model_json:
#         if isinstance(model_json[key], (int, float)):
#             model_json[key] = str(model_json[key])

#     arch_type = model_json.get("meta", {}).get("arch_type", "other")
#     task_type = model_json.get("meta", {}).get("task_type", model_json.get("task_type", "other"))

#     if task_type not in filtered_models:
#         filtered_models[task_type] = {}
#     if arch_type not in filtered_models[task_type]:
#         filtered_models[task_type][arch_type] = []
#     filtered_models[task_type][arch_type].append(model_json)

# sorted_filtered_models = {
#     task: {arch: models for arch, models in sorted(archs.items())}
#     for task, archs in sorted(filtered_models.items())
# }
# model_arch_selector = Select(
#     items=[Select.Item("no models", disabled=True)], widget_id="model_arch_selector"
# )

# columns = ["Model name", "Size (pixels)", "mAP", "Params (M)", "FLOPs (B)"]
# columns_options = [
#     {},
#     {"postfix": "px", "tooltip": "Input image size"},
#     {"maxValue": 1, "tooltip": "Mean Average Precision (mAP)"},
#     {"postfix": "M", "tooltip": "Number of parameters (M)"},
#     {"postfix": "B", "tooltip": "Number of FLOPs (B)"},
# ]
# model_selector_table = FastTable(
#     columns=columns, columns_options=columns_options, widget_id="model_selector_fast_table"
# )
# model_selector_text = Text("", status="success", widget_id="model_selector_text")
# model_selector_text.hide()

# model_selector_section_cont = Container(
#     [model_arch_selector, model_selector_table, model_selector_text],
#     widget_id="model_selector_container",
# )
# model_selector_section = Card(
#     content=model_selector_section_cont,
#     widget_id="model_selector_card",
#     collapsable=True,
#     title="Model",
#     description="Select a model for training",
# )

# # hyperparameters
# hyperparameters_editor = Editor(language_mode="yaml", widget_id="hyperparameters_editor")
# hyperparameters_btn = Button(text="Select", widget_id="hyperparameters_button")
# hyperparameters_section_cont = Container(
#     [hyperparameters_editor] * 10 + [hyperparameters_btn],
#     widget_id="hyperparameters_container",
# )
# hyperparameters_section = Card(
#     content=hyperparameters_section_cont,
#     collapsable=True,
#     title="Hyperparameters",
#     description="Select hyperparameters for training",
#     widget_id="hyperparameters_section",
# )

# # gpu
# gpu_selector = SelectCudaDevice(include_cpu_option=True, widget_id="gpu_selector")
# gpu_selector_btn = Button(text="Select", widget_id="gpu_selector_button")
# gpu_selector_section_cont = Container(
#     [gpu_selector, gpu_selector_btn],
#     widget_id="gpu_selector_container",
# )
# gpu_selector_section = Card(
#     content=gpu_selector_section_cont,
#     collapsable=True,
#     title="GPU",
#     description="Select a GPU for training",
#     widget_id="gpu_selector_section",
# )

# # train
# train_btn = Button(text="Train", widget_id="train_button", button_type="success")
# train_section_cont = Container(
#     widgets=[train_btn],
#     widget_id="train_section_cont",
# )
# train_section = Card(
#     content=train_section_cont,
#     collapsable=True,
#     title="Train",
#     description="Start training",
#     widget_id="train_section",
# )
# # train_section.collapse()
# # train_section.hide()

# widgets = [
#     # start_section,
#     cv_task_section,
#     training_data_section,
#     classes_list_selector_section,
#     train_val_split_section,
#     augmentations_section,
#     model_selector_section,
#     hyperparameters_section,
#     gpu_selector_section,
#     train_section,
# ]

# right_container = Container(
#     widgets=widgets,
#     widget_id="right_container",
# )

# one_of_selector = Select(
#     items=[
#         Select.Item("cv_task", "CV Task", content=cv_task_section),
#         Select.Item("training_data", "Training Data", content=training_data_section),
#         Select.Item("classes", "Classes", content=classes_list_selector_section),
#         Select.Item("train_val_split", "Train / Val Split", content=train_val_split_section),
#         Select.Item("augmentations", "Augmentations", content=augmentations_section),
#         Select.Item("model", "Model", content=model_selector_section),
#         Select.Item("hyperparameters", "Hyperparameters", content=hyperparameters_section),
#         Select.Item("gpu", "GPU", content=gpu_selector_section),
#         Select.Item("train", "Train", content=train_section),
#     ],
#     widget_id="oneof_selector",
# )
# one_of_selector.hide()
# one_of = OneOf(one_of_selector, widget_id="oneof")
# sidebar = Sidebar(
#     left_content=left_nav_bar,
#     right_content=one_of,
#     width_percent=18,
#     show_close=False,
#     show_open=False,
#     sidebar_left_padding="15px",
#     height="65vh",
#     standalone=False,
#     widget_id="main_sidebar",
# )
# layout = Container(widgets=[sidebar], widget_id="main_layout")

btn = Button("Click me")
layout = Container(widgets=[btn])
app = WebPyApplication(layout=layout)

# def update_nav_bar(clicked_btn):
#     for btn in navbar_btns:
#         btn.plain = True
#         btn.button_type = "text"
#     clicked_btn.plain = False
#     clicked_btn.button_type = "info"


# app = WebPyApplication(layout=layout)


# def _init_api():
#     from supervisely.api.api import Api

#     server_address = app.get_server_address()
#     api_token = app.get_api_token()
#     api = Api(server_address, api_token, ignore_task_id=True)
#     return api


# @cv_task.click
# def on_cv_task_click():
#     update_nav_bar(cv_task)
#     one_of_selector.set_value("cv_task")


# @cv_task_btn.click
# def on_cv_task_btn_click():
#     cv_task = cv_task_radio.get_value()
#     if cv_task in ["object detection", "instance segmentation"]:
#         arch_types = list(sorted_filtered_models[cv_task].keys())
#         arch_items = [Select.Item(a, a) for a in arch_types]
#         model_arch_selector.set(items=arch_items)
#         model_arch_selector.set_value(arch_items[0].value)
#         update_model_selector(arch_items[0].value)
#     else:
#         print("Unknown cv_task:", cv_task)
#         pass


# @training_data.click
# def on_training_data_click():
#     update_nav_bar(training_data)
#     update_training_data()
#     one_of_selector.set_value("training_data")


# @training_data_table.row_click
# def row_click(event: FastTable.ClickedRow):
#     row = event.row
#     row_index = event.row_index
#     training_data_text.text = f"Selected row: {row_index}. {row}"
#     training_data_text.show()
#     project_id = row[0]
#     api = _init_api()
#     project_meta_json = api.project.get_meta(project_id)
#     obj_classes = []
#     for obj_class_json in project_meta_json["objects"]:
#         obj_class = ObjClass.from_json(obj_class_json)
#         obj_classes.append(obj_class)
#     classes_list_selector.set(obj_classes)


# @classes.click
# def on_classes_list_selector_click():
#     update_nav_bar(classes)
#     one_of_selector.set_value("classes")


# @train_val_split.click
# def on_train_val_split_click():
#     update_nav_bar(train_val_split)
#     one_of_selector.set_value("train_val_split")


# @augmentations.click
# def on_augmentations_click():
#     update_nav_bar(augmentations)
#     one_of_selector.set_value("augmentations")


# @model.click
# def on_model_click():
#     update_nav_bar(model)
#     one_of_selector.set_value("model")


# @model_selector_table.row_click
# def on_model_selector_row_click(event: FastTable.ClickedRow):
#     row = event.row
#     row_index = event.row_index

#     model_selector_text.text = f"Selected row: {row_index}. {row}"
#     model_selector_text.show()


# @hyperparameters.click
# def on_hyperparameters_click():
#     update_nav_bar(hyperparameters)
#     one_of_selector.set_value("hyperparameters")


# @gpu.click
# def on_gpu_selector_click():
#     update_nav_bar(gpu)
#     one_of_selector.set_value("gpu")


# @train.click
# def on_train_click():
#     update_nav_bar(train)
#     one_of_selector.set_value("train")


# @model_arch_selector.value_changed
# def on_model_arch_changed(value):
#     update_model_selector(value)


# def update_model_selector(value):
#     task_type = cv_task_radio.get_value()
#     if value in sorted_filtered_models[task_type]:
#         table_data = []
#         for model in sorted_filtered_models[task_type][value]:
#             _map = model.get("mAP")
#             if _map is None:
#                 if task_type == "object detection":
#                     _map = model.get("mAP (box)")
#                 else:
#                     _map = model.get("mAP (mask)")

#             table_data.append(
#                 [
#                     model["model_name"],
#                     model["Size (pixels)"],
#                     _map,
#                     model["params (M)"],
#                     model["FLOPs (B)"],
#                 ]
#             )
#         data = pd.DataFrame(
#             data=table_data,
#             columns=["Model name", "Size (pixels)", "mAP", "Params (M)", "FLOPs (B)"],
#         )
#         model_selector_table.read_pandas(data)


# def update_training_data():
#     api = _init_api()

#     projects = api.project.get_list(
#         workspace_id=7, filters=[{"field": "type", "operator": "=", "value": "images"}]
#     )
#     data = []
#     for p in projects:
#         data.append([p.id, p.updated_at, p.name, p.images_count])

#     columns = ["ID", "Updated At", "Project name", "Items count"]
#     dataframe = pd.DataFrame(data=data, columns=columns)
#     training_data_table.read_pandas(dataframe)
