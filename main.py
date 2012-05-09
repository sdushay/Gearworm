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
from kivy.properties import NumericProperty
from kivy.uix.label import Label
import math

class Music(Widget):
	sound = None

	def start(self):
		if self.sound is None:
			self.sound = SoundLoader.load("music.ogg")
			self.sound.volume = 0.8
			self.sound.play()
			self.sound.on_stop = self.sound.play

class Gear(Widget):
	attached = False
	images = ["assets/gearblue.png", "assets/gearred.png", "assets/gearyellow.png", "assets/geargreen.png", "assets/gearpink.png"]
	def setup(self):
		self.colornum = randint(0, 4)
		self.size = (30, 30)
		self.pos = (randint(1, Window.size[0] - 50), randint(1, Window.size[1] - 50))
		with self.canvas:
			self.image = Rectangle(size=(30,30), pos=self.pos, source=self.images[self.colornum])
				
class Snake(Widget):
	gears = []
	dir = "none"
	positions = []
	def setup(self):
		self.pos = (Window.center[0], Window.center[1])
		self.velocity = 30
		self.size= (30, 30)
		self.positions.append(self.pos)
		with self.canvas:
			self.head = Rectangle(size=(30,30), pos=self.pos, source='assets/head.png')
			
	def update(self, dt):
		pos = self.head.pos
		if self.dir == "up":
			self.head.pos = (self.head.pos[0], self.head.pos[1] + self.velocity)
			pos = (self.head.pos[0], self.head.pos[1] - 31)
		elif self.dir == "down":
			self.head.pos = (self.head.pos[0], self.head.pos[1] - self.velocity)
			pos = (self.head.pos[0], self.head.pos[1] + 31)
		elif self.dir == "left":
			self.head.pos = (self.head.pos[0] - self.velocity, self.head.pos[1])
			pos = (self.head.pos[0] + 31, self.head.pos[1])
		elif self.dir == "right":
			self.head.pos = (self.head.pos[0] + self.velocity, self.head.pos[1])
			pos = (self.head.pos[0] - 31, self.head.pos[1])
		self.positions.insert(0, pos)
		self.positions.pop(len(self.positions)-1)
		for i in range(0, len(self.positions) - 1):
			self.gears[i].pos = self.positions[i]
			self.gears[i].image.pos = self.gears[i].pos
		self.pos = self.head.pos
		for g in self.gears:
			if g.collide_widget(self):
				self.parent.parent.end_game()
		if self.pos[0] < 0 or self.pos[0] + 30 > Window.size[0] or self.pos[1] < 0 or self.pos[1] + 30 > Window.size[1]:
			self.parent.parent.end_game()
		
class SnookGame(Widget):
	snake = Snake()
	dir = "none"
	score = NumericProperty(0)
	allgears = []
	def start(self):
		self.add_widget(self.snake)
		gear = Gear()
		gear.setup()
		self.allgears.append(gear)
		self.add_widget(gear)
		self.snake.setup()
		Clock.schedule_interval(self.snake.update, .1)
		Clock.schedule_interval(self.create_gear, 2)
		Clock.schedule_interval(self.check_collisions, 1.0 / 60.0)
		
	def check_collisions(self, dt):
		for gear in self.allgears:
			if gear.collide_widget(self.snake):
				self.remove_widget(gear)
				self.allgears.remove(gear)
				self.snake.gears.append(gear)
				self.snake.add_widget(gear)
				pos = self.snake.positions[len(self.snake.positions) - 1]
				self.snake.positions.append(pos)
				self.score += 10
		
	def create_gear(self, dt):
		gear = Gear()
		gear.setup()
		found = False
		for g in self.allgears:
			if gear.collide_widget(g):
				found = True
		for sg in self.snake.gears:
			if gear.collide_widget(sg):
				found = True
		if gear.collide_widget(self.snake):
			found = True
		if not found:
			self.add_widget(gear)
			self.allgears.append(gear)
		else:
			self.create_gear(1.0/60.0)
		
	
	def on_touch_down(self, touch):
		with self.canvas:
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
		self.game = SnookGame()
		self.game.start()
		self.add_widget (self.game)

	def end_game(self):
		Clock.unschedule(self.game.snake.update)
		Clock.unschedule(self.game.create_gear)
		Clock.unschedule(self.game.check_collisions)
		with self.canvas:
			label = Label(text='Game Over', font_size=30)
			label.pos = (Window.center[0] - label.size[0] / 2, Window.center[1])
			
class SnookApp(App):
	icon = 'assets/icon.png'
	def build(self):
		root = SnookRoot()
		root.size = Window.size
		root.start()
		return root

Factory.register("SnookGame", SnookGame)
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
