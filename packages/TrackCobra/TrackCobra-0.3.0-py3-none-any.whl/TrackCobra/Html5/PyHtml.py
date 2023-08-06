
"""


all  ©copyrights save by TrackCobra
the programmer MrGps
library: PyHtml5
the library using for [ Development ] website/s and you can used if you haven't internet

Programe language used: html, css, python
library used: os, webbrowser, requests,

to know the library codes

type code help()

progrmmer channels:
	
youtube : Mr GPS
telegram: @MrGps0

to communicate | telegram : MrGps1



"""


"""

Youtube or telegram 

y.t / Mr GPS

t.me / @MrGps0


for details of the library and its explanations


"""


def help():
	codes="""codes of library /help
	
telegram /// MrGps0
	
_______________________________________________________________

h1, h2, h3, h4, h5, h6 --> have(text,style,name,id,__class__)
_______________________________________________________________

img(src,text,id,style,name',alt,__class__)

a(text,target,id,name,href,style,__class__)
_______________________________________________________________

input(name,id,text,style,placeholder,__class__)

button(name,id,text,style,__class__)

textarea(name,id,style,text,placeholder,__class__)

br() --> used for spacing
_______________________________________________________________

line, DTH, html_start/end, head_start/end, body_start/end --> just add

line(count)
_______________________________________________________________

title(text)

style(id,__class__,styles)
_______________________________________________________________

html_add(code) --> Add codes to written codes

html_free(code) --> Write all the codes on without any additions

get_source_code_form(url) --> get source code form by url
_______________________________________________________________

PyHtml5 run?



PyHtml5.run(port) without port or with



e.g


PyHtml5.run(port=8888)

or

PyHtml5.run()


and you can open auto using

PyHtml.run(auto_open=True)

_______________________________________________________________
	"""
	print(codes)






import os
import webbrowser
import requests



file1 = open("TrackCobra.html",'w')
file1.write('')

def run(port='',auto_open=''):
	if port== '':
		print('\033[1;31mHosted By \033[1;32mTrackCobra\033[0;37m ')
		print('[port] http://127.0.0.1:8000/TrackCobra.html')
		if auto_open == True:
			webbrowser.open('http://127.0.0.1:8000/TrackCobra.html')
		os.system('python3 -m http.server 8000')
		
	else:
		print('\033[1;31mHosted By \033[1;32mTrackCobra\033[0;37m ')
		print(f'[port] http://127.0.0.1:{port}/TrackCobra.html')
		if auto_open == True:
			webbrowser.open(f'http://127.0.0.1:{port}/TrackCobra.html')
		os.system(f'python3 -m http.server {port}')
		
		
		
		
	
		
		
	
		
		
	
		
	
	
	
def DTH():
	file = open('TrackCobra.html','a')
	file.write('<!DOCTYPE Html>')
	file.close()
	
	
	
	
	
def html_start():
	file = open('TrackCobra.html','a')
	file.write('<html>')
	file.close()
	
def html_end():
	file = open('TrackCobra.html','a')
	file.write('</html>')
	file.close()




	
def head_start():
	file = open('TrackCobra.html','a')
	file.write('<head>')
	file.close()
	
def head_end():
	file = open('TrackCobra.html','a')
	file.write('</head>')
	file.close()
	
	
	
	
def title(text):
	file = open('TrackCobra.html','a')
	file.write('<title>{text}</title>')
	file.close()
	
	
	
def style(__class__='',id='',styles=''):
	file = open('TrackCobra.html','a')
	file.write('<style>')
	file.close()
	if __class__ == '':
		name=''
	else:
		file = open('TrackCobra.html','a')
		file.write(f'.{__class__}'+'{'+styles+'}')
		file.close()
			
	if id == '':
		name=''
	else:
		file = open('TrackCobra.html','a')
		file.write(f'#{id}'+'{'+styles+'}')
		file.close()
		
	file = open('TrackCobra.html','a')
	file.write(f'</style>')
	file.close()
	
	
	
	
def body_start():
	file = open('TrackCobra.html','a')
	file.write('<body>')
	file.close()
	
def body_end():
	file = open('TrackCobra.html','a')
	file.write('</body>')
	file.close()
	
	
	
	
def html_free(code):
	file = open('TrackCobra.html','w')
	file.write(f"""{code}""")
	file.close()
	
def html_add(code):
	file = open('TrackCobra.html','a')
	file.write(f"""{code}""")
	file.close()

	
	
	
	
	
	
	
	
	
	
	
	
def br():
	file = open('TrackCobra.html','a')
	file.write('<br></br>')
	file.close()
	
	
	
def line(count=0):
	file = open('TrackCobra.html','a')
	file.write('\n'*count)
	file.close()
		
		
	
	
	
def button(name='',id='',text='',style='',__class__=''):
	file = open('TrackCobra.html','a')
	file.write('<button ')
	file.close()
	if name == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'name="{name}" ')
		file.close()
		
	if id == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'id="{id}" ')
		file.close()
		
	if __class__ == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'class="{__class__}" ')
		file.close()
		
		
	if style == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'style="{style}" ')
		file.close()
		
	if text == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'>{text}')
		file.close()
		
	file = open('TrackCobra.html','a')
	file.write('</button>')
	file.close()








def input(name='',id='',text='',style='',placeholder='',__class__=''):
	file = open('TrackCobra.html','a')
	file.write('<input ')
	file.close()
	if name == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'name="{name}" ')
		file.close()
		
	if id == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'id="{id}" ')
		file.close()
		
	if __class__ == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'class="{__class__}" ')
		file.close()
		
	if style == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'style="{style}" ')
		file.close()
		
	if placeholder == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'placeholder="{placeholder}"')
		file.close()
		
	if text == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'>{text}')
		file.close()
		
	file = open('TrackCobra.html','a')
	file.write('</input>')
	file.close()
	
	
	
	
	
	
	
