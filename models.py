"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything
that you interact with on the screen is model: the ship, the laser bolts, and
the aliens.

Just because something is a model does not mean there has to be a special class
for it.  Unless you need something special for your extra gameplay features,
Ship and Alien could just be an instance of GImage that you move across the
screen. You only need a new class when you add extra features to an object.
So technically Bolt, which has a velocity, is really the only model that needs
to have its own class.

With that said, we have included the subclasses for Ship and Aliens. That is
because there are a lot of constants in consts.py for initializing the objects,
and you might want to add a custom initializer.  With that said, feel free to
keep the pass underneath the class definitions if you do not want to do that.

You are free to add even more models to this module.  You may wish to do this
when you add new features to your game, such as power-ups.  If you are unsure
about whether to make a new class or not, please ask on Piazza.

# Xiaolu Zhang xz327 Haomiao Liu hl745
# Dec 4th
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other
# than consts.py.  If you need extra information from Gameplay, then it should
# be a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships
    dimensions. These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a ship
    just means changing the x attribute (which you can do directly), you want
    to prevent the player from moving the ship offscreen.  This is an ideal
    thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We do not
    require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to keep
    this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those inherited
    by GImage. You would only add attributes if you needed them for extra
    gameplay features (like animation). If you add attributes, list them below.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getX(self):
        """
        Returns the x-coordinate of the ship.

        The method returns the attribute x directly. Any changes made to its
        x position will modify the value returned.
        """
        return self.x

    def getY(self):
        """
        Returns the y-coordinate of the ship.

        The method returns the attribute y directly. Any changes made to its
        y position will modify the value returned.
        """
        return self.y

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self,x,y,w,h,source):
        """
        Initializes the ship.

        Parameter x: the x-coordinate of the center of the ship
        Precondition: x is an int; SHIP_WIDTH/2 <= x <=GAME_WIDTH-SHIP_WIDTH/2

        Parameter y: the y-coordinate of the center of the ship
        Precondition: y is an int; y=SHIP_BOTTOM + SHIP_HEIGHT/2

        Parameter w: the width of the ship
        Precondition: w is an int = SHIP_WIDTH

        Parameter h: the height of the ship
        Precondition: h is an int = SHIP_HEIGHT

        Parameter source: the source of the photo
        Precondition: source is a png image.
        """
        super().__init__(x=x,y=y,width=w,height=h,source=source)

    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def collides(self,bolt):
        """
        Returns: True if the bolt was fired by the player and collides with this
        alien.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        upperleft_x=bolt.getX()-BOLT_WIDTH/2
        upperleft_y=bolt.getY()+BOLT_HEIGHT/2
        upperright_x=bolt.getX()+BOLT_WIDTH/2
        upperright_y=bolt.getY()+BOLT_HEIGHT/2
        lowerleft_x=bolt.getX()-BOLT_WIDTH/2
        lowerleft_y=bolt.getY()-BOLT_HEIGHT/2
        lowerright_x=bolt.getX()+BOLT_WIDTH/2
        lowerright_y=bolt.getY()-BOLT_HEIGHT/2
        para1= (self.contains([upperleft_x,upperleft_y]) or
        self.contains([upperright_x,upperright_y]) or
        self.contains([lowerleft_x,lowerleft_y]) or
        self.contains([lowerright_x,lowerright_y]))
        para2= not bolt.isPlayerBolt()
        return para1 and para2

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def changeX(self,value):
        """
        The method sets increases the ship's x-coordinate by value.
        """
        self.x+=value


class Alien(GSprite):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien
    dimensions. These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We do
    not require this. You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide with
    different bolts. Ships collide with Alien bolts, not Ship bolts. And Aliens
    collide with Ship bolts, not Alien bolts. An easy way to keep this straight
    is for this class to have its own collision method.

    However, there is no need for any more attributes other than those inherited
    by GImage. You would only add attributes if you needed them for extra
    gameplay features (like giving each alien a score value). If you add
    attributes, list them below.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getX(self):
        """
        Returns the x-coordinate of the alien.

        The method returns the attribute x directly. Any changes made to its
        x position will modify the value returned.
        """
        return self.x

    def getY(self):
        """
        Returns the y-coordinate of the alien.

        The method returns the attribute y directly. Any changes made to its
        y position will modify the value returned.
        """
        return self.y

    def getFrame(self):
        """
        Returns the frame of the alien.

        The method returns the attribute frame directly. Any changes made to its
        y position will modify the value returned.
        """
        return self.frame

    def setFrame(self,value):
        """
        The method that sets the attribute frame to the parameter value.

        Parameter value: the value of the alien's frame
        Precondition: value is a number
        """
        self.frame=value

    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self,x,y,w,h,source,format=(3,2)):
        """
        Initializes the alien.

        Parameter x: the x-coordinate of the center of the alien
        Precondition: x is an int; ALIEN_WIDTH/2 <= x <=GAME_WIDTH-ALIEN_WIDTH/2

        Parameter y: the y-coordinate of the center of the alien
        Precondition: y is an int;
        DEFENSE_LINE+ALIEN_WIDTH/2<=y<=GAME_HEIGHT-ALIEN_CEILING+ALIEN_HEIGHT/2

        Parameter w: the width of the alien
        Precondition: w is an int = ALIEN_WIDTH

        Parameter h: the height of the alien
        Precondition: h is an int = ALIEN_HEIGHT

        Parameter source: the source of the photo
        Precondition: source is a png image.
        """
        super().__init__(x=x,y=y,width=w,height=h,source=source,format=(3,2))

    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides(self,bolt):
        """
        Returns: True if the bolt was fired by the player and collides with this
                 alien. False otherwise.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        upperleft_x=bolt.getX()-BOLT_WIDTH/2
        upperleft_y=bolt.getY()+BOLT_HEIGHT/2
        upperright_x=bolt.getX()+BOLT_WIDTH/2
        upperright_y=bolt.getY()+BOLT_HEIGHT/2
        lowerleft_x=bolt.getX()-BOLT_WIDTH/2
        lowerleft_y=bolt.getY()-BOLT_HEIGHT/2
        lowerright_x=bolt.getX()+BOLT_WIDTH/2
        lowerright_y=bolt.getY()-BOLT_HEIGHT/2
        para1= (self.contains([upperleft_x,upperleft_y]) or
        self.contains([upperright_x,upperright_y]) or
        self.contains([lowerleft_x,lowerleft_y]) or
        self.contains([lowerright_x,lowerright_y]))
        para2=bolt.isPlayerBolt()
        return para1 and para2

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def changeY(self,value):
        """
        The method sets increases the ship's y-coordinate by value.
        """
        self.y+=value

    def changeX(self,value):
        """
        The method sets increases the ship's x-coordinate by value.
        """
        self.x+=value

    def changeFrame(self):
        """
        The method that adds one to the attribute, and divide it by two.
        """
        self.frame = (self.frame+1) % 2

    def plusFrame(self):
        """
        The method that adds one to the attribute frame.
        """
        self.frame = self.frame+1


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles.  The size of the bolt is
    determined by constants in consts.py. We MUST subclass GRectangle, because
    we need to add an extra attribute for the velocity of the bolt.

    The class Wave will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for the velocities.  That is because the velocity is fixed and
    cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set
    the starting velocity. This __init__ method will need to call the __init__
    from GRectangle as a helper.

    You also MIGHT want to create a method to move the bolt.  You move the bolt
    by adding the velocity to the y-position.  However, the getter allows Wave
    to do this on its own, so this method is not required.

    INSTANCE ATTRIBUTES:
        _velocity: The velocity in y direction [int or float]

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getY(self):
        """
        Returns the y-coordinate of the bolt.

        The method returns the attribute y directly. Any changes made to its
        y position will modify the value returned.
        """
        return self.y
    def getX(self):
        """
        Returns the x-coordinate of the bolt.

        The method returns the attribute x directly. Any changes made to its
        x position will modify the value returned.
        """
        return self.x

    # INITIALIZER TO SET THE VELOCITY
    def __init__(self,x,y,w,h,fillcolor,velocity):
        """
        Initializes the bolt.

        Parameter x: the x-coordinate of the center of the bolt
        Precondition: x is an int or float;
        BOLT_WIDTH/2 <= x <=GAME_WIDTH-BOLT_WIDTH/2

        Parameter y: the y-coordinate of the center of the bolt
        Precondition: y is an int or float;
        BOLT_HEIGHT/2 <= y <= GAME_HEIGHT-BOLT_HEIGHT/2

        Parameter w: the width of the bolt
        Precondition: w is an int or float; w=BOLT_WIDTH

        Parameter h: the height of the bolt
        Precondition: h is an int or float; h=BOLT_HEIGHT

        Parameter fillcolor: the color of the bolt
        Precondition: fillcolor is a valid color name.

        Parameter velocity: the velocity of the bolt.
        Precondition: velocity is an int or float; velocity=BOLT_SPEED
        """
        super().__init__(x=x,y=y,width=w,height=h,fillcolor=fillcolor)
        self._velocity=velocity

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def isPlayerBolt(self):
        """
        return true if it's player's bolt. False otherwise.

        The method checks the speed of the bolt. It returns True if the speed
        is positive.
        """
        return self._velocity>0

    def changeY(self,value):
        """
        The method sets increases the bolt's y-coordinate by value.
        """
        self.y+=value


# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
class ShipsOption(GImage):
    """
    This is the class for options of ships. We have three options of ship for
    users to choose from.

    Attributes are all inherited from the super class GImage.
    """
    def __init__(self,x,y,w, h,source):
        """
        Initializes the images of ships' options.

        Parameter x: the x-coordinate of the center of images of ships' options
        Precondition: x is an int or a float

        Parameter y: the y-coordinate of the center of images of ships' options
        Precondition: y is an int or a float

        Parameter w: the width of the images of ships' options
        Precondition: w is an int or a float

        Parameter h: the height of the images of ships' options
        Precondition: h is an int or a float

        Parameter source: the source of the photo
        Precondition: source is a png image.
        """
        super().__init__(x=x,y=y,width=w,height=h,source=source)


class BarrierWall(GSprite):
    """
    This is the class for barrier wall.

    INSTANCE ATTRIBUTES:
        _counter: used to count the number of collision with the bolts[int]
    """
    def getCounter(self):
        """
        Returns the counter of the barrier wall.

        The method returns the attribute counter directly. Any changes made to
        its counter will modify the value returned.
        """
        return self._counter

    def getX(self):
        """
        Returns the x-coordinate of the barrier wall.

        The method returns the attribute x directly. Any changes made to its
        x position will modify the value returned.
        """
        return self.x

    def getY(self):
        """
        Returns the y-coordinate of the barrier wall.

        The method returns the attribute y directly. Any changes made to its
        x position will modify the value returned.
        """
        return self.y

    def getFrame(self):
        """
        Returns the frame of the alien.

        The method returns the attribute frame directly. Any changes made to its
        frame will modify the value returned.
        """
        return self.frame

    def __init__(self,x,y,w,h,source,format=(2,2),counter=0):
        """
        Initializes the images of barrier walls

        Parameter x: the x-coordinate of the center of images of barrier walls
        Precondition: x is an int or a float

        Parameter y: the y-coordinate of the center of images of barrier walls
        Precondition: y is an int or a float

        Parameter w: the width of the images of barrier walls
        Precondition: w is an int or a float

        Parameter h: the height of the images of barrier walls
        Precondition: h is an int or a float

        Parameter source: the source of the photo
        Precondition: source is a png image.

        Parameter counter: used to count the number of collision with the bolts
        Precondition: counter is an int.
        """
        super().__init__(x=x,y=y,width=w,height=h,source=source,format=(2,2))
        self._counter=0

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def addCounter(self):
        """
        The method that adds one the attribute counter.
        """
        self._counter+=1

    def setCounter(self,value):
        """
        The method sets the attribute _counter to the parameter value.

        Parameter value: used to count the number of collision with the bolts
        Precondition: value is an int.
        """
        self._counter=value

    def addFrame(self):
        """
        The method that adds one to the attribute frame if frame is less than 3.
        """
        if self.frame < 3:
            self.frame=self.frame+1

    def collides(self,bolt):
        """
        Returns: True if the bolt was fired by the player and collides with this
        alien.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        upperleft_x=bolt.getX()-BOLT_WIDTH/2
        upperleft_y=bolt.getY()+BOLT_HEIGHT/2
        upperright_x=bolt.getX()+BOLT_WIDTH/2
        upperright_y=bolt.getY()+BOLT_HEIGHT/2
        lowerleft_x=bolt.getX()-BOLT_WIDTH/2
        lowerleft_y=bolt.getY()-BOLT_HEIGHT/2
        lowerright_x=bolt.getX()+BOLT_WIDTH/2
        lowerright_y=bolt.getY()-BOLT_HEIGHT/2
        para1= (self.contains([upperleft_x,upperleft_y]) or
        self.contains([upperright_x,upperright_y]) or
        self.contains([lowerleft_x,lowerleft_y]) or
        self.contains([lowerright_x,lowerright_y]))
        return para1
