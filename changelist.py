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

opera = []
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
    print(''.join(changed))
    return changed
alist = list('(a|b)*,d+&e?')
Change(alist)