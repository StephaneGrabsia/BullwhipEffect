import actors_bis
import random
import numpy as np
import matplotlib.pyplot as plt

def binomial_demand(x):
    return(np.random.binomial(8, 0.5))

def uniform_demand(x):
    return(np.random.randint(0,9))

def constant_demand(x):
    n = np.random.random()
    if n < 0.90 : 
        return 4
    else:
        if n<0.95:
            return 3
        else:
            return 5


retailer = actors_bis.Agent("retailer")
wholesaler = actors_bis.Agent("wholesaler")
distributor = actors_bis.Agent("distributor")
factory = actors_bis.Agent("factory", command_delay=1, desired_security_inventory=8)

game = actors_bis.Game([retailer, wholesaler, distributor, factory], constant_demand)

game.display()


while game.timestep < 50:
    game.display()
    game.play()
    print(factory.desired_security_inventory)


print(game.global_cost)
game.calculate_variability(50)
fig, axs = game.plot_orders_made(10)
fig2, axs2 = game.plot_stocks(10)

def find_k():
    costs = []
    for k in np.linspace(-5,5,21):
        mean_cost = 0
        for i in range(25):
            retailer = actors_bis.Agent("retailer", stock_constant=k)
            wholesaler = actors_bis.Agent("wholesaler", stock_constant=k)
            distributor = actors_bis.Agent("distributor", stock_constant=k)
            factory = actors_bis.Agent("factory", command_delay=1, desired_security_inventory=8, stock_constant=k)

            game = actors_bis.Game([retailer, wholesaler, distributor, factory], constant_demand)
            while game.timestep < 200:
                game.play()
            mean_cost += game.global_cost
        costs.append(mean_cost/50)
    plt.plot(np.linspace(-5,5,21), costs)
    plt.show()