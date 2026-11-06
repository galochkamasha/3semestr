import numpy as np
import matplotlib.pyplot as plt

# ---------- Данные ----------
nu_all = np.array([150, 200, 250, 300, 400, 500, 600, 800, 1500,
                   12000, 15000, 20000, 25000], dtype=float)
L_all  = np.array([7.2100, 6.1260, 5.3320, 4.7670, 4.0680, 3.6830,
                   3.4530, 3.2100, 2.9650, 3.0530, 3.2300, 3.7200,
                   4.7790])

L_min = 2.9650   # L при 1500 Гц
L_max = 7.2100   # L при 150 Гц (оценка снизу)

# ========== РИСУНОК 1: L(nu) ==========
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(nu_all, L_all, 'o-', ms=7, label='эксперимент')
ax.set_xscale('log')
ax.set_xlabel(r'$\nu$, Гц')
ax.set_ylabel(r'$L$, мГн')
ax.grid(True, which='both', alpha=0.3)
ax.legend()
plt.tight_layout()
plt.savefig('L_nu.png', dpi=150)
plt.show()

# ========== ФИТ для п.10 ==========
mask = (nu_all > 150) & (nu_all < 1500)   # 200..800 Гц
nu_f = nu_all[mask]
L_f  = L_all[mask]

y = (L_max - L_f) / (L_f - L_min)
x = nu_f**2

k = np.sum(x*y) / np.sum(x**2)
resid = y - k*x
s2 = np.sum(resid**2) / (len(x)-1)
k_err = np.sqrt(s2 / np.sum(x**2))

# sigma
a   = 0.0225
h   = 1.5e-3
mu0 = 4*np.pi*1e-7
sigma     = np.sqrt(k)     / (np.pi*a*h*mu0)
sigma_err = 0.5 * sigma * k_err/k

print("========== Пункт 10 ==========")
print(f"L_min = {L_min:.4f} мГн")
print(f"L_max = {L_max:.4f} мГн")
print(f"k     = ({k:.3e} ± {k_err:.1e}) Гц^-2")
print(f"sigma = ({sigma:.3e} ± {sigma_err:.1e}) См/м")
print("\nТаблица расчётных величин:")
print("nu, Гц | L, мГн | y        | x, Гц^2")
for a_, b_, c_, d_ in zip(nu_f, L_f, y, x):
    print(f"{a_:6.0f} | {b_:7.4f} | {c_:8.4f} | {d_:.3e}")

# ========== РИСУНОК 2: (Lmax-L)/(L-Lmin) от nu^2 ==========
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y, 'o', ms=9, label='данные')
xx = np.linspace(0, x.max()*1.05, 200)
ax.plot(xx, k*xx, 'r-', lw=2,
        label=f'$y = k\\nu^2$,  $k={k:.2e}$ Гц$^{{-2}}$')
ax.set_xlabel(r'$\nu^2$, Гц$^2$')
ax.set_ylabel(r'$(L_{max}-L)/(L-L_{min})$')
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig('L_fit_lin.png', dpi=150)
plt.show()