import plotly.graph_objects as go
import numpy as np
from utils.math import interpolate_curve_3d
from typing import *

class VectorPlotter:
    def __init__(self, x_label: str = "Энергия, Дж", 
                 y_label: str = "Длительность, мс", 
                 z_label: str = "Толщина отложений, мм"):
        self.x_label = x_label
        self.y_label = y_label
        self.z_label = z_label
    
    def plot_3d(self, X: list[float | int], Y: list[float | int], Z: list[float | int], title: str = "Годограф отложений"):
        """
        Строит 3D-График: векторы от 0 до точек (X[i], Y[i], Z[i])
        :param X: Массив значений энергии (столбец E)
        :param Y: Массив значений длительности (столбец F)
        :param Z: Массив значений толщины отложений (столбец A)
        :param title: Заголовок графика
        """
        fig = go.Figure()

        # Добавляем точки (концы векторов)
        fig.add_trace(go.Scatter3d(
            x=X, y=Y, z=Z,
            mode='markers+text',
            marker=dict(size=8, color='red', opacity=0.8),
            text=[f"Z={z:.1f}" for z in Z],
            textposition="top center",
            name='Точки годографа'
        ))

        # Добавляем векторы как линии + маркеры на конце
        for i in range(len(X)):
            fig.add_trace(go.Scatter3d(
                x=[0, X[i]], y=[0, Y[i]], z=[0, Z[i]],
                mode='lines',
                line=dict(color='blue', width=3),
                name=f'Вектор {i+1} (линия)',
                hoverinfo='skip'
            ))

            fig.add_trace(go.Scatter3d(
                x=[X[i]], y=[Y[i]], z=[Z[i]],
                mode='markers',
                marker=dict(size=6, color='blue', symbol='circle'),
                name=f'Конец вектора {i+1}',
                hoverinfo='skip'
            ))

        # Настройки UI
        fig.update_layout(
            title=title,
            scene=dict(
                xaxis_title=self.x_label,
                yaxis_title=self.y_label,
                zaxis_title=self.z_label,
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)),
                aspectmode='cube',
                xaxis=dict(range=[0, max(X)*1.1]),
                yaxis=dict(range=[0, max(Y)*1.1]),
                zaxis=dict(range=[0, max(Z)*1.1])
            ),
            margin=dict(l=0, r=0, b=0, t=40),
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        )

        fig.show(renderer="browser", config={'responsive': True})

    def plot_godograph_3d(self, X: list[float | int], Y: list[float | int], Z: list[float | int], title: str ="Годограф толщины отложений"):
        """
        Строит 3D-годограф: векторы от 0 до точек (X[i], Y[i], Z[i]) + кривая, соединяющая концы векторов
        :param X: Массив значений энергии (столбец E)
        :param Y: Массив значений длительности (столбец F)
        :param Z: Массив значений толщины отложений (столбец A)
        :param title: Заголовок графика
        """
        fig = go.Figure()

        # Сортируем данные по Z, чтобы годограф рисовался в порядке роста толщины
        indices = np.argsort(Z)
        X_sorted = np.array(X)[indices]
        Y_sorted = np.array(Y)[indices]
        Z_sorted = np.array(Z)[indices]

        fig.add_trace(go.Scatter3d(
            x=X_sorted, y=Y_sorted, z=Z_sorted,
            mode='markers+text',
            marker=dict(size=3, color='red', opacity=0.8),
            text=[f"Z={z:.1f}" for z in Z_sorted],
            textposition="top center",
            name='Точки годографа'
        ))

        # Рисуем годограф перед этим интерполировав его
        X_smooth, Y_smooth, Z_smooth = interpolate_curve_3d(X_sorted, Y_sorted, Z_sorted, num_points=300)
        fig.add_trace(go.Scatter3d(
            x=X_smooth, y=Y_smooth, z=Z_smooth,
            mode='lines',
            line=dict(color='green', width=4),
            name='Годограф (гладкая кривая)',
            hoverinfo='skip'
        ))

        # Добавляем векторы как линии + конусы на концах
        for i in range(len(X_sorted)):
            fig.add_trace(go.Scatter3d(
                x=[0, X_sorted[i]], y=[0, Y_sorted[i]], z=[0, Z_sorted[i]],
                mode='lines',
                line=dict(color='blue', width=3),
                name=f'Вектор {i+1} (линия)',
                hoverinfo='skip'
            ))

            fig.add_trace(go.Cone(
                x=[X_sorted[i]], y=[Y_sorted[i]], z=[Z_sorted[i]],
                u=[X_sorted[i]], v=[Y_sorted[i]], w=[Z_sorted[i]],
                sizeref=0.05,
                anchor="tip",
                showscale=False,
                colorscale=[[0, 'blue'], [1, 'blue']],
                name=f'Стрелка {i+1}',
                hoverinfo='skip'
            ))

        fig.update_layout(
            title=title,
            scene=dict(
                xaxis_title=self.x_label,
                yaxis_title=self.y_label,
                zaxis_title=self.z_label,
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)),
                aspectmode='cube',
                xaxis=dict(range=[0, max(X)*1.1]),
                yaxis=dict(range=[0, max(Y)*1.1]),
                zaxis=dict(range=[0, max(Z)*1.1])
            ),
            margin=dict(l=0, r=0, b=0, t=40),
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        )

        fig.show(renderer="browser", config={'responsive': True})