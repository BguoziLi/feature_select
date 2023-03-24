import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.feature_selection import RFECV

rf = RandomForestClassifier(random_state=42)
gb = GradientBoostingClassifier(random_state=42)
xgb = XGBClassifier()
svm = SVC(random_state=42)
mlp = MLPClassifier(random_state=42)
models = [rf, rf, gb, xgb, svm, mlp]


def univariate_statistics(df, filename: str):
    filename_split = filename.strip().split('/')[-1].split('.')
    output_filename = filename_split[0] + '_uni_output' + filename_split[0]
    print(df.head())
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    colNames = X.columns.to_list()
    select = SelectKBest(score_func=f_classif, k=10).fit(X, y)
    features = [i for i, j in zip(colNames, select.get_support()) if j]
    df = pd.concat([X.loc[:, features], y])
    df.to_csv(f'./output/{output_filename}', index=False)
    return output_filename


def select_from_model(df, p2, filename):
    filename_split = filename.strip().split('/')[-1].split('.')
    output_filename = filename_split[0] + '_model_output' + filename_split[0]
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    colNames = X.columns.to_list()
    select = SelectFromModel(models[p2], max_features=10).fit(X, y)
    features = [i for i, j in zip(colNames, select.get_support()) if j]
    df = pd.concat([X.loc[:, features], y])
    df.to_csv(f'./output/{output_filename}', index=False)
    return output_filename


def select_from_RFECV(df, p2, filename):
    filename_split = filename.strip().split('/')[-1].split('.')
    output_filename = filename_split[0] + '_RFECV_output' + filename_split[0]
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    colNames = X.columns.to_list()
    select = RFECV(models[p2], step=1, cv=5).fit(X, y)
    features = [i for i, j in zip(colNames, select.get_support()) if j]
    df = pd.concat([X.loc[:, features], y])
    df.to_csv(f'./output/{output_filename}', index=False)
    return output_filename
