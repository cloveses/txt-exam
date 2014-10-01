import tornado.ioloop
import tornado.httpserver
import tornado.web
import tornado.escape
import os
from tmodel import Stu,Test,TestInfo

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('html/index.html')
    def post(self):
        para_keys=('name','ps')
        para_dict={}
        for key in para_keys:
            para_dict.update({key:self.get_argument(key,default='')})
        if all(para_dict.values()):
            stu=Stu.objects(name=para_dict['name']).first()
            if stu and stu.ps==para_dict['ps']:
                t_i = TestInfo.objects(sid=stu.sid).first()
                if (t_i and t_i.test_status != 'started') or not t_i:
                    self.set_cookie('name',tornado.escape.url_escape(para_dict['name']))
                    self.set_cookie('sid',str(stu.sid))
                    self.redirect('/test')
                else:
                    self.write('你已经参加完考试，请不要重新登录！')
            else:
                self.render('html/index.html')
        else:
            self.render('html/index.html')
        
class SignUpHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('html/signup.html')
    def post(self):
        para_keys=('name','ps','psbak')
        para_dict={}
        for key in para_keys:
            para_dict.update({key:self.get_argument(key,default='')})
        if all(para_dict.values()):
            if para_dict['ps']==para_dict['psbak']:
                Stu(name=para_dict['name'],ps=para_dict['ps']).save()
                self.redirect('/')
            else:
                self.write('密码不匹配')
                self.redirect('/signup')
        else:
            self.write('参数不全')
            self.redirect('/signup')

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        if self.get_cookie('name'):
            self.render('html/test.html',name=tornado.escape.url_unescape(self.get_cookie('name')))
        else:
            self.redirect('/')

class GetTestHandler(tornado.web.RequestHandler):
    def get(self,test_type,tno=1):
        if self.get_cookie('sid'):
            aTest=Test.objects(test_type=int(test_type),tno=int(tno)).first()
            htmlstr=''
            if aTest:
                htmlstr=self.get_html_str(test_type,aTest)
            para_keys=('kt_type','kt_tid','key')
            para_dict={}
            for key in para_keys:
                para_dict.update({key:self.get_argument(key,default='')})
            #print('...................',para_dict['key'])
            if all(para_dict.values()):
                sid=int(self.get_cookie('sid'))
                self.save_key(sid,int(para_dict['kt_type']),int(para_dict['kt_tid']),para_dict['key'])
            #print(htmlstr)
            self.write(htmlstr)
        else:
            self.write('你还没有登录！')

    def save_key(self,sid,test_type,tid,key):
        #print('save stu key........')
        TestInfo().update_key(sid,test_type,tid,key)

    def get_html_str(self,test_type,aTest):
        from testnum import testnum
        if int(test_type)==1:
            html_str_lst=[
                r'<input name="test_num" type="hidden" value="',str(testnum[0]),r'" />',
                r'<input name="test_tid" type="hidden" value="',str(aTest.tid),r'" />',
                r'<input name="test_type" type="hidden" value="1" />',
                r'<input name="test_no" type="hidden" value="',str(aTest.tno),r'" />',
                '<p>',str(aTest.tno),aTest.test_content,'</p>']
            if aTest.image_url:
                html_str_lst+=[r'<img src="/static/'+aTest.image_url+r'"/>']
            html_str_lst+=[
                '<p>',
                 r'<input type="radio" name="key_input" value="A" />',aTest.item_a,
                 '</p>',
                 '<p>',
                 r'<input type="radio" name="key_input" value="B" />',aTest.item_b,
                 '</p>',
                 '<p>',
                 r'<input type="radio" name="key_input" value="C" />',aTest.item_c,
                 '</p>',
                 '<p>',
                 r'<input type="radio" name="key_input" value="D" />',aTest.item_d,
                 '</p>']
            return ' '.join(html_str_lst)
        elif int(test_type)==2:
            html_str_lst=[
                r'<input name="test_num" type="hidden" value="',str(testnum[1]),r'" />',
                r'<input name="test_tid" type="hidden" value="',str(aTest.tid),r'" />',
                r'<input name="test_type" type="hidden" value="2" />',
                r'<input name="test_no" type="hidden" value="',str(aTest.tno),r'" />',
                '<p>',str(aTest.tno),aTest.test_content,'</p>']
            if aTest.image_url:
                html_str_lst+=[r'<img src="/static/'+aTest.image_url+r'"/>']
            html_str_lst+=[
                 '<p>'
                 r'<input type="text" name="key_input" value="" />'
                 '</p>']
            return ' '.join(html_str_lst)
        elif int(test_type)==3:
            html_str_lst=[
                r'<input name="test_num" type="hidden" value="',str(testnum[2]),r'" />',
                r'<input name="test_tid" type="hidden" value="',str(aTest.tid),r'" />',
                r'<input name="test_type" type="hidden" value="3" />',
                r'<input name="test_no" type="hidden" value="',str(aTest.tno),r'" />',
                '<p>',str(aTest.tno),aTest.test_content,'</p>']
            if aTest.image_url:
                html_str_lst+=[r'<img src="/static/'+aTest.image_url+r'"/>']
            html_str_lst+=[
                 '<p>',
                 r'<input type="radio" name="key_input" value="Y" />','对',
                 '</p>',
                 '<p>',
                 r'<input type="radio" name="key_input" value="N" />','错',
                 '</p>']
            return ' '.join(html_str_lst)
        
