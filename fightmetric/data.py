from datetime import datetime as dt
from pprint import pprint
import pandas as pd
import json


def map_dataset(event_date):
    """Map event date to one of datasets train, validation or test."""
    date = dt.strptime(event_date, "%Y-%m-%d")
    if date > dt(2015, 1, 1):
        return "test"
    if date > dt(2013, 1, 1):
        return "validation"
    return "train"


def map_target(result):
    """Map result to a target."""
    return {"Win": 1, "Loss": 0}[result]


def split_data(data):
    """Splits data into training, testing and validating."""
    data["set"] = data["date"].apply(map_dataset)
    # Split data
    xtrain = data[data["set"] == "train"].drop(["result", "set"])
    xvalidation = data[data["set"] == "validation"].drop(["result", "set"])
    xtest = data[data["set"] == "test"].drop(["result", "set"])
    # Split target
    ytrain = data[data["set"] == "train"]["result"].apply(map_target)
    yvalidation = data[data["set"] == "validation"].apply(map_target)
    ytest = data[data["set"] == "test"].apply(map_target)
    # Return data
    return xtrain, xvalidation, xtest, ytrain, yvalidation, ytest


if __name__ == "__main__":
    frame = pd.read_csv("data/transformed.csv", sep="|")
