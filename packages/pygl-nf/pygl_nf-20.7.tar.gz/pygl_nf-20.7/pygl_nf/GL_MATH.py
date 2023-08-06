import math
import random

def Mod(num):
    if num < 0:num = -num
    return num


class Math_:

    def __init__(self):
        pass

    def COS(self,ugl):
        return math.cos(ugl)

    def SIN(self,ugl):
        return math.sin(ugl) 

    def RAST(self,pos1=[],pos2=[]):
        if pos1[0]>pos2[0]:w = pos1[0]-pos2[0]
        else:              w = pos2[0]-pos1[0]
        if pos1[1]>pos2[1]:h = pos1[1]-pos2[1]
        else:              h = pos2[1]-pos1[1]
        dl = math.sqrt(w*w+h*h)
        return dl   

    class Randomings():
        def __init__(self):
            pass

        class Randints():
            def __init__(self,a,b):
                self.a = a
                self.b = b
                self.num = random.randint(self.a,self.b)
            def Get(self):
                return self.num

        class Randrages():
            def __init__(self,a,b,step):
                self.a = a
                self.b = b
                self.step = step
                self.num = random.randrange(self.a,self.b,self.step)
            def Get(self):
                return self.num

        class Randoms():
            def __init__(self):
                self.num = random.random()
            def Get(self):
                return self.num

class Vec2_:
        def __init__(self,vect2d_start=[-1],vect2d_end=[-1],pos=[0,0]): 
            if vect2d_start[0]!=-1 and vect2d_end[0]!=-1:
                self.vect2d_start = vect2d_start
                self.vect2d_end = vect2d_end
                self.vec2D = [self.vect2d_start,self.vect2d_end]
                self.x = vect2d_end[0]-vect2d_start[0]
                self.y = vect2d_end[1]-vect2d_start[1]
            else:
                self.x = pos[0]
                self.y = pos[1]
            self.size = int(math.sqrt(self.x**2+self.y**2))
            self.absv = Mod(self.size)
            self.pos1 = [self.x,self.y]

        def RAV_2D(self,vector2D):
            parperx_st_ = int(vector2D.vect2d_start[0]-self.vect2d_start[0])
            parperx_en_ = int(vector2D.vect2d_end[0]-self.vect2d_end[0])
            parpery_st_ = int(vector2D.vect2d_start[1]-self.vect2d_start[1])
            parpery_en_ = int(vector2D.vect2d_end[1]-self.vect2d_end[1])
            if Mod(parperx_st_) == Mod(parperx_en_) and Mod(parpery_st_) == Mod(parpery_en_):
                return True
            else:
                return False

        def POV_2D(self,ugl):
            pos = [int(self.x*math.cos(ugl)-self.y*math.sin(ugl)),int(self.y*math.cos(ugl)+self.x*math.sin(ugl))]
            vec3 = Vec2_(pos=pos)
            return vec3

        def SUM(self,vector2D):
            pos=[self.x+vector2D.x,self.y+vector2D.y]
            vec3 = Vec2_(pos=pos)
            return vec3

        def RAZ(self,vector2D):
            pos=[self.x-vector2D.x,self.y-vector2D.y]
            vec3 = Vec2_(pos=pos)
            return vec3

        def UMN(self,delta):
            pos=[self.x*delta,self.y*delta]
            vec3 = Vec2_(pos=pos)
            return vec3

        def SCAL(self,vector2D):
            scl = self.x*vector2D.x+self.y*vector2D.y
            return scl

        def NUL(self):
            if self.vect2d_end==self.vect2d_start:return True
            else:return False

        def NAP(self,vector2D):
            parperx_st_ = int(vector2D.vect2d_start[0]-self.vect2d_start[0])
            parperx_en_ = int(vector2D.vect2d_end[0]-self.vect2d_end[0])
            parpery_st_ = int(vector2D.vect2d_start[1]-self.vect2d_start[1])
            parpery_en_ = int(vector2D.vect2d_end[1]-self.vect2d_end[1])
            
            if parperx_en_ == parperx_st_ and parpery_en_ == parpery_st_ :
                    return True
            else:
                    return False     




