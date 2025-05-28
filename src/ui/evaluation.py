import src.sly_globals as g
from supervisely.app.widgets import Checkbox, Container, Empty, Field, Text

# evaluate
info = """
After model training, you can choose to automatically evaluate its performance on the validation dataset.
This helps you understand how well your model generalizes to unseen data and provides important metrics
to assess model quality.<br><br>

The evaluation process includes:<br>
- Computing standard metrics (accuracy, precision, recall, F1-score, IoU)<br>
- Generating visualizations of model predictions<br>
- Creating confusion matrices and performance charts<br>
- Saving detailed reports for future reference (this report can be used to compare different model evaluations)<br>
"""
evaluate_text = Text(status="info", widget_id="evaluate_text", text=info, font_size=12)
evaluate_checkbox = Checkbox(
    content=Field(
        title="Run Model Evaluation",
        description="Evaluate the trained model on the validation dataset to measure accuracy and performance",
        content=Empty(),
        widget_id="eval_checkbox_field",
    ),
    checked=True,
    widget_id="evaluate_checkbox",
)
speedtest_checkbox = Checkbox(
    content=Field(
        title="Run Speed Test",
        description="Measure model inference speed (FPS) on your hardware configuration",
        content=Empty(),
        widget_id="speedtest_checkbox_field",
    ),
    checked=False,
    widget_id="speedtest_checkbox",
)
eval_note = Text(
    status="info",
    text="""
<strong>What to expect:</strong><br>
- Evaluation results will be stored in Team Files (e.g. <i>/model-benchmark/project_name/task_id_app_name/visualizations/Model Evaluation Report.lnk</i>)<br>
- Speedtest results will include average inference time per image and throughput (FPS)<br>
- The entire evaluation process typically takes a few minutes depending on dataset size<br>

For more information about evaluation metrics and how to interpret them, please see our <a href="https://docs.supervisely.com/neural-networks/model-evaluation-benchmark" target="_blank" style="color: #007bff; cursor: pointer; text-decoration: underline;">documentation</a>.
""",
    widget_id="eval_note",
    font_size=12,
)

evaluate_section_cont = Container(
    [evaluate_text, evaluate_checkbox, speedtest_checkbox, eval_note],
    widget_id="evaluate_container",
)
evaluate_section = Field(
    content=evaluate_section_cont,
    title="Model Evaluation",
    widget_id="evaluate_field",
)


@evaluate_checkbox.value_changed
def handle_evaluate_checkbox_change(value):
    g.run_evaluation = value


@speedtest_checkbox.value_changed
def handle_speedtest_checkbox_change(value):
    g.run_speed_test = value
