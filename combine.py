import re  # 要实现的是leaning的树，叶子节点的是句子
import random
import sys
from scipy.special import comb
#sys.path.append('E:/python/final/membership.py')
import copy
import membership



numgenerate=0
F1value=[]
changed = []  # 转换后的后缀字符串
opera = []  # 运算符栈
pos = []  # 正例集S+
neg = []  # S-
Tnodelist = []  # 返回的根节点列表
test = []
ts = []
finall = []
alphabet = []

class TreeNode:  # 树节点类的定义

    def __init__(self, value=0, root=None, leftchild=None, rightchild=None, treetype=-1, treecheck=0, treeadd=0):
        self.root = root  # 父节点
        self.value = value
        self.leftchild = leftchild
        self.rightchild = rightchild
        self.treetype = treetype  # 用来判断结点是什么类型的结点
        self.treecheck = treecheck  # 用来判断该节点是否被遍历过
        self.treeadd = treeadd

    def left(self, leftchild):
        self.leftchild = leftchild

    def right(self, rightchild):
        self.rightchild = rightchild


class binarytree:
    def __init__(self, root=None):
        self.root = root


def traverse(node, num=0, Lout = 0):  # 中序遍历二叉树，num = 1的时候返回带','的表达式
    if num == 0:
        # 左孩子递归
        if node.leftchild != None:
            traverse(node.leftchild)
        # 根节点自身，中
        # print(node.value)  # 输出自身
        #print(node.value, node.treetype, node.treecheck)  # 输出自身
        # 右孩子递归
        if node.rightchild != None:
            traverse(node.rightchild)
        return True


    elif num == 1:
        lx = 0
        x1 = 0
        # 左孩子递归
        if node.leftchild != None:
            traverse(node.leftchild, 1)

        # print(node.value, node.treetype, node.treecheck,node.treeadd)  # 输出自身
        if node.treetype == 4:              #如果是根节点，入ts的list。
            ts.append(node)
        if node.treetype == 1:              #如果是一目运算符
            if node.leftchild.treetype == 0:
                if node.leftchild.treeadd  != 0 :  # 存在多重括号
                    node.leftchild.treeadd  = node.leftchild.treeadd  * 10 + 1  # 1/11/111
                elif node.leftchild.treeadd == 0:
                    node.leftchild.treeadd  = 1  # 左括号标志位
            else:
                lx = 1
                newnode = node
                while node.leftchild != None:
                    node = node.leftchild
                # 注意可能有多层括号的情况
                if node.treeadd != 0:  # 存在多重括号
                    node.treeadd = node.treeadd * 10 + 1  # 1/11/111
                elif node.treeadd == 0:
                    node.treeadd = 1  # 左括号标志位
                node = newnode.leftchild
                while node.rightchild != None:
                    node = node.rightchild
                if node.treeadd != 0 :               #存在多重括号
                    node.treeadd = node.treeadd * 10 + 2                #2/22/222
                elif node.treeadd == 0:
                    node.treeadd = 2  # 右括号
                node = newnode


            #ts.append(node)
        if node.treetype == 2 and node.root != None:  # 如果是二目
            ts.append(node)
            # elif node.treetype != 4:             #如果不是根节点,比较与父节点的优先级
            n1 = getOperOrder(node.value)
            n2 = getOperOrder(node.root.value)          #父节点的优先级
            if n1 < n2:  # 子节点优先级比父节点小，要加括号（）
                tempt = node
                # 左孩子递归
                while node.leftchild != None:
                    node = node.leftchild
                #注意可能有多层括号的情况
                if node.treeadd != 0 :               #存在多重括号
                    node.treeadd = node.treeadd * 10 + 1                #1/11/111
                elif node.treeadd == 0:
                    node.treeadd = 1  # 左括号标志位
                node = tempt                #还是换回父节点
                # 右孩子递归
                while node.rightchild != None:
                    node = node.rightchild
                if node.treeadd != 0 :               #存在多重括号
                    node.treeadd = node.treeadd * 10 + 2                #2/22/222
                elif node.treeadd == 0:
                    node.treeadd = 2  # 右括号
                node = tempt

        elif node.root == None:
            x1 = 1
        else:
            ts.append(node)

        # 右孩子递归
        if node.rightchild != None:
            traverse(node.rightchild, 1)

        if x1 == 1:             #x1为1的话是说明有根节点，遍历已经完成
            for x in ts:
                b = int(str(x.treeadd)[-1])             #b为标志位的最后一位
                aa = len(str(x.treeadd))
                if b == 0:
                    finall.append(x.value)
                elif b == 1:
                    while aa > 0:
                        finall.append('(')
                        aa = aa - 1
                    finall.append(x.value)
                    if x.root.treetype == 1:
                        finall.append(')')
                    x.treeadd = 0  # 重新置零
                elif b == 2:
                    finall.append(x.value)
                    while aa > 0:
                        finall.append(')')
                        aa = aa - 1
                    x.treeadd = 0

            ii = 0
            for i in finall:
                if i == '(':
                    if finall[ii + 1] == '&' or finall[ii + 1] == '|':
                        finall[ii] = '-'
                        finall.remove('-')
                        finall[ii + 1] = '-'
                        finall.remove('-')
                ii += 1

            rr = []
            rr = ''.join(finall)
            if Lout == 1:
                print('结果为：', ''.join(finall))
            ts.clear()
            finall.clear()

            return rr
        # print('结果:', ts)


