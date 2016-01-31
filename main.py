#!/usr/bin/python

import g_interpreter          
  
#Setup game controller class, initialize its variables, and start the game
game=g_interpreter.controller()
game.var_reset()
print("You awake to find yourself in a dimly lit room!\nWhat will you do?\nFor a list of commands, type HELP.")
while (True):
    testinput=input()
    n=game.user_interpret(testinput)
    if (n>0):
        break

print("DEBUG: Program succesfully terminated.")
