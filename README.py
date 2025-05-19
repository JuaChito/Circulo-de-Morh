import numpy as np
import matplotlib.pyplot as plt

sigma_x = float(input("σx [MPa]: "))
sigma_y = float(input("σy [MPa]: "))
tau_xy = float(input("τxy [MPa]: "))

sigma_prom = (sigma_x + sigma_y) / 2
R = np.sqrt(((sigma_x - sigma_y) / 2) ** 2 + tau_xy ** 2)
sigma_max = sigma_prom + R
sigma_min = sigma_prom - R
theta_s_rad =(np.arctan((2 * tau_xy)/(sigma_x - sigma_y)))
theta_s_deg = np.degrees(theta_s_rad)

print("\n=== RESULTADOS ===")
print(f"Esfuerzo promedio (σ_prom): {sigma_prom:.4f} MPa")
print(f"Radio del círculo de Mohr (R): {R:.4f} MPa")
print(f"Esfuerzo máximo (σ_max): {sigma_max:.4f} MPa")
print(f"Esfuerzo mínimo (σ_min): {sigma_min:.4f} MPa")
print(f"Orientación del esfuerzo cortante máximo (2θp): {theta_s_deg:.4f}°")
print(f"\nPunto X(σx, -τxy): ({sigma_x:.4f}, {-tau_xy:.4f}) MPa")
print(f"Punto Y(σy, +τxy): ({sigma_y:.4f}, {tau_xy:.4f}) MPa")
print(f"Punto C(σ_prom, 0): ({sigma_prom:.4f}, 0.0000) MPa")

thetas = [0, 45, 90]
transformed_points = []

print("\n=== TRANSFORMACIONES DE ESFUERZOS ===")
for theta in thetas:
    rad = np.radians(theta)
    cos2 = np.cos(rad) ** 2
    sin2 = np.sin(rad) ** 2
    sin2theta = np.sin(2 * rad)
    cos2theta = np.cos(2 * rad)

    sigma_xp = sigma_x * cos2 + sigma_y * sin2 + 2 * tau_xy * np.sin(rad) * np.cos(rad)
    sigma_yp = sigma_x * sin2 + sigma_y * cos2 - 2 * tau_xy * np.sin(rad) * np.cos(rad)
    tau_xyp = (sigma_y - sigma_x) * np.sin(rad) * np.cos(rad) + tau_xy * cos2theta

    print(f"\nθ = {theta}°:")
    print(f"  σx' = {sigma_xp:.4f} MPa")
    print(f"  σy' = {sigma_yp:.4f} MPa")
    print(f"  τx'y' = {tau_xyp:.4f} MPa")
    print(f"  Punto X'(σx', τx'y')  = ({sigma_xp:.4f}, {tau_xyp:.4f}) MPa")
    print(f"  Punto Y'(σy', -τx'y') = ({sigma_yp:.4f}, {-tau_xyp:.4f}) MPa")

    transformed_points.append({
        'theta': theta,
        "sigma_x'": sigma_xp,
        "sigma_y'": sigma_yp,
        "tau_xy'": tau_xyp
    })

X = (sigma_x, -tau_xy)
Y = (sigma_y, tau_xy)
C = (sigma_prom, 0)
fig, ax = plt.subplots()
ax.set_aspect('equal')

circle = plt.Circle(C, R, fill=False, color='gray', linestyle='-', linewidth=1.5)
ax.add_artist(circle)

ax.axhline(0, color='black', linewidth=1)
ax.axvline(0, color='black', linewidth=1)

ax.plot([X[0], Y[0]], [X[1], Y[1]], 'k--', linewidth=1)

ax.plot(*X, 'ko')
ax.plot(*Y, 'ko')
ax.plot(*C, 'ko')

ax.text(X[0] + 3, X[1] - 5, 'X(σx, -τxy)', fontsize=9)
ax.text(Y[0] - 35, Y[1] + 5, 'Y(σy, +τxy)', fontsize=9)
ax.text(C[0] - 5, C[1] - 5, 'C', fontsize=9)

ax.plot([Y[0], Y[0]], [0, Y[1]], 'k:', linewidth=1)
ax.plot([X[0], X[0]], [0, X[1]], 'k:', linewidth=1)

ax.text(sigma_max + 2, 2, f'σ_max = {sigma_max:.4f}', fontsize=9)
ax.text(sigma_min - 30, 2, f'σ_min = {sigma_min:.4f}', fontsize=9)
ax.text(C[0] - 5, 5, f'σ_prom = {sigma_prom:.4f}', fontsize=9)
ax.text(C[0] + 10, -R / 2, r'$2θ_p$ = {:.4f}°'.format(theta_s_deg * 2), color='purple', fontsize=10)

colors = ['red', 'blue', 'green']
for i, pt in enumerate(transformed_points):
    x1 = pt["sigma_x'"]
    y1 = pt["tau_xy'"]
    x2 = pt["sigma_y'"]
    y2 = -pt["tau_xy'"]

    ax.plot(x1, y1, 'o', color=colors[i], label=f"X' θ={pt['theta']}°")
    ax.plot(x2, y2, 's', color=colors[i], label=f"Y' θ={pt['theta']}°")

    ax.plot([x1, x2], [y1, y2], linestyle=':', color=colors[i], linewidth=1)

ax.set_xlabel('Esfuerzo normal σ [MPa]')
ax.set_ylabel('Esfuerzo cortante τ [MPa]')
ax.set_title('Círculo de Mohr')
ax.grid(True)
ax.legend()
ax.set_xlim(sigma_prom - R * 1.8, sigma_prom + R * 1.8)
ax.set_ylim(-R * 1.5, R * 1.5)

plt.show()
