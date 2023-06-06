import actors
import random
import numpy as np
import matplotlib.pyplot as plt

def binomial_demand(x):
    return(np.random.binomial(8, 0.5))

def uniform_demand(x):
    return(np.random.randint(0,9))

def constant_demand(x):
    if x < 10:
        return 4
    else:
        return 8


retailer = actors.Agent("retailer")
wholesaler = actors.Agent("wholesaler")
distributor = actors.Agent("distributor")
factory = actors.Agent("factory", command_delay=1, desired_security_inventory=8)

game = actors.Game([retailer, wholesaler, distributor, factory], binomial_demand)

game.display()


while game.timestep < 100:
    game.display()
    game.play()
    print(factory.desired_security_inventory)


print(game.global_cost)
game.calculate_variability(100)
fig, axs = game.plot_orders_made()


def find_k():
    costs = []
    for k in np.linspace(-5,5,21):
        mean_cost = 0
        for i in range(25):
            retailer = actors.Agent("retailer", stock_constant=k)
            wholesaler = actors.Agent("wholesaler", stock_constant=k)
            distributor = actors.Agent("distributor", stock_constant=k)
            factory = actors.Agent("factory", command_delay=1, desired_security_inventory=8, stock_constant=k)

            game = actors.Game([retailer, wholesaler, distributor, factory], binomial_demand)
            while game.timestep < 200:
                game.play()
            mean_cost += game.global_cost
        costs.append(mean_cost/50)
    plt.plot(np.linspace(-5,5,21), costs)
    plt.show()