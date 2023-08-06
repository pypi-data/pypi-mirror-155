import typing as t
from pathlib import Path

import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

from bookRecommender import __version__ as _version
from bookRecommender.config.core import DATASET_DIR, TRAINED_MODEL_DIR, config


def load_dataset(*, file_name_book, file_name_user, file_name_rating: str) -> pd.DataFrame:
    book = pd.read_csv(
        Path(f"{DATASET_DIR}/{file_name_book}"), sep=";", encoding="latin-1", on_bad_lines="skip", low_memory=False
    )
    book.columns = [
        "ISBN",
        "bookTitle",
        "bookAuthor",
        "yearOfPublication",
        "publisher",
        "imageUrlS",
        "imageUrlM",
        "imageUrlL",
    ]
    user = pd.read_csv(
        Path(f"{DATASET_DIR}/{file_name_user}"), sep=";", encoding="latin-1", on_bad_lines="skip", low_memory=False
    )
    user.columns = ["userID", "Location", "Age"]
    rating = pd.read_csv(
        Path(f"{DATASET_DIR}/{file_name_rating}"), sep=";", encoding="latin-1", on_bad_lines="skip", low_memory=False
    )
    rating.columns = ["userID", "ISBN", "bookRating"]
    combine_book_rating = pd.merge(rating, book, on="ISBN")
    dataset = combine_book_rating.merge(user, left_on="userID", right_on="userID", how="left")
    return dataset


def save_pipeline(*, pipeline_to_persist: Pipeline) -> None:
    """Persist the pipeline.
    Saves the versioned model, and overwrites any previous
    saved models. This ensures that when the package is
    published, there is only one trained model that can be
    called, and we know exactly how it was built.
    """

    # Prepare versioned save file name
    save_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
    save_path = TRAINED_MODEL_DIR / save_file_name

    remove_old_pipelines(files_to_keep=[save_file_name])
    joblib.dump(pipeline_to_persist, save_path)


def load_pipeline(*, file_name: str) -> Pipeline:
    """Load a persisted pipeline."""

    file_path = TRAINED_MODEL_DIR / file_name
    trained_model = None
    try:
        trained_model = joblib.load(filename=file_path)
    except BaseException:
        print("Cannot load saved pipline")

    return trained_model


def remove_old_pipelines(*, files_to_keep: t.List[str]) -> None:
    """
    Remove old model pipelines.
    This is to ensure there is a simple one-to-one
    mapping between the package version and the model
    version to be imported and used by other applications.
    """
    do_not_delete = files_to_keep + ["__init__.py"]
    for model_file in TRAINED_MODEL_DIR.iterdir():
        if model_file.name not in do_not_delete:
            model_file.unlink()
