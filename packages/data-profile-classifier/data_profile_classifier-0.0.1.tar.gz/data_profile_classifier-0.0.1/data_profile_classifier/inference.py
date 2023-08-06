from data_profile_classifier.preprocess import (
    load_object, predict,
    TARGET_ENCODER_FILENAME,
)


def make_predictions(predict_data_raw, models_dir):
    y_pred = predict(predict_data_raw, models_dir)
    le = load_object(models_dir, TARGET_ENCODER_FILENAME)
    return le.inverse_transform(y_pred)
