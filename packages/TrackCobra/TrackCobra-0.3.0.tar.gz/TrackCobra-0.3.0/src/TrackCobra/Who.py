import requests
url = 'https://ipinfo.io/'
class Get:
	def MyFormation(Form):
		try:
			response = requests.get(url)
			if 'IP' in Form:
				return response.json()['ip']
				pass
			elif 'City' in Form:
				return response.json()['city']
				pass
			elif 'Region' in Form:
				return response.json()['region']
				pass
			elif 'Country' in Form:
				return response.json()['country']
				pass
			elif 'Location' in Form:
				return response.json()['loc']
				pass	
			elif 'Org' in Form:
				return response.json()['org']
				pass
			elif 'Timezone' in Form:
				return response.json()['timezone']
				pass
			elif 'All' in Form:
				return f"""IP : {response.json()['ip']}
City : {response.json()['city']}
Region : {response.json()['region']}
Country : {response.json()['country']}
Timezone : {response.json()['timezone']}
Loc : {response.json()['loc']}
Org : {response.json()['org']}"""
				pass
			elif 'Help' in Form:
				print("""all types:
				
IP
City
Region
Country
Location
Org
Timezone
All --> all types""")
			else:
				return False
				pass
		except:
			return 'Error'
			pass
			
			
			
			
	def IPFormation(IP,Form):
		try:
			response = requests.get(url+IP)
			if 'IP' in Form:
				return IP
				pass
			elif 'City' in Form:
				return response.json()['city']
				pass
			elif 'Region' in Form:
				return response.json()['region']
				pass
			elif 'Country' in Form:
				return response.json()['country']
				pass
			elif 'Location' in Form:
				return response.json()['loc']
				pass	
			elif 'Org' in Form:
				return response.json()['org']
				pass
			elif 'Timezone' in Form:
				return response.json()['timezone']
				pass
			elif 'All' in Form:
				all = f"""IP : {response.json()['ip']}
City : {response.json()['city']}
Region : {response.json()['region']}
Country : {response.json()['country']}
Timezone : {response.json()['timezone']}
Loc : {response.json()['loc']}
Org : {response.json()['org']}"""
				return all
				pass
			elif 'Help' in Form:
				print("""all types:
				
IP
City
Region
Country
Location
Org
Timezone
All --> all types""")
			else:
				return False
				pass
		except:
			return 'Error'
			pass