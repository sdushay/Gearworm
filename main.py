from kivy.app import App
from random import random, randint
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from math import sin
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from functools import partial
import math

class Music(Widget):
	sound = None

	def start(self):
		if self.sound is None:
			self.sound = SoundLoader.load("music.ogg")
			self.sound.volume = 0.8
			self.sound.play()
			self.sound.on_stop = self.sound.play
				
'''class gear(Widget):
	def __init__(self, attached):
		images = ["gearblue.png", "gearred.png", "gearyellow.png", "geargreen.png", "gearpink.png", "gearblue.png"]
		chooser = randint(0,5)
		self.image = images[chooser]
		colors = ["blue", "red", "yellow", "green", "pink", "blue"]
		self.color = colors[chooser]
		self.lifespan = randint(3,6)
		self.attached = attached
		self.pos				
'''
class Gear(Widget):
	attached = False
	images = ["gearblue.png", "gearred.png", "gearyellow.png", "geargreen.png", "gearpink.png"]
	def setup(self):
		self.color = randint(1, 5)
		self.pos = (randint(1, Window.size[0]), randint(1, Window.size[1]))
		with self.canvas:
			self.image = Rectangle(size=(30,30), pos=self.pos, source=images[color])
				
class Snake(Widget):
	gears = []
	dir = "none"
	def setup(self):
		self.pos = (Window.center[0], Window.center[1])
		self.velocity = 5
		with self.canvas:
			self.head = Rectangle(size=(30,30), pos=self.pos, source='assets/head.png')
		
	def update(self, dt):
		if self.dir == "up":
			self.head.pos = (self.head.pos[0], self.head.pos[1] + self.velocity)
		elif self.dir == "down":
			self.head.pos = (self.head.pos[0], self.head.pos[1] - self.velocity)
		elif self.dir == "left":
			self.head.pos = (self.head.pos[0] - self.velocity, self.head.pos[1])
		elif self.dir == "right":
			self.head.pos = (self.head.pos[0] + self.velocity, self.head.pos[1])
		
	
class SnookGame(Widget):
	snake = Snake()
	dir = "none"
	score = 0
	def start(self):
		self.add_widget(self.snake)
		self.snake.setup()
		Clock.schedule_interval(self.snake.update, 1.0/60.0)
	
	def create_gear(self, dt):
		pass
	
	def on_touch_down(self, touch):
		with self.canvas:
			Color(random(), 1, 1, mode='hsv')
			d = 30.
			touch.ud['origX'] = touch.x
			touch.ud['origY'] = touch.y
		
	def on_touch_up(self, touch):
		diffX = touch.x - touch.ud['origX']
		diffY = touch.y - touch.ud['origY']
		if diffX != 0 or diffY != 0:
			angle = 180 / 3.14 * math.atan2(diffY, diffX)
			if angle < 45 and angle > -45:
				self.snake.dir = "right"
			elif angle < -45 and angle > -135:
				self.snake.dir = "down"
			elif angle < -135 or angle > 135:
				self.snake.dir = "left"
			else:
				self.snake.dir = "up"
		
				
class SnookMenu(Widget):
	pass
		
class SnookRoot(Widget):
	STATE_MENU = 0
	STATE_PLAY = 1
	STATE_LOSE = 2
	
	def start(self):
		self.state = SnookRoot.STATE_MENU
		self.menu = SnookMenu()
		self.menu.size = Window.size
		self.add_widget(self.menu)
		
	def start_game(self):
		self.state = SnookRoot.STATE_PLAY
		self.remove_widget(self.menu)
		print "here"
		self.game = SnookGame()
		self.game.start()
		self.add_widget (self.game)

class SnookApp(App):
	icon = 'assets/icon.png'
	def build(self):
		root = SnookRoot()
		root.size = Window.size
		root.start()
		return root


'''


		
			

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
	SnookApp().run()
