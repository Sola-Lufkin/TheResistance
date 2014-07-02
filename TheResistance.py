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
playerFlag = 1

leaderid = 0
bad_guy_list =[]

class Player:
	"""docstring for Player"""

	is_leader = False
	is_good = True

	def __init__(self, **kwargs):
		self.name = kwargs['name']
		self.id = kwargs['id']
		self.wechatID = kwargs['wechatID']

	def show_self_info(self):
		if self.is_good:
			x = "好人"
		else:
			x = "坏人"

		if self.is_leader:
			a = "你的名称是%s，ID是%s，身份是%s 。并且你是本局的队长"% (self.name, self.id, x)
			print a
			return a
		else:
			a = "你的名称是%s，ID是%s，身份是%s 。"% (self.name, self.id, x)
			print a
			return a

	def show_leader(self):
		for i in player_list:
			if i.is_leader:
				print "当前队长是%s"% i.name
				break

	def choose_executant(self, num_of_executants):
		t = []
		executants = []
		if self.is_leader:
			print "本次任务需要%d人来执行，请输入你决定派遣的人的ID，ID之间请用空格分格开"% num_of_executants
			#玩家的输入验证，确保玩家输入有效的ID信息
			while 1:
				a  = raw_input_nospace()
				if not a.replace(" ","").isdigit():
					print "无效输入，请重新输入，确保你输入的为有效的玩家ID号"
					continue
				t = a.split( )
				if (int(max(t)) > num_of_player) or (int(min(t)) < 1):
					print "无效输入，请重新输入，确保你输入的为有效的玩家ID号"
					continue
				#x是由t列表通过set()生成相应的集合，再通过list()转换而得的列表，这样做是为了去掉t集合中用户可能输入的重复项
				x = list(set(t))
				#如果不通过sort重新排序的话，直接比较x和t列表，很可能因为列表项的顺序不同误判认为x和t所包含的项不相同。为此我们通过sort方法重新排序两个列表
				x.sort()
				t.sort()
				if x != t:
					print "无效输入，请重新输入，确保你输入的为不同的玩家ID"
					continue
				if len(t) == num_of_executants:
					break
				print "无效输入，请确保你输入的派遣人数为本次任务所需要的人数，本次任务需要%d人来执行。"% num_of_executants
			for i in t:
				executants.append(player_list[int(i)-1])
		else:
			print "对不起，只有队长才有权选择派遣的人"
		return executants

	def vote(self):
		print "请你为本局队长做出的派遣决定进行投票，小写y代表同意，小写n代表不同意"
		ballot = raw_input_vote()
		return ballot

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
	
def start_game():
	print "游戏开始"
	executants = []
	gamestatus = []
	num_of_executants = 2
	flag = 1

	#展示玩家的个人身份信息	
	for i in player_list:
		i.show_self_info()

	#游戏一共有5个单局任务构成，其中一旦失败的任务，或者成功的任务数超过3个，游戏都将结束
	#以下代码使用一个while循环来进行这5个单据任务，flag指示了当前所处任务局数
	while flag < 6:
		print "游戏当前处于任务%d"% flag
		print "当前已经成功了%d个任务，失败了个%d任务"% (gamestatus.count("y"), gamestatus.count("n"))
		ballots = ""
		task = ""
		leaderid = 0

		if flag == 1:
			num_of_executants = 2
		if flag == 2:
			num_of_executants = 3
		if flag == 3:
			num_of_executants = 4
		if flag == 4:
			num_of_executants = 3
		if flag == 5:
			num_of_executants = 4

		#队长提议执行者
		for i in player_list:
			if i.is_leader:
				print "当前队长是%d号玩家%s"% (i.id, i.name)
				leaderid = i.id
				executants = i.choose_executant(num_of_executants)
				break
		
		#众人进行投票
		print "队长提议的任务执行者是" + print_executants(executants, num_of_executants)
		for i in player_list:
			ballots += i.vote();

		if ballots.count('y') > (num_of_player/2):
			#投票通过
			print "%s个人同意，%s个人反对。票数过半，投票通过"% (ballots.count('y'), ballots.count('n'))

			#投票通过后任务执行者开始执行任务
			print "现在请"+ print_executants(executants, num_of_executants) +"进行任务"

			for i in executants:
				task += i.execution();
			if task.count("n") >0:
				print "%d票成功，%d票失败。任务失败"% (task.count("y"), task.count("n"))
				gamestatus.append("n")
			else:
				print "%d票成功，%d票失败。任务成功"% (task.count("y"), task.count("n"))
				gamestatus.append("y")

			#做5局3胜的判断
			if gamestatus.count("n") > 2:
				print "游戏结束，成功了%d个任务，失败了个%d任务，坏人赢得了比赛"% (gamestatus.count("y"), gamestatus.count("n"))
				break
			elif gamestatus.count("y") > 2:
				print "游戏结束，成功了%d个任务，失败了个%d任务，好人赢得了比赛"% (gamestatus.count("y"), gamestatus.count("n"))
				break
			flag += 1
			#将队长的身份向后移
			player_list[leaderid-1].is_leader = False
			if leaderid == 6:
				player_list[0].is_leader = True
			else:
				player_list[leaderid].is_leader = True

		else:
			#投票未通过
			print "%s个人同意，%s个人反对。票数未过半，更换队长，并且游戏继续"% (ballots.count('y'), ballots.count('n'))
			#将队长的身份向后移
			player_list[leaderid-1].is_leader = False
			if leaderid == 6:
				player_list[0].is_leader = True
			else:
				player_list[leaderid].is_leader = True

