import pygame
import random


pygame.init()
pygame.mixer.init(44100)

# Colors
WHITE 			= (255,255,255)
BLACK 			= (0,0,0)
RED 			= (200,0,0)
LIGHT_RED 		= (255,0,0)
GREEN 			= (34,177,76)
LIGHT_GREEN 	= (0,255,0)
BLUE 			= (0,0,200)
LIGHT_BLUE 		= (0,0,255)
YELLOW 			= (200,200,0)
LIGHT_YELLOW 	= (255,255,0)
MAGENTA 		= (255,0,255)
CYAN			= (0,255,255)

# Display parameters
SCREEN_WIDTH 	= 1024
SCREEN_HEIGHT	= 576

# Game class
class Game():
	def __init__(self):
		self.board = Board()
		self.playerPaddle = Paddle()
		self.aiPaddle = AIPaddle()
		self.gameBall = Ball()
		self.displaySurf = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
		# self.score = 0
		self.mouse = pygame.mouse
		self.state = "GAME_START"
		self.smallFont = pygame.font.SysFont("comicsansms",25)
		self.medFont = pygame.font.SysFont("comicsansms",50)
		self.bigFont = pygame.font.SysFont("comicsansms",80)
	
	def display(self):
		pygame.display.set_caption("PONG!!!")
		clock = pygame.time.Clock()
		self.board.display(self.displaySurf)
		self.playerPaddle.display(self.displaySurf)
		self.aiPaddle.display(self.displaySurf)
		self.gameBall.display(self.displaySurf)
		# self.displayText("SCORE: "+str(self.score),BLACK,"small","topleft")
		

		if self.state == "GAME_START":
			self.displayText("PONG!!!",RED,"big","center",0,0,-50)
			self.displayText("The objective of the game is to return the ball",LIGHT_BLUE,"small","center",0,0,20)
			self.displayText("Failure to return reduces one life. You must remain alive longer than AI!!!",LIGHT_BLUE,"small","center",0,0,80)
			self.displayText("Press s to start, q to exit the game. Control the paddle by moving your mouse.",LIGHT_BLUE,"small","center",0,0,110)
			self.displayText("Good luck!",LIGHT_GREEN,"medium","center",0,0,180)

		if self.state == "GAME_RUNNING":
			self.displayText("LIVES REMAINING: "+str(self.playerPaddle.numLives),RED,"small","topleft")
			self.displayText("LIVES REMAINING: "+str(self.aiPaddle.numLives),BLUE,"small","topright")
		
		if self.state == "GAME_CONFIRM":
			self.displayText("Are you sure you want to quit?",RED,"medium","center",0,0,-50)
			self.displayText("Yes (y)",LIGHT_BLUE,"small","center",0,0,50)
			self.displayText("No (n)",LIGHT_BLUE,"small","center",0,0,100)

		if self.state == "GAME_PAUSED":
			self.displayText("Game Paused",RED,"big","center",0,0,-50)
			self.displayText("Press r to resume or q to quit",LIGHT_BLUE,"small","center",0,0,20)
		
		if self.state == "GAME_OVER":
			if self.aiPaddle.numLives==0 and self.playerPaddle.numLives > 0:
				self.displayText("You Win!!!",LIGHT_GREEN,"big","center",0,0,-50)

			if self.aiPaddle.numLives > 0 and self.playerPaddle.numLives == 0:
				self.displayText("You Lose!!!",RED,"big","center",0,0,-50)

			self.displayText("To replay, press r",LIGHT_BLUE,"small","center",0,0,20)
			self.displayText("To quit to main menu, press m",LIGHT_BLUE,"small","center",0,0,50)
			self.displayText("To directly quit the game, press q",LIGHT_BLUE,"small","center",0,0,80)
		

		pygame.display.update()
		clock.tick(30)
	
	def getTxtSurfRect(self,text,color,size):
		if size=="small":
			txtSurface = self.smallFont.render(text,True,color)
		elif size=="medium":
			txtSurface = self.medFont.render(text,True,color)
		elif size=="big":
			txtSurface = self.bigFont.render(text,True,color)
		txtRect = txtSurface.get_rect()
		return txtSurface,txtRect

	def displayText(self,text,color,size="small",align="center",x=0,y=0,y_offset=0):
		txtSurface,txtRect = self.getTxtSurfRect(text,color,size)
		if align == "center":
			txtRect.center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2+y_offset)
			self.displaySurf.blit(txtSurface,txtRect)
		elif align == "topleft":
			self.displaySurf.blit(txtSurface,[x,y])
		elif align == "topright":
			txtRect.topleft = SCREEN_WIDTH - txtRect.width,0
			self.displaySurf.blit(txtSurface,list(txtRect))


	def update(self):
		x,y = self.mouse.get_pos()
		self.playerPaddle.move(y)
		self.aiPaddle.move(self.gameBall)
		lifeAdd_player,lifeAdd_ai,gameState = self.gameBall.move(self.playerPaddle,self.aiPaddle)
		self.gameState = gameState
		if self.gameState == "GAME_LIFE_LESS":
			self.aiPaddle.reset()
			self.playerPaddle.reset()
			self.gameBall.reset()
			self.aiPaddle.numLives += lifeAdd_ai
			self.playerPaddle.numLives += lifeAdd_player

	def gameLoop(self):
		self.state = "GAME_RUNNING"
		while self.state == "GAME_RUNNING":
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.gameQuit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
						self.gamePause()
					elif event.key == pygame.K_q:
						self.gameConfirmMenu()

			if self.state == "GAME_LIFE_LESS":
				if self.playerPaddle.numLives == 0 or self.aiPaddle.numLives == 0:
					self.gameOver()
				else:	
					pygame.time.wait(1000)
					self.gameState = "GAME_RUNNING"

			self.update()
			self.display()

	def gameOver(self):
		self.state = self.state = "GAME_OVER"
		while self.state == "GAME_OVER":
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.gameQuit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_r:
						self.gameStart()
					elif event.key == pygame.K_q:
						self.gameConfirmMenu()
					elif event.key == pygame.K_m:
						self.gameStart()	
			self.display()

	def gamePause(self):
		self.state = "GAME_PAUSED"
		while self.state == "GAME_PAUSED":
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.gameQuit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_r:
						self.gameLoop()
					elif event.key == pygame.K_q:
						self.gameConfirmMenu()
			self.display()


	def gameQuit(self):
		self.state = "GAME_QUIT"
		pygame.quit()
		quit()

	def gameStart(self):
		self.state = "GAME_START"
		while self.state == "GAME_START":
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.gameQuit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_s:
						self.gameLoop()
					elif event.key == pygame.K_q:
						self.gameConfirmMenu()
					elif event.key == pygame.K_o:
						self.gameOptions()
			self.display()

	def gameConfirmMenu(self):
		self.state = "GAME_CONFIRM"
		while self.state == "GAME_CONFIRM":
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.gameQuit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_y:
						self.gameQuit()
					if event.key == pygame.K_n:
						self.gameLoop()
			self.display()


