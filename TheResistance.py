#! /usr/bin/env python
# -*- coding: utf-8 -*-
import random
import hashlib
import time 
from bottle import *
import xml.etree.cElementTree as ET
import thread
import threading


num_of_player = 6
num_of_good = 4 
num_of_bad = 2
player_list = []
player_wechatIDs = []
playerFlag = 1

leaderid = 0
bad_guy_list =[]

class Player:
	"""docstring for Player"""

	is_leader = False
	is_good = True
	is_executant = False

	def __init__(self, **kwargs):
		self.name = kwargs['name']
		self.id = kwargs['id']
		self.wechatID = kwargs['wechatID']

	def show_self_info(self):
		if self.is_good:
			x = u"好人"
		else:
			x = u"坏人"

		if self.is_leader:
			a = u"你的名称是%s，ID是%s，身份是%s 。并且你是本局的队长"% (self.name, self.id, x)
			return a
		else:
			a = u"你的名称是%s，ID是%s，身份是%s 。"% (self.name, self.id, x)
			return a

	def choose_executant(self, num_of_executants, msg_content):
		t = []
		main_content = msg_content.split(":",1)[1]
		t = main_content.split()
		#x是由t列表通过set()生成相应的集合，再通过list()转换而得的列表，这样做是为了去掉t集合中用户可能输入的重复项
		x = list(set(t))
		#如果不通过sort重新排序的话，直接比较x和t列表，很可能因为列表项的顺序不同误判认为x和t所包含的项不相同。为此我们通过sort方法重新排序两个列表
		x.sort()
		t.sort()
		if self.is_leader:
			#玩家的输入验证，确保玩家输入有效的ID信息
			if (main_content.isspace()) or (len(main_content)==0):
				return u"对不起，妳的输入有误，选择妳想要派遣执行任务的玩家的ID，并且按照例如 “select:1 2” 的形式输入，多个玩家ID之间使用空格隔开1"	
			elif not main_content.replace(" ","").isdigit():
				return u"对不起，妳的输入有误，选择妳想要派遣执行任务的玩家的ID，并且按照例如 “select:1 2” 的形式输入，多个玩家ID之间使用空格隔开2"
			elif (int(max(t)) > num_of_player) or (int(min(t)) < 1):
				return u"对不起，妳的输入有误，选择妳想要派遣执行任务的玩家的ID，并且按照例如 “select:1 2” 的形式输入，多个玩家ID之间使用空格隔开3"
			elif x!= t:
				return u"对不起，妳的输入有误，选择妳想要派遣执行任务的玩家的ID，并且按照例如 “select:1 2” 的形式输入，多个玩家ID之间使用空格隔开4"
			elif len(t) != num_of_executants:
				return u"对不起，妳的输入有误，请确保你输入的派遣人数为本次任务所需要的人数，本次任务需要%d人来执行。"% num_of_executants
			else:
				a = ""
				for i in t:
					player = find_player_by_id(i)
					player.is_executant = True
					a = a + u" %s号 "%i
				#保存被选择出的任务玩家
				for i in t:
					executants.append(player_list[int(i)-1])
				return u"妳选择了"+ a + u"玩家进行任务，现在请所有玩家进行投票表决，以决定是否让这几位玩家进行任务"
		else:
			return u"对不起，只有队长才有权选择派遣的人"

	def vote(self, msg_content):
		valid = False
		main_content = msg_content.split(":",1)[1]
		ballot = main_content.strip()
		if ( ballot == "y")or(ballot == "n"):
			valid = True
		return (valid, ballot)

	def execution(self):
		ballot = ""
		if self.is_good :
			print "请做出你的任务决定（请注意你是好人），小写y代表成功，小写n代表失败"
			while 1:
				ballot = raw_input_vote()
				if ballot == 'y':
					print "%s已做出决定"% self.name
					break
				else:
					print "你是好人，你只能做出使任务成功的决定，请重新做决定"
		else:
			print "请做出你的任务决定（请注意你是坏人），小写y代表成功，小写n代表失败"
			ballot = raw_input_vote()
			print "%s已做出决定"% self.name
		return ballot


# def start_game():
# 	print "游戏开始"
# 	executants = []
# 	gamestatus = []
# 	num_of_executants = 2
# 	flag = 1

