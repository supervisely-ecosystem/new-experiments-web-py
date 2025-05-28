import os

from dotenv import load_dotenv

import supervisely as sly

if sly.is_development():
    load_dotenv(os.path.expanduser("~/orig_supervisely.env"))
    load_dotenv("local.env")


team_id = sly.env.team_id()
workspace_id = sly.env.workspace_id()
# # initial setup
# has_augmentations = True
# has_hyperparameters = True
api: sly.Api = None

# STATE:
cv_task = sly.nn.TaskType.OBJECT_DETECTION  # ok
cache_project = False
selected_project = None  # ok
selected_project_id = None  # ok
selected_classes = None  # ok

# Train/Val split settings:
selected_split_method = None  # ok
train_split_percent = None  # ok
train_collections = None  # ok
val_collections = None  # ok
train_datasets = None  # ok
val_datasets = None  # ok

# selected_augmentations = None  # str or "ml_pipelines"
# selected_hyperparameters = None
save_hyperparameters = True
selected_arch = None
selected_model = None
selected_gpu = None
selected_export_formats = None
export_to_onnx = False
export_to_tensorrt = False
run_evaluation = True
run_speed_test = False
experiment_name_changed = False

YOLO_SLUG = "supervisely-ecosystem/yolo/supervisely_integration/train"
RT_DETR_SLUG = "supervisely-ecosystem/rt-detrv2/supervisely_integration/train"
DEIM_SLUG = "supervisely-ecosystem/deim/supervisely_integration/train"
ML_PIPELINES_SLUG = "supervisely-ecosystem/data-nodes"

pipeline_templates = {
    sly.nn.TaskType.INSTANCE_SEGMENTATION: "basic-segmentation-augmentations",
    sly.nn.TaskType.OBJECT_DETECTION: "basic-detection-augmentations",
}

framework2slug = {
    "YOLO": YOLO_SLUG,
    "RT-DETRv2": RT_DETR_SLUG,
    "DEIM": DEIM_SLUG,
}