def textarea(name='',id='',style='',text='',placeholder='',__class__=''):
	file = open('TrackCobra.html','a')
	file.write('<textarea ')
	file.close()
	if name == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'name="{name}" ')
		file.close()
		
	if id == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'id="{id}" ')
		file.close()
		
	if __class__ == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'class="{__class__}" ')
		file.close()
		
	if style == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'style="{style}" ')
		file.close()
		
	if placeholder == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'placeholder="{placeholder}"')
		file.close()
		
	if text == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'>{text}')
		file.close()
		
	file = open('TrackCobra.html','a')
	file.write('</textarea>')
	file.close()
	






def a(text='',target='',id='',name='',href='',style='',__class__=''):
	file = open('TrackCobra.html','a')
	file.write('<a ')
	file.close()
	if name == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'name="{name}" ')
		file.close()
		
	if target == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'target="{target}" ')
		file.close()
		
	if id == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'id="{id}" ')
		file.close()
		
	if __class__ == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'class="{__class__}" ')
		file.close()
		
	if href == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'href="{href}" ')
		file.close()
		
	if style == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'style="{style}" ')
		file.close()
		
	if text == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'>{text}')
		file.close()
		
	file = open('TrackCobra.html','a')
	file.write('</a>')
	file.close()
	
	
	



def img(src='',text='',id='',style='',name='',alt='',__class__=''):
	file = open('TrackCobra.html','a')
	file.write('<img ')
	file.close()
	if name == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'name="{name}" ')
		file.close()
		
	if src == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'src="{src}" ')
		file.close()
		
	if id == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'id="{id}" ')
		file.close()
		
	if __class__ == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'class="{__class__}" ')
		file.close()
		
	if alt == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'alt="{alt}" ')
		file.close()
		
	if style == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'style="{style}" ')
		file.close()
		
	if text == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'>{text}')
		file.close()
		
	file = open('TrackCobra.html','a')
	file.write('>')
	file.close()
	




	
def h1(name='',id='',text='',style='',__class__=''):
	file = open('TrackCobra.html','a')
	file.write('<h1 ')
	file.close()
	if name == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'name="{name}" ')
		file.close()
		
		
	if id == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'id="{id}" ')
		file.close()
		
	if __class__ == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'class="{__class__}" ')
		file.close()

		
	if style == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'style="{style}" ')
		file.close()
		
	if text == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'>{text}')
		file.close()
		
	file = open('TrackCobra.html','a')
	file.write('</h1>')
	file.close()
	
	
	
	
	
	
	
def h2(name='',id='',text='',style='',__class__=''):
	file = open('TrackCobra.html','a')
	file.write('<h1 ')
	file.close()
	if name == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'name="{name}" ')
		file.close()
		
		
	if id == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'id="{id}" ')
		file.close()
		
	if __class__ == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'class="{__class__}" ')
		file.close()

		
	if style == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'style="{style}" ')
		file.close()
		
	if text == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'>{text}')
		file.close()
		
	file = open('TrackCobra.html','a')
	file.write('</h1>')
	file.close()
	
	
	
	
	
	
def h3(name='',id='',text='',style='',__class__=''):
	file = open('TrackCobra.html','a')
	file.write('<h1 ')
	file.close()
	if name == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'name="{name}" ')
		file.close()
		
		
	if id == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'id="{id}" ')
		file.close()
		
	if __class__ == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'class="{__class__}" ')
		file.close()

		
	if style == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'style="{style}" ')
		file.close()
		
	if text == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'>{text}')
		file.close()
		
	file = open('TrackCobra.html','a')
	file.write('</h1>')
	file.close()
	
	
	
	
	
	
def h4(name='',id='',text='',style='',__class__=''):
	file = open('TrackCobra.html','a')
	file.write('<h1 ')
	file.close()
	if name == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'name="{name}" ')
		file.close()
		
		
	if id == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'id="{id}" ')
		file.close()
		
	if __class__ == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'class="{__class__}" ')
		file.close()

		
	if style == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'style="{style}" ')
		file.close()
		
	if text == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'>{text}')
		file.close()
		
	file = open('TrackCobra.html','a')
	file.write('</h1>')
	file.close()
	
	
	
	
	
	
def h5(name='',id='',text='',style='',__class__=''):
	file = open('TrackCobra.html','a')
	file.write('<h1 ')
	file.close()
	if name == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'name="{name}" ')
		file.close()
		
		
	if id == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'id="{id}" ')
		file.close()
		
	if __class__ == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'class="{__class__}" ')
		file.close()

		
	if style == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'style="{style}" ')
		file.close()
		
	if text == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'>{text}')
		file.close()
		
	file = open('TrackCobra.html','a')
	file.write('</h1>')
	file.close()
	
	
	
	
	
	
def h6(name='',id='',text='',style='',__class__=''):
	file = open('TrackCobra.html','a')
	file.write('<h1 ')
	file.close()
	if name == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'name="{name}" ')
		file.close()
		
		
	if id == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'id="{id}" ')
		file.close()
		
	if __class__ == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'class="{__class__}" ')
		file.close()

		
	if style == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'style="{style}" ')
		file.close()
		
	if text == '':
		none=None
	else:
		file = open('TrackCobra.html','a')
		file.write(f'>{text}')
		file.close()
		
	file = open('TrackCobra.html','a')
	file.write('</h1>')
	file.close()
	
	
	
	
	
	
	
def get_source_code_form(url=''):
		
	if 'http' in url:
		code = requests.get(url).text
		file = open('TrackCobra.html','w')
		file.write(str(code))
		file.close()
	else:
		print('http/https !!?') 
	
	
