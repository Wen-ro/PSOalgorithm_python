import math
import random as rd
import numpy as np
import matplotlib.pyplot as plt
import timeit

bounds = [(-1, 3), (-1, 2)]
swarm_size = 50
iteration = 500
weight = 0.8  # 前一代的影響程度 initial weight
c1 = 2
c2 = 2
kv = 0.3  # fix it to the heart


def obj_fun(x, s):  # 求fitness值
    if (x[s][0] + x[s][1]) >= -1:
        y = 6 - ((math.sin(math.sqrt(x[s][0] ** 2 + x[s][1] ** 2))) ** 2) / (
                    (1 + 0.1 * (x[s][0] ** 2 - x[s][1] ** 2)) ** 8)
    else:  # add penalty: x+y<-1
        y = 6 - ((math.sin(math.sqrt(x[s][0] ** 2 + x[s][1] ** 2))) ** 2) / (
                    (1 + 0.1 * (x[s][0] ** 2 - x[s][1] ** 2)) ** 8) - 2000
    return y


def initialization():
    initial_location = []  # swarm location
    initial_velocity = []  # swarm velocity
    initial_fitness = []  # all initial fitness

    for s in range(swarm_size):
        particle_location = []  # single particle position
        particle_velocity = []  # single particle velocity

        for i in range(2):  # random
            lower_bound = bounds[i][0]
            upper_bound = bounds[i][1]
            position_temp = rd.uniform(0, 1)  # random generate the x,y in initial particle
            position = lower_bound + position_temp * (upper_bound - lower_bound)  # revise the position
            particle_location.append(position)  # generate random initial position
            particle_velocity.append(rd.uniform(0, 1) * 2 + lower_bound)  # generate random initial velocity
        initial_location.append(particle_location)  # 把單一粒子插入群體
        initial_velocity.append(particle_velocity)
        # initial evaluation
        fitness = obj_fun(initial_location, s)
        initial_fitness.append(fitness)  # get each particle fitness
    return initial_location, initial_velocity, initial_fitness


def evaluation(current_location, gbest_fitness, gbest_location):
    current_fitness_temp = []
    for s in range(swarm_size):
        fitness = obj_fun(current_location, s)  # evaluate each particle fitness
        current_fitness_temp.append(fitness)
        current_fitness = current_fitness_temp  # store in current fitness
        # update pbest
        if current_fitness[s] > pbest_fitness[s]:
            pbest_fitness[s] = current_fitness[s]  # replace pbest fitness
            pbest_location[s] = current_location[s]  # replace pbest location
        # update gbest
        if current_fitness[s] > gbest_fitness:
            gbest_fitness = current_fitness[s]  # replace gbest fitness (single value)
            gbest_location = current_location[s]    # replace gbest fitness (single particle)

    return pbest_location, pbest_fitness, gbest_location, gbest_fitness


def calculate_velocity(pbest_location, gbest_location, current_location, current_velocity):
    r1 = rd.uniform(0, 1)
    r2 = rd.uniform(0, 1)
    # 因list無法直接計算，故以下皆先轉成np計算再轉回list
    cognitive_velocity_temp = c1 * r1 * (np.array(pbest_location) - np.array(current_location))
    social_velocity_temp = c2 * r2 * (np.array(gbest_location) - np.array(current_location))
    front_part_temp = weight * np.array(current_velocity)
    update_velocity_temp = front_part_temp + cognitive_velocity_temp + social_velocity_temp  # calculate new velocity
    update_velocity = update_velocity_temp.tolist()

    xvmax = kv * 3  # 限制 x 的加速度，使其下次不會直接跳出邊界
    for i in range(swarm_size):
        if update_velocity[i][0] > xvmax:
            update_velocity[i][0] = xvmax
        elif update_velocity[i][0] < -xvmax:
            update_velocity[i][0] = -xvmax
    #print(s,"x_vel:", update_velocity[i][0])
    yvmax = kv * 2  # 限制 y 的加速度，使其下次不會直接跳出邊界
    for i in range(swarm_size):
        if update_velocity[i][1] > yvmax:
            update_velocity[i][1] = yvmax
        elif update_velocity[i][1] < (-yvmax):
            update_velocity[i][1] = (-yvmax)
    return update_velocity


def calculate_location(current_location, update_velocity):  # calculate new location
    update_location_temp = np.array(current_location) + np.array(update_velocity)
    current_location = update_location_temp.tolist()  # 因list無法直接計算，故先轉成np計算再轉回list
    if current_location[s][0] > 2:  # repair location: x <= 2
        current_location[s][0] = 2
    elif current_location[s][0] < -1:  # repair location: x >= -1
        current_location[s][0] = -1
    elif current_location[s][1] > 1:  # repair location: y <= 1
        current_location[s][1] = 1
    elif current_location[s][1] < -1:  # repair location: y >= -1
        current_location[s][1] = -1
    return current_location


###################


# Initialization (include initial evaluation)
current_location, current_velocity, initial_fitness = initialization()
pbest_location = current_location  # pbest is the current location in first iteration
pbest_fitness = initial_fitness  # fitness in first iteration is pbest
gbest_fitness = max(initial_fitness)    # best fitness among the iteration
gbest_location = current_location[initial_fitness.index(gbest_fitness)]  # record gbest location

# PSO
history_gbest_fitness = []  # for gbest every iteration
for j in range(iteration):

    pbest_location, pbest_fitness, gbest_location, gbest_fitness = evaluation(current_location, gbest_fitness,
                                                                              gbest_location)  # include pbest, gbest
    history_gbest_fitness.append(gbest_fitness)  # store gbest every iteration

    for s in range(swarm_size):
        update_velocity = calculate_velocity(pbest_location, gbest_location, current_location, current_velocity)
        current_location = calculate_location(current_location, update_velocity)

print("max history_gbest_fitness:", max(history_gbest_fitness))
print("optimal x:", gbest_location[0])
print("optimal y:", gbest_location[1])
print("time:", timeit.timeit())
#plt.plot(history_gbest_fitness)
#plt.show()
