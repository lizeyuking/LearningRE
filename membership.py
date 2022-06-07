#coding:utf-8

def bracket_shuffle(re1):
    if re1[0] == "(" and re1[-1] == ")":
        pass
    elif re1[0] == "(" and re1[-2] == ")":
        pass
    elif "," in re1 or "|" in re1:
        re1 = "(" + re1 + ")"
    else:
        pass
    return re1

def re_link(re1,re2):
    if re1=="#" or re2=="#":
        return "#"
    elif re1=="~":
        return re2
    elif re2=="~":
        return re1
    elif re1==re2 and re1[-1]=='*':
        return re1
    else:
        # if re1[0] == "(" and re1[-1] == ")":
        #     pass
        # elif "&" in re1 or "|" in re1:
        #     re1="("+re1+")"
        # else:
        #     pass
        return re1+","+re2

def re_shuffle(re1,re2):
    if re1=="#" or re2=="#":
        return "#"
    elif re1=="~":
        return re2
    elif re2=="~":
        return re1
    elif re1==re2 and re1[-1]=='*':
        return re1
    else:
        # re1=bracket_shuffle(re1)
        # re2=bracket_shuffle(re2)
        return "("+re1+"&"+re2+")"

def re_or(re1,re2):
    if re1==re2:
        return re1
    elif re1==re2[0:-1] and re2[-1]=='*':
        return re2
    elif re1==re2[0:-1] and re2[-1]=='*':
        return re2
    # elif re1[-1]==']' and re2[-1]==']':
    #     index1=re1.rindex('[')
    #     index2=re2.rindex('[')
    #     if re1[0:index1]==re2[0:index2]:
    #         c1=re1[index1+1:-1].split(',')
    #         c2=re2[index1+1:-1].split(',')
    #         cm=min(int(c1[0]),int(c2[0]))
    #         cn=min(int(c1[1]),int(c2[1]))
    #         return re1[0,index1]+"["+str(cm)+','+s
    else:
        if re1=="#":
            return re2
        elif re2=="#":
            return re1
        else:
            return re1+"|"+re2


