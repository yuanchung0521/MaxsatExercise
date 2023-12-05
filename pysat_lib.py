import pysat
import time

#!/usr/bin/env python
# coding: utf-8


file_name = 'A2O1A1Ixp33_ASAP7_75t_R.txt'
cell_num_sel = 4
cell_count_number = 2
is_opt = True
bool_flag = True


metal_num = 3

now = time.ctime()

print("time now:", now)


# In[29]:


class Mos(object):
    
    def __init__(self, name, d, g, s, is_n, w, l, f):
        self.g = g
        self.d = d
        self.s = s
        self.name = name
        self.is_n = is_n
        self.w = w
        self.l = l
        self.f = f
        self.x = -1
        
    def __str__(self):
        return f"{self.name}: ({self.is_n}) g = {self.g}, d = {self.d}, s = {self.s}"
    
    def if_SD_Intersect(self, mos):
        if self.d == mos.d:
            return 4
        elif self.s == mos.s:
            return 1
        elif self.d == mos.s:
            return 3
        elif self.s == mos.d:
            return 2
        else: return -1

    
class Cell(object):
    
    def __init__(self, name, ports):
        self.n = []
        self.p = []
        self.sig = set()
        self.name = name
        self.ports = ports
        self.mos = []
        self.pa = []
        self.na = []
        
    def __str__(self):
        return f"{self.name}, {str(self.n)}"
           
    def if_same_g(self, x, y):
        return self.p[x].g == self.n[y].g
        


# In[30]:


with open('asap7_75t_SRAM_24.cdl') as f:
    lines = f.readlines()
    i = 0
    cells = []
    while i < len(lines):
        line = lines[i].strip().replace("\n","")
        #print(i, line)
        
        #empty newline
        if not line: 
            i = i + 1
            continue
        
        #spilit word
        words = line.split()
        if words[0] == ".SUBCKT":
            
            ckt = Cell(words[1], words[2:])
            i = i + 1
            
            words = lines[i].strip().replace("\n","").split()
            
            # deal with transistor
            while words[0] != ".ENDS":
                idw = words[6].find("=")
                idl = words[7].find("=")
                idf = words[8].find("=")
                
                #m = Mos(words[0], words[1], words[2], words[3], 
                #          words[5][0], words[6][idw:], 
                #          words[7][idl:], words[8][idf:])
                
                m = Mos(words[0], words[1], words[2], words[3], 
                          words[5][0], 81, 
                          words[7][idl+1:len(words[7])-1], words[8][idf+1:])
                
                #m = Mos(words[0], words[1], words[2], words[3], 
                #          words[5][0], words[6][idw+1:len(words[6])-1], 
                #          words[7][idl+1:len(words[7])-1], words[8][idf+1:])
                
                if m.is_n == "n":
                    ckt.n.append(m)
                    
                else:
                    ckt.p.append(m)
                    
                ckt.mos.append(m)
                    
                ckt.sig.add(m.s)
                ckt.sig.add(m.g)
                ckt.sig.add(m.d)
                
                i = i + 1
                words = lines[i].strip().replace("\n","").split()
                
            #print([ str(m) for m in ckt.mos])
            #print("\n")
            cells.append(ckt)
            #print([str(n) for n in ckt.n])
            #break
        
        else:
            i = i + 1     
                     
    #print(len(cells), '\n',  cells[0].name, '\n', cells[0].n[1], cells[0].n[0])
    #print((cells[0].n[0]).if_SD_Intersect(cells[0].n[1]))


# In[31]:


num = []
for i in range(len(cells) - len(cells) + 1):
    pnum = len(cells[i].p)
    nnum = len(cells[i].n)
    snum = len(cells[i].sig) 
    cnum = max(pnum, nnum)
    
    pp = [dict() for _ in range(cnum)]
    nn = [dict() for _ in range(cnum)]
    
    for x in range(pnum):
        for xi in range(pnum):
            
            if x == xi: continue
                
            if cells[i].p[x].d == cells[i].p[xi].s:
                if xi not in pp[x]: 
                    pp[x][xi] = set()
                pp[x][xi].add("ds")        
            if cells[i].p[x].s == cells[i].p[xi].s:
                if xi not in pp[x]: 
                    pp[x][xi] = set()
                pp[x][xi].add("ss")
            if cells[i].p[x].s == cells[i].p[xi].d:
                if xi not in pp[x]: 
                    pp[x][xi] = set()
                pp[x][xi].add("sd")
            if cells[i].p[x].d == cells[i].p[xi].d:
                if xi not in pp[x]:
                    pp[x][xi] = set()
                pp[x][xi].add("dd")
            
            if cells[i].n[x].d == cells[i].n[xi].s:
                if xi not in nn[x]:
                    nn[x][xi] = set()
                nn[x][xi].add("ds")
            if cells[i].n[x].s == cells[i].n[xi].s:
                if xi not in nn[x]: 
                    nn[x][xi] = set()
                nn[x][xi].add("ss")
            if cells[i].n[x].s == cells[i].n[xi].d:
                if xi not in nn[x]:
                    nn[x][xi] = set()
                nn[x][xi].add("sd")
            if cells[i].n[x].d == cells[i].n[xi].d:
                if xi not in nn[x]: 
                    nn[x][xi] = set()
                nn[x][xi].add("dd")
                    
    cells[i].pa = pp.copy()
    cells[i].na = nn.copy()
    num.append([pnum, nnum, snum, cnum])


# In[32]:


class Vertex(object):
    
    def __init__(self, v_type, z, y, x):
        self.z = z
        self.y = y
        self.x = x
        self.v_type = v_type
        self.pin_name = ""
        self.up = 0
        self.down = 0
        self.left = 0
        self.right = 0
        self.front = 0
        self.back = 0
        self.super_node = 0
        self.adj_num = 0
        self.adj = []
        #self.adj = [self.up, self.down, self.left, self.right, self.front, self.back, self.super_node]


# In[33]:


fin_num = 2
empty_track_num = 2
track_num = 2 * fin_num + empty_track_num

IO_pin = []
POWER_pin = []

