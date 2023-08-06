import os

from cftool.misc import LoggingMixin

INFO_PREFIX = LoggingMixin.info_prefix
ERROR_PREFIX = LoggingMixin.error_prefix
WARNING_PREFIX = LoggingMixin.warning_prefix

LOSS_KEY = "loss"
INPUT_KEY = "input"
LATENT_KEY = "latent"
PREDICTIONS_KEY = "predictions"
LABEL_KEY = "labels"
ORIGINAL_LABEL_KEY = "original_labels"
BATCH_INDICES_KEY = "batch_indices"

PT_PREFIX = "model_"
SCORES_FILE = "scores.json"
CHECKPOINTS_FOLDER = "checkpoints"

META_CONFIG_NAME = "__meta__"
ML_PIPELINE_SAVE_NAME = "ml_pipeline"

DEFAULT_ZOO_TAG = "default"
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "carefree-learn")
DATA_CACHE_DIR = os.path.join(CACHE_DIR, "data")