class Re_de_nu(object):

    def __init__(self):
        self.re=""
        self.deriva=""
        self.renull=True
        self.denull=False

    def add_element(self,re,a):
        self.re=re
        if self.re=="#" or self.re=="~":
            self.deriva="#"
            self.denull=False
        elif self.re==a:
            self.deriva="~"
            self.denull=True
        else:
            self.deriva="#"
            self.denull = False
        if self.re=="~":
            self.renull=True
        else:
            self.renull=False
        return self

    def closure_operate(self): # * 闭包
        if self.re=="#" or self.re=="~":
            self.deriva="#"
            self.denull=False
            if self.re=="#":
                self.renull=False
            else:
                self.renull=True
        else:
            self.re = self.re+"*"
            if self.deriva == "#":
                self.denull = False
            elif self.deriva=="~":
                self.deriva=self.re
                self.denull = True
            else:
                self.deriva =self.deriva+","+self.re
            self.renull = True
        return  self

    def plus_operate(self): # +至少一次闭包
        if self.re == "#" or self.re == "~":
            self.deriva = "#"
            self.denull = False
            if self.re == "#":
                self.renull = False
            else:
                self.renull = True
        else:
            if self.deriva == "#":
                self.denull = False
            elif self.deriva == "~":
                self.deriva=self.re+"*"
                self.denull = True
            else:
                self.deriva = self.deriva + "," + self.re+"*"
            self.re = self.re + "," + self.re + "*"
        return self

    def counting_operate(self,couting):  # +至少一次闭包
        s = couting[1:-1]
        s = s.split(",")
        m = int(s[0])
        n = int(s[1])
        if m<0 or n<0:
            self.re="#"
            self.deriva="#"
            self.renull=False
            self.denull=False
        elif m==0 and n==0:
            self.deriva = "#"
            self.denull = False
            self.re="~"
            self.renull=True
        elif self.re == "#" or self.re == "~":
            self.deriva = "#"
            self.denull=False
            if self.re == "#":
                self.renull = False
            else:
                self.renull = True
        else:
            if m>n:
                self.re="#"
                self.deriva="#"
                self.renull=False
                self.denull=False
            else:
               # self.re = self.re +couting
                if m>=1:
                    if m-1==0:
                        if self.deriva!="#" and self.re!="#":
                            self.denull=True
                        else:
                            self.denull=False
                    else:
                        self.denull=self.denull&self.renull
                    self.deriva = re_link(self.deriva, self.re + "[" + str(m - 1) + "," + str(n - 1) + "]")
                else:
                    if self.deriva!="#":
                        self.denull=True
                    else:
                        self.denull=False
                    self.deriva = re_link(self.deriva,self.re+"["+str(0)+","+str(n-1)+"]")
            self.re=self.re+couting
            if self.renull==True:
                pass
            elif m==0:
                self.renull=True
            else:
                self.renull=False
        return self

    def question_operate (self):  # ?操作
        if self.re!="#":
            self.renull=True
        else:
            self.renull=False

        if self.re == "#" or self.re=="~":
            pass
        else:
            self.re= "("+self.re + "|" + "~"+")"
        # if self.denull!="#" and self.deriva!="~":
        #     self.denull=True
        # else:
        #     self.denull=False
        return self

    def a_or_b (self,re_de_nu_item):  # a|b 操作
        if self.renull==False and re_de_nu_item.renull==False:
            self.renull = False
        else:
            self.renull=True
        if self.denull==True or re_de_nu_item.denull==True:
            self.denull=True
        else:
            self.denull=False
        self.re = re_or(self.re, re_de_nu_item.re)
        self.deriva = re_or(self.deriva, re_de_nu_item.deriva)
        return self

    def a_link_b (self,re_de_nu_item):  # a,b 操作
        self.re=re_link(self.re,re_de_nu_item.re)
        if self.renull==True:
            self.deriva=re_or(re_link(self.deriva,re_de_nu_item.re),re_de_nu_item.deriva)
            if self.denull==True and re_de_nu_item.renull==True:
                self.denull=True
            elif re_de_nu_item.denull==True:
                self.denull=True
            else:
                self.denull=False
        else:
            self.deriva=re_link(self.deriva,re_de_nu_item.re)
            if self.denull==True and re_de_nu_item.renull==True:
                self.denull=True
            else:
                self.denull=False
        if self.renull==True and re_de_nu_item.renull==True:
            self.renull=True
        else:
            self.renull=False
        return self

    def a_interleaving_b(self,re_de_nu_item):  # a|b 操作
        # print("$"*80)
        # print(self.deriva)
        # print(re_de_nu_item.re)
        # print(self.re)
        # print(re_de_nu_item.deriva)
        if self.denull==True and re_de_nu_item.renull==True:
            # print("yes1")
            # print(self.re)
            # print(self.deriva)
            self.denull=True
        elif self.renull==True and re_de_nu_item.denull==True:
            # print("yes2")
            self.denull=True
        else:
            self.denull=False
        #print(self.deriva)
        if self.renull == True and re_de_nu_item.renull == True:
            self.renull = True
        else:
            self.renull = False
        self.deriva = re_or(re_shuffle(self.deriva, re_de_nu_item.re), re_shuffle(self.re, re_de_nu_item.deriva))
        self.re = re_shuffle(self.re, re_de_nu_item.re)
        return  self

    def self_generate(self,operator):
        if operator=='?':
            return self.question_operate()
        if operator=='*':
            return self.closure_operate()
        if operator=='+':
            return self.plus_operate()
        else:
            print('self operate error')

    def calculate_2automat(self,b,operator):
        if operator==',':
            return self.a_link_b(b)
        if operator=='|':
            return self.a_or_b(b)
        if operator=='&':
            return self.a_interleaving_b(b)
        else:
            print('calculate operate error : %s' %(operator))

    def brackets(self):
        self.re="("+self.re+")"
        return self

    def print_de(self):
        print(self.deriva)
    def getde(self):
        return self.deriva
    def getdenull(self):
        return self.denull

def splice(re):
    posl,posr = marked(re)
    n = len(posl)
    num_re = re

    for i in range(n):
        tmp = re[posl[i]:posr[i] + 1]
        num_re = num_re.replace(tmp,'')

    num_re = num_re.replace('*','').replace('?','').replace('+','').replace('(','').replace(')','')
    num_re = num_re.replace(',', ' ').replace('|', ' ').replace('&', ' ')

    return num_re

def marked(re):
    posl,posr = [],[]
    n = len(re)

    for i in range(n):
        if re[i]=='[':
            posl.append(i)
        if re[i]==']':
            posr.append(i)
    pos = (posl,posr)
    return pos