count = 0
for i in range(len(cells)):
    #if cells[i].name == 'INVxp67_ASAP7_75t_R':
    if len(cells[i].n) == cell_num_sel:
        print(cells[i].name)
        x = i
        count += 1
    if count == cell_count_number:
        break

#x = 0
this_cell = cells[x]

for pin in this_cell.ports:
    if(pin not in IO_pin and pin != 'VDD' and pin != 'VSS'):
        IO_pin.append(pin)
    if pin not in POWER_pin and pin not in IO_pin:
        POWER_pin.append(pin)
        
pin_list = []
flow_table = []
power_table = [0]

for y in range(len(this_cell.mos)):
    pin = this_cell.mos[y].d
    if pin not in POWER_pin:
        if pin not in pin_list:
            pin_list.append(pin)
            temp1 = []
            temp1.append(1)
            temp1.append(pin)
            #temp1.append(x)
            #temp1.append(y)
            if this_cell.mos[y] in this_cell.n:
                temp1.append('N')
                temp1.append(this_cell.n.index(this_cell.mos[y]))
            elif this_cell.mos[y] in this_cell.p:
                temp1.append('P')
                temp1.append(this_cell.p.index(this_cell.mos[y]))
            else:
                print("wrong")
            temp1.append('d')
            flow_table.append(temp1)
        else:
            index = pin_list.index(pin)
            flow_table[index][0] += 1
            #flow_table[index].append(x)
            #flow_table[index].append(y)
            if this_cell.mos[y] in this_cell.n:
                flow_table[index].append('N')
                flow_table[index].append(this_cell.n.index(this_cell.mos[y]))
            elif this_cell.mos[y] in this_cell.p:
                flow_table[index].append('P')
                flow_table[index].append(this_cell.p.index(this_cell.mos[y]))
            else:
                print("wrong")
            flow_table[index].append('d')
    else:
        power_table[0] += 1
        if this_cell.mos[y] in this_cell.n:
            power_table.append('N')
            power_table.append(this_cell.n.index(this_cell.mos[y]))
        elif this_cell.mos[y] in this_cell.p:
            power_table.append('P')
            power_table.append(this_cell.p.index(this_cell.mos[y]))
        power_table.append('d')
        
    pin = this_cell.mos[y].g
    if pin not in POWER_pin:
        if pin not in pin_list:
            pin_list.append(pin)
            temp1 = []
            temp1.append(1)
            temp1.append(pin)
            #temp1.append(x)
            #temp1.append(y)
            if this_cell.mos[y] in this_cell.n:
                temp1.append('N')
                temp1.append(this_cell.n.index(this_cell.mos[y]))
            elif this_cell.mos[y] in this_cell.p:
                temp1.append('P')
                temp1.append(this_cell.p.index(this_cell.mos[y]))
            else:
                print("wrong")
            temp1.append('g')
            flow_table.append(temp1)
        else:
            index = pin_list.index(pin)
            flow_table[index][0] += 1
            #flow_table[index].append(x)
            #flow_table[index].append(y)
            if this_cell.mos[y] in this_cell.n:
                flow_table[index].append('N')
                flow_table[index].append(this_cell.n.index(this_cell.mos[y]))
            elif this_cell.mos[y] in this_cell.p:
                flow_table[index].append('P')
                flow_table[index].append(this_cell.p.index(this_cell.mos[y]))
            else:
                print("wrong")
            flow_table[index].append('g')
    else:
        power_table[0] += 1
        if this_cell.mos[y] in this_cell.n:
            power_table.append('N')
            power_table.append(this_cell.n.index(this_cell.mos[y]))
        elif this_cell.mos[y] in this_cell.p:
            power_table.append('P')
            power_table.append(this_cell.p.index(this_cell.mos[y]))
        power_table.append('g')
    
    
    pin = this_cell.mos[y].s
    if pin not in POWER_pin:
        if pin not in pin_list:
            pin_list.append(pin)
            temp1 = []
            temp1.append(1)
            temp1.append(pin)
            #temp1.append(x)
            #temp1.append(y)
            if this_cell.mos[y] in this_cell.n:
                temp1.append('N')
                temp1.append(this_cell.n.index(this_cell.mos[y]))
            elif this_cell.mos[y] in this_cell.p:
                temp1.append('P')
                temp1.append(this_cell.p.index(this_cell.mos[y]))
            else:
                print("wrong")
            temp1.append('s')
            flow_table.append(temp1)
        else:
            index = pin_list.index(pin)
            flow_table[index][0] += 1
            #flow_table[index].append(x)
            #flow_table[index].append(y)
            if this_cell.mos[y] in this_cell.n:
                flow_table[index].append('N')
                flow_table[index].append(this_cell.n.index(this_cell.mos[y]))
            elif this_cell.mos[y] in this_cell.p:
                flow_table[index].append('P')
                flow_table[index].append(this_cell.p.index(this_cell.mos[y]))
            else:
                print("wrong")
            flow_table[index].append('s')
    else:
        power_table[0] += 1
        if this_cell.mos[y] in this_cell.n:
            power_table.append('N')
            power_table.append(this_cell.n.index(this_cell.mos[y]))
        elif this_cell.mos[y] in this_cell.p:
            power_table.append('P')
            power_table.append(this_cell.p.index(this_cell.mos[y]))
        power_table.append('s')
    
flow_cnt = 0
for i in range(len(flow_table)):
    #temp = flow_table[i][0]
    #flow_cnt += temp*(temp-1) / 2
    if flow_table[i][1] in IO_pin:
        #flow_table[i][0] += 1
        for j in range(3):
            continue
            #flow_table[i].append('EX')

print(IO_pin)
print(POWER_pin)    
print(' ')
#print(flow_table)

for x in flow_table:
    print(x)
    
#print(flow_cnt)
#print(len(flow_table))


# In[34]:


n_length = len(this_cell.n)
print(n_length)
p_length = len(this_cell.p)
pin_length = len(this_cell.ports)
P_NET = []
N_NET = []
for i in range(n_length):
    P_NET.append([])
    N_NET.append([])

    
