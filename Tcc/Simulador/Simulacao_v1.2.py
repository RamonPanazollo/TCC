# Importação das bibliotecas
import simpy
import random

# Calcula o tempo com base na área de iluminação e velocidade da via fornecidos pelo usuário
def obter_tempo(area_iluminacao, velocidade_via):
    vel_via_m_por_s = velocidade_via / 3.6  # km/h para m/s
    tempo = area_iluminacao / vel_via_m_por_s
    return tempo

# Converte o tempo (Horas, Minutos ou Segundos)
def converter_para_horas_minutos_segundos(tempo_em_segundos):
    horas = tempo_em_segundos // 3600
    minutos = (tempo_em_segundos % 3600) // 60
    segundos = tempo_em_segundos % 60
    return horas, minutos, segundos

def poste_iluminacao(env, sensor, luminaria, tempo):
    while True:
        yield env.timeout(random.uniform(1, 15))
        print(f"Alerta! Carro se aproximando no tempo {env.now}, ligando luz")
        luz_acesa = env.now
        with sensor.request() as req:
            yield req
            yield env.timeout(abs(random.gauss(tempo, desvio_padrao)))
            print(f"Alerta! Carro saindo no tempo {env.now}, desligando luz")
            luz_apagada = env.now
            luminaria.append(luz_apagada - luz_acesa)

def simulacao(area_iluminacao, velocidade_via, desvio_padrao, tempo_simulacao, unidade_tempo_simulacao):
    tempo = obter_tempo(area_iluminacao, velocidade_via)
    if unidade_tempo_simulacao == "minutos":
        tempo_simulacao *= 60  # Converte minutos para segundos
    elif unidade_tempo_simulacao == "horas":
        tempo_simulacao *= 3600  # Converte horas para segundos
    env = simpy.Environment()
    sensor = simpy.Resource(env, capacity=1)
    luminaria = []
    env.process(poste_iluminacao(env, sensor, luminaria, tempo))
    env.run(until=tempo_simulacao)
    tempo_total_acesa = sum(luminaria)
    percentual_tempo_acesa = (tempo_total_acesa / tempo_simulacao) * 100
    return percentual_tempo_acesa

def imprimir_resultados(tempo_total_acesa, quantidade_carros):
    horas, minutos, segundos = converter_para_horas_minutos_segundos(tempo_total_acesa)
    print(f"Tempo total que a luminária permaneceu acesa: {horas} horas, {minutos} minutos e {segundos} segundos.")
    print(f"Quantidade de carros que passaram durante a simulação: {quantidade_carros}.")
    print(f"Percentual de tempo que a luminária esteve acesa: {tempo_total_acesa:.2f}%")

# Entrada do usuário
desvio_padrao = 1
area_iluminacao = float(input("Digite a área de iluminação em metros: "))  ## para roraima, aproximadamente 31m
velocidade_via = float(input("Digite a velocidade da via em km/h: "))  ## 30~50
tempo_simulacao = float(input("Digite o tempo de simulação: ")) # 10
unidade_tempo_simulacao = input("Digite a unidade de tempo (segundos (S), minutos (M) ou horas (H)): ").lower() # Minutos

# Executando a simulação
percentual_tempo_acesa = simulacao(area_iluminacao, velocidade_via, desvio_padrao, tempo_simulacao, unidade_tempo_simulacao)

# Resultados da simulação
imprimir_resultados(percentual_tempo_acesa, int(tempo_simulacao))