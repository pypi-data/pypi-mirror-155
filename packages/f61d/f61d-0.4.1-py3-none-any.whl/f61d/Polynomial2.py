class Polynomial2():
    '''
    模二多项式环，定义方式有三种
    一是
        >>> Polynomial2([1,1,0,1]) # 指定每一项的系数，不能为空
        x^3 + x^2 + 1

    二是
        >>> Polynomial2('1101')
        x^3 + x^2 + 1

    三是
        >>> Poly([3,1,4]) # 直接给出系数为1的项的阶
        x^4 + x^3 + x
        >>> Poly()        # 可以为空，代表所有项系数为0，也就是0
        0
        >>> Poly(9,6,5)
        x^9 + x^6 + x^5
    '''
    def __init__(self,ll):
        
        if type(ll) ==  str:
            ll = list(map(int,ll))

        self.param = ll[::-1]
        self.ones = [i for i in range(len(self.param)) if self.param[i] == 1] # 系数为1的项的阶数列表
        self.Latex = self.latex()
        self.b = ''.join([str(i) for i in ll]) # 二进制形式打印系数
        
        self.order = 0 # 最高阶
        try:self.order = max(self.ones)
        except:pass
        
    def format(self,reverse = True):
        '''
            格式化打印字符串
            
            reverse = False时，可以低位在左
            但是注意定义多项式时只能高位在右
        '''
        r = ''
        if len(self.ones) == 0:
            return '0'
        if reverse:
            return ((' + '.join(f'x^{i}' for i in self.ones[::-1])+' ').replace('x^0','1').replace('x^1 ','x ')).strip()
        return ((' + '.join(f'x^{i}' for i in self.ones)+' ').replace('x^0','1').replace('x^1 ','x ')).strip()

    def __call__(self,x):# 懒得写
        '''
            懒得写了
        '''
        print(f'call({x})')

    def __add__(self,other):
        a,b = self.param[::-1],other.param[::-1]
        if len(a) < len(b):a,b = b,a
        for i in range(len(a)):
            try:a[-1-i] = (b[-1-i] + a[-1-i]) % 2
            except:break
        return Polynomial2(a)

    def __mul__(self,other):
        a,b = self.param[::-1],other.param[::-1]
        r = [0 for i in range(len(a) + len(b) - 1)]
        for i in range(len(b)):
            if b[-i-1] == 1:
                if i != 0:sa = a+[0]*i
                else:sa = a
                sa = [0] * (len(r)-len(sa)) + sa
                #r += np.array(sa)
                #r %= 2
                r = [(r[t] + sa[t])%2 for t in range(len(r))]
        return Polynomial2(r)

    def __sub__(self,oo):
        # 在模二多项式环下，加减相同
        return self + oo

    def div(self,other):
        r,b = self.param[::-1],other.param[::-1]
        if len(r) < len(b):
            return Polynomial2([0]),self

        q=[0] * (len(r) - len(b) + 1)
        for i in range(len(q)):
            if len(r)>=len(b):
                index = len(r) - len(b) + 1  # 确定所得商是商式的第index位
                q[-index] = int(r[0] / b[0])
                # 更新被除多项式
                b_=b.copy()
                b_.extend([0] * (len(r) - len(b)))
                b_ = [t*q[i] for t in b_] 
                r = [(r[t] - b_[t])%2 for t in range(len(r))]
                for j in range(len(r)):     #除去列表最左端无意义的0
                    if r[0]==0:
                        r.remove(0)
                    else:
                        break
            else:
                break
            
        return Polynomial2(q),Polynomial2(r)

    def __floordiv__(self,other): # 只重载了整除，即//
        return self.div(other)[0]

    def __mod__(self,other):
        return self.div(other)[1]

    def __repr__(self) -> str:
        return self.format()
    
    def __str__(self) -> str:
        return self.format()

    def __pow__(self,a):
        # 没有大数阶乘的需求，就没写快速幂
        t = Polynomial2([1])
        for i in range(a):
            t *= self
        return t
    
    def latex(self,reverse=True):
        '''
            Latex格式打印...其实就是给大于一位长度的数字加个括号{}
        '''
        def latex_pow(x):
            if len(str(x)) <= 1:
                return str(x)
            return '{'+str(x)+'}'
        
        r = ''
        if len(self.ones) == 0:
            return '0'
        if reverse:
            return (' + '.join(f'x^{latex_pow(i)}' for i in self.ones[::-1])+' ').replace('x^0','1').replace(' x^1 ',' x ').strip()
        return (' + '.join(f'x^{latex_pow(i)}' for i in self.ones)+' ').replace('x^0','1').replace(' x^1 ',' x ').strip()

    def __eq__(self,other):
        return self.ones == other.ones


def Poly(*args):
    '''
        另一种定义方式
        Poly([3,1,4]) 或 Poly(3,1,4)
    '''
    if len(args) == 1 and type(args[0]) in [list,tuple]:
        args = args[0]
        
    if len(args) == 0:
        return Polynomial2('0')
    ll = [0 for i in range(max(args)+1)]
    for i in args:
        ll[i] = 1
    return Polynomial2(ll[::-1])

PP = Polynomial2

P = Poly
