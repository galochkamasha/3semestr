import numpy as np
import matplotlib.pyplot as plt

# ---------- Данные ----------
nu3 = np.array([22.5, 31.5, 40.5, 49.5, 58.5, 67.5, 76.5, 85.5, 94.5, 103.5, 112.5])
U3  = np.array([0.149, 0.206, 0.259, 0.309, 0.355, 0.398, 0.436, 0.471, 0.502, 0.530, 0.555])
I3  = np.array([479.7, 476.9, 472.6, 467.4, 461.6, 455.4, 449.0, 442.6, 436.3, 430.2, 424.3]) * 1e-3
xi3 = U3 / (nu3 * I3)

nu4  = np.array([113.0, 135.5, 158.0, 180.5, 203.0, 293.0, 383.0, 473.0,
                 563.0, 653.0, 743.0, 833.0, 923.0, 1013.0, 1103.0])
psi4 = np.array([0.16, 0.21, 0.25, 0.28, 0.30, 0.32, 0.32, 0.39,
                 0.40, 0.46, 0.45, 0.55, 0.56, 0.50, 0.53]) * np.pi

a, h, mu0 = 0.0225, 1.5e-3, 4*np.pi*1e-7
sigma_nom, sigma_tab = 3.64e7, 5.0e7
nu_h = 1.0/(np.pi*h**2*sigma_nom*mu0)

# ---------- xi_0 ----------
x3 = nu3**2
A_mat = np.vstack([np.ones_like(x3), -x3]).T
xi0, _ = np.linalg.lstsq(A_mat, xi3, rcond=None)[0]
ratio_exp = xi3 / xi0

# ---------- Теория ----------
def H1_over_H0(nu, sigma):
    omega = 2*np.pi*nu
    delta = np.sqrt(2.0/(omega*sigma*mu0))
    alpha = (1+1j)/delta
    return np.abs(1.0/(np.cosh(alpha*h) + 0.5*alpha*a*np.sinh(alpha*h)))

def psi_theory(nu, sigma):
    omega = 2*np.pi*nu
    delta = np.sqrt(2.0/(omega*sigma*mu0))
    alpha = (1+1j)/delta
    return -np.angle(1.0/(np.cosh(alpha*h) + 0.5*alpha*a*np.sinh(alpha*h)))

# ============================================================
# ГРАФИК 1 — эксперимент + одна теоретическая кривая
# ============================================================
nu_th1 = np.logspace(np.log10(15), np.log10(200), 300)

fig, ax = plt.subplots(figsize=(8, 5.5))
ax.plot(nu_th1, H1_over_H0(nu_th1, sigma_nom), '-', lw=2, color='tab:red',
        label=r'теория, $\sigma=3{,}64\cdot10^7$ См/м')
ax.plot(nu3, ratio_exp, 'o', ms=8, color='tab:blue',
        label='эксперимент ')
ax.set_xlabel(r'$\nu$, Гц', fontsize=12)
ax.set_ylabel(r'$|H_1|/|H_0|$', fontsize=12)
ax.set_xlim(15, 130)
ax.set_ylim(0.82, 1.01)
ax.legend(fontsize=11, loc='lower left')
ax.grid(False)
for spine in ax.spines.values():
    spine.set_linewidth(0.8)
plt.tight_layout()
plt.savefig('H_ratio.png', dpi=150)
plt.show()

# ============================================================
# ГРАФИК 2 — чистая теория в широком диапазоне
# ============================================================
nu_th = np.logspace(1, 6, 800)   # <-- ВОТ ЭТА СТРОКА БЫЛА ПРОПУЩЕНА

fig, ax = plt.subplots(figsize=(9, 5.5))
for sig, lab, col in [(3.64e7, r'$\sigma=3.64\cdot10^7$', 'tab:red'),
                      (5.0e7,  r'$\sigma=5\cdot10^7$ (табл.)', 'tab:blue'),
                      (1.0e7,  r'$\sigma=10^7$', 'tab:green')]:
    ax.loglog(nu_th, H1_over_H0(nu_th, sig), lw=2, label=lab, color=col)
ax.axvline(nu_h, color='gray', ls=':', label=r'$\nu_h$')
ax.set_xlabel(r'$\nu$, Гц', fontsize=12)
ax.set_ylabel(r'$|H_1|/|H_0|$', fontsize=12)
ax.grid(True, which='both', alpha=0.3)
ax.legend(fontsize=10)
ax.set_title(r'Теоретическая зависимость $|H_1|/|H_0|(\nu)$', fontsize=12)
plt.tight_layout()
plt.savefig('H_ratio_theory.png', dpi=150)
plt.show()

# ============================================================
# ГРАФИК 3 — psi(nu), обрезаем по данным (~до 1.5 кГц)
# ============================================================
nu_th3 = np.logspace(np.log10(100), np.log10(1500), 400)
nu_asym = np.logspace(np.log10(0.5*nu_h), np.log10(1500), 200)
psi_asym = np.pi/4 + h*np.sqrt(2*np.pi*nu_asym*sigma_nom*mu0/2)

fig, ax = plt.subplots(figsize=(8, 5.5))
ax.plot(nu_th3, psi_theory(nu_th3, sigma_nom)/np.pi, '-', lw=2,
        color='tab:red', label=r'теория, $\sigma=3{,}64\cdot10^7$ См/м')
ax.plot(nu_asym, psi_asym/np.pi, ':', lw=1.8, color='tab:orange',
        label=r'асимптотика')
ax.plot(nu4, psi4/np.pi, 'o', ms=8, color='tab:blue',
        label='эксперимент ')
ax.set_xscale('log')
ax.set_xlabel(r'$\nu$, Гц', fontsize=12)
ax.set_ylabel(r'$\psi/\pi$', fontsize=12)
ax.set_xlim(100, 1500)
ax.set_ylim(0.1, 0.6)
ax.legend(fontsize=11, loc='upper left')
ax.grid(False)
for spine in ax.spines.values():
    spine.set_linewidth(0.8)
plt.tight_layout()
plt.savefig('phase_theory.png', dpi=150)
plt.show()

print("Готово: H_ratio.png, H_ratio_theory.png, phase_theory.png")
print(f"nu_h = {nu_h:.1f} Гц,  xi_0 = {xi0:.4f}")