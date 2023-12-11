import simpy
import random

area_iluminacao = 35  # metros
velocidade_via = 60  # km/h
vel_via = velocidade_via / 3.6  # m/s


def poste_iluminacao(env, sensor, luminaria):
    while True:
        yield env.timeout(random.expovariate(1.0))
        print(f"Alerta! Carro se aproximando no tempo {env.now}, ligando luz")
        luz_acesa = env.now
        with sensor.request() as req:
            yield req
            yield env.timeout(random.uniform(1, 10))
            print(f"Alerta! Carro saindo no tempo {env.now}, desligando luz")
            luz_apagada = env.now
            luminaria.append(luz_apagada - luz_acesa)


env = simpy.Environment()
sensor = simpy.Resource(env, capacity=1)
luminaria = []

env.process(poste_iluminacao(env, sensor, luminaria))

env.run(until=100)

tempo_total_acesa = sum(luminaria)
print(f"Tempo total que a luminária permaneceu acesa: {tempo_total_acesa}")