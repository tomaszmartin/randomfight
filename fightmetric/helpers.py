"""Helper methods for machine learning tasks."""
import pandas as pd

def get_feuture_importances(columns, model):
    """Creates a pandas DataFrame of feature importances.
    :param columns (list): List of column names.
    :param model (ClassifierMixin): trained model.
    :returns feature_importances (DataFrame): DataFrame of feature importances."""
    feats = {}
    for feature, importance in zip(columns, model.feature_importances_):
        feats[feature] = importance

    importances = pd.DataFrame.from_dict(feats, orient='index')
    importances = importances.rename(columns={0: 'Importance', 1: 'Feature'})
    return importances

def print_coeffs(columns, model):
    """Print coefficients with their weights."""
    print()
    for feature, importance in zip(columns, model.coef_[0]):
        print(f'{feature :20} {importance:.2f}')
    print()

def print_models(pairs):
    """Print models with their accuracy."""
    print()
    for name, accuracy in pairs:
        print(f'{name :20} {100*accuracy:.2f}%')
    print()