class SubmitHandler(tornado.web.RequestHandler):
    def get(self):
        sid=int(self.get_cookie('sid'))
        #print(',,,,,,,,,,,,,,,,,',sid)
        aTestInfo=TestInfo.objects(sid=sid).first()
        score=0
        if aTestInfo:
            keys=aTestInfo.key_s
            for item in keys:
                tt=Test.objects(test_type=item.test_type,tid=item.tid).first()
                rkey=tt.key
                if self.is_right(rkey,item.key):
                    score +=2
                else:
                    tt.errors += 1
                    tt.save()
            stu=Stu.objects(sid=sid).first()
            stu.score=score
            stu.save()
        self.set_cookie('name','')
        self.clear_all_cookies()
        self.write('考试结束，请离开考场！')

    def is_right(self,rkey,skey):
        for item in rkey.split(','):
            if item==skey:
                return True
        return False

class adminHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('html/get_score_test.html')

    def post(self):
        ps=self.get_argument('ps',default='')
        self.set_cookie('ps',ps)
        if ps==passwd:
            self.render('html/adminselect.html')

class GetScoreHandler(tornado.web.RequestHandler):
    def get(self):
        if self.get_cookie('ps') and passwd==self.get_cookie('ps'):
            stus = Stu.objects()
            self.render('html/getscore.html',stus=stus)

class GetAllTestHandler(tornado.web.RequestHandler):
    def get(self):
        if self.get_cookie('ps') and passwd==self.get_cookie('ps'):
            tests = Test.objects(test_type=1).order_by('tno')
            testf = Test.objects(test_type=2).order_by('tno')
            testy = Test.objects(test_type=3).order_by('tno')
            self.render('html/getalltest.html',tests=tests,testf=testf,testy=testy)

class ClearTestHandler(tornado.web.RequestHandler):
    def get(self):
        if self.get_cookie('ps') and passwd==self.get_cookie('ps'):
            print("正在清理考试数据......")
            Test.objects().delete()
            TestInfo.objects().delete()
            for stu in Stu.objects():
                stu.score=0
                stu.save()
            print("清理完毕......")
            print("正在装入考试数据......")
            Test().read_file()
            print("装入完毕，请启动服务器")
            self.redirect('/admin')

def get_ps(filename='ps.txt'):
    if os.path.exists(filename):
        with open(filename) as f:
            ps=f.readline().strip('\n')
    else:
        ps='kaoshi'
    return ps
passwd=get_ps()

settings={'static_path':os.path.join(os.path.dirname(__file__),'static'),
            # 'debug':True
            }        

application=tornado.web.Application([
    (r'/',MainHandler),
    (r'/signup',SignUpHandler),
    (r'/test',TestHandler),
    (r'/gettest/([0-9]+)/([0-9]+)',GetTestHandler),
    (r'/submit',SubmitHandler),
    (r'/getscore',GetScoreHandler),
    (r'/getalltest',GetAllTestHandler),
    (r'/cleartest',ClearTestHandler),
    (r'/admin',adminHandler)
    ],**settings)

if __name__=='__main__':
    application.listen(8888) #,'192.168.3.123')
    tornado.ioloop.IOLoop.instance().start()
    # http_server = tornado.httpserver.HTTPServer(application)
    # http_server.listen(8888)
    # io_loop = tornado.ioloop.IOLoop.instance()
    # io_loop.start()
