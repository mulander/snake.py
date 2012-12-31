#!/usr/bin/python

import curses.wrapper
from time import sleep
from random import randint

class Food:
	def __init__(self):
		self.eaten = False
		self.char  = '*'
		self.x	   = randint(1,80)
		self.y	   = randint(2,25)
		self.score = randint(1,3)
		self.extend= randint(1,3)

class Snake:
	def __init__(self):
		self.face = 'E' # N W S E
		self.score= 0
		self.y    = 10
		self.x    = 10
		self.char = 'o'
		self.body = []
		self.body.append( (self.y,self.x) )
		self.extend = 0
	def head(self):
		self.body.append( (self.y,self.x) )
		self.extend -= 1
		return self.body[0]
	def tail(self):
		self.body.append( (self.y,self.x) )
		return self.body.pop(0)

def run(stdscr):
	snake = Snake()
	try:
		stdscr.hline(1,1,0,80)
		stdscr.hline(26,1,0,80)
		stdscr.vline(2,0,0,24)
		stdscr.vline(2,81,0,24)
	except curses.error:
		stdscr.erase()
		stdscr.addstr(0,0,"Sorry your terminal is to small\n" +
				  "Please resize it and try again\n"  +
				  "Press any key to exit")
		stdscr.refresh()
		stdscr.getch()
		return
	stdscr.move(0,0)
	stdscr.clrtoeol()
	stdscr.addstr(0,0,'Score: ' + str(snake.score))
	stdscr.nodelay(1)
	food  = Food()
	stdscr.addstr(food.y,food.x,food.char)
	stdscr.refresh()
	snake.extend = 5
	while True:
		c = stdscr.getch()
		if c == curses.KEY_UP:
			snake.face = 'N'
		elif c == curses.KEY_DOWN:
			snake.face = 'S'
		elif c == curses.KEY_LEFT:
			snake.face = 'W'
		elif c == curses.KEY_RIGHT:
			snake.face = 'E'

		if snake.face == 'N':
			snake.y -= 1
		elif snake.face == 'S':
			snake.y += 1
		elif snake.face == 'W':
			snake.x -= 1
		elif snake.face == 'E':
			snake.x += 1

		# check if the snake hit itself
		if snake.body[-1] in snake.body[:-1]:
			stdscr.addstr(0,0,'You run into yourself!')
			stdscr.refresh()
			break
		# check if we teleport
		if snake.x < 1 and snake.face == 'W':
			snake.x = 80
		elif snake.x > 80 and snake.face == 'E':
			snake.x = 1
		elif snake.y < 2 and snake.face == 'N':
			snake.y = 25
		elif snake.y > 25 and snake.face == 'S':
			snake.y = 2

		# remove tail
		if snake.extend == 0:
			tail = snake.tail()
			stdscr.addstr(tail[0],tail[1],' ')
		else:
			snake.head()
			
		# check if we hit any food
		if snake.body[-1] == (food.y,food.x):
			snake.score  += food.score
			snake.extend += food.extend
			stdscr.move(0,0)
			stdscr.clrtoeol()
			stdscr.addstr(0,0,'Score: ' + str(snake.score))
			food.eaten = True
			food = Food()
			while (food.y,food.x) in snake.body:
				food = Food()
			stdscr.addstr(food.y,food.x,food.char)
		# move snake
		stdscr.addstr(snake.y,snake.x,snake.char)
		stdscr.move(snake.y,snake.x)

		stdscr.refresh()
		curses.napms(50)
	sleep(5)

curses.wrapper(run)
