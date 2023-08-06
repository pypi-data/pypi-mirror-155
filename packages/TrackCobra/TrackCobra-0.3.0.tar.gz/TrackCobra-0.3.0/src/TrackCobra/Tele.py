import requests

class Telegram:
	def SendMessage(ID,Token,Message):
		try:
			req = requests.get(f'https://api.telegram.org/bot{Token}/getme').json()
			if req['ok'] == True:
				t = requests.post(f"https://api.telegram.org/bot{Token}/sendMessage?chat_id={ID}&text={Message}")
				return True
				pass
			else:
				return False
				pass
		except:
			return 'Error'
			pass
