import optuna
from sklearn.metrics import f1_score
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from config import SEED

def optimize_svc(X_train, y_train, X_dev, y_dev, n_trials=100, random_state=42):
    best_model = None
    best_f1 = -1.0

    def objective(trial):
        nonlocal best_model, best_f1

        params = {
            'C': trial.suggest_loguniform('C', 1e-3, 1e2),
            'kernel': trial.suggest_categorical('kernel', ['linear', 'rbf', 'poly']),
            'probability': True
        }

        if params['kernel'] in ['rbf', 'poly']:
            params['gamma'] = trial.suggest_loguniform('gamma', 1e-4, 1e0)

        if params['kernel'] == 'poly':
            params['degree'] = trial.suggest_int('degree', 2, 5)

        model = SVC(**params)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_dev)
        f1 = f1_score(y_dev, y_pred, average='weighted')

        if f1 > best_f1:
            best_f1 = f1
            best_model = model

        return f1

    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=n_trials)

    return best_model

def optimize_knn(X_train, y_train, X_dev, y_dev, n_trials=100, random_state=42):
    best_model = None
    best_f1 = -1.0

    def objective(trial):
        nonlocal best_model, best_f1

        params = {
            'n_neighbors': trial.suggest_int('n_neighbors', 1, 30),
            'weights': trial.suggest_categorical('weights', ['uniform', 'distance']),
            'p': trial.suggest_int('p', 1, 2)
        }

        model = KNeighborsClassifier(**params)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_dev)
        f1 = f1_score(y_dev, y_pred, average='weighted')

        if f1 > best_f1:
            best_f1 = f1
            best_model = model

        return f1

    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=n_trials)

    return best_model

def optimize_tree(X_train, y_train, X_dev, y_dev, n_trials=100, random_state=42):
    best_model = None
    best_f1 = -1.0

    def objective(trial):
        nonlocal best_model, best_f1

        params = {
            'criterion': trial.suggest_categorical('criterion', ['gini', 'entropy']),
            'max_depth': trial.suggest_int('max_depth', 1, 5),
            'min_samples_split': trial.suggest_int('min_samples_split', 2, 10),
            'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 5),
            'class_weight': 'balanced'
        }

        model = DecisionTreeClassifier(**params)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_dev)
        f1 = f1_score(y_dev, y_pred, average='weighted')

        # Lưu lại mô hình tốt nhất
        if f1 > best_f1:
            best_f1 = f1
            best_model = model

        return f1

    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=n_trials)

    return best_model

def optimize_lightgbm(X_train, y_train, X_dev, y_dev, n_trials=100, random_state=42):
    best_model = None
    best_f1 = -1.0
    def objective(trial):
      nonlocal best_model, best_f1
      params = {
          'n_estimators': trial.suggest_int('n_estimators', 50, 200),
          'learning_rate': trial.suggest_float('learning_rate', 0.001, 1.0, log=True),
          'verbosity': -1,
          'num_leaves': trial.suggest_int('num_leaves', 10, 100),
          'max_depth': trial.suggest_int('max_depth', 1, 10),
          'min_child_samples': trial.suggest_int('min_child_samples', 1, 100),
          'subsample': trial.suggest_float('subsample', 0.1, 1.0),
          'colsample_bytree': trial.suggest_float('colsample_bytree', 0.1, 1.0),
          'reg_alpha': trial.suggest_float('reg_alpha', 0.0, 1.0),
          'reg_lambda': trial.suggest_float('reg_lambda', 0.0, 1.0),
          'class_weight': 'balanced'
      }
      model = LGBMClassifier(**params)
      model.fit(X_train, y_train)
      y_pred = model.predict(X_dev)
      f1 = f1_score(y_dev, y_pred, average='weighted')

      if f1 > best_f1:
        best_f1 = f1
        best_model = model

        return f1

    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=n_trials)

    return best_model

def optimize_catboost(X_train, y_train, X_dev, y_dev, n_trials=100, random_state=42):
    best_model = None
    best_f1 = -1.0

    def objective(trial):
        nonlocal best_model, best_f1

        params = {
            'iterations': trial.suggest_int('iterations', 50, 200),
            'learning_rate': trial.suggest_float('learning_rate', 0.001, 1.0, log=True),
            'depth': trial.suggest_int('depth', 3, 10),
            'l2_leaf_reg': trial.suggest_float('l2_leaf_reg', 1e-8, 100, log=True),
            'border_count': trial.suggest_int('border_count', 32, 255),
            'verbose': 0,
            'auto_class_weights': 'Balanced'
        }

        model = CatBoostClassifier(**params)
        model.fit(X_train, y_train, eval_set=[(X_dev, y_dev)], early_stopping_rounds=10, verbose=0)
        y_pred = model.predict(X_dev)
        f1 = f1_score(y_dev, y_pred, average='weighted')

        if f1 > best_f1:
            best_f1 = f1
            best_model = model

        return f1

    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=n_trials)

    return best_model



