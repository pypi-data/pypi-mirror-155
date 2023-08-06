import numpy as np

from runner.action.set.variable import Variable


class Continuous(Variable):
    """Continuous variable

        low <= variable < high

        Args:
            low (float): low boundary
            high (float): high boundary
            route (str): route to value (see Action)
    """

    def __init__(self, low=0.0, high=1.0, route='.~~', **kwargs):
        super().__init__(**kwargs)
        self.low = low
        self.high = high
        self.route = route

    def post_call(self, *args, **kwargs):
        self.set(self.route, np.random.uniform(self.low, self.high))
