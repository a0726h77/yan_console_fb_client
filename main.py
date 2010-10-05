# coding:utf-8

#
# A comand line fasebook publisher
#

# Your Configuration
email = ''
passwd = ''

# My Configuration
API_KEY = '11e517548871c8813a8923b40009a060'
SECRET = 'c322efb76ecbdb2eca2b61a1719cc8e4'
session_code = ''

import urllib
import urllib2
import time
import sys
import re
import facebook

class myFBAuth():
    def __init__(self):
        # build opener with HTTPCookieProcessor
        self.opener = urllib2.build_opener( urllib2.HTTPCookieProcessor() )
        urllib2.install_opener( self.opener )

        print 'Login...'
	self.form_id = self.login(email, passwd)

    def login(self, email, passwd):
        login_url = 'https://login.facebook.com/login.php?m=m&refsrc=http://m.facebook.com/index.php&fbb=rd88e1687&refid=8'
        loginRequest = urllib2.Request ( login_url , 'email=%s&pass=%s&login=Login' % (email, passwd))
        urllib2.urlopen (loginRequest)                                                 
        connection = urllib2.urlopen ('http://m.facebook.com/')                        
        form_id = re.findall ('name="post_form_id" value="(\w+)"', connection.read ())[0]

        print 'Get form id : %s' % form_id

        return form_id 

    def get_session_code(self):
        print 'Get session code : ',

        p = urllib.urlencode( {'fb_dtsg':'v-rAp','generate': '1','v' : '1.0','api_key':API_KEY,'post_form_id':self.form_id} )
        request = urllib2.Request('http://m.facebook.com/code_gen.php/code_gen.php?api_key=%s&fbb=r97f53b86&' % API_KEY, p)
        connection = urllib2.urlopen (request)
        session_code = re.findall ('你的單次有效的驗證碼是： <b>(\w+)</b>', connection.read ())[0]

	print session_code

        return session_code

def main():
    auth = myFBAuth()
    session_code = auth.get_session_code()
    
    fb = facebook.Facebook(API_KEY, SECRET, session_code)
    session = fb.auth.getSession ()

    uid = fb.users.getInfo ([fb.uid])[0]['uid']
    print 'Get Uid : %s' % uid 

    info = fb.users.getInfo([fb.uid], ['name'])[0]
    print 'Your Name :', info['name'][1:]

    if len(sys.argv) > 1:
        print 'Update status : %s' % " ".join(sys.argv[1:])
	# 張貼到此用戶的塗鴉牆
	try:
            fb.status.set(status=" ".join(sys.argv[1:]), uid=uid)
        except:
            print 'Oops!! Maybe I don\'t have permission to do \'status_update\'.'
	    print 'To gain extended permission to this progam, please auth bellow.'
            print 'http://www.facebook.com/authorize.php?api_key=%s&v=1.0&ext_perm=status_update' % API_KEY

    #fb.users.setStatus(status='test...', clear=False, status_includes_verb=True, uid=uid)
    #fb.stream.publish("test...",None,None,uid,uid)

    print '\n\n'

if __name__ == "__main__":
    main()

