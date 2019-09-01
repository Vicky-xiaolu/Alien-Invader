"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the
Alien Invaders game.  Instances of Wave represent a single wave.  Whenever you
move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a
complicated issue.  If you do not know, ask on Piazza and we will answer.

# Xiaolu Zhang xz327 Haomiao Liu hl745
# Dec 4th
"""
from game2d import *
from consts import *
from models import *
import random
import threading

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)

class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you should create a NEW instance of Wave
    (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update. See subcontrollers.py from Lecture 24 for an example. This class
    be similar to than one in how it interacts with the main class Invaders.

    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of Alien
                 or None]
        _bolts:  the laser bolts currently on screen [list of Bolt, possibly
                 empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]

    As you can see, all of these attributes are hidden.  You may find that you
    want to access an attribute in class Invaders. It is okay if you do, but you
    MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter
    for any attribute that you need to access in Invaders.  Only add the getters
    and setters that you need for Invaders. You can keep everything else hidden.

    You may change any of the attributes above as you see fit. For example, may
    want to keep track of the score.  You also might want some label objects to
    display the score and number of lives. If you make changes, please list the
    changes with the invariants.
        _track: the direction aliens are supposed to move[boolean]
                if it is true, then aliens move to the right.
                Otherwise, to the left
        : record the last key pressed for creating bolts[boolean]
                         default to False
        _numOfShipBolt: to record the number of bolts sent from ships[int]
                        either be 0 or 1
        _alienBolt: to control the bolts fired by aliens[int]
                    in the 1...BOLT_RATE
        _step: count number of steps of the aliens[int]
               cannot be greater than BOLT_RATE
        _bgm: the object of type Sound for bakcground music [Sound]
        _xpos: record the position of the ship when destroyed [float]
        _ypos: record the position of the ship when destroyed [float]
        _sounds: the list of sound object to play [list]
        _last_keys_sound :record the key press to control sound [[boolean]]
                        default to false
        _time_sound: the time of pressing the key when controling the speed
                    [float] default to 0
        _numAliensKilled: number of aliens killed unitl now [int]
         _numAliensKilled>=0 default to 0
        _volume: the volume of the music played [0<=float<=1]
        _recordTime: number of seconds since last animation of explosion[float]
        _shipOpt: the ship chosen, a string of the name of the ship
                  [string]
        _lastVolume: the volume of the sound
                     [float] or [int]
        _barrierWall: barrier walls that used to protect the ship from the
                      aliens' bolts.
                      [list; every element is an instance of BarrierWall]
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getWaveAlien(self,m,n):
        """
        Returns the nth alien of the mth row of the alien list

        The method returns the (n+1)th alien of the (m+1)th row of
        attribute _aliens. Any changes made to that alien will modify
        the alien returned.
        """
        return self._aliens[m][n]

    def getAliens(self):
        """
        Returns the list of aliens in the wave.

        The method returns the attribute _aliens directly. Any changes made to
        the list will modify the set of aliens
        """
        return self._aliens

    def getBolt(self):
        """
        Returns the list of bolts in the wave.

        The method returns the attribute _bolts directly. Any changes
        made to the list will modify the set of bolts.
        """
        return self._bolts

    def getShip(self):
        """
        Returns the ship model in the wave.

        The method returns the attribute _ship directly. Any change made to the
        ship model will modify the ship returned.
        """
        return self._ship

    def getLives(self):
        """
        Returns the number of lives in the wave.

        The method returns the attribute _lives directly. Any change made to the
        number of lives will modify the number returned.
        """
        return self._lives

    def setShip(self):
        """
        The method that create a ship to the position assigned. The method
        allows a new ship to be set to the desired position when starting a new
        life.
        """
        self._ship=Ship(x=self.getXpos(),y=self.getYpos(),w=SHIP_WIDTH
                        ,h=SHIP_HEIGHT,source=self._shipOpt)

    def getXpos(self):
        """
        Returns the x-coordinate of the ship that was just destroyed.

        The method returns the attribte xpos directly. Any change made to the
        last position of the ship will modify the x-coordinate returned.
        """
        return self._xpos

    def getYpos(self):
        """
        Returns the y-coordinate of the ship that was just destroyed.

        The method returns the attribte xpos directly. Any change made to the
        last position of the ship will modify the y-coordinate returned.
        """
        return self._ypos

    def getVolume(self):
        """
        Returns the volume of the bgm(music) played.

        The method returns the volume of the attribute _bgm directly.
        """
        return self._bgm._volume

    def setVolume(self):
        """
        The method sets the volume of the bgm(music) played to the attribute
        _lastVolume.
        """
        self._bgm._volume=self._lastVolume

    def getBarrierWall(self):
        """
        Returns the list of instances of BarrierWall.

        The method returns the attribte _barrierWall directly. Any change made
        to the barrier wall inside the list will modify the list returned.
        """
        return self._barrierWall

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def initAlien(self):
        """
        Returns a wave of alien in a list.

        The method is a helper function of the built-in initializer, __init__.
        It creates a wave of alien that have ALIEN_ROWS rows and ALIENS_IN_ROW
        in a row. It returns the wave of alien in a list that will go to the
        attribute _aliens in the buit-in initializer, __init__.
        """
        aliens=[]
        for i in range(1,ALIEN_ROWS+1):
            row=[]
            for j in range(1,ALIENS_IN_ROW+1):
                xValue= ALIEN_H_SEP*j+(j-1)*ALIEN_WIDTH + ALIEN_WIDTH/2
                yValue= GAME_HEIGHT-(ALIEN_CEILING+(i-1)*ALIEN_V_SEP
                +ALIEN_HEIGHT*(i-1 + 1/2))
                #tell the num of alien image to use
                if ALIEN_ROWS % 2==0:
                    if i % 2 !=0:
                        num=int((ALIEN_ROWS//2-(i-1)//2)%(len(ALIEN_IMAGES)))
                    else:
                        num=int((ALIEN_ROWS//2-i//2+1)%(len(ALIEN_IMAGES)))
                else:
                    if i%2 == 0:
                        num=int(((ALIEN_ROWS-i+1)//2)%(len(ALIEN_IMAGES)))
                    else:
                        num=int(((ALIEN_ROWS-i)//2+1)%(len(ALIEN_IMAGES)))
                alien=Alien(x=xValue,y=yValue,w=ALIEN_WIDTH,h=ALIEN_HEIGHT,
                source=ALIEN_IMAGES[num-1],format=(3,2))
                row.append(alien)
            aliens.append(row)
        return aliens

    def initSound(self):
        """
        Initializes the attribute, _sounds, and achieve the sound effect.

        The method is a helper function of the built-in initializer __init__.
        It initializes the attribte _sounds as a list and it adds the sound
        files into the list.
        """
        self._sounds={}
        self._sounds['blast1']=Sound('blast2.wav')
        self._sounds['blast2']=Sound('blast3.wav')
        self._sounds['pew']=Sound('pew1.wav')
        self._sounds['pop']=Sound('pop1.wav')

    def initDline(self):
        """
        Returns the defense line.

        The method is a helper function of the built-in initializer __init__.
        It returns the defense line at DEFENSE_LINE pixels from the bottom of
        the screen.
        """
        line=GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],linewidth=2
                   ,linecolor='grey')
        return line

    def initBarrierWall(self):
        """
        Returns the barrierwall that protects the ship from the aliens' bolts.

        The method is a helper function of the built-in initializer __init__.
        It returns a list that has NUM_BARRIER_WALL instances of Barrierwall.
        The method does the job of initializing all the barrierwall, and the
        returned list will go to the attribte _barrierWall.
        """
        barrierWall=[]
        for i in range(1,NUM_BARRIER_WALL+1):
            temp=BarrierWall(x=i*BARRIER_WALL_H_SEP,y=BARRIER_WALL_V
        ,w=BARRIER_WALL_WIDTH,h=BARRIER_WALL_HEIGHT,source='barrierwall.png')
            barrierWall.append(temp)
        return barrierWall

    def __init__(self,bgm,s,barrierwall=None,life=0):
        """
        Initializes a wave that excutes the entire game.

        The optional argument barrierwall is the list of instances of
        BarrierWall. It passed the attribute _barrierWall from the last upate.
        It would be None if there is all the barrier walls are destroyed by the
        bolts. The optional argument life is the number of lives left. It passed
        the attribute _lives from the last update. It would be 0 if there is
        no lives left.

        Parameter bgm: the sound effect of the game
        Precondition: bgm is a list that every element is a wav file.

        Parameter s: the name of the ship that user chose.
        Precondition: s is a string.

        Parameter barrierwall: barrier walls that used to protect the ship from
        the aliens' bolts.
        Precondition: barrierwall is either None or a list that every element
        inside is an instance of BarrierWall.

        Parameter life: the number of lives left
        Precondition: life is an int that is bigger or equal than 0.
        """
        self._bgm=bgm
        self._bgm.play(loop=True)
        self._aliens=self.initAlien()
        self._shipOpt=s
        self._ship = Ship(x=GAME_WIDTH/2,y=SHIP_BOTTOM,w=SHIP_WIDTH
        ,h=SHIP_HEIGHT,source=s)
        self._dline=self.initDline()
        self._time=0
        Wave._track=True
        self._bolts=[]
        self._last_keys_bolts = False
        self._numOfShipBolt=0
        self._alienBolt=random.randint(1,BOLT_RATE)
        self._step=0
        if life==0:
            self._lives=SHIP_LIVES
        else:
            self._lives=life
        self._xpos=GAME_WIDTH/2
        self._ypos=GAME_HEIGHT/2
        self.initSound()
        self._last_keys_sound=False
        self._time_sound=0
        self._numAliensKilled=0
        self._recordTime=0
        self._lastVolume=1
        if barrierwall!=None:
            self._barrierWall=barrierwall
        else:
            self._barrierWall=self.initBarrierWall()

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def moveShip(self,input):
        """
        MOVE the ship by SHIP_MOVEMENT per updates.

        This method is a helper function of the function update.
        If the input is 'right', the ship moves to the right; if the
        input is 'left', the ship moves to the left.


        Parameter input: the user's input--keys they pressed.
        Precondition: a instance of Invaders's attribute input
        """
        if self._ship!=None:
            if self._ship.getX()<=SHIP_WIDTH/2 and input.is_key_down('left'):
                self._ship.changeX(0)
            elif (self._ship.getX()>=GAME_WIDTH-SHIP_WIDTH/2 and
                        input.is_key_down('right')):
                self._ship.changeX(0)
            else:
                if input.is_key_down('left'):
                    self._ship.changeX(-SHIP_MOVEMENT)
                if input.is_key_down('right'):
                    self._ship.changeX(SHIP_MOVEMENT)

    def moveAlienRight(self,curwave):
        """
        Move the wave of aliens right.

        This method is a helper function of the function moveAliens.

        Parameter curwave: the number of waves that have existed since beginning
        Precondition: curwave is an int >=1
        """
        if (self._time>=
        ALIEN_SPEED*SPD_INCRE_EACH_NEW_WAVE**(curwave+self._numAliensKilled-1)):
            for i in self._aliens:
                for j in i:
                    if j!=None:
                        j.changeX(ALIEN_H_WALK)
                        j.changeFrame()
            self._time=0
            self._step+=1

    def moveAlienLeft(self,curwave):
        """
        Move the wave of aliens left.

        This method is a helper function of the function moveAliens.

        Parameter curwave: the number of waves that have existed since beginning
        Precondition: curwave is an int >=1
        """
        if (self._time>=
        ALIEN_SPEED*SPD_INCRE_EACH_NEW_WAVE**(curwave+self._numAliensKilled-1)):
            for i in self._aliens:
                for j in i:
                    if j!=None:
                        j.changeX(-ALIEN_H_WALK)
                        j.changeFrame()
            self._time=0
            self._step+=1

    def moveAlienDown(self):
        """
        Move the wave of aliens down.

        This method is a helper function of the function moveAliens.
        The method moves all the alien in the attribte _aliens down by
        ALIEN_V_SEP pixels.
        """
        for i in self._aliens:
            for j in i:
                if j!=None:
                    j.changeY(-ALIEN_V_SEP)

    def moveAliens(self,dt,curwave):
        """
        Move aliens to the right position.

        This method is a helper function of the function update.
        The method moves aliens to the right position according to dt, the
        accumulative time since last move, and the curwave, which is the number
        of waves.

        Parameter dt: object of GImage to display the background
        Precondition: GImage

        Parameter curwave: the number of waves that have existed since beginning
        Precondition: curwave is an int >=1
        """
        for i in self._aliens:
            for j in i:
                if j!=None:
                    if (Wave._track==True and GAME_WIDTH-j.getX()<=
                        ALIEN_H_SEP + ALIEN_WIDTH/2):
                        self.moveAlienDown()
                        Wave._track=False

        for i in self._aliens:
            for j in i:
                if j!=None:
                    if (Wave._track==False and j.getX()<=
                        (ALIEN_H_SEP+ALIEN_WIDTH/2)):
                        self.moveAlienDown()
                        Wave._track=True
        if Wave._track==True:
            self.moveAlienRight(curwave)
        if Wave._track==False:
            self.moveAlienLeft(curwave)

    def createShipBolt(self,input):
        """
        Creates the ship's bolts

        This method is a helper function of the function update.
        This method detects for a 'up' key press, and if there is one, change
        the state from STATE_INACTIVE to STATE_NEWWAV. A key press is when a key
        is pressed for the FIRST TIME. We do not want the state to continue to
        change as we hold down the key.  The user must release the key and press
        it again to change the state.

        Parameter input: the user's input--keys they pressed.
        Precondition: a instance of Invaders's attribute input
        """
        curr_keys=input.is_key_down('up') or input.is_key_down('spacebar')
        if (curr_keys==True and self._last_keys_bolts == False and
                          self._numOfShipBolt==0):
            if self._ship!=None:
                bolt=Bolt(x=self._ship.getX(),y=self._ship.getY()+
                BOLT_HEIGHT/2+SHIP_HEIGHT/2,w=BOLT_WIDTH
                ,h=BOLT_HEIGHT,fillcolor='white',velocity=BOLT_SPEED)
                self._bolts.append(bolt)
                self._numOfShipBolt=1
                self._sounds['pew'].play()
        self._last_keys_bolts==curr_keys

    def moveBolt(self):
        """
        Moves the players' and aliens' bolts.

        This method is a helper function of the function update.
        The method that moves every bolt according to the BOLT_SPEED every
        update. It deals with players' and aliens' bolts.
        """
        for i in self._bolts:
            if i!=None:
                if i.isPlayerBolt():
                    i.changeY(BOLT_SPEED)
                else:
                    i.changeY(-BOLT_SPEED)
        i = 0
        while i < len(self._bolts):
            if self._bolts[i].getY()+BOLT_HEIGHT/2 >=GAME_HEIGHT:
                del self._bolts[i]
                self._numOfShipBolt=0
            else:
                i += 1

    def alienMove(self):
        """
        Finds the alien that's the on the most bottom of a random column.

        This method is a helper function of the function update. It generates
        a random alien to shoot a bolt.
        """
        if self._step==self._alienBolt:
            self._step=0
            templist=[]
            col=0
            for i in range(ALIEN_ROWS):
                for j in range(ALIENS_IN_ROW):
                    if self._aliens[i][j]!=None and not j in templist:
                        templist.append(j)
            if len(templist)!=0:
                col=templist[random.randint(0,len(templist)-1)]
            lower=0
            for j in range(ALIEN_ROWS):
                if self._aliens[j][col]!=None and j>lower:
                    lower=j
            if self._aliens[lower][col]!=None:
                xPosition=self._aliens[lower][col].getX()
                yPosition=(self._aliens[lower][col].getY()-ALIEN_HEIGHT/2-
                                BOLT_HEIGHT/2)
                self._bolts.append(Bolt(x=xPosition,y=yPosition,w=BOLT_WIDTH,
                        h=BOLT_HEIGHT,fillcolor='red',velocity=-BOLT_SPEED))
                self._alienBolt=random.randint(1,BOLT_RATE)

    def soundControl(self,input,dt):
        """
        Determine the current state and assigns it to self.state.

        This method is a helper function of the function update.
        This method cjecks for a 's' key press, and if there is one, change the
        state from STATE_INACTIVE to STATE_NEWWAV. A key press is when a key is
        pressed for the FIRST TIME. We do not want the state to continue to
        change as we hold down the key.  The user must release the key and press
        it again to change the state.

        Parameter input: the user's input--keys they pressed.
        Precondition: a instance of Invaders's attribute input.

        Parameter dt: object of GImage to display the background
        Precondition: GImage
        """
        if input.is_key_down('d'):
            if self._time_sound>=TIME_LIMIT_SOUND:
                self._time_sound+=dt
                self._bgm.volume=0
                for k in self._sounds:
                    self._sounds[k].volume=0
        if input.is_key_down('u'):
            if self._bgm.volume<=0.95:
                self._bgm.volume+=0.05
            for k in self._sounds:
                if self._sounds[k].volume<=0.95:
                    self._sounds[k].volume+=0.05
        if input.is_key_down('d'):
            if self._bgm.volume>=0.05:
                self._bgm.volume-=0.05
            for k in self._sounds:
                if self._sounds[k].volume>=0.05:
                    self._sounds[k].volume-=0.05
        self._lastVolume=self._bgm.volume

    def update(self,input,dt,curwave,score):
        """
        Animates a single frame in the game.

        Parameter input: the user's input--keys they pressed.
        Precondition: a instance of Invaders's attribute input.

        Parameter dt: object of GImage to display the background
        Precondition: GImage

        Parameter curwave: the number of waves that have existed since beginning
        Precondition: curwave is an int >=1

        Parameter score: the score the player earns
        Precondition: score is a list with int inside
        """
        self._time+=dt
        self._recordTime+=dt
        self.moveShip(input)
        self.moveAliens(dt,curwave)
        self.createShipBolt(input)
        self.alienMove()
        self.moveBolt()
        self.collisionShip()
        self.collisionAlien(score,dt)
        self.soundControl(input,dt)
        self.collisionBarrier()

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def drawAliens(self,view):
        """
        Draws the alien on screen.

        The method is a helper function of the function draw.

        Parameter view: the view to draw aliens on
        Precondition: it is the attribute view of an instance of Class Invaders.
        """
        for i in self._aliens:
            for j in i:
                if j!=None:
                    j.draw(view)

    def drawBarrierWall(self,view):
        """
        Draws the barrier walls on screen.

        The method is a helper function of the function draw.

        Parameter view: the view to draw barrier walls on
        Precondition: it is the attribute view of an instance of Class Invaders.
        """
        for i in range(len(self._barrierWall)):
            if self._barrierWall[i]!=None:
                self._barrierWall[i].draw(view)

    def drawShip(self,view):
        """
        Draws the ship on screen.

        The method is a helper function of the function draw.

        Parameter view: the view to draw ships on
        Precondition: it is the attribute view of an instance of Class Invaders.
        """
        if self._ship!=None:
            self._ship.draw(view)

    def drawDline(self,view):
        """
        Draws the defense line on screen.

        The method is a helper function of the function draw.

        Parameter view: the view to draw defense line on
        Precondition: it is the attribute view of an instance of Class Invaders.
        """
        self._dline.draw(view)

    def drawBolt(self,view):
        """
        Draws the bolts on screen.

        The method is a helper function of the function draw.

        Parameter view: the view to draw bolts on
        Precondition: it is the attribute view of an instance of Class Invaders.
        """
        for i in self._bolts:
            if i!=None:
                i.draw(view)

    def draw(self,view):
        """
        Draws the everything the game needs on screen.

        The method draws all the components per update.

        Parameter view: the view to draw aliens on
        Precondition: it is the attribute view of an instance of Class Invaders.
        """
        self.drawAliens(view)
        self.drawShip(view)
        self.drawDline(view)
        self.drawBolt(view)
        self.drawBarrierWall(view)

    # HELPER METHODS FOR COLLISION DETECTION
    def collisionAlien(self,score,dt):
        """
        Deals with the collision betweeen players' bolts and aliens.

        This method is a helper function of the function update.
        This method detects the collision betweeen players' bolts and aliens,
        and it modifies the alien to None. Also, it pops the sound effect as
        well.

        Parameter score: the score the player earns
        Precondition: score is a list with int inside

        Parameter dt: object of GImage to display the background
        Precondition: GImage
        """
        for i in range(ALIEN_ROWS):
            for j in range(ALIENS_IN_ROW):
                for k in range(len(self._bolts)):
                    if i!=None and j!=None and self._aliens[i][j]!=None:
                        if self._aliens[i][j].collides(self._bolts[k]):
                            self._aliens[i][j].setFrame(2)
                            self._recordTime=0
                            self._aliens[i][j]=None
                            del self._bolts[k]
                            self._numAliensKilled+=1
                            if ALIEN_ROWS%2==0:
                                if (i+1)%2==0:
                                    score[0]+=int((i+1)/2*10)
                                else:
                                    score[0]+=int((i+2)/2*10)
                            else:
                                if (i+1)%2==0:
                                    score[0]+=int((i+1)/2*10)+10
                                else:
                                    score[0]+=int(i/2*10)+10
                            self._sounds['pop'].play()
                            self._numOfShipBolt=0

    def collisionShip(self):
        """
        Deals with the collision betweeen bolts and the ship.

        This method is a helper function of the function update.
        This method detects the collision betweeen bolts and the ship.
        It eliminates the collided bolts and the ship (setting it to None).
        """
        for i in range(len(self._bolts)):
            if self._ship!=None:
                if self._ship.collides(self._bolts[i]):
                    del self._bolts[i]
                    self._xpos=self._ship.x
                    self._ypos=self._ship.y
                    self._ship=None
                    self._sounds['blast1'].play()
                    for i in range(len(self._bolts)):
                        """error messege index out of bounds"""
                        if i in range(len(self._bolts)):
                            if self._bolts[i].isPlayerBolt():
                                del self._bolts[i]
                                self._numOfShipBolt=0
                    if self._lives>0:
                        self._lives-=1

    def collisionBarrier(self):
        """
        Deals with the collision betweeen bolts and barrier wall.

        This method is a helper function of the function update.
        This method detects the collision betweeen bolts and barrier wall.
        It modifies the barrier wall and it eliminates the collided bolts.
        """
        for i in range(len(self._barrierWall)):
            for j in range (len(self._bolts)):
                if (j in range(len(self._bolts)) and i in
                                range(len(self._barrierWall))):
                    if self._barrierWall[i]!=None and self._bolts[j]!=None:
                        if self._barrierWall[i].collides(self._bolts[j]):
                            if self._bolts[j].isPlayerBolt():
                                self._numOfShipBolt=0
                            del self._bolts[j]
                            self._barrierWall[i].addCounter()
                            if (self._barrierWall[i].getCounter()>=
                                                BARRIER_WALL_RESISTANCE):
                                if self._barrierWall[i].getFrame() == 3:
                                    del self._barrierWall[i]
                                else:
                                    self._barrierWall[i].addFrame()
                                    self._barrierWall[i].setCounter(0)
