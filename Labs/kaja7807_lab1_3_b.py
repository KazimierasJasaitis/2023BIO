import numpy as np
import matplotlib.pyplot as plt

def quadratic_function(t, a, b, c):
    return a*t**2 + b*t + c

def calculate_err(y_true, y_pred):
    return ((y_true - y_pred) ** 2).mean()

T = 1
N = 100
h = 1/N
time_points = np.arange(0, T+h, h)
sigma = 0.2
best_a, best_b, best_c = 0, 0, 0
lowest_error = np.inf
best_y_pred = None


true_a, true_b, true_c = np.random.uniform(-1, 1, 3).round(2)

y_true = quadratic_function(time_points, true_a, true_b, true_c)
y_noisy = y_true + np.random.normal(0, sigma, len(time_points))

param_step = 0.25

for a in np.arange(-1, 1+param_step, param_step):
    for b in np.arange(-1, 1+param_step, param_step):
        for c in np.arange(-1, 1+param_step, param_step):
            y_pred = quadratic_function(time_points, a, b, c)
            error = calculate_err(y_noisy, y_pred)
            if error < lowest_error:
                best_a, best_b, best_c = a, b, c
                lowest_error = error
                best_y_pred = y_pred 


print(f"True: a={true_a}, b={true_b}, c={true_c}")
print(f"Found: a={best_a}, b={best_b}, c={best_c}")
print(f"Difference: a={abs(best_a-true_a)}, b={abs(best_a-true_a)}, c={abs(best_a-true_a)}")

print(f"Mažiausias error: {lowest_error}")


plt.scatter(time_points, y_noisy, label='Duomenys', color='blue', s=10)
plt.plot(time_points, best_y_pred, label='Labiausiai tinkanti', color='red', lw=2)
plt.plot(time_points, y_true, label='Tikroji', color='grey', lw=2)
plt.xlabel('T')
plt.ylabel('x(t)')
plt.title('Pokytis per laiką')
plt.legend()
plt.show()



