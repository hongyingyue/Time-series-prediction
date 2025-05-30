"""tfts package for time series prediction with TensorFlow"""

from tfts.datasets.get_data import get_data
from tfts.models.auto_config import AutoConfig
from tfts.models.auto_model import (
    AutoModel,
    AutoModelForAnomaly,
    AutoModelForClassification,
    AutoModelForPrediction,
    AutoModelForSegmentation,
    AutoModelForUncertainty,
)
from tfts.trainer import KerasTrainer, Trainer
from tfts.training_args import TrainingArguments

__all__ = [
    "AutoModel",
    "AutoModelForPrediction",
    "AutoModelForClassification",
    "AutoModelForSegmentation",
    "AutoModelForAnomaly",
    "AutoModelForUncertainty",
    "AutoConfig",
    "Trainer",
    "KerasTrainer",
    "TrainingArguments",
    "get_data",
]

__version__ = "0.0.0"