def Traverse(node):  # 用来输出标准正则表达式的
    x1 = 0
    # 左孩子递归
    if node.leftchild != None:
        Traverse(node.leftchild)

    if node.treetype == 1:
        if node.leftchild.treeadd != 0:  # 存在多重括号
            node.leftchild.treeadd = node.leftchild.treeadd * 10 + 1  # 1/11/111
        elif node.leftchild.treeadd == 0:
            node.leftchild.treeadd = 1  # 左括号标志位
    if node.treetype == 4:
        ts.append(node)
    if node.treetype == 2 and node.root != None:  # 如果是二目
        if node.value == ',':
            x1 = 0
        elif node.value == '|' or node.value == '&':
            ts.append(node)
        # elif node.treetype != 4:             #如果不是根节点,比较与父节点的优先级
        n1 = getOperOrder(node.value)
        n2 = getOperOrder(node.root.value)
        if n1 < n2:  # 子节点优先级比父节点小，要加括号（）
            tempt = node
            # 左孩子递归
            while node.leftchild != None:
                node = node.leftchild
            # 注意可能有多层括号的情况
            if node.treeadd != 0 and node.treeadd != 4:  # 存在多重括号
                node.treeadd = node.treeadd * 10 + 1  # 1/11/111
            elif node.treeadd == 0:
                node.treeadd = 1  # 左括号标志位
            node = tempt  # 还是换回父节点
            # 右孩子递归
            while node.rightchild != None:
                node = node.rightchild
            if node.treeadd != 0 and node.treeadd != 4:  # 存在多重括号
                node.treeadd = node.treeadd * 10 + 2  # 2/22/222
            elif node.treeadd == 0:
                node.treeadd = 2  # 右括号
            node = tempt


    elif node.root == None:
        x1 = 1
    else:
        ts.append(node)

    # 右孩子递归
    if node.rightchild != None:
        Traverse(node.rightchild)

    if x1 == 1:
        for x in ts:
            if x.value == ',':
                x.treeadd=19
            b = int(str(x.treeadd)[-1])  # b为标志位的最后一位
            aa = len(str(x.treeadd))
            if b == 0:
                finall.append(x.value)
            elif b == 1:
                while aa > 0:
                    finall.append('(')
                    aa = aa - 1
                finall.append(x.value)
                if x.root.treetype == 1:
                    finall.append(')')
                x.treeadd = 0  # 重新置零
            elif b == 2:
                finall.append(x.value)
                while aa > 0:
                    finall.append(')')
                    aa = aa - 1
                x.treeadd = 0

            x.treeadd = 0
        ii = 0
        for i in finall:
            if i == '(':
                if finall[ii + 1] == '&' or finall[ii + 1] == '|':
                    finall[ii] = '-'
                    finall.remove('-')
                    finall[ii + 1] = '-'
                    finall.remove('-')
            ii += 1
        rr = []
        rr = ''.join(finall)
        print('结果为：', ''.join(finall))
        ts.clear()
        finall.clear()




