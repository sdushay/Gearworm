from kivy.app import App
from random import random
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
				print "right"	
			elif angle < -45 and angle > -135:
				print "down"
			elif angle < -135 or angle > 135:
				print "left"
			else:
				print "up"
			

class ChipApp(App):
	def build(self):
		swipeW = SwipeWidget()
		return swipeW
		
if __name__ == '__main__':
	ChipApp().run()
