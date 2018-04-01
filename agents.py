# Author: Manuel Stephan

from random import randint

class BasicAgent:
    """ The basic agent is a very simple version of a reflex agent
        It can however be specialized and new functionality can be added to the BasicAgent
        in order to give the agent intelligent behavior
    """
    def __init__(self,name):
        self.current_state = "chose_direction"
        self.map_int_to_direction = ["up","down","left","right"]
        self.current_direction = "none"
        self.name = name

    def giveName(self):
        return self.name

    def chose_direction(self):
        return self.map_int_to_direction[randint(0,3)]

    def move(self,environment):
        environment.attempt_to_move(self.current_direction)

    def suck(self,environment):
        environment.suck()

    # operate is the function called by the simulation environment
    # it is granular, on each call, one atomic action of the robot is executed
    def operate(self, environment):
        #print self.current_state
        #print self.current_direction
        if self.current_state == "chose_direction":
            self.current_direction = self.chose_direction()
            self.current_state = "move"
            return
        if self.current_state == "move":
            self.move(environment)
            self.current_state = "suck"
            return
        if self.current_state == "suck":
            self.suck(environment)
            self.current_state = "chose_direction"
            return

class DustPerceptAgent(BasicAgent):
    """
    The DustPerceptAgent is able to perceive dust in the environment in order to
    save energy it will only execute the operation suck when it perceives dust via its dust sensor
    """
    def __init__(self,name):
        BasicAgent.__init__(self,name)

    def senseDust(self,environment):
            return environment.senseDustResponse()

    def operate(self,environment):
        if self.current_state == "chose_direction":
            self.current_direction = self.chose_direction()
            self.current_state = "move"
            return
        if self.current_state == "move":
            self.move(environment)
            self.current_state = "senseDust"
            return
        if self.current_state == "senseDust":
            if self.senseDust(environment):
                self.current_state = "suck"
            else:
                self.current_state = "chose_direction"
            return
        if self.current_state == "suck":
            self.suck(environment)
            self.current_state = "chose_direction"
            return