# Game elements
class Board():
	def __init__(self,boardColor=GREEN):
		self.boardColor = boardColor

	def display(self,surface):
		surface.fill(self.boardColor)
		pygame.draw.line(surface,BLACK,(SCREEN_WIDTH/2,0),(SCREEN_WIDTH/2,SCREEN_HEIGHT))
		pygame.draw.circle(surface,BLACK,(SCREEN_WIDTH/2,SCREEN_HEIGHT/2),150,1)


class Paddle():
	def __init__(self,width=15,height=100,color=RED,numLives=10):
		self.width = width
		self.height = height
		self.center_x = self.width
		self.center_y = SCREEN_HEIGHT/2
		self.color = color
		self.numLives = numLives

	def display(self,surface):
		pygame.draw.rect(surface,self.color,(0,self.center_y - self.height/2,self.width,self.height))
		# pass

	def move(self,y):
		y_old = self.center_y
		self.center_y = y
		if self.center_y <= self.height/2 + 1:
			self.center_y = self.height/2
		elif self.center_y >= SCREEN_HEIGHT - self.height/2 - 1:
			self.center_y = SCREEN_HEIGHT - self.height/2 - 1

	def reset(self):
		self.center_x = self.width
		self.center_y = SCREEN_HEIGHT/2

class AIPaddle():
	def __init__(self,speedFactor=3,width=15,height=100,color=BLUE,numLives=10):
		self.width = width
		self.height = height
		self.center_x = SCREEN_WIDTH - self.width
		self.center_y = SCREEN_HEIGHT/2
		self.color = color
		self.numLives = numLives
		self.speedFactor = speedFactor

	def display(self,surface):
		pygame.draw.rect(surface,self.color,(SCREEN_WIDTH-self.width,self.center_y - self.height/2,self.width,self.height))
		# pass

	def move(self,ball):
		# y_old = self.center_y
		# TODO: AI smartness
		# 1,2,3,4,5 => very easy, easy, normal, hard, very hard
		if self.center_y < ball.center_y:
			self.center_y += self.speedFactor/3.0 * ball.speed_y

		elif self.center_y > ball.center_y:
			self.center_y -= self.speedFactor/3.0 * ball.speed_y
		
		elif self.center_y == ball.center_y:
			self.center_y = self.center_y

		if self.center_y <= self.height/2 + 1:
			self.center_y = self.height/2
		
		elif self.center_y >= SCREEN_HEIGHT - self.height/2 - 1:
			self.center_y = SCREEN_HEIGHT - self.height/2 - 1

	def reset(self):
		self.center_x = SCREEN_WIDTH - self.width
		self.center_y = SCREEN_HEIGHT/2


