""" Module to train a predictor. """
import argparse
import logging
import soil
from soil import logger
from soil.modules.retrain_predictor import retrain_predictor

# These lines allow the use the use of data structures in its current state
# Use these during code development if any change has been done since data was uploaded
# from soil.data_structures import es_data_structure
# from soil.modules.to_es_data_structure import to_es_data_structure


logger.setLevel(logging.DEBUG)


def train_predictor():
    """Main function to train a predictor."""

    data = soil.data("iris-data")
    predictor_ref, = retrain_predictor(data)
    soil.alias("trained-model-simple", predictor_ref)


def main():
    """Argument parsing."""
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    train_predictor(**vars(args))


if __name__ == "__main__":
    main()
