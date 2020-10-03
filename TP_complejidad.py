import pygame
import time
import random
import sys
import heapq
# set up pygame window
WIDTH = 700
HEIGHT = 650

# Define colours
WHITE = (255, 255, 255)
GREEN = (0, 255, 0,)
BLUE = (0, 0, 255)
YELLOW = (255 ,255 ,0)
RED=(255,0,0)
MAGNETA=(255,0,255)
# initalise Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quoridor")

grid = []   #se guarda las coordenadas de los nodos principalmente lo uso para dibujar
tablas_h=[]     #se guarda un arreglo de 64 rectangulos horizontales totales
tablas_v=[]     #se guarda un arreglo de 64 rectangulos verticales totales
tablas_h_p=[None]*64    #se guarda un arreglo de rectangulos que se pusieron por el jugador
tablas_v_p=[None]*64    #se guarda un arreglo de rectangulos que se pusieron por el jugador

# hacemos que cada nodo tenga sus coordenadas, y guardamos 64 rectangulos horizontalees y verticales en sus dos arreglos
def build_grid(x, y, w):
    for i in range(1,10):
        x = 80                                                           
        y = y + 60                                                       
        for j in range(1, 10):
            pygame.draw.rect(screen, WHITE, (x , y, w, w), 0)
            if j!=9 and len(tablas_h)<64:
                a=pygame.Rect(x, y+40,100,20)
                b=pygame.Rect(x+40, y,20,100)
                tablas_h.append(a)
                tablas_v.append(b)
            if len(grid)<81:
                grid.append([x,y])                                           
            x = x + 60                                                   

###############
############### bot 1
###########33
#creamos una clase nodo para cada cuadro blanco
class Node:

    def __init__(self, name):
           self.name = name
           self.visited = False
           self.adjacenciesList = []
           self.predecessor = None
           self.mindistance = sys.maxsize    
    def __lt__(self, other):
           return self.mindistance < other.mindistance

#arista clase
class Edge:

       def __init__(self, weight, startvertex, endvertex):
           self.weight = weight
           self.startvertex = startvertex
           self.endvertex = endvertex

#
def calculateshortestpath(startvertex):
       q = []
       startvertex.mindistance = 0
       heapq.heappush(q, startvertex)

       while q:
           actualnode = heapq.heappop(q)
           for edge in actualnode.adjacenciesList:
               tempdist = edge.startvertex.mindistance + edge.weight
               if tempdist < edge.endvertex.mindistance:
                   edge.endvertex.mindistance = tempdist
                   edge.endvertex.predecessor = edge.startvertex
                   heapq.heappush(q,edge.endvertex)

def getshortestpath(targetvertex):
       print("La distancia mas corta recorrida: ",targetvertex.mindistance)
       node = targetvertex
       sig_paso=node.predecessor.name
       while node:
           print(node.name)
           node = node.predecessor
       return sig_paso
##############################3
#llamamos la funcion de arriba para darle todos los valores a los arreglos tablas y grid
build_grid(0, 0, 40)
#creamos nodos vacios
arrayNodes = [None]*81
for i in range(81):
    arrayNodes[i] = Node(i)
###############
#creamos aristas con los nodos cercanos como arriba, abajo, izquierda y derecha
for i in range(81):
    if i >= 1 and i <= 7:                                                 # 3 aristas
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i-1]))
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i+1]))
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i+9]))
    elif i >= 73 and i <= 79:                                             # 3 aristas
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i-1]))
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i+1]))
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i-9]))
        
    elif i >= 9 and i <= 63 and i % 9 == 0:                               # 3 aristas
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i-9]))
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i+1]))
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i+9]))
    elif i >= 17 and i <= 71 and (i + 1) % 9 == 0:                        # 3 aristas
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i-9]))
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i-1]))
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i+9]))
    elif i != 0 and i != 8 and i != 72 and i != 80:                       # 4 aristas
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i-9]))
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i-1]))
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i+1]))
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i+9]))
    elif i == 0:                                                          # 2 aristas
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i+9]))
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i+1]))
    elif i == 8:
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i+9]))
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i-1]))
    elif i == 72:
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i-9]))
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i+1]))
    elif i == 80:
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i-9]))
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i-1]))
        
