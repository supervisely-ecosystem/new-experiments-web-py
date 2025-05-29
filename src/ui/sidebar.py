import src.sly_functions as f
# from src.ui.augmentations import augmentations_section
from src.ui.classes import classes_list_selector_section
from src.ui.cv_task import cv_task_section
from src.ui.evaluation import evaluate_section
from src.ui.export_weights import export_formats_section
from src.ui.gpu_agent import gpu_selector_section
from src.ui.hyperparameters import hyperparameters_section
from src.ui.model import model_selector_section
from src.ui.projects import training_data_section
from src.ui.train import train_section
from src.ui.train_val_split import train_val_split_section
from supervisely.app.widgets import Button, Container, OneOf, Select, Sidebar


# left nav bar
def get_navbar_btn(text):
    widget_id = "_".join([s for s in text.lower().split() if not f.is_digit(s) and s != "/"])
    # widget_id = widget_id.replace("/", "").replace(" ", "_")
    widget_id = f"{widget_id}_left_navbar_btn"
    return Button(text, "text", "mini", True, False, widget_id=widget_id)


start = get_navbar_btn("START")
cv_task = get_navbar_btn("1. CV TASK")
training_data = get_navbar_btn("2. TRAINING DATA")
classes = get_navbar_btn("3. CLASSES")
train_val_split = get_navbar_btn("4. TRAIN / VAL SPLIT")
model = get_navbar_btn("5. MODEL")
# augmentations = get_navbar_btn("6. AUGMENTATIONS")
hyperparameters = get_navbar_btn("6. HYPERPARAMETERS")
gpu = get_navbar_btn("7. GPU")
export = get_navbar_btn("8. EXPORT")
evaluate = get_navbar_btn("9. EVALUATION")
train = get_navbar_btn("10. TRAIN")
# start = get_navbar_btn("START")

navbar_btns = [
    # start,
    cv_task,
    training_data,
    classes,
    train_val_split,
    model,
    # augmentations,
    hyperparameters,
    gpu,
    export,
    evaluate,
    train,
]


left_nav_bar = Container(widgets=navbar_btns, widget_id="left_nav_bar")


widgets = [
    # start_section,
    cv_task_section,
    training_data_section,
    classes_list_selector_section,
    train_val_split_section,
    # augmentations_section,
    model_selector_section,
    hyperparameters_section,
    gpu_selector_section,
    export_formats_section,
    evaluate_section,
    train_section,
]

right_container = Container(
    widgets=widgets,
    widget_id="right_container",
)

one_of_selector = Select(
    items=[
        Select.Item("cv_task", "CV Task", content=cv_task_section),
        Select.Item("training_data", "Training Data", content=training_data_section),
        Select.Item("classes", "Classes", content=classes_list_selector_section),
        Select.Item("train_val_split", "Train / Val Split", content=train_val_split_section),
        # Select.Item("augmentations", "Augmentations", content=augmentations_section),
        Select.Item("model", "Model", content=model_selector_section),
        Select.Item("hyperparameters", "Hyperparameters", content=hyperparameters_section),
        Select.Item("gpu", "GPU", content=gpu_selector_section),
        Select.Item("export", "Export Formats", content=export_formats_section),
        Select.Item("evaluate", "Evaluate", content=evaluate_section),
        Select.Item("train", "Train", content=train_section),
    ],
    widget_id="oneof_selector",
)
one_of_selector.hide()
one_of = OneOf(one_of_selector, widget_id="oneof")
sidebar = Sidebar(
    left_content=left_nav_bar,
    right_content=one_of,
    width_percent=22,
    show_close=False,
    show_open=False,
    sidebar_left_padding="15px",
    height="75vh",
    standalone=False,
    widget_id="main_sidebar",
)

f.update_nav_bar(cv_task, navbar_btns)

@cv_task.click
def on_cv_task_click():
    f.update_nav_bar(cv_task, navbar_btns)
    one_of_selector.set_value("cv_task")


@training_data.click
def on_training_data_click():
    f.update_nav_bar(training_data, navbar_btns)
    one_of_selector.set_value("training_data")


@classes.click
def on_classes_list_selector_click():
    f.update_nav_bar(classes, navbar_btns)
    one_of_selector.set_value("classes")


@train_val_split.click
def on_train_val_split_click():
    f.update_nav_bar(train_val_split, navbar_btns)
    one_of_selector.set_value("train_val_split")


# @augmentations.click
# def on_augmentations_click():
#     f.update_nav_bar(augmentations, navbar_btns)
#     one_of_selector.set_value("augmentations")


@model.click
def on_model_click():
    f.update_nav_bar(model, navbar_btns)
    one_of_selector.set_value("model")


@hyperparameters.click
def on_hyperparameters_click():
    f.update_nav_bar(hyperparameters, navbar_btns)
    one_of_selector.set_value("hyperparameters")


@gpu.click
def on_gpu_selector_click():
    f.update_nav_bar(gpu, navbar_btns)
    one_of_selector.set_value("gpu")


@export.click
def on_export_click():
    f.update_nav_bar(export, navbar_btns)
    one_of_selector.set_value("export")


@evaluate.click
def on_evaluate_click():
    f.update_nav_bar(evaluate, navbar_btns)
    one_of_selector.set_value("evaluate")


@train.click
def on_train_click():
    f.update_nav_bar(train, navbar_btns)
    one_of_selector.set_value("train")
