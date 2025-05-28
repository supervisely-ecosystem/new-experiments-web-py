import pandas as pd

import src.sly_functions as f
import src.sly_globals as g
from src.ui.common import handle_project_selection
from src.ui.train import change_experiment_name, experiment_name_input
from supervisely.app.widgets import (
    Button,
    Checkbox,
    Container,
    FastTable,
    Field,
    Flexbox,
    NotificationBox,
    OneOf,
    RadioGroup,
    SolutionsProject,
    Text,
)

# training data
columns = ["ID", "Project name", "Images count", "Classes"]
columns_options = [{}, {}, {"postfix": "images"}]
# # 5 most recently used projects
data = []
dataframe = pd.DataFrame(data=data, columns=columns)
info = """
    In this section, you can select the training data for the experiment.
    You can select a project from the table of the most recently used projects or all projects.
"""
training_data_info = Text(status="info", widget_id="training_data_info", text=info)
training_data_table_recent_title = Text(
    "Most Recently Used Projects:",
    widget_id="training_data_table_recent_title",
)
training_data_table_recent = FastTable(
    data=data,
    columns=columns,
    columns_options=columns_options,
    widget_id="training_data_table_recent",
    # show_header=False,
)
recent_cont = Container(
    [training_data_table_recent_title, training_data_table_recent],
    widget_id="recent_cont",
)
# # all projects
training_data_selected_card = SolutionsProject(
    # title="Selected project",
    width=150,
    widget_id="training_data_selected_card",
)
training_data_selected_card.add_badge(
    SolutionsProject.Badge("⛔︎", "Select a project", "warning")
)
stats_url = Button(
    "QA & Stats",
    icon="zmdi zmdi-open-in-new",
    button_size="mini",
    plain=True,
    widget_id="stats_url",
    link="",
)
open_project_btn = Button(
    "Open project",
    icon="zmdi zmdi-open-in-new",
    button_size="mini",
    plain=True,
    widget_id="open_project_btn",
    link="",
)
versioning_text = "Each new training session creates a new version in the training project. You can track all changes in the {}'Versions'{} tab of the training project."
get_versioning_text = lambda link: versioning_text.format(
    f'<a href="{link}" target="_blank">', "</a>"
)
versioning_notification = NotificationBox(
    title="Data Versioning",
    description=(
        "Each new training session creates a new version in the training project. You can track all changes in the 'Versions' tab of the training project."
    ),
    widget_id="versioning_notification",
    box_type="success",
)
project_info_cont = Container(
    [
        Flexbox([open_project_btn, stats_url], widget_id="prooject_btns_box", gap=5),
        versioning_notification,
    ],
    widget_id="project_info_cont",
    style="max-width: 260px;",
)
training_data_selected_project = Flexbox(
    [training_data_selected_card, project_info_cont], widget_id="training_data_selected_project"
)


training_data_table_title = Text("All Projects:", widget_id="training_data_table_title")
training_data_table = FastTable(
    data=data,
    columns=columns,
    columns_options=columns_options,
    widget_id="training_data_table",
    page_size=5,
)
all_cont = Container(
    [training_data_table_title, training_data_table],
    widget_id="all_cont",
)
training_data_text = Text("", status="success", widget_id="training_data_text")
training_data_text.hide()
training_data_cache_checkbox = Checkbox(
    "Cache data on the agent to optimize project downloading for future trainingss",
    widget_id="training_data_cache_checkbox",
)
# training_data_confirm_btn = Button(
#     text="Confirm",
#     widget_id="training_data_confirm_button",
# )

# select mode (recent or all)
training_data_mode = RadioGroup(
    items=[
        RadioGroup.Item("recent", "Most Recently Used Projects", recent_cont),
        RadioGroup.Item("all", "All Projects", all_cont),
    ],
    widget_id="training_data_mode",
    direction="vertical",
)
training_data_oneof = OneOf(training_data_mode, widget_id="training_data_oneof")


training_data_section_cont = Container(
    [
        training_data_info,
        training_data_selected_project,
        training_data_cache_checkbox,
        training_data_mode,
        training_data_oneof,
        training_data_text,
    ],
    widget_id="training_data_container",
)
training_data_section = Field(
    content=training_data_section_cont,
    widget_id="training_data_field",
    title="Training Data",
)


def _project_selected(project_id: int):
    g.selected_project_id = project_id
    training_data_text.text = f"Selected project_id: {project_id}"
    training_data_text.show()
    g.selected_project = g.api.project.get_info_by_id(g.selected_project_id)
    stats_url.link = g.selected_project.url.replace("datasets", "stats/datasets")
    open_project_btn.link = g.selected_project.url
    versioning_notification.description = get_versioning_text(
        g.selected_project.url.replace("datasets", "versions")
    )
    training_data_selected_card.set_project(g.selected_project)
    training_data_selected_card.remove_badge_by_key("Select a project")
    training_data_selected_card.remove_badge_by_key("Project selected")
    training_data_selected_card.add_badge(
        SolutionsProject.Badge("✔︎", "Project selected", "success")
    )
    handle_project_selection()
    if g.selected_model:
        experiment_name = f"{g.selected_project.name}_{g.selected_model}"
        experiment_name_input.set_value(experiment_name)
        change_experiment_name.text = experiment_name


@training_data_table.row_click
def row_click(event: FastTable.ClickedRow):
    row = event.row
    project_id = row[0]
    _project_selected(project_id=project_id)


@training_data_table_recent.row_click
def row_click_recent(event: FastTable.ClickedRow):
    row = event.row
    project_id = row[0]
    _project_selected(project_id=project_id)


def set_training_data_table(api):
    all_projects, recent_projects = f.update_training_data(api)
    training_data_table.read_pandas(all_projects)
    training_data_table_recent.read_pandas(recent_projects)


@training_data_cache_checkbox.value_changed
def handle_training_data_cache_checkbox(value):
    g.cache_project = value
