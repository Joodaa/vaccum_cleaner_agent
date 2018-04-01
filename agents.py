# Author: Manuel Stephan

from random import randint

class BasicAgent:
    """ The basic agent is a very simple version of a reflex agent
        It can however be specialized and new functionality can be added to the BasicAgent
        in order to give the agent intelligent behavior
    """
    def __init__(self,name):
        self.current_state = "chose_direction"
        self.map_int_to_direction = ["left","right","up","down"]
        self.current_direction = "up"
        self.name = name

    def giveName(self):
        return self.name

    def chose_direction(self):
        return self.map_int_to_direction[randint(0,3)]

    def move(self,environment):
        return environment.attempt_to_move(self.current_direction)

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



class DustPerceptWallMemAgent(BasicAgent):
    """
    The Agent is able to:
        - preceive Dust
        - memorize if it drove against a wall and chose not to do it again
    """
    def __init__(self,name):
        BasicAgent.__init__(self,name)
        self.last_direction = "none"
        self.last_move_success = True

    def senseDust(self,environment):
            return environment.senseDustResponse()

    def operate(self,environment):
        if self.current_state == "chose_direction":
            self.last_direction = self.current_direction
            while(True):
                self.current_direction = self.chose_direction()
                if not( (self.last_move_success == False) and (self.last_direction == self.current_direction)):
                    break
            self.current_state = "move"
            return
        if self.current_state == "move":
            self.last_move_success = self.move(environment)
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





class RepeatMovementSuccessAgent(BasicAgent):
    """
    The Agent is able to:
        - preceive Dust
        - memorize if it was able to move in one direction and then will try to repeat the successful move
    """
    def __init__(self,name):
        BasicAgent.__init__(self,name)
        self.last_direction = self.chose_direction()
        self.last_move_success = True

    def senseDust(self,environment):
            return environment.senseDustResponse()

    def operate(self,environment):
        if self.current_state == "chose_direction":
            self.last_direction = self.current_direction
            if self.last_move_success == True:
                self.current_direction = self.last_direction
            else:
                self.current_direction = self.chose_direction()
            self.current_state = "move"
            return
        if self.current_state == "move":
            self.last_move_success = self.move(environment)
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




class FullSenseAgent(BasicAgent):
    """
    The Agent is able to:
        - preceive dust, on its current position
        - perceive walls, floor and dust arround it
        - plan its actions towards its goal (clean environment)
    """
    def __init__(self,name):
        BasicAgent.__init__(self,name)
        self.last_direction = self.chose_direction()
        self.last_move_success = True
        self.current_state = "senseDust"
        self.environmentPercepts = [None,None,None,None]

    def senseDust(self,environment):
        return environment.senseDustResponse()

    def senseEnvironment(self, environment):
        return environment.give_sense_surrounding_response()

    def operate(self,environment):
        #print self.current_state
        #print self.current_direction
        if self.current_state == "chose_direction":
            self.current_state = "move"
            int_direction = 0
            #print "environment percepts",self.environmentPercepts
            for percept in self.environmentPercepts:
                if percept == 1:
                    self.current_direction = self.map_int_to_direction[int_direction]
                    return
                int_direction += 1
            self.current_direction = self.chose_direction()
            return
        if self.current_state == "move":
            self.last_move_success = self.move(environment)
            self.current_state = "senseDust"
            return
        if self.current_state == "senseDust":
            if self.senseDust(environment):
                self.current_state = "suck"
            else:
                self.current_state = "senseEnvironment"
            return
        if self.current_state == "senseEnvironment":
            self.environmentPercepts = self.senseEnvironment(environment)
            #print self.environmentPercepts
            self.current_state = "chose_direction"
            return

        if self.current_state == "suck":
            self.suck(environment)
            self.current_state = "senseEnvironment"
            return
