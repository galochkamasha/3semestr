import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

plt.rcParams.update({
    'font.size': 12,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'figure.figsize': (10, 8),
})

# ============ ПАРАМЕТРЫ ============
N_t0 = 1750
N_t1 = 300
D    = 0.10

kH = N_t0 / (np.pi * D)
print(f"kH = {kH:.2f} А/(м·А)")

# ============ ПОГРЕШНОСТИ ============
dx_err  = 0.2
dI_err  = 0.0001

# ============ ПЕТЛЯ ============
I1  = np.array([1725.00, 939.70, 584.10, 487.10, 397.54, 354.68,
                323.95, 283.46, 245.10, 186.10, 109.81, 1.28])
dx1_arr = np.array([0, 14.3, 10.8, 3.5, 3.1, 1.6, 1.1, 1.4, 1.2, 1.8, 2.2, 2.6])

I2  = np.array([1.28, 109.73, 185.94, 244.99, 282.62, 323.64,
                354.27, 397.08, 485.03, 583.00, 938.60, 1722.60])
dx2_arr = np.array([0, 6.2, 11.5, 16.6, 14.7, 16.9, 10.3, 12.0, 16.2, 9.9, 18.0, 15.5])

I3  = np.array([1726.00, 940.00, 584.20, 487.10, 397.55, 354.72,
                323.99, 283.24, 245.45, 186.12, 109.81, 1.41])
dx3_arr = np.array([0, -13.6, -10.3, -3.4, -3.2, -1.5, -1.1, -1.4, -1.2, -1.8, -2.3, -2.6])

I4  = np.array([0.00, 109.75, 185.97, 245.12, 283.17, 323.74,
                354.33, 397.16, 485.10, 583.30, 938.40, 1723.40])
dx4_arr = np.array([0, -5.9, -10.9, -15.3, -13.6, -15.3, -9.9, -11.2, -14.8, -9.3, -16.4, -14.4])

H1 = +kH * I1 * 1e-3
H2 = -kH * I2 * 1e-3
H3 = -kH * I3 * 1e-3
H4 = +kH * I4 * 1e-3

def accumulate(dx, B0):
    B = np.zeros(len(dx))
    B[0] = B0
    for i in range(1, len(dx)):
        B[i] = B[i-1] - dx[i]
    return B

B1t = accumulate(dx1_arr, 0.0)
B2t = accumulate(dx2_arr, B1t[-1])
B3t = accumulate(dx3_arr, B2t[-1])
B4t = accumulate(dx4_arr, B3t[-1])

B_all_tmp = np.concatenate([B1t, B2t, B3t, B4t])
B_max = B_all_tmp.max()
B_min = B_all_tmp.min()
shift = -(B_max + B_min) / 2

B1 = B1t + shift
B2 = B2t + shift
B3 = B3t + shift
B4 = B4t + shift
Bs = (B_max - B_min) / 2

print(f"\n=== Диагностика петли ===")
print(f"Сумма Δx, 1-й проход: {dx1_arr.sum():+.2f} см")
print(f"Сумма Δx, 2-й проход: {dx2_arr.sum():+.2f} см")
print(f"Сумма Δx, 3-й проход: {dx3_arr.sum():+.2f} см")
print(f"Сумма Δx, 4-й проход: {dx4_arr.sum():+.2f} см")
print(f"Bs* = {Bs:.2f} см (полуразмах)")

# ============ НАЧАЛЬНАЯ КРИВАЯ ============
I_init = np.array([0, 109.60, 185.67, 247.40, 281.98, 323.24,
                   353.82, 420.00, 484.58, 582.60, 937.30, 1721.40])
dx_init = np.array([0, -1.7, -1.6, -2.2, -1.8, -1.9,
                    -1.2, -1.4, -2.0, -2.2, -4.6, -4.0])

H_init = +kH * I_init * 1e-3
B_init_raw = np.cumsum(np.abs(dx_init))
k_init = 3.8
B_init = B_init_raw * k_init
Berr_init = np.sqrt(np.arange(len(dx_init)) * dx_err**2) * k_init

print(f"\n=== Начальная кривая (приведена, k = {k_init}) ===")
print(f"H: {H_init}")
print(f"B* (приведено): {B_init}")

