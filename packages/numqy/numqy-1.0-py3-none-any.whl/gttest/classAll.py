"""
给定一串字符，不超过100个字符，可能包括括号、数字、字母、标点符号、空格，编程检查这一串字符中的( ) ,[ ],{ }是否匹配。

输入格式:
输入在一行中给出一行字符串，不超过100个字符，可能包括括号、数字、字母、标点符号、空格。

输出格式:
如果括号配对，输出yes，否则输出no。

输入样例1:
sin(10+20)
输出样例1:
yes
输入样例2:
{[}]
输出样例2:
no
"""

try:
    n = []
    flag = True
    symbol = input()
    for i in symbol:
        if i in '([{':
            n.append(i)
        elif i in ')]}':
            if n==[]:
                flag = False
            else:
                top = n.pop()
                if not '([{'.index(top)==')]}'.index(i):
                    flag=Flase
    if n==[] and flag:
        print("yes")
    else:
        print("no")
except:
    print("no")


"""
假设以S和X分别表示入栈和出栈操作。如果根据一个仅由S和X构成的序列，对一个空堆栈进行操作，相应操作均可行（如没有出现删除时栈空）且最后状态也是栈空，则称该序列是合法的堆栈操作序列。请编写程序，输入S和X序列，判断该序列是否合法。

输入格式:
输入第一行给出两个正整数N和M，其中N是待测序列的个数，M（≤50）是堆栈的最大容量。随后N行，每行中给出一个仅由S和X构成的序列。序列保证不为空，且长度不超过100。

输出格式:
对每个序列，在一行中输出YES如果该序列是合法的堆栈操作序列，或NO如果不是。

输入样例：
4 10
SSSXXSXXSX
SSSXXSXXS
SSSSSSSSSSXSSXXXXXXXXXXX
SSSXXSXXX
输出样例：
YES
NO
NO
NO
"""

a, b = map(int, input().split())
for i in range(a):
    num = 0
    zz = list(input())
    for i in range(len(zz)):
        if zz[i] == 'S' and num < b:
            num += 1
        elif zz[i] == "X" and num > 0:
            num -= 1
        else:
            num+=2
            break


    if i == len(zz)-1 and num == 0:
        print("YES")
    else:
        print("NO")

"""
算术表达式有前缀表示法、中缀表示法和后缀表示法等形式。日常使用的算术表达式是采用中缀表示法，即二元运算符位于两个运算数中间。请设计程序将中缀表达式转换为后缀表达式。

输入格式:
输入在一行中给出不含空格的中缀表达式，可包含+、-、*、\以及左右括号()，表达式不超过20个字符。

输出格式:
在一行中输出转换后的后缀表达式，要求不同对象（运算数、运算符号）之间以空格分隔，但结尾不得有多余空格。

输入样例:
2+3*(7-4)+8/4
输出样例:
2 3 7 4 - * + 8 4 / +
"""

ans = []
stk = []
char_dict = {'+': 1, '-': 1, '*': 2, '/': 2, '(': 3, ')': 3}
s = input()
i = 0
while i < len(s):
    if (i < 1 or s[i - 1] == '(') and s[i] in ['+', '-'] or s[i].isdigit():
        tmp_s = ""
        if s[i] != '+':
            tmp_s += s[i]
        while i + 1 < len(s) and (s[i + 1] == '.' or s[i + 1].isdigit()):
            tmp_s += s[i + 1]
            i += 1
        ans.append(tmp_s)
    else:
        if s[i] == '(':
            stk.append(s[i])
        elif s[i] == ')':
            while stk and stk[-1] != '(':
                ans.append(stk.pop())
            stk.pop()
        else:
            while stk and stk[-1] != '(' and char_dict[stk[-1]] >= char_dict[s[i]]:
                ans.append(stk.pop())
            stk.append(s[i])
    i += 1
while stk:
    ans.append(stk.pop())
print(*ans)


