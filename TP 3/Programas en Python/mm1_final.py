import numpy as np
import matplotlib.pyplot as plt


class Queue_mm1:
    def __init__(self, num_events, mean_interarrival, mean_service, Q_LIMIT):
        self.num_events = num_events
        self.mean_interarrival = mean_interarrival
        self.mean_service = mean_service
        self.Q_LIMIT = Q_LIMIT
        self.parameter_lambda = 1 / self.mean_interarrival
        self.parameter_mu = 1 / self.mean_service

        self.initialize()

    def initialize(self):
        self.clock = 0.0
        self.num_custs_delayed = 0
        self.total_of_delays = 0.0
        self.num_in_q = 0
        self.server_status = 0
        self.probI = []

        self.time_last_event = 0.0
        self.time_arrival = [0.0 for i in range(1000)]
        # self.time_arrival = [0.0 for i in range(Q_LIMIT + 1)]
        self.qdet = []

        self.next_event_time = np.empty(self.num_events + 1)
        self.next_event_type = 0
        self.clientes_denegados = 0
        self.area_num_in_q = 0.0
        self.area_server_status = 0.0

        self.total_time_spent = 0.0
        self.total_time_in_queue = 0.0

        self.time = 0.0

        self.initialize_next_event()

    def initialize_next_event(self):
        self.next_event_time[1] = self.time + self.expon(self.mean_interarrival)
        self.next_event_time[2] = 1.0e+30

    def timing(self):
        self.next_event_type = 0
        min_time_next_event = 1.0e+29

        for i in range(1, self.num_events + 1):
            if self.next_event_time[i] < min_time_next_event:
                min_time_next_event = self.next_event_time[i]
                self.next_event_type = i

        if self.next_event_type == 0:
            print("Event list empty at time {}".format(self.time))
            exit(1)

        self.time = min_time_next_event

    def arrive(self):
        self.next_event_time[1] = self.time + self.expon(self.mean_interarrival)

        if self.server_status == 1:
            self.num_in_q += 1
            if self.num_in_q >= len(self.probI):
                self.probI.extend([0] * (self.num_in_q - len(self.probI) + 1))
            self.probI[self.num_in_q] += 1  # chequear
            # Si es mm1k y la cola está llena
            if (self.num_in_q > self.Q_LIMIT):
                self.clientes_denegados += 1
            else:
                self.time_arrival[self.num_in_q] = self.time

        else:
            self.delay = 0.0
            self.total_of_delays += self.delay

            self.num_custs_delayed += 1
            self.server_status = 1
            self.next_event_time[2] = self.time + self.expon(self.mean_service)

    def depart(self):
        if self.num_in_q > 0:
            self.num_in_q -= 1
            self.delay = self.time - self.time_arrival[1]
            self.total_of_delays += self.delay
            self.probI[self.num_in_q] += 1  # chequear
            self.num_custs_delayed += 1
            self.next_event_time[2] = self.time + self.expon(self.mean_service)
            for i in range(self.num_in_q):
                self.time_arrival[i] = self.time_arrival[i + 1]
            self.time_arrival[self.num_in_q] = 0.0

        else:
            self.server_status = 0
            self.next_event_time[2] = 1.0e+30

    def update_time_avg_stats(self):
        self.time_since_last_event = self.time - self.time_last_event
        self.time_last_event = self.time

        self.qdet.append(self.num_in_q * self.time_since_last_event / self.time)
        self.area_num_in_q += self.num_in_q * self.time_since_last_event
        self.area_server_status += self.server_status * self.time_since_last_event

    def expon(self, mean):
        return -mean * np.log(np.random.rand())

    def simulate(self):
        countWhile = 0
        while self.time <= 100:
            countWhile += 1
            self.timing()
            self.update_time_avg_stats()
            if self.next_event_type == 1:
                self.arrive()
            elif self.next_event_type == 2:
                self.depart()

            self.qdet.append(self.num_in_q)
        for i in range(self.num_in_q):
            self.probI[i] /= countWhile


