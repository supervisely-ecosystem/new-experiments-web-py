from supervisely.app.widgets import (
    Button,
    Container,
    Editor,
    Empty,
    Field,
    Image,
    OneOf,
    RadioGroup,
    Text,
)

# augmentations
info = """
    To apply augmentations to the training data, you can select one of the options below.<br>
    1. Predefined Augmentations: use a set of augmentations that are already defined by the framework.<br>
    2. Custom Augmentations: define your own augmentations using the ML Pipelines app.<br>
    3. No Augmentations: disable augmentations.
"""
augmentations_info = Text(status="info", widget_id="augmentations_info", text=info, font_size=12)

augmentations_editor = Editor(
    language_mode="yaml",
    widget_id="augmentations_editor",
    height_lines=20,
    restore_default_button=False,
)
custom_augmentations_text = Text(
    """You can define custom augmentations using the <strong>ML Pipelines</strong> app.<br> By default, the app will build a pipeline with the basic augmentations for the selected CV task.<br>"""
)
custom_augmentations_image = Image(url="static/data/ml_pipelines.png", widget_id="custom_aug_image")
custom_augmentations_in_progress = Text(
    """in progress...""",
    status="warning",
    widget_id="custom_augmentations_in_progress",
)
custom_augmentations_in_progress.hide()
custom_augmentations = Container(
    [custom_augmentations_text, custom_augmentations_image, custom_augmentations_in_progress],
    widget_id="custom_augmentations",
)
augmentations_mode = RadioGroup(
    items=[
        RadioGroup.Item("predefined", "Predefined Augmentations", content=augmentations_editor),
        RadioGroup.Item("custom", "Custom Augmentations", content=custom_augmentations),
        RadioGroup.Item("none", "No Augmentations", content=Empty(widget_id="no_augmentations")),
    ],
    widget_id="augmentations_mode",
    direction="vertical",
)
augmentations_oneof = OneOf(augmentations_mode, widget_id="augmentations_oneof")
# augmentations_btn = Button(text="Confirm", widget_id="augmentations_button")
augmentations_section_cont = Container(
    [augmentations_info, augmentations_mode, augmentations_oneof],
    widget_id="augmentations_container",
)
augmentations_section = Field(
    content=augmentations_section_cont,
    widget_id="augmentations_field",
    title="Augmentations",
    description="Specify augmentations for training",
)