def split_elem(re):
    line = re
    items = line.split('?')
    line = ' ? '.join(items)
    items = line.split('+')
    line = ' + '.join(items)
    items = line.split('*')
    line = ' * '.join(items)
    items = line.split(',')
    line = ' , '.join(items)
    items = line.split('|')
    line = ' | '.join(items)
    items = line.split('&')
    line = ' & '.join(items)
    items = line.split('(')
    line = ' ( '.join(items)
    items = line.split(')')
    line = ' ) '.join(items)
    items = line.split('[')
    line = ' [ '.join(items)
    items = line.split(']')
    line = ' ] '.join(items)
    line = line.replace('  ', ' ')
    # print line
    if len(line)>0:
        if line[0] == ' ':
            # print line
            # print line[1:]
            line = line[1:]
            # print line
        if line[-1] == ' ':
            line = line[:-1]

    posl, posr = marked(line)
    n = len(posl)
    num_re = line
    for i in range(n):
        tmp = line[posl[i]:posr[i] + 1]
        s=tmp.replace(" ","")
        num_re = num_re.replace(tmp, s)
    return num_re

    # return l


def TrimBrackets(str):
    leftF='('
    rightF=')'
    # 存放需要删除的括号位置
    priorityLevel={'[':[1, 5],']': [1, 5],'+':[1, 5],'*': [1, 5],'?': [1, 5],
                   ',': [2, 4],'&': [2, 3],'|': [2, 2],'(':[-1,-1],')':[-1,-1]}
    position=[]
    # 存放符号的栈
    stack = []
    #临时存放括号位置栈
    temp = []
    length = len(str)
    for i in range(0,length):
        # 正在处理的字符
        ch = str[i]
        if ((ch >= '0' and ch <= '9') or (ch >= 'a' and ch <= 'z') or (ch >= 'A' and ch <= 'Z')):
            continue
        if (leftF == ch):
            temp.append(i)
        if (rightF == ch):
            # 取得后面一个运算符的优先级
            if length - 1 == i:
                nextLevel=-1
            else:
                # print(str([str[i + 1]))
                # print str[i+1]
                nextLevel=priorityLevel[str[i + 1]][1]
            # 前面一个运算符优先级
            preLevel = -1
            # 取得前面对应的左括弧位置
            prePosition = temp[-1]
            # 如果前面已经没有运算符或前面运算符是一元运算符则不用判断
            if (prePosition != 0 and 1 != priorityLevel[str[prePosition - 1]][0]):
                preLevel = priorityLevel[str[prePosition - 1]][1]
            # 真则表示该括号可以被删除
            flag = True
            while (True):
                if (len(stack)!=0):
                    character = stack.pop()
                if (leftF == character):
                    break
                if (flag==True):
                    # 取得当前得优先级
                    currentLevel = priorityLevel[character][1];
                    if (currentLevel <nextLevel or currentLevel < preLevel):
                        flag = False
            # 可以删除
            if (flag==True):
                position.append(temp.pop())
                position.append(i)
            else:
                temp.pop()
            continue
        stack.append(ch)
    # 删除括号
    stringBuffer = ""
    for i in range(0,len(str)):
        if i not in position:
            stringBuffer=stringBuffer+str[i]
    return stringBuffer
def simpli_count(str):
    s=str.split('|')
    if(len(s)>=2):
        r2=s[-1]
        r1=s[-2]
        if(r1[-1]==']' and r2[-1]==']'):
            u1=r1.index('[')
            u2=r2.index('[')
            if(r1[0:u1]==r2[0:u2]):
                mn1=r1[u1+1:-1].split(',')
                m1,n1=int(mn1[0]),int(mn1[1])
                mn2 = r2[u2 + 1:-1].split(',')
                m2, n2 = int(mn2[0]), int(mn2[1])
                m=min(m1,m2)
                n=max(n1,n2)
                print(type(m),type(n))
                ss=str[0:str[0:-1].rindex(']')]
                ss=ss[0:ss.rindex('[')]
                return ss+"["+str(m)+"'"+str(n)+"]"

#(,),?,,,*,+,|的优先级，第一行表示栈顶是(，新来符号的优先级如果大于他，就为1，入栈，如果小于他，就出栈，2表示不确定
dic_2d={
        '$':{'(':1,')':1,'?':1,',':1,'|':1,'*':1,'+':1,'[':1,']':1,'&':1},
        '(':{'(':1,')':0,'?':1,',':1,'|':1,'*':1,'+':1,'[':1,']':1,'&':1},
        '[':{'(':2,')':2,'?':2,',':2,'|':2,'*':2,'+':2,'[':2,']':0,'&':2},
        ']':{'(':0,')':0,'?':0,',':0,'|':0,'*':0,'+':0,'[':2,']':2,'&':2},
        '?':{'(':2,')':0,'?':2,',':0,'|':0,'*':2,'+':2,'[':2,']':0,'&':0},
        '+':{'(':2,')':0,'?':2,',':0,'|':0,'*':2,'+':2,'[':2,']':0,'&':0},
        '*':{'(':2,')':0,'?':2,',':0,'|':0,'*':2,'+':2,'[':2,']':0,'&':0},
        ',':{'(':1,')':0,'?':1,',':0,'|':0,'*':1,'+':1,'[':1,']':2,'&':0},
        '&':{'(':1,')':0,'?':1,',':1,'|':0,'*':1,'+':1,'[':1,']':2,'&':0},
        '|':{'(':1,')':0,'?':1,',':1,'|':0,'*':1,'+':1,'[':1,']':2,'&':1}
       }

