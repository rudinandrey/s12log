import socket
import sys, os
import mysql.connector

host = os.environ['HOST']
user = os.environ['USER']
password = os.environ['PASSWORD']
database = os.environ['DATABASE']
raptor = os.environ['RAPTOR']

def main():
	if raptor == '':
		print('Не указан сервер S-12')
		exit(1)
	if host == '':
		print('Не указан сервер базы данных MySQL')
		exit(1)
	if database == '':
		print('Не указана база данных')
		exit(1)
	if user == '':
		print('не указан пользователь базы данных')
		exit(1)
	print(raptor)
	print(host, database, user)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((raptor, 23))

	cnx = mysql.connector.connect(
		host=host, user=user, password=password, database=database)
	cursor = cnx.cursor()

	sql = ("INSERT INTO leninogorsk"
		"(data, body)"
		"VALUES (NOW(), %(body)s)"
		)

	f = open("log.log", "a")
	mess = ''

	try:
		while True:
			data = sock.recv(16)
			mess = mess + data.decode()
			f.write(mess)
			start = mess.find(chr(2))
			end = mess.find(chr(3))
			if start < end:
				log = mess[start+1: end]
				print(log)
				mess = mess[end+1:]
				cursor.execute(sql, {'body': log})
				cnx.commit()
	finally:
		sock.close()
		f.close()
		cursor.close()
		cnx.close()

if __name__ == '__main__':
	try:	
		main()
	except KeyboardInterrupt:
		print("interrupted")
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
	finally:
		pass