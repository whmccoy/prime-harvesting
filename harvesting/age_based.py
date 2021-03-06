from .abc import HarvestingStrategy
from decimal import Decimal
import math

class AgeBased(HarvestingStrategy):
    def __init__(self, portfolio, n, starting_age=65):
        """ n: This is the number you subtract the age from. 120 - age, 100 - age, and so on. """
        super().__init__(portfolio)
        self.n = n
        self.age = starting_age

    def get_stock_pct(self):
        return Decimal(self.n - self.age) / 100

    def do_harvest(self, amount):
        # first generate some cash
        self.portfolio.sell_stocks(self.portfolio.stocks)
        self.portfolio.sell_bonds(self.portfolio.bonds)

        # We can only take out however much is actually left in the portfolio
        actual_amount = min(self.portfolio.value, amount)

        new_val = self.portfolio.value - actual_amount
        if new_val > 0:
            self.portfolio.buy_stocks(new_val * self.get_stock_pct())
            self.portfolio.buy_bonds(self.portfolio.cash - actual_amount)

        self.age += 1

class AgeBased_100(AgeBased):
    def __init__(self, portfolio):
        super().__init__(portfolio, 100)

class AgeBased_110(AgeBased):
    def __init__(self, portfolio):
        super().__init__(portfolio, 110)

class AgeBased_120(AgeBased):
    def __init__(self, portfolio):
        super().__init__(portfolio, 120)

class Glidepath(AgeBased):
    def __init__(self, portfolio):
        super().__init__(portfolio, 100)

    def get_stock_pct(self):
        n = max(10, self.n - self.age)
        n = math.log(n, 10)
        return Decimal(n - 1)

class InverseGlidepath(AgeBased):
    def __init__(self, portfolio):
        super().__init__(portfolio, 100)

    def get_stock_pct(self):
        n = max(10, self.n - self.age)
        n = math.log(n, 10)
        bond_pct = Decimal(n - 1)
        return 1 - bond_pct
