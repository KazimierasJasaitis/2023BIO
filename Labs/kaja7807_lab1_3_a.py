import random
import matplotlib.pyplot as plt
import numpy as np

def generate_data(n, func, xmin=0, xmax=3,filename="data.txt"):
    with open(filename, 'w') as file:
        for _ in range(n):
            x = random.uniform(xmin, xmax)
            y = func(x)
            file.write(f"{x}, {y}\n")

generate_data(20,lambda x: np.cos(3*x))


def read_data(n, filename="data.txt"):
    X_values = []
    Y_values = []
    with open(filename, 'r') as file:
        for i, line in enumerate(file):
            if i >= n:
                break
            parts = line.split(',')
            if len(parts) == 2:
                x, y = parts
                X_values.append(float(x.strip()))
                Y_values.append(float(y.strip()))

    return X_values, Y_values

def lagranzas3(X, Y, x):    
    result = 0
    n = len(X)
    for i in range(n):
        term = Y[i]
        for j in range(n):
            if i != j:
                term *= (x - X[j]) / (X[i] - X[j])
        result += term
    return result

(X, Y) = read_data(20)
new_X_values = np.linspace(min(X), max(X), len(X)**2)
interpolated_Y = []

for x in new_X_values:
    distances = np.abs(np.array(X) - x)
    nearest_indices = np.argsort(distances)[:4]
    nearest_X = [X[i] for i in nearest_indices]
    nearest_Y = [Y[i] for i in nearest_indices]

    sorted_indices = np.argsort(nearest_X)
    nearest_X_sorted = [nearest_X[i] for i in sorted_indices]
    nearest_Y_sorted = [nearest_Y[i] for i in sorted_indices]

    interpolated_Y.append(lagranzas3(nearest_X_sorted, nearest_Y_sorted, x))

plt.plot(new_X_values, interpolated_Y, 'b-', label='Interpoliuoti')
plt.plot(X, Y, 'ro', label='Pradiniai')
plt.legend()
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Originalūs taškai ant interpoliacijos funkcijos grafiko')
plt.grid(True)
plt.show()