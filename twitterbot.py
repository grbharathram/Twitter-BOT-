import twitter
import re
import pickle
import sys
import urllib
import httplib2
import random,os

#using regex for phone number and email validation
phone=re.compile('\d{10}$')
email=re.compile('[a-zA-Z0-9+_\-\.\ ]*[ ]*<?[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z][.-0-9a-zA-Z]*.[a-zA-Z]+>?')

#-------------------Reading the Horroscope File-------------------------#
def horroscope():
	filename="horroscope"
	file = open(filename,'r')

	#Get the total file size
	file_size = os.stat(filename)[6]

#this part is used to seek a random line from the horroscope file
	while 1:
	      #Seek to a place in the file which is a random distance away
	      #Mod by file size so that it wraps around to the beginning
	      file.seek((file.tell()+random.randint(0,file_size-1))%file_size)
	
	      #dont use the first readline since it may fall in the middle of a line
	      file.readline()
	      #this will return the next (complete) line from the file
	      line = file.readline()
	
	      #here is your random line in the file
	      print line
	      return str(line)
	
#------------------sms function---------------------------------------------#

# Here I am using the Unofficial Way2sms api - the website offers you unlimited free sms once you registered
# Original API by Abhishek Anand, June 12, 2010, abhishek@bitproxy.co.cc, http://proxyspeaks.blogspot.com
# Updated by Master Yoda

def sms(username,password,mobileNo, message):
    #Check validity of MobileNumber and length of message ( should be less than 160)
    if len(mobileNo) <> 10 or len(message) > 140:
        return False
    # These are some of the CNAMES or roughly servers you are directed
    #  (to balance load i guess)
    serverList = ['site1','site2','site3','site4','site5','site6']
    # Get a random server from list
    server = serverList[random.randint(0,len(serverList)-1)]
    # Make a authentication request and get the cookie
    http = httplib2.Http()
    url = 'http://' + server + '.way2sms.com:80/auth.cl'
    body = {'username': username, 'password': password,'login': 'Login'}
    headers = {'Content-type': 'application/x-www-form-urlencoded',
               'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)'}
    try:
        response, content = http.request(url,
                                     'POST',
                                     headers=headers,
                                     body=urllib.urlencode(body))
    except:
        print("Authenticaiton post failed")
        return False
    # Set the cookie we got for future requests
    try:
   	 headers = {'Content-type': 'application/x-www-form-urlencoded',
               'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
                                                   'Cookie':response['set-cookie']}
    except:
 	 print "cookie error"
    newBody = {'custid': 'undefined',
               'HiddenAction': 'instantsms',
               'Action':'sa65sdf656fdfd',
               'login': '',
               'pass': '',
               'MobNo': mobileNo,
               'textArea': message}
    newurl = "http://"+ server +".way2sms.com/FirstServletsms?custid="
    # Send message with the cookie we got
    try:
        response, content = http.request(newurl,
                                     'POST',
                                     headers=headers,
                                     body=urllib.urlencode(newBody))
    except:
        print("sms sending failed")
        return False
    # If the returned text contains word successfully, your message is sent
    if content.find("successfully") <> -1:
        print("sent")
        return True
    else:
        print("Failed")
        return False

#------------------------Beginning of the program-------------------------------------#


def read_file(word):
	print word
	file = open("DictionaryForBot","r")
	line=file.readline()
	
	while(line):
		if line.split()[0]==word:
			reply_str=line
			break
		else:
			line=file.readline()
		if not line:
			reply_str="sorry! My creators @grbharathram and @yeskarthik forgot to load "+word+" into my brain :( please contact him"
	file.close()
	return str(reply_str)	


api=twitter.Api()
flag=0
#lastid=None
api = twitter.Api(consumer_key,consumer_secret,access_token_key,access_token_secret)

ipfile=open('lastid.pkl','rb')
if ipfile != None:
	lastid=long(pickle.load(ipfile))
	print lastid
ipfile.close()
opfile=open('lastid.pkl','wb')

recentMentions=api.GetMentions(since_id=lastid)

for status in recentMentions:
	if len(status.text.split())==2:
		word=status.text.split()[1]
		if len(word)<>10:
			reply='@'+status.user.screen_name+' Please enter a proper 10-digit phone number your highness'
		else:
			reply_name=status.user.screen_name	
			#reply=read_file(word)
			reply=horroscope()
			sms("9952955920","abcxyz007",word,reply)
		
			print reply_name
			print status.text
			print reply
			flag=1
			pickle.dump(status.id,opfile) 
			final=api.PostUpdate('@'+reply_name+' '+reply)
	else:
		reply="Please Enter your phone number alone , your highness!"
		flag=1
		reply_name=status.user.screen_name
		print reply_name
		pickle.dump(status.id,opfile) 
		final=api.PostUpdate('@'+reply_name+' '+reply)
		
if flag==0:
	pickle.dump(lastid,opfile)
opfile.close()

