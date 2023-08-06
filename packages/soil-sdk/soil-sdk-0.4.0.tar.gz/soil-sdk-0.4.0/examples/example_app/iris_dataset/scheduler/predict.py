""" Module to train a predictor. """
import argparse
import logging
import soil
import pandas as pd
from soil.modules.make_predictions import make_predictions

soil.logger.setLevel(logging.INFO)


def get_preditictions(unlabeled_data_file=None):
    """Main function to train a predictor."""

    model = soil.data("trained-model-simple")

    data = pd.read_csv(unlabeled_data_file)
    data_ref = soil.data(data)

    preds, = make_predictions(model, data_ref)

    print("The predicted species for the input data are the following:")
    for i in preds.data:
        print(i)

    soil.alias("preds-simple", preds)


def main():
    """Argument parsing."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--unlabeled-data-file",
        type=argparse.FileType("r"),
        help="Pass unlabeled data here",
        required=True,
    )
    args = parser.parse_args()
    get_preditictions(**vars(args))


if __name__ == "__main__":
    main()
