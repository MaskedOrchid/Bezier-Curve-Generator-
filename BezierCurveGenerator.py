#!/usr/bin/python3
#-*-python-*-##################################################################
# Copyright (C) 2021 by Leland Smith
#
#   This program is free software: you can redistribute it and/or modify it
#   under the terms of the GNU General Public License as published by the Free
#   Software Foundation, either version 3 of the License, or (at your option)
#   any later version.
#
#   This program is distributed in the hope that it will be useful, but WITHOUT
#   ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#   FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#   more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################

"""
This Python script can generate Bézier curves up to the nth power. Although,
I can not guarantee that it will work with n powers above 6.

The code is heavily commented in hopes that you can understand it a bit more
easily.

The script should work equally well on MacOS, Linux, and Windows.

"""

###############################################################################
# Import:
#

# The line below installs the WX GUI toolkit.  You can install this toolkit
# using the command:
#
#     python3 -m pip install wxPython
#
import wx

import math

# from wx.core import Height

###############################################################################
# Globals:
#

VERSION = "1.0"
"""
The script version number.

"""

DEFAULT_TITLE = "Bezier Curve"
"""
The example window default title.

"""

DEFAULT_SIZE = wx.DefaultSize
"""
The default window size.

"""

###############################################################################
# Class DrawingCanvas:
#

class DrawingCanvas(wx.Frame):
    """
    Class that creates a simple frame with a canvas we can draw on.

    """

    def __init__(
        self,
        window_title = DEFAULT_TITLE,
        window_size = DEFAULT_SIZE
        ):
        """
        Method that initializes the DrawingCanvas class.
        """

        # Initialize the base class
        wx.Frame.__init__(
            self,
            parent = None,
            id = wx.ID_ANY,
            title = window_title,
            pos = wx.DefaultPosition,
            size = window_size,
            style = wx.DEFAULT_FRAME_STYLE,
            name = "DrawingCanvas"
        )

        self.window_size=window_size

        # This places the window in the center of the display.
        self.Centre(direction = wx.BOTH)

        # For grins, we create a simple menu bar so you see how to do that with
        # wxPython

        self.menu_bar = wx.MenuBar()
        self.SetMenuBar(self.menu_bar)

        # And let's create two menu options under a "File" menu.  Note that
        # MacOS will relocate menu options to conform with MacOS GUI standards.
        self.file_menu = wx.Menu()
        self.file_new_option = self.file_menu.Append(
            -1,
            "&New...",
            "Create a new canvas."
        )
        self.file_exit_option = self.file_menu.Append(wx.ID_EXIT)

        self.menu_bar.Append(self.file_menu, "&File")

        # We now bind events to event handling methods.
        self.Bind(wx.EVT_PAINT, self.paint)
        self.Bind(wx.EVT_CLOSE, self.window_close)
        self.Bind(wx.EVT_LEFT_DOWN, self.left_button_down)
        self.Bind(wx.EVT_LEFT_UP, self.left_button_up)
        self.Bind(wx.EVT_MOTION, self.mouse_move)

        self.Bind(wx.EVT_MENU, self.file_new, self.file_new_option)
        self.Bind(wx.EVT_MENU, self.file_exit, self.file_exit_option)

        # This is a position value we use for the demo.
        self.current_position = wx.Point(0, 0)
        self.P = [
            [210, 135 ],
            [ 200, 205],
            [ 130,110],
            [200, 100 ],
            [210, 50]
        ]
