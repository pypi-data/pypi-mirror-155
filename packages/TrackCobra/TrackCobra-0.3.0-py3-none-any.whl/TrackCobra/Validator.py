import requests
import json
import mechanize

class Valid:
	def Facebook(Email):
		try:
			br = mechanize.Browser()
			br.set_handle_robots(False)
			url = 'https://mbasic.facebook.com/login/identify/?ctx=recover'
			br.addheaders = [('User-agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/45.0.2454101')]
			br.open(url)
			br.select_form(nr=0)
			br.set_all_readonly(False)
			br["email"] = Email
			req = br.submit()
			if 'login/identify/?ctx=recove' in req.geturl():
				return False
				pass
			else:
				return True
				pass
		except:
			return 'Error'
			pass

	
	
	def Instagram(Email):
		try:
			s = requests.Session()
			head={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
'X-CSRFToken':'klMtcv9FbwmJ2O1VRrQSDYoqbiKAUpRf',
'Cookie':'g_cb=1; ig_did=7C6F65B9-9D23-470F-B8E3-D2F3AFF47C98; csrftoken=klMtcv9FbwmJ2O1VRrQSDYoqbiKAUpRf; mid=X4MymwAEAAHgt_F9tnHQS9uwxPV_; ig_nrcb=1'}

			data = {'email_or_username':Email,'recaptcha_challenge_field':'','flow':'','app_id':'','source_account_id':	""}
			r=s.get("https://www.instagram.com/accounts/password/reset/",headers=head)
			cookies={"csrftoken":s.cookies.get_dict().get('csrftoken'),"ig_cb":"1","ig_did":"7C6F65B9-9D23-470F-B8E3-D2F3AFF47C98",
"ig_nrcb":"1",'mid':"X4MymwAEAAHgt_F9tnHQS9uwxPV_"
}
			head["csrftoken"]=s.cookies.get_dict().get('csrftoken')
			r=s.post("https://www.instagram.com/accounts/account_recovery_send_ajax/",headers=head,data=data,cookies=cookies)
			return r.ok
			pass
		except:
			return 'Error'
			pass


	
	def Account(Email):
		try:
			api_key = "1f4b397c-f68f-4c9d-89e5-7a62c05f5032"
			email_address = Email
			response = requests.get(
    "https://isitarealemail.com/api/email/validate",params = {'email': email_address},headers = {'Authorization': "Bearer " + api_key })

			status = response.json()['status']
			if status == "valid":
				return True
				pass
			elif status == "invalid":
				return False
				pass
			else:
				return 'Band'
				pass
		except:
			return 'Error'
			pass