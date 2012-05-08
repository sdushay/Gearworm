from kivy.app import App
from random import random, randint
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
import math

class SwipeWidget(Widget):
	def on_touch_down(self, touch):
		with self.canvas:
			Color(random(), 1, 1, mode='hsv')
			d = 30.
			touch.ud['origX'] = touch.x
			touch.ud['origY'] = touch.y
			touch.ud['line'] = Line(points=(touch.x, touch.y))
			
	def on_touch_move(self, touch):
		touch.ud['line'].points += [touch.x, touch.y]
		
	def on_touch_up(self, touch):
		self.canvas.clear()
		diffX = touch.x - touch.ud['origX']
		diffY = touch.y - touch.ud['origY']
		if diffX != 0 or diffY != 0:
			angle = 180 / 3.14 * math.atan2(diffY, diffX)
			print angle
			if angle < 45 and angle > -45:
				swpdir = "right"
				print "right"	
			elif angle < -45 and angle > -135:
				swpdir = "down"
				print "down"
			elif angle < -135 or angle > 135:
				swpdir = "left"
				print "left"
			else:
				swpdir = "up"
				print "up"
			

class ChipApp(App):
	def build(self):
		swipeW = SwipeWidget()
		#Snake()
		return swipeW


'''

class gear(Widget):
	def __init__(self, attached):
		images = ["gearblue.png", "gearred.png", "gearyellow.png", "geargreen.png", "gearpink.png", "gearblue.png"]
		chooser = randint(0,5)
		self.image = images[chooser]
		colors = ["blue", "red", "yellow", "green", "pink", "blue"]
		self.color = colors[chooser]
		self.lifespan = randint(3,6)
		self.attached = attached
		self.pos
		
			

class Snake(Widget):
	def __init__(self):
		self.images = ["head.png", "tail.png"]
		self.length = 3
		self.speed = (0, -1)
		
		# head maintains the position of the head
		self.head = (200, 200)
		self.body = []
		for i in range(0,2):
			snake.append(gear(True))
	
	def update(self, screen): 
		# Direction Queue
		
		DQ = []
	
		# Event Handling
		
		if swpdir == "up":
			DQ.append(("up", head))
			speed = (0, -1)
		if swpdir == "left":
			DQ.append(("left", head))
			speed = (-1, 0)
		if swpdir == "down":
			DQ.append(("down", head))
			speed = (0, 1)
		if swpdir == "right":
			DQ.append(("right", head))
			speed = (1, 0)
		
		# moving the snake
		for g in self.body:
			if gear.pos
			

	def cleave(self):
		for l in range(0, length-2):
			if snake[l].color == snake[l+1].color and snake[l+1].color == snake[l+2].color:
				snake.remove(l, l+1, l+2)

 '''

		
if __name__ == '__main__':
	ChipApp().run()
