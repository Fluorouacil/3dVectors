from scipy.interpolate import make_interp_spline
import numpy as np

def interpolate_curve_3d(X: list[float | int], Y: list[float | int], Z: list[float | int], num_points: int=300):
    """
    Создает гладкую 3D-кривую с помощью сплайна по точкам (X, Y, Z)
    :param X: Массив значений по оси X
    :param Y: Массив значений по оси Y
    :param Z: Массив значений по оси Z
    :param num_points: Количество точек для интерполяции (по умолчанию 300)
    :return: Кортеж (X_smooth, Y_smooth, Z_smooth) — координаты гладкой кривой
    """
    if len(X) < 4:
        return X, Y, Z

    t = np.linspace(0, 1, len(X))
    t_new = np.linspace(0, 1, num_points)

    spl_x = make_interp_spline(t, X, k=3)
    spl_y = make_interp_spline(t, Y, k=3)
    spl_z = make_interp_spline(t, Z, k=3)

    X_smooth = spl_x(t_new)
    Y_smooth = spl_y(t_new)
    Z_smooth = spl_z(t_new)

    return X_smooth, Y_smooth, Z_smooth