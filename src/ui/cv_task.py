import src.sly_globals as g
import supervisely as sly
from src.ui.common import handle_cv_changed
from supervisely.app.widgets import (
    Container,
    Empty,
    Field,
    Image,
    RadioCard,
    RadioGroup,
    Text,
)

# cv task
obj_det_info = """
    Object detection is a computer vision task that involves identifying and locating objects within an image or video.
    Available geometry type is bounding box (Rectangle). For other geometry types the app will try to convert them to bounding boxes"""
cv_task_radio = RadioGroup(
    items=[
        RadioGroup.Item(sly.nn.TaskType.OBJECT_DETECTION, "Object Detection"),
        RadioGroup.Item(sly.nn.TaskType.INSTANCE_SEGMENTATION, "Instance Segmentation"),
    ],
    widget_id="cv_task_radio",
    direction="vertical",
)
# cv_task_btn = Button(text="Select", widget_id="cv_task_button")
info = """
    In this section, you can select the CV task for your experiment.
    The selected task will determine the model architecture, training data, and other parameters.
"""
cv_task_info = Text(status="info", widget_id="cv_task_info", text=info)

handle_cv_changed(sly.nn.TaskType.OBJECT_DETECTION)


@cv_task_radio.value_changed
def on_cv_task_btn_click(cv_task):
    handle_cv_changed(cv_task)


items = [
    RadioCard.Item(
        title="Object Detection",
        content=Image(
            url="https://demo.supervisely.com/img/images-v2-light-dark.121c868.png",
            widget_id="object_detection_image",
        ),
        description="Object detection is a computer vision task that involves identifying and locating objects within an image or video. Available geometry type is bounding box (Rectangle). For other geometry types the app will try to convert them to bounding boxes",
    ),
    RadioCard.Item(
        title="Instance Segmentation",
        content=Image(
            url="https://demo.supervisely.com/img/images-v2-light-dark.121c868.png",
            widget_id="instance_segmentation_image",
        ),
        description="Instance segmentation takes object detection a step further by not only identifying and locating objects but also delineating their precise boundaries at the pixel level. This means that each instance of an object is segmented from the background and from other instances of the same object class.",
    ),
    RadioCard.Item(
        title="Semantic Segmentation",
        content=Image(
            url="https://demo.supervisely.com/img/images-v2-light-dark.121c868.png",
            widget_id="semantic_segmentation_image",
        ),
        description="Semantic segmentation is a computer vision task that involves classifying each pixel in an image into a predefined category or class. Unlike instance segmentation, which distinguishes between different instances of the same object class, semantic segmentation treats all instances of a class as belonging to the same category.",
        tag="Comming soon...",
        tag_icon="zmdi-lock",
        disabled=True,
    ),
]
cv_radio_card = RadioCard(items=items, widget_id="cv_radio_card", items_width=140)
cv_radio_card_container = Container(
    [cv_radio_card],
    widget_id="cv_radio_card_container",
    style="margin: 20px 0",
)


@cv_radio_card.value_changed
def on_cv_task_section_cont_value_changed(selected_idx):
    task_type = [
        sly.nn.TaskType.OBJECT_DETECTION,
        sly.nn.TaskType.INSTANCE_SEGMENTATION,
        sly.nn.TaskType.SEMANTIC_SEGMENTATION,
    ][selected_idx]
    handle_cv_changed(task_type)


cv_task_section_cont = Container(
    [cv_task_info, cv_task_radio, Empty(style="height: 100px"), cv_radio_card],
    widget_id="cv_task_container",
)
cv_task_section = Field(content=cv_task_section_cont, widget_id="cv_task_section", title="CV Task")
