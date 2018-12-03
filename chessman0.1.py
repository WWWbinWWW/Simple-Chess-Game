import numpy as np
import copy

#棋盘尺寸
WIDTH = 7
HEIGHT = 5
#双方棋子初始数量
CHESS_NUMBER = 5
#棋子初始化位置

#用于标识方向
Direction = {'w':'Top', 'a':'Left', 's':'Buttom', 'd':'Right'}

class StateNode(object):
	def __init__(self,map):
		self.map = map
		self.child = []

class StateTree(object):
	def __init__(self):
		self.root = None

	def add(self, parent, map):
		statenode = StateNode(map)
		if self.root is None:
			self.root = statenode
		else:
			parent.child.append(statenode)

	def traverse(self):
		if self.root is None:
			return
		else:
			q = [self.root]
			res = [self.root.map]
			while q != []:
				pop_node = q.pop(0)
				if pop_node.child != []:
					for item in pop_node.child:
						q.append(item)
						res.append(item.map)
		return res


class chessmen(object):
	'''棋子类'''
	def __init__(self, befx, befy, curx, cury, onwer, name, life):
		'''记录当前位置和上一步位置，onwer取值A、B'''
		self.name = name
		self.life = life
		self.onwer = onwer
		self.befx = befx
		self.befy = befy
		self.curx = curx
		self.cury = cury

	def get_eat(self,chess_map):
		#将被吃棋子从棋盘中移除remove
		if self.onwer == 'A':
			temp = 'B'
		else:
			temp = 'A'

		#将棋子按阵营分配标记
		for item in chess_map.countA:
			tempx, tempy = item.curx, item.cury
			chess_map.state[tempx, tempy] = 'A'
		for item in chess_map.countB:
			tempx, tempy = item.curx, item.cury
			chess_map.state[tempx, tempy] = 'B'

		#判断是否能吃对手棋子
		#Top Direction
		if self.curx - 1 >= 0:
			if chess_map.state[self.curx-1][self.cury] == self.onwer:
				if self.curx - 2 >= 0:
					if chess_map.state[self.curx-2][self.cury] == temp:
						print("You can eat the chess {} form {}".format((self.curx-2,self.cury), temp))
						#根据被吃棋子的坐标找到该棋子，life置为0，并从棋盘中移除
						tempx, tempy = self.curx-2, self.cury
						#遍历对手场上所有棋子
						for item in chess_map.get_owner(temp):
							#将对应位置棋子置0
							if item.curx == tempx and item.cury == tempy:
								item.life = 0
								chess_map.get_owner(temp).remove(item)
						#chess_map.get_owner(temp).remove((self.curx-2,self.cury))
						chess_map.state[self.curx-2][self.cury] = '0.0'
						return chess_map
				if self.curx + 1 < chess_map.height:
					if chess_map.state[self.curx+1][self.cury] == temp:
						print("You can eat the chess {} form {}".format((self.curx+1,self.cury), temp))
						#根据被吃棋子的坐标找到该棋子，life置为0，并从棋盘中移除
						tempx, tempy = self.curx+1, self.cury
						for item in chess_map.get_owner(temp):
							if item.curx == tempx and item.cury == tempy:
								item.life = 0
								chess_map.get_owner(temp).remove(item)
						#chess_map.get_owner(temp).remove((self.curx+1,self.cury))
						chess_map.state[self.curx+1][self.cury] = '0.0'
						return chess_map

		#Buttom Direction
		if self.curx + 1 < chess_map.height:
			if chess_map.state[self.curx+1][self.cury] == self.onwer:
				if self.curx + 2 < chess_map.height:
					if chess_map.state[self.curx+2][self.cury] == temp:
						print("You can eat the chess {} form {}".format((self.curx+2,self.cury), temp))
						#根据被吃棋子的坐标找到该棋子，life置为0，并从棋盘中移除
						tempx, tempy = self.curx+2, self.cury
						for item in chess_map.get_owner(temp):
							if item.curx == tempx and item.cury == tempy:
								item.life = 0
								chess_map.get_owner(temp).remove(item)
						#chess_map.get_owner(temp).remove((self.curx+2,self.cury))
						chess_map.state[self.curx+2][self.cury] = '0.0'
						return chess_map
				if self.curx - 1 >= 0:
					if chess_map.state[self.curx-1][self.cury] == temp:
						print("You can eat the chess {} form {}".format((self.curx-1,self.cury), temp))
						#根据被吃棋子的坐标找到该棋子，life置为0，并从棋盘中移除
						tempx, tempy = self.curx-1, self.cury
						for item in chess_map.get_owner(temp):
							if item.curx == tempx and item.cury == tempy:
								item.life = 0
								chess_map.get_owner(temp).remove(item)
						#chess_map.get_owner(temp).remove((self.curx-1,self.cury))
						chess_map.state[self.curx-1][self.cury] = '0.0'
						return chess_map

		#Left Direction
		if self.cury - 1 >= 0:
			if chess_map.state[self.curx][self.cury-1] == self.onwer:
				if self.cury - 2 >= 0:
					if chess_map.state[self.curx][self.cury-2] == temp:
						print("You can eat the chess {} form {}".format((self.curx,self.cury-2), temp))
						#根据被吃棋子的坐标找到该棋子，life置为0，并从棋盘中移除
						tempx, tempy = self.curx, self.cury-2
						for item in chess_map.get_owner(temp):
							if item.curx == tempx and item.cury == tempy:
								item.life = 0
								chess_map.get_owner(temp).remove(item)
						#chess_map.get_owner(temp).remove((self.curx,self.cury-2))
						chess_map.state[self.curx][self.cury-2] = '0.0'
						return chess_map
				if self.cury + 1 < chess_map.width:
					if chess_map.state[self.curx][self.cury+1] == temp:
						print("You can eat the chess {} form {}".format((self.curx,self.cury+1), temp))
						#根据被吃棋子的坐标找到该棋子，life置为0，并从棋盘中移除
						tempx, tempy = self.curx, self.cury+1
						for item in chess_map.get_owner(temp):
							if item.curx == tempx and item.cury == tempy:
								item.life = 0
								chess_map.get_owner(temp).remove(item)
						#chess_map.get_owner(temp).remove((self.curx,self.cury+1))
						chess_map.state[self.curx][self.cury+1] = '0.0'
						return chess_map

		#Right Direction
		if self.cury + 1 < chess_map.width:
			if chess_map.state[self.curx][self.cury+1] == self.onwer:
				if self.cury + 2 < chess_map.width:
					if chess_map.state[self.curx][self.cury+2] == temp:
						print("You can eat the chess {} form {}".format((self.curx,self.cury+2), temp))
						#根据被吃棋子的坐标找到该棋子，life置为0，并从棋盘中移除
						tempx, tempy = self.curx, self.cury+2
						for item in chess_map.get_owner(temp):
							if item.curx == tempx and item.cury == tempy:
								item.life = 0
								chess_map.get_owner(temp).remove(item)
						#chess_map.get_owner(temp).remove((self.curx,self.cury+2))
						chess_map.state[self.curx][self.cury+2] = '0.0'
						return chess_map
				if self.cury - 1 >= 0:
					if chess_map.state[self.curx][self.cury-1] == temp:
						print("You can eat the chess {} form {}".format((self.curx,self.cury-1), temp))
						#根据被吃棋子的坐标找到该棋子，life置为0，并从棋盘中移除
						tempx, tempy = self.curx, self.cury-1
						for item in chess_map.get_owner(temp):
							if item.curx == tempx and item.cury == tempy:
								item.life = 0
								chess_map.get_owner(temp).remove(item)
						#chess_map.get_owner(temp).remove((self.curx,self.cury-1))
						chess_map.state[self.curx][self.cury-1] = '0.0'
						return chess_map
		#判断是否自杀
		#上方向
		if self.curx - 1 >= 0:
			if self.curx - 2 >= 0:
				if chess_map.state[self.curx-1][self.cury] == temp and chess_map.state[self.curx-2][self.cury] == temp:
					print("Your chess {}{} is eaten!".format(self.onwer,(self.curx,self.cury)))
					for item in chess_map.get_owner(self.onwer):
							if item.curx == self.curx and item.cury == self.cury:
								item.life = 0
								chess_map.state[self.curx][self.cury] = '0.0'
								chess_map.get_owner(self.onwer).remove(item)
						#chess_map.get_owner(temp).remove((self.curx+2,self.cury))
					return chess_map
		#下方向
		if self.curx + 1 < chess_map.height:
			if self.curx + 2 < chess_map.height:
				if chess_map.state[self.curx+1][self.cury] == temp and chess_map.state[self.curx+2][self.cury] == temp:
					print("Your chess {}{} is eaten!".format(self.onwer,(self.curx,self.cury)))
					for item in chess_map.get_owner(self.onwer):
							if item.curx == self.curx and item.cury == self.cury:
								item.life = 0
								chess_map.state[self.curx][self.cury] = '0.0'
								chess_map.get_owner(self.onwer).remove(item)
						#chess_map.get_owner(temp).remove((self.curx+2,self.cury))			
					return chess_map
		#左方向
		if self.cury - 1 >= 0:
			if self.cury - 2 >= 0:
				if chess_map.state[self.curx][self.cury-1] == temp and chess_map.state[self.curx][self.cury-2] == temp:
					print("Your chess {}{} is eaten!".format(self.onwer,(self.curx,self.cury)))
					for item in chess_map.get_owner(self.onwer):
							if item.curx == self.curx and item.cury == self.cury:
								item.life = 0
								chess_map.state[self.curx][self.cury] = '0.0'
								chess_map.get_owner(self.onwer).remove(item)
						#chess_map.get_owner(temp).remove((self.curx+2,self.cury))
					return chess_map

		if self.cury + 1 < chess_map.width:
			if self.cury + 2 < chess_map.width:
				if chess_map.state[self.curx][self.cury+1] == temp and chess_map.state[self.curx][self.cury+2] == temp:
					print("Your chess {}{} is eaten!".format(self.onwer,(self.curx,self.cury)))
					for item in chess_map.get_owner(self.onwer):
							if item.curx == self.curx and item.cury == self.cury:
								item.life = 0
								chess_map.state[self.curx][self.cury] = '0.0'
								chess_map.get_owner(self.onwer).remove(item)
						#chess_map.get_owner(temp).remove((self.curx+2,self.cury))
					return chess_map

		return chess_map


	def move_top(self,chess_map):
		if chess_map.state[self.curx-1][self.cury] == '0.0':
			#此处无棋子则可更新棋盘
			self.befx = self.curx
			self.befy = self.cury
			self.curx = self.curx - 1
			self.cury = self.cury
			#更新棋盘
			chess_map.state[self.befx][self.befy] = '0.0'
			chess_map.state[self.curx][self.cury] = self.name
			#删除之前棋子，并添加新棋子
			#chess_map.get_owner(self.onwer).remove((self.befx, self.befy))
			#chess_map.get_owner(self.onwer).insert(0,(self.curx, self.cury))

			chess_map = self.get_eat(chess_map)
			chess_map.game_begin()
			print("New chess map:\n{}".format(chess_map.state))
			return chess_map, 1
		else:
			print("You can't walk this way, choose another way, please.")
			return chess_map, 0

	def move_left(self,chess_map):
		if chess_map.state[self.curx][self.cury-1] == '0.0':
			#此处无棋子则可更新棋盘
			self.befx = self.curx
			self.befy = self.cury
			self.curx = self.curx
			self.cury = self.cury - 1
			#更新棋盘
			chess_map.state[self.befx][self.befy] = '0.0'
			chess_map.state[self.curx][self.cury] = self.name
			#删除之前棋子，并添加新棋子
			#chess_map.get_owner(self.onwer).remove((self.befx, self.befy))
			#chess_map.get_owner(self.onwer).insert(0,(self.curx, self.cury))

			chess_map = self.get_eat(chess_map)
			chess_map.game_begin()
			print("New chess map:\n{}".format(chess_map.state))
			return chess_map, 1
		else:
			print("You can't walk this way, choose another way, please.")
			return chess_map, 0

	def move_buttom(self,chess_map):
		if chess_map.state[self.curx+1][self.cury] == '0.0':
			#此处无棋子则可更新棋盘
			self.befx = self.curx
			self.befy = self.cury
			self.curx = self.curx + 1
			self.cury = self.cury
			#更新棋盘
			chess_map.state[self.befx][self.befy] = '0.0'
			chess_map.state[self.curx][self.cury] = self.name
			#删除之前棋子，并添加新棋子
			#chess_map.get_owner(self.onwer).remove((self.befx, self.befy))
			#chess_map.get_owner(self.onwer).insert(0,(self.curx, self.cury))

			chess_map = self.get_eat(chess_map)
			chess_map.game_begin()
			print("New chess map:\n{}".format(chess_map.state))
			return chess_map, 1
		else:
			print("You can't walk this way, choose another way, please.")
			return chess_map, 0

	def move_right(self,chess_map):
		if chess_map.state[self.curx][self.cury+1] == '0.0':
			#此处无棋子则可更新棋盘
			self.befx = self.curx
			self.befy = self.cury
			self.curx = self.curx
			self.cury = self.cury + 1
			#更新棋盘
			chess_map.state[self.befx][self.befy] = '0.0'
			chess_map.state[self.curx][self.cury] = self.name
			#删除之前棋子，并添加新棋子
			#chess_map.get_owner(self.onwer).remove((self.befx, self.befy))
			#chess_map.get_owner(self.onwer).insert(0,(self.curx, self.cury))

			chess_map = self.get_eat(chess_map)
			chess_map.game_begin()
			print("New chess map:\n{}".format(chess_map.state))
			return chess_map, 1
		else:
			print("You can't walk this way, choose another way, please.")
			return chess_map, 0

	def chess_move(self,chess_map,type):
		#判断方向以及是否越界，chess_map为ChessPlate实例
		#chess_map, result = A.chess_move(chess_map,type)
		#result为移动结果，能否成功移动
		if type == 'Top' and self.curx-1 >= 0:
			chess_map, result = self.move_top(chess_map)
			return chess_map, result
		elif type == 'Left' and self.cury-1 >= 0:
			chess_map, result = self.move_left(chess_map)
			return chess_map, result
		elif type == 'Buttom' and self.curx+1 < HEIGHT:
			chess_map, result = self.move_buttom(chess_map)
			return chess_map, result
		elif type == 'Right' and self.cury+1 < WIDTH:
			chess_map, result = self.move_right(chess_map)
			return chess_map, result
		else:
			print("You can't take this way.")
			return chess_map, 0


