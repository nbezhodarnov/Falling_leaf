from graphics import *
import time
import math

def sign(x):
	if x > 0:
		return 1
	elif x < 0:
		return -1
	else:
		return 0

def clear(win):
	for item in win.items[:]:
		item.undraw()
	win.update()

# Алгоритм Брезенхема (целочисленный)
def lineDraw(win, point1, point2):
	dx = int(point2.getX() - point1.getX())
	dy = int(point2.getY() - point1.getY())
	sign_x = sign(dx)
	sign_y = sign(dy)
	dx = abs(dx)
	dy = abs(dy)

	x = point1.getX()
	y = point1.getY()
	x_end = point2.getX()
	y_end = point2.getY()

	e = dx - dy
	while (x != x_end or y != y_end):
		Point(x, y).draw(win)
		e2 = e * 2
		if (e2 > -dy):
			e -= dy
			x += sign_x
		if (e2 < dx):
			e += dx
			y += sign_y
	Point(x, y).draw(win)

def Leaf(point = Point(0, 0), radius = 20, angle = 0):
	points = [] # 0-3 - 4-хугольник, 4-5 - линия
	for i in range(6):
		points.append(Point(0, 0))

	points[0].x = -radius
	points[1].y = int(-radius / 2)
	points[2].x = int(radius / 2)
	points[3].y = int(radius / 2)
	points[5].x = radius
	for i in range(6):
		temp_x = points[i].x
		temp_y = points[i].y
		points[i].x = round(temp_x * math.cos(angle) - temp_y * math.sin(angle)) + point.getX()
		points[i].y = -round(temp_x * math.sin(angle) + temp_y * math.cos(angle)) + point.getY()
	return points

def leafDraw(win, points):
	for i in range(3):
		Line(points[i], points[i + 1]).draw(win)
	Line(points[3], points[0]).draw(win)
	Line(points[4], points[5]).draw(win)

def moveObject(points, point = Point(0, 0)):
	for i in range(len(points)):
		points[i].x += point.x
		points[i].y += point.y

def rotatePoints(points, angle):
	for i in range(len(points)):
		temp_x = points[i].x
		temp_y = points[i].y
		points[i].x = round(temp_x * math.cos(-angle) - temp_y * math.sin(-angle))
		points[i].y = round(temp_x * math.sin(-angle) + temp_y * math.cos(-angle))

def resizePoints(points, coefficient):
	for i in range(len(points)):
		points[i].x = round(points[i].x * coefficient)
		points[i].y = round(points[i].y * coefficient)

def main():
	win = GraphWin("Falling leaf (lab1)", 700, 600)
	time.sleep(1)
	point = Point(int(win.width / 2), 0)
	point.draw(win)
	#lineDraw(win, Point(500, 600), Point(300, 400))
	leaf = Leaf(Point(int(win.width * 4 / 5), int(1.7 * win.height / 5)), 20, math.pi / 4)
	leafDraw(win, leaf)
	
	angle = 0
	coefficient_move = 1.01
	coefficient_resize = 1.01
	angle_sign = -1
	while (leaf[0].y <= win.height or leaf[1].y <= win.height or leaf[3].y <= win.height or leaf[5].y <= win.height):
		moveObject(leaf, Point(-point.x, -point.y))
		rotatePoints(leaf, angle_sign * math.pi / 20)
		center_x = leaf[4].x
		center_y = leaf[4].y
		moveObject(leaf, Point(-center_x, -center_y))
		resizePoints(leaf, coefficient_resize)
		moveObject(leaf, Point(round(center_x * coefficient_move + point.x), round(center_y * coefficient_move + point.y)))
		clear(win)
		leafDraw(win, leaf)
		angle -= angle_sign * math.pi / 20
		time.sleep(10 * abs(angle - math.pi / 4) / 60 + 0.05)
		if (abs(angle - math.pi / 4) >= math.pi / 4):
			angle_sign *= -1
		leaf = Leaf(Point(leaf[4].x, leaf[4].y), round(coefficient_resize * ((leaf[0].x - leaf[4].x) ** 2  + (leaf[0].y - leaf[4].y) ** 2) ** 0.5), -angle + math.pi / 4)
	#for i in range(6):
		#print(leaf[i].x, leaf[i].y)
	#print()
	#print(win.width, win.height)
	print("Done!")
		
	
	win.getMouse()
	clear(win)
	win.close()

if __name__ == '__main__':
	main()
