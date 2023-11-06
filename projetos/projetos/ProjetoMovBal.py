import math

# Dados iniciais
v0 = 26.8
alpha0 = math.radians(69.3)
h0 = 0.74
g = 9.81

# a) Componentes da velocidade inicial
v0x = v0 * math.cos(alpha0)
v0y = v0 * math.sin(alpha0)

# b) Tempo no ar
t_top = v0y / g
t_total = 2 * t_top

# c) Posição no instante td = 2.45 s
td = 2.45
x_td = v0x * td
y_td = h0 + v0y*td - 0.5*g*td**2

# d) Velocidade no instante td = 2.45 s
vx_td = v0x
vy_td = v0y - g*td
v_td = math.sqrt(vx_td**2 + vy_td**2)

# e) Altura máxima
h_max = h0 + (v0y**2)/(2*g)

# f) Alcance horizontal
x_max = v0x * t_total

# g) Velocidade antes de alcançar o solo
vy_bottom = math.sqrt(v0y**2 + 2*g*h_max)
v_bottom = math.sqrt(v0x**2 + vy_bottom**2)

# h) Velocidade na altura máxima
vx_top = v0x
vy_top = 0
v_top = vx_top

print("a) v0x =", round(v0x, 3), "m/s, v0y =", round(v0y, 3), "m/s")
print("b) Tempo no ar =", round(t_total, 3), "s")
print("c) Posição no instante td =", round(x_td, 3), "m,", round(y_td, 3), "m")
print("d) Velocidade no instante td =", round(vx_td, 3), "m/s,", round(vy_td, 3), "m/s,", round(v_td, 3), "m/s")
print("e) Altura máxima =", round(h_max, 3), "m")
print("f) Alcance horizontal =", round(x_max, 3), "m")
print("g) Velocidade antes de alcançar o solo =", round(vx_td, 3), "m/s,", round(vy_bottom, 3), "m/s,", round(v_bottom, 3), "m/s")
print("h) Velocidade na altura máxima =", round(vx_top, 3), "m/s,", round(vy_top, 3), "m/s,", round(v_top, 3), "m/s")