class ChessPlate(object):
	'''棋盘类'''
	def __init__(self, width, height, countA, countB, state=None):
		'''state为棋盘状态矩阵，countA、countB为双方棋子坐标列表'''
		self.width = width
		self.height = height
		if state is None:
			self.state = np.zeros([self.height, self.width]).astype(str)
		else:
			self.state = state
		#countA=[(0,0),(1,0),(2,0),(3,0),(4,0)]
		self.countA = countA
		#countB=[(0,6),(1,6),(2,6),(3,6),(4,6)]
		self.countB = countB

	def game_begin(self):
		for item in self.countA:
			tempx, tempy = item.curx, item.cury
			self.state[tempx, tempy] = item.name
		for item in self.countB:
			tempx, tempy = item.curx, item.cury
			self.state[tempx, tempy] = item.name

	def is_end(self):
		'''通过场上棋子数量判断游戏是否结束，若只剩下一个棋子则必输'''
		if len(self.countA) == 1:
			print("The winner is Player B!!!")
			return True
		elif len(self.countB) == 1:
			print("The winner is Player A!!!")
			return True
		else:
			print("The game is continue.")
			return False

	def get_owner(self, onwer):
		'''寻找当前棋子拥有者'''
		if onwer == 'A':
			return self.countA
		else:
			return self.countB

	def showmap(self):
		return self.state

	def is_alive(self, Player, num):
		#棋子A
		if Player == 1:
			for item in self.countA:
				if item.name == 'A'+num:
					if item.life == 1:
						print("You choosed the chess {}".format(item.name))
						return True
					else:
						print("Choose another chess, please.")
						return False
		if Player == 0:
			for item in self.countB:
				if item.name == 'B'+num:
					if item.life == 1:
						print("You choosed the chess {}".format(item.name))
						return True
					else:
						print("Choose another chess, please.")
						return False
		print("Please input right number!")
		return False

