import src.sly_functions as f
import src.sly_globals as g
from src.ui.classes import classes_list_selector, classes_selected_text
from src.ui.model import (
    model_selector_cont,
    model_selector_table,
    model_selector_text,
    sorted_filtered_models,
)
from src.ui.train_val_split import collections_split, random_split, train_ds, val_ds, train_val_mode_radio

def handle_project_selection(
    classes: list = None,
    train_datasets: list = None,
    val_datasets: list = None,
):
    classes_list_selector.read_project_from_id(g.selected_project_id)
    if classes is None:
        classes_list_selector.select_all()
    else:
        classes_list_selector.select_classes(classes)
    g.selected_classes = classes_list_selector.get_selected_classes()
    classes_selected_text.text = f.get_classes_text(g.selected_classes)

    train_ds.project_id = g.selected_project_id
    val_ds.project_id = g.selected_project_id
    if train_datasets is None:
        train_datasets = []
    if val_datasets is None:
        val_datasets = []
    train_ds.set_project_id(g.selected_project_id)
    val_ds.set_project_id(g.selected_project_id)
    train_ds.set_dataset_ids(train_datasets)
    val_ds.set_dataset_ids(val_datasets)
    collections_split.set_project_id_for_collections(g.selected_project_id)
    train, val = f.get_train_val_collections_ids(g.api, g.selected_project_id)
    if len(train) > 0 and len(val) > 0:
        g.selected_split_method = "collections"
        train_val_mode_radio.set_value("collections")
        collections_split.set_collections_splits(train, val)
    else:
        train_val_mode_radio.set_value("random")
        g.selected_split_method = "random"

    project = g.api.project.get_info_by_id(g.selected_project_id)
    random_split.set_items_count(project.items_count)


def handle_cv_changed(cv_task):
    g.cv_task = cv_task
    g.selected_arch = None
    g.selected_model = None
    model_selector_text.hide()
    data = f.update_model_selector("ALL MODELS", g.cv_task, sorted_filtered_models)
    model_selector_table.read_pandas(data)
