# main.py
from data_loader import load_and_split_data
from tuning_models import optimize_svc
from threshold_tuning import optimize_svm_threshold_recall
from visualization import plot_log_loss_vs_threshold_multiclass_all_in_one, plot_multiclass_roc_auc, plot_multiclass_det, plot_learning_curve
from sklearn.metrics import recall_score, f1_score

X_train, X_dev, X_test, y_train, y_dev, y_test, df = load_and_split_data()

model, thresholds, recall = optimize_svm_threshold_recall(X_train, y_train, X_dev, y_dev)

# Apply to test set
probas = model.predict_proba(X_test)
adjusted_preds = []
for row in probas:
    adjusted = row / thresholds
    adjusted = adjusted / sum(adjusted)
    pred = np.argmax(adjusted)
    adjusted_preds.append(pred)

print("📌 Recall (test):", recall_score(y_test, adjusted_preds, average='weighted'))
print("📌 F1-score (test):", f1_score(y_test, adjusted_preds, average='weighted'))

# Visualization
plot_log_loss_vs_threshold_multiclass_all_in_one(model, X_test, y_test)
plot_multiclass_roc_auc(model, X_test, y_test, sorted(df['target'].unique()))
plot_multiclass_det(model, X_test, y_test, sorted(df['target'].unique()))
plot_learning_curve(model, df.drop(columns=['target']), df['target'], scoring='f1_weighted')
