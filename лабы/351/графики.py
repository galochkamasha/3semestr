import matplotlib.pyplot as plt
import numpy as np

Ip_mA = np.array([4.93, 3.04, 1.50])
Te_eV = np.array([2.1, 2.8, 3.8])
ne_SI = np.array([2.92e18, 1.35e18, 4.96e17])

# Настройки шрифта для красивых подписей
plt.rcParams.update({'font.size': 12})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# График Te(Ip)
ax1.plot(Ip_mA, Te_eV, 'o-', color='tab:red', linewidth=2, markersize=8)
ax1.set_xlabel('Ток разряда $I_p$, мА')
ax1.set_ylabel('Температура $T_e$, эВ')
ax1.set_title('Зависимость $T_e$ от тока разряда')
ax1.grid(True, linestyle='--', alpha=0.7)

# График ne(Ip)
ax2.plot(Ip_mA, ne_SI, 's-', color='tab:blue', linewidth=2, markersize=8)
ax2.set_xlabel('Ток разряда $I_p$, мА')
ax2.set_ylabel('Концентрация $n_e$, м$^{-3}$')
ax2.set_title('Зависимость $n_e$ от тока разряда')
ax2.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig('graphics_Te_ne_pretty.png', dpi=300)
plt.show()