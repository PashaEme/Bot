from math import sqrt
import random
from loderunnerclient.internals.element import Element
from loderunnerclient.internals.point import Point
from loderunnerclient.internals.actions import LoderunnerAction

brick = Element("#")
wall = Element("☼")
hole = Element(" ")
green = Element('&')
yellow = Element("$")
red = Element("@")
up=list(LoderunnerAction)[2]
right=list(LoderunnerAction)[1]
left=list(LoderunnerAction)[0]
down=list(LoderunnerAction)[3]


class Board:
    """ Class describes the Board field for Loderunner game."""

    def __init__(self, board_string):
        self._string = board_string.replace("\n", "")
        self._len = len(self._string)  # the length of the string
        self._size = int(sqrt(self._len))  # size of the board
        # print("Board size is sqrt", self._len, self._size)

    def _find_all(self, element: Element):
        """ Returns the list of points for the given element type."""
        _points = []
        _a_char = element.get_char()
        for i, c in enumerate(self._string):
            if c == _a_char:
                _points.append(self._strpos2pt(i))
        return _points

    def get_at(self, x, y):
        """ Return an Element object at coordinates x,y."""
        return Element(self._string[self._xy2strpos(x, y)])

    def has_element_at(self, x, y, element_object):
        """ Return True if Element is at x,y coordinates."""
        return element_object == self.get_at(x, y)

    def is_barrier_at(self, x, y):
        """ Return true if barrier is at x,y."""
        return Point(x, y) in self.get_barriers()

    def get_my_position(self):
        """ Return the point where your hero is."""
        points = set()
        points.update(self._find_all(Element("HERO_DIE")))
        points.update(self._find_all(Element("HERO_DRILL_LEFT")))
        points.update(self._find_all(Element("HERO_DRILL_RIGHT")))
        points.update(self._find_all(Element("HERO_FALL_RIGHT")))
        points.update(self._find_all(Element("HERO_FALL_LEFT")))
        points.update(self._find_all(Element("HERO_LADDER")))
        points.update(self._find_all(Element("HERO_LEFT")))
        points.update(self._find_all(Element("HERO_RIGHT")))
        points.update(self._find_all(Element("HERO_PIPE_LEFT")))
        points.update(self._find_all(Element("HERO_PIPE_RIGHT")))
        points.update(self._find_all(Element("HERO_SHADOW_DRILL_LEFT")))
        points.update(self._find_all(Element("HERO_SHADOW_DRILL_RIGHT")))
        points.update(self._find_all(Element("HERO_SHADOW_LADDER")))
        points.update(self._find_all(Element("HERO_SHADOW_LEFT")))
        points.update(self._find_all(Element("HERO_SHADOW_RIGHT")))
        points.update(self._find_all(Element("HERO_SHADOW_FALL_LEFT")))
        points.update(self._find_all(Element("HERO_SHADOW_FALL_RIGHT")))
        points.update(self._find_all(Element("HERO_SHADOW_PIPE_LEFT")))
        points.update(self._find_all(Element("HERO_SHADOW_PIPE_RIGHT")))
        assert len(points) <= 1, "There should be only one hero"
        return list(points)[0]

    def is_game_over(self):
        """ Returns False if your hero still alive."""
        return Element("HERO_DIE").get_char() in self._string

    def get_enemy_positions(self):
        """ Return the list of points for other heroes."""
        points = set()
        points.update(self._find_all(Element("ENEMY_LADDER")))
        points.update(self._find_all(Element("ENEMY_LEFT")))
        points.update(self._find_all(Element("ENEMY_PIPE_LEFT")))
        points.update(self._find_all(Element("ENEMY_PIPE_RIGHT")))
        points.update(self._find_all(Element("ENEMY_RIGHT")))
        points.update(self._find_all(Element("ENEMY_PIT")))
        return list(points)

    def get_other_hero_positions(self):
        """ Return the list of points for other heroes."""
        points = set()
        points.update(self._find_all(Element("OTHER_HERO_LADDER")))
        points.update(self._find_all(Element("OTHER_HERO_LEFT")))
        points.update(self._find_all(Element("OTHER_HERO_RIGHT")))
        points.update(self._find_all(Element("OTHER_HERO_PIPE_LEFT")))
        points.update(self._find_all(Element("OTHER_HERO_PIPE_RIGHT")))
        points.update(self._find_all(Element("OTHER_HERO_SHADOW_LEFT")))
        points.update(self._find_all(Element("OTHER_HERO_SHADOW_RIGHT")))
        points.update(self._find_all(Element("OTHER_HERO_SHADOW_LADDER")))
        points.update(self._find_all(Element("OTHER_HERO_SHADOW_PIPE_LEFT")))
        points.update(self._find_all(Element("OTHER_HERO_SHADOW_PIPE_RIGHT")))
        return list(points)

    def get_shadow_pills(self):
        points = set()
        points.update(self._find_all(Element("THE_SHADOW_PILL")))
        return list(points)

    def get_portals(self):
        points = set()
        points.update(self._find_all(Element("PORTAL")))
        return list(points)

    def __get_shadows(self):
        points = set()
        points.update(self._find_all(Element("HERO_SHADOW_DRILL_LEFT")))
        points.update(self._find_all(Element("HERO_SHADOW_DRILL_RIGHT")))
        points.update(self._find_all(Element("HERO_SHADOW_LADDER")))
        points.update(self._find_all(Element("HERO_SHADOW_LEFT")))
        points.update(self._find_all(Element("HERO_SHADOW_RIGHT")))
        points.update(self._find_all(Element("HERO_SHADOW_FALL_LEFT")))
        points.update(self._find_all(Element("HERO_SHADOW_FALL_RIGHT")))
        points.update(self._find_all(Element("HERO_SHADOW_PIPE_LEFT")))
        points.update(self._find_all(Element("HERO_SHADOW_PIPE_RIGHT")))

        points.update(self._find_all(Element("OTHER_HERO_SHADOW_LEFT")))
        points.update(self._find_all(Element("OTHER_HERO_SHADOW_RIGHT")))
        points.update(self._find_all(Element("OTHER_HERO_SHADOW_LADDER")))
        points.update(self._find_all(Element("OTHER_HERO_SHADOW_PIPE_LEFT")))
        points.update(self._find_all(Element("OTHER_HERO_SHADOW_PIPE_RIGHT")))
        return list(points)

    def get_wall_positions(self):
        """ Returns the list of walls Element Points."""
        points = set()
        points.update(self._find_all(Element("BRICK")))
        points.update(self._find_all(Element("UNDESTROYABLE_WALL")))
        return list(points)

    def get_ladder_positions(self):
        """Returns the set of ladder Points"""
        points = set()
        points.update(self._find_all(Element("LADDER")))
        points.update(self._find_all(Element("HERO_LADDER")))
        points.update(self._find_all(Element("OTHER_HERO_LADDER")))
        points.update(self._find_all(Element("ENEMY_LADDER")))
        points.update(self._find_all(Element("HERO_SHADOW_LADDER")))
        points.update(self._find_all(Element("OTHER_HERO_SHADOW_LADDER")))
        return list(points)

    def get_gold_positions(self):
        points = set()
        points.update(self._find_all(Element("YELLOW_GOLD")))
        points.update(self._find_all(Element("GREEN_GOLD")))
        points.update(self._find_all(Element("RED_GOLD")))
        return list(points)

    def get_pipe_positions(self):
        """Returns the set of pipe Points"""
        points = set()
        points.update(self._find_all(Element("PIPE")))
        points.update(self._find_all(Element("HERO_PIPE_LEFT")))
        points.update(self._find_all(Element("HERO_PIPE_RIGHT")))
        points.update(self._find_all(Element("OTHER_HERO_PIPE_LEFT")))
        points.update(self._find_all(Element("OTHER_HERO_PIPE_RIGHT")))
        points.update(self._find_all(Element("ENEMY_PIPE_LEFT")))
        points.update(self._find_all(Element("ENEMY_PIPE_RIGHT")))
        points.update(self._find_all(Element("HERO_SHADOW_PIPE_LEFT")))
        points.update(self._find_all(Element("HERO_SHADOW_PIPE_RIGHT")))
        points.update(self._find_all(Element("OTHER_HERO_SHADOW_PIPE_LEFT")))
        points.update(self._find_all(Element("OTHER_HERO_SHADOW_PIPE_RIGHT")))
        return list(points)

    def get_barriers(self):
        """ Return the list of barriers Points."""
        points = set()
        points.update(self.get_wall_positions())
        return list(points)

    def is_near_to_element(self, x, y, elem):
        _is_near = False
        if not Point(x, y).is_bad(self._size):
            _is_near = (
                self.has_element_at(x + 1, y, elem)
                or self.has_element_at(x - 1, y, elem)
                or self.has_element_at(x, 1 + y, elem)
                or self.has_element_at(x, 1 - y, elem)
            )
        return _is_near

    def has_enemy_at(self, x, y):
        return Point(x, y) in self.get_enemy_positions()

    def has_other_hero_at(self, x, y):
        return Point(x, y) in self.get_other_hero_positions()

    def has_wall_at(self, x, y):
        return Point(x, y) in self.get_wall_positions()

    def has_ladder_at(self, x, y):
        return Point(x, y) in self.get_ladder_positions()

    def has_gold_at(self, x, y):
        return Point(x, y) in self.get_gold_positions()

    def has_pipe_at(self, x, y):
        return Point(x, y) in self.get_pipe_positions()

    def has_shadow_at(self, x, y):
        return Point(x, y) in self.__get_shadows()

    def get_count_elements_near_to_point(self, x, y, elem):
        """ Counts the number of occurencies of elem nearby """
        _near_count = 0
        if not Point(x, y).is_bad(self._size):
            for _x, _y in ((x + 1, y), (x - 1, y), (x, 1 + y), (x, 1 - y)):
                if self.has_element_at(_x, _y, elem):
                    _near_count += 1
        return _near_count

    def print_board(self):
        print(self._line_by_line())

    def _line_by_line(self):
        return "\n".join(
            [self._string[i : i + self._size] for i in range(0, self._len, self._size)]
        )

    def _strpos2pt(self, strpos):
        return Point(*self._strpos2xy(strpos))

    def _strpos2xy(self, strpos):
        return (strpos % self._size, strpos // self._size)

    def _xy2strpos(self, x, y):
        return self._size * y + x


    def ladder(self,myPos, tup):
        lenght_ladder = []
        print('tup = ', tup)
        counter1 = myPos._y
        counter2 = myPos._y
        lenght_ladder.append(counter1)
        while self.has_ladder_at(myPos._x, counter1) or self.has_ladder_at(myPos._x, counter2):
            counter1-=1
            if self.has_ladder_at(myPos._x, counter1):
                lenght_ladder.append(counter1)
            counter2+=1
            if self.has_ladder_at(myPos._x, counter2):
                lenght_ladder.append(counter2)
        lenght_ladder.sort()
        left_side = {}
        rigt_side = {}
        for i in lenght_ladder:
            #left_side
            if self.has_element_at(myPos._x-1,i, wall) or self.has_element_at(myPos._x-1,i, brick):
                left_side[i] = "Wall"
            if self.has_element_at(myPos._x-1,i, green):
                left_side[i] = 1
            if self.has_element_at(myPos._x-1,i, yellow):
                left_side[i] = 2
            if self.has_element_at(myPos._x-1,i, red):
                left_side[i] = 3
            if self.has_pipe_at(myPos._x-1,i):
                left_side[i] = "Pipe"
            #right_side
            if self.has_element_at(myPos._x+1,i, wall) or self.has_element_at(myPos._x-1,i, brick):
                rigt_side[i] = "Wall"
            if self.has_element_at(myPos._x+1,i, green):
                rigt_side[i] = 1
            if self.has_element_at(myPos._x+1,i, yellow):
                rigt_side[i] = 2
            if self.has_element_at(myPos._x+1,i, red):
                rigt_side[i] = 3
            if self.has_pipe_at(myPos._x+1,i):
                rigt_side[i] = "Pipe"
            
        bar_up = False
        bar_down = False
        if self.has_wall_at(myPos._x, max(lenght_ladder)+1) or self.has_other_hero_at(myPos._x, max(lenght_ladder)+1):
            bar_down = True
        if self.has_wall_at(myPos._x, min(lenght_ladder)-1) or self.has_other_hero_at(myPos._x, min(lenght_ladder)-1):
            bar_up = True
            

        if self.has_gold_at(myPos._x-1,myPos._y) and self.has_gold_at(myPos._x-1,myPos._y-1):
            return up
        if self.has_gold_at(myPos._x-1,myPos._y) and (self.has_gold_at(myPos._x-1,myPos._y-1) == False):
            return left
        if self.has_gold_at(myPos._x+1,myPos._y) and self.has_gold_at(myPos._x+1,myPos._y-1):
            return up
        if self.has_gold_at(myPos._x+1,myPos._y) and (self.has_gold_at(myPos._x+1,myPos._y-1) == False):
            return right
        Left_Side = True
        Right_Side = True
        if (1 not in left_side) or (2 not in left_side) or (3 not in left_side):
            Left_Side = False
        if (1 not in rigt_side) or (2 not in rigt_side) or (3 not in rigt_side):
            Right_Side = False

        if tup == False:
            
            if (Left_Side or Right_Side) == False:
                print("Вокруг лестницы ничего нет")
                c1 = 0
                c2 = 0
                for i in lenght_ladder:
                    if self.has_wall_at(myPos._x+1,i):
                        c1+=1
                    if self.has_wall_at(myPos._x+1,i):
                        c1+=1
                left_wall = False
                right_wall = False
                if c1 == len(lenght_ladder):
                    left_wall = True
                    print("left_wall = ", left_wall)
                if c2 == len(lenght_ladder):
                    right_wall = True 
                if tup == False:
                    if bar_up == True and bar_down == False:
                        return down
                    if bar_down == True and bar_up == False:
                        return up
                    if bar_up and bar_down:
                        if right_wall:
                            return left #!!!
                        if left_wall:
                            return right #!!!
                        c = random.randint(0,1)
                        if c == 0:
                            return left
                        if c == 1:
                            return right
                    if bar_up == False and bar_down == False:
                        return up
            
            if tup == True:
                if self.has_element_at(myPos._x-1,myPos._y, Element(" ")) and self.has_element_at(myPos._x+1,myPos._y, Element(" ")):
                    h = random.randint(0,1)
                    if h == 1:
                        return right
                    else:
                        return left
                if (self.has_element_at(myPos._x-1,myPos._y, Element(" ")) == False) and self.has_element_at(myPos._x+1,myPos._y, Element(" ")):
                    return right
                if (self.has_element_at(myPos._x+1,myPos._y, Element(" ")) == False) and self.has_element_at(myPos._x-1,myPos._y, Element(" ")):
                    return left

        return up
    
    def truba(self,myPos):
        print("!!!!!!!!!!!")
        
        barierDown=self.has_element_at(myPos._x,myPos._y+1, brick) or self.has_element_at(myPos._x,myPos._y+1, wall) or self.has_ladder_at(myPos._x,myPos._y+1) or self.has_enemy_at(myPos._x,myPos._y+1)
        if self.has_pipe_at(myPos._x, myPos._y):
            wide_pipe = []
            count1 = myPos._x
            count2 = myPos._x
            wide_pipe.append(count1)
            while self.has_pipe_at(count1, myPos._y) or self.has_pipe_at(count2, myPos._y) :
                count1-=1
                if self.has_pipe_at(count1, myPos._y):
                    wide_pipe.append(count1)
                count2+=1
                if self.has_pipe_at(count2, myPos._y):
                    wide_pipe.append(count2)
            wide_pipe.sort()
            left_barrier = False
            right_barrier = False
            if self.has_element_at(min(wide_pipe)-1, myPos._y, wall) or self.has_element_at(min(wide_pipe)-1, myPos._y, brick) or self.has_element_at(min(wide_pipe)-1, myPos._y, Element("H")):
                left_barrier = True
            if self.has_element_at(max(wide_pipe)+1, myPos._y, wall) or self.has_element_at(max(wide_pipe)+1, myPos._y, brick) or self.has_element_at(min(wide_pipe)+1, myPos._y, Element("H")):
                right_barrier = True
            dct = {}
            if left_barrier and right_barrier: # слева и справа есть препятствие
                for i in range(min(wide_pipe), max(wide_pipe)+1):
                    if self.has_element_at(i, myPos._y+1,green):
                        dct[i] = 1
                    if self.has_element_at(i, myPos._y+1,yellow):
                        dct[i] = 2
                    if self.has_element_at(i, myPos._y+1,red):
                        dct[i] = 3
            if left_barrier == False and right_barrier: # слева нет препятствия
                if self.has_element_at(min(wide_pipe)-1, myPos._y,green):          #алмазы на уровне
                    dct[min(wide_pipe)-1] = 1                               #
                if self.has_element_at(min(wide_pipe)-1, myPos._y,yellow):             #
                    dct[min(wide_pipe)-1] = 2                               #
                if self.has_element_at(min(wide_pipe)-1, myPos._y,red):                #
                    dct[min(wide_pipe)-1] = 3                               #
                for i in range(min(wide_pipe)-1, max(wide_pipe)+1):
                    if self.has_element_at(i, myPos._y+1,green):
                        dct[i] = 1
                    if self.has_element_at(i, myPos._y+1,yellow):
                        dct[i] = 2
                    if self.has_element_at(i, myPos._y+1,red):
                        dct[i] = 3


            if left_barrier == False and right_barrier == False: # нет препятствий
                if self.has_element_at(min(wide_pipe)-1, myPos._y+1,green): #алмазы на уроне
                    dct[min(wide_pipe)-1] = 1
                if self.has_element_at(min(wide_pipe)-1, myPos._y+1,yellow):
                    dct[min(wide_pipe)-1] = 2
                if self.has_element_at(min(wide_pipe)-1, myPos._y+1,red):
                    dct[min(wide_pipe)-1] = 3

                for i in range(min(wide_pipe)-1, max(wide_pipe)+2):
                    if self.has_element_at(i, myPos._y+1,green):
                        dct[i] = 1
                    if self.has_element_at(i, myPos._y+1,yellow):
                        dct[i] = 2
                    if self.has_element_at(i, myPos._y+1,red):
                        dct[i] = 3


            if left_barrier and right_barrier == False:  #справа нет препятствия

                if self.has_element_at(min(wide_pipe), myPos._y+1,green): #алмазы на уроне
                    dct[min(wide_pipe)] = 1
                if self.has_element_at(min(wide_pipe), myPos._y+1,yellow):
                    dct[min(wide_pipe)] = 2
                if self.has_element_at(min(wide_pipe), myPos._y+1,red):
                    dct[min(wide_pipe)] = 3

                for i in range(min(wide_pipe), max(wide_pipe)+2):
                    if self.has_element_at(i, myPos._y+1,green):
                        dct[i] = 1
                    if self.has_element_at(i, myPos._y+1,yellow):
                        dct[i] = 2
                    if self.has_element_at(i, myPos._y+1,red):
                        dct[i] = 3
            print(dct)
            if dct == {}:
                if barierDown:
                    a=random.randint(0,1)
                    if a==1:
                        return left
                    else:
                        return right
                else:
                    return down
            metka = max(dct, key=dct.get)
            while True:
                #если под трубой
                if metka > myPos._x:
                    return LoderunnerAction.GO_RIGHT
                if metka < myPos._x:
                    return LoderunnerAction.GO_LEFT
                if metka == myPos._x:
                    return LoderunnerAction.GO_DOWN
                if self.has_pipe_at(myPos._x, myPos._y) == False:
                    break

    def tupic(self ,myPos, tup):
        count1 = myPos._x
        count2 = myPos._x
        wide_pustota = []
        c1 = 1
        c2 = 1
        while True:
            if self.has_element_at(myPos._x-c,myPos_y, brick) or self.has_element_at(myPos._x-c,myPos_y, wall):
                wide_pustota.append(myPos._x-c)
            c1+=1
            break
        while True:
            if self.has_element_at(myPos._x+c,myPos_y, brick) or self.has_element_at(myPos._x+c,myPos_y, wall):
                wide_pustota.append(myPos._x+c)
            c2+=1
            break
        wide_pustota.sort()
        print("wide_pustota = ", wide_pustota)
        gold_mas = []
        tablet_mas = []
        portal_mas = []
        ladder_mass = []
        for i in range(wide_pustota[0]+1,wide_pustota[1]):
            if self.has_gold_at(i, myPos._y):
                gold_mas.append(i)
            if self.has_element_at(i, myPos._y, Element("⊛")):
                portal_mas.append(i)
            if self.has_element_at(i, myPos._y, Element("S")):
                tablet_mas.append(i)
        tablet_mas.sort()
        portal_mas.sort()
        if gold_mas == []:
            if tablet_mas!=[]:
                if len(tablet_mas) == 1:
                    if tablet_mas[0]>myPos._x:
                        return right
                    if tablet_mas[0]<myPos._x:
                        return left
                if len(tablet_mas)>1:
                    a = random.randint(min(tablet_mas), max(tablet_mas))
                    if a>myPos._x:
                        return right
                    if a<myPos._x:
                        return left
            if portal_mas!=[]:
                if len(portal_mas) == 1:
                    if portal_mas[0]>myPos._x:
                        return right
                    if portal_mas[0]<myPos._x:
                        return left
                if len(portal_mas)>1:
                    b = random.randint(min(portal_mas), max(portal_mas))
                    if b>myPos._x:
                        return right
                    if b<myPos._x:
                        return left
            if self.has_ladder_at(myPos._x, myPos._y+1):
                tup = True
                return down
        if gold_mas!=[]:
            print("NO GOLD_MAS")
            
            
                    
                    
        
        
                

    
    


if __name__ == "__main__":
    raise RuntimeError("This module is not designed to be ran from CLI")