# 	#展示玩家的个人身份信息	
# 	for i in player_list:
# 		i.show_self_info()

# 	#游戏一共有5个单局任务构成，其中一旦失败的任务，或者成功的任务数超过3个，游戏都将结束
# 	#以下代码使用一个while循环来进行这5个单据任务，flag指示了当前所处任务局数
# 	while flag < 6:
# 		print "游戏当前处于任务%d"% flag
# 		print "当前已经成功了%d个任务，失败了个%d任务"% (gamestatus.count("y"), gamestatus.count("n"))
# 		ballots = ""
# 		task = ""
# 		leaderid = 0

# 		if flag == 1:
# 			num_of_executants = 2
# 		if flag == 2:
# 			num_of_executants = 3
# 		if flag == 3:
# 			num_of_executants = 4
# 		if flag == 4:
# 			num_of_executants = 3
# 		if flag == 5:
# 			num_of_executants = 4

# 		#队长提议执行者
# 		for i in player_list:
# 			if i.is_leader:
# 				print "当前队长是%d号玩家%s"% (i.id, i.name)
# 				leaderid = i.id
# 				executants = i.choose_executant(num_of_executants)
# 				break
		
# 		#众人进行投票
# 		print "队长提议的任务执行者是" + print_executants(executants, num_of_executants)
# 		for i in player_list:
# 			ballots += i.vote();

# 		if ballots.count('y') > (num_of_player/2):
# 			#投票通过
# 			print "%s个人同意，%s个人反对。票数过半，投票通过"% (ballots.count('y'), ballots.count('n'))

# 			#投票通过后任务执行者开始执行任务
# 			print "现在请"+ print_executants(executants, num_of_executants) +"进行任务"

# 			for i in executants:
# 				task += i.execution();
# 			if task.count("n") >0:
# 				print "%d票成功，%d票失败。任务失败"% (task.count("y"), task.count("n"))
# 				gamestatus.append("n")
# 			else:
# 				print "%d票成功，%d票失败。任务成功"% (task.count("y"), task.count("n"))
# 				gamestatus.append("y")

# 			#做5局3胜的判断
# 			if gamestatus.count("n") > 2:
# 				print "游戏结束，成功了%d个任务，失败了个%d任务，坏人赢得了比赛"% (gamestatus.count("y"), gamestatus.count("n"))
# 				break
# 			elif gamestatus.count("y") > 2:
# 				print "游戏结束，成功了%d个任务，失败了个%d任务，好人赢得了比赛"% (gamestatus.count("y"), gamestatus.count("n"))
# 				break
# 			flag += 1
# 			#将队长的身份向后移
# 			player_list[leaderid-1].is_leader = False
# 			if leaderid == 6:
# 				player_list[0].is_leader = True
# 			else:
# 				player_list[leaderid].is_leader = True

# 		else:
# 			#投票未通过
# 			print "%s个人同意，%s个人反对。票数未过半，更换队长，并且游戏继续"% (ballots.count('y'), ballots.count('n'))
# 			#将队长的身份向后移
# 			player_list[leaderid-1].is_leader = False
# 			if leaderid == 6:
# 				player_list[0].is_leader = True
# 			else:
# 				player_list[leaderid].is_leader = True

def init_player(name,wechatID):
	global player_list
	global playerFlag
	global player_wechatIDs
	player_list.append(Player(id=playerFlag, name=name, wechatID=wechatID))
	player_wechatIDs.append(wechatID)
	playerFlag += 1	

def random_leader():
	leaderid = random.randrange(1,6,1)
	return leaderid

def random_bad_guy():
	bad_guy_list = []
	bad_guy_1 = random.randrange(1,6,1)
	bad_guy_2 = random.randrange(1,6,1)
	i =True
	while i:
		if bad_guy_1 == bad_guy_2:
			bad_guy_2 = random.randrange(1,6,1)
		else:
			i = False
	bad_guy_list.append(bad_guy_1)
	bad_guy_list.append(bad_guy_2)
	return bad_guy_list

def find_player_by_wechatID(wechatID):
	for a in player_list:
		if a.wechatID == wechatID:
			return a