"""
请实现一个MyQueue类，实现出队，入队，显示队列，求队列长度。

实现入队方法 push(int x); 实现出队方法 pop(); 实现求队列长度方法 size();实现显示队列方法：show() 。

输入格式:
每个输入包含1个测试用例。

每个测试用例第一行给出一个正整数 n (n <= 10^6) ，接下去n行每行一个数字，表示一种操作： 1 x ： 表示从队尾插入x，0<=x<=2^31-1。 2 ： 表示队首元素出队。 3 ： 表示求队列长度。4：表示显示队列中所有元素。

输出格式:
对于操作1，将要添加的元素添加到队列的尾部

对于操作2，若队列为空，则输出 “Invalid”,否则请输出队首元素，并将这个元素从队列中删除。

对于操作3，请输出队列长度。 每个输出项最后换行。

对于操作4，输出队列中每个元素，元素之间用空格分隔，最后一个元素后面没有空格。

输入样例:
在这里给出一组输入。例如：

9
1 23
1 34
3
4
2
1 56
2
3
1 90
输出样例:
在这里给出相应的输出。例如：

2
23 34
23
34
1
"""

n = []
for i in range(int(input())):
    oder = str(input()).split()
    if '1' == oder[0]:
        n.append(oder[1])
    elif '2' == oder[0]:
        if len(n)>0:
            print(n.pop(0))
        else:
            print("Invalid")
    elif '3' == oder[0]:
        print(len(n))
    else:
        print(' '.join(n))


"""
有n个人围成一圈（编号为1～n），从第1号开始进行1、2、3报数，凡报3者就退出，下一个人又从1开始报数……直到最后只剩下一个人时为止。请问此人原来的位置是多少号?

输入格式:
测试数据有多组，处理到文件尾。每组测试输入一个整数n（5≤n≤100）。

输出格式:
对于每组测试，输出最后剩下那个人的编号。

输入样例:
10
28
69
输出样例:
4
23
68
"""

n = []
try:
    while True:
        s = eval(input())
        for i in range(1,s+1):
            n.insert(0,i)
        i = 1
        while len(n)>1:
            num = n.pop()
            if i % 3 is not 0:
                n.insert(0,num)
            i+=1
        print(n.pop())
except:
    pass


"""
设某银行有A、B两个业务窗口，且处理业务的速度不一样，其中A窗口处理速度是B窗口的2倍 —— 即当A窗口每处理完2个顾客时，B窗口处理完1个顾客。给定到达银行的顾客序列，请按业务完成的顺序输出顾客序列。假定不考虑顾客先后到达的时间间隔，并且当不同窗口同时处理完2个顾客时，A窗口顾客优先输出。

输入格式:
输入为一行正整数，其中第1个数字N(≤1000)为顾客总数，后面跟着N位顾客的编号。编号为奇数的顾客需要到A窗口办理业务，为偶数的顾客则去B窗口。数字间以空格分隔。

输出格式:
按业务处理完成的顺序输出顾客的编号。数字间以空格分隔，但最后一个编号后不能有多余的空格。

输入样例:
8 2 1 3 9 4 11 13 15
输出样例:
1 3 2 9 11 4 13 15
"""

aa=input().split()
AA=[]
BB=[]
cc=[]
for i in range(1,len(aa)):
    if int(aa[i])%2==0:
        BB.append(aa[i])
    else:
        AA.append(aa[i])
c=0
for i in range(len(aa)-1):
    if len(AA)!=0:
        cc.append(AA.pop(0))
        c=c+1
    if len(BB)!=0 and (i+1)%2==0:
        cc.append(BB.pop(0))
print(" ".join(cc))


"""
读入n值及n个整数，建立单链表并遍历输出。

输入格式:
读入n及n个整数。

输出格式:
输出n个整数，以空格分隔（最后一个数的后面没有空格）。

输入样例:
在这里给出一组输入。例如：

2
10 5
输出样例:
在这里给出相应的输出。例如：

10 5
"""

try:
    n=input()
    s=input().split()
    print(" ".join(s))
except:
    pass


