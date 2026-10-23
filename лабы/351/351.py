import numpy as np
import matplotlib.pyplot as plt

# --- Константы (СГС) ---
e_C = 1.602e-19      # Кл
e_SGSE = 4.803e-10   # ед. СГСЭ
me = 9.109e-28       # г
mi = 22 * 1.66e-24   # г (масса иона неона-22)
k = 1.38e-16         # эрг/К (постоянная Больцмана в СГС)
k_SI = 1.38e-23      # Дж/К
eV_to_K = 11604.5    # 1 эВ в Кельвинах (или 11800, как в методичке, но 11604 точнее. Возьмем 11800 из методички для соответствия)

# --- Параметры установки ---
d = 0.2e-3           # м (0.2 мм)
l = 5.2e-3           # м (5.2 мм)
S_SI = np.pi * d * l # м^2
S_SGSE = S_SI * 1e4  # см^2
P_torr = 2           # торр
T_gas = 300          # К (комнатная)

# --- Данные из эксперимента ---
# Ip (мА), I_in (мкА), Te (эВ) - берем Te из второго метода (через dU)
Ip_mA = np.array([4.93, 3.04, 1.50])
I_in_mkA = np.array([83.6, 44.8, 19.1])
Te_eV = np.array([2.1, 2.8, 3.8])

Ip_A = Ip_mA * 1e-3
I_in_A = I_in_mkA * 1e-6
Te_K = Te_eV * 11800 # Переводим эВ в К (как в методичке 1эВ ≈ 11800К)

# --- 11б. Концентрация электронов (формула Бома) ---
# I_in = 0.4 * ne * e * S * sqrt(2*k*Te / mi)
# ne = I_in / (0.4 * e * S * sqrt(2*k*Te / mi))
v_Bohm = np.sqrt(2 * k_SI * Te_K / mi) # м/с
ne_SI = I_in_A / (0.4 * e_C * S_SI * v_Bohm) # м^-3
ne_SGSE = ne_SI * 1e-6 # см^-3 (1 м^-3 = 1e-6 см^-3)

# --- 12. Плазменная частота и радиусы ---
# wp = sqrt(4 * pi * ne * e^2 / me)
wp = np.sqrt(4 * np.pi * ne_SGSE * e_SGSE**2 / me) # рад/с

# r_De = sqrt(k*Te / (4*pi*ne*e^2))
r_De = np.sqrt(k * Te_K / (4 * np.pi * ne_SGSE * e_SGSE**2)) # см

# r_D = sqrt(k*T_i / (4*pi*ne*e^2))
r_D = np.sqrt(k * T_gas / (4 * np.pi * ne_SGSE * e_SGSE**2)) # см

# --- 13. Число ионов в дебаевской сфере ---
# ND = (4/3)*pi*(r_D^3)*ne (берем r_D, так как это полный радиус экранирования)
ND = (4/3) * np.pi * (r_D**3) * ne_SGSE

# --- 14. Степень ионизации ---
# n_gas = P / (k*T_gas)
P_Pa = P_torr * 133.322
n_gas_SI = P_Pa / (k_SI * T_gas) # м^-3
alpha = ne_SI / n_gas_SI

# Вывод результатов
print("--- Результаты расчетов ---")
for i in range(len(Ip_mA)):
    print(f"Ip = {Ip_mA[i]} мА:")
    print(f"  ne = {ne_SI[i]:.2e} м^-3 ({ne_SGSE[i]:.2e} см^-3)")
    print(f"  wp = {wp[i]:.2e} рад/с")
    print(f"  r_De = {r_De[i]:.2e} см")
    print(f"  r_D = {r_D[i]:.2e} см")
    print(f"  ND = {ND[i]:.2e}")
    print(f"  alpha = {alpha[i]:.2e}")
    print("-" * 25)

# --- 15. Построение графиков ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# График Te(Ip)
ax1.plot(Ip_mA, Te_eV, 'o-', color='tab:red', label='\(T_e\)')
ax1.set_xlabel('\(I_p\), мА')
ax1.set_ylabel('\(T_e\), эВ')
ax1.set_title('Зависимость \(T_e\) от тока разряда')
ax1.grid(True)
ax1.legend()

# График ne(Ip)
ax2.plot(Ip_mA, ne_SI, 's-', color='tab:blue', label='\(n_e\)')
ax2.set_xlabel('\(I_p\), мА')
ax2.set_ylabel('\(n_e\), м\(^{-3}\)')
ax2.set_title('Зависимость \(n_e\) от тока разряда')
ax2.grid(True)
ax2.legend()

plt.tight_layout()
plt.savefig('graphics_Te_ne.png', dpi=300)
plt.show()