# 不同类型节点的栈
Type1 = []
Type2 = []
Type0 = []
Type4 = []


def emptyType():  # 清空分类list
    Type0.clear()
    Type1.clear()
    Type2.clear()
    Type4.clear()


def allzero(node):  # treecheck归零
    # 左孩子递归
    if node.leftchild != None:
        traverse(node.leftchild)
    # 根节点自身，中
    node.treecheck = 0  # 输出自身
    # 右孩子递归
    if node.rightchild != None:
        traverse(node.rightchild)


def classification(node):  # 将表达式树中的结点按Type值进行归类
    # 左孩子递归

    if node.leftchild != None:
        classification(node.leftchild)

    # 根节点自身，中

    if node.treetype == 0:  # 入栈分类
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


# ___________________________________________________________________________________________________________________________________________________________

def isOper(ch):
    if ch in ['+', '|', '*', '&', '.', '(', ')', '?']:  # 第一部分——转后缀部分
        return True
    return False
    # 获取运算符所对应的优先级别


def getOperOrder(ch):
    if ch == '|':
        return 1
    if ch in ['+', '*', '?']:
        return 4
    if ch == ',':  # 如果是连接符','
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


endeavor = []  # 将字符串处理为元素的操作队列
symbol = 0  # 标志位判断


def judge(s):
    global endeavor
    global changed
    if s == 1 and len(endeavor) != 0:
        changed.append(''.join(endeavor))
        endeavor.clear()  # 清空中转队列
        return True
    else:
        return False


def Change(a):  # 转后缀函数
    global endeavor
    global changed
    changed = []
    for c in a:
        if c.isalpha():  # 如果是字母
            endeavor.append(c)  # 加入中间队列
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
        elif c == '+' or c == '*' or c == '?' or c == '&':
            symbol = 1
            judge(symbol)
            opappend(c)  # 如果运算符，判断后入栈
    judge(1)  # 如果最后是字母，也出栈
    while len(opera) != 0:  # 处理完所有的输入字符
        # print(opera)
        changed += opera.pop()  # 栈顶运算符出栈

    return changed


