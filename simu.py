# Author: stephan.manuel@posteo.de
# Requirements:
# 1) The simu shall provide a two-dimensional matrix structure that serves as 'environment'
# 2) The simu shall be able to print the environment whenever needed
# 3) The environment matrix shall be able to represent different states
# 4) The simu shall be able to interface with a agent
# 5) The simu shall provide performance metrics about an agents efficency
# 6) The simu shall be able to initialize itself with random but senseful values
# 7) The matrix shall contain 3 states:
#           a) Wall represented by the integer -1 - the wall is made out of concrete without doors and the agent is not able to pass walls
#           b) clean floor represented by the integer 0 - the robot can move on this floor, it is already cleaned, it can be cleaned by the robot, however it will have no effect
#           c) dirty floor represented by the integer 1 - the robot can move on this floor, it is dirty and can be cleaned by the robot by the action 'suck_dirt'
from numpy import matrix
from pandas import *
import time
import sys
from termcolor import colored


class Simu:
    """ simulation for vaccum cleaner robot """
    def __init__(self,environment,robot,robot_postion,enable_console_output):

        self.enable_console_output = enable_console_output
        self.robot = robot

        self.environment_layer = environment
        self.robot_layer = environment.copy()

        self.update_robot_position(robot_postion)

        # definitions for performance measure
        self.move_energy_cost = 1 # moving (no matter if up, down, left or right will cost the agent 1 energy point)
        self.suck_dirt_energy_cost = 3 # sucking dirt from the floor costs the agent an 3 energy points
        self.move_time_cost = 1 # moving (no matter if up, down, left or right) will cost the agent one time point
        self.suck_time_cost = 1 # sucking dirt from the floor will cost the agent one time point

        self.total_energy_cost = 0
        self.total_time_cost = 0

        # simulation settings
        self.max_iterations = 5000
        self.current_iteration = 0

    def senseDustResponse(self):
        current_robot_coordinates = self.give_current_robot_coordinates()
        #print current_robot_coordinates
        if self.environment_layer[current_robot_coordinates[0],current_robot_coordinates[1]] == 1:
            return True
        return False

    def is_there_still_dirt(self):
        zeilenZahl =  np.size(self.environment_layer,0)
        spaltenZahl =  np.size(self.environment_layer,1)
        for zeilennummer in range(0,zeilenZahl):
            for spaltennummer in range(0,spaltenZahl):
                if self.environment_layer[zeilennummer,spaltennummer] == 1:
                    return True
        return False

    def print_current_environment(self):
        print "environment layer"
        print DataFrame(self.environment_layer)

    def print_current_robot_layer(self):
        print "robot layer"
        print DataFrame(self.robot_layer)

    def print_environment_and_robot(self):
        zeilenZahl =  np.size(self.environment_layer,0)
        spaltenZahl =  np.size(self.environment_layer,1)
        for zeilennummer in range(0,zeilenZahl):
            for spaltennummer in range(0,spaltenZahl):
                if self.environment_layer[zeilennummer,spaltennummer] == -1:
                    if ((zeilennummer == 0 ) or (zeilennummer == zeilenZahl-1)):
                        sys.stdout.write( colored("-",'cyan') )
                    else:
                        sys.stdout.write( colored("|",'cyan') )
                else:
                    if (self.robot_layer[zeilennummer,spaltennummer] == 1):
                        sys.stdout.write( colored('A','red') )
                    else:
                        sys.stdout.write( str(self.environment_layer[zeilennummer,spaltennummer]) )

            print ""


    def give_current_robot_coordinates(self):
        zeilenZahl =  np.size(self.robot_layer,0)
        spaltenZahl =  np.size(self.robot_layer,1)
        for zeilennummer in range(0,zeilenZahl):
            for spaltennummer in range(0,spaltenZahl):
                if self.robot_layer[zeilennummer,spaltennummer] == 1:
                    return [zeilennummer,spaltennummer]
        return [-1,-1]

    #[left,right,up,down]
    def give_sense_surrounding_response(self):
        current_robot_coordinates = self.give_current_robot_coordinates()
        #print current_robot_coordinates
        z = current_robot_coordinates[0]
        s = current_robot_coordinates[1]
        #print self.environment_layer[z,s]
        #print "left: ",self.environment_layer[z,(s-1)]
        #print "right: ",self.environment_layer[z,(s+1)]
        #print "up: ",self.environment_layer[(z-1),s]
        #print "down: ", self.environment_layer[(z+1),s]
        return [self.environment_layer[z,(s-1)],self.environment_layer[z,(s+1)],self.environment_layer[(z-1),s],self.environment_layer[(z+1),s]]

    def update_robot_position(self,position):
        zeilenZahl =  np.size(self.environment_layer,0)
        spaltenZahl =  np.size(self.environment_layer,1)
        for zeilennummer in range(0,zeilenZahl):
            for spaltennummer in range(0,spaltenZahl):
                self.robot_layer[zeilennummer,spaltennummer] = 0
        self.robot_layer[position[0],position[1]] = 1

    def update_environment_layer_status(self,position,status):
        self.environment_layer[position[0],position[1]] = 0

    def suck(self):
        self.total_energy_cost += self.suck_dirt_energy_cost
        self.total_time_cost += self.suck_time_cost
        self.update_environment_layer_status(self.give_current_robot_coordinates(),0)

    def attempt_to_move(self,direction):
        self.total_energy_cost += self.move_energy_cost
        self.total_time_cost += self.move_time_cost
        current_robot_coordinates = self.give_current_robot_coordinates()
        if direction == "up":
            attempted_future_robot_coordinates = [(current_robot_coordinates[0]-1),current_robot_coordinates[1]]
        if direction == "down":
            attempted_future_robot_coordinates = [(current_robot_coordinates[0]+1),current_robot_coordinates[1]]
        if direction == "left":
            attempted_future_robot_coordinates = [current_robot_coordinates[0],(current_robot_coordinates[1]-1)]
        if direction == "right":
            attempted_future_robot_coordinates = [current_robot_coordinates[0],(current_robot_coordinates[1]+1)]
        #print self.environment_layer[attempted_future_robot_coordinates[0],attempted_future_robot_coordinates[1]]
        if not (self.environment_layer[attempted_future_robot_coordinates[0],attempted_future_robot_coordinates[1]] == -1): # is the agent trying to move trough a wall?
            self.update_robot_position(attempted_future_robot_coordinates)
            return True
        return False

    def run(self,iterations, update_time_seconds):
        for iteration in range(0,iterations):
            self.robot.operate(self)

            if self.enable_console_output:
                print "Iteration: ", iteration
                self.print_environment_and_robot()
            #self.print_current_robot_layer()
            #self.print_current_environment()
            if not self.is_there_still_dirt():
                break
            time.sleep(update_time_seconds)


    def give_total_energy_cost(self):
        return self.total_energy_cost

    def give_total_time_cost(self):
        return self.total_time_cost

    def print_statistics(self):
        print "AI - agent succeded!"
        print ""
        print "    '._==_==_=_.'"
        print "    .-\:      /-."
        print "   | (|:.     |) |"
        print "    '-|:.     |-'"
        print "      \::.    /"
        print "       '::. .'"
        print "         ) ("
        print "       _.' '._"
        print "     `\"\"\"\"\"\"\"`\" "
        print "Agent: ", self.robot.giveName()
        print "Total energy cost: ",self.total_energy_cost
        print "Total time cost: ",self.total_time_cost
