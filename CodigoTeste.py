import pygame  
import numpy as np 
import matplotlib.pyplot as plt

# Função para carregar a trajetória da bola de um arquivo
def load_bola_trajectory(file_name):
    try:
        # Lê o arquivo e substitui as vírgulas por pontos para garantir que os dados sejam interpretados corretamente
        data = np.genfromtxt(file_name, delimiter="\t", dtype=str)
        data = np.char.replace(data, ',', '.').astype(float)
        # Retorna as coordenadas x e y da bola
        return data[:,1], data[:,2]
    except Exception as e:
        # Em caso de erro, imprime a mensagem de erro e retorna None
        print(f"Erro ao ler o arquivo: {str(e)}")
        return None, None

# Função para obter a posição inicial do robô
def get_robo_initial_position():
    # Mensagem inicial para o usuário
    pos_input = input("Aperte Enter para usar a posição aleatória ou digite 1 para selecionar as coordenadas em X e Y: ")

    # Caso o usuário pressione Enter (entrada NULL), gera coordenadas aleatórias dentro do raio de 1 metro ao redor da posição inicial da bola
    if not pos_input:
        while True:
            # Gera coordenadas aleatórias dentro do retângulo de dimensões 2x2 metros ao redor da bola
            x_rand = np.random.uniform(0, 2) + 0.5  # x entre 0.5 e 2.5
            y_rand = np.random.uniform(0, 2)  # y entre 0 e 2

            # Verifica se as coordenadas estão dentro do raio de 1 metro ao redor da posição inicial da bola
            distance = np.sqrt((x_rand - 1)**2 + (y_rand - 0.5)**2)
            if distance <= 1:
                return x_rand, y_rand

    # Caso o usuário digite 1, solicita as coordenadas manualmente
    elif pos_input == '1':
        while True:
            try:
                # Solicita a coordenada X
                x_input = float(input("Coordenadas de X (0 até 51 m): "))
                # Verifica se X está no intervalo válido
                if not 0 <= x_input <= 51:
                    raise ValueError

                # Solicita a coordenada Y
                y_input = float(input("Coordenadas de Y (0 até 10.5 m): "))
                # Verifica se Y está no intervalo válido
                if not 0 <= y_input <= 10.5:
                    raise ValueError

                # Retorna as coordenadas inseridas
                return x_input, y_input

            except ValueError:
                # Mensagem de erro para entradas inválidas
                print("As coordenadas selecionadas não são válidas")

    else:
        # Caso o usuário digite algo diferente de NULL ou 1, re-solicita a entrada
        return get_robo_initial_position()