def game_init():
	Player = 1
	Num = 1
	Dir = 1
	chessA1 = chessmen(0,0,0,0,'A','A1',1)
	chessA2 = chessmen(1,0,1,0,'A','A2',1)
	chessA3 = chessmen(2,0,2,0,'A','A3',1)
	chessA4 = chessmen(3,0,3,0,'A','A4',1)
	chessA5 = chessmen(4,0,4,0,'A','A5',1)
	chessB1 = chessmen(0,6,0,6,'B','B1',1)
	chessB2 = chessmen(1,6,1,6,'B','B2',1)
	chessB3 = chessmen(2,6,2,6,'B','B3',1)
	chessB4 = chessmen(3,6,3,6,'B','B4',1)
	chessB5 = chessmen(4,6,4,6,'B','B5',1)
	PlayerA = [chessA1, chessA2, chessA3, chessA4, chessA5]
	PlayerB = [chessB1, chessB2, chessB3, chessB4, chessB5]

	Chess_map = ChessPlate(WIDTH, HEIGHT, PlayerA, PlayerB)
	Chess_map.game_begin()
	print(Chess_map.showmap())
	ChessA_map = {'1':chessA1,
				'2':chessA2,
				'3':chessA3,
				'4':chessA4,
					'5':chessA5}
	ChessB_map = {'1':chessB1,
				'2':chessB2,
				'3':chessB3,
				'4':chessB4,
				'5':chessB5}

	while Chess_map.is_end() == False:

		if Player == 1:
			print("PLayerA's time!")
			Num = input("Please input number of chessA:")
			while Chess_map.is_alive(Player, Num) == False:
				Num = input("Please input number of chessA:")
			Dir = input("Please input the direction w,a,s,d:")
			while Dir not in ['w','a','s','d']:
				Dir = input("Please choose one form w,a,s,d:")
			Chess_map, flat = ChessA_map[Num].chess_move(Chess_map, Direction[Dir])
			while flat != 1:
				Dir = input("Please choose the right direction again:")
				Chess_map, flat = ChessA_map[Num].chess_move(Chess_map, Direction[Dir])
			Player = 0

		if Player == 0:
			print("PLayerB's time!")
			Num = input("Please input number of chessB:")
			while Chess_map.is_alive(Player, Num) == False:
				Num = input("Please input number of chessB:")
			Dir = input("Please input the direction w,a,s,d:")
			while Dir not in ['w','a','s','d']:
				Dir = input("Please choose one form w,a,s,d:")
			Chess_map, flat = ChessB_map[Num].chess_move(Chess_map, Direction[Dir])
			while flat != 1:
				Dir = input("Please choose the right direction again:")
				Chess_map, flat = ChessB_map[Num].chess_move(Chess_map, Direction[Dir])
			Player = 1

