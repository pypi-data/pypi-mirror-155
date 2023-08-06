# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring, no-self-use
import unittest
from unittest.mock import patch
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from iris_dataset.modules import retrain_predictor
from .patch_decorators import patch_modulify


metadata = {
    "columns": {
        "X_columns": {
            "sepal_length": {"name": "sepal_length", "type": "float"},
            "sepal_width": {"name": "sepal_width", "type": "float"},
            "petal_length": {"name": "petal_length", "type": "float"},
            "petal_width": {"name": "petal_width", "type": "float"},
        },
        "y_columns": {"species": {"name": "species", "type": "str"}},
    }
}


class InputDS:
    def __init__(self, data, metadata_ref=None):
        self.data = data
        self.metadata = metadata_ref if metadata_ref is not None else {}
        self.iter = iter([d[1] for d in self.data.iterrows()])

    def __iter__(self):
        return self.iter
        # self.iter = iter([d[1] for d in self.data.iterrows()])
        # return self

    def __next__(self):
        return next(self.iter)

    def get_data(self):
        return self.data


# This test is buggy
# class TestModulifiedRetrainPredictor(unittest.TestCase):
#     def test_output_types(self):
#         # This is a bit hacky but in tests it's fine.
#         output_types_fn = retrain_predictor().retrain_predictor.__closure__[-1].cell_contents
#         assert output_types_fn() == [RandomForestModel]


@patch_modulify(retrain_predictor)
class TestRetrainPredictor(unittest.TestCase):
    @patch("iris_dataset.modules.retrain_predictor.RandomForestModel")
    def test_retrain_predictor(self, mocked_rfmodel):
        np.random.seed(1111)
        mocked_rfmodel.return_value = "ok"
        fixture = pd.read_csv("./data/iris.csv")
        dataset = InputDS(fixture, metadata)  # Mock DS??
        [result] = retrain_predictor.retrain_predictor(dataset)
        assert result == "ok"
        assert len(mocked_rfmodel.call_args_list) == 1
        args, _kwargs = mocked_rfmodel.call_args_list[0]
        assert len(args) == 2
        assert isinstance(args[0], RandomForestClassifier)
        assert args[0].oob_score
        assert args[1] == {
            "oob_score": 0.9466666666666667,
            "error": 0.053333333333333344,
            "x_labels": metadata["columns"]["X_columns"],
            "y_labels": {"species": {"name": "species", "type": "str"}},
        }
