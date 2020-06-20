import structlog
import os
import pickle
import pandas as pd
import src.helpers as helpers

logger = structlog.get_logger()


def main(ARGS):
    logger.info("reading in test data 📚")
    data = pd.read_json("~/hotel_bookings/test.json.gz", compression="gzip", lines=True)
    # data = pd.read_csv('/Users/evanlutins/Downloads/hotel-booking-demand.zip', compression='zip')
    logger.info("done reading in data 📚", data_points=len(data))    

    logger.info("transforming data to necessary format for prediction 🤖")
    data = helpers.transform_data(data, training_flag=False)

    logger.info("loading model 🚚")
    model_file = os.path.join(ARGS.data_dir, "model.pkl")
    model = pickle.load(open(model_file, "rb"))
    logger.info("model loaded 🚚", model_file=model_file)

    feature_names = model.feature_names

    logger.info("cross referencing training & testing fields")
    data = helpers.crosscheck_testing_fields(test_data=data, training_fields=feature_names)
    
    logger.info("forming predictions 🎯")
    preds = model.predict(data[feature_names])
    data["preds"] = preds

    if not ARGS.local:
        logger.info("exporting predictions 🚀")
        output_file = os.path.join(ARGS.data_dir, "output.json.gz")
        helpers.ensure_file_path(os.path.dirname(output_file))
        data.to_json(output_file, orient="records", compression="gzip", lines=True)
        logger.info("predictions have been successfully exported 🚀", output_file=output_file)
