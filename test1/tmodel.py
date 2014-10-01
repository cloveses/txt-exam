import os
from mongoengine import *

connect('test')

class Stu(Document):
    sid = SequenceField()
    name = StringField()
    ps = StringField()
    score = IntField()

class skey(EmbeddedDocument):
    tid=IntField()
    test_type=IntField()
    key=StringField()

class TestInfo(Document):
    sid=IntField()
    test_status=StringField()
    key_s=ListField(EmbeddedDocumentField(skey))

    def update_key(self,sid,test_type,tid,key):
        t_i = TestInfo.objects(sid=sid).first()
        if t_i:
            index = self.exists(t_i,test_type,tid)
            if index:
                t_i.key_s[index-1].key=key
                t_i.save()
            else:
                akey = skey(tid=tid,test_type=test_type,key=key)
                t_i.key_s.append(akey)
                t_i.save()
                
        else:
            akey = skey(tid=tid,test_type=test_type,key=key)
            TestInfo(sid=sid,test_status='started',key_s=[akey]).save()

    def exists(self,t_i,test_type,tid):
        all_tested=[(item.test_type,item.tid) for item in t_i.key_s]
        if (test_type,tid) in all_tested:
            return all_tested.index((test_type,tid))+1
        else:
            return 0

class Test(DynamicDocument):
    tid=SequenceField()
    tno=IntField()
    test_type=IntField()
    test_content=StringField()
    key=StringField()
    image_url=StringField(default='')
    errors = IntField(default=0)
    

    def read_file(self,filename='mytest.txt'):
        filename=os.sep.join([os.getcwd(),'testsrc',filename])
        if os.path.exists(filename):
            f=open(filename,'r')
            all_test=[]
            for line in f:
                all_test.append(line.strip('\n').split(' '))
            #print(all_test)
            type_count={'1':1,'2':1,'3':1}
            for item in all_test:
                self.add_test(item,type_count)
                type_count[str(item[0])] +=1
            f.close()
            f=open('testnum.py','w',encoding='utf-8')
            f.write('testnum=('+ str(type_count['1']-1)+','+ str(type_count['2']-1)+','+ str(type_count['3']-1) +')')
            f.close()
        else:
            print('test file is not exists')

    def add_test(self,item,type_count):
        if item[0]=='1' and 7<=len(item)<=8:
            imageurl=item[7] if len(item)==8 else ''
            Test(test_type=int(item[0]),test_content=item[1],key=item[6],
                 item_a=item[2],item_b=item[3],item_c=item[4],item_d=item[5],image_url=imageurl,
                 tno=type_count[item[0]]).save()
        elif item[0]=='2'  and 3<=len(item)<=4:
            imageurl=item[3] if len(item)==4 else ''
            Test(test_type=int(item[0]),test_content=item[1],key=item[2],image_url=imageurl,
                 tno=type_count[item[0]]).save()
        elif item[0]=='3'  and 3<=len(item)<=4:
            imageurl=item[3] if len(item)==4 else ''
            Test(test_type=int(item[0]),test_content=item[1],key=item[2],image_url=imageurl,
                 tno=type_count[item[0]]).save()
        else:
            print('a error in:',item)
            # raise NameError('HiThere')


