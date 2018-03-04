__author__ = 'roguezilla'
__version__ = 'release 1.0'

import pyglet, math, ctypes, numpy, time
from pyglet.gl import *
from OpenGL.GLUT import *


def glut_string(x, y, text, color = [1,1,1]):
	"""Draw a string using GLUT functions."""
	glutInit()
	glColor3f(color[0], color[1], color[2])
	glRasterPos2f(x,y)
	for ch in text:
		glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ctypes.c_int(ord(ch)))


class graph_window(pyglet.window.Window):
	def __init__(self, equation, *args, **kwargs):
		super(graph_window, self).__init__(*args, **kwargs)

		"""Stores x:y values."""
		self.values = [[],[]]

		"""Our equation, you are asked to input it when the program starts."""
		self.equation = lambda x: eval(equation)

		"""x variable, adjust for each equation."""
		for i in numpy.arange(-7.95, 8.05, 0.1):
			self.values[0].append(i)

		"""y variable, got by using the input equation."""
		for each_value in self.values[0]:
			self.values[1].append(self.equation(each_value))

		"""Other varibales"""
		self.MULT = 50 				 # the window is pretty big so we need to adjust point values to meet the size

		self.ADD_X = self.width / 2  # ADD_X and ADD_Y exist because we need to adjust point position 
		self.ADD_Y = self.height / 2 # because we start at 0,0 and this way we can move out points to the right point in the graph

		self.point_index = 0 		 # each x and y variable has an index, this is used for drawing a certain point

	def on_key_press(self, button, modifiers):
		if button == pyglet.window.key.ESCAPE: self.close()

		if button == pyglet.window.key.RIGHT:
			self.point_index = self.point_index + 1
			if self.point_index > len(self.values[0]) - 1:
				self.point_index = 0
		
		if button == pyglet.window.key.LEFT:
			self.point_index = self.point_index - 1
			if self.point_index < 0:
				self.point_index = len(self.values[0]) - 1

	def on_draw(self):
		self.clear()

		glClear(GL_COLOR_BUFFER_BIT)
		glLoadIdentity()

		"""Draws the base of graph."""
		glBegin(GL_LINES)
		glVertex2f(0, self.ADD_Y)
		glVertex2f(self.ADD_X * 2, self.ADD_Y)
		glEnd()
		glBegin(GL_LINES)
		glVertex2f(self.ADD_X,  15)
		glVertex2f(self.ADD_X, self.ADD_Y * 2)
		glEnd()

		"""Draws a line which separates graph and a small spot which will be used to draw point coordinates."""
		glBegin(GL_LINES)
		glVertex2f(0,  15)
		glVertex2f(self.ADD_X * 2, 15)
		glEnd()

		"""Draws the equation."""
		glBegin(GL_LINES)
		for i in range(len(self.values[0]) - 1):
			glVertex2f(self.values[0][i] * self.MULT + self.ADD_X, self.values[1][i] * self.MULT + self.ADD_Y)
			glVertex2f(self.values[0][i + 1] * self.MULT + self.ADD_X, self.values[1][i + 1] * self.MULT + self.ADD_Y)
		glEnd()

		"""Draws a square arround the point which corresponds to current point index."""
		glPushAttrib(GL_CURRENT_BIT)
		glColor3f(1,0,0)
		glBegin(GL_QUADS)
		glVertex2f(self.values[0][self.point_index] * self.MULT + self.ADD_X + 5, self.values[1][self.point_index] * self.MULT + self.ADD_Y + 5)
		glVertex2f(self.values[0][self.point_index] * self.MULT + self.ADD_X + 5, self.values[1][self.point_index] * self.MULT + self.ADD_Y - 5)
		glVertex2f(self.values[0][self.point_index] * self.MULT + self.ADD_X - 5, self.values[1][self.point_index] * self.MULT + self.ADD_Y - 5)
		glVertex2f(self.values[0][self.point_index] * self.MULT + self.ADD_X - 5, self.values[1][self.point_index] * self.MULT + self.ADD_Y + 5)
		glEnd()
		glPopAttrib()

		"""Draws point coordinates in the zone mentioned above."""
		glut_string(0, 2, 'Point Coordinates: {}, {}'.format(self.values[0][self.point_index], self.values[1][self.point_index]))

if __name__ == "__main__":
	print('Welcome to Graph Tool by roguezilla.')
	print('You will be asked to input an equation in a moment(input math.cos(x) for example).')
	time.sleep(1)
	graph_window = graph_window(input('Input equation: '), width=800, height=700,caption='Graph Tool')
	pyglet.app.run()