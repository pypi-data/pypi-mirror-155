# README

This is an example SOIL application using the iris dataset, which is created when staring a new soil project (soil init <project-name>).

This data set contains 3 classes of 50 instances each, where each class refers to a type of iris plant.

The example trains a model to predict the type of 10 additional instances.

## Install

Create a python virtual enviorment
```sh
python -m venv .venv
```

Activate the virtual enviorment


```sh
source .venv/bin/activate
```
Install required packages to

```sh
pip install -r requirements.txt
```

```sh
pip install -r requirements_remote.txt
```

Only if you are creating a new repo.
```sh
git init
```

You are going to love and hate this (not in this order).
```
pre-commit install
```

## Scripts

The virtual enviorment should be activated everytime you work with this project.

```sh
source .venv/bin/activate
```

To run a specific script follow soil.yml

### Reset indexes
Run this script to reset the data uploaded to elasticsearch (data set and predictors).
It does not delete the index but removes all documents updated to those indexes.
```sh
soil run setup reset-dbs
```


### Upload new data
Run this script to upload the iris data set to elasticsearch.
As soil.yml does not set a input-file, it must be passed as an argument (data/iris.csv)
```sh
soil run data new-data data/iris.csv
```

### Train model

Run this script to train the model.

```sh
soil run schedules train
```


### Do predictions
Run this script to predict the type of the iris plants described in unkonwn.csv.
Note that this time soil.yml does fix data/unknown.csv as the input-file (cf. Upload new data)
```sh
soil run schedules predict
```
