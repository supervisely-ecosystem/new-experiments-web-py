import src.sly_functions as f
import src.sly_globals as g
from supervisely.app.widgets import Button, ClassesTable, Container, Field, Text

# classes
info = """
    In this table, you can explore the classes of the project you selected in the previous step.
    You can select the classes for training. According to the selected CV task, the classes will be filtered.
    For example, for the object detection task, only bounding box classes will be available.
    For the instance segmentation task, only polygon and bitmap classes will be available.
"""
classes_info = Text(status="info", widget_id="classes_info", text=info)
classes_list_selector = ClassesTable()
classes_selected_text = Text("", status="success", widget_id="classes_selected_text")
# classes_list_selector_btn = Button(text="Confirm", widget_id="classes_list_selector_button")
classes_list_selector_section_cont = Container(
    [classes_info, classes_list_selector, classes_selected_text],
    widget_id="classes_list_selector_container",
)
classes_list_selector_section = Field(
    content=classes_list_selector_section_cont,
    widget_id="classes_list_selector_field",
    title="Classes",
)


@classes_list_selector.value_changed
def on_classes_list_selector_value_changed(value):
    g.selected_classes = value
    text = f.get_classes_text(value)
    classes_selected_text.text = text