def calculate_robo_trajectory(x_bola, y_bola, x_robo, y_robo, a=2.8, delta_t=0.02):
    v_robo = 0  # velocidade inicial do robô
    x_traj, y_traj = [x_robo], [y_robo]  # listas para armazenar a trajetória do robô

    intercept_point = None
    intercept_time = None
    robo_radius = 0.15  # raio de interceptação do robô em metros

    for i in range(len(x_bola)):
        # Calcula a distância entre o robô e a bola em um ponto específico
        distance = np.sqrt((x_bola[i] - x_robo)**2 + (y_bola[i] - y_robo)**2)
        if distance <= robo_radius:
            # Se a bola está dentro do raio de interceptação, o robô deve parar
            intercept_point = (x_bola[i], y_bola[i])
            intercept_time = i * delta_t
            break

        # Calcula o tempo necessário para o robô chegar até a bola usando a fórmula quadrática
        discriminant = v_robo**2 + 2*a*(distance - robo_radius)
        if discriminant >= 0:
            time_needed = (-v_robo + np.sqrt(discriminant)) / a
            if time_needed <= i*delta_t:
                # Marca as coordenadas de colisão e o tempo
                intercept_point = (x_bola[i], y_bola[i])
                intercept_time = time_needed
                break

    if intercept_point:
        # Se o robô tem um ponto de interceptação
        # Calcula a direção que o robô deve seguir para interceptar a bola em linha reta
        direction_x = (intercept_point[0] - x_robo) / intercept_time
        direction_y = (intercept_point[1] - y_robo) / intercept_time
        # Calcula a velocidade necessária para mover-se na direção correta
        v_direction = np.sqrt(direction_x**2 + direction_y**2)
        
        for i in np.arange(0, intercept_time, delta_t):
            # Atualiza a posição do robô com limitação de velocidade máxima
            v_increment = min(a * delta_t, 2.8 - v_robo)
            v_robo += v_increment
            # Normaliza a direção para que o robô se mova na direção correta
            x_robo += (direction_x / v_direction) * v_robo * delta_t
            y_robo += (direction_y / v_direction) * v_robo * delta_t
            x_traj.append(x_robo)
            y_traj.append(y_robo)
            # Se o robô atingir a velocidade máxima, mantém essa velocidade
            if v_robo >= 2.8:
                v_robo = 2.8
        # Preenche o restante da trajetória com o ponto de interceptação
        x_traj.extend([intercept_point[0]] * (len(x_bola) - len(x_traj)))
        y_traj.extend([intercept_point[1]] * (len(y_bola) - len(y_traj)))
    else:
        # Se não houver um ponto de interceptação, continue atualizando a trajetória normalmente
        for i in range(len(x_bola) - len(x_traj)):
            x_robo += v_robo * delta_t + 0.5 * a * delta_t**2
            y_robo += v_robo * delta_t + 0.5 * a * delta_t**2  # assumindo a mesma aceleração em y
            v_robo += a * delta_t  # atualiza a velocidade usando v = u + at
            x_traj.append(x_robo)
            y_traj.append(y_robo)

    return np.array(x_traj), np.array(y_traj), intercept_time, intercept_point

def calculate_velocity(positions, delta_t):
    # Usar diferenças finitas para calcular a velocidade
    velocities = np.zeros(len(positions))
    velocities[0] = (positions[1] - positions[0]) / delta_t  # Diferença para frente no início
    velocities[-1] = (positions[-1] - positions[-2]) / delta_t  # Diferença para trás no final

    # Diferença central para os pontos intermediários
    for i in range(1, len(positions) - 1):
        velocities[i] = (positions[i + 1] - positions[i - 1]) / (2 * delta_t)
    
    return velocities

def calculate_acceleration(velocities, delta_t):
    # Usar diferenças finitas para calcular a aceleração
    accelerations = np.zeros(len(velocities))
    accelerations[0] = (velocities[1] - velocities[0]) / delta_t  # Diferença para frente no início
    accelerations[-1] = (velocities[-1] - velocities[-2]) / delta_t  # Diferença para trás no final

    # Diferença central para os pontos intermediários
    for i in range(1, len(velocities) - 1):
        accelerations[i] = (velocities[i + 1] - velocities[i - 1]) / (2 * delta_t)

    return accelerations


def calculate_distances(x_traj, y_traj, x_bola, y_bola):
    # Calcula a distância entre o robô e a bola em cada ponto da trajetória
    distances = np.sqrt((x_traj - x_bola)**2 + (y_traj - y_bola)**2)
    return distances


def plot_trajectory(x_bola, y_bola, x_traj, y_traj):
    # Plota a trajetória da bola e do robô
    plt.figure()
    plt.plot(x_bola, y_bola, label='Trajetória da Bola')
    plt.plot(x_traj, y_traj, label='Trajetória do Robô')
    plt.legend()
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.title('Trajetória da Bola e do Robô')
    plt.show()

