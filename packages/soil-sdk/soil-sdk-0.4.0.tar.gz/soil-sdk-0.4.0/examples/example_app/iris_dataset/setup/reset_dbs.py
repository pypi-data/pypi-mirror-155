""" This program runs when new data arrives. """
import logging
import argparse
import soil
from soil.modules.to_es_data_structure import to_es_data_structure

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def _reset_dbs():

    # We replace all data in each used data structure by an empty lists, efectively reseting data bases.
    data = []

    logging.info("Cleaning index: simple-data")
    data_ref = soil.data(data, metadata={"index": "simple-data", "rewrite": True})
    (res,) = to_es_data_structure(data_ref)
    soil.alias("flowers", res)

    logging.info("Cleaning index: simple-preds")
    data_ref = soil.data(data, metadata={"index": "simple-preds", "rewrite": True})
    (res,) = to_es_data_structure(data_ref)
    soil.alias("preds", res)

    # # This can be added (in this case we have to modify the corresponding test)
    # # Also, modules should admit empty predictors
    # logging.info('Cleaning trained-model')
    # data_ref = soil.data(data, metadata={'rewrite': True})
    # soil.alias('trained-model', data_ref)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    _reset_dbs(**vars(args))
