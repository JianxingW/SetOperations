def ListDim(alist):
    '''
    description: 
    获得列表维度
    原则为：
    若list中元素全部为int/float/string,则为1D列表
    若list中元素全部为list,则为2D列表
    否则触发异常
    alist：'[1,5,1,1]', '[[1,5,1,1], [8,10,1,1]....]'
    '''
    type1=[type(i) in [int, float, str] for i in alist]
    type2=[type(i) in [list] for i in alist]
    if sum(type1)==len(alist):
        return 1
    elif sum(type1)==len(alist):
        return 2 
    else:
        raise Exception('Please give the right expressions!') 
    
def Expression2Limit(string):
    '''
    description: 
    求约束区间
    string：'x>=10', 'x>10 or x<100....', ...
    '''
    lim=[]
    count_or=string.count('or')
    if count_or>=1:
        for i in string.split(' or '):
            lim.append(_Expression2Limit_single(i))
    else:
        lim=_Expression2Limit_single(string)
    return lim

def _Expression2Limit_single(string):
    '''
    description: 
    *此函数不建议单独使用
    求约束区间，区间必须一段区间，不允许包含or
    string：'x>=10', 'x<100....', ...
    '''
    string=string.replace(' ', '')
    string=string.replace('=<', '<=')
    string=string.replace('=>', '>=')
    # 仅仅针对单个区间，不要包含or多个区间，否则触发异常
    # 同时包含上下限时不允许写成10>x>0,必须写成0<x<10，否则出发异常
    lim=[-float('inf'), float('inf'), 0, 0]
    count1=string.count('>')
    count2=string.count('<')
    count3=string.count('=')
    count4=string.count('or')
    if (count4>=1) or (count1==2) or (count1>=1 and count2>=1) or (count3>2):
        raise Exception('Single interval should be provided!')
    if count1==1:
        if count3==1:  #x>=10
            lim[0]=float(string.split('>=')[-1])
            lim[2]=1
        else:    #x>10
            lim[0]=float(string.split('>')[-1])
            lim[2]=0
    elif count2==1:
        if count3==1:  #x<=10
            lim[1]=float(string.split('<=')[-1])
            lim[3]=1
        else:
            lim[1]=float(string.split('<')[-1])
            lim[3]=0
    else:   #count2=2
        lim[0]=float(string.split('<')[0])
        lim[1]=float(string.split('<')[-1].split('=')[-1])
        if '=' in string.split('<')[1]:  # x<=10(...)20
            lim[2]=1
        if '=' in string.split('<')[2]:  # x(...)10<=20
            lim[3]=1
    return lim

def Limit2Expression(constraints):
    '''
    description: 
    constraints:若单个区间则constraints为1维列表; 若多个区间并且为or的关系，则constraints为2维列表
    约束区间[0, 10, 1, 0]翻译为0<=x<10
    约束区间[[0, 10, 1, 0], [20, 30, 1, 1],...]翻译为0<=x<10 or 20<=x<=30...
    '''
    mid=[]
    dim=ListDim(constraints)
    if dim==1:
        expres=_Limit2Expression_single(constraints)
    else:
        for constraint in constraints:
            mid.append(_Limit2Expression_single(constraint))
        if len(mid)==1:
            expres=mid[0]
        else:
            expres=mid[0]
            for mid_i in mid[1:]:
                expres=expres+' or '+mid_i
    return expres    

def _Limit2Expression_single(constraints):
    '''
    description: 
    *此函数不建议单独使用
    约束区间[0, 10, 1, 0]翻译为0<=x<10 
    constraints：必须写成1维列表形式[0, 10, 1, 0]否则触发异常
    '''
    if ListDim(constraints)>1:
        raise Exception('The input parameter should be a 1D list!')
    elif constraints==[]:
        expre=[]
    else: 
        if constraints[0]==-float('inf'):
            if constraints[3]==0:
                expre='x'+'<'+str(constraints[1])
            else:
                expre='x'+'<='+str(constraints[1])        
        elif constraints[1]==float('inf'):  
            if constraints[2]==0:
                expre='x'+'>'+str(constraints[0])
            else:
                expre='x'+'>='+str(constraints[0])  
        else:
            if constraints[2]==0:
                expre1=str(constraints[0])+'<'
            else:
                expre1=str(constraints[0])+'<='
            if constraints[3]==0:
                expre2='<'+str(constraints[1])
            else:
                expre2='<='+str(constraints[1])
            expre=expre1+'x'+expre2
    return expre