for y in range(len(this_cell.p)):
    pin = this_cell.p[y].d
    print(pin)
    x = 0
    for n in range(len(flow_table)):
        if pin == flow_table[n][1]:
            x = n
            break
        if pin=="VDD":
            x=-1
            break
        if pin=="VSS":
            x=-2
            break
    P_NET[y].append(x)
    
    pin = this_cell.p[y].g
    x = 0
    for n in range(len(flow_table)):
        if pin == flow_table[n][1]:
            x = n
            break
        if pin=="VDD":
            x=-1
            break
        if pin=="VSS":
            x=-2
            break
    P_NET[y].append(x)
    
    pin = this_cell.p[y].s
    x = 0
    for n in range(len(flow_table)):
        if pin == flow_table[n][1]:
            x = n
            break
        if pin=="VDD":
            x=-1
            break
        if pin=="VSS":
            x=-2
            break
        
    P_NET[y].append(x)
    
for y in range(len(this_cell.n)):
    pin = this_cell.n[y].d
    x = 0
    for n in range(len(flow_table)):
        if pin == flow_table[n][1]:
            x = n
            break
        if pin=="VDD":
            x=-1
            break
        if pin=="VSS":
            x=-2
            break
    N_NET[y].append(x)
    
    pin = this_cell.n[y].g
    x = 0
    for n in range(len(flow_table)):
        if pin == flow_table[n][1]:
            x = n
            break
        if pin=="VDD":
            x=-1
            break
        if pin=="VSS":
            x=-2
            break
    N_NET[y].append(x)
    
    pin = this_cell.n[y].s
    x = 0
    for n in range(len(flow_table)):
        if pin == flow_table[n][1]:
            x = n
            break
        if pin=="VDD":
            x=-1
            break
        if pin=="VSS":
            x=-2
            break
    N_NET[y].append(x)

    
print(N_NET)
print(P_NET)


# In[35]:


#print(P_NET)
#print(N_NET)

VDD_cnt = 0
VSS_cnt = 0

NET_cnt = []
for i in range(len(flow_table)):
    NET_cnt.append(0)

P_FLOW = []
N_FLOW = []
for i in range(n_length):
    P_FLOW.append([])
    N_FLOW.append([])
    
for i in range(n_length):
    for j in range(3):
        x = P_NET[i][j]
        if x == -1:
            P_FLOW[i].append(VDD_cnt)
            VDD_cnt += 1
        elif x == -2:
            P_FLOW[i].append(VSS_cnt)
            VSS_cnt += 1
        else:
            P_FLOW[i].append(NET_cnt[x])
            NET_cnt[x] += 1
    for j in range(3):
        x = N_NET[i][j]
        if x == -1:
            N_FLOW[i].append(VDD_cnt)
            VDD_cnt += 1
        elif x == -2:
            N_FLOW[i].append(VSS_cnt)
            VSS_cnt += 1
        else:
            N_FLOW[i].append(NET_cnt[x])
            NET_cnt[x] += 1
            
    #print(VDD_cnt)
    #print(VSS_cnt)
    #print(NET_cnt)
            
print(P_FLOW)
print(N_FLOW)


# In[36]:


from z3 import *

c = num[0][3]

#cell_num = 2
#x = cell_num-1

###opt = Optimize()

if is_opt:
    opt = Optimize()
else:
    t1 = Tactic("smt")
    opt = t1.solver()

#N = []
#n_length = []
#p_length = []
#pin_length = []
#V = []


V = []                             #first index is z, second index is y, last index is x

#x_col_cnt = (len(this_cell.n) + len(this_cell.p) ) * 3  #assume the number of nmos and pmos is equal 
x_col_cnt = len(this_cell.n) * 3

temp1 = []
for j in range(2):
    temp2 = []
    for i in range(x_col_cnt):
        v_temp = Vertex('super_inner_node', 0, j, i)
        temp2.append(v_temp)
    temp1.append(temp2)
#temp1.append([Vertex('super_outer_node', 0, 0, x_col_cnt)])
temp1.append([Vertex('super_outer_node', 0, 2, 0)])
V.append(temp1)

for i in range(1, metal_num+1):
    temp1 = []
    #for j in range(7):
    for j in range(track_num):
        temp2 = []
        for k in range(x_col_cnt):
            v_type = ''
            if i == 1:
                v_type = 'inner_pin'
            elif i == 2:
                v_type = 'grid'
            elif i == 3:
                if j == 0 or j == track_num-1:
                    v_type = 'outer_pin'      #outer node in M3
                else:
                    v_type = 'grid'
            elif i == 4:
                v_type = 'grid'
                 
            v_temp = Vertex(v_type, i, j, k)
            temp2.append(v_temp)
        temp1.append(temp2)
    V.append(temp1)


# In[37]:


if is_opt:
    opt.set(priority='lex')


# In[ ]:





# In[38]:


for i in range(len(V)):
    for j in range(len(V[i])):
        for k in range(len(V[i][j])):
            V[i][j][k].adj_num = 0
            if i == 0:
                temp = []
                if V[i][j][k].v_type == 'super_inner_node':
                    if j == 0:
                        for t in range(fin_num):
                            temp.append(V[1][t][k])
                    elif j == 1:
                        for t in range(fin_num):
                            temp.append(V[1][t+fin_num+empty_track_num][k])
                    V[i][j][k].adj_num += fin_num
                elif V[i][j][k].v_type == 'super_outer_node':
                    for i1 in range(1, len(V)):
                        #print(i1)
                        for j1 in range(len(V[i1])):
                            for k1 in range(len(V[i1][j1])):
                                if V[i1][j1][k1].v_type == 'outer_pin':
                                    
                                    temp.append(V[i1][j1][k1])
                                    V[i][j][k].adj_num += 1
                V[i][j][k].super_node = temp
                
            elif i == 1:
                if j != 0:
                    V[i][j][k].back = V[i][j-1][k]
                    V[i][j][k].adj_num += 1
                if j != track_num-1:
                    V[i][j][k].front = V[i][j+1][k]
                    V[i][j][k].adj_num += 1
                #if j != 0 and j != track_num-1:
                #    V[i][j][k].up = V[i+1][j][k]
                #    V[i][j][k].adj_num += 1
                V[i][j][k].up = V[i+1][j][k]
                V[i][j][k].adj_num += 1
                if j < fin_num:
                    V[i][j][k].super_node = V[0][0][k]
                    V[i][j][k].adj_num += 1
                    
                    '''if k%3==2 and k!=len(V[i][j])-1:
                        V[i][j][k].right = V[i][j][k+1]
                        V[i][j][k].adj_num += 1
                    if k%3==0 and k !=0:
                        V[i][j][k].left = V[i][j][k-1]
                        V[i][j][k].adj_num += 1'''
                    
                elif j > fin_num + empty_track_num - 1:
                    V[i][j][k].super_node = V[0][1][k]
                    V[i][j][k].adj_num += 1
                    
                    '''if k%3==2 and k!=len(V[i][j])-1:
                        V[i][j][k].right = V[i][j][k+1]
                        V[i][j][k].adj_num += 1
                    if k%3==0 and k !=0:
                        V[i][j][k].left = V[i][j][k-1]
                        V[i][j][k].adj_num += 1'''
            elif i == 2:
                if True:
                #if j != 0 and j != track_num-1:
                    #if V[i][j][k].v_type == 'outer_pin':
                    #    V[i][j][k].super_node = V[0][2][0]
                    #    V[i][j][k].adj_num += 1
                    if k != 0:
                        V[i][j][k].left = V[i][j][k-1]
                        V[i][j][k].adj_num += 1
                    if k != len(V[i][j])-1:
                        V[i][j][k].right = V[i][j][k+1]
                        V[i][j][k].adj_num += 1
                    if metal_num >= 3:
                        V[i][j][k].up = V[i+1][j][k]
                        V[i][j][k].adj_num += 1
                    V[i][j][k].down = V[i-1][j][k]
                    V[i][j][k].adj_num += 1
            elif i == 3:
                if V[i][j][k].v_type == 'outer_pin':
                    V[i][j][k].super_node = V[0][2][0]
                    V[i][j][k].adj_num += 1
                if j != 0:
                    V[i][j][k].back = V[i][j-1][k]
                    V[i][j][k].adj_num += 1
                if j != track_num-1:
                    V[i][j][k].front = V[i][j+1][k]
                    V[i][j][k].adj_num += 1
                
                #if j != 0 and j != track_num-1:
                #    V[i][j][k].down = V[i-1][j][k]
                #    V[i][j][k].up = V[i+1][j][k]
                #    V[i][j][k].adj_num += 2
                
                V[i][j][k].down = V[i-1][j][k]
                V[i][j][k].adj_num += 1
                if metal_num >= 4:
                    V[i][j][k].up = V[i+1][j][k]
                    V[i][j][k].adj_num += 1
            elif i == 4:
                #if j != 0 and j != track_num-1:
                #    if V[i][j][k].v_type == 'outer_pin':
                #        V[i][j][k].super_node = V[0][2][0]
                #        V[i][j][k].adj_num += 1
                #    V[i][j][k].down = V[i-1][j][k]
                #    V[i][j][k].adj_num += 1
                if k != 0:
                    V[i][j][k].left = V[i][j][k-1]
                    V[i][j][k].adj_num += 1
                if k != len(V[i][j])-1:
                    V[i][j][k].right = V[i][j][k+1]
                    V[i][j][k].adj_num += 1
                V[i][j][k].down = V[i-1][j][k]
                V[i][j][k].adj_num += 1


# In[39]:


for i in range(len(V)):
    for j in range(len(V[i])):
        for k in range(len(V[i][j])):
            #V[i][j][k].adj = [V[i][j][k].up, V[i][j][k].down, V[i][j][k].left, V[i][j][k].right, V[i][j][k].front, V[i][j][k].back, V[i][j][k].super_node]
            V[i][j][k].adj = []
            if V[i][j][k].up != 0:
                V[i][j][k].adj.append(['up', V[i][j][k].up])
            if V[i][j][k].down != 0:
                V[i][j][k].adj.append(['down', V[i][j][k].down])
            if V[i][j][k].left != 0:
                V[i][j][k].adj.append(['left', V[i][j][k].left])
            if V[i][j][k].right != 0:
                V[i][j][k].adj.append(['right', V[i][j][k].right])
            if V[i][j][k].front != 0:
                V[i][j][k].adj.append(['front', V[i][j][k].front])
            if V[i][j][k].back != 0:
                V[i][j][k].adj.append(['back', V[i][j][k].back])
            if V[i][j][k].super_node != 0:
                #if type(V[i][j][k].super_node) == list:
                if isinstance(V[i][j][k].super_node, list):
                    #print(len(V[i][j][k].adj))
                    for h in range(len(V[i][j][k].super_node)):
                        V[i][j][k].adj.append(['super_node', V[i][j][k].super_node[h]])
                else:
                    V[i][j][k].adj.append(['super_node', V[i][j][k].super_node])
            
            if V[i][j][k].adj_num != len(V[i][j][k].adj):
                print([i, j, k])
                print([V[i][j][k].adj_num, len(V[i][j][k].adj)])
                print("error")
                
            
print(V[0][2][0].v_type)
#print(V[0][2][0].adj)


# In[40]:


list_cnt = 0
var_list = []



E_list = []
for i in range(len(V)):
    temp4 = []
    for j in range(len(V[i])):
    #for m in range(flow_table[n][0]):
        temp3 = []
        for k in range(len(V[i][j])):
            temp2 = []
            for h in range(V[i][j][k].adj_num):
                temp2.append(-1)
            temp3.append(temp2)
        temp4.append(temp3)
    E_list.append(temp4)
                
E_count = 0