#usamos para actualizar vaciando estos valores y poder segir usando esta funcion "calculateshortestpath()"
def update():
    for i in range(81):
        arrayNodes[i].predecessor = None
        arrayNodes[i].mindistance = sys.maxsize

def movbot1(x1_y1,turno,www):
    #en resumen de esta parte es que halla todos los recorridos con los nodos de la ultima fila
    #para hallar el camino más optimo por donde ir 
    #recalcando es nuestro codigo no sabemos hacer que el bot ponga paredes solo se mueva
    #y tambien el salto en diagonal ya que era muy complicado
    calculateshortestpath(arrayNodes[8])   
    a_min=arrayNodes[x1_y1].mindistance
    x_y_aux_min=8
    for i in range(2,10):
        update()
        calculateshortestpath(arrayNodes[(i*9)-1])
        if(a_min>=arrayNodes[x1_y1].mindistance):
            a_min=arrayNodes[x1_y1].mindistance
            x_y_aux_min=(i*9)-1
    
    if www==True:
        update()
        calculateshortestpath(arrayNodes[x_y_aux_min]) 
        x1_y1=getshortestpath(arrayNodes[x1_y1])
        for i in range(1,10):
            if(x1_y1==(i*9)-1):
                www=False
                break;
    turno=3
    ###############

    return turno,www,x1_y1
######################################3
######################################
##################################
#############tablas
#hacemos que mediante el x_table obtengamos la posicion del nodo que le corresponde a esa tabla
#cada nodo tiene siempre 2 tablas(horizontal y vertical) excepto la ultima fila inferior y la ultima columna de la derecha
def obtener_tabla_a_nodo(x_tabla):

    if x_tabla>=0 and x_tabla<=7:
        x_nodo=x_tabla
    elif x_tabla>=8 and x_tabla<=15:
        x_nodo=x_tabla+1
    elif x_tabla>=16 and x_tabla<=23:
        x_nodo=x_tabla+2
    elif x_tabla>=24 and x_tabla<=31:
        x_nodo=x_tabla+3
    elif x_tabla>=32 and x_tabla<=39:
        x_nodo=x_tabla+4
    elif x_tabla>=40 and x_tabla<=47:
        x_nodo=x_tabla+5
    elif x_tabla>=48 and x_tabla<=55:
        x_nodo=x_tabla+6
    elif x_tabla>=56 and x_tabla<=63:
        x_nodo=x_tabla+7
    return x_nodo

#hacemos que al tener la coordenada de la tabla_horizontal rompa la arista con los nodos que le corresponda eliminar 
#ej:28 29   ->elimna la conexion del nodo 28 con 37 y el 29 con 38
#   37 38
def romper_aristas_tabla_hori(x_tabla):
    
    x_nodo=obtener_tabla_a_nodo(x_tabla)

    for i in range(len(arrayNodes[x_nodo].adjacenciesList)):
        if arrayNodes[x_nodo].adjacenciesList[i].endvertex.name == x_nodo+9:
            arrayNodes[x_nodo].adjacenciesList.pop(i)
            break
    for i in range(len(arrayNodes[x_nodo+9].adjacenciesList)):
        if arrayNodes[x_nodo+9].adjacenciesList[i].endvertex.name == x_nodo:
            arrayNodes[x_nodo+9].adjacenciesList.pop(i)
            break
        
    for i in range(len(arrayNodes[x_nodo+1].adjacenciesList)):
        if arrayNodes[x_nodo+1].adjacenciesList[i].endvertex.name == x_nodo+10:
            arrayNodes[x_nodo+1].adjacenciesList.pop(i)
            break
    for i in range(len(arrayNodes[x_nodo+10].adjacenciesList)):
        if arrayNodes[x_nodo+10].adjacenciesList[i].endvertex.name == x_nodo+1:
            arrayNodes[x_nodo+10].adjacenciesList.pop(i)
            break

