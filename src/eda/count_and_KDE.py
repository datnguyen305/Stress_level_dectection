import seaborn as sns
import matplotlib.pyplot as plt
import math

def plot_discrete_distribution_by_target_combined(df, target_col='target', custom_orders=None, max_cols=2):
    """
    Vẽ biểu đồ countplot cho các cột rời rạc trong DataFrame trong 1 figure duy nhất (nhiều subplot).
    
    Parameters:
    - df: DataFrame
    - target_col: tên cột target
    - custom_orders: dict ánh xạ tên cột -> thứ tự giá trị hiển thị (order)
    - max_cols: số lượng cột tối đa trong layout subplot
    """
    if custom_orders is None:
        custom_orders = {}

    discrete_cols = df.select_dtypes(include=['object', 'category', 'int64', 'float64']).columns.drop(target_col, errors='ignore')
    num_cols = len(discrete_cols)
    num_targets = df[target_col].nunique()

    # Tạo grid subplot
    rows = math.ceil(num_cols / max_cols)
    fig, axes = plt.subplots(rows, max_cols, figsize=(max_cols * 6, rows * 5))
    axes = axes.flatten() if num_cols > 1 else [axes]

    for i, col in enumerate(discrete_cols):
        order = custom_orders.get(col)
        try:
            sns.countplot(data=df, x=col, hue=target_col, order=order, ax=axes[i])
            axes[i].set_title(f'Phân phối {col} theo {target_col}')
            axes[i].tick_params(axis='x', rotation=45)
        except Exception as e:
            print(f"⚠️ Không thể vẽ cột '{col}': {e}")
            axes[i].set_visible(False)  # Ẩn subplot bị lỗi

    # Ẩn subplot thừa
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)

    plt.tight_layout()
    plt.show()