for i in range(len(V)):
    for j in range(len(V[i])):
        for k in range(len(V[i][j])):
            for h in range(V[i][j][k].adj_num):
                i1 = V[i][j][k].adj[h][1].z
                j1 = V[i][j][k].adj[h][1].y
                k1 = V[i][j][k].adj[h][1].x
                #print([i, j, k])
                #print([i1, j1, k1])
                for h1 in range(V[i1][j1][k1].adj_num):
                    if V[i1][j1][k1].adj[h1][1] == V[i][j][k]:
                        if E_list[i][j][k][h] == -1:
                            if E_list[i1][j1][k1][h1] == -1:
                                E_list[i][j][k][h] = E_count
                                E_list[i1][j1][k1][h1] = E_count
                                E_count += 1
                            else:
                                E_list[i][j][k][h] = E_list[i1][j1][k1][h1]
                        else:
                            if E_list[i1][j1][k1][h1] == -1:
                                E_list[i1][j1][k1][h1] = E_list[i][j][k][h]
                            else:
                                if E_list[i1][j1][k1][h1] != E_list[i][j][k][h]:
                                    print("something wrong.....")
 


# In[41]:


min_dis = 2

cell_size = Int('cell_size')
gate_same = Int('gate_same')
df_no_share = Int('no_share')

    
N_COUNT = [ Int('n_count[%s]' %  i) for i in range(n_length) ]
P_COUNT = [ Int('p_count[%s]' %  i) for i in range(p_length) ]


N = [ Int('n[%s]' %  i) for i in range(x_col_cnt) ]
P = [ Int('p[%s]' %  i) for i in range(x_col_cnt) ]
#N = Array('N', IntSort(), IntSort())
#P = Array('P', IntSort(), IntSort())

N_NUM = [ Int('n_num[%s]' %  i) for i in range(x_col_cnt) ]
P_NUM = [ Int('p_num[%s]' %  i) for i in range(x_col_cnt) ]


# In[42]:



#for x in range(cell_num):
#this_cell = cells[x]


for i in range(n_length):
    opt.add(P_COUNT[i] >= 0)
    opt.add(P_COUNT[i] < n_length)
opt.add(Distinct(P_COUNT))
for i in range(n_length):
    for j in range(n_length):
        x = 3*j+1
        opt.add(Implies(P_COUNT[i]==j, And(P[x]==P_NET[i][1], P_NUM[x]==P_FLOW[i][1])))
        opt.add(Implies(P_COUNT[i]==j, Or(And([P[x-1] == P_NET[i][0], P[x+1] == P_NET[i][2], P_NUM[x-1] == P_FLOW[i][0], P_NUM[x+1] == P_FLOW[i][2]]), And([P[x+1] == P_NET[i][0], P[x-1] == P_NET[i][2], P_NUM[x-1] == P_FLOW[i][2], P_NUM[x+1] == P_FLOW[i][0]]))))

    
for i in range(n_length):
    opt.add(N_COUNT[i] >= 0)
    opt.add(N_COUNT[i] < n_length)
opt.add(Distinct(N_COUNT))
for i in range(n_length):
    for j in range(n_length):
        x = 3*j+1
        opt.add(Implies(N_COUNT[i]==j, And(N[x]==N_NET[i][1], N_NUM[x]==N_FLOW[i][1])))
        opt.add(Implies(N_COUNT[i]==j, Or(And([N[x-1] == N_NET[i][0], N[x+1] == N_NET[i][2], N_NUM[x-1] == N_FLOW[i][0], N_NUM[x+1] == N_FLOW[i][2]]), And([N[x+1] == N_NET[i][0], N[x-1] == N_NET[i][2], N_NUM[x-1] == N_FLOW[i][2], N_NUM[x+1] == N_FLOW[i][0]]))))


opt.add(Sum([ If(P[3*i+1]!=N[3*i+1], 1, 0) for i in range(n_length) ]) == gate_same)

opt.add(df_no_share == Sum(Sum([If(P[3*i-1]!=P[3*i], 1, 0)  for i in range(1, p_length)]), Sum([If(N[3*i-1]!=N[3*i], 1, 0)  for i in range(1, n_length)])))


# In[43]:


count = 0
for constraint in opt.assertions():
    #print(simplify(constraint))
    #print((constraint))
    count += 1
print(count)


if is_opt:
    p0 = opt.minimize(df_no_share)
    p1 = opt.minimize(gate_same)
    
#print(opt.check())
#print(opt)
if opt.check() == sat:
    print('sat')
    print(opt.model())    
else:
    print('unsat')
    print (opt.unsat_core())

model = opt.model()


# In[ ]:

p_str = "PMOS: "
for i in range(x_col_cnt):
    #p_str += str(model[P[i]]) + " "
    if model[P[i]] == -1:
        p_str += 'VDD'
    elif model[P[i]] == -2:
        p_str += 'VSS'
    else:
        p_str += str(model[P[i]])
    p_str += " "
print(p_str)

n_str = "NMOS: "
for i in range(x_col_cnt):
    #n_str += str(model[N[i]]) + " "
    if model[N[i]] == -1:
        n_str += 'VDD'
    elif model[N[i]] == -2:
        n_str += 'VSS'
    else:
        n_str += str(model[N[i]])
    n_str += " "
print(n_str)


fp = open("placement.txt", "w")
fp.write(p_str)
fp.write('\n')
fp.write(n_str)
fp.close()

# In[46]:


FLOW = []
for i in range(E_count):
    temp4 = []
    for n in range(len(flow_table)):
        temp0 = []
        for m in range(flow_table[n][0]-1):
            temp0.append(list_cnt)
            list_cnt += 1
        temp4.append(temp0)
    FLOW.append(temp4)
#print(FLOW)

for i in range(E_count):
    for n in range(len(flow_table)):
        for m in range(flow_table[n][0]-1):
            var_list.append(FLOW[i][n][m])

VN = []

for i in range(len(V)):
    temp2 = []
    for j in range(len(V[i])):
        temp1 = []
        for k in range(len(V[i][j])):
            temp0 = []
            for n in range(len(flow_table)):
                temp0.append(list_cnt)
                list_cnt += 1
            temp1.append(temp0)
        temp2.append(temp1)
    VN.append(temp2)
    