#hacemos que al tener la coordenada de la tabla_vertical rompa la arista con los nodos que le corresponda eliminar 
#ej:28 29   ->elimna la conexion del nodo 28 con 29 y el 37 con 38
#   37 38
def romper_aristas_tabla_verti(x_tabla):

    x_nodo=obtener_tabla_a_nodo(x_tabla)

    for i in range(len(arrayNodes[x_nodo].adjacenciesList)):
        if arrayNodes[x_nodo].adjacenciesList[i].endvertex.name == x_nodo+1:
            arrayNodes[x_nodo].adjacenciesList.pop(i)
            break
    for i in range(len(arrayNodes[x_nodo+1].adjacenciesList)):
        if arrayNodes[x_nodo+1].adjacenciesList[i].endvertex.name == x_nodo:
            arrayNodes[x_nodo+1].adjacenciesList.pop(i)
            break
        
    for i in range(len(arrayNodes[x_nodo+9].adjacenciesList)):
        if arrayNodes[x_nodo+9].adjacenciesList[i].endvertex.name == x_nodo+10:
            arrayNodes[x_nodo+9].adjacenciesList.pop(i)
            break
    for i in range(len(arrayNodes[x_nodo+10].adjacenciesList)):
        if arrayNodes[x_nodo+10].adjacenciesList[i].endvertex.name == x_nodo+9:
            arrayNodes[x_nodo+10].adjacenciesList.pop(i)
            break

def dibujar_tablas_general(tablas_h_p,tablas_v_p):
    for i in range(64):
        if tablas_h_p[i]!=None:
            pygame.draw.rect(screen, YELLOW, tablas_h_p[i], 0)
        if tablas_v_p[i]!=None:
            pygame.draw.rect(screen, YELLOW, tablas_v_p[i], 0)

#arregla las aristas que elimino antes tan solo lo uso para ver que no se le puede encerrar al bot
def arreglar_pared_hori(x_tabla):
    
    x_nodo=obtener_tabla_a_nodo(x_tabla)

    arrayNodes[x_nodo].adjacenciesList.append(Edge(1,arrayNodes[x_nodo],arrayNodes[x_nodo+9]))
    arrayNodes[x_nodo+1].adjacenciesList.append(Edge(1,arrayNodes[x_nodo+1],arrayNodes[x_nodo+10]))
    arrayNodes[x_nodo+9].adjacenciesList.append(Edge(1,arrayNodes[x_nodo+9],arrayNodes[x_nodo]))
    arrayNodes[x_nodo+10].adjacenciesList.append(Edge(1,arrayNodes[x_nodo+10],arrayNodes[x_nodo+1]))

#arregla las aristas que elimino antes tan solo lo uso para ver que no se le puede encerrar al bot
def arreglar_pared_verti(x_tabla):
    
    x_nodo=obtener_tabla_a_nodo(x_tabla)

    arrayNodes[x_nodo].adjacenciesList.append(Edge(1,arrayNodes[x_nodo],arrayNodes[x_nodo+1]))
    arrayNodes[x_nodo+1].adjacenciesList.append(Edge(1,arrayNodes[x_nodo+1],arrayNodes[x_nodo]))
    arrayNodes[x_nodo+9].adjacenciesList.append(Edge(1,arrayNodes[x_nodo+9],arrayNodes[x_nodo+10]))
    arrayNodes[x_nodo+10].adjacenciesList.append(Edge(1,arrayNodes[x_nodo+10],arrayNodes[x_nodo+9]))
