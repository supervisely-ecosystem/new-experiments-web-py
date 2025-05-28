import src.sly_globals as g
from supervisely.app.widgets import Checkbox, Container, Editor, Field, Text
from supervisely._utils import abs_url

# hyperparameters
apps_url = abs_url("/ecosystem/augmentation")
info = f"""
In this section, you can define the general settings and advanced configuration for the training process.<br>
You can use the default settings or modify them according to your needs.<br>
For example, you can change the number of epochs, batch size, learning rate, and other parameters.<br><br>

By default, all augmentations are already set up inside the training pipeline. If you want to apply custom augmentations, you can perform this using one of corresponding apps from the <a href="{apps_url}" target="_blank">Ecosystem</a> page.<br>
"""
hyperparameters_info = Text(
    status="info", widget_id="hyperparameters_info", text=info, font_size=12
)

hyperparameters_text = Text(
    "<strong>Hyperparameters</strong>",
    widget_id="hyperparameters_text",
)
hyperparameters_editor = Editor(
    language_mode="yaml",
    widget_id="hyperparameters_editor",
    height_lines=40,
    restore_default_button=False,
)
# training_params_text = Text(
#     "<strong>Training Parameters</strong>",
#     widget_id="training_params_text",
# )
# training_params_editor = Editor(
#     language_mode="yaml",
#     widget_id="training_params_editor",
#     height_lines=20,
# )
save_checkbox = Checkbox(
    "Save hyperparameters to Team Files for future use",
    checked=g.save_hyperparameters,
    widget_id="save_hyperparameters",
)
# hyperparameters_btn = Button(text="Confirm", widget_id="hyperparameters_btn")
# hyperparameters_save_btn = Button(
#     text="Save template to Team Files", widget_id="hyperparameters_save_btn", plain=True
# )
hyperparameters_section_cont = Container(
    [
        hyperparameters_info,
        hyperparameters_text,
        hyperparameters_editor,
        # training_params_text,
        # training_params_editor,
        save_checkbox,
        # Flexbox(
        #     [hyperparameters_btn, hyperparameters_save_btn], widget_id="hyperparameters_btns", gap=5
        # ),
    ],
    widget_id="hyperparameters_container",
)
hyperparameters_section = Field(
    content=hyperparameters_section_cont,
    widget_id="hyperparameters_field",
    title="Hyperparameters",
    description="Define general settings and advanced configuration",
)


@save_checkbox.value_changed
def on_save_checkbox_value_changed(checked: bool):
    g.save_hyperparameters = checked