for i in range(len(V)):
    for j in range(len(V[i])):
        for k in range(len(V[i][j])):
            for n in range(len(flow_table)):
                var_list.append(VN[i][j][k][n])
    


EN = []

for i in range(E_count):
    temp0 = []
    for n in range(len(flow_table)):
        temp0.append(list_cnt)
        list_cnt += 1
    EN.append(temp0)

for i in range(E_count):
    for n in range(len(flow_table)):
        var_list.append(EN[i][n])


    
M = []

for i in range(E_count):
    M.append(list_cnt)
    list_cnt += 1


#for i in range(E_count):
    var_list.append(M[i])
   #obj_list.append(-1)


obj_list_1 = []
obj_list_4 = []
'''
for i in range(len(V)):
    for j in range(len(V[i])):
        for k in range(len(V[i][j])):
            for h in range(V[i][j][k].adj_num):
                weight = -1
                #if i == 4 and (V[i][j][k].adj[h][0] == 'right' or V[i][j][k].adj[h][0] == 'left'):
                if i == 4:
                    #weight = 4
                    obj_list_4.append((-1) * M[E_list[i][j][k][h]])
                else:
                    if V[i][j][k].adj[h][0] == 'right' or V[i][j][k].adj[h][0] == 'left' or V[i][j][k].adj[h][0] == 'front' or V[i][j][k].adj[h][0] == 'back':
                       #weight = 1
                       obj_list_1.append((-1) * M[E_list[i][j][k][h]])
                    elif V[i][j][k].adj[h][0] == 'up' or V[i][j][k].adj[h][0] == 'down':
                        #weight = 4
                        obj_list_4.append((-1) * M[E_list[i][j][k][h]])
                    elif V[i][j][k].adj[h][0] == 'super_node':
                        #weight = 0
                        continue
                #obj_list[M[E_list[i][j][k][h]]] = weight
                #obj_list[M[E_list[i][j][k][h]]] = weight

'''
   
#for i in obj_list:
#    if i == -1:
#        print("-----problem in obj_list-----")


var_len = len(var_list)

#from lpsolve55 import *
#from lp_solve import *
#from lp_maker import *
from pysat.formula import WCNFPlus
from pysat.formula import WCNF
#wcnf = WCNFPlus()
wcnf = WCNF()

#help(lp_solve)

#for i in range(len(var_list)):
#    wcnf.append([(-1)*var_list[i]], weight = 1)
    #var_list_inv.append((-1)*var_list[i])
#wcnf.append(obj_list_1, weight=1)
#wcnf.append(obj_list_4, weight=4)
#wcnf.append(var_list_inv, weight = 1)




