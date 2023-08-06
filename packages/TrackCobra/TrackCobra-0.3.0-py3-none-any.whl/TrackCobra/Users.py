import requests

headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
        }

class User:
    def Pypi(Name):
      	  try:
      	  	url = f"https://pypi.org/user/{Name}/"
      	  	req = requests.get(url,headers=headers).ok
      	  	return req
      	  	pass
      	  except:
      	  	return 'Error'
      	  	pass



    def Github(Name):
        	try:
        		url = f"https://github.com/{Name}"
        		req = requests.get(url,headers=headers).ok
        		return req
        		pass
        	except:
        		return 'Error'
        		pass



    def Snapchat(Name):
    	    try:
    	    	url = f"https://www.snapchat.com/add/{Name}"
    	    	req = requests.get(url,headers=headers).ok
    	    	return req
    	    	pass
    	    except:
    	    	return 'Error'
    	    	pass
    	    


    def Xbox(Name):
     	   try:
     	   	url = f"https://xboxgamertag.com/search/{Name}"
     	   	req = requests.get(url,headers=headers).ok
     	   	return req
     	   	pass
     	   except:
     	   	return 'Error'
     	   	pass


    def Steam(Name):
       	 try:
       	 	url = f"https://steamcommunity.com/id/{Name}"
       	 	req = requests.get(url,headers=headers).text
       	 	if "An error was encountered while processing your request" in req:
       	 	   return False
       	 	   pass
       	 	else:
       	 		return True
       	 		pass
       	 except:
       	 	return 'Error'
       	 	pass
			


    def Telegram(Name):
     	   try:
     	   	url = f"https://t.me/{Name}"
     	   	req = requests.get(url,headers=headers).text
     	   	if f'<meta property="og:title" content="Telegram: Contact @{Name}">' in req:
     	   	   return False
     	   	   pass
     	   	else:
     	   		return True
     	   		pass
     	   except:
     	   	return 'Error'
     	   	pass


    def Likee(Name):
      	  try:
      	  	url = f"https://likee.video/@{Name}"
      	  	req = requests.get(url,headers=headers).ok
      	  	return req
      	  	pass
      	  except:
      	  	return 'Error'
      	  	pass


    def Playstation(Name):
        	try:
        		url = f"https://psnprofiles.com/search/users?q={Name}"
        		req = requests.get(url,headers=headers).text
        		if "We couldn't find anything" in req:
        			return False
        			pass
        		else:
        		   return True
        		   pass
        	except:
        		return 'Error'
        		pass
			

    def Tellonym(Name):
      	  try:
      	  	url = f"https://api.tellonym.me/profiles/name/{Name}?limit=13"
      	  	req = requests.get(url,headers=headers).text
      	  	if '{"err":' in req:
      	  	   return False
      	  	   pass
      	  	else:
      	  	   return True
      	  	   pass
      	  except:
      	  	return 'Error'
      	  	pass 