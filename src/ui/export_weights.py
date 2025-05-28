import src.sly_globals as g
from supervisely.app.widgets import Checkbox, Container, Empty, Field, Text

# export
info = """
Your trained model weights can be exported in different formats to support various deployment scenarios and frameworks. 
By default, the model will be saved in PyTorch format (`.pth` or `.pt` files), but you can select additional formats from the options below.

Currently Selected Model Framework Supports:<br>
"""
export_info = Text(status="info", widget_id="export_info", text=info, font_size=12)

pytorch_checkbox = Checkbox(
    content=Field(
        title="PyTorch",
        description="Default format to save checkpoints after training (.pth or .pt)",
        content=Empty(),
        widget_id="pytorch_checkbox_field",
    ),
    checked=True,
    widget_id="pytorch_checkbox",
)
pytorch_checkbox.disable()
onnx_checkbox = Checkbox(
    content=Field(
        title="ONNX",
        description="Export the model in ONNX format (.onnx)",
        content=Empty(),
        widget_id="onnx_checkbox_field",
    ),
    checked=False,
    widget_id="onnx_checkbox",
)
onnx_checkbox.hide()
tesorrt_checkbox = Checkbox(
    content=Field(
        title="TensorRT",
        description="Export the model in TensorRT format (.engine)",
        content=Empty(),
        widget_id="tensorrt_checkbox_field",
    ),
    checked=False,
    widget_id="tensorrt_checkbox",
)
tesorrt_checkbox.hide()

export_note = Text(
    status="warning",
    text="""
After training, the model will be saved in the selected format(s) in the experiment directory.<br>
<strong>Note:</strong> This conversion process may take several additional minutes.<br><br>

For information on how to use these different model formats in your own code, please see our 
<a style="color: #3B96FF; cursor: pointer; text-decoration: underline;" href="https://docs.supervisely.com/neural-networks/overview-1/using-standalone-pytorch-models#quick-start-rt-detrv2-example" target="_blank">documentation</a>.
""",
    widget_id="export_format_note",
    font_size=12,
)
export_formats_cont = Container(
    [export_info, export_note, pytorch_checkbox, onnx_checkbox, tesorrt_checkbox],
    widget_id="export_formats_container",
)
export_formats_section = Field(
    content=export_formats_cont,
    widget_id="export_formats_field",
    title="Export Model",
)


@onnx_checkbox.value_changed
def on_onnx_checkbox_value_changed(checked):
    g.export_to_onnx = checked


@tesorrt_checkbox.value_changed
def on_tensorrt_checkbox_value_changed(checked):
    g.export_to_tensorrt = checked