for i in range(len(V)):
    for j in range(len(V[i])):
        for k in range(len(V[i][j])):
            if i==0:
                for n in range(len(flow_table)):
                    if j==1:
                        if model[P[k]]==n:
                            wcnf.append( [VN[i][j][k][n]] )
                            #print((i, j, k, n, VN[i][j][k][n]))

                            
                            for m in range(flow_table[n][0]-1):
                                if model[P_NUM[k]]==0 or model[P_NUM[k]]==m+1:
                                    for h1 in range(V[i][j][k].adj_num - 1):
                                        for h2 in range(h1+1, V[i][j][k].adj_num):
                                            #print(h1, h2)
                                            wcnf.append([(-1)*FLOW[E_list[i][j][k][h1]][n][m], (-1)*FLOW[E_list[i][j][k][h2]][n][m]])
                                    temp = []
                                    for h in range(V[i][j][k].adj_num):
                                        temp.append(FLOW[E_list[i][j][k][h]][n][m])
                                    wcnf.append(temp)
                                    #temp = []
                                    #temp1 = []
                                    #for h in range(V[i][j][k-].adj_num):
                                    #    temp.append(FLOW[E_list[i][j][k][h]][n][m])
                                    #    temp1.append((-1)*FLOW[E_list[i][j][k][h]][n][m])
                                    #wcnf.append([temp, 1], is_atmost = True)
                                    #wcnf.append([temp1, -1], is_atmost = True)
                                else:
                                    for h in range(V[i][j][k].adj_num):
                                        wcnf.append([(-1)*FLOW[E_list[i][j][k][h]][n][m]])

                        else:
                            wcnf.append([(-1)*VN[i][j][k][n]])
                            for m in range(flow_table[n][0]-1):
                                for h in range(V[i][j][k].adj_num):
                                    wcnf.append([(-1)*FLOW[E_list[i][j][k][h]][n][m]])

                    elif j==0:
                        if model[N[k]]==n:
                            wcnf.append([VN[i][j][k][n]])
                            for m in range(flow_table[n][0]-1):
                                if model[N_NUM[k]]==0 or model[N_NUM[k]]==m+1:
                                    for h1 in range(V[i][j][k].adj_num - 1):
                                        for h2 in range(h1+1, V[i][j][k].adj_num):
                                            #continue
                                            wcnf.append( [(-1)*FLOW[E_list[i][j][k][h1]][n][m], (-1)*FLOW[E_list[i][j][k][h2]][n][m]] )
                                    temp = []
                                    for h in range(V[i][j][k].adj_num):
                                        temp.append(FLOW[E_list[i][j][k][h]][n][m])
                                    wcnf.append(temp)
                                    #temp = []
                                    #temp1 = []
                                    #for h in range(V[i][j][k].adj_num):
                                    #    temp.append(FLOW[E_list[i][j][k][h]][n][m])
                                    #    temp1.append((-1)*FLOW[E_list[i][j][k][h]][n][m])
                                    #wcnf.append([temp, 1], is_atmost = True)
                                    #wcnf.append([temp1, -1], is_atmost = True)
                                else:
                                    for h in range(V[i][j][k].adj_num):
                                        wcnf.append( [(-1)*FLOW[E_list[i][j][k][h]][n][m]] ) 
                                        
                        else:
                            wcnf.append([(-1)*VN[i][j][k][n]])
                            for m in range(flow_table[n][0]-1):
                                for h in range(V[i][j][k].adj_num):
                                    wcnf.append([(-1)*FLOW[E_list[i][j][k][h]][n][m]])
                            
                    else:
                        wcnf.append([(-1)*VN[i][j][k][n]])
                        for m in range(flow_table[n][0]-1):
                            for h in range(V[i][j][k].adj_num):
                                wcnf.append([(-1)*FLOW[E_list[i][j][k][h]][n][m]])
                        

            else:
                for n in range(len(flow_table)):
                    for m in range(flow_table[n][0]-1):
                        if V[i][j][k].adj_num == 1:
                            wcnf.append([(-1)*FLOW[E_list[i][j][k][0]][n][m]])
                        
                        elif V[i][j][k].adj_num == 2:
                            wcnf.append( [(-1)*FLOW[E_list[i][j][k][0]][n][m], FLOW[E_list[i][j][k][1]][n][m]] )
                            wcnf.append( [FLOW[E_list[i][j][k][0]][n][m], (-1)*FLOW[E_list[i][j][k][1]][n][m]] )
                        elif V[i][j][k].adj_num == 3:
                            wcnf.append( [(-1)*FLOW[E_list[i][j][k][0]][n][m], (-1)*FLOW[E_list[i][j][k][1]][n][m], (-1)*FLOW[E_list[i][j][k][2]][n][m]] )
                            wcnf.append( [(-1)*FLOW[E_list[i][j][k][0]][n][m], FLOW[E_list[i][j][k][1]][n][m], FLOW[E_list[i][j][k][2]][n][m]] )
                            wcnf.append( [FLOW[E_list[i][j][k][0]][n][m], (-1)*FLOW[E_list[i][j][k][1]][n][m], FLOW[E_list[i][j][k][2]][n][m]] )
                            wcnf.append( [FLOW[E_list[i][j][k][0]][n][m], FLOW[E_list[i][j][k][1]][n][m], (-1)*FLOW[E_list[i][j][k][2]][n][m]] )
                        elif V[i][j][k].adj_num == 4:
                            wcnf.append( [(-1)*FLOW[E_list[i][j][k][0]][n][m], (-1)*FLOW[E_list[i][j][k][1]][n][m], (-1)*FLOW[E_list[i][j][k][2]][n][m]] )
                            wcnf.append( [(-1)*FLOW[E_list[i][j][k][0]][n][m], (-1)*FLOW[E_list[i][j][k][1]][n][m], (-1)*FLOW[E_list[i][j][k][3]][n][m]] )
                            wcnf.append( [(-1)*FLOW[E_list[i][j][k][0]][n][m], FLOW[E_list[i][j][k][1]][n][m], FLOW[E_list[i][j][k][2]][n][m], FLOW[E_list[i][j][k][3]][n][m]] )
                            wcnf.append( [(-1)*FLOW[E_list[i][j][k][0]][n][m], (-1)*FLOW[E_list[i][j][k][2]][n][m], (-1)*FLOW[E_list[i][j][k][3]][n][m]] )
                            wcnf.append( [FLOW[E_list[i][j][k][0]][n][m], (-1)*FLOW[E_list[i][j][k][1]][n][m], FLOW[E_list[i][j][k][2]][n][m], FLOW[E_list[i][j][k][3]][n][m]] )
                            wcnf.append( [FLOW[E_list[i][j][k][0]][n][m], FLOW[E_list[i][j][k][1]][n][m], (-1)*FLOW[E_list[i][j][k][2]][n][m], FLOW[E_list[i][j][k][3]][n][m]] )
                            wcnf.append( [FLOW[E_list[i][j][k][0]][n][m], FLOW[E_list[i][j][k][1]][n][m], FLOW[E_list[i][j][k][2]][n][m], (-1)*FLOW[E_list[i][j][k][3]][n][m]] )
                            wcnf.append( [(-1)*FLOW[E_list[i][j][k][1]][n][m], (-1)*FLOW[E_list[i][j][k][2]][n][m], (-1)*FLOW[E_list[i][j][k][3]][n][m]] )
                        elif V[i][j][k].adj_num == 5:
                            wcnf.append( [(-1)*FLOW[E_list[i][j][k][0]][n][m], (-1)*FLOW[E_list[i][j][k][1]][n][m], (-1)*FLOW[E_list[i][j][k][2]][n][m]] )
                            wcnf.append( [(-1)*FLOW[E_list[i][j][k][0]][n][m], (-1)*FLOW[E_list[i][j][k][1]][n][m], (-1)*FLOW[E_list[i][j][k][3]][n][m]] )
                            wcnf.append( [(-1)*FLOW[E_list[i][j][k][0]][n][m], (-1)*FLOW[E_list[i][j][k][1]][n][m], (-1)*FLOW[E_list[i][j][k][4]][n][m]] )
                            wcnf.append( [(-1)*FLOW[E_list[i][j][k][0]][n][m], FLOW[E_list[i][j][k][1]][n][m], FLOW[E_list[i][j][k][2]][n][m], FLOW[E_list[i][j][k][3]][n][m], FLOW[E_list[i][j][k][4]][n][m]] )
                            wcnf.append( [(-1)*FLOW[E_list[i][j][k][0]][n][m], (-1)*FLOW[E_list[i][j][k][2]][n][m], (-1)*FLOW[E_list[i][j][k][3]][n][m]] )
                            wcnf.append( [(-1)*FLOW[E_list[i][j][k][0]][n][m], (-1)*FLOW[E_list[i][j][k][2]][n][m], (-1)*FLOW[E_list[i][j][k][4]][n][m]] )
                            wcnf.append( [(-1)*FLOW[E_list[i][j][k][0]][n][m], (-1)*FLOW[E_list[i][j][k][3]][n][m], (-1)*FLOW[E_list[i][j][k][4]][n][m]] )
                            wcnf.append( [FLOW[E_list[i][j][k][0]][n][m], (-1)*FLOW[E_list[i][j][k][1]][n][m], FLOW[E_list[i][j][k][2]][n][m], FLOW[E_list[i][j][k][3]][n][m], FLOW[E_list[i][j][k][4]][n][m]] )
                            wcnf.append( [FLOW[E_list[i][j][k][0]][n][m], FLOW[E_list[i][j][k][1]][n][m], (-1)*FLOW[E_list[i][j][k][2]][n][m], FLOW[E_list[i][j][k][3]][n][m], FLOW[E_list[i][j][k][4]][n][m]] )
                            wcnf.append( [FLOW[E_list[i][j][k][0]][n][m], FLOW[E_list[i][j][k][1]][n][m], FLOW[E_list[i][j][k][2]][n][m], (-1)*FLOW[E_list[i][j][k][3]][n][m], FLOW[E_list[i][j][k][4]][n][m]] )
                            wcnf.append( [FLOW[E_list[i][j][k][0]][n][m], FLOW[E_list[i][j][k][1]][n][m], FLOW[E_list[i][j][k][2]][n][m], FLOW[E_list[i][j][k][3]][n][m], (-1)*FLOW[E_list[i][j][k][4]][n][m]] )
                            wcnf.append( [(-1)*FLOW[E_list[i][j][k][1]][n][m], (-1)*FLOW[E_list[i][j][k][2]][n][m], (-1)*FLOW[E_list[i][j][k][3]][n][m]] )
                            wcnf.append( [(-1)*FLOW[E_list[i][j][k][1]][n][m], (-1)*FLOW[E_list[i][j][k][2]][n][m], (-1)*FLOW[E_list[i][j][k][4]][n][m]] )
                            wcnf.append( [(-1)*FLOW[E_list[i][j][k][1]][n][m], (-1)*FLOW[E_list[i][j][k][3]][n][m], (-1)*FLOW[E_list[i][j][k][4]][n][m]] )
                            wcnf.append( [(-1)*FLOW[E_list[i][j][k][2]][n][m], (-1)*FLOW[E_list[i][j][k][3]][n][m], (-1)*FLOW[E_list[i][j][k][4]][n][m]] )
                
                for n in range(len(flow_table)):
                    temp = []
                    #temp_inv = []    
                    temp.append((-1)*VN[i][j][k][n])
                    #temp_inv.append((-1)*VN[i][j][k][n])
                    for h in range(V[i][j][k].adj_num):
                        temp.append(EN[E_list[i][j][k][h]][n])
                        wcnf.append( [VN[i][j][k][n], (-1)*EN[E_list[i][j][k][h]][n]])
                    wcnf.append(temp)
                    #wcnf.append(temp_inv)
                            
                if i==1:
                    #if j==4 or j==5:
                    if j==4:
                        for n in range(len(flow_table)):
                            if model[P[k]]==n:  
                                wcnf.append( [VN[i][j][k][n], VN[i][j+1][k][n]] )      
                                wcnf.append( [(-1)*VN[i][j][k][n], (-1)*VN[i][j+1][k][n]] )                      
                                #wcnf.append([[VN[i][j][k][n], VN[i][j+1][k][n]], 1], is_atmost = True)
                                #wcnf.append([[(-1)*VN[i][j][k][n], (-1)*VN[i][j+1][k][n]], -1], is_atmost = True)
                            else:
                                ###opt.add( Not(Or(VN[i][j][k][n], VN[i][j+1][k][n])) )
                                wcnf.append([(-1)*VN[i][j][k][n]])
                                wcnf.append([(-1)*VN[i][j+1][k][n]])
                                #upper_bound[VN[i][j][k][n]] = 0
                                #upper_bound[VN[i][j+1][k][n]] = 0

                    #elif j==0 or j==1:
                    elif j==0:
                        for n in range(len(flow_table)):
                            if model[N[k]]==n:
                                wcnf.append( [VN[i][j][k][n], VN[i][j+1][k][n]] )      
                                wcnf.append( [(-1)*VN[i][j][k][n], (-1)*VN[i][j+1][k][n]] ) 
                                #wcnf.append([[VN[i][j][k][n], VN[i][j+1][k][n]], 1], is_atmost = True)
                                #wcnf.append([[(-1)*VN[i][j][k][n], (-1)*VN[i][j+1][k][n]], -1], is_atmost = True)
                            else:
                                ###opt.add( Not(Or(VN[i][j][k][n], VN[i][j+1][k][n])) )
                                wcnf.append([(-1)*VN[i][j][k][n]])
                                wcnf.append([(-1)*VN[i][j+1][k][n]])
                                #upper_bound[VN[i][j][k][n]] = 0
                                #upper_bound[VN[i][j+1][k][n]] = 0
