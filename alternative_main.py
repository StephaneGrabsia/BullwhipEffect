import shared_knowledge_actors
import random
import numpy as np

def binomial_demand(x):
    return(np.random.binomial(10, 0.5))

def constant_demand(x):
    if x < 10:
        return 4
    else:
        return 8


retailer = shared_knowledge_actors.Agent("retailer")
wholesaler = shared_knowledge_actors.Agent("wholesaler")
distributor = shared_knowledge_actors.Agent("distributor")
factory = shared_knowledge_actors.Agent("factory", command_delay=1, desired_security_inventory=8)

game = shared_knowledge_actors.Game([retailer, wholesaler, distributor, factory], binomial_demand)

game.display()


while game.timestep < 30:
    game.display()
    game.play()
    print(factory.desired_security_inventory)


print(game.global_cost)
game.calculate_variability(100)
fig, axs = game.plot_orders_made()
