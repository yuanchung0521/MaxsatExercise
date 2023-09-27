import pysat

#path = './pysat_data'
#pysat.params['data_dirs'] = path


file_name = 'A2O1A1Ixp33_ASAP7_75t_R.txt'
# file_name = 'placement.txt'
cell_num_sel = 7
cell_count_number = 1
is_opt = True
bool_flag = True
import time

metal_num = 3

now = time.ctime()

print(now)

P = []
N = []
P_NUM = []
N_NUM = []

net_name = []
net_count = []
with open(file_name) as f:
    lines = f.readlines()
    
    line = lines[0].strip().replace("\n","")
    words = lines[0].strip().replace("\n","").split()
    #cell_num_sel = (len(words) - 1) / 3
    cell_num_sel = (len(words)) / 3
    for j in range(1, len(words)):
        net = words[j]
        if net == 'VDD' or net == 'VSS':
            P.append(-1)
            P_NUM.append(-1)
        else:
            if net not in net_name:
                net_name.append(net)
                P.append(net_name.index(net))
                P_NUM.append(0)
                net_count.append(0)
            else:
                num = net_name.index(net)
                P.append(num)
                net_count[num] += 1
                P_NUM.append(net_count[num])
                
                
            
    line = lines[1].strip().replace("\n","")
    words = lines[1].strip().replace("\n","").split()
    for j in range(1, len(words)):
        net = words[j]
        if net == 'VDD' or net == 'VSS':
            N.append(-1)
            N_NUM.append(-1)
        else:
            if net not in net_name:
                net_name.append(net)
                N.append(net_name.index(net))
                N_NUM.append(0)
                net_count.append(0)
            else:
                num = net_name.index(net)
                N.append(num)
                net_count[num] += 1
                N_NUM.append(net_count[num])
            

EX = ["dummy"]
for i in range(len(net_count)):
    if net_count[i] == 0:
        EX.append(net_name[i])
P = []
N = []
P_NUM = []
N_NUM = []

net_name = []
net_count = []
with open(file_name) as f:
    lines = f.readlines()
    
    line = lines[0].strip().replace("\n","")
    words = lines[0].strip().replace("\n","").split()
    #cell_num_sel = (len(words) - 1) / 3
    cell_num_sel = (len(words)) / 3
    for j in range(1, len(words)):
        net = words[j]
        #if net == 'VDD' or net == 'VSS' or net in EX:
        if net == 'VDD' or net == 'VSS':
            P.append(-1)
            P_NUM.append(-1)
        elif net in EX:
            P.append(-2)
            P_NUM.append(-2)
        else:
            if net not in net_name:
                net_name.append(net)
                P.append(net_name.index(net))
                P_NUM.append(0)
                net_count.append(0)
            else:
                num = net_name.index(net)
                P.append(num)
                net_count[num] += 1
                P_NUM.append(net_count[num])
                
                
            
    line = lines[1].strip().replace("\n","")
    words = lines[1].strip().replace("\n","").split()
    for j in range(1, len(words)):
        net = words[j]
        #if net == 'VDD' or net == 'VSS' or net in EX:
        if net == 'VDD' or net == 'VSS':
            N.append(-1)
            N_NUM.append(-1)
        elif net in EX:
            N.append(-2)
            N_NUM.append(-2)
        else:
            if net not in net_name:
                net_name.append(net)
                N.append(net_name.index(net))
                N_NUM.append(0)
                net_count.append(0)
            else:
                num = net_name.index(net)
                N.append(num)
                net_count[num] += 1
                N_NUM.append(net_count[num])

for i in range(len(net_count)):
    net_count[i] += 1 # why?
    
    
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
        
    
fin_num = 2
empty_track_num = 2
track_num = 2 * fin_num + empty_track_num

print(P)
print(N)

flow_table = []


V = []                             #first index is z, second index is y, last index is x

#x_col_cnt = (len(this_cell.n) + len(this_cell.p) ) * 3  #assume the number of nmos and pmos is equal
x_col_cnt = int(cell_num_sel) * 3

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
                
list_cnt = 1
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
                                    

FLOW = []
for i in range(E_count):
    temp4 = []
    for n in range(len(net_name)):
        temp0 = []
        for m in range(net_count[n]-1):
            temp0.append(list_cnt)
            list_cnt += 1
        temp4.append(temp0)
    FLOW.append(temp4)
