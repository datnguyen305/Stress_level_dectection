# threshold_tuning.py
import optuna
import numpy as np
from sklearn.metrics import recall_score, f1_score
from sklearn.svm import SVC
from config import SEED

def optimize_svm_threshold_recall(X_train, y_train, X_dev, y_dev, n_trials=200):
    n_classes = len(np.unique(y_train))
    best_model, best_thresholds = None, None
    best_recall, best_f1 = -1.0, -1.0

    def objective(trial):
        nonlocal best_model, best_thresholds, best_recall, best_f1

        params = {
            'C': trial.suggest_float('C', 1e-3, 1e3, log=True),
            'kernel': trial.suggest_categorical('kernel', ['linear', 'rbf', 'poly']),
            'degree': trial.suggest_int('degree', 2, 5),
            'gamma': trial.suggest_categorical('gamma', ['scale', 'auto']),
            'probability': True,
            'class_weight': 'balanced'
        }
        model = SVC(**params)
        model.fit(X_train, y_train)
        probas = model.predict_proba(X_dev)

        thresholds = [trial.suggest_float(f"thresh_{i}", 0.1, 1.0) for i in range(n_classes)]
        adjusted_preds = np.argmax(probas / thresholds, axis=1)

        recall = recall_score(y_dev, adjusted_preds, average='weighted')
        f1 = f1_score(y_dev, adjusted_preds, average='weighted')

        if recall > best_recall:
            best_model = model
            best_thresholds = thresholds
            best_recall = recall
            best_f1 = f1

        return recall

    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=n_trials)
    return best_model, best_thresholds, best_recall