"""
已知两个非降序链表序列S1与S2，设计函数构造出S1与S2合并后的新的非降序链表S3。

输入格式:
输入分两行，分别在每行给出由若干个正整数构成的非降序序列，用−1表示序列的结尾（−1不属于这个序列）。数字用空格间隔。

输出格式:
在一行中输出合并后新的非降序链表，数字间用空格分开，结尾不能有多余空格；若新链表为空，输出NULL。

输入样例:
1 3 5 -1
2 4 6 8 10 -1
输出样例:
1 2 3 4 5 6 8 10
"""

lst = input().split()[:-1] + input().split()[:-1]
lst = list(map(int, lst))
if not lst:
    print('NULL')
else:
    lst.sort()
    for i in range(len(lst)):
        if i == len(lst) - 1:
            print(lst[i])
        else:
            print(lst[i], end=' ')


"""
输入若干个不超过100的整数，建立单链表，然后将链表中所有结点的链接方向逆置，要求仍利用原表的存储空间。输出逆置后的单链表。

输入格式:
首先输入一个整数T，表示测试数据的组数，然后是T组测试数据。每组测试数据在一行上输入数据个数n及n个不超过100的整数。

输出格式:
对于每组测试，输出逆置后的单链表，每两个数据之间留一个空格。

输入样例:
1
11 55 50 45 40 35 30 25 20 15 10 5
输出样例:
5 10 15 20 25 30 35 40 45 50 55
"""

i = int(input())
for j in range(i):
    n = input().split()
    s = []
    for jj in range(1,len(n)):
        s.append(n[jj])
    n = reversed(s)
    print(" ".join(n))
"""
对于给定的二叉树，本题要求你按从上到下、从左到右的顺序输出其所有叶节点。

输入格式：
首先第一行给出一个正整数 N（≤10），为树中结点总数。树中的结点从 0 到 N−1 编号。随后 N 行，每行给出一个对应结点左右孩子的编号。如果某个孩子不存在，则在对应位置给出 "-"。编号间以 1 个空格分隔。

输出格式：
在一行中按规定顺序输出叶节点的编号。编号间以 1 个空格分隔，行首尾不得有多余空格。

输入样例：
8
1 -
- -
0 -
2 7
- -
- -
5 -
4 6
输出样例：
4 1 5
"""

n=eval(input())
s={}
g=[str(x) for x in range(n)]
for i in range(n):
    s[str(i)]=input().split()
    for x in s[str(i)]:
        if x!='-':
            g.remove(x)
ans=[]
while g:
    temp=[]
    for x in g:
        if x=='-':
            continue
        l,r=s[x]
        if l=='-' and r=='-':
            ans.append(x)
        temp.append(l)
        temp.append(r)
    g=temp
print(' '.join(ans))


"""
给定一棵二叉树的先序遍历序列和中序遍历序列，要求计算该二叉树的高度。

输入格式:
输入首先给出正整数N（≤50），为树中结点总数。下面两行先后给出先序和中序遍历序列，均是长度为N的不包含重复英文字母（区别大小写）的字符串。

输出格式:
输出为一个整数，即该二叉树的高度。

输入样例:
9
ABDFGHIEC
FDHGIBEAC
输出样例:
5
"""

class BinaryTree:
    def __init__(self, newValue):
        self.key = newValue
        self.left = None
        self.right = None
        pass

    def insertLeft(self, newNode):
        if isinstance(newNode, BinaryTree):
            self.left = newNode
        else:
            p = BinaryTree(newNode)
            p.left = self.left
            self.left = p

    def insertRight(self, newNode):
        if isinstance(newNode, BinaryTree):
            self.right = newNode
        else:
            p = BinaryTree(newNode)
            p.right = self.right
            self.right = p

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def setRoot(self, newValue):
        self.key = newValue

    def getRoot(self):
        return self.key


def GetHeight(BT):
    h1 = 1
    h2 = 1
    if BT.getLeft() or BT.getRight():
        try:
            h1 += GetHeight(BT.getLeft())
        except:
            pass
        try:
            h2 += GetHeight(BT.getRight())
        except:
            pass
        return h1 if h1 > h2 else h2
    else:
        return 1


