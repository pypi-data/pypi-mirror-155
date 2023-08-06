from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError

from bookRecommender.config.core import config


def drop_na_inputs(*, input_data: pd.DataFrame) -> pd.DataFrame:
    """Check model inputs for na values and filter."""
    validated_data = input_data.copy()
    new_vars_with_na = [var for var in config.model_config.features if var in validated_data[var].isnull().sum() > 0]
    validated_data.dropna(subset=new_vars_with_na, inplace=True)

    return validated_data


def validate_inputs(*, input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    """Check model inputs for unprocessable values."""

    # convert syntax error field names (beginning with numbers)

    # input_data["MSSubClass"] = input_data["MSSubClass"].astype("O")
    relevant_data = input_data.copy()
    validated_data = drop_na_inputs(input_data=relevant_data)
    errors = None

    try:
        # replace numpy nans so that pydantic can validate
        RecommenderBookDataInputs(inputs=validated_data.replace({np.nan: None}).to_dict(orient="records"))
    except ValidationError as error:
        errors = error.json()

    return validated_data, errors


class BookDataInputSchema(BaseModel):
    userID: Optional[int]
    ISBN: Optional[str]
    bookRating: Optional[int]
    bookTitle: Optional[str]
    bookAuthor: Optional[str]
    yearOfPublication: Optional[int]
    publisher: Optional[float]
    imageUrlS: Optional[str]
    imageUrlM: Optional[str]
    imageUrlL: Optional[float]
    Location: Optional[float]
    Age: Optional[int]


class RecommenderBookDataInputs(BaseModel):
    inputs: List[BookDataInputSchema]
