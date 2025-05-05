import pandas as pd
from supervisely.app.widgets import (
    Button,
    Card,
    ClassesListSelector,
    Container,
    FastTable,
    RadioGroup,
    Stepper,
    Text,
)

from sly_sdk.annotation.obj_class import ObjClass
from sly_sdk.geometry.bitmap import Bitmap
from sly_sdk.geometry.rectangle import Rectangle
from sly_sdk.webpy.app import WebPyApplication

# start
start_btn = Button("Start", widget_id="start_button")
start_card = Card(title="Start", content=start_btn, widget_id="info_card")


# cv task
cv_task_radio = RadioGroup(
    items=[
        RadioGroup.Item("object_detection", "Object Detection"),
        RadioGroup.Item("instance_segmentation", "Instance Segmentation"),
        RadioGroup.Item("semantic_segmentation", "Semantic Segmentation"),
    ],
    widget_id="cv_task_radio",
)
cv_task_btn = Button("Select", widget_id="cv_task_button")
cv_task_card = Card(
    title="Select CV Task",
    content=Container([cv_task_radio, cv_task_btn], widget_id="cv_task_container"),
    widget_id="success_card",
)
cv_task_card.disable()


# discuss
discuss_text = Text(text="Discuss", status="info", widget_id="discuss_text")
discuss_btn = Button("ok", widget_id="discuss_button")
discuss_card = Card(
    title="Discuss",
    content=Container([discuss_text, discuss_btn], widget_id="discuss_container"),
    widget_id="discuss_card",
)
discuss_card.disable()

# training data
data = [["apples", "21"], ["bananas", "15"]]
columns = ["Project name", "Items count"]
columns_options = [{}, {"maxValue": 21, "postfix": "images", "tooltip": "description text"}]
dataframe = pd.DataFrame(data=data, columns=columns)
training_data_table = FastTable(
    data=data,
    columns=columns,
    columns_options=columns_options,
    widget_id="training_data_table",
)
training_data_reset_btn = Button("Reset", widget_id="training_data_reset_button")
training_data_text = Text("", status="success", widget_id="training_data_text")
training_data_text.hide()
training_data_reset_btn.hide()
training_data_card = Card(
    title="Training Data",
    content=Container(
        [training_data_table, training_data_text, training_data_reset_btn],
        widget_id="training_data_container",
    ),
    widget_id="training_data_card",
)
training_data_card.disable()

# classes list selector
classes = [
    ObjClass(name="class1", geometry_type=Bitmap),
    ObjClass(name="class2", geometry_type=Rectangle),
]
classes_list_selector = ClassesListSelector(
    classes=classes,
    multiple=True,
    widget_id="classes_list_selector",
)
classes_list_selector_btn = Button(
    "Select Classes",
    widget_id="classes_list_selector_button",
)
classes_list_selector_card = Card(
    title="Classes List Selector",
    content=Container(
        [classes_list_selector, classes_list_selector_btn],
        widget_id="classes_list_selector_container",
    ),
    widget_id="classes_list_selector_card",
)
classes_list_selector_card.disable()


stepper = Stepper(
    widgets=[
        start_card,
        cv_task_card,
        discuss_card,
        training_data_card,
        classes_list_selector_card,
    ],
    titles=["Start", "CV Task", "Discuss", "Training Data", "Select Classes"],
    widget_id="stepper_widget",
)

card = Card(
    title="Stepper",
    content=stepper,
    widget_id="stepper_card",
)
layout = Container(widgets=[card], widget_id="layout_container")

app = WebPyApplication(layout=layout)


@start_btn.click
def click_start_button():
    stepper.set_active_step(2)
    cv_task_card.enable()
    start_card.disable()


@cv_task_btn.click
def click_cv_task_button():
    stepper.set_active_step(3)
    discuss_card.enable()
    cv_task_card.disable()


@discuss_btn.click
def click_discuss_button():
    stepper.set_active_step(4)
    training_data_card.enable()
    discuss_card.disable()
    training_data_reset_btn.hide()
    training_data_text.hide()


@training_data_table.row_click
def row_click(event: FastTable.ClickedRow):
    stepper.set_active_step(5)

    training_data_reset_btn.show()
    row = event.row
    row_index = event.row_index
    training_data_text.text = f"Selected row: {row_index}. {row}"
    training_data_text.show()
    training_data_card.disable()
    classes_list_selector_card.enable()


@training_data_reset_btn.click
def click_training_data_reset_button():
    stepper.set_active_step(4)
    training_data_card.enable()
    classes_list_selector_card.disable()
    training_data_reset_btn.hide()
    training_data_text.hide()


@classes_list_selector_btn.click
def click_classes_list_selector_button():
    stepper.set_active_step(1)
    classes_list_selector_card.disable()
    start_card.enable()
