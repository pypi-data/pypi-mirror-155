class Boundaries:

    def __init__(self, lower_bound=None, upper_bound=None, is_date=None):
        if is_date or is_date is None:
            self.lower_bound = lower_bound
            self.upper_bound = upper_bound
        else:
            self.lower_bound = int(lower_bound)
            self.upper_bound = int(upper_bound)
        self.is_date = is_date

    def exists(self):
        return self.lower_bound or self.upper_bound
