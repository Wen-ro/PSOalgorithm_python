import math
import random as rd
import numpy as np

bounds = [(-1, 3), (-1, 2)]
particle_size = 50
iteration = 100
weight = 0.8  # 前一代的影響程度 initial weight
c1 = 2
c2 = 2


def obj_fun(x):  # 求fitness值
    if (x[0] + x[1]) >= -1:
        y = 6 - ((math.sin(math.sqrt(x[0] ** 2 + x[1] ** 2))) ** 2) / ((1 + 0.1 * (x[0] ** 2 - x[1] ** 2)) ** 8)
    else:  # add penalty: x+y<-1
        y = 6 - ((math.sin(math.sqrt(x[0] ** 2 + x[1] ** 2))) ** 2) / ((1 + 0.1 * (x[0] ** 2 - x[1] ** 2)) ** 8) - 20
    return y


def initialization():
    initial_location = []  # swarm location
    initial_velocity = []  # swarm velocity
    initial_fitness = []  # all initial fitness

    for s in range(particle_size):
        particle_location = []  # single particle position
        particle_velocity = []  # single particle velocity

        for i in range(2):
            particle_location.append(rd.uniform(bounds[i][0], bounds[i][1]))  # generate random initial position
            particle_velocity.append(rd.uniform(-1, 1))  # generate random initial velocity
        initial_location.append(particle_location)  # 把單一粒子插入群體
        initial_velocity.append(particle_velocity)
        # initial evaluation
        fitness = obj_fun(initial_location)
        initial_fitness.append(fitness)  # get each particle fitness

    return initial_location, initial_velocity, initial_fitness


def evaluation(current_location):
    current_fitness = []
    # evaluation
    fitness = obj_fun(current_location)
    current_fitness.append(fitness)  # get each particle fitness

    print("##########decide pbest###########")

    if fitness > pbest_fitness:
        print("particle position:", particle_position)
        fitness_of_pbest_particle = fitness
        print(s, "pbest fitness:", fitness_of_pbest_particle)
        pbest_particle_position = particle_position
        print("pbest location:", pbest_particle_position)  # 對第1代而言自己也是pbest
        #return fitness_of_pbest_particle, pbest_particle_position
    return fitness, current_fitness, pbest_particle_position


def find_global_best(fitness_value, particle_position, fitness_of_each_particle):
    print("##########decide global best###########")
    print('each particle fitness:', fitness_of_each_particle)
    print('best fitness', max(fitness_of_each_particle))
    gbest_particle_position = particle_position
    print("test gbest:", gbest_particle_position)
    fitness_of_gbest_particle = max(fitness_of_each_particle)
    print("fitness_of_gbest_particle:", fitness_of_gbest_particle)
    print("fit value:", fitness_value)

    if fitness_value > fitness_of_gbest_particle:
        print('!!!each particle fitness:', fitness_of_each_particle)
        print(s, 'particle fitness:', fitness_value)
        gbest_particle_position.append(particle_position)  # put global best into list
        print('gbest particle', gbest_particle_position)
        fitness_of_gbest_particle = fitness_value  # update the fitness of the global best
        print("fitness_of_gbest_particle:", fitness_of_gbest_particle)
    return gbest_particle_position, fitness_of_gbest_particle


def calculate_particle_velocity(particle_velocity, pbest_particle_position, gbest_particle_position):
    for i in range(2):
        r1 = rd.random()
        r2 = rd.random()
        print("###########calculate velocity############")
        print("particle position:", particle_position)
        print("pbest_location", pbest_particle_position)
        print("gbest_location", gbest_particle_position)
        cognitive_velocity_temp = c1 * r1 * (np.array(pbest_particle_position) - np.array(particle_position))
        social_velocity_temp = c2 * r2 * (np.array(gbest_particle_position) - np.array(particle_position))
        front_part_temp = weight * np.array(particle_velocity)
        particle_velocity_temp = front_part_temp + cognitive_velocity_temp + social_velocity_temp
        particle_velocity = particle_velocity_temp.tolist()  # 因list無法直接計算，故先轉成np計算再轉回list
    return particle_velocity


def update_location():
    print("###########update location############")  # 下一代
    print(" original particle position:", particle_position)
    particle_position_temp = np.array(particle_position) + particle_velocity_temp
    # np.array(particle_velocity)
    particle_position = particle_position_temp.tolist()  # 因list無法直接計算，故先轉成np計算再轉回list
    print("after particle position:", particle_position)


#############
#pbest_location = []  # best position of the particle
gbest_location = []  # global best particle of the swarm
#pbest_fitness = []  # objective function value of the local best particle position
gbest_fitness = []  # objective function value of the global best particle position (in swarm)


# Initialization
current_location, current_velocity, current_fitness = initialization()
pbest_location = current_location  # best position of the particle
pbest_fitness = current_fitness   # objective function value of the local best particle position
gbest_fitness = max(pbest_fitness)
gbest_location = pbest_location[pbest_fitness.index(gbest_fitness)]

# PSO
for j in range(iteration):
    for s in range(particle_size):

        fitness_value, current_fitness, pbest_location = evaluation(pbest_fitness, pbest_location)
        find_global_best(fitness_value, particle_position, current_fitness)


    gbest_fitness = []  # objective function value of the global best particle position (in swarm)

    for s in range(particle_size):
        calculate_particle_velocity(particle_velocity, pbest_location, gbest_location)
        update_location()


print("Done")