####################
####################
#####################
def confirmar_movimiento(x2_y2,x_y_bot,movimiento,relac_x_y_bot_x2_y2,sig_pos,bloque_ariba,bloque_abajo,bloque_izquierda,bloque_derecha):
    for j in range(len(arrayNodes[x2_y2].adjacenciesList)):
        if arrayNodes[x2_y2].adjacenciesList[j].endvertex.name == x_y_bot:
            relac_x_y_bot_x2_y2=True

    #calculamos por separado que recorrado todas las arista y busca si existe conexion con sus nodos cercanos
    for p in range(len(arrayNodes[x_y_bot].adjacenciesList)):
        if arrayNodes[x_y_bot].adjacenciesList[p].endvertex.name == x_y_bot-9:
            bloque_ariba=False
        if arrayNodes[x_y_bot].adjacenciesList[p].endvertex.name == x_y_bot+9:
            bloque_abajo=False
        if arrayNodes[x_y_bot].adjacenciesList[p].endvertex.name == x_y_bot-1:
            bloque_izquierda=False
        if arrayNodes[x_y_bot].adjacenciesList[p].endvertex.name == x_y_bot+1:
            bloque_derecha=False

    #recorremos todas la aristas de la posicion del bot para ver si puede realizar un doble salto, o salto en diagonal
    #cuando esta alcostado del bot
    for i in range(len(arrayNodes[x_y_bot].adjacenciesList)):

        if relac_x_y_bot_x2_y2==True and  arrayNodes[x_y_bot].adjacenciesList[i].endvertex.name ==sig_pos:

            #revisamos si puede realizar el doble salto
            if(x2_y2==sig_pos+18):
                movimiento=True
                break
            if(x2_y2==sig_pos-18):
                movimiento=True
                break
            if(x2_y2==sig_pos-2):
                movimiento=True
                break
            if(x2_y2==sig_pos+2):
                movimiento=True
                break

            #revisamos si hay un bloque que impida el doble salto y que se pueda ir en diagonal del jugador
            if((sig_pos+1==x_y_bot or sig_pos-1==x_y_bot) and (bloque_ariba==True) and (x2_y2-9==x_y_bot)):
                movimiento=True
                break
            if((sig_pos+1==x_y_bot or sig_pos-1==x_y_bot) and (bloque_abajo==True) and (x2_y2+9==x_y_bot)):
                movimiento=True
                break
            if((sig_pos+9==x_y_bot or sig_pos-9==x_y_bot)  and (bloque_izquierda==True) and (x2_y2-1==x_y_bot)):
                movimiento=True
                break
            if((sig_pos+9==x_y_bot or sig_pos-9==x_y_bot)  and (bloque_derecha==True) and (x2_y2+1==x_y_bot)):
                movimiento=True
                break

    #recorro otra vez las arista del x2_y2 si puede moverse para arriba, abajo, izquierda, derecha
    for l in range(len(arrayNodes[x2_y2].adjacenciesList)):

        if arrayNodes[x2_y2].adjacenciesList[l].endvertex.name == sig_pos and arrayNodes[x2_y2].adjacenciesList[l].endvertex.name != x_y_bot:
            movimiento=True
            break
    return movimiento



#aca se crea el movimiento del jugador 
def mov_jugador(x,y,x2_y2,x3_y3,turno,x1_y1):

    encontro=False
    movimiento=False

    #mediante el click del mouse sacamos la coordenada del nodo que le corresponde si existe en dicho caso
    for i in range(81):
        if x>=grid[i][0] and x<=grid[i][0]+40 and y>=grid[i][1] and y<=grid[i][1]+40:
            sig_pos=i       #es la coordenada del nodo mediante el mouse click
            encontro=True   #encuentra la posicion del nodo que le corresponde
            break

    #primero creo un if que en caso si encontro el nodo que le corresponde al click
    if encontro==True:
        #calculamos si o no existe una arista que conecte al nodo del jugador y el bot
        movimiento=confirmar_movimiento(x2_y2,x1_y1,movimiento,False,sig_pos,True,True,True,True)
        if(movimiento==False):
            movimiento=confirmar_movimiento(x2_y2,x3_y3,movimiento,False,sig_pos,True,True,True,True)
    #y si se puede mover se va a la posicion del nodo donde se dio click y acabo el turno del jugador
    if(movimiento==True):
        x2_y2 = sig_pos
        turno=2

    return x2_y2,turno

#busca si cuando pones tabla encierras al jugador o bot
def encerrado_por_tabla(x1_y1,x2_y2,x3_y3,i,tipo):
    if(tipo=='h'):
        romper_aristas_tabla_hori(i)
    elif(tipo=='v'):
        romper_aristas_tabla_verti(i)
    calculateshortestpath(arrayNodes[72])
    a_min_bot1=arrayNodes[x1_y1].mindistance
    update()
    calculateshortestpath(arrayNodes[72])
    a_min_bot2=arrayNodes[x3_y3].mindistance
    update()
    calculateshortestpath(arrayNodes[72])
    a_min_jug=arrayNodes[x2_y2].mindistance
    update()
    # a_min>=1000 si pasa esto es que el bot no pudo encontrar ni un solo camino a la vez que impide poner una pared ahi
    if(a_min_bot1>=1000 or a_min_jug>=1000 or a_min_bot2>=1000):
        encerrado=True
    else:
        encerrado=False
    return encerrado

