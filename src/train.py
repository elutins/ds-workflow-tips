import structlog
import os
import pandas as pd
import numpy as np 
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

import src.helpers as helpers

logger = structlog.get_logger()


def main(ARGS):
    logger.info("reading in data 📚")
    data = pd.read_csv('/Users/evanlutins/Downloads/hotel-booking-demand.zip', compression='zip')
    logger.info("done reading in data 📚", data_points=len(data))

    if len(data) < 100:
        logger.warning("insuffient data. proceeding anyways 🤥", data_points=len(data))

    # creating and saving a test set to predict on later in pipeline
    msk = np.random.rand(len(data)) < 0.2
    test = data[~msk]
    helpers.ensure_file_path(os.path.dirname("~/hotel_bookings/test.json.gz"))
    test.to_json("~/hotel_bookings/test.json.gz", orient="records", compression="gzip", lines=True)
    
    logger.info('transforming data to necessary format for modeling 🤖')
    data = helpers.transform_data(data, training_flag=True)
    
    X_train, X_test, y_train, y_test = helpers.generate_test_train_sets(data, field='is_canceled')

    logger.info("fitting model 👟", training_points=len(X_train))
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    logger.info("model fitting complete 👟")

    model.feature_names = list(X_train.columns.values)

    # printing out some model metrics to include in logging message
    preds = model.predict(X_test)
    accuracy = round(metrics.accuracy_score(y_test, preds), 3)
    roc = round(metrics.roc_auc_score(y_test, preds), 3)
    
    logger.info("model metrics 🎯", accuracy=accuracy, roc_auc=roc)

    if not ARGS.local:
        logger.info("exporting model to be loaded during predicting 🚀", data_dir=ARGS.data_dir)
        model_file = os.path.join(ARGS.data_dir, "model.pkl")
        helpers.ensure_file_path(os.path.dirname(model_file))
        pickle.dump(model, open(model_file, "wb"))
        logger.info("successfully exported model 🚀", output_file=model_file)