def plot_robot_ball_interception(x_robo, y_robo, x_bola, y_bola, intercept_time, delta_t=0.02):
    # Encontrar o número de pontos até o tempo de interceptação
    num_points = int(intercept_time / delta_t) + 1  # +1 para incluir o ponto de interceptação

    # Criar array de passos de tempo até o intercept_time
    time_steps = np.linspace(0, intercept_time, num_points)

    plt.figure(figsize=(10, 5))

    # Plota as posições do robô até o num_points
    plt.plot(time_steps, x_robo[:num_points], 'r-', label='Robô X')
    plt.plot(time_steps, y_robo[:num_points], 'orange', label='Robô Y')

    # Plota as posições da bola até o num_points
    plt.plot(time_steps, x_bola[:num_points], 'b-', label='Bola X')
    plt.plot(time_steps, y_bola[:num_points], 'purple', label='Bola Y')

    # Marca o ponto de interceptação
    plt.scatter(time_steps[-1], x_robo[num_points-1], color='red', label='Interceptação X')
    plt.scatter(time_steps[-1], y_robo[num_points-1], color='orange', label='Interceptação Y')

    plt.xlabel('Tempo (s)')
    plt.ylabel('Posição (m)')
    plt.title('Trajetória do Robô e da Bola até a Interceptação')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_velocity(x_robo, y_robo, x_bola, y_bola, intercept_time, delta_t=0.02):
    # Encontrar o índice para o tempo de interceptação
    intercept_index = int(intercept_time / delta_t) + 1

    # Calcula as velocidades
    vx_robo = calculate_velocity(x_robo[:intercept_index], delta_t)
    vy_robo = calculate_velocity(y_robo[:intercept_index], delta_t)
    vx_bola = calculate_velocity(x_bola[:intercept_index], delta_t)
    vy_bola = calculate_velocity(y_bola[:intercept_index], delta_t)

    time_array = np.arange(0, intercept_time, delta_t)[:intercept_index]

    plt.figure(figsize=(10, 5))

    # Plota as velocidades do robô
    plt.plot(time_array, vx_robo, 'r-', label='Velocidade Robô X (m/s)')
    plt.plot(time_array, vy_robo, 'orange', label='Velocidade Robô Y (m/s)')

    # Plota as velocidades da bola
    plt.plot(time_array, vx_bola, 'b-', label='Velocidade Bola X (m/s)')
    plt.plot(time_array, vy_bola, 'purple', label='Velocidade Bola Y (m/s)')

    plt.xlabel('Tempo (s)')
    plt.ylabel('Velocidade (m/s)')
    plt.title('Velocidade do Robô e da Bola até o Ponto de Interceptação')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_accelerations(x_traj, y_traj, x_bola, y_bola, delta_t, intercept_time):
    # Calcula a velocidade para cada componente
    vel_robo_x = calculate_velocity(x_traj, delta_t)
    vel_robo_y = calculate_velocity(y_traj, delta_t)
    vel_bola_x = calculate_velocity(x_bola, delta_t)
    vel_bola_y = calculate_velocity(y_bola, delta_t)
    
    # Calcula a aceleração para cada componente
    acel_robo_x = calculate_acceleration(vel_robo_x, delta_t)
    acel_robo_y = calculate_acceleration(vel_robo_y, delta_t)
    acel_bola_x = calculate_acceleration(vel_bola_x, delta_t)
    acel_bola_y = calculate_acceleration(vel_bola_y, delta_t)
    
    # Prepara o vetor de tempo
    tempos = np.arange(0, len(x_traj) * delta_t, delta_t)
    # Limita os dados ao tempo de interceptação
    idx_interceptacao = int(intercept_time // delta_t)

    # Plota as acelerações
    plt.figure(figsize=(10, 6))
    plt.plot(tempos[:idx_interceptacao], acel_robo_x[:idx_interceptacao], 'r-', label='Aceleração Robô X (m/s²)')
    plt.plot(tempos[:idx_interceptacao], acel_robo_y[:idx_interceptacao], 'orange', label='Aceleração Robô Y (m/s²)')
    plt.plot(tempos[:idx_interceptacao], acel_bola_x[:idx_interceptacao], 'b-', label='Aceleração Bola X (m/s²)')
    plt.plot(tempos[:idx_interceptacao], acel_bola_y[:idx_interceptacao], 'purple', label='Aceleração Bola Y (m/s²)')

    plt.xlabel('Tempo (s)')
    plt.ylabel('Aceleração (m/s²)')
    plt.title('Aceleração do Robô e da Bola em função do Tempo')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_distances_over_time(distances, delta_t, intercept_time=None):
    # Cria um vetor de tempo correspondente às distâncias calculadas
    times = np.arange(0, len(distances) * delta_t, delta_t)
    
    # Limita os vetores ao tempo de interceptação se um for fornecido
    if intercept_time is not None:
        max_index = int(intercept_time / delta_t)
        times = times[:max_index + 1]
        distances = distances[:max_index + 1]

    plt.figure()
    plt.plot(times, distances, label='Distância entre robô e bola')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Distância (m)')
    plt.title('Redução da Distância entre Robô e Bola com o Tempo')
    plt.legend()
    plt.grid(True)
    plt.show()
def main():
    # Carrega a trajetória da bola
    x_bola, y_bola = load_bola_trajectory("trajetoria_da_bola.txt")
    if x_bola is None or y_bola is None:
        print("Erro ao carregar dados da bola. Encerrando o programa.")
        return

    # Obtém a posição inicial do robô
    x_robo, y_robo = get_robo_initial_position()
    
    # Calcula a trajetória do robô, o tempo e o ponto de interceptação
    x_traj, y_traj, intercept_time, intercept_point = calculate_robo_trajectory(x_bola, y_bola, x_robo, y_robo)

    # Calcula a distância do robô e da bola até o ponto de interceptação
    distances = calculate_distances(x_traj, y_traj, x_bola, y_bola)

    # Inicializa o pygame e configura a janela
    pygame.init()
    window_size = (1200, 900)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption('Trajetória da Bola e do Robô')

    # Dimensões do campo de futebol em metros
    campo_largura_m = 9
    campo_altura_m = 6

    # Define a escala para o campo de futebol
    # Calcula a escala para que o campo de futebol caiba na janela mantendo a proporção
    scale_x = window_size[0] / campo_largura_m
    scale_y = window_size[1] / campo_altura_m
    scale = min(scale_x, scale_y)  # Mantém a proporção sem distorcer

    # Centraliza o campo na janela
    offset_x = (window_size[0] - (campo_largura_m * scale)) / 2
    offset_y = (window_size[1] - (campo_altura_m * scale)) / 2

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))  # Preenche a tela com branco

        max_points = min(len(x_bola), len(x_traj))
        # Armazena os pontos das trajetórias em listas
        points_bola = [(int(x_bola[i] * scale) + offset_x, window_size[1] - (int(y_bola[i] * scale) + offset_y)) for i in range(max_points)]
        points_robo = [(int(x_traj[i] * scale) + offset_x, window_size[1] - (int(y_traj[i] * scale) + offset_y)) for i in range(max_points)]

        # Desenha as trajetórias da bola e do robô
        pygame.draw.lines(screen, (0, 0, 255), False, points_bola, 7)
        pygame.draw.lines(screen, (255, 0, 0), False, points_robo, 7)

        # Desenha as linhas do campo de futebol
        campo_color = (0, 100, 0)
        pygame.draw.rect(screen, campo_color, (offset_x, offset_y, campo_largura_m * scale, campo_altura_m * scale), 3)

        # Se um ponto de interceptação foi calculado, desenha um círculo nesse ponto
        if intercept_point is not None:
            # Converte as coordenadas de interceptação para a escala da janela
            intercept_point_scaled = (int(intercept_point[0] * scale) + offset_x, window_size[1] - (int(intercept_point[1] * scale) + offset_y))
            pygame.draw.circle(screen, (0, 255, 0), intercept_point_scaled, 10)

        pygame.display.flip()  # Atualiza a tela
        clock.tick(60)  # Limita o FPS a 60

    pygame.quit()
    
    # Chama as funções de plotagem após o loop do Pygame
    plot_trajectory(x_bola, y_bola, x_traj, y_traj)
    if intercept_time is not None:
        plot_robot_ball_interception(x_traj, y_traj, x_bola, y_bola, intercept_time)
        plot_velocity(x_traj, y_traj, x_bola, y_bola, intercept_time)
        plot_accelerations(x_traj, y_traj, x_bola, y_bola, 0.02, intercept_time)
        plot_distances_over_time(distances, 0.02, intercept_time)

if __name__ == "__main__":
    main()
