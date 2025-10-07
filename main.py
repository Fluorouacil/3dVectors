from plotter.VectorPlotter import VectorPlotter

# Пример данных
X = [81.8928, 42.4162, 23.2282, 14.6381, 16.4917, 14.2877]  # Энергия
Y = [0.0898, 0.0677, 0.0493, 0.0336, 0.0314, 0.033]         # Длительность
Z = [0, 1, 2, 3, 4, 5]                                     # Толщина отложений

plotter = VectorPlotter()
plotter.plot_godograph_3d(X, Y, Z, "Годограф толщины отложений")