def build(data):  # 给定一个表达式，建立树结构并对结点进行初始化
    t1 = Change(data)
    t2 = ''.join(t1)
    #print('转后缀:', t2)
    i = t1
    count = 0
    stack = []  # 对应下标
    newnode = []  # 根据后续生成的顺序list

    for c in i:
        if "*+?".find(c) != -1:  # 如果是一目运算符
            node = TreeNode(c, None, None, None, 1, 0)  # 建立结点
            newnode.append(node)
            num = stack.pop()
            stack.append(count)
            newnode[count].left(newnode[num])
            newnode[num].root = newnode[count]
            count = count + 1

        elif re.match(c, ','):
            newnode.append(TreeNode(c, None, None, None, 2, 0))
            num1 = stack.pop()  # rightchild
            num2 = stack.pop()  # 左子下标弹出

            stack.append(count)  # 压入二目的运算符下标
            # 父节点连接子节点
            newnode[count].left(newnode[num2])
            newnode[count].right(newnode[num1])
            # 子节点连接父节点
            newnode[num1].root = newnode[count]
            newnode[num2].root = newnode[count]

            count = count + 1


        elif re.match(c, '&'):
            newnode.append(TreeNode(c, None, None, None, 2, 0))
            num1 = stack.pop()  # rightchild
            num2 = stack.pop()
            stack.append(count)
            newnode[count].left(newnode[num2])
            newnode[count].right(newnode[num1])
            newnode[num1].root = newnode[count]
            newnode[num2].root = newnode[count]
            count = count + 1


        elif re.match(c, '|'):
            newnode.append(TreeNode(c, None, None, None, 2, 0))
            num1 = stack.pop()  # rightchild
            num2 = stack.pop()
            stack.append(count)
            newnode[count].left(newnode[num2])
            newnode[count].right(newnode[num1])
            newnode[num1].root = newnode[count]
            newnode[num2].root = newnode[count]

            count = count + 1



        else:  # 如果是字母或者单词
            newnode.append(TreeNode(c, None, None, None, 0, 0))
            stack.append(count)
            count = count + 1

    # 优先级小的二目运算符是根，是对（）的考虑
    newnode[len(newnode) - 1].treetype = 4

    traverse(newnode[len(newnode) - 1])  # 中序遍历
    return newnode[len(newnode) - 1]  # 返回根节点


def choosetype():  # 选择交换节点的类型
    RD = random.random()  # 随机数轮盘赌选择Type
    if RD <= 0.1:  # 交配叶节点
        return 0
    elif RD > 0.1 and RD <= 0.5:
        return 1
    elif RD > 0.5 and RD <= 1:
        return 2
    else:
        return 2
    # 根节点的处理还没想好
    '''
    else:                  
        return 4
    '''


def chooseone(num):  # 选择具体的运算符进行交叉操作，num是2就是二目运算符
    if num == 0 and len(Type0) != 0:
        choosenode = random.choice(Type0)
        if choosenode.treecheck == 1:  # 如果是已经选过的节点就换一个
            Type0.remove(choosenode)  # 去掉这个点，避免二次重复遍历
            chooseone(num)
        choosenode.treecheck = 1  # 标记为已选择
        return choosenode
    elif num == 1 and len(Type1) != 0:
        choosenode = random.choice(Type1)
        if choosenode.treecheck == 1:  # 如果是已经选过的节点就换一个
            Type1.remove(choosenode)  # 去掉这个点，避免二次重复遍历
            chooseone(num)
        choosenode.treecheck = 1  # 标记为已选择
        return choosenode
    elif num == 2 and len(Type2) != 0:  # 要交换的是二目结点且有可选择的算符
        choosenode = random.choice(Type2)
        if choosenode.treecheck == 1:  # 如果是已经选过的节点就换一个
            Type2.remove(choosenode)  # 去掉这个点，避免二次重复遍历
            chooseone(num)
        choosenode.treecheck = 1  # 标记为已选择
        return choosenode  # 随机选择一个二目运算符
    elif num == 4 and len(Type4) != 0:
        choosenode = random.choice(Type4)
        if choosenode.treecheck == 1:  # 如果是已经选过的节点就换一个
            Type4.remove(choosenode)  # 去掉这个点，避免二次重复遍历
            chooseone(num)
        choosenode.treecheck = 1  # 标记为已选择
        return choosenode
    else:
        return False


