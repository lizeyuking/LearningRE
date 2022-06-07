import re    #要实现的是leaning的树，叶子节点的是句子
import  random
changed = []  # 转换后的后缀字符串
opera = []  # 运算符栈

class TreeNode:   #树节点类的定义

    def __init__(self,value=0,root=None,leftchild=None,rightchild=None,treetype = -1,treecheck = 0):
        self.root=root                #父节点
        self.value=value
        self.leftchild=leftchild
        self.rightchild=rightchild
        self.treetype = treetype    #用来判断结点是什么类型的结点
        self.treecheck = treecheck  #用来判断该节点是否被遍历过

    def left(self,leftchild):
        self.leftchild=leftchild

    def right(self,rightchild):
        self.rightchild=rightchild

class binarytree:
    def __init__(self,root=None):
        self.root=root

'''
def aberration(node=None,randomdate=1): # 判断节点是否变异
    if node.treetype == 2:          #定义二目运算符的变异率
        if randomdate <= 0.01:
            return True                  #小于0.01，变异
        else:
            return False
    if node.treetype == 1:          #定义一目运算符的变异率
        if randomdate <= 0.05:
            return True                  #小于0.01，变异
        else:
            return False
    if node.treetype == 0:          #定义单词的变异率
        if randomdate <0:
            return True                  #单词先不变异
        else:
            return False
'''

def traverse(node):     #中序遍历二叉树
    #左孩子递归
    if node.leftchild!=None:
        traverse(node.leftchild)
    #根节点自身，中
    #print(node.value)  # 输出自身
    print(node.value,node.treetype,node.treecheck)    #输出自身
    #右孩子递归
    if node.rightchild!=None:
        traverse(node.rightchild)

#不同类型节点的栈
Type1 = []
Type2 = []
Type0 = []
Type4 = []

def emptyType():        #清空分类list
    Type0.clear()
    Type1.clear()
    Type2.clear()
    Type4.clear()



def classification(node):           #将表达式树中的结点按Type值进行归类
    # 左孩子递归

    if node.leftchild != None:
        classification(node.leftchild)


    # 根节点自身，中

    if node.treetype == 0:     #入栈分类
        Type0.append(node)
    elif node.treetype == 1:
        Type1.append(node)
    elif node.treetype == 2:
        Type2.append(node)
    elif node.treetype == 4:
        Type4.append(node)

    # 右孩子递归
    if node.rightchild != None:
        classification(node.rightchild)


#___________________________________________________________________________________________________________________________________________________________

def isOper(ch):
    if ch in ['+', '|', '*', '&', '.', '(', ')', '?']:            #第一部分——转后缀部分
        return True
    return False
    # 获取运算符所对应的优先级别


def getOperOrder(ch):
    if ch == '|':
        return 1
    if ch in ['+', '*', '?']:
        return 4
    if ch == ',':       #如果是连接符','
        return 3
    if ch == '&':
        return 2
    elif ch == '(':
        return 5
    return 0


def opappend(oper):  # 运算符入栈
    global changed
    if len(opera) == 0:
        opera.append(oper)  # 栈空，入栈
    else:
        ch = opera[-1]  # ch为栈顶运算符
        if ch == '(' and oper != ')':
            opera.append(oper)  # 如果是（，都进
        elif getOperOrder(ch) < getOperOrder(oper):
            opera.append(oper)  # 栈顶元素优先级小于待入运算符优先级,栈顶元素应该是优先级最小的
        elif getOperOrder(ch) >= getOperOrder(oper) and ch != '(':  # 栈顶元素优先级等于大于参数字符，出栈
            changed += opera.pop()  # 栈顶运算符出栈
            opappend(oper)  # 递归调用
        elif oper == ')':
            while ch != '(':  # 出栈到（之间的所有运算符
                changed += opera.pop()
                ch = opera[-1]
            if ch == '(':
                opera.pop()  # 左括号也出栈

    return True

endeavor = []    #将字符串处理为元素的操作队列
symbol = 0     #标志位判断
def judge(s):
    global endeavor
    global changed
    if s == 1 and len(endeavor)!=0:
        changed.append(''.join(endeavor))
        endeavor.clear()  #清空中转队列
        return True
    else:
        return False

def Change(a):  # 转后缀函数
    global endeavor
    global changed
    for c in a:
        if c.isalpha():  # 如果是字母
            endeavor.append(c)         #加入中间队列
            symbol = 0
        elif c == '(':
            symbol = 1
            judge(symbol)
            opera.append('(')  # 左括号进栈
        elif c == ')':
            symbol = 1
            judge(symbol)
            opappend(c)  # 弹出（及以后的运算符栈中的元素
        elif c == '|' or c == ',':
            symbol = 1
            judge(symbol)
            opappend(c)  # 如果运算符，判断后入栈
        elif c == '+' or c == '*' or c == '?' or c == '&'  :
            symbol = 1
            judge(symbol)
            opappend(c)  # 如果运算符，判断后入栈
    judge(1)                                                #如果最后是字母，也出栈
    while len(opera) != 0:  # 处理完所有的输入字符
        # print(opera)
        changed += opera.pop()  # 栈顶运算符出栈

    return changed

