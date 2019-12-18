# @author: 1173710217_侯鹏钰, 1173710132_牟虹霖, 1173300919史纪元
# @time: 2019/12/16

from random import choice

class Monkey_System(object):
    def __init__(self):
        # random.seed()
        self.__location_set = ['a','b','c']
        self.monkey_loc = choice(self.__location_set)
        self.banana_loc = choice(self.__location_set)
        self.box_loc = choice(self.__location_set)
        self.get_banana = False
        self.on_box = False
        self.movement = []
        self.insert_movement()
    
    def insert_movement(self):
        self.movement.append((self.monkey_loc, self.banana_loc, self.box_loc, self.get_banana, self.on_box))

    def check_exit(self):
        if self.monkey_loc == self.banana_loc and self.box_loc == self.monkey_loc \
             and self.get_banana == True and self.on_box == True:
            return True
        return False
    
    def next(self):
        # rule_set
        # move monkey to box
        if self.monkey_loc != self.box_loc \
            and self.get_banana == False and self.on_box == False:
            self.monkey_loc = self.box_loc
            self.insert_movement()
            return

        # move monkey and box to banana
        if self.monkey_loc == self.box_loc and self.monkey_loc != self.banana_loc \
            and self.get_banana == False and self.on_box == False:
            self.monkey_loc = self.banana_loc
            self.box_loc = self.banana_loc
            self.insert_movement()
            return

        # monkey get on box
        if self.monkey_loc == self.box_loc and self.monkey_loc == self.banana_loc \
            and self.get_banana == False and self.on_box == False:
            self.on_box = True
            self.insert_movement()
            return
        
        # get banana
        if self.monkey_loc == self.box_loc and self.monkey_loc == self.banana_loc \
            and self.get_banana == False and self.on_box == True:
            self.get_banana = True
            self.insert_movement()
            return
        
        raise RuntimeError('out of rule set!!!')
    
    def print_trace(self):
        print("(Monkey_Location, Banana_Location, Box_Location, get_banana, on_box)")
        for state in self.movement:
            print(state)

if __name__ == "__main__":
    system = Monkey_System()
    while not system.check_exit():
        system.next()
    system.print_trace()