def checkonce(node1, Tnode1, node2, root2):  # 确保单次性的函数
    t3 = []
    t4 = []
    t5 = []
    t8 = []

    treeall1 = []
    treeall2 = []
    node1all = []
    node2all = []
    tree1 = []          #树一剩下的结点
    tree2 = []
    emptyType()
    classification(node1)
    t1 = Type0
    for x in t1:
        t3.append(x.value)          #t3是树一所有子叶
        treeall1.append(x)
    emptyType()
    classification(node2)
    t2 = Type0
    for x1 in t2:
        t4.append(x1.value)         #t4是结点2的子叶
        node2all.append(x1)
    emptyType()
    classification(Tnode1)
    t6 = Type0
    for x1 in t6:
        t5.append(x1.value)         #t5是结点1的子叶
        node1all.append(x1)
    emptyType()
    classification(root2)
    rt = Type0
    for rx in rt:
        t8.append(rx.value)         #t8是树二的所有子叶
        treeall2.append(rx)

    t7 = [i for i in t3 if i not in t5]             #t7是树一剩余的叶子
    for i in treeall1:
        if i.value not in t5:
            tree1.append(i)

    t9 = [i1 for i1 in t8 if i1 not in t4]          #t9是树二剩余的叶子
    for i in treeall2:
        if i.value not in t4:
            tree2.append(i)
    a = []
    a = [x for x in t7 if x in t4]  # 两个列表表都存在,即新树一里面有重复元素
    b = []
    b = [x for x in t9 if x in t5]
    emptyType()
    Ldou = 0  # 双运算符标志位
    # 为防止出现两个一目运算符重叠，加一步判断
    TRoot1 = Tnode1.root
    TRoot2 = node2.root
    if Tnode1.treetype == 1 and TRoot2.treetype == 1:

        Ldou = 1
    if node2.treetype == 1 and TRoot1.treetype == 1:
        Ldou = 1
    if Ldou == 1 :              #父子节点同为一目运算符
        return False
    if len(a) != 0:
        treeone = [x for x in tree1 if x.value in t4]           #新树一中的重复结点
        t1value = t4 + t7

        va1tree = [x for x in alphabet if x not in t1value]
        if len(va1tree) < len(treeone):
            return False
        for i in treeone:
            i.value =  va1tree[0]
            va1tree.pop(0)
        va1tree.clear()
    if len(b) != 0 :
        treetwo = [x for x in tree2 if x.value in t5]
        t1value = t5 + t9
        va1tree = [x for x in alphabet if x not in t1value]
        if len(va1tree) < len(treetwo):
            return False
        for i in treetwo:
            i.value = va1tree[0]
            va1tree.pop(0)
        va1tree.clear()
    return True
    # if len(a) != 0 or len(b) != 0 :  # 如果有相同元素
    #     # print('不满足单次性')
    #     return False
    #else:
        # print('满足单次性！')
       # return True

def checkalph(node,alp = []):                  #保证变异后的单次性
    tp = []             #叶节点list
    apllist = []
    rootnode = node
    while node.root != None:
        node = node.root
    emptyType()
    classification(node)
    t = Type0
    for x in t:
        tp.append(x.value)
    emptyType()
    node = rootnode
    apllist = [x for x in alp if x not in tp]           #找到可以满足单次性的单词集合

    if len(apllist) > 0 :
        value = random.choice(apllist)
        return value
    else:
        return node.value