def main(argv=None):
	game_init()

if __name__ == '__main__':
	main()

#MapStates = StateTree()
#MapStates.add(MapStates.root,Chess_map.state)
"""
Chess_map, _ = chessA1.chess_move(Chess_map, 'Right')
Chess_map, _ = chessB1.chess_move(Chess_map, 'Left')
Chess_map, _ = chessB1.chess_move(Chess_map, 'Left')
Chess_map, _ = chessB1.chess_move(Chess_map, 'Left')
Chess_map, _ = chessB1.chess_move(Chess_map, 'Left')
Chess_map.game_begin()
Chess_map, _ = chessA2.chess_move(Chess_map, 'Top')
print(Chess_map.is_end())
"""
#Chess_map, _ = chessA2.chess_move(Chess_map, 'Top')
#print("----------------")
#print(Chess_map.showmap())

#用于遍历所有棋子


#for item in ChessA_map:
#	The_chess = ChessA_map[item]
#	if The_chess.life == 0:
#		continue
#	else:		
#		for direction in ('Top', 'Left', 'Right', 'Buttom'):
#			temp_map = ChessPlate(WIDTH, HEIGHT, Chess_map.countA, Chess_map.countB, Chess_map.state)
#			temp_map, result = The_chess.chess_move(temp_map, direction)
#			if result == 1:
#				MapStates.add(MapStates.root, temp_map.state)

#print("----------------")
#print(Chess_map.showmap())
