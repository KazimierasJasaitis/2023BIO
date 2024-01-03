import numpy as np
import matplotlib.pyplot as plt

def reaction_rates(t, y):
    A, B, C, D = y
    dAdt = -k1 * A
    dBdt = k1 * A
    dCdt = k1 * A - k2 * C
    dDdt = k1 * A + k2 * C
    return np.array([dAdt, dBdt, dCdt, dDdt])

def rk4_step(xn, yn, dx, function):
    k1 = dx * function(xn, yn)
    k2 = dx * function(xn + 0.5*dx, yn + 0.5*k1)
    k3 = dx * function(xn + 0.5*dx, yn + 0.5*k2)
    k4 = dx * function(xn + dx, yn + k3)
    yn1 = yn + (k1 + 2*k2 + 2*k3 + k4) / 6.0
    xn1 = xn + dx
    return xn1, yn1

# Reakcijų greičiai [0,2]
k1 = 1.5
k2 = 1.0

# Pradinės sąlygos (koncentracijos)
A0 = 1.0
B0 = 0.0
C0 = 0.0
D0 = 0.0
y0 = np.array([A0, B0, C0, D0])

a = 0
b = 5
N = 100
dx = (b - a) / N
t = np.linspace(a, b, N)
results = []

y = y0
for tn in t[:-1]:
    results.append(y)
    tn1, y = rk4_step(tn, y, dx, reaction_rates)
results.append(y)

results = np.array(results)

plt.plot(t, results[:, 0], label='A(t)')
plt.plot(t, results[:, 1], label='B(t)')
plt.plot(t, results[:, 2], label='C(t)')
plt.plot(t, results[:, 3], label='D(t)')
plt.xlabel('t')
plt.ylabel('Koncentracija')
plt.title('Koncentracijų kitimo grafikas')
plt.legend()
plt.show()