def mating(node1, node2):  # 两棵树进行交配
    emptyType()
    classification(node1)  # 对树一进行节点分类操作
    Ct1 = choosetype()
    # print("type1:",Ct1)
    Tnode1 = chooseone(Ct1)  # 先选一个二目的试一下
    while Tnode1 == False:              #如果为空，再选一个
        Ct1 = choosetype()
        Tnode1 = chooseone(Ct1)
    emptyType()
    classification(node2)
    Ct2 = choosetype()
    # print('type2:',Ct2)
    Tnode2 = chooseone(Ct2)
    while Tnode2 == False:
        Ct2 = choosetype()
        Tnode2 = chooseone(Ct2)
    emptyType()

    # checkonce(node1,Tnode2)

    # 检测单次性!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # import sys
    # sys.setrecursionlimit(1000000)         #修改递归次数
    if checkonce(node1, Tnode1, Tnode2, node2) == False:  # 如果不满足单次性,先换Tnode2，再换Tnode1
        emptyType()
        classification(node1)
        TN = []
        for x in Type0:
            TN.append(x)
        for x in Type1:
            TN.append(x)
        for x in Type2:
            TN.append(x)
        emptyType()
        classification(node2)
        TN2 = []

        for x in Type0:
            TN2.append(x)
        for x in Type1:
            TN2.append(x)
        for x in Type2:
            TN2.append(x)
        emptyType()
        ct = 0
        tn1 = []
        tn2 = []
        #for x in TN:
            #for y in TN2:
        xw = 0
        while xw == 0:
            x = random.choice(TN)
            y = random.choice(TN2)
            tt = checkonce(node1, x, y, node2)  # 如果Tnode2有结点，再次判断是否满足
            if tt == True:
                xw = 1
                    #ct = 1
                    #tn1.append(x)
                    #tn2.append(y)
                    # print('约束成功！')
                Tnode1 = x
                Tnode2 = y

        #             break
        #     if ct == 1:
        #         break
        # if ct == 0:
        #     print('/////单次失败/////')
        #elif ct == 1:
            #s = len(tn1)
            #num = random.randint(0, s - 1)
            #Tnode1 = tn1[num]
            #Tnode2 = tn2[num]

    #print('choose 1AND2:', Tnode1.value, Tnode2.value)

    FatherNode1 = Tnode1.root  # fathernode1是树1选出节点的父节点           #这点有问题，会存在false返回后当成节点的问题
    FatherNode2 = Tnode2.root  # fathernode2是树2选出节点的父节点

   # print('F1 and F2', FatherNode1.value, FatherNode2.value)

    if FatherNode1.rightchild == Tnode1:  # 如果Tnode1是右孩子
        if FatherNode2.leftchild == Tnode2:  # 右左
            FatherNode1.rightchild = Tnode2
            Tnode2.root = FatherNode1
            FatherNode2.leftchild = Tnode1
            Tnode1.root = FatherNode2

        elif FatherNode2.rightchild == Tnode2:  # 右右
            FatherNode1.rightchild = Tnode2
            Tnode2.root = FatherNode1
            FatherNode2.rightchild = Tnode1
            Tnode1.root = FatherNode2

    elif FatherNode1.leftchild == Tnode1:  # 如果Tnode1是左孩子
        if FatherNode2.leftchild == Tnode2:  # 左左
            Tnode1.root = FatherNode2  # 连
            FatherNode1.leftchild = Tnode2  # 断
            Tnode2.root = FatherNode1  # 连
            FatherNode2.leftchild = Tnode1  # 断

        elif FatherNode2.rightchild == Tnode2:  # 左右
            FatherNode1.leftchild = Tnode2
            Tnode2.root = FatherNode1
            FatherNode2.rightchild = Tnode1
            Tnode1.root = FatherNode2

   # print('交配后树1')
    #traverse(node1)
    #print('交配后树2')
    #traverse(node2)
    #print('输出表达式：')
    # traverse(node1,1)
    # traverse(node2, 1)


Lnewlist = []
x = 0


def RandomMating(nodelist):
    global x
    length = len(nodelist)
    if len(nodelist) == 0:
        return 0
    while length >= 1:
        Lnewlist.append(x)
        x += 1
        length = length - 1
    if len(Lnewlist) < 2:
        print('nodenum error')
        return  False
    while len(Lnewlist) >= 2:  # 能继续交配就递归交配
        n1 = random.choice(Lnewlist)
        node1 = nodelist[n1]  # 选取列表中的一个根节点
        Lnewlist.remove(n1)  # 移出列表，避免二次交配
        n2 = random.choice(Lnewlist)
        node2 = nodelist[n2]
        Lnewlist.remove(n2)
        mating(node1, node2)

    for li in Lnewlist:
        Lnewlist.remove(li)
        # nodelist.remove(li)
    #print('随机交配成功')
    x = 0
    return True
    # Lnewlist.clear()
    # print('ll:',len(Lnewlist))


