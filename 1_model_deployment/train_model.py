"""
Train a scikit learn model on the iris dataset and save it as an artifact
"""
if __name__ == "__main__":
    import pathlib

    import joblib
    from loguru import logger
    from sklearn.datasets import load_iris
    from sklearn.ensemble import RandomForestClassifier

    logger.info("Loading iris dataset")
    iris = load_iris()

    X = iris.data
    logger.info("Example feature: {}", X[0])
    y = iris.target

    model = RandomForestClassifier()

    logger.info("Training model")
    model.fit(X, y)

    model_path = pathlib.Path("model.joblib")
    logger.info(f"Saving model to {model_path}")
    joblib.dump(model, model_path)
