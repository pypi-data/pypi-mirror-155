""" Module to train the predictor """
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from soil import modulify
from soil import logger
from soil.data_structures.random_forest_model import RandomForestModel


@modulify(output_types=lambda *input_types, **args: [RandomForestModel])
def retrain_predictor(data):
    """Trains the predictor with available data"""

    model = RandomForestClassifier(oob_score=True)

    metadata = data.metadata
    x_labels = metadata["columns"]["X_columns"]  # list (metada)
    y_labels = metadata["columns"]["y_columns"]

    # Since Data frame can be defined from an iterator, there is no need to acces data.data
    # df = pd.DataFrame(data.get_data())
    df = pd.DataFrame(data)

    model = model.fit(df[x_labels].values, df[y_labels].values.ravel())

    logger.info("Model oob score: %s", model.oob_score_)
    logger.info("Model error: %s", 1 - model.oob_score_)

    model_metadata = {
        "oob_score": model.oob_score_,
        "error": 1 - model.oob_score_,
        "x_labels": x_labels,
        "y_labels": y_labels,
    }

    return [RandomForestModel(model, model_metadata)]
