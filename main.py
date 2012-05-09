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

class Screw(Widget):
	def setup(self):
		self.size = (30,30)
		self.pos = (randint(1, Window.size[0] - 50), randint(1, Window.size[1] - 50))
		with self.canvas:
			self.image = Rectangle(size=(30,30), pos=self.pos, source='assets/screw.png')
			
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
		self.positions = []
		self.gears = []
		self.dir = "none"
		self.pos = (Window.center[0], Window.center[1])
		self.velocity = 30
		self.size= (30, 30)
		self.positions.append(self.pos)
		with self.canvas:
			self.head = Rectangle(size=(30,30), pos=self.pos, source='assets/head.png')
	
	def reset(self):
		self.positions = []
		self.gears = []
		self.dir = "none"
		self.positions.append(self.pos)
		self.head.pos = (Window.center[0], Window.center[1])
	
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
		end = False
		for g in self.gears:
			if g.collide_widget(self):
				end = True
		if self.pos[0] < 0 or self.pos[0] + 30 > Window.size[0] or self.pos[1] < 0 or self.pos[1] + 30 > Window.size[1]:
			end = True
		if end:
			self.parent.parent.end_game()
		
class SnookGame(Widget):
	score = NumericProperty(0)
	allgears = []
	dir = "none"
	snake = Snake()
	screws = []
	def start(self):
		self.dir = "none"
		self.score = 0
		self.add_widget(self.snake)
		gear = Gear()
		gear.setup()
		self.allgears.append(gear)
		self.add_widget(gear)
		self.snake.setup()
		Clock.schedule_interval(self.snake.update, .1)
		Clock.schedule_interval(self.create_gear, 2)
		Clock.schedule_interval(self.check_collisions, 1.0 / 60.0)
		Clock.schedule_interval(self.create_screw, 7)
	
	def restart_game(self):
		for g in self.allgears:
			self.remove_widget(g)
		for g in self.snake.gears:
			self.snake.remove_widget(g)
		for s in self.screws:
			self.remove_widget(s)
		self.allgears = []
		self.screws = []
		self.snake.reset()
		gear = Gear()
		gear.setup()
		self.allgears.append(gear)
		self.add_widget(gear)
		self.score = 0
		Clock.schedule_interval(self.snake.update, .1)
		Clock.schedule_interval(self.create_gear, 2)
		Clock.schedule_interval(self.check_collisions, 1.0 / 60.0)
		Clock.schedule_interval(self.create_screw, 7)
	
	def check_collisions(self, dt):
		for gear in self.allgears:
			if gear.collide_widget(self.snake):
				self.remove_widget(gear)
				self.allgears.remove(gear)
				if len(self.snake.gears) > 1:
					if gear.colornum == self.snake.gears[len(self.snake.gears) - 1].colornum and gear.colornum == self.snake.gears[len(self.snake.gears) - 2].colornum:
						print "3 of a kind"
						self.snake.remove_widget(self.snake.gears[len(self.snake.gears) - 1])
						self.snake.remove_widget(self.snake.gears[len(self.snake.gears) - 2])
						self.snake.gears.pop(len(self.snake.gears) - 1)
						self.snake.gears.pop(len(self.snake.gears) - 1)
						self.snake.positions.pop(len(self.snake.positions) - 1)
						self.snake.positions.pop(len(self.snake.positions) - 1)
						self.score += 50
					else:
						self.snake.gears.append(gear)
						self.snake.add_widget(gear)
						pos = self.snake.positions[len(self.snake.positions) - 1]
						self.snake.positions.append(pos)
						self.score += 10
				else:
					self.snake.gears.append(gear)
					self.snake.add_widget(gear)
					pos = self.snake.positions[len(self.snake.positions) - 1]
					self.snake.positions.append(pos)
					self.score += 10
		for screw in self.screws:
			if screw.collide_widget(self.snake):
				self.parent.end_game()

	def create_screw(self, dt):
		screw = Screw()
		screw.setup()
		found = False
		for g in self.allgears:
			if screw.collide_widget(g):
				found = True
		for sg in self.snake.gears:
			if screw.collide_widget(sg):
				found = True
		for s in self.screws:
			if screw.collide_widget(s):
				found = True
		if screw.collide_widget(self.snake):
			found = True
		if not found:
			self.add_widget(screw)
			self.screws.append(screw)
		else:
			self.create_screw(1.0/60.0)
	
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
		for s in self.screws:
			if gear.collide_widget(s):
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
	
class SnookRestartMenu(Widget):
	score = NumericProperty(0)
	def setup(self, score):
		self.score = score
		
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
		
	def restart_game(self):
		self.game.restart_game()
		self.remove_widget(self.lose)
		self.add_widget(self.game)
		
	def end_game(self):
		Clock.unschedule(self.game.snake.update)
		Clock.unschedule(self.game.create_gear)
		Clock.unschedule(self.game.check_collisions)
		Clock.unschedule(self.game.create_screw)
		self.state = SnookRoot.STATE_LOSE
		self.remove_widget(self.game)
		self.lose = SnookRestartMenu()
		self.lose.size = Window.size
		self.lose.setup(self.game.score)
		self.add_widget(self.lose)
			
class SnookApp(App):
	icon = 'assets/icon.png'
	def build(self):
		root = SnookRoot()
		root.size = Window.size
		root.start()
		return root

Factory.register("SnookGame", SnookGame)
		
if __name__ == '__main__':
	SnookApp().run()