def init_player(name,wechatID):
	global player_list
	global playerFlag
	player_list.append(Player(id=playerFlag, name=name, wechatID=wechatID))
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
	
def raw_input_nospace():
	words = ""
	while 1:
		words = raw_input()
		if (not words.isspace())and(len(words)!=0):
			break
		print "你的输入为无效输入，请重新输入"
	words = words.strip()
	return words

def raw_input_vote():
	words = ""
	while 1:
		words = raw_input_nospace()
		if (words == "y")or(words == "n"):
			break
		print "无效输入，请重新输入，小写y代表同意，小写n代表不同意"
	return words

def print_executants(executants, num_of_executants):
	sentence = ""
	if num_of_executants == 2:
		sentence = "%d号玩家%s, %d号玩家%s"% (executants[0].id, executants[0].name, executants[1].id, executants[1].name)
	if num_of_executants == 3:
		sentence = "%d号玩家%s, %d号玩家%s, %d号玩家%s"% (executants[0].id, executants[0].name, executants[1].id, executants[1].name, executants[2].id, executants[2].name)
	if num_of_executants == 4:
		sentence = "%d号玩家%s, %d号玩家%s, %d号玩家%s, %d号玩家%s"% (executants[0].id, executants[0].name, executants[1].id, executants[1].name, executants[2].id, executants[2].name, executants[3].id, executants[3].name)
	return sentence




#####################################################


AuthorID = "oLXjgjiWeAS1gfe4ECchYewwoyTc"

gameStart = False
gameInit = False

TPL_TEXT = """<xml>
             <ToUserName><![CDATA[%s]]></ToUserName>
             <FromUserName><![CDATA[%s]]></FromUserName>
             <CreateTime>%s</CreateTime>
             <MsgType><![CDATA[text]]></MsgType>
             <Content><![CDATA[%s]]></Content>
             <FuncFlag>0</FuncFlag>
             </xml>"""

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
	global player_list
	global playerFlag
	global leaderid
	global bad_guy_list

	commands = ['vote:','show:','select:','view:']
	super_commands = commands + ['s','c']

	msg = parse_msg()
	msg_user = msg["FromUserName"]

	if msg["MsgType"] == "event" :
		echostr =  mix_echostr(msg_user,  msg['ToUserName'], u"欢迎关注sola的个人订阅号！！")
		return echostr
	else:
		msg_content = msg["Content"]
		if gameStart:
			if playerFlag < 7:
					for a in player_list :
						if msg_user == a.wechatID:
							print "你已经在游戏中了"
							content = u"你已经在游戏中了，等待其她玩家加入"
							echostr = mix_echostr(msg_user, msg['ToUserName'], content)
							print player_list
							return echostr
					init_player(msg_content,msg_user)

					player = player_list[playerFlag-2]
					if player.id == leaderid:
						player.is_leader = True
					if player.id in bad_guy_list:
						player.is_good = False

					content = u"你已成功加入游戏，你是%s号玩家，你的昵称为%s，身份为%s，是否是本局队长%s"% (player.id,player.name,player.is_good,player.is_leader)
					echostr = mix_echostr(msg_user, msg['ToUserName'], content)
					if playerFlag == 6:
						gameInit = True

					print player_list
					return echostr
			else:
				content = u"游戏已满员"
				echostr = TPL_TEXT %(msg_user, msg['ToUserName'],str(int(time.time())), content)
				return echostr
		else:
			if msg_user == AuthorID:
				if msg_content == 's':
					gameStart = 1
					leaderid = random_leader()
					bad_guy_list = random_bad_guy()

					init_player("sola",msg_user)
					player = player_list[playerFlag-2]
					if player.id == leaderid:
						player.is_leader = True
					if player.id in bad_guy_list:
						player.is_good = False
					content = u"游戏即将开始，当前为%d人局，%d个好人，%d个坏人，你是%s号玩家，昵称%s为，身份为%s，是否是本局队长%s"% (num_of_player, num_of_good, num_of_bad,player.id,player.name,player.is_good,player.is_leader)
					echostr = mix_echostr(msg_user, msg['ToUserName'], content)
					return echostr
				else:
					echostr = mix_echostr(msg_user, msg['ToUserName'], u"游戏还没有开始，输入小写s开始游戏")
					return echostr	
			else:
				echostr = mix_echostr(msg_user, msg['ToUserName'], u"游戏还没有开始")
				return echostr		
		

if __name__ == '__main__':
	debug(True)
	run(host='localhost',port=8080,reloader=True)
else:
	pass
