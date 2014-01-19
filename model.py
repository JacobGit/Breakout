# model.py
# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""Model module for Breakout

This module contains the model classes for the Breakout game. Instances of
Model storee the paddle, ball, and bricks.  The model has methods for resolving
collisions between the various game objects.  A lot of your of your work
on this assignment will be in this class.

This module also has an additional class for the ball.  You may wish to add
more classes (such as a Brick class) to add new features to the game.  What
you add is up to you."""
from constants import *
from game2d import *
import random # To randomly generate the ball velocity

class Model(object):
    """An instance is a single game of breakout.  The model keeps track of the
    state of the game.  It tracks the location of the ball, paddle, and bricks.
    It determines whether the player has won or lost the game.  
    
    To support the game, it has the following instance attributes:
    
        _bricks:  the bricks still remaining 
                  [list of GRectangle, can be empty]
        _paddle:  the paddle to play with 
                  [GRectangle, never None]
        _ball:    the ball 
                  [Ball, or None if waiting for a serve]
    
    As you can see, all of these attributes are hidden.  You may find that you
    want to access an attribute in call Breakout. It is okay if you do, but
    you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter and/or
    setter for any attribute that you need to access in Breakout.  Only add
    the getters and setters that you need.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY:
        _lives:   the number of balls remaining
                  [int, <= NUMBER_TURNS and >= 0]
    """


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getBricks(self):
        """Returns the list of brick GRectangle objects"""
        return self._bricks

    def getPaddle(self):
        """Returns the _paddle GRectangle object"""
        return self._paddle

    def getBall(self):
        """Returns the _ball object"""
        return self._ball

    def getLives(self):
        """Returns the number of lives remaining"""
        return self._lives

    def setLives(self, amount):
        """Increments _lives by amount
        Precondition: amount is an int"""
        assert isinstance(amount,int), "Amount must be an integer"
        self._lives += amount

    # INITIALIZER (TO CREATE PADDLES AND BRICKS)
    def __init__(self):
        """Initializes the model, setting the class attributes such that
        they satisfy the class invariants. Should only be called once when
        game enters STATE_COUNTDOWN"""
        self._bricks = []
        self.fillWithBricks()
        self._paddle = GRectangle(x = GAME_WIDTH/2, y=PADDLE_OFFSET,
                                  width = PADDLE_WIDTH, height = PADDLE_HEIGHT,
                                  fillcolor = colormodel.BLACK)
        self._ball = None
        self._lives = NUMBER_TURNS

    # ADD ANY ADDITIONAL METHODS (FULLY SPECIFIED) HERE
    def fillWithBricks(self):
        """Fills the attribute _bricks with rows and columns of GRectangle
        objects as specified by the constants BRICK_ROWS AND BRICKS_IN_ROW"""
        for row in range(BRICK_ROWS):
            for pos in range(BRICKS_IN_ROW):
                self._bricks.append(GRectangle(
                x=(BRICK_SEP_H/2) + BRICK_WIDTH*pos + pos*BRICK_SEP_H,
                y=GAME_HEIGHT-BRICK_Y_OFFSET-BRICK_HEIGHT*row-row*BRICK_SEP_V,
                width=BRICK_WIDTH, height=BRICK_HEIGHT,
                fillcolor = BRICK_COLORS[row%10],
                linecolor=BRICK_COLORS[row%10]))

    def createBall(self):
        """Sets _ball to be a newly created Ball object"""
        self._ball = Ball()

    def movePaddle(self, touch, prev):
        """Sets the x position of _paddle to the x-pos of the paddle plus the
        difference between the x-pos of the current and previous touch. Also
        ensures that the leftmost and rightmost x-values of paddles never
        exceed the bounds of the window.
        
        Precondition: touch and prev are GPoint objects"""
        if touch != None and prev != None:
            self._paddle.center_x += (touch.x - prev.x)
            self._paddle.left = max(0,self._paddle.left)
            self._paddle.right = min(GAME_WIDTH,self._paddle.right)

    def moveBall(self):
        """Moves the ball by incrementing x and y according to velocity
        and handles any physics associated with collisions/bouncing"""
        self._ball.x += self._ball.getVelocity('x')
        self._ball.y += self._ball.getVelocity('y')
        self.wallCollisions()
        if (self._getCollidingObject() == self._paddle and
        self._ball.getVelocity('y') < 0):
            self._ball.negateVelocity('y')
            self.paddleLeftCollisions()
            self.paddleRightCollisions()
        elif (self._getCollidingObject() == self._paddle and
        self._ball.getVelocity('y') > 0):
            pass
        elif self._getCollidingObject() == None:
            pass
        else:
            self._bricks.remove(self._getCollidingObject())
            self._ball.negateVelocity('y')

    def paddleLeftCollisions(self):
        """A helper method for dealing with paddle collisions on the left
        1/4 of the paddle. If it hits with a positive velocity (coming from
        the left), it negates the x velocity. If it hits with a negative
        velocity (from the right), it increments the x velocity slightly"""
        first_quarter = range(int(self._paddle.x),
                              int(self._paddle.x+(.25*PADDLE_WIDTH)))
        for xValues in first_quarter:
            if (self._ball.contains(xValues,PADDLE_OFFSET+PADDLE_HEIGHT)
            and self._ball.getVelocity('x') > 0):
                self._ball.negateVelocity('x')
                return
            elif (self._ball.contains(xValues,PADDLE_OFFSET+PADDLE_HEIGHT)
            and self._ball.getVelocity('x') < 0):
                self._ball.addVelocity(-.5,'x')
                return

    def paddleRightCollisions(self):
        """A helper method for dealing with paddle collisions on the right
        1/4 of the paddle. If it hits with a positive velocity (coming from
        the left), it increments the x velocity slightly. If it hits with
        a negative velocity (from the right), it negates the x velocity"""
        fourth_quarter = range(int(self._paddle.right-.25*PADDLE_WIDTH),
                               int(self._paddle.right))
        for xValues in fourth_quarter:
            if (self._ball.contains(xValues,PADDLE_OFFSET+PADDLE_HEIGHT)
            and self._ball.getVelocity('x') > 0):
                self._ball.addVelocity(.5,'x')
                return
            elif (self._ball.contains(xValues,PADDLE_OFFSET+PADDLE_HEIGHT)
            and self._ball.getVelocity('x') < 0):
                self._ball.negateVelocity('x')
                return

    def wallCollisions(self):
        """Helper function to handle any collisions with walls."""
        if self._ball.top >= GAME_HEIGHT:
            self._ball.negateVelocity('y')
        elif self._ball.right >= GAME_WIDTH and self._ball.getVelocity('x')>0:
            self._ball.negateVelocity('x')
        elif self._ball.left <= 0 and self._ball.getVelocity('x') < 0:
            self._ball.negateVelocity('x')

    def _getCollidingObject(self):
        
        """Returns: GObject that has collided with the ball
    
        This method checks the four corners of the ball, one at a 
        time. If one of these points collides with either the paddle 
        or a brick, it stops the checking immediately and returns the 
        object involved in the collision. It returns None if no 
        collision occurred."""
        for brick in self._bricks:
            if brick.contains(self._ball.x,self._ball.y) or (
                brick.contains(self._ball.x, self._ball.y + BALL_DIAMETER) or
                brick.contains(self._ball.x + BALL_DIAMETER,
                               self._ball.y + BALL_DIAMETER) or
                brick.contains(self._ball.x, self._ball.y + BALL_DIAMETER)):
                return brick
        if (self._paddle.contains(self._ball.x,self._ball.y) or
        self._paddle.contains(self._ball.x, self._ball.y + BALL_DIAMETER)):
            return self._paddle
        else:
            return None

    def checkBottom(self):
        """Returns True if the ball has hit the floor; False otherwise"""
        if self._ball.bottom <= 0:
            return True
        else:
            return False


class Ball(GEllipse):
    """Instance is a game ball.
    
    We extend GEllipse to a ball in order to add attributes for a 
    velocity. This subclass adds these two attributes.
    
    INSTANCE ATTRIBUTES:
        _vx: Velocity in x direction [int or float]
        _vy: Velocity in y direction [int or float]
    
    The class Model will need to access the attributes. You will
    need getters and setters for these attributes.
    
    In addition to the getters and setter, you should add two
    methods to this class: an initializer to set the starting velocity 
    and a method to "move" the ball. The move method should adjust the 
    ball position according to the velocity.
    
    NOTE: The ball does not have to be a GEllipse. It could be an instance
    of GImage (why?). This change is allowed, but you must modify the class
    header up above.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY:
    """

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getVelocity(self, vector):
        """Returns the x or y vector velocity of the ball
        
        Precondition: vector is a string, 'x' or 'y'"""
        assert isinstance(vector, str)
        assert vector == 'x' or vector == 'y', "Vector must be x or y"
        return self._vx if vector == 'x' else self._vy

    # INITIALIZER TO SET VELOCITY
    def __init__(self):
        """Initializes the Ball instance to have a negative starting velocity
        and random magnitude/vector x velocity."""
        GEllipse.__init__(self, x=GAME_WIDTH/2,y=GAME_HEIGHT/2,
                          width=BALL_DIAMETER,height=BALL_DIAMETER,
                          fillcolor=colormodel.RED)
        self._vy = -5.0
        self._vx = random.uniform(1.0,5.0)
        self._vx = self._vx * random.choice([-1, 1])

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def negateVelocity(self, vector):
        """Negates the velocity of vector x or y of the ball
        
        Precondition: vector is a string, 'x' or 'y'"""
        assert isinstance(vector, str)
        assert vector == 'x' or vector == 'y', "Vector must be x or y"
        if vector == 'x':
            self._vx = -self._vx
        else:
            self._vy = -self._vy

    def addVelocity(self, amount, vector):
        """Increments the x or y velocity by amount
        
        Precondition: vector is a string, 'x' or 'y'
        amount is float -2...2"""
        assert isinstance(amount,float) and isinstance(vector,str)
        assert amount > -2 and amount < 2
        assert vector == 'x' or vector == 'y', "vector must be x or y"
        if vector == 'x':
            self._vx += amount
        else:
            self._vy += amount

# ADD ANY ADDITIONAL CLASSES HERE