def find_player_by_id(id):
	id = int(id)
	for a in player_list:
		if a.id == id:
			return a
	
# def print_executants(executants, num_of_executants):
# 	sentence = ""
# 	if num_of_executants == 2:
# 		sentence = "%d号玩家%s, %d号玩家%s"% (executants[0].id, executants[0].name, executants[1].id, executants[1].name)
# 	if num_of_executants == 3:
# 		sentence = "%d号玩家%s, %d号玩家%s, %d号玩家%s"% (executants[0].id, executants[0].name, executants[1].id, executants[1].name, executants[2].id, executants[2].name)
# 	if num_of_executants == 4:
# 		sentence = "%d号玩家%s, %d号玩家%s, %d号玩家%s, %d号玩家%s"% (executants[0].id, executants[0].name, executants[1].id, executants[1].name, executants[2].id, executants[2].name, executants[3].id, executants[3].name)
# 	return sentence




#####################################################
AuthorID = "oLXjgjiWeAS1gfe4ECchYewwoyTc"
TPL_TEXT = """<xml>
             <ToUserName><![CDATA[%s]]></ToUserName>
             <FromUserName><![CDATA[%s]]></FromUserName>
             <CreateTime>%s</CreateTime>
             <MsgType><![CDATA[text]]></MsgType>
             <Content><![CDATA[%s]]></Content>
             <FuncFlag>0</FuncFlag>
             </xml>"""

##初始化游戏全局参数
gameStart = False
gameInit = False
gameVote = False
gameExe = False
executants = []	
gamestatus = []
num_of_executants = 2
flag = 1
ballots = ""
voted_players = []
executants = []


@get("/")
def checkSignature():
	"""
	这里是用来做接口验证的，从微信Server请求的URL中拿到“signature”,“timestamp”,"nonce"和“echostr”，
	然后再将token, timestamp, nonce三个排序并进行Sha1计算，并将计算结果和拿到的signature进行比较，
	如果相等，就说明验证通过。
	话说微信的这个验证做的很渣，因为只要把echostr返回去，就能通过验证，这也就造成我看到一个Blog中，
	验证那儿只返回了一个echostr，而纳闷了半天。
	附微信Server请求的Url示例：http://yoursaeappid.sinaapp.com/?signature=730e3111ed7303fef52513c8733b431a0f933c7c
	&echostr=5853059253416844429&timestamp=1362713741&nonce=1362771581
	"""
	token = "solairwechat"  # 你在微信公众平台上设置的TOKEN
	signature = request.GET.get('signature', None)  # 拼写不对害死人那，把signature写成singnature，直接导致怎么也认证不成功
	timestamp = request.GET.get('timestamp', None)
	nonce = request.GET.get('nonce', None)
	echostr = request.GET.get('echostr', None)
	tmpList = [token, timestamp, nonce]
	tmpList.sort()
	tmpstr = "%s%s%s" % tuple(tmpList)
	hashstr = hashlib.sha1(tmpstr).hexdigest()
	if hashstr == signature:
		return echostr
	else:
		return None

def parse_msg():
	"""
	这里是用来解析微信Server Post过来的XML数据的，取出各字段对应的值，以备后面的代码调用，也可用lxml等模块。
	"""
	recvmsg = request.body.read()  # 严重卡壳的地方，最后还是在Stack OverFlow上找到了答案
	root = ET.fromstring(recvmsg)
	msg = {}
	for child in root:
		msg[child.tag] = child.text
	return msg

def mix_echostr(user, touser, content):
	echostr = TPL_TEXT %(user, touser,str(int(time.time())), content)
	return echostr
		