####################################################################新
def get_F1(regex):  # 计算F1
    TP = 0  # 真正例
    FP = 0  # 假正例
    FN = 0  # 假反例
    TN = 0  # 真反例
    for sen in pos:  # 正例
        if membership.member(regex, sen) == False:  # 假正例
            FN += 1
        else:
            TP += 1
    for sen in neg:  # 反例
        if membership.member(regex, sen) == False:
            TN += 1
        else:
            FP += 1

    F1 = (TP - FN  + TN - FP) / (TP+FN+TN+FP)


    return F1


def get_F1final(regex):  # 计算F1
    global F1value
    TP = 0  # 真正例
    FP = 0  # 假正例
    FN = 0  # 假反例
    TN = 0  # 真反例
    for sen in pos:  # 正例
        if membership.member(regex, sen) == False:  # 假正例
            FN += 1
        else:
            TP += 1
    for sen in neg:  # 反例
        if membership.member(regex, sen) == False:
            TN += 1
        else:
            FP += 1

    F1 = (TP - FN  + TN - FP) / (TP+FN+TN+FP)
    F1value.append(F1)


    return F1


def screen(Tnodelist):  # 进行筛选，去掉一般的元素
    nodeF1value = []
    for node in Tnodelist:
        regex = traverse(node, 1)  # !!!!!!!!

        nodeF1value.append(get_F1(regex))

    for i in range(0, int(len(Tnodelist) / 2)):
        min = nodeF1value[0]
        for node in nodeF1value:
            if min > node:
                min = node
        Ztemp=0
        for temp in nodeF1value:
            if temp==min:
                break
            Ztemp+=1

        Tnodelist.remove(Tnodelist[Ztemp])
        nodeF1value.remove(min)


    Ztest=copy.deepcopy(Tnodelist)
    return Ztest


def screenfinal(Tnodelist):  # 进行最后筛选，去掉一般的元素，输出F1
    nodeF1value = []
    for node in Tnodelist:
        regex = traverse(node, 1)  # !!!!!!!!

        nodeF1value.append(get_F1final(regex))

    for i in range(0, int(len(Tnodelist) / 2)):
        min = nodeF1value[0]
        for node in nodeF1value:
            if min > node:
                min = node
        Ztemp=0
        for temp in nodeF1value:
            if temp==min:
                break
            Ztemp+=1

        Tnodelist.remove(Tnodelist[Ztemp])
        nodeF1value.remove(min)


    Ztest=copy.deepcopy(Tnodelist)
    return Ztest

def variation(test):  # 对test进行逐个变异
    for tree in test:
        varytraverse(tree)


def ReadTxtName(rootdir):  # 按行读文件函数
    lines = []
    with open(rootdir, 'r') as file_to_read:
        while True:
            line = file_to_read.readline()
            if not line:
                break
            line = line.strip('\n')  # 去掉换行符
            # line = line.replace(",","")           #去掉逗号拼接为字符
            lines.append(line)
    return lines


def varytraverse(node):  # 遍历进行变异
    if node.leftchild != None:
        varytraverse(node.leftchild)
    newrandom = random.random()
    aberration(node, newrandom)
    if node.rightchild != None:
        varytraverse(node.rightchild)


def aberration(node=None, randomdate=1):  # 判断节点是否变异
    if node.treetype == 2:  # 定义二目运算符的变异率
        if randomdate <= 0.9:
            check = random.random()
            if check <= 0.33:
                node.value = '&'
            elif check <= 0.66:
                node.value = '|'
            else:
                node.value = ','
        else:
            return False
    if node.treetype == 1:  # 定义一目运算符的变异率
        if randomdate <= 0.8:
            check = random.random()  # 小于0.01，变异
            if check <= 0.33:
                node.value = '+'
            elif check <= 0.66:
                node.value = '*'
            else:
                node.value = '?'  # 小于0.01，变异
        else:
            return False
    if node.treetype == 0:          #定义单词的变异率
         if randomdate <=0.8:###改
             node.value = checkalph(node,alphabet)
         else:
             return False


