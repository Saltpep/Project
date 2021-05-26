import pygame
import sys

def GetLegalMoves():
	LegalMoves = []
	for x in range(3):
		for y in range(3):
			if Matrix[x][y] == 0:
				LegalMoves.append([x,y])
	return LegalMoves

def IsPositionOccuped(Position):
	return Position not in GetLegalMoves()

def GetOccupedPosition(Marker):
	Occuped = []
	for x in range(3):
		for y in range(3):
			if Matrix[x][y] == Marker:
				Occuped.append([x,y])
	return Occuped

def IsMatrixFull():
	return GetLegalMoves().count == 0

def IsGameWon(Marker):
	for Row in Matrix:
		if Row.count(Marker) == 3:
			return True
	for col in range(3):
		if Matrix[0][col] == Marker and Matrix[1][col] == Marker and Matrix[2][col] == Marker:
			return True
	if Matrix[0][0] == Marker and Matrix[1][1] == Marker and Matrix[2][2] == Marker:
		return True
	if Matrix[0][2] == Marker and Matrix[1][1] == Marker and Matrix[2][0] == Marker:
		return True
	if IsMatrixFull():
		return 'Draw'
	return False

def GetOpponentMarker(Marker):
	return 'x' if Marker == 'o' else 'o'

def GetState(Marker):
	OpponentMarker = GetOpponentMarker(Marker)
	if IsGameWon(Marker):
		return 1000
	if IsGameWon(OpponentMarker):
		return -1000
	else:
		return 0

def IsGameDone():
	if IsMatrixFull or GetState() != 0:
		return True
	else:
		return False

def AI():
	if CountEmptyCells() > 0:
		Move = MiniMax('o', 0, -1000, 1000)[1]
		Matrix[Move[0]][Move[1]] = 'o'

def MiniMax(Marker, depth, alpha, beta):
	BestMove = [-1,-1]
	BestScore = -1000 if Marker == 'o' else 1000
	if IsMatrixFull() or GetState('o') != 0:
		BestScore = GetState('o')
		return [BestScore, BestMove]
	LegalMoves = GetLegalMoves()
	for Move in LegalMoves:
		Matrix[Move[0]][Move[1]] = Marker
		if Marker == 'o':
			Score = MiniMax('x', depth + 1, alpha, beta)[0]
			if BestScore < Score:
				BestScore = Score - depth * 10
				BestMove = Move
				alpha = max(alpha, BestScore)
				Matrix[Move[0]][Move[1]] = 0
				if beta <= alpha:
					break
		else:
			Score = MiniMax('o', depth + 1, alpha, beta)[0]
			if BestScore > Score:
				BestScore = Score + depth * 10
				BestMove = Move
				beta = min(beta, BestScore)
				Matrix[Move[0]][Move[1]] = 0
				if beta <= alpha:
					break
		Matrix[Move[0]][Move[1]] = 0
	return [BestScore, BestMove]

def CountEmptyCells():
	EmptyCells = int(0)
	for Row in Matrix:
		EmptyCells += Row.count(0)
	return EmptyCells

pygame.init()
BlockSize = 100
Margin = 15
Width = Heigth = BlockSize * 3 + Margin * 4

WindowSize = (Width, Heigth)
Window = pygame.display.set_mode(WindowSize)
pygame.display.set_caption("Крестики-нолики")

black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
Matrix = [[0] * 3 for i in range(3)]
Query = 0
game_over = False

while True:
	for Event in pygame.event.get():
		if Event.type == pygame.QUIT:
			pygame.quit()
			sys.exit(0)
		elif Event.type == pygame.MOUSEBUTTONDOWN and not game_over:
			x_mouse, y_mouse = pygame.mouse.get_pos()
			Column = x_mouse // (BlockSize + Margin)
			Row = y_mouse // (BlockSize + Margin)
			if Matrix[Row][Column] == 0:
				if Query % 2 == 0:
					Matrix[Row][Column] = 'x'
				else:
					Matrix[Row][Column] = 'o'
				Query += 1
				if not IsGameWon('x' if (Query - 1) % 2 == 0 else 'o'):
					AI()
					Query += 1
		elif Event.type == pygame.KEYDOWN and Event.key == pygame.K_SPACE:
			game_over = False
			Matrix = [[0] * 3 for i in range(3)]
			Query = 0
			Window.fill(black)
	if not game_over:
		for Row in range(3):
				for Column in range(3):
					if Matrix[Row][Column] == 'x':
						color = red
					elif Matrix[Row][Column] == 'o':
						color = green
					else:
						color = white

					x = Column * BlockSize + (Column + 1) * Margin
					y = Row * BlockSize + (Row + 1) * Margin
					pygame.draw.rect(Window, color, (x,y,BlockSize, BlockSize))

					if color == red:
						pygame.draw.line(Window, white, (x + 5,y + 5), (x + BlockSize - 5, y + BlockSize - 5),3)
						pygame.draw.line(Window, white, (x + BlockSize - 5,y + 5), (x + 5, y + BlockSize - 5),3)
					elif color == green:
						pygame.draw.circle(Window,white,(x + BlockSize // 2,y + BlockSize // 2),BlockSize // 2 - 3,3)
		ch = 'x' if (Query - 1) % 2 == 0 else 'o'
		if IsGameWon(ch) == True:
			game_over = ch
		elif IsGameWon(ch) == False:
			if IsGameWon(GetOpponentMarker(ch)):
				game_over = GetOpponentMarker(ch)
		else:
			game_over = 'Draw'
		if game_over:
			Window.fill(black)
			font = pygame.font.SysFont('stxingkai', 80)
			text1 = font.render(game_over, True, white)
			text_rect = text1.get_rect()
			text_x = Window.get_width() / 2 - text_rect.width / 2
			text_y = Window.get_height() / 2 - text_rect.height / 2
			Window.blit(text1, [text_x, text_y])

		pygame.display.update()