def preInTree(preOrder, inOrder):
    if preOrder == "":
        return
    T = BinaryTree(preOrder[0])
    n, r = len(inOrder), 0
    for i in range(n):
        if inOrder[i] == preOrder[0]:
            r = i
            break
    T.left = preInTree(preOrder[1: r + 1], inOrder[0: r])
    T.right = preInTree(preOrder[r + 1:], inOrder[r + 1:])
    return T


n = int(input())
preOrder = input()
inOrder = input()
T = preInTree(preOrder, inOrder)
print(GetHeight(T))


"""
6-1 二叉树的后序遍历（Python语言描述）

本题要求输出二叉树的后序遍历，输出格式见样例。

"""

def postOrder(T):
    if T == None:
        return
    postOrder(T.left)
    postOrder(T.right)
    print(T.key, end=' ')


"""
6-2 求二叉树高度（Python语言描述）

本题要求输出二叉树的高度（树根在第1层）。
"""

def getHeight(T):
    if T== None:
        return 0
    l=getHeight(T.left)
    r=getHeight(T.right)
    if l+1>r+1:
        return l+1
    return r+1

"""
6-3 二叉树的层次遍历（Python语言描述）

本题要求输出二叉树的层次遍历，输出格式见样例。
"""


def layerOrder(T):
    q = Queue()
    q.push(T)
    while not q.isEmpty():
        s = q.pop()
        print(s.key, end=' ')
        if s.left != None: q.push(s.left)
        if s.right != None: q.push(s.right)


"""
6-4 统计二叉树结点个数（Python语言描述）

本题要求统计二叉树结点个数。
"""


def nodeCount(T):
    if T == None:
        return 0
    l = nodeCount(T.left)
    r = nodeCount(T.right)
    return r + l + 1


"""
6-5 统计二叉树叶子结点的个数（Python语言描述）

本题要求计算二叉树中有多少片树叶，输出格式见样例。
"""


def leafCount(T):
    if T == None:
        return 0
    if T.left == None and T.right == None:
        return 1

    l = leafCount(T.left)
    r = leafCount(T.right)
    return l + r


"""
6-1 图的邻接表的实现python版

在图的邻接表存储结构下（基于顶点列表和单链表实现），本题要求图类里实现2个方法函数 def addVertex(self, vex_val): def addEdge(self, f, t, cost=0):
"""

class arcnode:
    pass

class vexnode:
    pass

    # 代码填写部分
    def addVertex(self, vex_val):
        s = vexnode(vex_val)
        self.vex_list.append(s)
        self.vex_num = self.vex_num + 1


    def addEdge(self, f, t, cost=0):
        s = arcnode(t, cost, self.vex_list[f].first_arc)
        self.vex_list[f].first_arc = s
        s = arcnode(f, cost, self.vex_list[t].first_arc)
        self.vex_list[t].first_arc = s


"""
6-2 邻接矩阵存储图的深度优先遍历（Python语言描述）

本题要求实现一个函数，试实现邻接矩阵存储图的深度优先遍历。
"""

def dfs(G,v):
    G.vis[v]=True
    print('',G.vertex[v],end='')
    for i in range(G.verNum):
        if G.edge[v][i]==1 and G.vis[i]==False:dfs(G,i)


"""
6-3 求采用邻接矩阵作为存储结构的无向图各顶点的度（Python语言描述）

本题要求实现一个函数，输出无向图每个顶点的数据元素的值，以及每个顶点度的值。
"""


def printDegree(G):
    for i in range(G.verNum):
        gree=0
        for j in range(G.verNum):
            if G.edge[i][j]==1:gree=gree+1
        print(str(G.vertex[i])+':'+str(gree))


"""
6-4 邻接矩阵存储图的广度优先遍历（Python语言描述）

本题要求实现一个函数，试实现邻接矩阵存储图的广度优先遍历。
"""

def bfs(G,v):
    q=Queue()
    q.push(v)
    print('',G.vertex[v],end='')
    G.vis[v]=True
    while(not q.isEmpty()):
        s=q.pop()
        for i in range(G.verNum):
            if G.edge[s][i]==1 and G.vis[i]==False:
                 G.vis[i]=True
                 print('',G.vertex[i],end='')
                 q.push(i)