def merge(Tnodelist,test):
   # global Tnodelist
    global Inputlist1
    if len(Inputlist1) % 2 != 0:
        test.remove(test[len(test) - 1])
    ZTnodelist = Tnodelist + test
    return ZTnodelist


def contrust(line):#扫描进行判断
    global alphabet
    word = ''
    for i in neg:
        word = ''
        for z in i:

            if z == ',':
                if word not in alphabet:
                    alphabet.append(word)
                word = ''
                continue
            else:
                word = word + z
        if word not in alphabet:
            alphabet.append(word)



def geneticalgorithm( test):
    global Tnodelist
    test.clear()
    test=screen(Tnodelist)  # 筛选
    variation(test)  # 变异
    RandomMating(test)  # 交配
    # 拼接
    Tnodelist.clear
    Tnodelist=merge(Tnodelist,test)




# 针对sire形式计算CC程序
class Renode:  # 定义cc结点类
    def __init__(self, regl=None, ccnum=0):
        self.regl = regl
        self.ccnum = ccnum

    def reg(self, regl):
        self.reg = regl

    def cnum(self, ccnum):
        self.ccnum = ccnum

def takecc(node):
    return  node.ccnum
def split_regex(regex):
    regex = regex.replace("+", "").replace("?", "").replace("*", "")
    return regex.split("&")


def cnt_cc(elems):
    nums = [elem.count(",") + 1 for elem in elems]
    cc, sum_num = 1, nums[0]
    for i in range(0, len(nums)):
        if i + 1 < len(nums):
            sum_num += nums[i + 1]
            cc *= comb(sum_num, nums[i + 1])

    return cc


def Rankcc(Relist):
    cclist = []
    for i in Relist:
        regex = i

        elems = split_regex(regex)
        cc = cnt_cc(elems)
        node = Renode(i,cc)
        cclist.append(node)


    cclist.sort(key=takecc)
    return  cclist

def geneticalgorithmfinal(test):
    global Tnodelist
    global numgenerate
    test.clear()
    test = screenfinal(Tnodelist)  # 筛选



    variation(test)  # 变异
    RandomMating(test)  # 交配


    Tnodelist.clear
    Tnodelist = merge(Tnodelist, test)  # 拼接
    # 输出
    numgenerate+=1
    k = F1value.index(max(F1value))
    print(numgenerate, " ", max(F1value), )
    traverse(Tnodelist[k], 1, 1)
    F1value.clear()







###############################################主函数区域
Inputlist1 = ['a*,b+|c?,d+', 'a*,b*,(c*,d*|e*)', 'a,b,c,d', 'a|b,c,d+','a*,b+&(c|d),e+','a,b*,(c+|d*)&e','a*,b*,c|d','b+&c,(d?|e)','a+,(b|d?)+,d*','(a|b)*,d+,e?','(a,b|c)*,d|e','(a|(b,c)*,d*)*','((a|c)*|d)*,e+','b*,a|c*,d']
neg = ReadTxtName(r'C:\Users\1\Desktop\LearningTree\no1_sigma=5_neg=75.txt')
pos = ReadTxtName(r'C:\Users\1\Desktop\LearningTree\no1_sigma=5_pos=25.txt')
contrust(neg)
contrust(pos)



for i in Inputlist1:
    a = build(i)
    Tnodelist.append(a)
time=1000
for i in range(time):
    geneticalgorithmfinal(test)

#geneticalgorithmfinal(test)

Lcclist = []
zfinal=0
# for i in Tnodelist:
#     Lcclist.append(traverse(i,1,1))
# #    print(F1value[zfinal])
#     zfinal+=1
# #Lfinal= Rankcc(Lcclist)
# #print(Lfinal[0].regl,Lfinal[0].ccnum)







