from datetime import datetime
import pandas as pd
import numpy as np
import cx_oracle

import numpy as np

# Crear un arreglo NumPy unidimensional
arr1d = np.array([1, 2, 3, 4, 5])
print("Arreglo unidimensional:")
print(arr1d)

# Crear un arreglo NumPy bidimensional (matriz)
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("\nArreglo bidimensional (matriz):")
print(arr2d)

# Operaciones básicas con arreglos NumPy
print("\nOperaciones básicas con arreglos NumPy:")
print("Suma:", arr1d + 2)
print("Resta:", arr1d - 2)
print("Multiplicación:", arr1d * 2)
print("División:", arr1d / 2)

# Funciones matemáticas de NumPy
print("\nFunciones matemáticas de NumPy:")
print("Seno:", np.sin(arr1d))
print("Coseno:", np.cos(arr1d))
print("Exponencial:", np.exp(arr1d))

# Indexación y rebanado de arreglos NumPy
print("\nIndexación y rebanado de arreglos NumPy:")
print("Elemento en la posición 2:", arr1d[2])
print("Segunda fila, segunda columna:", arr2d[1, 1])
print("Primer fila:", arr2d[0, :])
print("Segunda columna:", arr2d[:, 1])

# Generar arreglos NumPy automáticamente
print("\nGenerar arreglos NumPy automáticamente:")
arr_zeros = np.zeros((2, 3))  # Matriz de ceros de 2x3
arr_ones = np.ones((3, 2))    # Matriz de unos de 3x2
arr_range = np.arange(0, 10, 2)  # Secuencia de 0 a 10 con paso de 2
arr_linspace = np.linspace(0, 1, 5)  # 5 valores igualmente espaciados entre 0 y 1

print("Matriz de ceros:")
print(arr_zeros)
print("Matriz de unos:")
print(arr_ones)
print("Secuencia arange:")
print(arr_range)
print("Secuencia linspace:")
print(arr_linspace)
