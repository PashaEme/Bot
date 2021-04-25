import logging
import random

from loderunnerclient.internals.actions import LoderunnerAction
from loderunnerclient.internals.element import Element
from loderunnerclient.internals.point import Point
from loderunnerclient.internals.board import Board
from loderunnerclient.game_client import GameClient

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)
NAPRAVLENIE=None
kopnul=0
vragL=0
vragR=0
l=0
YblokR=0 # если есть кристал и стоит блок
YblokL=0 # если есть кристал справа и стоит блок

def turn(gcb: Board):
    try:
        global NAPRAVLENIE
        global kopnul
        global YblokR
        global YblokL
        global vragR
        global vragL
        global l
        tup=False
        brick = Element("#")
        wall = Element("☼")
        hole = Element(" ")
        green = Element('&')
        yellow = Element("$")
        red = Element("@")
        GOLD=gcb.get_gold_positions()
        myPos=gcb.get_my_position()
        x=myPos._x
        y=myPos._y
        tempL=[0]
        tempR=[0]
        left=list(LoderunnerAction)[0]
        right=list(LoderunnerAction)[1]
        up=list(LoderunnerAction)[2]
        down=list(LoderunnerAction)[3]
        kopR=list(LoderunnerAction)[4]
        kopL=list(LoderunnerAction)[5]
        stop=list(LoderunnerAction)[6]
        kill=list(LoderunnerAction)[7]
        hasPersonL=gcb.has_other_hero_at(myPos._x-1,myPos._y)
        hasPersonR=gcb.has_other_hero_at(myPos._x+1,myPos._y)
        hasGoldL=gcb.has_gold_at(myPos._x-1,myPos._y)
        hasGoldR=gcb.has_gold_at(myPos._x+1,myPos._y)
        barierR=gcb.has_wall_at(myPos._x+1,myPos._y) 
        barierL=gcb.has_wall_at(myPos._x-1,myPos._y) 
        barierUp=gcb.has_wall_at(myPos._x,myPos._y-1) or gcb.has_other_hero_at(myPos._x,myPos._y-1)
        barierDown=gcb.has_wall_at(myPos._x,myPos._y+1)
        trybaL=gcb.has_pipe_at(myPos._x-1,myPos._y)
        trybaR=gcb.has_pipe_at(myPos._x+1,myPos._y)
        teni=gcb.has_shadow_at(myPos._x,myPos._y)
        print("Мои кординаты:"+str(myPos))
        print("YblokR="+str(YblokR))
        print("l="+str(l))
        print("YblokL="+str(YblokL))
        if gcb.has_pipe_at(myPos._x, myPos._y):
            print("Труба отработала")
            return gcb.truba(myPos)
        
        
        if vragL==1:      #Если за нами бежит охотник, то удаляем
            vragL=0
            return right
        if vragR==1:
            vragR=0
            return left
        vragL=0
        vragR=0
        
        if gcb.has_element_at(myPos._x,myPos._y,Element('[')):   # если падает смотря направо, то бежим направо
            print("Падаю и смотрю направо")
            return right
        if gcb.has_element_at(myPos._x,myPos._y,Element(']')):   # если падает смотря налево, то бежит налево
            print("Падаю и смотрю налево")
            return left
        
        
        if myPos._y!=YblokR: # переменная обнулится, если уйдем с y т.е. с уровнягде есть блок  ДЛЯ ПРАВОГО БЛОКА!!!!
            YblokR=0
        if myPos._y!=YblokL: # переменная обнулится, если уйдем с y т.е. с уровнягде есть блок  ДЛЯ ЛЕВОГО БЛОКА!!!!
            YblokL=0
            
        if (l==1 or YblokL or YblokR) and gcb.has_ladder_at(myPos._x,myPos._y):
            print("Лестница отработала")
            l=1
            return gcb.ladder(myPos,tup)
        else:
            l=0
        if YblokR==myPos._y:
            return left
        if YblokL==myPos._y:
            if barierR:
                YblokL=0
                return left
            return right
        
        
        for i in GOLD:
            if (y==i._y) and i._x<=14 and myPos._x<=14:
                if(x-i._x<0):
                    tempR.append(x-i._x)
                if(x-i._x>0):
                    tempL.append(x-i._x)
            elif (y==i._y) and i._x>=14 and myPos._x>=14 and i._x<=28 and myPos._x<=28:
                if(x-i._x<0):
                    tempR.append(x-i._x)
                if(x-i._x>0):
                    tempL.append(x-i._x)
            elif (y==i._y) and i._x>=28 and myPos._x>=28 and i._x<=42 and myPos._x<=42:
                if(x-i._x<0):
                    tempR.append(x-i._x)
                if(x-i._x>0):
                    tempL.append(x-i._x)
            elif (y==i._y) and i._x>=42 and myPos._x>=42 and i._x<=56 and myPos._x<=56:
                if(x-i._x<0):
                    tempR.append(x-i._x)
                if(x-i._x>0):
                    tempL.append(x-i._x)

        tempR.sort()
        tempL.sort()
        minL=0
        minR=0
        if(len(tempR)>1):
            minR=tempR[-2]
        if(len(tempL)>1):
            minL=tempL[1]
        print("minR "+str(abs(minR)))
        print("minL "+str(minL))
        if (minL==0 and minR!=0) or(abs(minR)<minL and minR!=0):
            print('Двигаюсь вправо')
            NAPRAVLENIE=right
            if barierR:
                print("Встретил барьер справа")
                NAPRAVLENIE=left
                YblokR=myPos._y
        if (minL!=0 and minR==0) or (minL<abs(minR) and minL!=0):  
            NAPRAVLENIE=left
            print('Двигаюсь влево')
            if barierL:
                print("Встретил барьер слева")
                NAPRAVLENIE=right
                YblokL=myPos._y
        if (minL==minR) and (minL>0 or minR>0):
            return right
        
        
        
            
        #    
        if minL==0 and minR==0:
            if(gcb.has_ladder_at(myPos._x,myPos._y)):           # если надо на лестницу
                print("Отработал лестницу при нулевых кординатах")
                l=1
                return gcb.ladder(myPos,tup)
            if barierL:
                print("Есть барьер слева")
                NAPRAVLENIE=right
            if barierR:
                print("Есть барьер справа")
                NAPRAVLENIE=left
            if NAPRAVLENIE==None:
                print('налево')
                NAPRAVLENIE=left
                
        if teni==False:   
            # За нами бежит охотник
            # Увидел охотника справа
            if (gcb.has_enemy_at(myPos._x+3,myPos._y) or gcb.has_enemy_at(myPos._x+2,myPos._y) or (gcb.has_shadow_at(myPos._x+3,myPos._y) or gcb.has_shadow_at(myPos._x+2,myPos._y))) and (gcb.has_element_at(myPos._x+1,myPos._y+1, brick)):       
                print("Увидел охотника справа и просверлил справа")
                NAPRAVLENIE=left
                return LoderunnerAction.DRILL_RIGHT
            # Увидел охотника слева
            if (gcb.has_enemy_at(myPos._x-3,myPos._y) or gcb.has_enemy_at(myPos._x-2,myPos._y) or (gcb.has_shadow_at(myPos._x-3,myPos._y) or gcb.has_shadow_at(myPos._x-2,myPos._y))) and (gcb.has_element_at(myPos._x-1,myPos._y+1, brick)): 
                print("Увидел охотника слева и просверлил справа")
                NAPRAVLENIE=right
                return LoderunnerAction.DRILL_LEFT  
            if ((gcb.has_enemy_at(myPos._x-3,myPos._y) or gcb.has_enemy_at(myPos._x-2,myPos._y) or (gcb.has_shadow_at(myPos._x-3,myPos._y) or gcb.has_shadow_at(myPos._x-2,myPos._y))) and (gcb.has_element_at(myPos._x-1,myPos._y+1, wall))) or (gcb.has_enemy_at(myPos._x-1,myPos._y)):
                l=1
                return LoderunnerAction.GO_RIGHT
                #охотник справа
            if ((gcb.has_enemy_at(myPos._x+3,myPos._y) or gcb.has_enemy_at(myPos._x+2,myPos._y) or (gcb.has_shadow_at(myPos._x+3,myPos._y) or gcb.has_shadow_at(myPos._x+2,myPos._y))) and (gcb.has_element_at(myPos._x+1,myPos._y+1, wall))) or (gcb.has_enemy_at(myPos._x+1,myPos._y)):
                l=1
                return LoderunnerAction.GO_LEFT
                
        
        #два золота слева
        if gcb.has_gold_at(myPos._x-1,myPos._y+2) and gcb.has_gold_at(myPos._x-1,myPos._y) and gcb.has_element_at(myPos._x-1,myPos._y+1,brick):
            return LoderunnerAction.GO_LEFT
        #два золота справа
        if gcb.has_gold_at(myPos._x+1,myPos._y+2) and gcb.has_gold_at(myPos._x+1,myPos._y) and gcb.has_element_at(myPos._x+1,myPos._y+1,brick): 
            return LoderunnerAction.GO_RIGHT
        #золото под дыркой слева
        if (gcb.has_gold_at(myPos._x-1,myPos._y+2) or gcb.has_element_at(myPos._x-1,myPos._y+2,Element('S'))) and gcb.has_element_at(myPos._x-1,myPos._y+1,brick) and ((gcb.has_element_at(myPos._x-1,myPos._y,brick) or gcb.has_element_at(myPos._x-1,myPos._y,wall) or gcb.has_other_hero_at(myPos._x-1,myPos._y) or gcb.has_ladder_at(myPos._x-1,myPos._y)) == False): 
            kopnul=1
            return LoderunnerAction.DRILL_LEFT                              #
        if (gcb.has_gold_at(myPos._x-1,myPos._y+2) or gcb.has_element_at(myPos._x-1,myPos._y+2,Element('S'))) and kopnul==1:#
            kopnul=0
            return LoderunnerAction.GO_LEFT #
        #золото под дыркой cправа
        if (gcb.has_gold_at(myPos._x+1,myPos._y+2) or gcb.has_element_at(myPos._x+1,myPos._y+2,Element('S'))) and gcb.has_element_at(myPos._x+1,myPos._y+1,brick) and ((gcb.has_element_at(myPos._x+1,myPos._y,brick) or gcb.has_element_at(myPos._x+1,myPos._y,wall) or gcb.has_other_hero_at(myPos._x+1,myPos._y) or gcb.has_ladder_at(myPos._x+1,myPos._y)) == False): 
            kopnul=1
            return LoderunnerAction.DRILL_RIGHT                              #
        if (gcb.has_gold_at(myPos._x+1,myPos._y+2) or gcb.has_element_at(myPos._x+1,myPos._y+2,Element('S'))) and kopnul==1:#
            kopnul=0
            return LoderunnerAction.GO_RIGHT #
        #золото под нами
        if gcb.has_gold_at(myPos._x,myPos._y+2) and gcb.has_element_at(myPos._x,myPos._y+1,brick):
            a=random.randint(0,1) # чтобы рандомно шагал для вскапывания
            if ((gcb.has_element_at(myPos._x-1,myPos._y+1,brick) or  gcb.has_element_at(myPos._x-1,myPos._y+1,wall)) and (gcb.is_barrier_at(myPos._x-1,myPos._y) == False)) and a==0:
                return LoderunnerAction.GO_LEFT
            if ((gcb.has_element_at(myPos._x+1,myPos._y+1,brick) or  gcb.has_element_at(myPos._x+1,myPos._y+1,wall)) and (gcb.is_barrier_at(myPos._x+1,myPos._y) == False)) and a==1:
                return LoderunnerAction.GO_RIGHT
                
        if teni==False:
            # Встретили игрока
            # Увидел игрока справа
            if gcb.has_other_hero_at(myPos._x+1,myPos._y):  
                print("Увидел игрока справа, шагнул влево")
                return left
            if gcb.has_other_hero_at(myPos._x+2,myPos._y) and (gcb.has_element_at(myPos._x-1,myPos._y+1, brick)):       
                print("Увидел игрока справа и просверлил слева")
                vragR=1
                return LoderunnerAction.DRILL_LEFT
            elif gcb.has_other_hero_at(myPos._x+2,myPos._y) and (gcb.has_element_at(myPos._x+1,myPos._y+1, brick)):
                print("Увидел игрока справа и просверлил справа")
                vragL=1
                return LoderunnerAction.DRILL_RIGHT
            # Увидел игрока слева
            if gcb.has_other_hero_at(myPos._x-1,myPos._y): 
                print("Увидел игрока слева, шагнул вправо")
                return right
            if gcb.has_other_hero_at(myPos._x-2,myPos._y) and (gcb.has_element_at(myPos._x+1,myPos._y+1, brick)): 
                print("Увидел игрока слева и просверлил справа")
                vragL=1
                return LoderunnerAction.DRILL_RIGHT  
            elif gcb.has_other_hero_at(myPos._x-2,myPos._y) and (gcb.has_element_at(myPos._x-1,myPos._y+1, brick)):
                print("Увидел игрока слева и просверлил слева")
                vragR=1
                return LoderunnerAction.DRILL_LEFT
    
        return NAPRAVLENIE
        
    except:
        
        tup=False
        brick = Element("#")
        wall = Element("☼")
        hole = Element(" ")
        green = Element('&')
        yellow = Element("$")
        red = Element("@")
        GOLD=gcb.get_gold_positions()
        myPos=gcb.get_my_position()
        x=myPos._x
        y=myPos._y
        tempL=[0]
        tempR=[0]
        left=list(LoderunnerAction)[0]
        right=list(LoderunnerAction)[1]
        up=list(LoderunnerAction)[2]
        down=list(LoderunnerAction)[3]
        kopR=list(LoderunnerAction)[4]
        kopL=list(LoderunnerAction)[5]
        stop=list(LoderunnerAction)[6]
        kill=list(LoderunnerAction)[7]
        hasPersonL=gcb.has_other_hero_at(myPos._x-1,myPos._y)
        hasPersonR=gcb.has_other_hero_at(myPos._x+1,myPos._y)
        hasGoldL=gcb.has_gold_at(myPos._x-1,myPos._y)
        hasGoldR=gcb.has_gold_at(myPos._x+1,myPos._y)
        barierR=gcb.has_wall_at(myPos._x+1,myPos._y) 
        barierL=gcb.has_wall_at(myPos._x-1,myPos._y) 
        barierUp=gcb.has_wall_at(myPos._x,myPos._y-1) or gcb.has_other_hero_at(myPos._x,myPos._y-1)
        barierDown=gcb.has_wall_at(myPos._x,myPos._y+1)
        trybaL=gcb.has_pipe_at(myPos._x-1,myPos._y)
        trybaR=gcb.has_pipe_at(myPos._x+1,myPos._y)
        teni=gcb.has_shadow_at(myPos._x,myPos._y)
        print("Мои кординаты:"+str(myPos))
        print("YblokR="+str(YblokR))
        print("l="+str(l))
        print("YblokL="+str(YblokL))
        if gcb.has_pipe_at(myPos._x, myPos._y):
            print("Труба отработала")
            return gcb.truba(myPos)
        
        
        if vragL==1:      #Если за нами бежит охотник, то удаляем
            vragL=0
            return right
        if vragR==1:
            vragR=0
            return left
        vragL=0
        vragR=0
        
        if gcb.has_element_at(myPos._x,myPos._y,Element('[')):   # если падает смотря направо, то бежим направо
            print("Падаю и смотрю направо")
            return right
        if gcb.has_element_at(myPos._x,myPos._y,Element(']')):   # если падает смотря налево, то бежит налево
            print("Падаю и смотрю налево")
            return left
        
        
        if myPos._y!=YblokR: # переменная обнулится, если уйдем с y т.е. с уровнягде есть блок  ДЛЯ ПРАВОГО БЛОКА!!!!
            YblokR=0
        if myPos._y!=YblokL: # переменная обнулится, если уйдем с y т.е. с уровнягде есть блок  ДЛЯ ЛЕВОГО БЛОКА!!!!
            YblokL=0
            
        if (l==1 or YblokL or YblokR) and gcb.has_ladder_at(myPos._x,myPos._y):
            print("Лестница отработала")
            l=1
            return gcb.ladder(myPos,tup)
        else:
            l=0
        if YblokR==myPos._y:
            return left
        if YblokL==myPos._y:
            if barierR:
                YblokL=0
                return left
            return right
        
        
        for i in GOLD:
            if (y==i._y) and i._x<=14 and myPos._x<=14:
                if(x-i._x<0):
                    tempR.append(x-i._x)
                if(x-i._x>0):
                    tempL.append(x-i._x)
            elif (y==i._y) and i._x>=14 and myPos._x>=14 and i._x<=28 and myPos._x<=28:
                if(x-i._x<0):
                    tempR.append(x-i._x)
                if(x-i._x>0):
                    tempL.append(x-i._x)
            elif (y==i._y) and i._x>=28 and myPos._x>=28 and i._x<=42 and myPos._x<=42:
                if(x-i._x<0):
                    tempR.append(x-i._x)
                if(x-i._x>0):
                    tempL.append(x-i._x)
            elif (y==i._y) and i._x>=42 and myPos._x>=42 and i._x<=56 and myPos._x<=56:
                if(x-i._x<0):
                    tempR.append(x-i._x)
                if(x-i._x>0):
                    tempL.append(x-i._x)

        tempR.sort()
        tempL.sort()
        minL=0
        minR=0
        if(len(tempR)>1):
            minR=tempR[-2]
        if(len(tempL)>1):
            minL=tempL[1]
        print("minR "+str(abs(minR)))
        print("minL "+str(minL))
        if (minL==0 and minR!=0) or(abs(minR)<minL and minR!=0):
            print('Двигаюсь вправо')
            NAPRAVLENIE=right
            if barierR:
                print("Встретил барьер справа")
                NAPRAVLENIE=left
                YblokR=myPos._y
        if (minL!=0 and minR==0) or (minL<abs(minR) and minL!=0):  
            NAPRAVLENIE=left
            print('Двигаюсь влево')
            if barierL:
                print("Встретил барьер слева")
                NAPRAVLENIE=right
                YblokL=myPos._y
        if (minL==minR) and (minL>0 or minR>0):
            return right
        
        
        
            
        #    
        if minL==0 and minR==0:
            if(gcb.has_ladder_at(myPos._x,myPos._y)):           # если надо на лестницу
                print("Отработал лестницу при нулевых кординатах")
                l=1
                return gcb.ladder(myPos,tup)
            if barierL:
                print("Есть барьер слева")
                NAPRAVLENIE=right
            if barierR:
                print("Есть барьер справа")
                NAPRAVLENIE=left
            if NAPRAVLENIE==None:
                print('налево')
                NAPRAVLENIE=left
                
        if teni==False:   
            # За нами бежит охотник
            # Увидел охотника справа
            if (gcb.has_enemy_at(myPos._x+3,myPos._y) or gcb.has_enemy_at(myPos._x+2,myPos._y) or (gcb.has_shadow_at(myPos._x+3,myPos._y) or gcb.has_shadow_at(myPos._x+2,myPos._y))) and (gcb.has_element_at(myPos._x+1,myPos._y+1, brick)):       
                print("Увидел охотника справа и просверлил справа")
                NAPRAVLENIE=left
                return LoderunnerAction.DRILL_RIGHT
            # Увидел охотника слева
            if (gcb.has_enemy_at(myPos._x-3,myPos._y) or gcb.has_enemy_at(myPos._x-2,myPos._y) or (gcb.has_shadow_at(myPos._x-3,myPos._y) or gcb.has_shadow_at(myPos._x-2,myPos._y))) and (gcb.has_element_at(myPos._x-1,myPos._y+1, brick)): 
                print("Увидел охотника слева и просверлил справа")
                NAPRAVLENIE=right
                return LoderunnerAction.DRILL_LEFT  
            if ((gcb.has_enemy_at(myPos._x-3,myPos._y) or gcb.has_enemy_at(myPos._x-2,myPos._y) or (gcb.has_shadow_at(myPos._x-3,myPos._y) or gcb.has_shadow_at(myPos._x-2,myPos._y))) and (gcb.has_element_at(myPos._x-1,myPos._y+1, wall))) or (gcb.has_enemy_at(myPos._x-1,myPos._y)):
                l=1
                return LoderunnerAction.GO_RIGHT
                #охотник справа
            if ((gcb.has_enemy_at(myPos._x+3,myPos._y) or gcb.has_enemy_at(myPos._x+2,myPos._y) or (gcb.has_shadow_at(myPos._x+3,myPos._y) or gcb.has_shadow_at(myPos._x+2,myPos._y))) and (gcb.has_element_at(myPos._x+1,myPos._y+1, wall))) or (gcb.has_enemy_at(myPos._x+1,myPos._y)):
                l=1
                return LoderunnerAction.GO_LEFT
                
        
        #два золота слева
        if gcb.has_gold_at(myPos._x-1,myPos._y+2) and gcb.has_gold_at(myPos._x-1,myPos._y) and gcb.has_element_at(myPos._x-1,myPos._y+1,brick):
            return LoderunnerAction.GO_LEFT
        #два золота справа
        if gcb.has_gold_at(myPos._x+1,myPos._y+2) and gcb.has_gold_at(myPos._x+1,myPos._y) and gcb.has_element_at(myPos._x+1,myPos._y+1,brick): 
            return LoderunnerAction.GO_RIGHT
        #золото под дыркой слева
        if (gcb.has_gold_at(myPos._x-1,myPos._y+2) or gcb.has_element_at(myPos._x-1,myPos._y+2,Element('S'))) and gcb.has_element_at(myPos._x-1,myPos._y+1,brick) and ((gcb.has_element_at(myPos._x-1,myPos._y,brick) or gcb.has_element_at(myPos._x-1,myPos._y,wall) or gcb.has_other_hero_at(myPos._x-1,myPos._y) or gcb.has_ladder_at(myPos._x-1,myPos._y)) == False): 
            kopnul=1
            return LoderunnerAction.DRILL_LEFT                              #
        if (gcb.has_gold_at(myPos._x-1,myPos._y+2) or gcb.has_element_at(myPos._x-1,myPos._y+2,Element('S'))) and kopnul==1:#
            kopnul=0
            return LoderunnerAction.GO_LEFT #
        #золото под дыркой cправа
        if (gcb.has_gold_at(myPos._x+1,myPos._y+2) or gcb.has_element_at(myPos._x+1,myPos._y+2,Element('S'))) and gcb.has_element_at(myPos._x+1,myPos._y+1,brick) and ((gcb.has_element_at(myPos._x+1,myPos._y,brick) or gcb.has_element_at(myPos._x+1,myPos._y,wall) or gcb.has_other_hero_at(myPos._x+1,myPos._y) or gcb.has_ladder_at(myPos._x+1,myPos._y)) == False): 
            kopnul=1
            return LoderunnerAction.DRILL_RIGHT                              #
        if (gcb.has_gold_at(myPos._x+1,myPos._y+2) or gcb.has_element_at(myPos._x+1,myPos._y+2,Element('S'))) and kopnul==1:#
            kopnul=0
            return LoderunnerAction.GO_RIGHT #
        #золото под нами
        if gcb.has_gold_at(myPos._x,myPos._y+2) and gcb.has_element_at(myPos._x,myPos._y+1,brick):
            a=random.randint(0,1) # чтобы рандомно шагал для вскапывания
            if ((gcb.has_element_at(myPos._x-1,myPos._y+1,brick) or  gcb.has_element_at(myPos._x-1,myPos._y+1,wall)) and (gcb.is_barrier_at(myPos._x-1,myPos._y) == False)) and a==0:
                return LoderunnerAction.GO_LEFT
            if ((gcb.has_element_at(myPos._x+1,myPos._y+1,brick) or  gcb.has_element_at(myPos._x+1,myPos._y+1,wall)) and (gcb.is_barrier_at(myPos._x+1,myPos._y) == False)) and a==1:
                return LoderunnerAction.GO_RIGHT
                
        if teni==False:
            # Встретили игрока
            # Увидел игрока справа
            if gcb.has_other_hero_at(myPos._x+1,myPos._y):  
                print("Увидел игрока справа, шагнул влево")
                return left
            if gcb.has_other_hero_at(myPos._x+2,myPos._y) and (gcb.has_element_at(myPos._x-1,myPos._y+1, brick)):       
                print("Увидел игрока справа и просверлил слева")
                vragR=1
                return LoderunnerAction.DRILL_LEFT
            elif gcb.has_other_hero_at(myPos._x+2,myPos._y) and (gcb.has_element_at(myPos._x+1,myPos._y+1, brick)):
                print("Увидел игрока справа и просверлил справа")
                vragL=1
                return LoderunnerAction.DRILL_RIGHT
            # Увидел игрока слева
            if gcb.has_other_hero_at(myPos._x-1,myPos._y): 
                print("Увидел игрока слева, шагнул вправо")
                return right
            if gcb.has_other_hero_at(myPos._x-2,myPos._y) and (gcb.has_element_at(myPos._x+1,myPos._y+1, brick)): 
                print("Увидел игрока слева и просверлил справа")
                vragL=1
                return LoderunnerAction.DRILL_RIGHT  
            elif gcb.has_other_hero_at(myPos._x-2,myPos._y) and (gcb.has_element_at(myPos._x-1,myPos._y+1, brick)):
                print("Увидел игрока слева и просверлил слева")
                vragR=1
                return LoderunnerAction.DRILL_LEFT
    
        return NAPRAVLENIE

    


def main():
    gcb = GameClient(
        # change this url to your
        "https://dojorena.io/codenjoy-contest/board/player/dojorena425?code=4306548223354110059"
    )
    gcb.run(turn)


if __name__ == "__main__":
    main()         #
