import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go
import pandas as pd

def plot_discrete_countplots_plotly(df, target_col='target', custom_orders=None, n_cols=3, figsize_per_plot=(300, 300)):
    custom_orders = {
        'academic_year': [1, 2, 3, 4, 5, 6],
        'last_semester_student_ranking': ['Trung bình', 'Khá', 'Giỏi', 'Xuất sắc'],
        'conduct_score': ['< 50', '50-64', '65-79', '80-89', '90-100'],
        'last_semester_GPA': ['< 5','5-6','6-7','7-8','8-9','9-10'],
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
        'family_major_support': [1,2,3,4,5],
        'target_colors': {
            0: '#2ecc71',   # Green
            1: "#aaff2b",   # Yellow
            2: "#ff9d00",   # Light Orange
            3: '#e67e22',   # Dark Orange
            4: '#e74c3c'    # Red
        }
    }

    discrete_cols = df.select_dtypes(include=['object', 'category', 'int64', 'float64']) \
                      .drop(columns=[target_col], errors='ignore') \
                      .columns
    discrete_cols = [col for col in discrete_cols if df[col].nunique() <= 20]

    num_plots = len(discrete_cols)
    num_rows = -(-num_plots // n_cols)

    fig = sp.make_subplots(
        rows=num_rows, cols=n_cols,
        subplot_titles=discrete_cols,
        horizontal_spacing=0.1,
        vertical_spacing=0.05
    )

    shown_targets = set()

    for i, col in enumerate(discrete_cols):
        row = i // n_cols + 1
        col_pos = i % n_cols + 1

        order = custom_orders.get(col)
        df_plot = df.copy()
        if order:
            df_plot[col] = pd.Categorical(df_plot[col], categories=order, ordered=True)

        count_data = df_plot.groupby([col, target_col]).size().reset_index(name='count')

        for tgt in sorted(count_data[target_col].unique()):
            df_tgt = count_data[count_data[target_col] == tgt]

            show_legend = tgt not in shown_targets
            shown_targets.add(tgt)

            fig.add_trace(
                go.Bar(
                    x=df_tgt[col],
                    y=df_tgt['count'],
                    name=str(tgt),
                    showlegend=show_legend,
                    marker_color=custom_orders['target_colors'].get(tgt, px.colors.qualitative.Plotly[tgt])
                ),
                row=row, col=col_pos
            )

    fig.update_layout(
        height=500 * num_rows,
        width=500 * n_cols,
        title_text="Phân phối các biến rời rạc theo Target",
        title=dict(
            text="Đồ thị phân phối tần suất của các biến phân loại",
            x=0.5,
            font=dict(size=24)
        ),
        barmode='group',
        legend_title_text=target_col
    )

    fig.update_xaxes(tickangle=45 )

    fig.show()