@post("/")
def response_msg():
	global gameStart
	global gameInit
	global gameVote
	global gameExe
	global player_list
	global player_wechatIDs #####
	global playerFlag
	global leaderid
	global bad_guy_list
	global num_of_executants
	global flag
	global ballots
	global voted_players
	global executants

	
	##这里把系统命令分成了 普通命令，带参数命令，超级命令。其中超级命令只有授权账号才能使用
	commands = ['show:','view:']
	super_commands = ['start:','exit:','reset:']
	commands_with_args = ['vote:','select:','exe:']

	msg = parse_msg()
	msg_user = msg["FromUserName"]

	if msg["MsgType"] == "event" :
		echostr =  mix_echostr(msg_user,  msg['ToUserName'], u"欢迎关注sola的个人订阅号！！")
		return echostr
	else:
		msg_content = msg["Content"]

		##如果用户输入的是系统超级命令
		if msg_content in super_commands:
			if msg_user == AuthorID:
				if msg_content == 'start:':
				##系统超级命令 —— 开始游戏
					if gameStart:
						content = u"游戏已经开始了！！！" 
						echostr = mix_echostr(msg_user, msg['ToUserName'], content)
						return echostr
					else:
						gameStart = True
						##标记游戏开始，并随机出玩家身份
						leaderid = random_leader()
						bad_guy_list = random_bad_guy()
						content = u"游戏即将开始，等待玩家依次加入游戏 ... ..." 
						echostr = mix_echostr(msg_user, msg['ToUserName'], content)
						return echostr
				elif msg_content == 'exit:':
				##系统超级命令 —— 结束游戏
					if gameStart:
						content = u"游戏已经强行结束！！！"
						gameStart = 0
						# 此处释放已经初始化的player实例，清空player_list
						player_list = []
						player_wechatIDs = []
						playerFlag = 1
						num_of_executants = 2
						flag = 1
						echostr = TPL_TEXT %(msg_user, msg['ToUserName'],str(int(time.time())), content)
						return echostr
					else:
						content = u"游戏并没有开始！！！" 
						echostr = mix_echostr(msg_user, msg['ToUserName'], content)
						return echostr
				elif msg_content == 'reset:':
				##系统超级命令 —— 重置玩家身份
					if gameInit:
						gameVote = False
						gameExe = False
						num_of_executants = 2
						flag = 1
						leaderid = random_leader()
						bad_guy_list = random_bad_guy()
						for a in player_list:
							a.is_executant = False
							if a.id == leaderid:
								a.is_leader = True
							else:
								a.is_leader = False
							if a.id in bad_guy_list:
								a.is_good = False
							else:
								a.is_good = True

						content = u"已经重新分配了玩家身份，可以重新开始新一轮游戏了！！！" 
						echostr = mix_echostr(msg_user, msg['ToUserName'], content)
						return echostr
					else:
						content = u"玩家还没有完全加入游戏！！！" 
						echostr = mix_echostr(msg_user, msg['ToUserName'], content)
						return echostr
			else:
				echostr = mix_echostr(msg_user, msg['ToUserName'],u'妳没有权限使用该系统命令')
				return echostr
		##如果用户输入的是普通命令
		elif msg_content in commands:
			##
			if msg_content == 'show:':
				if gameStart and gameInit:
					for i in player_list:
						if msg_user == i.wechatID:
							echostr = mix_echostr(msg_user, msg['ToUserName'],i.show_self_info())
							return echostr
				else:
					echostr = mix_echostr(msg_user, msg['ToUserName'],u"等待所有玩家加入游戏后才可使用show:命令")
					return echostr
			##
			elif msg_content == 'view:':
				if gameStart and gameInit:
					content = u"现在是本轮游戏的第%d局，该局需要推选出%d人进行任务，本局队长是%d号玩家"% (flag,num_of_executants,leaderid)
					echostr = mix_echostr(msg_user, msg['ToUserName'],content)
					return echostr
				else:
					echostr = mix_echostr(msg_user, msg['ToUserName'],u"等待所有玩家加入游戏后才可使用view:命令")
					return echostr
		##如果用户输入的是带参数的命令
		elif msg_content.split(":",1)[0]+":" in commands_with_args and msg_content.find(":") >= 0:
			##
			if msg_content.split(":",1)[0]+":" == 'select:':
				if gameStart and gameInit and not gameExe:
					player = find_player_by_wechatID(msg_user)
					if player:
						if player.is_leader:
							##队长选择任务执行者后，开启玩家投票命令的权限
							gameVote = True
							echostr = mix_echostr(msg_user, msg['ToUserName'],player.choose_executant(num_of_executants,msg_content))
							return echostr
						else:
							echostr = mix_echostr(msg_user, msg['ToUserName'],u"只有本局队长才有权使用select:命令")
							return echostr
					else:
						echostr = mix_echostr(msg_user, msg['ToUserName'],u"妳并没有加入游戏，无法使用select:命令")
						return echostr						
				else:
					echostr = mix_echostr(msg_user, msg['ToUserName'],u"现在无法使用select:命令")
					return echostr
			##
			elif msg_content.split(":",1)[0]+":" == 'vote:':
				if gameStart and gameInit and gameVote:
					player = find_player_by_wechatID(msg_user)
					if player:
						if player not in voted_players:
							valid, ballot = player.vote(msg_content)
							if not valid:
								echostr = mix_echostr(msg_user, msg['ToUserName'],u"无效输入，请重新输入，小写y代表同意，小写n代表不同意，并且按照例如 “vote:y” 的形式输入")
							else:
								voted_players.append(player)
								ballots += ballot
								if len(ballots) == num_of_player:
									#关闭投票标记
									gameVote = False
									#将队长的身份向后移
									player_list[leaderid-1].is_leader = False
									if leaderid == 6:
										player_list[0].is_leader = True
										leaderid = 1
									else:
										player_list[leaderid].is_leader = True
										leaderid += 1
									
									if ballots.count('y') > (num_of_player/2):
										#投票通过
										gameExe = True
										result = u"其中%s个人同意，%s个人反对。票数过半，投票通过，接下来等待所选定的玩家进行任务投票"% (ballots.count('y'), ballots.count('n'))
										#清空所有投票
										voted_players = []
										ballots = ""
									else:
										#投票未通过
										result = u"其中%s个人同意，%s个人反对。票数未过半，更换队长，新队长为%s号玩家，并且继续进行该局"% (ballots.count('y'), ballots.count('n'), leaderid)
										#清空所有投票
										voted_players = []
										ballots = ""
										executants = []
									echostr = mix_echostr(msg_user, msg['ToUserName'],u"妳已投票成功，并且所有玩家也已投票完毕。"+result)
								else:
									echostr = mix_echostr(msg_user, msg['ToUserName'],u"妳已投票成功，等待其她玩家投票中...")
							return echostr
						else:
							echostr = mix_echostr(msg_user, msg['ToUserName'],u"本局妳已经投过票了！！等待其她玩家投票中...")
							return echostr
					else:
						echostr = mix_echostr(msg_user, msg['ToUserName'],u"妳并没有加入游戏，无法使用vote:命令")
						return echostr	
				else:
					echostr = mix_echostr(msg_user, msg['ToUserName'],u"现在无法使用vote:命令")
					return echostr
			##
			elif msg_content.split(":",1)[0]+":" == 'exe:':
				if gameStart and gameInit and gameExe:
					player = find_player_by_wechatID(msg_user)
					if player:
						if player in executants:
							pass
							print "works"
						else:
							echostr = mix_echostr(msg_user, msg['ToUserName'],u"只有该局被选中的玩家才可以使用exe:命令进行任务投票！！！")
							return echostr
					else:
						echostr = mix_echostr(msg_user, msg['ToUserName'],u"妳并没有加入游戏，无法使用exe:命令")
						return echostr
				else:
					echostr = mix_echostr(msg_user, msg['ToUserName'],u"现在无法使用exe:命令")
					return echostr


		##如果用户输入的是普通文本
		else:
			if gameStart and not gameInit :
			##如果游戏开始，但还未完成玩家注册
				for a in player_list :
					if msg_user == a.wechatID:
						# print "你已经在游戏中了"
						content = u"你已经在游戏中了，等待其她玩家加入"
						echostr = mix_echostr(msg_user, msg['ToUserName'], content)
						# print player_list
						return echostr
				init_player(msg_content,msg_user)
				player = player_list[playerFlag-2]
				if player.id == leaderid:
					player.is_leader = True
				if player.id in bad_guy_list:
					player.is_good = False

				content = u"你已成功加入游戏，"+ player.show_self_info()
				echostr = mix_echostr(msg_user, msg['ToUserName'], content)
				if playerFlag == 7:
					gameInit = True
				# print player_list 
				return echostr
			else:
				echostr = mix_echostr(msg_user, msg['ToUserName'],u'无效的命令')
				return echostr

if __name__ == '__main__':
	debug(True)
	run(host='localhost',port=8080,reloader=True)
else:
	pass
