import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_categorical_distributions_plotly(df: pd.DataFrame, custom_orders: dict = None, n_cols: int = 3):
    if custom_orders is None:
        custom_orders = {
            'last_semester_student_ranking': ['Trung bình', 'Khá', 'Giỏi', 'Xuất sắc'],
            'conduct_score': ['< 50', '50-64', '65-79', '80-89', '90-100'],
            'last_semester_GPA': ['<5','5-6','6-7','7-8','8-9','9-10'],
            'self_study_hours': ['< 1', '1 - 2', '2 - 3', '3 - 4', '> 4'],
            'amount_hours_spent_on_social_media': ['< 2h', '2 - 5h', '5 - 7h', '> 7h'],
            'average_time_spent_sleeping': ['< 5', '5 - 6.9', '7 - 9', '> 9'],
            'class_attendance_percent': ['< 20%', '20 - 50', '50 - 80', '80 - 100'],
            'activity_engagement_level': [1,2,3,4,5],
            'internet_adaptation': [1,2,3,4,5],
            'workout_rate': [1,2,3,4,5],
            'sharing_frequency': [1,2,3,4,5],
            'family_affects': [1,2,3,4,5],
            'family_allowance_sufficiency': [1,2,3,4,5],
            'family_educational_level': [1,2,3,4,5],
            'family_major_support': [1,2,3,4,5]
        }

    categorical_cols = df.select_dtypes(include=['object', 'category', 'int64', 'float64']).columns.tolist()
    n_charts = len(categorical_cols)
    n_rows = -(-n_charts // n_cols)  # ceil division

    fig = make_subplots(rows=n_rows, cols=n_cols,
                        subplot_titles=categorical_cols,
                        horizontal_spacing=0.1,
                        vertical_spacing=0.05)

    for idx, col in enumerate(categorical_cols):
        row = idx // n_cols + 1
        col_pos = idx % n_cols + 1

        value_counts = df[col].value_counts(normalize=True) * 100

        # Reorder if needed
        if col in custom_orders:
            order = custom_orders[col]
            value_counts = value_counts.reindex(order).fillna(0)
        else:
            order = value_counts.sort_index().index.tolist()
            value_counts = value_counts.reindex(order).fillna(0)

        fig.add_trace(
            go.Bar(
                x=value_counts.index.astype(str),
                y=value_counts.values,
                marker=dict(color='green'),
                showlegend=False,
                hovertemplate='Value: %{x}<br>Percentage: %{y:.2f}%<extra></extra>'
            ),
            row=row,
            col=col_pos
        )
        

    fig.update_layout(
        height=500 * n_rows,
        width=500 * n_cols,
        title_text="Đồ thị phân phối tần suất của các biến phân loại",
        showlegend=False,
        title={
            "text": "Đồ thị phân phối tần suất của các biến phân loại",
            "x": 0.5,
            "y": 0.99,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 24}
        },
        plot_bgcolor='mintcream',        
        paper_bgcolor='white', 
    )
    fig.update_xaxes(showgrid=True, gridcolor='lightgrey', griddash='dot')
    fig.update_yaxes(
    showgrid=True,
    gridcolor='lightgrey',
    griddash='dot',
    ticksuffix='%',
    ticklabelposition="outside left",  # đặt tick ra ngoài bên trái
)

    for annotation in fig['layout']['annotations']:
        annotation['y'] += 0.002  # tăng 0.05 đơn vị normalized (tùy chỉnh thêm nếu cần)
    fig.show()
