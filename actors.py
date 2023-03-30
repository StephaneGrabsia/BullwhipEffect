class Client():
    """
    A client is just a timest
    """
    def __init__(self, demand_law):
        self.timestep = 1
        self.demand_law = demand_law
        self.sent_demand = 0
    
    def act(self):
        self.sent_demand = self.demand_law(self.timestep)
        self.timestep += 1

class Agent():
    """
    An agent is one actor of the supply chain
    """
    def __init__(self, name, command_delay, reception_delay):
        self.name = name
        self.timestep = 1
        self.inventory = 0
        self.sent_commands = [0] * command_delay
        self.command_to_be_received = [0] * reception_delay
        self.backlog = 0
        self.expected_order = 0
        self.alpha = 1
        self.beta = 1

    def __str__(self):
        return f"Actor {self.name} at timestep {self.timestep} - Inventory : {self.invetory}; Backlog : {self.backlog}; Command sent : {self.sent_commands[0]} | {self.sent_commands[1]} ; Supply line : {self.command_to_be_received[0]} | {self.command_to_be_received[1]}"
    
    def cost(self):
        """
        
        """

    def behoviour(self):
        """
        Return a command depending on the expected order, inventory, and parameters
        """
    def act(self):
        """
        Act at a time step : 
        - Receive a command
        - Receive an order
        - Send something in response to that order and update invetory
        - Send another command to the next actor
        """