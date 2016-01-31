#!/usr/bin/python

class dgn_room:
    #Initialize Varibles
    ID=0
    Name=""
    Dir=list()
    Rnx=list()
    Obj=list()
    Desc=list()
    Chk="It's the default room."
    Info=[ID,Name,Dir,Obj,Chk]
    def init_room(self,roomid):
        self.ID=roomid
        if (roomid==1):
            self.Name="Entrance"
            self.Dir=["EAST","NORTH"]
            self.Rnx=[4,2]
            self.Obj=["DOOR"]
            self.Desc=["It's a large, foreboding door..."]
            self.Chk="This is where you woke up."
        elif (roomid==2):
            self.Name="Dragon's Lair"
            self.Dir=["NORTH","SOUTH"]
            self.Rnx=[3,1]
            self.Obj=["DRAGON"]
            self.Desc=["It's a terrifying dragon! Pacify it, quickly!"]
            self.Chk="It's the DRAGON's lair!"
        elif (roomid==3):
            self.Name="Winner's Circle"
            self.Dir=["SOUTH"]
            self.Rnx=[2]
            self.Obj=["FLASK"]
            self.Desc=["It's the object that everyone desires! Grab it!"]
            self.Chk="There's a FLASK in the room! Go TAKE it!"
        elif (roomid==4):
            self.Name="Crossroads"
            self.Dir=["WEST","NORTH","EAST"]
            self.Obj=[]
            self.Rnx=[1,6,5]
            self.Chk="It looks like the room forks here."
        elif (roomid==5):
            self.Name="Puzzled"
            self.Dir=["WEST"]
            self.Rnx=[4]
            self.Obj=["PUZZLE"]
            self.Desc=["The puzzle asks, 'What is 5 times 10'?"]
            self.Chk="The room is empty, save for a PUZZLE on a piece of paper..."
        elif (roomid==6):
            self.Name="Foreboding Chamber"
            self.Dir=["SOUTH"]
            self.Rnx=[4]
            self.Obj=["BONES","MEAT"]
            self.Desc=["Looks like someone had a good meal... Too heavy to lift, though.",
                       "Still smells fresh. Might be useful to have around before it goes bad."]
            self.Chk="The room doesn't smell very good..."
        self.Info=[self.ID,self.Name,self.Dir,self.Obj,self.Chk]
    def update_room(self,roomid,flag):
        if (roomid==1):
            if (flag==1):self.Chk="The BIG DOOR has opened! It's time to see what's behind it!"
        elif (roomid==2):
            if (flag==1):self.Chk="The DRAGON wakes up! It looks hungry..."
            elif (flag==2):self.Chk="The DRAGON likes the MEAT, but seems to be bored..."
            elif (flag==3):self.Chk="The DRAGON refuses the TOY until it is fed."
            elif (flag==4):self.Chk="The DRAGON is contented."
            elif (flag==5):self.Chk="The DRAGON's hunger compels it to eat you! You have died!"
            elif (flag==6):self.Chk="The DRAGON's swipes at you in boredom! You have died!"
        elif (roomid==3):
            if (flag==1):self.Chk="FLASK in hand, you find an exit! You have won!"
        elif (roomid==5):
            if (flag==1):self.Obj=[];self.Chk="When you thought of the answer in your mind, a TOY suddenly appeared in your inventory!"
            elif (flag==2):self.Chk="This PUZZLE doesn't seem hard; you'll want to try again."
        elif (roomid==6):
            if (flag==1):self.Chk="The BONES are too heavy to pick up."
            elif (flag==2):
                self.Obj=["BONES"]
                self.Chk="The MEAT is a bit smelly, but you feel confident about TAKING it."