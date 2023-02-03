
class Interval:
    INF = -1
    interval: list

    def __init__(self):
        self.interval = [0, 0, 0, 0]

    def compareLeft(self, arg, func=None):
        # Return True if arg is larger or equal, cases depends.
        pass

    def compareRight(self, arg, func=None):
        # Return True if arg is smaller or equal, cases depends.
        pass

    def query_in_list(self, arg: list):
        pass

    def query_in_number(self, arg, func=None):
        retv = False
        a = self.compareLeft(arg, func)
        b = self.compareRight(arg, func)
        if a==True and b==True:
            retv = True
        return retv

    def query_in_Interval(self, arg):
        pass


