#!/usr/bin/python

import g_room
import json

class controller:
    def var_reset(self):
        self.u_roomid=0
        self.u_roomflags=[0,0,0,0,0,0,0] #base entries on number of rooms in g_room.py
        self.u_roomhistory=list()
        self.u_items=list()
        self.u_roomcurrent=g_room.dgn_room()
        self.u_roomcurrent.init_room(1)
        self.u_roomnext=g_room.dgn_room()
    def user_interpret(self,str_input):
        #Room 0 will be used to test if there a gameover (flag=1) 
        #and if the game needs to close (flag=2)
        self.u_roomflags[0]=0
        #len(str_input)>X for all inputs; otherwise ValueError will occur
        #Check the room/objects in the room function
        if (len(str_input)>=4 and (str_input[:4].upper()=="LOOK" or str_input[:4].upper()=="CHECK")):
            if (len(str_input)>4):
                #Is there an object in the room that can be checked?
                for i in range(0,len(self.u_roomcurrent.Obj)):
                    #Did the object match the string input?
                    if (str_input[5:].upper()==self.u_roomcurrent.Obj[i]):
                        #If so, print out the object's description.
                        print(self.u_roomcurrent.Desc[i])
                        if (self.u_roomcurrent.ID==2 and self.u_roomflags[2]==0):
                            #Special Case: Waking up the dragon in its lair
                            self.u_roomflags[2]=1
                            self.u_roomcurrent.update_room(2,1)
                            print(self.u_roomcurrent.Chk)
                            break
                        elif (self.u_roomcurrent.ID==5 and self.u_roomflags[5]!=1):
                            #Special Case: Solving the puzzle in the room "Puzzled"
                            temp_ans=int(input())
                            if (temp_ans!=50):
                                #Puzzle couldn't be solved; encourage player to try again
                                self.u_roomflags[5]=2
                                self.u_roomcurrent.update_room(5,2)
                                print(self.u_roomcurrent.Chk)
                                break
                            else:
                                #Puzzle was solved; give player the toy item
                                self.u_roomflags[5]=1
                                self.u_roomcurrent.update_room(5,1)
                                self.u_items.append("TOY") #New item in inventory that wasn't in world
                                print(self.u_roomcurrent.Chk)           
                                break
                    elif (self.u_roomflags[0]==0):
                        print("I'm not sure what I'm looking for...")
            else:
                #No object was specified, so print room name, description and objects
                print(self.u_roomcurrent.Name)
                print(self.u_roomcurrent.Chk)
                print("Potential exits are ",self.u_roomcurrent.Dir)
                print("Objects that can be found are ",self.u_roomcurrent.Obj)
        #Take an item from the room function
        elif (len(str_input)>=4 and (str_input[:4].upper()=="TAKE" or str_input[:3].upper()=="GET")):
            if (len(str_input)>4):                 
                temp_itemfind=0
                if (self.u_roomcurrent.ID==2):
                    if (self.u_roomflags[2]>0):
                        if (self.u_roomflags[2]==1 or self.u_roomflags[2]==3):
                            #Special Case: Annoying hungry dragon causes game over
                            self.u_roomflags[2]=5
                            self.u_roomcurrent.update_room(2,5)
                            print(self.u_roomcurrent.Chk)
                            self.u_roomflags[0]=1
                        elif (self.u_roomflags[2]==2):
                            #Special Case: Annoying bored dragon causes game over
                            self.u_roomflags[2]=6
                            self.u_roomcurrent.update_room(2,6)
                            print(self.u_roomcurrent.Chk)
                            self.u_roomflags[0]=1
                #Check all objects in the room
                for i in range(0,len(self.u_roomcurrent.Obj)):
                    #Did the object match the string input?
                    if (str_input[5:].upper()==self.u_roomcurrent.Obj[i] or str_input[4:].upper()==self.u_roomcurrent.Obj[i]):
                        temp_itemfind=1
                        if (self.u_roomcurrent.ID==6 and i==1):
                            #Although this is typically a general case, floor item pickup...
                            #Only occurs once in this scenario.
                            #Code below can be used in future cases if needed.
                            #Add item to inventory.
                            self.u_items.append(self.u_roomcurrent.Obj[i])
                            print("Added",self.u_roomcurrent.Obj[i],"to inventory.")
                            #Update the room so the object is not present.
                            self.u_roomflags[6]=2
                            self.u_roomcurrent.update_room(6,2)
                            break
                        elif (self.u_roomcurrent.ID==5 and self.u_roomflags[5]!=1):
                            #Special Case: Solving the puzzle in the room "Puzzled"
                            print(self.u_roomcurrent.Desc[0])
                            temp_ans=int(input())
                            if (temp_ans!=50):
                                #Puzzle couldn't be solved; encourage player to try again                                
                                self.u_roomflags[5]=2
                                self.u_roomcurrent.update_room(5,2)
                                print(self.u_roomcurrent.Chk)
                            else:
                                #Puzzle was solved; give player the toy item
                                self.u_roomflags[5]=1
                                self.u_roomcurrent.update_room(5,1)
                                self.u_items.append("TOY") #New item in inventory that wasn't in world
                                print(self.u_roomcurrent.Chk)
                        elif (self.u_roomcurrent.ID==3):
                            #Special Case: The Flask
                            self.u_roomflags[3]=1
                            self.u_roomcurrent.update_room(3,1)
                            #The player has won the game
                            print(self.u_roomcurrent.Chk)
                            self.u_roomflags[0]=1
                        else:
                            #Objects that cannot be picked up display the following
                            print("You try to take the",self.u_roomcurrent.Obj[i],"but cannot.")
                            if (self.u_roomcurrent.ID==2 and self.u_roomflags[2]==0):
                                #Special Case: Sleeping dragon wakes up
                                self.u_roomflags[2]=1
                                self.u_roomcurrent.update_room(2,1)
                                print(self.u_roomcurrent.Chk)
                            break
                if (temp_itemfind==0 and self.u_roomflags[0]==0): print("I couldn't find what you were trying to take.")
            elif (self.u_roomflags[0]==0):
                print("What am I supposed to take?")
        #Direction and room movement function
        elif (len(str_input)>=4 and (str_input[:5].upper()=="NORTH" or str_input[:5].upper()=="SOUTH" or str_input[:4].upper()=="EAST" or str_input[:4].upper()=="WEST")):
            temp_founddir=0            
            #Is it possible to move in the direction?            
            for i in range(0,len(self.u_roomcurrent.Dir)):    
                #If so, commence movement                
                if (str_input.upper()==self.u_roomcurrent.Dir[i]):
                    if (self.u_roomcurrent.ID==2):
                        if (self.u_roomflags[2]>0):
                            if (self.u_roomflags[2]==1 or self.u_roomflags[2]==3):
                                #Special Case: Dragon is awake and hungry; game over
                                self.u_roomflags[2]=5
                                self.u_roomcurrent.update_room(2,5)
                                print(self.u_roomcurrent.Chk)
                                self.u_roomflags[0]=1
                                break
                            elif (self.u_roomflags[2]==2):
                                #Special Case: Dragon is awake and bored; game over
                                self.u_roomflags[2]=6
                                self.u_roomcurrent.update_room(2,6)
                                print(self.u_roomcurrent.Chk)
                                self.u_roomflags[0]=1  
                                break
                            elif (self.u_roomflags[2]==4 and str_input.upper()=="NORTH"):
                                #Special Case: Usage of Key on locked door                             
                                #The Key should only be in slot 1 if it's not used already
                                if (len(self.u_items)>0 and self.u_items[0]=="KEY"): 
                                    self.u_items=[]
                                    print("You unlock the sealed door and travel onward!")                                
                        elif (str_input.upper()=="NORTH"): 
                            #Special Case: Dragon's Lair locked door without key
                            print("The door behind the DRAGON is locked!")
                            break
                    newroomid=self.u_roomcurrent.Rnx[i]
                    self.u_roomnext.init_room(newroomid)
                    #print("DEBUG: Initializing Room",newroomid)
                    #print("DEBUG: Moving to Room",newroomid)
                    self.u_roomcurrent=self.u_roomnext
                    temp_founddir=1
                    #Update any flags found in the new room to the current one            
                    if (self.u_roomflags[newroomid]!=0):
                        #print("DEBUG: Flag spotted")
                        self.u_roomcurrent.update_room(newroomid,self.u_roomflags[newroomid])
                    self.u_roomhistory.append(newroomid)
                    self.u_roomid=newroomid                    
                    #Print out new room description      
                    print(self.u_roomnext.Chk)
                    break
            if (temp_founddir==0): print("You ran into a wall.")
        #Item usage function
        elif (len(str_input)>=3 and str_input[:3].upper()=="USE"):
            if (len(str_input)>4):
                temp_haveitem=0
                #Is the item in the inventory?                
                for i in range(0,len(self.u_items)):
                    if (str_input[4:].upper()==self.u_items[i]):
                        temp_haveitem=1
                        if (str_input[4:].upper()=="MEAT"):
                            if (self.u_roomcurrent.ID!=2): print("You attempt to bite into the meat, but it's too rough...")
                            elif (self.u_roomflags[2]==1 or self.u_roomflags[2]==3):
                                #Case: Feeding the dragon
                                self.u_roomflags[2]=2
                                self.u_roomcurrent.update_room(2,2)
                                del self.u_items[i]
                                print(self.u_roomcurrent.Chk)      
                                break
                            else: print("You attempt to bite into the meat, but it's too rough...")
                        elif (str_input[4:].upper()=="TOY"):
                            if (self.u_roomcurrent.ID!=2): print("You play with the toy and get bored quickly.")
                            elif (self.u_roomflags[2]==1):
                                #Case: Dragon refusing to play until fed
                                self.u_roomflags[2]=3
                                self.u_roomcurrent.update_room(2,3)
                                print(self.u_roomcurrent.Chk)
                                break                                
                            elif (self.u_roomflags[2]==2):
                                #Case: Dragon contented by toy; key given
                                self.u_roomflags[2]=4
                                self.u_roomcurrent.update_room(2,4)
                                del self.u_items[i]
                                self.u_items.append("KEY")                                
                                print("The DRAGON takes the TOY and falls asleep while handing you a KEY!") 
                                break
                            elif (self.u_roomflags[2]==3):
                                #Case: Dragon fed up from hunger; game over
                                self.u_roomflags[2]=5
                                self.u_roomcurrent.update_room(2,5)
                                print(self.u_roomcurrent.Chk)            
                                self.u_roomflags[0]=1
                                break
                            elif (self.u_roomflags[2]==4):
                                print("The dragon should have the toy...")
                                break
                            else: print("You play with the toy and get bored quickly.")
                        elif (str_input[4:].upper()=="KEY"):
                            #Case: The key, and locked door in Dragon's Lair
                            if (self.u_roomcurrent.ID!=2): print("You fiddle around with the key.")
                            elif (self.u_roomflags[2]==4): 
                                del self.u_items[i]                                
                                print("You have unlocked the sealed door!")
                            else: print("How did you get the key...?")
                if (temp_haveitem==0 and self.u_roomflags[0]==0): print("What should I use?")
            elif (self.u_roomflags[0]==0):
                print("What should I use?")
        #Check inventory function
        elif (len(str_input)>=3 and (str_input[:3].upper()=="INV" or str_input[:9].upper()=="INVENTORY")):
            if (len(self.u_items)>0): print("Your current items:",self.u_items)
            else: print("You don't have anything on hand.")
        #Save function
        elif (len(str_input)>=4 and str_input[:4].upper()=="SAVE"):
            with open('savefile.txt','w') as file:
                #Make sure the default room is saved properly
                if (self.u_roomid==0): self.u_roomid=1
                #Consolidate necessary data into a list
                save_aggregate=[self.u_roomid,self.u_roomflags,self.u_roomhistory,self.u_items]
                #Save the list
                json.dump(save_aggregate,file)
            print("File saved.")
        #Load function
        elif (len(str_input)>=4 and str_input[:4].upper()=="LOAD"):
            with open('savefile.txt','r') as file:
                #Load the list of data
                load_aggregate=json.load(file)
                self.u_roomid=load_aggregate[0]
                self.u_roomflags=load_aggregate[1]
                self.u_roomhistry=load_aggregate[2]
                self.u_items=load_aggregate[3]
                newroomid=load_aggregate[0]
                self.u_roomnext.init_room(newroomid)
                #print("DEBUG: Initializing Room",newroomid)
                #print("DEBUG: Moving to Room",newroomid)
                self.u_roomcurrent=self.u_roomnext
                #Update any flags found in the new room to the current one            
                if (self.u_roomflags[newroomid]!=0):
                    #print("DEBUG: Flag spotted")
                    self.u_roomcurrent.update_room(newroomid,self.u_roomflags[newroomid])
                self.u_roomhistory.append(newroomid)
                #Print out new room description                    
                print(self.u_roomnext.Chk)
            print("File loaded.")
        elif (str_input=="?" or (len(str_input)>=4 and str_input[:4].upper()=="HELP")): print("Available commands are: LOOK, TAKE, USE, INVENTORY, <DIRECTION>, SAVE, LOAD, and QUIT")
        elif (not (str_input.upper()=="EXIT" or str_input.upper()=="STOP" or str_input.upper()=="QUIT" or str_input.upper()=="DIE")): print("Invalid command.")
        #Game Over!
        if (self.u_roomflags[0]==1):
            print("Game Over!")
            newinput=input("Retry? Y/N: ")
            while True:
                if (newinput.upper()=="Y" or newinput.upper()=="YES" or newinput=='Y' or newinput=='y'):
                    self.var_reset()
                    print("You awake to find yourself in a dimly lit room! \nWhat will you do? \nFor a list of commands, type HELP.")                 
                    break
                elif (newinput.upper()=="N" or newinput.upper()=="NO" or newinput=='N' or newinput=='n'):
                    self.u_roomflags[0]=2                  
                    break
                else:
                    print("Invalid response. Please type Y or N.")
                newinput=input("Retry? Y/N: ")
        #Exit Game
        if (self.u_roomflags[0]==2 or (len(str_input)==4 and (str_input.upper()=="EXIT" or str_input.upper()=="STOP" or str_input.upper()=="QUIT" or str_input.upper()=="DIE"))):
            print("Exiting game...")
            return 1
        else: #Continue operating
            return 0