#Above, these are the X and Y values of our points. Note that these 
#values are equal to pixels on the screen.

    def paint(self, event = None):
        """
        Method that is triggered to paint this window.

        :param event:
            The event that triggered this event handler.

        :type event: wx.PaintEvent
        """

        # We start by creating a paint device context.  We'll use this to draw
        # on our frame.  We tell the device context what we want to draw on (
        # which is, of course, this frame or "self").
        #
        # See https://wxpython.org/Phoenix/docs/html/wx.DC.html for a complete
        # list of methods we can use with a device context.
        dc = wx.PaintDC(self)

        # Clear out any settings in the device context.
        dc.Clear()

        # Create a nice pen for drawing.
        pen = wx.Pen(
            colour = wx.Colour(255, 0, 10),
            width = 3,
            style = wx.PENSTYLE_SOLID
        )
        h=dc.GetSize().height
        # Set a drawing pen we'll use.
        dc.SetPen(pen)


        dc.DrawCircle(210,h-135,3)
        dc.DrawCircle(200,h-205,3)
        dc.DrawCircle(130,h-110,3)
        dc.DrawCircle(200,h-100,3)
        dc.DrawCircle(210,h-50,3)

        # And draw a line
        #dc.DrawLine(
            #x1 = 0,
            #y1 = 0,
            #x2 = self.current_position.x,
            #y2 = self.current_position.y
        #)
        pen = wx.Pen(
            colour = wx.Colour(0, 0, 0),
            width = 2,
            style = wx.PENSTYLE_SOLID
        )
        dc.SetPen(pen)

        Ox = 0
        Oy = 0
        
        #Bezier Curves
        n=4
        for it in range(100):
            t= it / 100.0
            Sx = 0
            Sy = 0
            for i in range(n+1):
                b=math.comb(n,i)
                Sx = Sx + b * ((1-t)**(n-i)) * (t**i) * self.P[i][0]
                Sy = Sy + b * ((1-t)**(n-i)) * (t**i) * self.P[i][1]
                #print ("lee")
                #print (Sx,Sy )

            if Ox != 0 and Oy != 0:
                dc.DrawLine(Ox, h-Oy, Sx, h-Sy)

            Ox = Sx
            Oy = Sy

        #print (h)
        #print (b)
        #print (self.P)
    
        # Let's also put some text on the window.  We start by defining a font
        # to be used.
        font = wx.Font(
            8, # point size
            family = wx.FONTFAMILY_DEFAULT,
            style = wx.FONTSTYLE_NORMAL,
            weight = wx.FONTWEIGHT_NORMAL,
            underline = False
        )

        # Set the font.
        dc.SetFont(font)

        text = "(%d,%d)"%(self.current_position.x, self.current_position.y)
        dc.DrawText(
            text = text,
            x = self.current_position.x,
            y = self.current_position.y
        )


    def left_button_down(self, event = None):
        """
        Method that is triggered when the left button is pressed.

        :param event:
            The event that triggered this event handler.

        :type event: wx.MouseEvent

        """

        print("left button down")
        event.Skip()


    def left_button_up(self, event = None):
        """
        Method that is triggered when the left button is released.

        :param event:
            The event that triggered this event handler.

        :type event: wx.MouseEvent

        """

        print("left button up")
        event.Skip()


    def mouse_move(self, event = None):
        """
        Method that is triggered when the moose is moved.

        :param event:
            The event that triggered this event handler.

        :type event: wx.MouseEvent

        """

        # Create a device context for this frame.
        dc = wx.ClientDC(self)

        # Get the moose location - the position is a wx.Point instance.
        position = event.GetLogicalPosition(dc)

        # Save of the mouse position for our paint event.
        self.current_position = position

        # And show the result (for grins)
        #print("moved to: %s, %s"%(position.x, position.y))

        # Force us to perform a repaint from the event loop.
        self.Refresh()

        # And, skip any further processing of the event.
        event.Skip()


    def window_close(self, event):
        """
        Method that is triggered when the user attempts to close this window.

        :param event:
            The event that triggered the close.

        :type event: wx.CloseEvent

        """

        # This method is entered when we attempt to close the window.
        # We can either not trigger this method or destroy the window within
        # this method as we do below.

        self.Destroy()


    def file_new(self, event):
        """
        Method that is triggered when the user selects File | New...

        :param event:
            The event that triggered this call.

        :type event: wx.MenuEvent

        """

        print("File | New...")


    def file_exit(self, event):
        """
        Method that is triggered when the user selects File | Quit...

        :param event:
            The event that triggered this call.

        :type event: wx.MenuEvent

        """

        print("File | Quit...")

        # The line below requests that the window close.
        self.Close()

###############################################################################
# Class DrawingApplication:
#

class DrawingApplication(wx.App):
    """
    The main drawing application class.

    """

    def __init__(self):
        """
        Method that initializes the drawing application.

        """

        # Initialize the application base class.
        wx.App.__init__(self)


    def OnInit(self):
        """
        Method that is triggered after the application instance completes to
        initialize any required GUI elements.

        """

        # Call the base class implementation
        wx.App.OnInit(self)

        # Create a drawing canvas instance that is tied to the application.
        self.canvas = DrawingCanvas(
            window_title = "Bezier Curve",
            window_size = DEFAULT_SIZE
        )

        # And make certain the canvas window is visible.
        self.canvas.Show()

        return True

###############################################################################
# Main:
#

if __name__ == "__main__":
    # This line sets up our application instance.  The application instance
    # manages an event loop
    application = DrawingApplication()

    # And run our main event loop.
    application.MainLoop()
