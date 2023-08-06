from math import acos, pi
from turtle import *


class Rectangle():
	def __init__(self, width, height=None, **kwargs):
		penup()
		if not height: height=width
		if "position" in kwargs: goto(kwargs["position"])
		if "angle" in kwargs: setheading(kwargs["angle"])
		if "color" in kwargs: pencolor(kwargs["color"])
		if "fill" in kwargs: fillcolor(kwargs["fill"])
		if "size" in kwargs: pensize(kwargs["size"])
		pendown()

		if "fill" in kwargs: begin_fill()
		for _ in range(2):
			forward(width)
			left(90)
			forward(height)
			left(90)
		if "fill" in kwargs: end_fill()


class Triangle():
	def __init__(self, side1, side2=None, side3=None, **kwargs):
		def get_angle(a, b, c):
			return round(180/pi*acos((b**2 + c**2 - a**2)/(2*b*c)))

		if not side3:
			side3=side2
		if not side2 and not side3:
			side3=side1
			side2=side1

		angle1 = 180 - get_angle(side3, side1, side2)
		angle2 = 180 - get_angle(side1, side2, side3)
		angle3 = - angle1 - angle2

		penup()
		if "position" in kwargs: goto(kwargs["position"])
		if "angle" in kwargs: setheading(kwargs["angle"])
		if "color" in kwargs: pencolor(kwargs["color"])
		if "fill" in kwargs: fillcolor(kwargs["fill"])
		if "size" in kwargs: pensize(kwargs["size"])
		pendown()

		if "fill" in kwargs: begin_fill()
		forward(side1)
		left(angle1)
		forward(side2)
		left(angle2)
		forward(side3)
		left(angle3)
		if "fill" in kwargs: end_fill()


class Circle():
	def __init__(self, radius, **kwargs):
		penup()
		if "position" in kwargs: goto(kwargs["position"])
		if "angle" in kwargs: setheading(kwargs["angle"])
		if "color" in kwargs: pencolor(kwargs["color"])
		if "fill" in kwargs: fillcolor(kwargs["fill"])
		if "size" in kwargs: pensize(kwargs["size"])
		pendown()

		if "fill" in kwargs: begin_fill()
		circle(radius)
		if "fill" in kwargs: end_fill()