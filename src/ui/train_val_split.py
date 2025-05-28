import src.sly_globals as g
from supervisely.app.widgets import (
    Button,
    Container,
    Empty,
    Field,
    OneOf,
    RadioGroup,
    RandomSplitsTable,
    Select,
    NotificationBox,
    SelectDatasetTree,
    Text,
    TrainValSplits,
)

# train/val split
info = """
You can select one of the options below to split your data into train and val subsets. <br>
1. Based on collections: use the collections in the project to split the data. <br>
2. Based on datasets: use the datasets in the project to split the data. <br>
3. Random: use a random split of the data. <br>
Split settings will be saved in the project for future use. <br>
"""
# 4. Previous training split settings: use the same split as in the previous training (if available). <br>
train_val_split_info = Text(
    status="info", widget_id="train_val_split_info", text=info, font_size=12
)

collections_split = TrainValSplits(
    random_splits=False, datasets_splits=False, tags_splits=False, collections_splits=True
)
collections_split_content = collections_split._content._items[0].content
# train_col = Select(items=[], multiple=True, widget_id="train_col")
# train_col_text = Text("Train collections", widget_id="train_col_text")
# train_col_cont = Container(
#     [train_col_text, train_col],
#     widget_id="train_col_cont",
#     # direction="horizontal",
#     # fractions=[2, 3],
#     # style="margin: 5px;",
# )
# val_col = Select(items=[], multiple=True, widget_id="val_col")
# val_col_text = Text("Val collections", widget_id="val_col_text")
# val_col_cont = Container(
#     [val_col_text, val_col],
#     widget_id="val_col_cont",
#     # direction="horizontal",
#     # fractions=[2, 3],
#     # style="margin: 5px;",
# )
# collections_cont = Container([train_col_cont, val_col_cont], widget_id="collections_cont")
collections_cont = Container([collections_split_content], widget_id="collections_cont")

# train_ds = Select(items=[], multiple=True, widget_id="train_ds")
notification_box = NotificationBox(
    title="Notice: How to make equal splits",
    description="Choose the same dataset(s) for train/validation to make splits equal. Can be used for debug and for tiny projects",
    box_type="info",
)
train_ds = SelectDatasetTree(
    multiselect=True,
    flat=True,
    select_all_datasets=False,
    always_open=False,
    compact=True,
    team_is_selectable=False,
    workspace_is_selectable=False,
    append_to_body=False,
    widget_id="train_ds",
)

val_ds = SelectDatasetTree(
    multiselect=True,
    flat=True,
    select_all_datasets=False,
    always_open=False,
    compact=True,
    team_is_selectable=False,
    workspace_is_selectable=False,
    append_to_body=False,
    widget_id="val_ds",
)

train_field = Field(
    train_ds,
    title="Train dataset(s)",
    description=f"all images in selected dataset(s) are considered as training set",
)
val_field = Field(
    val_ds,
    title="Validation dataset(s)",
    description=f"all images in selected dataset(s) are considered as validation set",
)
ds_cont = Container(
    widgets=[notification_box, train_field, val_field], direction="vertical", gap=5, widget_id="datasets_cont"
)

random_split = RandomSplitsTable(items_count=100)


mode_text = Text("Split mode", widget_id="train_val_split_mode_text")
train_val_mode_radio = RadioGroup(
    items=[
        RadioGroup.Item("collections", "Based on collections", content=collections_cont),
        RadioGroup.Item("random", "Random", content=random_split),
        RadioGroup.Item("datasets", "Based on datasets", content=ds_cont),
        # RadioGroup.Item("previous", "Previous training split settings", content=Empty()),
    ],
    widget_id="train_val_mode_radio",
    direction="vertical",
)
train_val_mode_cont = Container(
    [mode_text, train_val_mode_radio],
    widget_id="train_val_mode_container",
    # direction="horizontal",
    # fractions=[2, 3],
    # style="margin: 10px 5px;",
)


train_val_split_oneof = OneOf(train_val_mode_radio, widget_id="train_val_split_oneof")
# split_cont

# train_val_split_btn = Button(text="Confirm", widget_id="train_val_split_button")
train_val_split_section_cont = Container(
    [train_val_split_info, train_val_mode_cont, train_val_split_oneof],
    widget_id="train_val_split_container",
)
train_val_split_section = Field(
    content=train_val_split_section_cont,
    widget_id="train_val_split_field",
    title="Train / Val Split",
    description="Define how to split your data into train / val subsets",
)
g.selected_split_method = train_val_mode_radio.get_value()
g.train_datasets = train_ds.get_selected_ids()
g.val_datasets = val_ds.get_selected_ids()


@train_val_mode_radio.value_changed
def on_train_val_mode_radio_value_changed(value):
    g.selected_split_method = value
    # if value == "random":
    #     g.train_split_percent = random_split.get_train_split_percent()
    # elif value == "datasets":
    #     g.train_datasets = train_ds.get_selected_ids()
    #     g.val_datasets = val_ds.get_selected_ids()
    # elif value == "collections":
    #     g.train_collections = collections_split.get_train_collections_ids()
    #     g.val_collections = collections_split.get_val_collections_ids()

# @train_ds.value_changed
# def on_train_ds_value_changed(value):
#     g.train_datasets = value


# @val_ds.value_changed
# def on_val_ds_value_changed(value):
#     g.val_datasets = value


# @train_col.value_changed
# def on_train_col_value_changed(value):
#     g.train_collections = value


# @val_col.value_changed
# def on_val_col_value_changed(value):
#     g.val_collections = value
