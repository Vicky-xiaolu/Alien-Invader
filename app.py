"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders
application. There is no need for any additional classes in this module.
If you need more classes, 99% of the time they belong in either the wave module
or the models module. If you are unsure about where a new class should go,
post a question on Piazza.

# Xiaolu Zhang xz327 Haomiao Liu hl745
# Dec 4th
"""
from consts import *
from game2d import *
from wave import *
from models import *

# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/
                #setters
# Invaders is NOT allowed to access anything in models.py
class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary for
    processing the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.

    The primary purpose of this class is to manage the game state: which is when
    the game started, paused, completed, etc. It keeps track of that in an
    attribute called _state.

    INSTANCE ATTRIBUTES:
        view:   the game view, used in drawing (see examples from class)
                [instance of GView; it is inherited from GameApp]
        input:  the user input, used to control the ship and change state
                [instance of GInput; it is inherited from GameApp]
        _state: the current state of the game represented as a value from
                consts.py
                [one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE,
                STATE_PAUSED, STATE_CONTINUE, STATE_COMPLETE]
        _wave:  the subcontroller for a single wave, which manages the ships
                and aliens
                [Wave, or None if there is no wave currently active]
        _text:  the currently active message
                [GLabel, or None if there is no message to display]


    STATE SPECIFIC INVARIANTS:
        Attribute _wave is only None if _state is STATE_INACTIVE.
        Attribute _text is only None if _state is STATE_ACTIVE.

    For a complete description of how the states work, see the specification for
    the method update.

    You may have more attributes if you wish (you might want an attribute to
    store any score across multiple waves). If you add new attributes, they need
    to be documented here.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        last_keys: whether the key pressed last frame is 's'
                [boolean, initialized to False]
        _status: whether the status for the player is winning or losing[boolean]
                True means winning and false means losing
        _time: the time for the state STATE_AGAIN to record time of the reminder
               [int or float; >=0]
        _curwave: the number of waves that have existed since beginning
                [int,initialized to 1]
        _score: the score the player earns
                 [list, len(_score)=1, element in list>=0]
        _bgm: the object of type Sound for bakcground music [Sound]
        _win: the object of type Sound for congratulations [Sound]
        _lose: the object of type Sound for losing [Sound]
        _lives: the number of lives the ship has left[int]
        _bg: object of GImage to display the background[instance of GImage]
        _listOfShips: dictionary of ships [dictionary]
        _scoreRecorder: a GLabel that shows the score [instance of GLabel]
        _livesRecorder: a GLabel that shows the lives left [instance of GLabel]
        _lastClick: True if you have clicked before, defaut to False [boolean]
    """

    # DO NOT MAKE A NEW INITIALIZER!
    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which
        you should not override or change). This method is called once the game
        is running.You should use it to initialize any game specific attributes.

        This method should make sure that all of the attributes satisfy the
        given invariants. When done, it sets the _state to STATE_INACTIVE and
        create a message (in attribute _text) saying that the user should
        press to play a game.
        """
        self._state=STATE_PREP
        self.state_output()
        self._listOfShips=[]
        for i in range(1,NUM_SHIPS+1):
            ship=ShipsOption(x=i*SHIP_H_SEP,y=SHIP_V_VALUE,w=SHIP_OPTION_WIDTH
            , h=SHIP_OPTION_HEIGHT, source='ship'+str(i)+'.png')
            self._listOfShips.append(ship)
        self._status=False
        self._time=0
        self._curwave=1
        self._text=GLabel(text='Choosing your own ship',x=GAME_WIDTH/2
                 ,y=GAME_HEIGHT/2-50,font_size=35,
                font_name='RetroGame.ttf',width=GAME_WIDTH,height=500,bold=True,
                halign='center',valign='middle', linecolor='white')
        self._wave=None
        self._score=[0]
        self._scoreRecorder=GLabel(text='Score: '+ str(self._score[0]),
                         x=80,y=650,font_size=25,
                        font_name='ComicSans.ttf',width=100,height=40,bold=True,
                        halign='center',valign='middle',linecolor='red')
        self._bgm=Sound('bgm.wav')
        self._lives=SHIP_LIVES
        self._livesRecorder=GLabel(text='Lives: '+ str(self._lives) ,x=700,y=650
                         ,font_size=25,
                        font_name='ComicSans.ttf',width=100,height=40,bold=True,
                        halign='center',valign='middle', linecolor='red')
        self._bg=GImage(x=GAME_WIDTH/2,y=GAME_HEIGHT/2,
                    width=GAME_WIDTH,height=GAME_HEIGHT,source='space.png')
        self._lastClick=None

    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of
        playing the game.  That is the purpose of the class Wave. The primary
        purpose of this game is to determine the current state, and -- if the
        game is active -- pass the input to the Wave object _wave to play the
        game.

        As part of the assignment, you are allowed to add your own states.
        However, at a minimum you must support the following states:
        STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED,
        STATE_CONTINUE, and STATE_COMPLETE.  Each one of these does its own
        thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.
        It is a paused state, waiting for the player to start the game.
        It displays a simple message on the screen. The application remains
        in this state so long as the player never presses a key.
        In addition, this is the state the application returns to when
        the game is over (all lives are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on
        the screen. The application switches to this state if the state was
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        This state only lasts one animation frame before switching to
        STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can
        move the ship and fire laser bolts.  All of this should be handled
        inside of class Wave (NOT in this class).  Hence the Wave class should
        have an update() method, just like the subcontroller example in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state.
        However, the game is still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed. The
        application switches to this state if the state was STATE_PAUSED in the
        previous frame, and the player pressed a key. This state only lasts one
        animation frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over, and is either won or lost.

        STATE_AGAIN: One of the waves is over and there is still mowe waves to
        come, and this stage print out something on the screen like "Warning:
        there are x more waves to come!". This is basically a transition state
        and it lasts for WAIT_SECONDS seconds to procede to the next state.

        STATE_PREP: this state is for choosing your own ships while playing.
        This is more user-friendly and make this game more interesitng. By
        chosing, you just need to click on the ship you like the most. This
        state will not precede to the next unless you click on one valid ship.

        You are allowed to add more states if you wish. Should you do so, you
        should describe them here.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._state == STATE_INACTIVE:
            self.state_output()
            self._score=[0]
            self._curwave=1
            self._detect_s()
        if self._state==STATE_NEWWAVE:
            self.update_newwave()
        if self._state==STATE_ACTIVE:
            self._wave.update(self.input, dt,self._curwave,self._score)
            self.state_output()
            self.changeStates()
        if self._state==STATE_PAUSED:
            self.state_output()
            self._detect_s()
        if self._state==STATE_CONTINUE:
            self._wave.setShip()
            self._wave.setVolume()
            self._state=STATE_ACTIVE
        if self._state==STATE_COMPLETE:
            self.update_complete(dt)
        if self._state==STATE_AGAIN:
            self.update_restart(dt)
        if self._state==STATE_PREP:
            self.start()
            self._checkClick()

    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To draw
        a GObject g, simply use the method g.draw(self.view).  It is that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are
        attributes in Wave. In order to draw them, you either need to add
        getters for these attributes or you need to add a draw method to class
        Wave.  We suggest the latter.
        Seethe example subcontroller.py from class.
        """
        if self._state==STATE_INACTIVE:
            self._animateAll()
            self._animateText()
        if self._state==STATE_NEWWAVE:
            self._animateImage()
        if self._state==STATE_ACTIVE:
            self._animateAll()
            self._animateImage()
        if self._state==STATE_PAUSED:
            self._animateAll()
            self._animateText()
            self._animateImage()
        if self._state==STATE_CONTINUE:
            self._animateAll()
            self._animateImage()
        if self._state==STATE_COMPLETE:
            self._animateAll()
            self._animateText()
        if self._state==STATE_AGAIN:
            self._animateAll()
            self._animateText()
        if self._state==STATE_RESTART:
            self._animateAll()
            self._animateText()
        if self._state==STATE_PREP:
            self._animateBg()
            self._animateShips()
            self._animateText()

    # HELPER METHODS FOR THE STATES GO HERE
    def state_output(self):
        """
        Ouputs all the text on screen corresonding to each state.

        The method is a helper function of the function upate.
        """
        if self._state==STATE_INACTIVE:
            self._text.text=text='Press SPACE to play'
        if self._state==STATE_PAUSED:
            info=('Press S to start over\nlives remaining: '
                   + str(self._wave.getLives()))
            self._text.text=info
        if self._state==STATE_ACTIVE:
            self._text.text=''
            self._scoreRecorder.text='Score: '+str(self._score[0])
            self._livesRecorder.text='Lives: '+str(self._wave.getLives())
        elif self._state==STATE_COMPLETE:
            if self._status==True:
                self._text.text='Congratulations!\nYou win!'
            if self._status==False:
                self._text.text='GAME OVER'
            self._wave=None
        elif self._state==STATE_AGAIN:
            info=('WARNING: ANOTHER WAVE IS COMING!\nLives remaining: '
            + str(self._wave.getLives())+'\n'
            +str(MAX_NUM_OF_WAVE-self._curwave)+' MORE WAVES TO COME')
            self._text.text=info
        self.last_keys = False

    def _checkClick(self):
        """
        Checks for a click and select a ship where clicked.

        This method is a helper function of the function update.
        A 'click' is the animation frame after the mouse is pressed for the
        first time in a while (so _lastclick is None).
        """
        # Input stores the touch information
        touch = self.input.touch

        if self._lastClick is None and not touch is None:
            # Click happened.  Add rocket to particle list.
            if (touch.x >= SHIP_H_SEP-SHIP_OPTION_WIDTH/2 and
            touch.x<=SHIP_H_SEP+SHIP_H_SEP/2 and
            touch.y >=SHIP_V_VALUE-SHIP_OPTION_HEIGHT/2 and
            touch.y <= SHIP_V_VALUE + SHIP_OPTION_HEIGHT/2):
                self._finalShip='ship1.png'
                self._state=STATE_INACTIVE
            if (touch.x >= SHIP_H_SEP*2-SHIP_OPTION_WIDTH/2 and
            touch.x<=SHIP_H_SEP*2+SHIP_H_SEP/2 and
            touch.y >=SHIP_V_VALUE-SHIP_OPTION_HEIGHT/2 and
            touch.y <= SHIP_V_VALUE + SHIP_OPTION_HEIGHT/2):
                self._finalShip='ship2.png'
                self._state=STATE_INACTIVE
            if (touch.x >= SHIP_H_SEP*3-SHIP_OPTION_WIDTH/2 and
            touch.x<=SHIP_H_SEP*3+SHIP_H_SEP/2 and
            touch.y >=SHIP_V_VALUE-SHIP_OPTION_HEIGHT/2 and
            touch.y <= SHIP_V_VALUE + SHIP_OPTION_HEIGHT/2):
                self._finalShip='ship3.png'
                self._state=STATE_INACTIVE
        # Update lastclick
        self._last = touch

    def _detect_s(self):
        """
        Determine the current state and assigns it to self.state

        This method is a helper function of the function update.
        This method cjecks for a 's' key press, and if there is one, change the
        state from STATE_INACTIVE to STATE_NEWWAV. A key press is when a key is
        pressed for the FIRST TIME. We do not want the state to continue to
        change as we hold down the key.  The user must release the key and press
        it again to change the state.
        """
        curr_keys=self.input.is_key_down('spacebar')
        if curr_keys==True and self.last_keys == False:
            self._state=self._state+1
            _text=None
        self.last_keys==curr_keys

    def allAliensDead(self):
        """
        Returns True if all the aliens are dead; Falso otherwise.

        This method is a helper function of the function update. It loops
        through all the aliens to check if all of them are None.
        """
        for i in range(ALIEN_ROWS):
            for j in range(ALIENS_IN_ROW):
                if self._wave.getWaveAlien(m=i,n=j)!=None:
                    return False
        return True

    def passDline(self):
        """
        Returns True if any of the alien passes the defense line; False
        otherwise.

        This method is a helper function of the function update. It loops
        through all the aliens to check if any of them thouchs the defense line.
        """
        for i in range(ALIEN_ROWS):
            for j in range(ALIENS_IN_ROW):
                if self._wave.getWaveAlien(i,j)!=None:
                    if (self._wave.getWaveAlien(i,j).getY()-ALIEN_HEIGHT/2<=
                        DEFENSE_LINE):
                        return True
        return False

    def changeStates(self):
        """
        This is for changing state in the game.

        This is called by the update() as a helper function to detect whether
        it's time to change states.

        """
        # This is when the ship is shot and also when the player havs lives
        # left. If this happens, then transit to STATE_PAUSED
        if self._wave.getShip()==None and self._wave.getLives()>0:
            self._state=STATE_PAUSED
        # When player doesn't have lives left then transfer to STATE_COMPLETE
        #with the message (self._status being false meaning the player is
        #losing)
        if self._wave.getLives()<=0:
            self._status=False
            self._state=STATE_COMPLETE
        # When all aliens are dead and when the player has lives remaining.
        # Also this is no
        if (self.allAliensDead() and self._wave.getLives()>0
             and MAX_NUM_OF_WAVE-self._curwave<=1):
            self._status=True
            self._state=STATE_COMPLETE
        if (self.allAliensDead() and self._wave.getLives()>0
             and self._curwave<MAX_NUM_OF_WAVE):
            self._state=STATE_AGAIN
        if self.passDline():
            self._status=False
            self._state=STATE_COMPLETE

    def update_newwave(self):
        """
        Updates everything if the state is STATE_NEWWAV.

        This method is a helper function of the function update. If the state
        is STATE_NEWWAV, the method is called to handle every update in that
        state.
        """
        if self._wave!=None:
            self._wave=Wave(bgm=self._bgm,s=self._finalShip,
        life=self._wave.getLives(),barrierwall=self._wave.getBarrierWall())
        else:
            self._wave=Wave(bgm=self._bgm,s=self._finalShip)
        self._state+=1

    def update_complete(self,dt):
        """
        Updates everything if the state is STATE_COMPLETE.

        This method is a helper function of the function update. If the state
        is STATE_COMPLETE, the method is called to handle every update in that
        state.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._time+=dt
        if (self._time<=WAIT_SECONDS):
            self.state_output()
        else:
            self._time=0
            self._state=STATE_INACTIVE

    def update_restart(self,dt):
       """
       Updates everything if the state is STATE_RESTART.

       This method is a helper function of the function update. If the state
       is STATE_RESTART, the method is called to handle every update in that
       state.

       Parameter dt: The time in seconds since last update
       Precondition: dt is a number (int or float)
       """
       self._time+=dt
       if (self._time<=WAIT_SECONDS):
           self.state_output()
       else:
           self._time=0
           self._curwave+=1
           self._state=STATE_NEWWAVE

    def _animateText(self):
       """
       Animates the text on the screen.

       The method is a helper function of the function draw.
       """
       if self._text!=None:
           self._text.draw(self.view)

    def _animateImage(self):
       """
       Animates the images (wave) on the screen.

       The method is a helper function of the function draw.
       """
       if self._wave!=None:
           self._wave.draw(self.view)

    def _animateTextScore(self):
       """
       Animates the score on the screen.

       The method is a helper function of the function _animateAll.
       """
       if self._scoreRecorder!=None:
           self._scoreRecorder.draw(self.view)

    def _animateTextLives(self):
       """
       Animates the the number of lives left on the screen.

       The method is a helper function of the function _animateAll.
       """
       if self._livesRecorder!=None:
           self._livesRecorder.draw(self.view)

    def _animateBg(self):
       """
       Animates the object of GImages on the screen.

       The method is a helper function of the function _animateAll.
       """
       if self._bg!=None:
           self._bg.draw(self.view)

    def _animateShips(self):
       """
       Animates the ships on the screen.

       The method is a helper function of the function draw.
       """
       if self._listOfShips!=None:
           for i in self._listOfShips:
               i.draw(self.view)

    def _animateAll(self):
       """
       Animates the score, the number of lives left, and the objects of GImages
       on the screen.

       The method is a helper function of the function draw.
       """
       self._animateBg()
       self._animateTextScore()
       self._animateTextLives()
