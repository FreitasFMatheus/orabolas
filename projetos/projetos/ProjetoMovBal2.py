import math

# Dados iniciais
v0 = 18.9  # m/s
alpha0 = math.radians(21.1)  # graus para radianos
g = 9.81  # m/s^2

# a) Tempo até que a bola retorne ao mesmo nível
# A altura como função do tempo h(t) = v0y*t - 0.5*g*t^2 e queremos encontrar o tempo para h(t) = 0.
v0y = v0 * math.sin(alpha0)  # Componente y da velocidade inicial
t_total = 2 * v0y / g  # Tempo total de voo

# b) Distância horizontal percorrida durante esse tempo
v0x = v0 * math.cos(alpha0)  # Componente x da velocidade inicial
x_total = v0x * t_total

# c) Altura máxima
# A altura máxima é alcançada quando vy = 0
t_max_height = v0y / g  # Tempo para alcançar altura máxima
h_max = v0y*t_max_height - 0.5*g*t_max_height**2  # Altura máxima

# Formatando as respostas
t_total = format(t_total, ".3g")
x_total = format(x_total, ".3g")
h_max = format(h_max, ".3g")

# Exibindo os resultados
print(f"a) Tempo até retornar ao nível inicial: {t_total} s")
print(f"b) Distância horizontal percorrida: {x_total} m")
print(f"c) Altura máxima alcançada: {h_max} m")
