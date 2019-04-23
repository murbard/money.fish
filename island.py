import random
import math
import numpy as np


class Order(object):
    def __init__(self, villager, shells):
        """
        Create an order where a given villager offers or requests a certain
        number of shells for a fish.
        :param villager: the villager
        :param shells: negative to buy fish, positive to sell
        """
        assert type(shells) is int
        assert isinstance(villager, Villager)
        self.villager = villager
        self.shells = shells
        self.rnd = random.random()


class OrderBook(object):
    """
    Create an empty order book
    """
    def __init__(self):
        self.orders = []

    def add_order(self, order):
        """
        Inserts an order into the order book
        """
        assert isinstance(order, Order)
        self.orders.append(order)

    def clear(self):
        """
        Market clearing to maximize volume traded
        """

        # Buys are indicated by a negative amount of shells
        # (the villager ends up with fewer shells).
        # Conversely sells are indicated with a positive amount of shells

        buys = sorted([(o.shells, o.rnd, o) for o in self.orders if o.shells <= 0])
        sells = sorted([(o.shells, o.rnd, o) for o in self.orders if o.shells > 0])

        # determining the crossing point
        q = 0
        buy_sells = list(zip(buys, sells))
        while q < len(buy_sells):
            (b, b_rnd, b_o), (s, s_rnd, s_o) = buy_sells[q]
            if (-b) <= s:
                break
            q = q + 1
        if q:
            price: int = (-buys[q - 1][0]) + sells[q - 1][0]
            # flip a coin to determine clearing price
            if price % 2 != 0:
                price = price + 2 * random.randint(0, 1) - 1
            price = price / 2
        else:
            price = None
        self.orders = []
        return [b[2] for b in buys[:q]], [b[2] for b in sells[:q]], price


class Villager(object):

    def __init__(self, name, shells=1000):
        """
        Create a villager, endow them with 1000 shells by default.
        """
        self.name = name
        self.shells = shells
        self.fish = 0
        self.available_fish = 0
        self.available_shells = shells


class Island(object):
    """
    General class representing an Island, its villagers, order book, etc.
    """

    def __init__(self):
        self.order_book = OrderBook()
        self.villagers = {}
        self.started = False

        # stochastic parameter for quantity of fish fished
        self.mu, self.kappa, self.sigma = 0.03, 0.99, 0.012
        self.theta = random.normalvariate(self.mu, self.sigma / np.sqrt(1.0 - self.kappa ** 2))
        self.day = 0
        self.last_price = None
        self.last_quantity = None

    def register_villager(self, name):
        if name in self.villagers:
            return False
        else:
            self.villagers[name] = Villager(name)
            return True

    def get_fish(self, name):
        return self.villagers[name].fish if name in self.villagers else None

    def get_shells(self, name):
        return self.villagers[name].shells if name in self.villagers else None

    def place_order(self, name, shells):
        try:

            villager = self.villagers[name]
            print('trying... %d' % villager.available_fish)
            if shells > 0:
                assert villager.available_fish > 0
                villager.available_fish -= 1
            else:
                assert villager.available_shells >= - shells
                villager.available_shells -= (-shells)
            order = Order(villager, shells)
            self.order_book.add_order(order)
            return True
        except Exception as e:
            print(e)
            return False

    def morning(self):
        print("It's morning!", self.villagers)
        for villager in self.villagers.values():
            u = random.random()
            print(u, math.exp(-np.exp(self.theta)))
            while u < 1.0 - math.exp(-np.exp(self.theta)):
                villager.fish += 1
                u = random.random()
            villager.available_fish = villager.fish
            print("%s has %d fish" % (villager.name, villager.fish))

    def evening(self):
        print("It's evening!")
        # trade
        (buys, sells, price) = self.order_book.clear()
        assert len(buys) == len(sells)

        self.last_quantity = len(buys)
        self.last_price = price

        for villager in buys:
            villager.fish += 1
            villager.shells -= price
        for villager in sells:
            villager.fish -= 1
            villager.shells += price

        # eat or leave
        self.villagers = {name: villager for name, villager in self.villagers.items()
                          if villager.fish >= 2}

        # fish rots
        for villager in self.villagers.values():
            villager.fish = 0
            villager.available_shells = villager.shells

        # update fish frequency
        self.theta = random.normalvariate(self.mu + self.kappa * (self.theta - self.mu), self.sigma)
        self.day += 1