# ============ ПОГРЕШНОСТИ ПЕТЛИ ============
def accum_err(n, Berr0=0.0):
    return np.sqrt(np.arange(n) * dx_err**2 + Berr0**2)

Berr1 = accum_err(len(dx1_arr))
Berr2 = accum_err(len(dx2_arr), Berr1[-1])
Berr3 = accum_err(len(dx3_arr), Berr2[-1])
Berr4 = accum_err(len(dx4_arr), Berr3[-1])

# ============ ГРАФИК ============
fig, ax = plt.subplots(figsize=(10, 8))

ax.errorbar(H1, B1, xerr=dI_err*1e3*kH, yerr=Berr1,
            fmt='o-', color='tab:red', ms=5, lw=1.4, capsize=2,
            label='1-й проход')
ax.errorbar(H2, B2, xerr=dI_err*1e3*kH, yerr=Berr2,
            fmt='s-', color='tab:blue', ms=5, lw=1.4, capsize=2,
            label='2-й проход')
ax.errorbar(H3, B3, xerr=dI_err*1e3*kH, yerr=Berr3,
            fmt='^-', color='tab:green', ms=5, lw=1.4, capsize=2,
            label='3-й проход')
ax.errorbar(H4, B4, xerr=dI_err*1e3*kH, yerr=Berr4,
            fmt='v-', color='tab:orange', ms=5, lw=1.4, capsize=2,
            label='4-й проход')

ax.errorbar(H_init, B_init, xerr=dI_err*1e3*kH, yerr=Berr_init,
            fmt='D-', color='black', ms=5, lw=1.4, capsize=2,
            label='Начальная кривая (приведена)')

ax.axhline(0, color='k', lw=0.5)
ax.axvline(0, color='k', lw=0.5)
ax.set_xlabel('H, А/м')
ax.set_ylabel(r'$B^*$, условные единицы (см)')
ax.set_title('Петля гистерезиса и начальная кривая')
ax.legend(loc='best')
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())
plt.tight_layout()
plt.savefig('hysteresis.png', dpi=150)
plt.show()

# ============ ХАРАКТЕРНЫЕ ТОЧКИ ============
H_all = np.concatenate([H1, H2, H3, H4])
B_all = np.concatenate([B1, B2, B3, B4])

def interp_zero_H(H, B):
    res = []
    for i in range(len(H)-1):
        if H[i]*H[i+1] < 0:
            t = -H[i]/(H[i+1]-H[i])
            res.append(B[i] + t*(B[i+1]-B[i]))
    return np.array(res)

def interp_zero_B(H, B):
    res = []
    for i in range(len(B)-1):
        if B[i]*B[i+1] < 0:
            t = -B[i]/(B[i+1]-B[i])
            res.append(H[i] + t*(H[i+1]-H[i]))
    return np.array(res)

Br_vals = interp_zero_H(H_all, B_all)
Br = np.mean(np.abs(Br_vals))
Hc_vals = interp_zero_B(H_all, B_all)
Hc = np.mean(np.abs(Hc_vals))

print(f"\n=== Характерные точки ===")
print(f"Br* = {Br:.2f} см")
print(f"Hc = {Hc:.1f} А/м")

dBdH_init = np.gradient(B_init, H_init)
mu_max = np.max(np.abs(dBdH_init))
print(f"μ_диф* (по начальной кривой) = {mu_max:.4f} см/(А/м)")

# ============ ОЦЕНКА ПРИ d_t = 1.5 см ============
mu0 = 4 * np.pi * 1e-7
N_c0, N_c1, l_c, d_c = 940, 500, 0.80, 0.07
dI1, dx1c = 1.2757, 3.4
kB_coef = mu0 * (N_c0*N_c1)/(N_t1*l_c) * dI1 / dx1c
kB_15 = kB_coef * (d_c/0.015)**2
print(f"\n=== Оценка при d_t = 1.5 см ===")
print(f"kB = {kB_15:.5f} Тл/см")
print(f"Bs ≈ {Bs * kB_15:.2f} Тл")
print(f"Br ≈ {Br * kB_15:.2f} Тл")
print(f"μ_диф ≈ {mu_max * kB_15 / mu0:.0f}")