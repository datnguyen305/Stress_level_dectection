# visualization.py
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import log_loss, roc_curve, auc, det_curve
from sklearn.preprocessing import label_binarize
from sklearn.model_selection import learning_curve, StratifiedKFold

def plot_log_loss_vs_threshold_multiclass_all_in_one(model, X_test, y_test):
    y_prob = model.predict_proba(X_test)
    n_classes = y_prob.shape[1]
    thresholds = np.linspace(0.01, 1.0, 50)

    plt.figure(figsize=(8, 6))
    for class_index in range(n_classes):
        log_losses = []
        for thresh in thresholds:
            adjusted_prob = y_prob.copy()
            adjusted_prob[:, class_index] = y_prob[:, class_index] / thresh
            adjusted_prob /= adjusted_prob.sum(axis=1, keepdims=True)
            adjusted_prob = np.clip(adjusted_prob, 1e-15, 1 - 1e-15)
            loss = log_loss(y_test, adjusted_prob, labels=np.arange(n_classes))
            log_losses.append(loss)

        plt.plot(thresholds, log_losses, label=f'Class {class_index}')
    plt.xlabel('Threshold (probability adjustment)')
    plt.ylabel('Log Loss')
    plt.title('Log Loss vs. Threshold per class')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_multiclass_roc_auc(model, X_test, y_test, class_names):
    y_score = model.predict_proba(X_test)
    y_bin = label_binarize(y_test, classes=class_names)

    fpr, tpr, roc_auc = {}, {}, {}
    for i in range(len(class_names)):
        fpr[i], tpr[i], _ = roc_curve(y_bin[:, i], y_score[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    plt.figure(figsize=(8, 6))
    for i in range(len(class_names)):
        plt.plot(fpr[i], tpr[i], label=f'Class {class_names[i]} (AUC = {roc_auc[i]:.2f})')
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve (Multi-class)')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_multiclass_det(model, X_test, y_test, class_names):
    y_score = model.predict_proba(X_test)
    y_bin = label_binarize(y_test, classes=class_names)

    plt.figure(figsize=(8, 6))
    for i in range(len(class_names)):
        fpr, fnr, _ = det_curve(y_bin[:, i], y_score[:, i])
        plt.plot(fpr, fnr, label=f'Class {class_names[i]}')

    plt.xlabel('False Positive Rate (FPR)')
    plt.ylabel('False Negative Rate (FNR)')
    plt.title('DET Curve (Multi-class)')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_learning_curve(estimator, X, y, title="Learning Curve",
                        scoring='f1_weighted', cv=5,
                        train_sizes=np.linspace(0.1, 1.0, 5),
                        n_jobs=-1, random_state=42):
    """
    Hàm vẽ learning curve cho một estimator.

    Parameters:
        estimator: mô hình huấn luyện (ví dụ: LogisticRegression(), SVC(), ...)
        X: features (ndarray hoặc DataFrame)
        y: labels
        title: tiêu đề đồ thị
        scoring: độ đo đánh giá (accuracy, f1_macro, ...)
        cv: số fold hoặc object chia tập cross-validation
        train_sizes: danh sách tỷ lệ dữ liệu huấn luyện dùng để vẽ (mặc định: từ 10% đến 100%)
        n_jobs: số lượng CPU để chạy song song (mặc định -1: dùng tất cả)
        random_state: để tái hiện được kết quả
    """

    if isinstance(cv, int):
        cv = StratifiedKFold(n_splits=cv, shuffle=True, random_state=random_state)

    train_sizes_abs, train_scores, test_scores = learning_curve(
        estimator, X, y,
        train_sizes=train_sizes,
        cv=cv,
        scoring=scoring,
        n_jobs=n_jobs,
        shuffle=True,
        random_state=random_state
    )

    train_scores_mean = train_scores.mean(axis=1)
    train_scores_std = train_scores.std(axis=1)

    test_scores_mean = test_scores.mean(axis=1)
    test_scores_std = test_scores.std(axis=1)

    plt.figure(figsize=(8, 6))
    plt.title(title)
    plt.xlabel("Số mẫu huấn luyện")
    plt.ylabel(f"Score ({scoring})")
    plt.xlim(0, 225)
    plt.ylim(0.2, 1.25)
    plt.grid(True)
    plt.fill_between(train_sizes_abs,
                     train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std,
                     alpha=0.1, color="r")
    plt.fill_between(train_sizes_abs,
                     test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std,
                     alpha=0.1, color="g")
    plt.plot(train_sizes_abs, train_scores_mean, 'o-', color="r", label="Train score")
    plt.plot(train_sizes_abs, test_scores_mean, 'o-', color="g", label="Validation score")

    plt.legend(loc="best")
    plt.tight_layout()
    plt.show()