def build(data):         #给定一个表达式，建立树结构并对结点进行初始化
    t1 = Change(data)
    t2 = ''.join(t1)
    print('转后缀:', t2)
    i=t1
    count=0
    stack=[]            #对应下标
    newnode=[]          #根据后续生成的顺序list

    for c in i:
        if "*+?".find(c)!=-1:   #如果是一目运算符
            node=TreeNode(c,None,None,None,1,0)   #建立结点
            newnode.append(node)
            num=stack.pop()
            stack.append(count)
            newnode[count].left(newnode[num])
            newnode[num].root=newnode[count]
            count=count+1

        elif re.match(c,','):
            newnode.append(TreeNode(c,None,None,None,2,0))
            num1=stack.pop()#rightchild
            num2=stack.pop()#左子下标弹出

            stack.append(count)  #压入二目的运算符下标
            #父节点连接子节点
            newnode[count].left(newnode[num2])
            newnode[count].right(newnode[num1])
            #子节点连接父节点
            newnode[num1].root=newnode[count]
            newnode[num2].root=newnode[count]

            count=count+1


        elif re.match(c,'&'):
            newnode.append(TreeNode(c,None,None,None,2,0))
            num1 = stack.pop()  # rightchild
            num2 = stack.pop()
            stack.append(count)
            newnode[count].left(newnode[num2])
            newnode[count].right(newnode[num1])
            newnode[num1].root = newnode[count]
            newnode[num2].root = newnode[count]
            count=count+1


        elif re.match(c,'|'):
            newnode.append(TreeNode(c,None,None,None,2,0))
            num1 = stack.pop()  # rightchild
            num2 = stack.pop()
            stack.append(count)
            newnode[count].left(newnode[num2])
            newnode[count].right(newnode[num1])
            newnode[num1].root = newnode[count]
            newnode[num2].root = newnode[count]

            count=count+1



        else :     #如果是字母或者单词
            newnode.append(TreeNode(c,None,None,None,0,0))
            stack.append(count)
            count=count+1

    #优先级小的二目运算符是根，是对（）的考虑
    newnode[len(newnode)-1].treetype = 4

    traverse(newnode[len(newnode)-1])    #中序遍历
    return newnode[len(newnode) - 1]  # 返回根节点

def choosetype():           #选择交换节点的类型
    pass


def chooseone(num):             #选择具体的运算符进行交叉操作，num是2就是二目运算符
    if num == 0 and len(Type0) != 0 :
        return random.choice(Type0)
    elif num == 1 and len(Type1) != 0:
        return random.choice(Type1)
    elif num == 2 and len(Type2) != 0:            #要交换的是二目结点且有可选择的算符
        return random.choice(Type2)            #随机选择一个二目运算符
    elif num == 4 and len(Type4) != 0:
        return random.choice(Type4)
    else:
        return False



def mating(node1,node2):                       #两棵树进行交配
    classification(node1)                  #对树一进行节点分类操作
    #choosetype()
    Tnode1 = chooseone(2)                #先选一个二目的试一下
    emptyType()
    classification(node2)
    Tnode2 = chooseone(2)
    print ('chose',Tnode1.value,Tnode2.value)
    FatherNode1 = Tnode1.root           #fathernode1是树1选出节点的父节点
    FatherNode2 = Tnode2.root  # fathernode2是树2选出节点的父节点
    if FatherNode1.rightchild == Tnode1:        #如果Tnode1是右孩子
        if FatherNode2.leftchild == Tnode2:     #右左
            FatherNode1.rightchild = Tnode2
            Tnode2.root = FatherNode1
            FatherNode2.leftchild = Tnode1
            Tnode1.root = FatherNode2

        elif FatherNode2.rightchild == Tnode2:  # 右右
            FatherNode1.rightchild = Tnode2
            Tnode2.root = FatherNode1
            FatherNode2.rightchild = Tnode1
            Tnode1.root = FatherNode2

    elif FatherNode1.leftchild == Tnode1:   #如果Tnode1是左孩子
        if FatherNode2.leftchild == Tnode2:     #左左
            Tnode1.root = FatherNode2           #连
            FatherNode1.leftchild = Tnode2      #断
            Tnode2.root = FatherNode1  # 连
            FatherNode2.leftchild = Tnode1  # 断

        elif FatherNode2.rightchild == Tnode2:     #左右
            FatherNode1.leftchild = Tnode2
            Tnode2.root = FatherNode1
            FatherNode2.rightchild = Tnode1
            Tnode1.root = FatherNode2
    print('交配后树1')
    traverse(node1)
    print('交配后树2')
    traverse(node2)






###############################################主函数区域
data = 'a,b|c,d'
d2 = 'a,c|b?&d'
b2 = build(data)
b1 = build(d2)
print('根1',b1.value)
print('根2',b2.value)
mating(b1,b2)




#______________________________________________________________________________________________________________________________________________________










