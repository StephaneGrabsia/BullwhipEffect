import numpy as np


class Client:
    """
    A client is just a random variable
    """

    def __init__(self, demand_law):
        self.demand_law = demand_law
        self.sent_demand = demand_law(0)

    def act(self, timestep):
        self.sent_demand = self.demand_law(timestep)


class Agent:
    """
    An agent is one actor of the supply chain
    """

    def __init__(
        self,
        name,
        command_delay=2,
        reception_delay=2,
        desired_security_inventory=16,
        desired_coordination_inventory=0,
        theta=1,
    ):
        self.name = name
        self.inventory = 12
        self.command_delay = command_delay
        self.reception_delay = reception_delay
        self.received_shipments = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        self.received_orders = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        self.sent_orders = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        self.sent_shipments = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        self.backlog = 0
        self.expected_order = 0
        self.alpha = 1
        self.beta = 1
        self.theta = theta
        self.desired_security_inventory = desired_security_inventory
        self.desired_coordination_inventory = desired_coordination_inventory

    def __str__(self):
        return f"Actor {self.name} at timestep {self.timestep} - Inventory : {self.inventory}; Backlog : {self.backlog}; Command sent : {self.sent_commands} ; Supply line : {self.sent_orders}"

    def update_desired_security_stock(self, timeslot=10):
        """
        Function using the formula from "Le vendeur de journaux"
        """

        cs = 0.5
        cm = 1
        Flim = cm / (cm + cs)
        if len(self.received_orders) > timeslot:
            empirical_demand = self.received_orders[-timeslot:]
        else:
            empirical_demand = self.received_orders
        F = np.zeros(max(empirical_demand) + 1)
        desired_security_stock = 0
        for i in range(0, max(empirical_demand) + 1):
            F[i] = (
                sum([1 for xi in empirical_demand if xi <= i]) / 10
            )  # fonction de répartition
            if F[i] >= Flim:
                desired_security_stock = i
                break
        self.desired_security_inventory = (desired_security_stock + (self.reception_delay + self.command_delay - 1) * int(np.mean(empirical_demand)))

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
        supply_line = np.sum(
            self.sent_orders[-(self.command_delay + self.reception_delay) :]
        )
        on_hand_inventory = self.inventory - self.backlog
        return max(
            0,
            self.expected_order
            + self.alpha
            * (desired_inventory - on_hand_inventory - self.beta * supply_line),
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

        self.update_desired_security_stock()
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
                self.backlog -= sent_shipment - received_order
            else:
                sent_shipment = received_order
        else:
            sent_shipment = self.inventory
            self.backlog += received_order - self.inventory

        # Update inventory
        self.inventory -= sent_shipment
        self.sent_shipments.append(sent_shipment)

        self.predict(order_made_by_previous_actor)
        new_order = self.behaviour()
        self.sent_orders.append(new_order)


class Game:
    """
    Pricipal class of the game, contains the series of actor
    """

    def __init__(self, list_of_actors, demand_law):
        self.timestep = 1
        self.list_of_actors = list_of_actors
        self.global_cost = 0
        self.client = Client(demand_law)

    def display(self):
        """
        TO DO : Create a beautiful displaying function
        """

        print("{: ^120}".format("Etat du jeu au timestep " + str(self.timestep)))
        print("=" * 120)

        # 1ere ligne
        print("|{: ^12}".format("Client:"), end="")
        for j in range(len(self.list_of_actors)):
            print("|{: ^13}".format(self.list_of_actors[j].name), end="")
            print("|{: ^12}".format("->"), end="")
        print("|")

        # 2eme ligne:
        print("|{: ^12}".format(" "), end="")
        for j in range(len(self.list_of_actors)):
            print("|{: ^13}".format("Inventory:"), end="")
            sent_orders = (
                self.list_of_actors[j]
                .sent_orders[-self.list_of_actors[j].command_delay :]
                .copy()
            )
            sent_orders.reverse()
            str_orders = "  ".join([str(el) for el in sent_orders])
            print("|{: ^12}".format(str_orders), end="")
        print("|")

        # 3eme ligne
        print("|{: ^12}".format(self.client.sent_demand), end="")
        for j in range(len(self.list_of_actors)):
            print("|{: ^13}".format(self.list_of_actors[j].inventory), end="")
            print("|{: ^12}".format(" "), end="")
        print("|")

        # 4eme ligne
        print("|{: ^12}".format("Total cost:"), end="")
        for j in range(len(self.list_of_actors)):
            print("|{: ^13}".format("Backlog :"), end="")
            print("|{: ^12}".format("<-"), end="")
        print("|")

        # 5eme ligne
        print("|{: ^12}".format(self.global_cost), end="")
        for j in range(len(self.list_of_actors)):
            print("|{: ^13}".format(self.list_of_actors[j].backlog), end="")
            if j != (len(self.list_of_actors) - 1):
                shipments_in_transit = self.list_of_actors[j + 1].sent_shipments[
                    -self.list_of_actors[j].reception_delay :
                ]
            else:
                shipments_in_transit = self.list_of_actors[j].sent_orders[
                    -(
                        self.list_of_actors[j].command_delay
                        + self.list_of_actors[j].reception_delay
                    ) : -self.list_of_actors[j].command_delay
                ]
            str_shipments = "  ".join([str(el) for el in shipments_in_transit])
            print("|{: ^12}".format(str_shipments), end="")
        print("|")

    def play(self):
        # First step : The client asks for some beer
        self.client.act(self.timestep)

        received_orders_at_each_step = [
            actor.sent_orders[-actor.command_delay] for actor in self.list_of_actors
        ]
        received_shipment_at_each_step = [
            actor.sent_shipments[-actor.reception_delay]
            for actor in self.list_of_actors
        ]

        for i in range(len(self.list_of_actors)):
            current_actor = self.list_of_actors[i]
            if i == 0:
                # If it's the first actor, then the precedent_actor is the client
                received_order = self.client.sent_demand

            else:
                received_order = received_orders_at_each_step[i - 1]

            if i == (len(self.list_of_actors) - 1):
                # If it's the last actor, then the next actor is the factory
                # So the receive shipments equals to the order sent 3 weeks ago

                actor = self.list_of_actors[i]
                received_shipment = actor.sent_orders[
                    -(actor.command_delay + actor.reception_delay)
                ]
            else:
                # If it's not the last, the received shipment corresponds to the shipment sent
                # by the next actor two weeks ago
                received_shipment = received_shipment_at_each_step[i + 1]

            current_actor.act(received_order, received_shipment)
            self.global_cost += current_actor.cost()

        self.timestep += 1

    def calculate_variability(self, timeslot):
        print("Client demand standard deviation :")
        var = np.std(self.list_of_actors[0].received_orders[-timeslot:])
        print(var)
        for agent in self.list_of_actors:
            print("Agent :" + agent.name + "has a standard deviation of:")
            var = np.std(agent.sent_orders[-timeslot:])
            print(var)
