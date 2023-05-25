import actors
import random
import numpy as np

def binomial_demand(x):
    return(np.random.binomial(10, 0.5))


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