class Ball():
	def __init__(self,radius=15,color=BLACK,speed=1):
		self.radius = radius
		self.center_x = SCREEN_WIDTH/2
		self.center_y = SCREEN_HEIGHT/2
		self.color = color
		# self.speed_x = 10
		# self.speed_y = 10
		self.speed_x = random.randrange(7,14)
		self.speed_y = random.randrange(7,14)
		self.direction = None

	def reset(self):
		self.center_x = SCREEN_WIDTH/2
		self.center_y = SCREEN_HEIGHT/2
		# self.speed_x = 10
		self.speed_x = random.randrange(7,14)
		# self.speed_y = 10
		self.speed_y = random.randrange(7,14)
		self.direction = None

	def display(self,surface):
		cx,cy = int(round(self.center_x)),int(round(self.center_y))
		pygame.draw.circle(surface,self.color,(cx,cy),self.radius)

	def move(self,playerPaddle,aiPaddle):
		# playerPaddle.isAlive = True
		# Check horizontal wall collisions
		lifeAdd_player,lifeAdd_ai,gameState = 0,0,"GAME_RUNNING"
		if self.center_y <= self.radius or self.center_y >= SCREEN_HEIGHT - self.radius:
			self.speed_y = - self.speed_y

		# Check vertical wall/paddle collisions
		if (self.center_x >= SCREEN_WIDTH - aiPaddle.width) and (aiPaddle.center_y-aiPaddle.height/2<=self.center_y<=aiPaddle.center_y+aiPaddle.height/2):
			self.speed_x = - self.speed_x
			self.speed_x += 0.05*self.speed_x
			self.speed_y += 0.05*self.speed_y
			# print "PING!!!"
			pygame.mixer.music.load("ping.wav")
			pygame.mixer.music.play()
			# scoreAdd,lifeAdd = 1,0

		elif self.center_x >= (SCREEN_WIDTH - self.radius):
			self.speed_x = 0
			self.speed_y = 0
			lifeAdd_player,lifeAdd_ai,gameState = 0,-1,"GAME_LIFE_LESS"

		elif (self.center_x <= self.radius + playerPaddle.width) and (playerPaddle.center_y-playerPaddle.height/2<=self.center_y<=playerPaddle.center_y+playerPaddle.height/2):
			self.speed_x = - self.speed_x
			# print "PONG!!!"
			pygame.mixer.music.load("pong.wav")
			pygame.mixer.music.set_volume(0.5)
			pygame.mixer.music.play()

		elif self.center_x <= self.radius:
			self.speed_x = 0
			self.speed_y = 0
			lifeAdd_player,lifeAdd_ai,gameState = -1,0,"GAME_LIFE_LESS"

		self.center_x += self.speed_x
		self.center_y += self.speed_y
		return lifeAdd_player,lifeAdd_ai,gameState

if __name__ == "__main__":
	myGame = Game()
	myGame.gameStart()
