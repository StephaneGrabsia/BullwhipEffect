import actors
import random

def constant_demand(x):
    x = random.random()
    if x < 0.01:
        return 3
    elif 0.01 <= x <0.02:
        return 5
    else:
        return 4


retailer = actors.Agent("retailer")
wholesaler = actors.Agent("wholesaler")
distributor = actors.Agent("distributor")
factory = actors.Agent("factory", command_delay=1, desired_security_inventory=8)

game = actors.Game([retailer, wholesaler, distributor, factory], constant_demand)

game.display()


while game.timestep < 10000:
    if game.timestep > 9950: 
        game.display()
    game.play()
    print(factory.desired_security_inventory)


print(game.global_cost)
game.calculate_variability(10000)
fig, axs = game.plot_orders_made()