def Limit2string(lim):
    '''
    description: 
    约束区间转换为表达式
    lim=[1,2,0,1]/[[1,2,1,1], [4,5,0,1],...]
    result='(1, 2]'/'[1, 2] or (4, 5]'
    '''
    result=''
    if lim==[]:
        result=[]
    elif ListDim(lim)==1:    # np.array(lists).ndim=1
        if lim[2]==0:
            mid0='('
        else:
             mid0='['
        if lim[3]==0:
            mid3=')'
        else:
             mid3=']'
        result=mid0+str(lim[0])+', '+str(lim[1])+mid3
    else:
        for i, lim_i in enumerate(lim):
            if lim_i[2]==0:
                mid0='('
            else:
                 mid0='['
            if lim_i[3]==0:
                mid3=')'
            else:
                 mid3=']'
            if i==0:
                result+=(mid0+str(lim_i[0])+', '+str(lim_i[1])+mid3)
            else:
                result+=' or ' + (mid0+str(lim_i[0])+', '+str(lim_i[1])+mid3)         
    return result

def trim_csv(x):
    '''
    description: 
    专用函数，请忽略
    '''
    mid=x['载荷提供故障值'].values
    index=[]
    for i in mid:
        index.append('x' in i)
    return x[index] 

def IsSubset(lim1, lim2):
    '''
    description: 
    判断lim1是否为lim2的子集
    
    单个区间直接给出lim0=[0, 10, 1, 1],或者[[0, 10, 1, 1]](不推荐)
    多个区间必须以2D列表给出, [[0, 10, 1, 1], [20, 30, 1, 1]]
    
    lim1：单区间[1, 10, 1, 1]或区间列表[[1, 10, 1, 1], [18, 20, 1, 1]]
    lim2：单区间[0, 12, 1, 1]或区间列表[[0, 12, 1, 1], [15, 20, 1, 1]]
    当lim1所有区间都是lim2的子集时,输出1
    '''
    return Intersections([lim1, lim2])==lim1   

def Complement(lim0):
    '''
    description: 
    求区间补集
    单个区间直接给出lim0=[0, 10, 1, 1],或者[[0, 10, 1, 1]](不推荐)
    多个区间必须以2D列表给出, [[0, 10, 1, 1], [20, 30, 1, 1]]
    '''
    dim=ListDim(lim0)
    lim=[]
    if (dim==2) and (len(lim0)==1):
        lim0=lim0[0]
        dim=ListDim(lim0)
    if lim0==[]:
        lim=[-float('inf'), float('inf'), 0, 0]
    elif dim==1:
        if lim0[0]==-float('inf'):
            if lim0[1]==float('inf'):
                True
            else:
                lim=[lim0[1], float('inf'), 1-lim0[3], 0]
        elif lim0[1]==float('inf'):
                lim=[-float('inf'), lim0[0], 0, 1-lim0[2]]
        else:
                lim.append([-float('inf'), lim0[0], 0, 1-lim0[2]])
                lim.append([lim0[1], float('inf'), 1-lim0[3], 0])         
    else:
        for i, lim_i in enumerate(lim0[:-1]):
            if i==0:
                if lim_i[0]==-float('inf'):
                    True
                else:
                    lim.append([-float('inf'), lim_i[0], 0, 1-lim_i[2]])
            lim.append([lim_i[1], lim0[i+1][0], 1-lim_i[3], 1-lim0[i+1][2]])
            
        lim_i=lim0[-1]
        if lim_i[1]==float('inf'):
            True
        else:
            lim.append([lim_i[1], float('inf'), 1-lim_i[3], 0])
    if len(lim)==1:
        lim=lim[0]
    return lim     

#列表表达式取交集                            
def Intersections(limits, another_limits=None):
    '''
    description: 
    多个区间求交集, limits为嵌套列表形式，每个元素为约束区间, 每个约束区间不限制单区间(1/2维列表皆可)
    
    单个区间直接给出lim0=[0, 10, 1, 1],或者[[0, 10, 1, 1]](不推荐)
    多个区间必须以2D列表给出, [[0, 10, 1, 1], [20, 30, 1, 1]]
    
    列表每个元素内部(每个区间之间)的关系为or, 列表元素之间的关系为and
    limits：[[[0, 10, 1, 1], [15, 30, 1, 1]], [5, 20, 0, 0]]
    tips:
    如果同时给出another_limits(不推荐),则会求limits和another_limits的交集
    '''
    if another_limits!=None:
        limits=[limits, another_limits]
    if ListDim(limits)==1:
        limits=[limits]
    limit=[-float('inf'), float('inf'), 1, 1]
    for limit_i in limits:
        if type(limit_i)==list:
            limit=Intersection(limit, limit_i)
#         else:   #如果limits中包含非list值处理方式  忽略?
#             limit=[]
    if limit==[-float('inf'), float('inf'), 1, 1]:
        limit=[]
    return limit
