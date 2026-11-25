import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# --- Данные для пункта 8 ---
tau_us = np.array([50, 100, 150, 200])          # мкс
inv_tau_kHz = 1000 / tau_us                     # 1/τ, кГц
delta_nu_exp = np.array([20.0, 9.95, 6.7, 5.0]) # кГц

# --- Данные для пункта 9 ---
T_ms = np.array([1.0, 2.0, 3.0, 4.0, 5.0])      # мс
inv_T_kHz = 1.0 / T_ms                          # 1/T, кГц
delta_nu_between = np.array([0.995, 0.472, 0.323, 0.248, 0.196]) # кГц

# --- Линейная регрессия (МНК) ---
# Для пункта 8: Δν = k * (1/τ) + b
res8 = linregress(inv_tau_kHz, delta_nu_exp)
# Для пункта 9: δν = k * (1/T) + b
res9 = linregress(inv_T_kHz, delta_nu_between)

print("=== Результаты МНК ===")
print(f"П.8 (Δν от 1/τ): наклон k = {res8.slope:.4f}, свободный член b = {res8.intercept:.4f}, R^2 = {res8.rvalue**2:.4f}")
print(f"П.9 (δν от 1/T): наклон k = {res9.slope:.4f}, свободный член b = {res9.intercept:.4f}, R^2 = {res9.rvalue**2:.4f}")

# --- Построение графиков ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# График 1: Δν(1/τ)
ax1.scatter(inv_tau_kHz, delta_nu_exp, color='blue', label='Эксперимент', zorder=5)
x_fit1 = np.linspace(0, 22, 100)
ax1.plot(x_fit1, res8.slope * x_fit1 + res8.intercept, 'r-', label='Линейная аппроксимация')
ax1.plot(x_fit1, x_fit1, 'k--', alpha=0.5, label='Теория: $\\Delta\\nu = 1/\\tau$')
ax1.set_xlabel('$1/\\tau$, кГц')
ax1.set_ylabel('$\\Delta\\nu$, кГц')
ax1.set_title('Зависимость $\\Delta\\nu(1/\\tau)$')
ax1.grid(True, linestyle=':', alpha=0.7)
ax1.legend()
ax1.set_xlim(0, 22)
ax1.set_ylim(0, 22)

# График 2: δν(1/T)
ax2.scatter(inv_T_kHz, delta_nu_between, color='blue', marker='s', label='Эксперимент', zorder=5)
x_fit2 = np.linspace(0, 1.1, 100)
ax2.plot(x_fit2, res9.slope * x_fit2 + res9.intercept, 'r-', label='Линейная аппроксимация')
ax2.plot(x_fit2, x_fit2, 'k--', alpha=0.5, label='Теория: $\\delta\\nu = 1/T$')
ax2.set_xlabel('$1/T$, кГц')
ax2.set_ylabel('$\\delta\\nu$, кГц')
ax2.set_title('Зависимость $\\delta\\nu(1/T)$')
ax2.grid(True, linestyle=':', alpha=0.7)
ax2.legend()
ax2.set_xlim(0, 1.1)
ax2.set_ylim(0, 1.1)

plt.tight_layout()
plt.savefig('uncertainty_plots.png', dpi=300) # Сохраняем в файл
plt.show()