import math
import random
import matplotlib.pyplot as plt

amount = 0
bigs = 0
bigs_alt = [0, 0, 0]
initial_inv_level = 60
inv_level = 0
next_event_type = 0
num_events = 0
num_months = 120
num_values_demand = 4
smalls = 0
smalls_alt = [0, 0, 0]

area_holding = 0.0
area_shortage = 0.0
holding_cost = 1.0
incremental_cost = 3.0
maxlag = 1.0
mean_interdemand = 0.1
minlag = 0.5
prob_distrib_demand = [0.167, 0.500, 0.833, 1.000]
setup_cost = 32.0
shortage_cost = 5.0
sim_time = 0.0
time_last_event = 0.0
time_next_event = [0.0] * 5
total_ordering_cost = 0.0

avg_total_cost_list = []
avg_ordering_cost_list = []
avg_holding_cost_list = []
avg_shortage_cost_list = []

def initialize():
    global sim_time, inv_level, time_last_event, total_ordering_cost, area_holding, area_shortage

    sim_time = 0.0
    inv_level = initial_inv_level
    time_last_event = 0.0
    total_ordering_cost = 0.0
    area_holding = 0.0
    area_shortage = 0.0

    time_next_event[1] = 1.0e+30
    time_next_event[2] = sim_time + expon(mean_interdemand)
    time_next_event[3] = num_months
    time_next_event[4] = 0.0

def timing():
    global next_event_type, sim_time

    min_time_next_event = 1.0e+29
    next_event_type = 0

    for i in range(1, num_events + 1):
        if time_next_event[i] < min_time_next_event:
            min_time_next_event = time_next_event[i]
            next_event_type = i

    if next_event_type == 0:
        print("La lista de eventos está vacía en el tiempo", sim_time)
        exit(1)

    sim_time = min_time_next_event

def order_arrival():
    global inv_level, time_next_event

    inv_level += amount

    time_next_event[1] = 1.0e+30

def demand():
    global inv_level, time_next_event

    inv_level -= random_integer(prob_distrib_demand)

    time_next_event[2] = sim_time + expon(mean_interdemand)

def evaluate():
    global inv_level, time_next_event, amount, total_ordering_cost

    if inv_level < smalls:
        amount = bigs - inv_level
        total_ordering_cost += setup_cost + incremental_cost * amount

        time_next_event[1] = sim_time + uniform(minlag, maxlag)

    time_next_event[4] = sim_time + 1.0

def report():
    global inv_level, time_next_event, amount, total_ordering_cost, area_holding, area_shortage
    avg_holding_cost = holding_cost * area_holding / num_months
    avg_ordering_cost = total_ordering_cost / num_months
    avg_shortage_cost = shortage_cost * area_shortage / num_months

    print(f"\n\n({smalls},{bigs})".rjust(7), end="")
    print(f"{(avg_ordering_cost + avg_holding_cost + avg_shortage_cost):15.2f}", end="")
    print(f"{avg_ordering_cost:15.2f}", end="")
    print(f"{avg_holding_cost:15.2f}", end="")
    print(f"{avg_shortage_cost:15.2f}", end="")

    avg_total_cost_list.append(avg_ordering_cost + avg_holding_cost + avg_shortage_cost)
    avg_ordering_cost_list.append(avg_ordering_cost)
    avg_holding_cost_list.append(avg_holding_cost)
    avg_shortage_cost_list.append(avg_shortage_cost)

    # Reset the area holding and area shortage for the next policy run
    area_holding = 0.0
    area_shortage = 0.0

def update_time_avg_stats():
    global area_holding, area_shortage, time_last_event, inv_level

    time_since_last_event = sim_time - time_last_event
    time_last_event = sim_time

    if inv_level < 0:
        area_shortage -= inv_level * time_since_last_event
    elif inv_level > 0:
        area_holding += inv_level * time_since_last_event

def random_integer(prob_distrib):
    u = random.random()
    i = 1

    while u >= prob_distrib[i]:
        i += 1

    return i

def expon(mean):
    u = random.random()
    return -mean * math.log(u)

def uniform(a, b):
    u = random.random()
    return a + u * (b - a)

def main():
    global num_events, sim_time, num_months, num_policies, num_values_demand, mean_interdemand, setup_cost
    global incremental_cost, holding_cost, shortage_cost, minlag, maxlag, smalls, bigs

    num_events = 4
    num_policies = 9
    num_values_demand = 4
    mean_interdemand = 0.1
    setup_cost = 32.0
    incremental_cost = 3.0
    holding_cost = 1.0
    shortage_cost = 5.0
    minlag = 0.5
    maxlag = 1.0

    print("Sistema de inventario de un solo producto\n")
    print(f"Nivel de inventario inicial: {initial_inv_level} artículos\n")
    print(f"Número de tamaños de demanda: {num_values_demand}\n")
    print("Función de distribución de tamaños de demanda:", end=" ")
    print(f"Tiempo medio entre demandas: {mean_interdemand:.2f}\n")
    print(f"Rango de demora de entrega: {minlag:.2f} a {maxlag:.2f} meses\n")
    print(f"Duración de la simulación: {num_months} meses\n")
    print(f"K = {setup_cost:.1f}, i = {incremental_cost:.1f}, h = {holding_cost:.1f}, pi = {shortage_cost:.1f}\n")
    print(f"Número de políticas: {num_policies}\n")
    print("Promedio".rjust(7), "Costo total".rjust(15), "Costo de orden".rjust(15), "Costo de almacenamiento".rjust(15), "Costo de escasez".rjust(15))

    smalls_alt = [20, 40, 60]
    bigs_alt = [40, 60, 80, 100]

    for smalls in smalls_alt:
        for bigs in bigs_alt:
            for i in range(num_policies):
                initialize()
                sim_time = 0.0

                while sim_time < num_months:
                    timing()
                    update_time_avg_stats()

                    if next_event_type == 1:
                        order_arrival()
                    elif next_event_type == 2:
                        demand()
                    elif next_event_type == 4:
                        evaluate()
                    elif next_event_type == 3:
                        report()

                    if next_event_type != 3:
                        sim_time = time_next_event[next_event_type]

                report()

    # Graficar los promedios de costos
    plt.figure(figsize=(10, 6))
    plt.plot(avg_total_cost_list, label='Costo total')
    plt.plot(avg_ordering_cost_list, label='Costo de orden')
    plt.plot(avg_holding_cost_list, label='Costo de almacenamiento')
    plt.plot(avg_shortage_cost_list, label='Costo de escasez')
    plt.xlabel('Política')
    plt.ylabel('Promedio de costo')
    plt.title('Promedios de costos por política')
    plt.legend()
    plt.show()

# Ejecutar la simulación
main()
