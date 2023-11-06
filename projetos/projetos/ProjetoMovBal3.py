import math

# Dados fornecidos
v0_kmh = 95  # Velocidade inicial em km/h
v0 = v0_kmh * 1000 / 3600  # Convertendo para m/s
alpha0 = 15.7  # Ângulo inicial em graus
h0_cm = 43  # Altura inicial em cm
h0 = h0_cm / 100  # Convertendo para m
g = 9.81  # Aceleração da gravidade em m/s^2

# Componentes da velocidade inicial
v0x = v0 * math.cos(math.radians(alpha0))  
v0y = v0 * math.sin(math.radians(alpha0))  

# Funções úteis
def get_xy_positions(t, v0x, v0y, h0):
    x = v0x * t
    y = h0 + v0y * t - 0.5 * g * t**2
    return x, y

def get_velocities(t, v0x, v0y):
    vx = v0x  
    vy = v0y - g * t
    v = math.sqrt(vx**2 + vy**2)
    return vx, vy, v

# Respostas
# a) Componentes da velocidade inicial
print(f"a) v0x = {v0x:.3f} m/s, v0y = {v0y:.3f} m/s")

# b) Tempo que a bola permanece no ar
t_flight = (v0y + math.sqrt(v0y**2 + 2*g*h0)) / g
print(f"b) Tempo de voo = {t_flight:.3f} s")

# c) Posição da bola no instante td = 0.842 s
td = 0.842
x_td, y_td = get_xy_positions(td, v0x, v0y, h0)
print(f"c) x(td) = {x_td:.3f} m, y(td) = {y_td:.3f} m")

# d) Velocidades no instante td
vx_td, vy_td, v_td = get_velocities(td, v0x, v0y)
print(f"d) vx(td) = {vx_td:.3f} m/s, vy(td) = {vy_td:.3f} m/s, |v(td)| = {v_td:.3f} m/s")

# e) Altura máxima
# A altura máxima ocorre quando vy=0. Podemos encontrar o tempo quando isso ocorre e substituir na equação de y
t_max_height = v0y / g
_, y_max = get_xy_positions(t_max_height, v0x, v0y, h0)
print(f"e) Altura máxima = {y_max:.3f} m")

# f) Alcance horizontal
# Utilizando o tempo de voo encontrado em (b)
x_range, _ = get_xy_positions(t_flight, v0x, v0y, h0)
print(f"f) Alcance = {x_range:.3f} m")

# g) Velocidade da bola imediatamente antes de alcançar o solo
vx_tf, vy_tf, v_tf = get_velocities(t_flight, v0x, v0y)
print(f"g) vx(tf) = {vx_tf:.3f} m/s, vy(tf) = {vy_tf:.3f} m/s, |v(tf)| = {v_tf:.3f} m/s")

# h) Velocidade no instante em que a bola atinge a altura máxima
vx_th, vy_th, v_th = get_velocities(t_max_height, v0x, v0y)
print(f"h) vx(th) = {vx_th:.3f} m/s, vy(th) = {vy_th:.3f} m/s, |v(th)| = {v_th:.3f} m/s")
