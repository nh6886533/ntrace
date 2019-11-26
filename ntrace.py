# -*- coding: UTF-8 -*-
#!/usr/bin/python3
#public module
import re, telnetlib, socket, sys, time

class TelnetHandler:
	'''use telnetlib to connect device
	'''
	def __init__(self,devip):
		'''
		'''
		self.tn = self.login(devip)

	def login(self,devip,username='xxx',password='xxx'):
		'''设备登陆，返回实例
		'''
		tn = None
		try:
			tn = telnetlib.Telnet(devip ,port = 23, timeout = 2)
			
			#如果用户名提示符不是username则报错
			prompt = tn.read_until(b'name:', timeout = 4).decode('ascii')
			if re.search('(name:)', prompt) == None:
				tn.close()
#				print('Error: No username prompt', end='')
			
			else:
				tn.write(username.encode('ascii') + b'\n')
				tn.read_until(b'word:')
				tn.write(password.encode('ascii') + b'\n')
				res = tn.read_until(b'#').decode('ascii')
				#当用户名或密码错误时返回' '
				
				if res == ' ':
					tn.close()
#					print('Error: Authentication failed', end='')
				
				#正常执行返回tn实例
				else:
					#得到设备名					
					tn.write(b'terminal length 0\n')
					res = tn.read_until(b'#').decode('ascii')
					self.hostname = re.search('(\S+)#', res).group(1)
					return tn
		
		#超时异常		
		except socket.timeout:
#			print('Error: Telnet '+devip+' timeout', end='')
			return None

	def is_login(self):
		'''判断login是否成功
		'''
		if self.tn != None:
			try:
				self.send_command('')
				host = re.search('(\S+)#', self.tn.read_until(b'#').decode('ascii'))
				if host:
					if host.group(1) == self.hostname:
						return True
					else:
						return False
				else:
					return False
			except Exception:
				return False
	
	def send_command(self, command):
		'''推送命令得到结果
		'''
		self.tn.write(command.encode('ascii') + b'\n')
#		return (self.tn.read_until(b'#').decode('ascii'))

	def read(self, flag):
		return self.tn.read_until(flag, timeout=3).decode('ascii')

	def close(self):
		'''关闭telnet连接
		'''
		self.tn.close()

def find_name(ip):
	'''telnet ip to find the hostname
	'''
	conn = TelnetHandler(ip)
	if conn.is_login():
		conn.close()
		return conn.hostname
	else:
		return ''

def main(src,dst):
	'''
	'''
	conn = TelnetHandler(src)
	if conn.is_login():
		conn.send_command('traceroute '+dst)
		line = 0
		while True:
			res = conn.read(b'\n')
			if conn.hostname in res:break
			line += 1
			if line <= 4:continue
			try:
				ip = re.search('(\d+\.\d+\.\d+\.\d+)', res).group(1)
			except AttributeError:
				print(res, end='')
			else:
				if re.match('10\.', ip) or re.match('172\.', ip):
					print(res.replace('\r\n', '\t'+find_name(ip)))
				else:
					print(res, end='')
		conn.close()

if __name__ == '__main__':
	main(sys.argv[1],sys.argv[2])
