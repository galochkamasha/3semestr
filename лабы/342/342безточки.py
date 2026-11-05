import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# --- Исходные данные ---
T_bath = np.array([14.12, 16.00, 18.02, 20.03, 22.00, 24.00, 26.01, 28.00, 30.00, 32.00, 34.00, 36.00, 38.00, 40.00])
tau = np.array([10.780, 10.718, 10.544, 10.218, 9.922, 9.600, 9.426, 9.358, 9.3036, 9.272, 9.243, 9.226, 9.211, 9.199])
U = np.array([-0.001, -0.009, -0.006, -0.0027, -0.006, -0.0088, -0.003, -0.0088, -0.078, -0.0083, -0.0059, -0.0078, -0.0076, -0.0089])

tau0 = 9.045  # мкс
k_thermo = 24.0  # град/мВ

# Температура образца
T_sample = T_bath + U * k_thermo

# Значения для графика
y_vals = 1.0 / (tau**2 - tau0**2)

# --- ИСКЛЮЧАЕМ ТОЧКУ ПРИ 30 ГРАДУСАХ (индекс 8) ---
# Создаем массив индексов, оставляя все, кроме 8-го
indices_to_keep = np.arange(len(T_sample)) != 8

T_sample_filtered = T_sample[indices_to_keep]
y_vals_filtered = y_vals[indices_to_keep]

# --- Аппроксимация (линейный участок, начиная с 24°C) ---
# Индекс 24°C в исходном массиве был 5. 
# В новом массиве (без 8-го элемента) он останется под индексом 5, 
# так как 30-й градус идет после 24-го.
start_idx = 5 
res = linregress(T_sample_filtered[start_idx:], y_vals_filtered[start_idx:])
slope, intercept, r_value, p_value, std_err = res

# Строим график
plt.figure(figsize=(10, 6))

# Рисуем "хорошие" точки
plt.plot(T_sample_filtered, y_vals_filtered, 'o', color='blue', label='Экспериментальные точки')

# Рисуем выброшенную точку красным крестиком, чтобы было видно, что мы её убрали


# Аппроксимация
x_fit = np.linspace(18, 42, 100)
y_fit = slope * x_fit + intercept
plt.plot(x_fit, y_fit, 'r--', label=f'Линейная аппроксимация\n(наклон {slope:.2e})')

# Новая точка Кюри
theta_p_new = -intercept / slope

plt.axvline(x=theta_p_new, color='g', linestyle=':', label=f'Новая точка Кюри: {theta_p_new:.2f} °C')
plt.axhline(y=0, color='k', linewidth=0.8)

plt.xlabel('Температура образца T, °C')
plt.ylabel('1 / (τ² - τ₀²), мкс⁻²')
plt.title('Закон Кюри-Вейсса для гадолиния (без выброса)')
plt.legend()
plt.grid(True)
plt.show()

# Вывод новых параметров
print(f"--- НОВЫЕ РЕЗУЛЬТАТЫ ---")
print(f"Уравнение прямой: y = {slope:.4e} * T + {intercept:.4e}")
print(f"Парамагнитная точка Кюри (Theta_p): {theta_p_new:.2f} °C")
print(f"Коэффициент детерминации R^2: {r_value**2:.5f}")