def get_deri(re,a):
    stack_operator=[]
    stack_Re_de_nu=[]
    stack_operator.append("$")
    split_re= split_elem(re).split(' ')
    for items in split_re:
        # print items
        # print "stack_operator_top" + stack_operator[-1]
        if '[' in items:
            Re_de_nu_1 = stack_Re_de_nu.pop()
            # Re_de_nu_1.print_Re_de_nu()
            stack_Re_de_nu.append(Re_de_nu_1.counting_operate(items))
        elif items not in {'?','*','+',',','|','(',')','&'}:
            tmp_Re_de_nu=Re_de_nu()
            tmp_Re_de_nu.add_element(items,a)
            stack_Re_de_nu.append(tmp_Re_de_nu)
        else:
            top_item=stack_operator[-1] #读取栈顶元素
            if dic_2d[top_item][items]==1:
                stack_operator.append(items)
                # print "stack_operator_top" + stack_operator[-1]
            else:
                if items!=')':
                    while dic_2d[top_item][items]==0 and len(stack_operator)>1:
                        operator=stack_operator.pop()
                        if operator in {'?','*','+'}:
                            Re_de_nu_1=stack_Re_de_nu.pop()
                            stack_Re_de_nu.append(Re_de_nu_1.self_generate(operator))
                            top_item=stack_operator[-1]
                        else:
                            Re_de_nu_3=stack_Re_de_nu.pop()
                            Re_de_nu_2=stack_Re_de_nu.pop()
                            stack_Re_de_nu.append(Re_de_nu_2.calculate_2automat(Re_de_nu_3,operator))
                            top_item = stack_operator[-1]
                    stack_operator.append(items)
                    if dic_2d[top_item][items]==2:
                        print("cant decide order:%s" %(re))
                        return
                else:
                    # print items
                    while top_item!='(':
                        operator = stack_operator.pop()
                        if operator in {'?', '*', '+'}:
                            Re_de_nu_1 = stack_Re_de_nu.pop()
                            stack_Re_de_nu.append(Re_de_nu_1.self_generate(operator))
                            top_item = stack_operator[-1]
                        else:
                            Re_de_nu_3 = stack_Re_de_nu.pop()
                            Re_de_nu_2 = stack_Re_de_nu.pop()
                            stack_Re_de_nu.append(Re_de_nu_2.calculate_2automat(Re_de_nu_3, operator))
                            top_item = stack_operator[-1]
                    stack_operator.pop()
                    Re_de_nu_1 = stack_Re_de_nu.pop()
                    stack_Re_de_nu.append(Re_de_nu_1.brackets())
    while len(stack_operator)>1:
        operator=stack_operator.pop()
        if operator in {'?', '*', '+'}:
            Re_de_nu_1 = stack_Re_de_nu.pop()
            stack_Re_de_nu.append(Re_de_nu_1.self_generate(operator))
        else:
            Re_de_nu_3 = stack_Re_de_nu.pop()
            Re_de_nu_2 = stack_Re_de_nu.pop()
            stack_Re_de_nu.append(Re_de_nu_2.calculate_2automat(Re_de_nu_3, operator))
    return stack_Re_de_nu.pop()



def member(re,w):#句子以空格为分隔符
    de=re
    cu_de = Re_de_nu()
    if ',' in w:
        s=w.split(",")
    else:
        s=w.split(" ")
    for item in s:
        cu_de=get_deri(de,item)
        de = cu_de.getde()
        # de = TrimBrackets(cu_de.getde())
        # print(de)
        # print("de is null:" + str(cu_de.denull))
        if de=="#":
            return False
    if  cu_de.getdenull()==True:
        return True
    else:
        return False

def runmember():
    if __name__ == "__main__":
        pos = set()
        re = "a,b|c&((d))+"
        w = "c,c,b"
        print(member(re, w))




#runmember()


