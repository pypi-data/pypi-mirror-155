"""
    DataStructure to serialize a Keras Model
    It puts the network architecture as metadata and pickles the weights.
"""
import pickle

# import logging
from soil.storage.object_storage import ObjectStorage
from soil.data_structures.data_structure import DataStructure


class RandomForestModel(DataStructure):
    """Data Structure for a Sklearn Model"""

    @classmethod
    def deserialize(cls, serialized, metadata):
        """Function to deserialize"""
        return cls(pickle.loads(serialized.get_object()), metadata)

    def serialize(self):
        """Function to serialize"""
        obj_storage = ObjectStorage()
        obj_storage.put_object(pickle.dumps(self.data))
        return obj_storage

    def get_data(self, **_args):
        # pylint: disable=no-self-use
        """Placeholder function for the API call"""
        return {}