def main():
    num_events = 2
    mean_service = 1

    arrival_rate_percentages = [0.25, 0.5, 0.75, 1.0, 1.25]

    max_queue_length = 0
    for arrival_rate_percentage in arrival_rate_percentages:
        mean_interarrival = arrival_rate_percentage * mean_service

        avg_num_in_system_list = []
        avg_num_in_queue_list = []
        avg_time_in_system_list = []
        avg_time_in_queue_list = []
        utilization_list = []
        prob_queue_list = []
        prob_denial_list = []
        simulation_time_list = []
        limit = [0, 2, 5, 10, 50]
        for Q_LIMIT in limit:

            for i in range(10):
                np.random.seed()

                queue = Queue_mm1(num_events, mean_interarrival, mean_service, Q_LIMIT)
                queue.simulate()

                avg_num_in_queue_list.append(queue.area_num_in_q / queue.time)
                avg_num_in_system_list.append(queue.num_in_q + queue.parameter_lambda / queue.parameter_mu)
                avg_time_in_queue_list.append(queue.total_of_delays / queue.num_custs_delayed)
                avg_time_in_system_list.append(queue.total_of_delays + 1 / queue.parameter_mu)
                utilization_list.append(queue.area_server_status / queue.time)
                simulation_time_list.append(queue.time)

                if queue.num_in_q > queue.Q_LIMIT:
                    num_custs_attempted = queue.num_in_q + queue.clientes_denegados
                    denegacion_servicio = queue.clientes_denegados / num_custs_attempted
                    prob_denial_list.append(denegacion_servicio)

                max_queue_length = max(max_queue_length, max(queue.qdet))
                prob_queue = np.bincount(queue.qdet) / len(queue.qdet)
                prob_queue_list.append(prob_queue)

            # Mostrar datos de la simulacion
            print(f"Tasa de llegada: {arrival_rate_percentage * 100}% de la tasa de servicio. Cola:{Q_LIMIT}")
            print("Promedio de clientes en el sistema:", np.mean(avg_num_in_system_list))
            print("Promedio de clientes en la cola:", np.mean(avg_num_in_queue_list))
            print("Tiempo promedio en el sistema:", np.mean(avg_time_in_system_list))
            print("Tiempo promedio en la cola:", np.mean(avg_time_in_queue_list))
            print("Utilización del servidor:", np.mean(utilization_list))
            print("Clientes denegados:", np.mean(queue.clientes_denegados))
            print("Número en cola:", np.mean(queue.num_in_q))
            print("Probabilidad de encontrar n clientes en la cola:")
            print(queue.probI)
            print("Probabilidad de denegación de servicio:")
            print(denegacion_servicio)

            plt.plot(simulation_time_list)
            plt.xlabel('Indice de la simulación')
            plt.ylabel('Tiempo de simulación')
            plt.title('Tiempo de simulación por simulación')
            plt.show()

            # Graficar avg_num_in_system_list
            plt.plot(avg_num_in_system_list)
            plt.xlabel('Indice de la simulación')
            plt.ylabel('Promedio de clientes en el sistema')
            plt.title('Promedio de clientes en el sistema por simulación')
            plt.show()

            # Graficar avg_num_in_queue_list
            plt.plot(avg_num_in_queue_list)
            plt.xlabel('Indice de la simulación')
            plt.ylabel('Promedio de clientes en la cola')
            plt.title('Promedio de clientes en la cola por simulación')
            plt.show()

            # Graficar avg_time_in_system_list
            plt.plot(avg_time_in_system_list)
            plt.xlabel('Indice de la simulación')
            plt.ylabel('Tiempo promedio en el sistema')
            plt.title('Tiempo promedio en el sistema por simulación')
            plt.show()

            # Graficar avg_time_in_queue_list
            plt.plot(avg_time_in_queue_list)
            plt.xlabel('Indice de la simulación')
            plt.ylabel('Tiempo promedio en la cola')
            plt.title('Tiempo promedio en la cola por simulación')
            plt.show()

            # Graficar utilization_list
            plt.plot(utilization_list)
            plt.xlabel('Indice de la simulación')
            plt.ylabel('Utilización del servidor')
            plt.title('Utilización del servidor por simulación')
            plt.show()

            # Encontrar la longitud mínima de las simulaciones
            min_length = min(len(simulation) for simulation in prob_queue_list)

            # Ajustar la longitud de todas las simulaciones al mínimo
            prob_queue_list_adjusted = [simulation[:min_length] for simulation in prob_queue_list]

            # Convertir prob_queue_list_adjusted en un arreglo de NumPy
            prob_queue_array = np.array(prob_queue_list_adjusted)

            # Calcular el promedio a lo largo del eje 0 (promedio de las simulaciones)
            promedio_prob_queue = np.mean(prob_queue_array, axis=0)

            # Crear una lista de valores para el eje x
            n = np.arange(len(promedio_prob_queue))

            # Graficar el promedio de prob_queue_list(Opcion 1)
            plt.plot(n, promedio_prob_queue)
            plt.xlabel('n')
            plt.ylabel('Probabilidad de encontrar n clientes en la cola')
            plt.title('Promedio de la probabilidad de encontrar n clientes en la cola')
            plt.show()

            # Graficar prob_queue_list(Opcion 2)
            unpacked_list = list(zip(*prob_queue_list))
            array = np.asarray(unpacked_list)
            plt.plot(array)
            plt.xlabel('Indice de la simulación')
            plt.ylabel('Probabilidad de encontrar n clientes en la cola')
            plt.title('Probabilidad de encontrar n clientes en la cola por simulación')
            plt.show()

            # Graficar prob_denial_list
            plt.plot(prob_denial_list)
            plt.xlabel('Indice de la simulación')
            plt.ylabel('Probabilidad de denegación de servicio')
            plt.title('Probabilidad de denegación de servicio por simulación')
            plt.show()


if __name__ == '__main__':
    main()