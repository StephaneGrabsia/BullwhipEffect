import numpy as np


class Client:
    """
    A client is just a random variable
    """

    def __init__(self, demand_law):
        self.timestep = 1
        self.demand_law = demand_law
        self.sent_demand = 0

    def act(self):
        self.sent_demand = self.demand_law(self.timestep)
        self.timestep += 1


class Agent:
    """
    An agent is one actor of the supply chain
    """

    def __init__(
        self,
        name,
        command_delay=2,
        reception_delay=2,
        desired_security_inventory=12,
        desired_coordination_inventory=0,
        theta=1,
    ):
        self.name = name
        self.timestep = 1
        self.inventory = 0
        self.command_delay = command_delay
        self.reception_delay = reception_delay
        self.received_shipments = [0, 0, 0, 0]
        self.received_orders = [0, 0, 0, 0]
        self.sent_orders = [0, 0, 0, 0]
        self.backlog = 0
        self.expected_order = 0
        self.alpha = 1
        self.beta = 1
        self.theta = theta
        self.desired_security_inventory = desired_security_inventory
        self.desired_coordination_inventory = desired_coordination_inventory

    def __str__(self):
        return f"Actor {self.name} at timestep {self.timestep} - Inventory : {self.inventory}; Backlog : {self.backlog}; Command sent : {self.sent_commands} ; Supply line : {self.sent_orders}"

    def update_desired_security_stock(self):
        """
        Function using the formula from "Le vendeur de journaux"
        """
        cs=0.5
        cm=1
        Flim=cm/(cm+cs)
        empirical_demand=[self.received_shipments[i] for i in range (len(self.received_shipments)-10,len(self.received_shipments))]
        desired_security_stock=0
        for i in range (0,max(empirical_demand)+1):
            F[i]=sum(1 for xi in empirical_demand if xi<=i)/10 # fonction de répartition
            if F[i]>=Flim:
                desired_security_stock=i
        return desired_security_stock
    def cost(self):
        """
        Calculate the cost caused by the stock and the inventory
        """

        return 0.5 * self.inventory + 1 * self.backlog

    def predict(self, last_order):
        """
        Function that update the estimation of expected_order,
        by using an adaptative formula, as mentionned in Croson
        """
        self.expected_order = (
            self.theta * last_order + (1 - self.theta) * self.expected_order
        )

    def behaviour(self):
        """
        Return a command depending on the expected order, inventory,
        and parameters
        """

        desired_inventory = (
            self.desired_coordination_inventory + self.desired_security_inventory
        )
        supply_line = np.sum(self.sent_orders[-(self.command_delay+self.reception_delay):])

        return max(
            0,
            self.expected_order
            + self.alpha
            * (desired_inventory - self.inventory - self.beta * supply_line),
        )

    def act(self, order_made_by_previous_actor, received_shipment):
        """
        Act at a time step :
        - Receive a shipment
        - Receive an order
        - Send something in response to that order and update invetory
        - Send another command to the next actor
        """

        # Receive a shipment and place it in the inventory:
        self.inventory += received_shipment
        self.received_shipments.append(received_shipment)

        # Receive the command of the previous actor
        received_order = order_made_by_previous_actor
        self.received_orders.append(order_made_by_previous_actor)

        # Answer this command:
        if self.inventory >= received_order:
            if (
                self.backlog > 0
            ):  # Si il y a du backlog, alors l'acteur a intéret a tenter de
                # le diminuer au max
                sent_shipment = min(self.inventory, received_order + self.backlog)
            else:
                sent_shipment = received_order
        else:
            sent_shipment = self.inventory

        # Update inventory
        self.inventory -= sent_shipment

        self.predict(order_made_by_previous_actor)
        new_order = self.behaviour()
        self.sent_orders.append(new_order)

        self.timestep += 1

