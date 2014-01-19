# controller.py
# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""Primary module for Breakout application

This module contains the controller class for the Breakout application.
There should not be any need for additional classes in this module.
If you need more classes, 99% of the time they belong in the model 
module. If you are ensure about where a new class should go, post a
question on Piazza."""
from constants import *
from game2d import *
from model import *
import sys

class Breakout(Game):
    """Instance is a Breakout Application
    
    This class extends Game and implements the various methods necessary 
    for running the game.
    
        Method init starts up the game.
        
        Method update updates the model objects (e.g. move ball, remove bricks)
        
        Method draw displays all of the models on the screen
    
    Because of some of the weird ways that Kivy works, you do not need to make
    an initializer __init__ for this class.  Any initialization should be done
    in the init method instead.
    
    Most of the work handling the game is actually provided in the class Model.
    Model should have a method called moveBall() that moves the ball and processes
    all of the game physics. This class should simply call that method in update().
    
    The primary purpose of this class is managing the game state: when is the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.
    
    Instance Attributes:
        view:   the game view, used in drawing 
                [Immutable instance of GView, it is inherited from Game]
        _state: the current state of the game
                [one of STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, 
                 STATE_ACTIVE, or STATE_COMPLETE]
        _model: the game model, which stores the paddle, ball, and bricks
                [GModel, or None if there is no game currently active
                 It is only None if _state is STATE_INACTIVE]
    
    You may have more attributes if you wish (you might need an attribute to store
    any text messages you display on the screen). If you add new attributes, they
    need to be documented here.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY:
        _msg:   the Welcome message to appear when STATE_INACTIVE
                [Immutable instance of GLabel, inherited from GObject;
                or None when not STATE_INACTIVE]
        _prev:  the previous (x,y) position of a mouse click
                [a GPoint object or None if no previous touch]
        _count: a counter for the frames updated
                [an int >= 0]
    """

    # METHODS
    def init(self):
        """Initialize the game state.
        
        This method is distinct from the built-in initializer __init__.
        This method is called once the game is running. You should use
        it to initialize any game specific attributes.
        
        This method should initialize any state attributes as necessary to
        statisfy invariants. When done, set the _state to STATE_INACTIVE and
        create a message saying that the user should press to play a game."""
        self._state = STATE_INACTIVE
        self._msg = GLabel(text='Press to Play',font_size=34,
                           font_name='Zapfino.ttf', linecolor=TEXT_COLOR,
                           center_x=GAME_WIDTH/2, center_y=GAME_HEIGHT/2,
                           halign='center',valign='middle')
        self._model = None
        self._prev = None
        self._count = 0

    def update(self,dt):
        """Animate a single frame in the game.
        
        It is the method that does most of the work. Of course, it should
        rely on helper methods in order to keep the method short and easy
        to read.  Some of the helper methods belong in this class, and
        others belong in class Model.
        
        The first thing this method should do is to check the state of the
        game. We recommend that you have a helper method for every single
        state: STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, STATE_ACTIVE.
        The game does different things in each state.
        
        In STATE_INACTIVE, the method checks to see if the player clicks
        the mouse. If so, it starts the game and switches to STATE_COUNTDOWN.

        STATE_PAUSED is similar to STATE_INACTIVE. However, instead of 
        restarting the game, it simply switches to STATE_COUNTDOWN.
        
        In STATE_COUNTDOWN, the game counts down until the ball is served.
        The player is allowed to move the paddle, but there is no ball.
        This state should delay at least one second.
        
        In STATE_ACTIVE, the game plays normally.  The player can move the
        paddle and the ball moves on its own about the board.  Both of these
        should be handled by methods inside of class Model (not in the class).
        Model should have methods named movePaddle and moveBall.
        
        While in STATE_ACTIVE, if the ball goes off the screen and there
        are tries left, it switches to STATE_PAUSED.  If the ball is lost 
        with no tries left, or there are no bricks left on the screen, the
        game is over and it switches to STATE_COMPLETE.
        
        While in STATE_COMPLETE, this method displays a message congratulating
        or admonishing the winner/loser before shutting down.
        
        You are allowed to add more states if you wish. Should you do so,
        you should describe them here.
        
        Precondition: dt is the time since last update (a float).  This
        parameter can be safely ignored. It is only relevant for debugging
        if your game is running really slowly."""
        # print str(dt)
        if self._state == STATE_INACTIVE and self.checkClick():
            self._msg=None; self._state=STATE_COUNTDOWN; self._model=Model()
            self._count = 0
        if self._state == STATE_COUNTDOWN:
            self._model.movePaddle(self.view.touch,self._prev);self._count += 1
            if self._count == 240:
                self._state = STATE_ACTIVE; self._model.createBall()
                self._count = 0
        if self._state == STATE_ACTIVE:
            self._model.movePaddle(self.view.touch, self._prev);
            self._model.moveBall()
            if self._model.checkBottom():
                self._model.setLives(-1); self._state = STATE_PAUSED
            if self._model.getBricks() == [] or self._model.getLives() == 0:
                self._state = STATE_COMPLETE
        if (self._state == STATE_PAUSED and self.checkClick()
        and self._model.getLives() > 0):
            self._state = STATE_COUNTDOWN
        if self._state == STATE_COMPLETE:
            self._count += 1
            if self._count == 360:
                sys.exit(0)
                
        #To capture the position of the touch at the end of each frame
        self._prev = self.view.touch

    def draw(self):
        """Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject. 
        To draw a GObject g, simply use the method g.draw(view).  It is 
        that easy!
        
        Many of the GObjects (such as the paddle, ball, and bricks) are
        attributes in Model. In order to draw them, you either need to
        add getters for these attributes or you need to add a draw method
        to class Model.  Which one you do is up to you."""
        self.drawBackground()
        #For STATE_INACTIVE
        if self._state == STATE_INACTIVE:
            self._count += 1; self._msg.draw(self.view)
            if self._count == 10:
                Sound('timpani.wav').play()
        #For STATE_COUNTDOWN
        if self._state == STATE_COUNTDOWN:
            self.drawBricks(); self.drawPaddle(); self.drawCountdown()
        #For STATE_ACTIVE
        elif self._state == STATE_ACTIVE:
            self.drawBall(); self.drawPaddle(); self.drawBricks()
        #For STATE_PAUSED
        elif self._state == STATE_PAUSED:
            self.drawWarning()
        #For STATE_COMPLETE
        elif self._state == STATE_COMPLETE:
            self.drawLose() if self._model.getLives() == 0 else self.drawWin()

    # HELPER METHODS
    def checkClick(self):
        """Returns True if the mouse is clicked (pressed);
        False otherwise"""
        return True if (self.view.touch != None
                        and self._prev == None) else False

    def drawBall(self):
        """Helper function for drawing the ball"""
        self._model.getBall().draw(self.view)

    def drawBricks(self):
        """A helper function for drawing each brick"""
        for bricks in self._model.getBricks():
                bricks.draw(self.view)

    def drawPaddle(self):
        """A helper function for drawing the paddle"""
        self._model.getPaddle().draw(self.view)

    def drawBackground(self):
        """Draws the background image"""
        x = GImage(x=0,y=0,width=GAME_WIDTH,
               height=GAME_HEIGHT,source='2.jpg')
        x.draw(self.view)

    def drawCountdown(self):
        """Runs the countdown timer, displaying the number of seconds left
        until STATE_ACTIVE and the ball is served"""
        if self._count >= ONE_SECOND and self._count < TWO_SECOND:
            three = GLabel(text='3',font_size=44,
                           font_name='Zapfino.ttf', linecolor=TEXT_COLOR,
                           center_x=GAME_WIDTH/2, center_y=GAME_HEIGHT/2,
                           halign='center',valign='middle')
            three.draw(self.view)
        if self._count >= TWO_SECOND and self._count < THREE_SECOND:
            two = GLabel(text='2',font_size=44,
                           font_name='Zapfino.ttf', linecolor=TEXT_COLOR,
                           center_x=GAME_WIDTH/2, center_y=GAME_HEIGHT/2,
                           halign='center',valign='middle')
            two.draw(self.view)
        if self._count >= THREE_SECOND and self._count < FOUR_SECOND:
            one = GLabel(text='1',font_size=44,
                           font_name='Zapfino.ttf', linecolor=TEXT_COLOR,
                           center_x=GAME_WIDTH/2, center_y=GAME_HEIGHT/2,
                           halign='center',valign='middle')
            one.draw(self.view)

    def drawWarning(self):
        """Creates a GLabel with a warning message with the number of
        lives remaining, then draws it"""
        warning = GLabel(text='You have '+str(self._model.getLives())+
                         ' balls remaining! \n Click to Serve',
                        font_size=26, font_name='Zapfino.ttf',
                        linecolor=TEXT_COLOR,center_x=GAME_WIDTH/2,
                        center_y=GAME_HEIGHT/2,halign='center',valign='middle')
        warning.draw(self.view)
    
    def drawWin(self):
        """Draws the winner's message and plays a congratulatory sound
        [http://har-bal.com/reference/brass/trumpets1_mm5000142_256_winamp25e.wav]
        found via the site: http://www.findsounds.com/ISAPI/search.dll"""
        win = GLabel(text='Congratulations!\nYou\'ve won!',
                    font_size=40, font_name='Zapfino.ttf',
                    linecolor=TEXT_COLOR,center_x=GAME_WIDTH/2,
                    center_y=GAME_HEIGHT/2,halign='center',valign='middle')
        win.draw(self.view)
        if self._count == 10:
            Sound('fanfare.wav').play()
    
    def drawLose(self):
        """Draws the loser's message and plays a sad sound
        [http://soundbible.com/grab.php?id=1830&type=wav]
        at site: http://soundbible.com/1830-Sad-Trombone.html"""
        loss = GLabel(text='Sorry, you lost \n\n Please try again!',
                    font_size=34, font_name='Zapfino.ttf',
                    linecolor=TEXT_COLOR,center_x=GAME_WIDTH/2,
                    center_y=GAME_HEIGHT/2,halign='center',valign='middle')
        loss.draw(self.view)
        if self._count == 10:
            Sound('sad_trombone.wav').play()
    