#print(FLOW)

for i in range(E_count):
    for n in range(len(net_name)):
        for m in range(net_count[n]-1):
            var_list.append(FLOW[i][n][m])

VN = []

for i in range(len(V)):
    temp2 = []
    for j in range(len(V[i])):
        temp1 = []
        for k in range(len(V[i][j])):
            temp0 = []
            for n in range(len(net_name)):
                temp0.append(list_cnt)
                list_cnt += 1
            temp1.append(temp0)
        temp2.append(temp1)
    VN.append(temp2)
    
for i in range(len(V)):
    for j in range(len(V[i])):
        for k in range(len(V[i][j])):
            for n in range(len(net_name)):
                var_list.append(VN[i][j][k][n])
    


EN = []

for i in range(E_count):
    temp0 = []
    for n in range(len(net_name)):
        temp0.append(list_cnt)
        list_cnt += 1
    EN.append(temp0)

for i in range(E_count):
    for n in range(len(net_name)):
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

var_list_inv = []
for i in range(len(var_list)):
    wcnf.append([(-1)*var_list[i]], weight = 1)
    #var_list_inv.append((-1)*var_list[i])
#wcnf.append(obj_list_1, weight=1)
#wcnf.append(obj_list_4, weight=4)
#wcnf.append(var_list_inv, weight = 1)



for i in range(len(V)):
    for j in range(len(V[i])):
        for k in range(len(V[i][j])):
            if i==0:
                for n in range(len(net_name)):
                    if j==1:
                        if P[k]==n:
                            wcnf.append( [VN[i][j][k][n]] )
                            #print((i, j, k, n, VN[i][j][k][n]))

                            
                            for m in range(net_count[n]-1):
                                if P_NUM[k]==0 or P_NUM[k]==m+1:
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
                            for m in range(net_count[n]-1):
                                for h in range(V[i][j][k].adj_num):
                                    wcnf.append([(-1)*FLOW[E_list[i][j][k][h]][n][m]])

                    elif j==0:
                        if N[k]==n:
                            wcnf.append([VN[i][j][k][n]])
                            for m in range(net_count[n]-1):
                                if N_NUM[k]==0 or N_NUM[k]==m+1:
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
                            for m in range(net_count[n]-1):
                                for h in range(V[i][j][k].adj_num):
                                    wcnf.append([(-1)*FLOW[E_list[i][j][k][h]][n][m]])
                            
                    else:
                        wcnf.append([(-1)*VN[i][j][k][n]])
                        for m in range(net_count[n]-1):
                            for h in range(V[i][j][k].adj_num):
                                wcnf.append([(-1)*FLOW[E_list[i][j][k][h]][n][m]])
                        

            else:
                for n in range(len(net_name)):
                    for m in range(net_count[n]-1):
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
                
                for n in range(len(net_name)):
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
                        for n in range(len(net_name)):
                            if P[k]==n:  
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
                        for n in range(len(net_name)):
                            if N[k]==n:
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
                        for n1 in range(len(net_name) - 1):
                            for n2 in range(n1+1, len(net_name)):
                                wcnf.append( [(-1)*VN[i][j][k][n1], (-1)*VN[i][j][k][n2]] )
                        #temp = []
                        #for n in range(len(net_name)):
                        #    temp.append(VN[i][j][k][n])
                        #wcnf.append([temp, 1], is_atmost = True)

                else:
                    for n1 in range(len(net_name) - 1):
                        for n2 in range(n1+1, len(net_name)):
                            wcnf.append( [(-1)*VN[i][j][k][n1], (-1)*VN[i][j][k][n2]] )
                    #temp = []
                    #for n in range(len(net_name)):
                    #    temp.append(VN[i][j][k][n])
                    #wcnf.append([temp, 1], is_atmost = True)
                



for i in range(E_count):
    temp = []
    #temp1 = []
    for n in range(len(net_name)):
        for m in range(net_count[n]-1):
            wcnf.append( [(-1)*FLOW[i][n][m], EN[i][n]] )

        temp.append(EN[i][n])
    temp.append((-1)*M[i])

    for j1 in range(len(temp) - 1):
        for j2 in range(j1+1, len(temp)):
            wcnf.append( [(-1)*temp[j1], (-1)*temp[j2]] )

    wcnf.append(temp)
    

wcnf.to_file('pysat_test.wcnf')