#hace que se pueda poner tabla o no
def poner_tablas_jugador(x,y,turno,x1_y1,x2_y2,x3_y3,cant_tabla_jugador):

    encerrado=False
    for i in range(64):

        #uso in if que para poner la tabla horizontal que debe cumplir que no puede encerrar al bot y saca la posicion del click para poner tabla
        if x>=tablas_h[i].x and x<=tablas_h[i].x+40 and y>=tablas_h[i].y and y<=tablas_h[i].y+20 and tablas_h_p[i]==None and tablas_h_p[i+1]==None and cant_tabla_jugador!=0 and tablas_v_p[i]==None:
           
             encerrado=encerrado_por_tabla(x1_y1,x2_y2,x3_y3,i,'h')

             if(encerrado==False):
                 tablas_h_p[i]=tablas_h[i]
                 turno=2
                 cant_tabla_jugador-=1
                 ###
                 remove_aris_bot2(arrayNodes_bot2,obtener_tabla_a_nodo(i),obtener_tabla_a_nodo(i)+9)
                 remove_aris_bot2(arrayNodes_bot2,obtener_tabla_a_nodo(i)+1,obtener_tabla_a_nodo(i)+10)
             else:
                 arreglar_pared_hori(i)
             break

        #casi lo mismo que el horizontal pero en vertical
        if x>=tablas_v[i].x and x<=tablas_v[i].x+20 and y>=tablas_v[i].y and y<=tablas_v[i].y+40 and tablas_v_p[i]==None and tablas_v_p[i-8]==None and cant_tabla_jugador!=0 and tablas_h_p[i]==None:
            
            encerrado=encerrado_por_tabla(x1_y1,x2_y2,x3_y3,i,'v')

            if(encerrado==False):
                tablas_v_p[i]=tablas_v[i]
                turno=2
                cant_tabla_jugador-=1
                #####
                remove_aris_bot2(arrayNodes_bot2,obtener_tabla_a_nodo(i),obtener_tabla_a_nodo(i)+1)
                remove_aris_bot2(arrayNodes_bot2,obtener_tabla_a_nodo(i)+9,obtener_tabla_a_nodo(i)+10)
            else:
                arreglar_pared_verti(i)
            break

    return turno,cant_tabla_jugador

 ###############################
 ###############################
 ############################### bot 2
 ###############################
 ###############################
arrayNodes_bot2 = [[] for i in range(81)]

for i in range(81):
    if i >= 1 and i <= 7:                                                 # 3 aristas
        arrayNodes_bot2[i].append(i+9)
        arrayNodes_bot2[i].append(i+1)
        arrayNodes_bot2[i].append(i-1)
    elif i >= 73 and i <= 79:                                             # 3 aristas
        arrayNodes_bot2[i].append(i+1)
        arrayNodes_bot2[i].append(i-1)
        arrayNodes_bot2[i].append(i-9)
        
    elif i >= 9 and i <= 63 and i % 9 == 0:                               # 3 aristas
        arrayNodes_bot2[i].append(i+9)
        arrayNodes_bot2[i].append(i+1)
        arrayNodes_bot2[i].append(i-9)
        
        
    elif i >= 17 and i <= 71 and (i + 1) % 9 == 0:                        # 3 aristas
        arrayNodes_bot2[i].append(i+9)
        arrayNodes_bot2[i].append(i-1)
        arrayNodes_bot2[i].append(i-9)

    elif i != 0 and i != 8 and i != 72 and i != 80:                       # 4 aristas
        arrayNodes_bot2[i].append(i+9)
        arrayNodes_bot2[i].append(i+1)
        arrayNodes_bot2[i].append(i-1)
        arrayNodes_bot2[i].append(i-9)  
    elif i == 0:                                                          # 2 aristas
        arrayNodes_bot2[i].append(i+9)
        arrayNodes_bot2[i].append(i+1)
    elif i == 8:
        arrayNodes_bot2[i].append(i+9)
        arrayNodes_bot2[i].append(i-1)
    elif i == 72:
        arrayNodes_bot2[i].append(i+1)
        arrayNodes_bot2[i].append(i-9)
        
    elif i == 80:
        arrayNodes_bot2[i].append(i-1)
        arrayNodes_bot2[i].append(i-9)

