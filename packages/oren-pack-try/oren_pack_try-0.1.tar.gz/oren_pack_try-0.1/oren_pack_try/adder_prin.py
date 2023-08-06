from .adder import plus

class prints(plus):   
    def __init__(self,plus=0):
        self.res = 4 + plus
        print('this is res: {}'.format(self.res))