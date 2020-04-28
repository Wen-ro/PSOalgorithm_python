"""""
Problem 4
Maximum f(x,y)= 6 - (sin^2(sqrt((x^2 + y^2)))) / (1 + 0.1 * (x^2 - y^2))^8
-1≤x≤2; -1≤y≤1; x+y≥-1	Maximum=6 at (x,y)=(0,0)

"""

import math
import random as rd
import numpy as np
import matplotlib.pyplot as plt


particle_size = 2
iteration = 100
weight = 0.8    # 前一代的影響程度 initial weight
c1 = 2
c2 = 2
x0_bound = (-1, 2)
x1_bound = (-1, 1)
bounds = [(-1, 3), (-1, 2)]  # 因uniform函數不含上界故上界要+1


# Evaluation
def obj_fun(x):     # 求fitness值
    if (x[0] + x[1]) >= -1:
        y = 6 - ((math.sin(math.sqrt(x[0] ** 2 + x[1] ** 2))) ** 2) / ((1 + 0.1 * (x[0] ** 2 - x[1] ** 2)) ** 8)
    else:  # add penalty: x+y<-1
        y = 6 - ((math.sin(math.sqrt(x[0] ** 2 + x[1] ** 2))) ** 2) / ((1 + 0.1 * (x[0] ** 2 - x[1] ** 2)) ** 8) - 20
    return y


#  Initialization
swarm_particle = []  # swarm position
swarm_velocity = []  # swarm velocity
pbest_particle_position = []  # best position of the particle
gbest_particle_position = []  # global best particle of the swarm
fitness_of_each_particle = []  # objective function value of the particle position
fitness_of_pbest_particle = 0  # objective function value of the local best particle position
fitness_of_gbest_particle = []  # objective function value of the global best particle position (in swarm)


def initialization():
    for i in range(2):
        particle_position.append(rd.uniform(bounds[i][0], bounds[i][1]))  # generate random initial position
        particle_velocity.append(rd.uniform(-1, 1))  # generate random initial velocity
    print(s, "particle：", particle_position)
    print(s, "particle velocity：", particle_velocity)
    swarm_particle.append(particle_position)  # 把單一粒子插入群體
    swarm_velocity.append(particle_velocity)


# First iteration
for s in range(particle_size):
    particle_position = []  # single particle position
    particle_velocity = []  # single particle velocity
    initialization()
    print("swarm：", particle_position)
    print("particle velocity：", particle_velocity)
    print("#########Evaluation###############")
    fitness_value = obj_fun(particle_position)
    print(s, "particle fitness：", fitness_value)
    fitness_of_each_particle.append(fitness_value)  # Evaluation: get each particle fitness

    print("##########decide local best#########")
    if fitness_value > fitness_of_pbest_particle:
        fitness_of_pbest_particle = fitness_value
        print("pbest fitness:", fitness_of_pbest_particle)
        pbest_particle_position = particle_position
        print("pbest location:", pbest_particle_position)  # 對第1代而言自己也是pbest
    else:
        continue

    print("##########decide global best###########")
    print('each particle fitness:', fitness_of_each_particle)
    print('best fitness', max(fitness_of_each_particle))

    if fitness_value > max(fitness_of_each_particle):
        print(s, 'particle fitness:', fitness_value)
        gbest_particle_position.append(particle_position)    # put global best into list
        print('gbest particle', gbest_particle_position[s])
        fitness_of_gbest_particle.append(fitness_value)  # update the fitness of the global best
        print("fitness_of_gbest_particle:", fitness_of_gbest_particle)
    else:
        continue

#################

    print("###########calculate Velocity############")
    print(s, "particle")
    print("pbest_particle_position", pbest_particle_position)
    print("particle_position", particle_position)
    print("gbest_particle_position", gbest_particle_position)
    for i in range(2):
        r1 = rd.random()
        r2 = rd.random()

        cognitive_velocity_temp = c1 * r1 * (np.array(pbest_particle_position[s]) - np.array(particle_position))
        social_velocity_temp = c2 * r2 * (np.array(gbest_particle_position) - np.array(particle_position))
        front_part_temp = weight * np.array(particle_velocity)
        particle_velocity_temp = front_part_temp + cognitive_velocity_temp + social_velocity_temp
        #particle_velocity = particle_velocity_temp.tolist()  # 因list無法直接計算，故先轉成np計算再轉回list

    print("###########update location############")  # 下一代
    print(" original particle position:", particle_position)
    particle_position_temp = np.array(particle_position) + particle_velocity_temp
                             #np.array(particle_velocity)
    particle_position = particle_position_temp.tolist()  # 因list無法直接計算，故先轉成np計算再轉回list
    print("after particle position:", particle_position)

#############



#for j in range(iteration):


print("first generation swarm position:", swarm_particle)
#print("swarm velocity:", swarm_velocity)
print('first generation gbest_particle_position:', gbest_particle_position)
print('first generation fitness_of_each_particle:', fitness_of_each_particle)
print('first generation gbest fitness:', fitness_of_gbest_particle)







