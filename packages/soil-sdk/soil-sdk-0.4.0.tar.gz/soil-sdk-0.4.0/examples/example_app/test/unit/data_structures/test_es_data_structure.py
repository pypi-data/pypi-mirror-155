# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
# pylint: disable=no-self-use, protected-access
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch, call
# from types import GeneratorType
import pandas
from soil.storage.elasticsearch import Elasticsearch
from iris_dataset.data_structures import es_data_structure


class TestESDataStructure(unittest.TestCase):
    @patch.object(es_data_structure.ESDataStructure, "__init__", return_value=None)
    def test_deserialize_expected_inputs(self, mock_init):
        es_mock = MagicMock(spec=Elasticsearch)
        instance = es_data_structure.ESDataStructure.deserialize(es_mock, "ok2")
        assert isinstance(instance, es_data_structure.ESDataStructure)
        assert mock_init.mock_calls == [call(None, "ok2", storage=es_mock)]

    # Tests deserialize when object storage is none or not an object storage
    # DataStructure and object storage classes are required to do these tests)

    def test_deserialize_no_object_storage(self):
        self.assertRaises(
            NotImplementedError,
            es_data_structure.ESDataStructure.deserialize,
            None,
            MagicMock(spec=Elasticsearch),
        )

    def test_deserialize_no_es_storage(self):
        self.assertRaises(
            NotImplementedError,
            es_data_structure.ESDataStructure.deserialize,
            "something",
            MagicMock(spec="Invalid db"),
        )

    # def test_get_data(self):
    #     obj = es_data_structure.ESDataStructure()
    #     assert obj.get_data() == {}

    def test_serialize_no_index(self):
        obj = es_data_structure.ESDataStructure()
        self.assertRaises(AttributeError, obj.serialize)

    def test_serialize_no_data(self):
        obj = es_data_structure.ESDataStructure()
        obj.metadata = {"index": "test_index"}
        self.assertRaises(AttributeError, obj.serialize)

    @patch.object(Elasticsearch, "__init__", return_value=None)
    def test_serialize_expected(self, es_mock):
        obj = es_data_structure.ESDataStructure()
        obj.metadata = {"index": "test_index"}

        # This is to avoid an attributeError (see previous test)
        df = pandas.DataFrame({"test": [1, 2, 3, 4]}).to_dict("records")
        obj.data = df

        res = obj.serialize()
        assert es_mock.mock_calls[0] == call(index="test_index")
        assert isinstance(res, Elasticsearch)
