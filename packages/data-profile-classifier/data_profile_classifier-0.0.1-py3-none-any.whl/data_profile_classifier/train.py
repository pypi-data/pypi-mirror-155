from data_profile_classifier.preprocess import (
    predict, train_model, clean_raw_data, split_train_data_raw,
    TARGET_FEATURE
)


def build_model(data_raw, models_dir):
    cleaned_data = clean_raw_data(data_raw)
    X_train, X_val, y_train, y_val = split_train_data_raw(
        cleaned_data, models_dir, TARGET_FEATURE)
    # Train model and predict
    train_model(X_train, y_train, models_dir)
    y_pred = predict(X_val, models_dir)
    return y_val, y_pred