#---------------------------------------------------------------------------------------------------------------------------------------
                    #else:
                        #opt.add(Sum([If(VN[i][j][k][n], 1, 0)  for n in range(len(flow_table)) ]) <= 1)
                    elif j==2 or j==3:
                        for n1 in range(len(flow_table) - 1):
                            for n2 in range(n1+1, len(flow_table)):
                                wcnf.append( [(-1)*VN[i][j][k][n1], (-1)*VN[i][j][k][n2]] )
                        #temp = []
                        #for n in range(len(flow_table)):
                        #    temp.append(VN[i][j][k][n])
                        #wcnf.append([temp, 1], is_atmost = True)

                else:
                    for n1 in range(len(flow_table) - 1):
                        for n2 in range(n1+1, len(flow_table)):
                            wcnf.append( [(-1)*VN[i][j][k][n1], (-1)*VN[i][j][k][n2]] )
                    #temp = []
                    #for n in range(len(flow_table)):
                    #    temp.append(VN[i][j][k][n])
                    #wcnf.append([temp, 1], is_atmost = True)
                



for i in range(E_count):
    temp = []
    #temp1 = []
    for n in range(len(flow_table)):
        for m in range(flow_table[n][0]-1):
            wcnf.append( [(-1)*FLOW[i][n][m], EN[i][n]] )

        temp.append(EN[i][n])
    temp.append((-1)*M[i])

    for j1 in range(len(temp) - 1):
        for j2 in range(j1+1, len(temp)):
            wcnf.append( [(-1)*temp[j1], (-1)*temp[j2]] )

    wcnf.append(temp)
    

wcnf.to_file('pysat_test.wcnf')
