""" This program runs when new data arrives. """
import logging
import argparse
import json
import soil
from soil import logger
from soil.modules.to_es_data_structure import to_es_data_structure
from ..lib.utils import get_columns_dictnames, read_data

logger.setLevel(logging.DEBUG)
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def _new_data(input_file=None, schema_file=None):

    # Read schema
    schema = json.load(schema_file)
    columns = get_columns_dictnames(schema["columns"])

    # Read data
    # Adding new data does not delete previous data unless metadata["rewrite"]= True
    # (those entries whose id appear in both datasets are rewritten in any case)

    # Read data as a list of dictionaries
    data = read_data(input_file)

    soil_data_structure = soil.data(data, metadata={"columns": columns, "index": "iris-data"})
    # Add "rewrite":True to metadata to replace old data

    # Upload a list of dictionaries (without NaN values) to elasticsearch
    elasticsearch_data_structure, = to_es_data_structure(soil_data_structure)
    soil.alias("iris-data", elasticsearch_data_structure, roles=["user"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # inputs given by soil.yml must start by --
    # inputs given during script call (soil run ... <input-file>) do not
    parser.add_argument(
        "input_file", type=argparse.FileType("r"), help="The input file"
    )
    parser.add_argument(
        "--schema-file",
        type=argparse.FileType("r"),
        help="The file with the schema of the data",
        required=True,
    )
    args = parser.parse_args()
    _new_data(**vars(args))
