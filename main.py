import actors

def constant_demand(x):
    return 4

retailer = actors.Agent("retailer")
wholesaler = actors.Agent("wholesaler")
distributor = actors.Agent("distributor")
factory = actors.Agent("factory", command_delay = 1, desired_security_inventory=12)

game = actors.Game([retailer, wholesaler, distributor, factory], constant_demand)

game.display()


while game.timestep < 20:
    game.play()
    game.display()

print(game.global_cost)