def Intersection(limit1, limit2):
    '''
    description: 
    两个区间求交集, 不限制单区间(1/2维列表皆可)
        
    单个区间直接给出lim0=[0, 10, 1, 1],或者[[0, 10, 1, 1]](不推荐)
    多个区间必须以2D列表给出, [[0, 10, 1, 1], [20, 30, 1, 1]]
    
    limit1：[0, 10, 1, 1]/[[0, 10, 1, 1], [15, 30, 1, 1]]
    limit2：[5, 20, 0, 0]/...
    '''
    lim=[]
    dim1, dim2 = ListDim(limit1), ListDim(limit2)
    if ([] in limit1) or ([] in limit2):
        True
    elif dim1+dim2==2:
        lim=_Intersection_singles(limit1, limit2)
    elif dim1+dim2==3:
        if dim1==1:
            for limit2_i in limit2:
                mid=_Intersection_singles(limit1, limit2_i)
                if mid!=[]: 
                    lim.append(mid)
        else:
            for limit1_i in limit1:
                mid=_Intersection_singles(limit1_i, limit2)
                if mid!=[]: 
                    lim.append(mid)
    else: #dim1=2 dim2=2
        for limit1_i in limit1:
            for limit2_i in limit2:
                mid=_Intersection_singles(limit1_i, limit2_i)
                if mid!=[]: 
                    lim.append(mid)
    if len(lim)==1:
        lim=lim[0]
    return lim
def _Intersection_singles(limit1, limit2):
    '''
    description: 
    *此函数不建议单独使用
    两个单区间求交集, 必须为单区间(1维列表)否则触发异常
       
    单个区间直接给出lim0=[0, 10, 1, 1],或者[[0, 10, 1, 1]](不推荐)
    多个区间必须以2D列表给出, [[0, 10, 1, 1], [20, 30, 1, 1]]
    
    limit1：[0, 10, 1, 1]
    limit2：[5, 20, 0, 0]
    '''
    lim=[]
    lim1, lim2=limit1, limit2
    dim1, dim2 = ListDim(lim1), ListDim(lim2)
    if (dim1==2) and (len(limit1)==1):
        lim1=limit1[0]
        dim1 = ListDim(lim1)
    if (dim2==2) and (len(limit2)==1):
        lim2=limit2[0]
        dim2 = ListDim(lim2)
    
    if dim1+dim2==2:
        if lim1==[] or lim2==[]:
            lim=[]
        elif (lim1[0]>lim2[1]) or (lim2[0]>lim1[1]):
                True
        else:
            lim=[-float('inf'), float('inf'), 0, 0]
            mins=max([lim1[0], lim2[0]])
            maxs=min([lim1[1], lim2[1]])
            lim[0]=mins
            lim[1]=maxs
            if mins==lim2[0]:
                lim[2]=lim2[2]
            else:
                lim[2]=lim1[2]
            if maxs==lim2[1]:
                lim[3]=lim2[3]
            else:
                lim[3]=lim1[3]   
            
            if lim[0]==lim[1]:
                if lim[2]+lim[3]==2:   #lim[2]=1 and lim[3]=1
#                     lim=[lim[0]]
                    True
                else:
                    lim=[]
    else:
        raise Exception('Single intervals should be provided!')
    return lim

def UnionSets(limits, another_limits=None):
    '''
    description: 
    多个区间求并集, limits为嵌套列表形式，每个元素为约束区间, 每个约束区间不限制单区间(1/2维列表皆可)
    
    单个区间直接给出lim0=[0, 10, 1, 1],或者[[0, 10, 1, 1]](不推荐)
    多个区间必须以2D列表给出, [[0, 10, 1, 1], [20, 30, 1, 1]]
    
    列表每个元素内部(每个区间之间)的关系为or, 列表元素之间的关系为and
    limits：[[[0, 10, 1, 1], [15, 30, 1, 1]], [5, 20, 0, 0]]
    tips:
    如果同时给出another_limits(不推荐),则会求limits和another_limits的交集
    '''
    
    if another_limits!=None:
        limits=[limits, another_limits]
    #bug: np.array([[[1,2,3], [4,5,6]], [1,5,6]]).ndim=1   wjx:2021-8-10
    if ListDim(limits)==1:
        limits=[limits]
    limit=[]
    for limit_i in limits:
        if type(limit_i)==list:
            limit=UnionSet(limit, limit_i)
#         else:   #如果limits中包含非list值处理方式  忽略?
#             raise Exception('The given parameter should be a 2D list!')
    return limit

def UnionSet(limit1, limit2):
    '''
    description: 
    两个区间求交集, 不限制单区间(1/2维列表皆可)
    单个区间直接给出lim0=[0, 10, 1, 1],或者[[0, 10, 1, 1]](不推荐)
    多个区间必须以2D列表给出, [[0, 10, 1, 1], [20, 30, 1, 1]]
    limit1：[0, 10, 1, 1]/[[0, 10, 1, 1], [15, 30, 1, 1]]
    limit2：[5, 20, 0, 0]/...
    '''
    lim1, lim2=limit1.copy(), limit2.copy()
    dim1, dim2=ListDim(limit1), ListDim(limit2)
    if dim1==2:
        mid=[]
        for i, lim1_i in enumerate(limit1):
            mid.append(Complement(lim1_i))
        lim1=Complement(Intersections(mid))
    if dim2==2:
        mid=[]
        for i, lim2_i in enumerate(limit2):
            mid.append(Complement(lim2_i))
        lim2=Complement(Intersections(mid))      
    return Complement(Intersection(Complement(lim1), Complement(lim2)))
