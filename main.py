import pyglet, math, ctypes, numpy, os
from pyglet.gl import *
from OpenGL.GLUT import *


def glut_string(x, y, text, color = [1,1,1]):
	"""Draw a string using GLUT functions."""
	glutInit()
	glColor3f(color[0], color[1], color[2])
	glRasterPos2f(x,y)
	for ch in text:
		glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ctypes.c_int(ord(ch)))

def circle(x, y, radius):
    iterations = int(2*radius*math.pi)
    s = math.sin(2*math.pi / iterations)
    c = math.cos(2*math.pi / iterations)

    dx, dy = radius, 0

    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)
    for i in range(iterations+1):
        glVertex2f(x+dx, y+dy)
        dx, dy = (dx*c - dy*s), (dy*c + dx*s)
    glEnd()

class graph_window(pyglet.window.Window):
	def __init__(self, equation, x_min, x_max, *args, **kwargs):
		super(graph_window, self).__init__(*args, **kwargs)

		#Stores x & y values.
		self.values = [[],[]]

		#Our equation(sys.argv[1])
		self.equation = lambda x: eval(equation)

		#x boundaries for the equation, adjust via x_mix(sys.argv[2]) and x_max(sys.argv[3])
		for i in numpy.arange(float(x_min), float(x_max), 0.1):
			self.values[0].append(i)

		#y variable, got via the equation.
		for each_value in self.values[0]:
			self.values[1].append(self.equation(each_value))

		#Other varibales
		self.MULT = 50 				 #we have to adjust (x, y) values because they are too small 

		self.ADD_X = self.width / 2  #ADD_X and ADD_Y exist because we need to adjust point positions
		self.ADD_Y = self.height / 2 #because we cannot translate point origin like in p5 framework

		self.point_index = 0 		 #each (x, y) pair has an index which we use for drawing the current point

		ctypes.windll.kernel32.SetConsoleTitleW('Equation: {} | Boundaries: {} to {}'.format(equation, x_min, x_max))
		print('Point table:')
		for i in range(len(self.values[0])):
			print('x: {} | y: {}'.format(self.values[0][i], self.values[1][i]))

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

		#Draws the base graph.
		glBegin(GL_LINES)
		glVertex2f(0, self.ADD_Y)
		glVertex2f(self.ADD_X * 2, self.ADD_Y)
		glEnd()
		glBegin(GL_LINES)
		glVertex2f(self.ADD_X,  15)
		glVertex2f(self.ADD_X, self.ADD_Y * 2)
		glEnd()

		#Draws a line which separates the graph and current point coordinates string.
		glBegin(GL_LINES)
		glVertex2f(0,  15)
		glVertex2f(self.ADD_X * 2, 15)
		glEnd()

		#Draws the equation.
		glBegin(GL_LINES)
		for i in range(len(self.values[0]) - 1):
			glVertex2f(self.values[0][i] * self.MULT + self.ADD_X, self.values[1][i] * self.MULT + self.ADD_Y)
			glVertex2f(self.values[0][i + 1] * self.MULT + self.ADD_X, self.values[1][i + 1] * self.MULT + self.ADD_Y)
		glEnd()

		#Draws lines on the axes
		glBegin(GL_LINES)
		for i in range(8):
			glVertex2f(i * self.MULT + self.ADD_X, .2 * self.MULT + self.ADD_Y)
			glVertex2f(i * self.MULT + self.ADD_X, -.2 * self.MULT + self.ADD_Y)
		glEnd()
		glBegin(GL_LINES)
		for i in range(8):
			glVertex2f(-i * self.MULT + self.ADD_X, .2 * self.MULT + self.ADD_Y)
			glVertex2f(-i * self.MULT + self.ADD_X, -.2 * self.MULT + self.ADD_Y)
		glEnd()
		glBegin(GL_LINES)
		for i in range(7):
			glVertex2f(.2 * self.MULT + self.ADD_X, i * self.MULT + self.ADD_Y)
			glVertex2f(-.2 * self.MULT + self.ADD_X, i * self.MULT + self.ADD_Y)
		glEnd()
		glBegin(GL_LINES)
		for i in range(6):
			glVertex2f(.2 * self.MULT + self.ADD_X, -i * self.MULT + self.ADD_Y)
			glVertex2f(-.2 * self.MULT + self.ADD_X, -i * self.MULT + self.ADD_Y)
		glEnd()

		#Draws a filled circle arround the current point index.
		glPushAttrib(GL_CURRENT_BIT)
		glColor3f(1,0,0)
		circle(self.values[0][self.point_index] * self.MULT + + self.ADD_X, self.values[1][self.point_index] * self.MULT + + self.ADD_Y, 5)
		glPopAttrib()


		#Draws point coordinates.
		glut_string(0, 2, 'Current Point: {}, {}'.format(self.values[0][self.point_index], self.values[1][self.point_index]))

if __name__ == "__main__":
	graph_window(sys.argv[1], sys.argv[2], sys.argv[3], width=700, height=600,caption='Graph Tool')
	pyglet.app.run()
