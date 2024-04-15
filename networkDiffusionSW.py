import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import math
import random
from tqdm import tqdm

def network_init(pop, inf_percentage, m, immune_percentage, aware_percentage):
    G = nx.barabasi_albert_graph(pop, m)

    inf_count = math.ceil(inf_percentage * pop)
    immune_count = math.ceil(immune_percentage * pop)
    aware_count = math.ceil(aware_percentage * pop)

    inf_list = np.zeros(pop, dtype = np.uint8)
    immunity_list = np.zeros(pop, dtype = np.uint8)
    aware_list = np.zeros(pop, dtype = np.uint8)

    infected_nodes = random.sample(range(pop), inf_count)
    immune_nodes = random.sample(range(pop), immune_count)
    aware_nodes = random.sample(range(pop), aware_count)

    for index in infected_nodes:
        inf_list[index] = 1
    
    for index in immune_nodes:
        immunity_list[index] = 1

    for index in aware_nodes:
        aware_list[index] = 1

    node_status = {i: j for i, j in zip(G.nodes, inf_list)}
    nx.set_node_attributes(G, node_status, "status")

    node_immunity = {i: j for i, j in zip(G.nodes, immunity_list)}
    nx.set_node_attributes(G, node_immunity, "immune")

    node_awareness = {i: j for i, j in zip(G.nodes, aware_list)}
    nx.set_node_attributes(G, node_immunity, "aware")

    return G

def iterate(G, beta, gamma, inf_count, sus_count, rem_count):
    inf_velocity, rem_velocity = 0, 0

    """aware_statuses = nx.get_node_attributes(G, "aware")
    for node, aware in aware_statuses.items():
        if aware == 1:
            node_neighbors = [n for n in G.neighbors(node)]
            for k in node_neighbors:
                if G.nodes[k]["aware"] == 0 and (random.random() <= beta):
                    G.nodes[k]["aware"] = 1 """

    statuses = nx.get_node_attributes(G, "status")
    for node, status in statuses.items():
        if status == 1:
            node_neighbors = [n for n in G.neighbors(node)]
            for k in node_neighbors:
                this_beta = beta
                if G.nodes[k]["aware"] == 1:
                    this_beta = beta * 0.8

                if G.nodes[k]["status"] == 0 and G.nodes[k]["immune"] == 0 and (random.random() <= this_beta):
                    G.nodes[k]["status"] = 1
                    inf_velocity += 1
                    inf_count += 1
                    sus_count -= 1

            if (random.random() <= gamma):
                G.nodes[node]["status"] = 2
                rem_velocity += 1
                inf_count -= 1 
                rem_count += 1

    return G, inf_count, sus_count, rem_count, inf_velocity, rem_velocity


def epidemic_model(pop, beta, gamma, density, inf_percentage, immune_percentage, aware_percentage, iterations):
    inf_count = math.ceil(inf_percentage * pop)
    rem_count = 0
    sus_count = pop - inf_count
    immune_count = math.ceil(immune_percentage * pop)

    sus_array = np.zeros(iterations, dtype = np.int32)
    inf_array = np.zeros(iterations, dtype = np.int32)
    rem_array = np.zeros(iterations, dtype = np.int32)
    inf_vel_array = np.zeros(iterations, dtype = np.int32)
    rem_vel_array = np.zeros(iterations, dtype = np.int32)
    x = range(iterations)

    sus_array[0] = sus_count
    inf_array[0] = inf_count
    rem_array[0] = rem_count

    print(f"Initializing Network: {immune_percentage*100}% Immune")
    G = network_init(pop, inf_percentage, m, immune_percentage, aware_percentage)

    for iter in tqdm(range(iterations), desc="Iterating", unit="iteration"):
        G, inf_count, sus_count, rem_count, inf_velocity, rem_velocity = iterate(G, beta, gamma, inf_count, sus_count, rem_count)
        sus_array[iter] = sus_count
        inf_array[iter] = inf_count
        rem_array[iter] = rem_count
        inf_vel_array[iter] = inf_velocity
        rem_vel_array[iter] = rem_velocity
    
    diff_vel_array = result = [i - j for i, j in zip(inf_vel_array, rem_vel_array)]

    mask = np.ones((30))/30
    inf_vel_array_avg = np.convolve(inf_vel_array, mask, 'same')
    rem_vel_array_avg = np.convolve(rem_vel_array, mask, 'same')
    diff_vel_array_avg = np.convolve(diff_vel_array, mask, 'same')

    fig, ax = plt.subplots(1, 1)

    ax.plot(x, inf_array, label='Infected', linestyle='-', color='orange', linewidth = 1)
    ax.plot(x, sus_array, label='Susceptible', linestyle='-', color='blue', linewidth = 1)
    ax.plot(x, rem_array, label='Removed', linestyle='-', color='green', linewidth = 1)
    ax.set_ylabel('Population')
    ax.set_xlabel('Days')
    ax.set_title(f"Percentage immune: {immune_percentage*100}%")
    ax.axhline(y=immune_count, color='red', linestyle='--', label='Immune population', linewidth = 1)
    ax.legend()

    """ ax[1].plot(x, inf_vel_array_avg, label='Infected velocity', linestyle='-', color='orange', linewidth = 0.5)
    ax[1].plot(x, rem_vel_array_avg, label='Removed velocity', linestyle='-', color='green', linewidth = 0.5)
    #ax[1].plot(x, diff_vel_array_avg, label='Velocity difference', linestyle='-', color='red', linewidth = 0.5)
    ax[1].set_xlabel('Iterations')
    ax[1].set_ylabel('Velocity')
    ax[1].set_title('Velocity (Moving average)')
    ax[1].legend() """

    
#Population, Beta, Gamma, Density, Infected percentage, Immune percentage, Iterations
pop = 500
beta = 0.005
gamma = 0.025
aware = 0.2
m = 13

epidemic_model(pop, beta, gamma, m, 0.01, 0.0, aware, 300)
epidemic_model(pop, beta, gamma, m, 0.01, 0.1, aware, 300)
epidemic_model(pop, beta, gamma, m, 0.01, 0.2, aware, 300)
epidemic_model(pop, beta, gamma, m, 0.01, 0.4, aware, 300)
epidemic_model(pop, beta, gamma, m, 0.01, 0.6, aware, 300)
epidemic_model(pop, beta, gamma, m, 0.01, 0.8, aware, 300)

plt.show()