def dfs_bot2(g,nodo_ini,nodo_fin):
    def dfsVisit(u):
        color[u] = 'gray'  #visitad
        for v in g[u]:
            if color[v] == 'white' and finnn[0]==False:

                  pi[v] = u
                  arr_con_padre.append([v,u])
                  if(v==nodo_fin):
                    finnn[0]=True

                  dfsVisit(v)

        color[u] = 'black'

    n = len(g)
    color = ['white']*n
    pi = [None]*n

    finnn=[False]
    arr_con_padre=[]
    ruta=False
    ###
    dfsVisit(nodo_ini)
    #####
    camino = []
    camino.append(nodo_fin)
    while nodo_fin != nodo_ini:
      for i in range(len(arr_con_padre)):
        if arr_con_padre[i][0] == nodo_fin:
          nodo_fin = arr_con_padre[i][1]
          camino.append(nodo_fin)
          break
    camino.reverse()
    
    return camino

def remove_aris_bot2(g, posa, posb):
  for i in range(81):
    if i == posa:
      for j in range(len(g[posa])-1,-1,-1):
        if g[posa][j] == posb:
          g[posa].pop(j)

  for i in range(81):
    if i == posb:
      for j in range(len(g[posb])-1,-1,-1):
        if g[posb][j] == posa:
          g[posb].pop(j)

def movbot2(x3_y3,turno,www):
    ###camino mass optimo
    camino = dfs_bot2(arrayNodes_bot2,x3_y3,72)
    x_y_aux_min=72
    tamañomin=len(camino)
    for i in range(73,81):

        camino = dfs_bot2(arrayNodes_bot2,x3_y3,i)
        if(tamañomin>=len(camino)):
            a_min=len(camino)
            x_y_aux_min=i
    ####
    if www==True:
        camino = dfs_bot2(arrayNodes_bot2,x3_y3,x_y_aux_min)
        x3_y3=camino[1]
        for i in range(72,81):
            if(x3_y3==i):
                www=False
                break;
    turno=1
    print(camino)
    return turno,www,x3_y3


x1_y1=36         #nodo inicio del bot1
x3_y3=4         #nodo inicio del bot2
x2_y2=76        #nodo incio del jugador
www=True        #cuando alguien llega al final acaba la partida
turno=1
cant_tabla_jugador=10       #cantidad de tablas maximas que puede poner el jugador
miFuente=pygame.font.Font(None,25)

while (True):
    #dibujo la tabla y los circulo de los jugadores
    pygame.draw.rect(screen, BLUE, (60, 40, 560, 560), 0)
    build_grid(40, 0, 40)  
    pygame. draw. circle(screen, GREEN, (grid[x1_y1][0]+20, grid[x1_y1][1]+20), 10, 0)
    pygame. draw. circle(screen, RED, (grid[x2_y2][0]+20, grid[x2_y2][1]+20), 10, 0)
    pygame. draw. circle(screen, MAGNETA, (grid[x3_y3][0]+20, grid[x3_y3][1]+20), 10, 0)
    dibujar_tablas_general(tablas_h_p,tablas_v_p)

    #turno jugador
    if(www==True):
        if turno==1:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()
                    x2_y2,turno=mov_jugador(x,y,x2_y2,x3_y3,turno,x1_y1)
                    turno,cant_tabla_jugador=poner_tablas_jugador(x,y,turno,x1_y1,x2_y2,x3_y3,cant_tabla_jugador)
                    for i in range(0,9):
                        if(x2_y2==i):
                            www=False
                            break;
        #turno bot
        elif turno==2:
            turno,www,x1_y1=movbot1(x1_y1,turno,www)
        elif turno==3:
            turno,www,x3_y3=movbot2(x3_y3,turno,www)

    #aca muestra la cantidad de tablas que le queda al jugador y la velocidad en que transcurre cada movimiento
    pygame.draw.rect(screen, (0,0,0), (0, 0, 650, 40), 0)
    Texto1=miFuente.render("Player walls: "+str(cant_tabla_jugador),5,RED)
    screen.blit(Texto1,(60,10))
    pygame.display.update()   
    update()
    time.sleep(0.2)