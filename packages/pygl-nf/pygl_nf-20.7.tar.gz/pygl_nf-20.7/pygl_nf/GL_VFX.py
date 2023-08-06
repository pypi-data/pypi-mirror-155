from GL_MATH import Vec2_, Math_
import random 
from copy import copy
from GL import Text_
import pygame

class Particles():
    class Point():
        def __init__(self,surf,point_pos, gravity, shape_data, life_time = 2, speed=1, particle_count=5, spawn_time = 10, size_resize=True, size_deller = 0.1, max_particles=300) -> None:
            self.point_pos = Vec2_(pos=point_pos)
            self.gravity = Vec2_(pos=gravity)
            self.spawn_time = spawn_time
            self.timer = 0
            self.speed = speed
            self.life_time = life_time
            self.surf = surf
            self.max_particles = max_particles
            
            self.size_resize = size_resize
            self.size_deller = size_deller

            self.shape = shape_data[0]
            if self.shape == 'i':
                self.img = shape_data[3]
                self.i = self.img
            self.color = shape_data[1]
            self.size =  shape_data[2]


            self.particle_count = particle_count
            
            self.particles = []
        def Emiter(self):
            self.timer+=1
            if self.timer%self.spawn_time==0:

              for i in range(self.particle_count):
                    sped_vector = Vec2_(pos = [random.randint(-self.speed,self.speed)*random.random(),random.randint(-self.speed,self.speed)*random.random()] )
                    particle = [self.point_pos,sped_vector,self.life_time,self.size]
                    self.particles.append(particle)
        def Lifeter(self):
            for i in range(len(self.particles)):
                self.particles[i][2]-=0.1
                if self.particles[i][0].y>self.surf.GET_WIN_HEIGHT() or self.particles[i][0].y<0 or self.particles[i][0].x<0 or self.particles[i][0].x>self.surf.GET_WIN_WIDTH():
                    del self.particles[i]
                    break
                if self.particles[i][2]<=0:
                    del self.particles[i]
                    break   
        def Xclean(self):
            for i in range(len(self.particles)):
                if self.particles[i][3]<=0:
                    del self.particles[i]
                    break
                if random.randint(0,1)==1:
                    del self.particles[i]
                    break
            if len(self.particles)>self.max_particles:
                del self.particles[0:50]
        def PCount(self,pos):
            Text_(str(len(self.particles)),True,'black','arial',20,pos,SURF=self.surf.screen).RENDER()       
        def Focus(self):
            for i in range(len(self.particles)):
                self.particles[i][1] = self.particles[i][1].SUM(self.gravity)
                self.particles[i][0] = self.particles[i][0].SUM(self.particles[i][1])
                if self.size_resize:
                    self.particles[i][3]-=self.size_deller              
        def Render(self):
            for i in range(len(self.particles)):
                if self.shape == 'r':
                    if self.particles[i][2]>0:
                        self.surf.GL.Rect(self.color,self.particles[i][0].pos1,[self.particles[i][3],self.particles[i][3]],0,'s','D')
                
                elif self.shape == 'c':
                    if self.particles[i][2]>0:
                        self.surf.GL.Circle(self.color,self.particles[i][0].pos1,self.particles[i][3],0,'s','D')

                elif self.shape == 'i':
                    if self.particles[i][2]>0:
                        self.i = self.img
                        self.i.Set_pos(self.particles[i][0].pos1)
                        self.i.Scale([self.size,self.size])
                        self.i.Draw(self.surf.screen)
        def Set_position(self,pos):
            self.point_pos = Vec2_(pos=pos)
        def Set_color(self,color):
            self.color = color
        def Set_gravity(self,gravity):
            self.gravity = Vec2_(pos=gravity)
        def Set_speed(self,speed):
            self.speed = speed
        def Set_particle_count(self,count):
            self.particle_count = count
        def Set_spawn_time(self,time):
            self.spawn_time = time
        def Set_size_deller(self,deller):
            self.size_deller = deller
        def Set_size(self,size):
            self.size = size

    class Rect():
        def __init__(self,
                        surf,
                        rect,
                        shape_data,
                        color_randoming=False,
                        color_index=0,
                        circle_speed = 1,
                        vector_speed = [],
                        size_deller = 1,
                        return_size=False,
                        size_resize = True,
                        particle_count = 5,
                        max_particle = 300,
                        dell_count = 100,
                        gravity=[],
                        life_time = 2,
                        life_dell_count = 5,
                        life_delta = 0.1,
                        spawn_time = 5,
                        spawn_delta = 0.1,
                        image_rotating = False,
                        image_rotating_delta = 1,
                        randomig_iamge = False
                        ) -> None:

                self.image_rotating = image_rotating
                self.image_rotating_delta = image_rotating_delta
                self.rect = rect
                self.posx = self.rect[0]
                self.posy = self.rect[1]
                self.width = self.rect[2]
                self.height = self.rect[3]
                self.circle_speed = circle_speed
                self.size_deller = size_deller
                self.partcle_count = particle_count
                self.max_particle = max_particle
                self.size_resize = size_resize
                self.return_size = return_size
                self.gravity = Vec2_(pos=gravity)
                self.dell_count = dell_count
                self.vector_speed = vector_speed
                self.life_time = life_time
                self.life_dell_count = life_dell_count
                self.life_delta = life_delta
                self.spawn_time = spawn_time
                self.spawn_delta = spawn_delta
                self.time = 0
                self.surf = surf
                self.move_point = []
                self.move_point_set = False
                self.move_point_speed = 100
                self.move_radius = 100
                self.move_radius_delta_x = 1
                self.move_radius_delta_y = 1
                self.color_randoming = color_randoming
                self.color_index = color_index
                self.randoming_image = randomig_iamge
                

                self.shape_data = shape_data
                self.shape = self.shape_data[0]
                self.shape_color = self.shape_data[2]
                if self.shape == 'i':
                    self.img = self.shape_data[2]
                    self.orig_image = self.img
                    

                self.shape_max_size = self.shape_data[1]


                if self.return_size:self.shape_widt = 0
                else:self.shape_widt = self.shape_data[1]
                


                self.particles = []

        def Set_move_point(self,pos,speed=100,move_radius=100,move_radius_delta_x=4,move_radius_delta_y=4):
                self.move_point = pos
                self.move_point_set = True
                self.move_point_speed = speed
                self.move_radius = move_radius
                self.move_radius_delta_x = move_radius_delta_x
                self.move_radius_delta_y = move_radius_delta_y

        def Emiter(self):
                self.time+=self.spawn_delta
                if self.time%self.spawn_time==0:
                    for i in range(self.partcle_count):
                        pos = Vec2_(pos=[
                            random.randint(self.posx,self.posx+self.width),
                            random.randint(self.posy,self.posy+self.height)
                        ])
                        
                        self.cirkul_speed = Vec2_(pos=[
                            random.random()*self.circle_speed*random.randint(-1,1),
                            random.random()*self.circle_speed*random.randint(-1,1)
                        ])

                        self.vector_spee = Vec2_(pos=self.vector_speed)
                        if self.shape != 'i':
                            if self.color_randoming == True and type(self.shape_color)==list and len(self.shape_color)>1:
                                color = self.shape_color[random.randint(0,len(self.shape_color)-1)]
                            else:
                                color = self.shape_color[self.color_index]
                                
                                        
                        else:
                            color = None
                            rotate = random.randint(-self.image_rotating_delta,self.image_rotating_delta)
                            
                        if self.randoming_image:
                            ri = random.randint(0,len(self.img)-1)
                            img = self.img[ri]
                            
                            rect = self.img[ri].img.get_rect(center = pos.pos1)
                            particle = [pos,self.cirkul_speed,self.shape_widt,self.vector_spee,self.life_time,color,rotate,0,rect,img]
                        else:
                            rect = self.img.img.get_rect(center = pos.pos1)
                            particle = [pos,self.cirkul_speed,self.shape_widt,self.vector_spee,self.life_time,color,rotate,0,rect]

                        

                        self.particles.append(particle)

        def Render(self):
                for i in range(len(self.particles)):
                    if self.shape == 'r':

                        self.surf.GL.Rect(self.particles[i][5],self.particles[i][0].pos1,[self.particles[i][2],self.particles[i][2]],0,'s','D')
                    elif self.shape == 'c':

                        self.surf.GL.Circle(self.particles[i][5],self.particles[i][0].pos1,self.particles[i][2],0,'s','D')
                    elif self.shape == 'i':
                        if self.randoming_image:
                            
                            image = copy(self.particles[i][9])
                        else:
                            image = copy(self.img)
                        
                        
                        image.Set_pos([self.particles[i][0].pos1[0]-self.particles[i][2]/2,self.particles[i][0].pos1[1]-self.particles[i][2]/2])
                        if self.particles[i][2]>0:
                            image.Scale([self.particles[i][2],self.particles[i][2]])
                            new_image = pygame.transform.rotate(image.img,self.particles[i][7])
                            self.particles[i][8] = new_image.get_rect(center=[self.particles[i][8].center[0]++self.particles[i][0].pos1[0]-self.particles[i][8].center[0],self.particles[i][8].center[1]+self.particles[i][0].pos1[1]-self.particles[i][8].center[1]])
                            
                            
                            
                            self.surf.screen.blit(new_image,self.particles[i][8])

        def Focus(self):
                for i in range(len(self.particles)):
                    self.particles[i][1] = self.particles[i][1].SUM(self.gravity)

                    if self.move_point_set:    
                        sx = -(self.particles[i][0].pos1[0]-self.move_point[0])/self.move_point_speed
                        sy = -(self.particles[i][0].pos1[1]-self.move_point[1])/self.move_point_speed
                        if Math_().RAST(self.particles[i][0].pos1,self.move_point)<self.move_radius:
                            sx*=self.move_radius_delta_x
                            sy*=self.move_radius_delta_y
                        
                        sv = Vec2_(pos=[sx,sy])
                        self.particles[i][0] = self.particles[i][0].SUM(sv)
                    if self.image_rotating:
                        self.particles[i][7]+=self.particles[i][6]
                    self.particles[i][1] = self.particles[i][1].SUM(self.particles[i][3])
                    self.particles[i][0] = self.particles[i][0].SUM(self.particles[i][1])
                    self.particles[i][4]-=self.life_delta
                    if self.size_resize:
                        if self.return_size:  
                            if self.particles[i][2]<=self.shape_max_size+10:
                                self.particles[i][2]+=self.size_deller
                        else:
                            self.particles[i][2]-=self.size_deller
                    


        def Xclean(self):
                for i in range(len(self.particles)):
                    if self.particles[i][1].pos1==[0,0]:
                        del self.particles[i]
                        break

                for i in range(len(self.particles)):
                    if self.surf.IN_WINDOW(self.particles[i][0].pos1):
                        pass
                    else:
                        del self.particles[i]
                        break

                for i in range(len(self.particles)):
                    if self.particles[i][2]<=0:
                        del self.particles[i]
                        break

                for i in range(len(self.particles)):
                    if self.particles[i][4]<0:
                        del self.particles[-self.life_dell_count:]
                        break

                if self.return_size:
                    for i in range(len(self.particles)):
                        if self.particles[i][2]>self.shape_max_size:
                            del self.particles[i]
                            break

                

                if len(self.particles)>self.max_particle:
                    del self.particles[1:self.dell_count]
                

                
                
        def PCount(self,pos):
                Text_(str(len(self.particles)),True,'black','arial',15,pos,SURF=self.surf.screen).RENDER()

        def Set_width(self,width):
                self.width = width

        def Set_height(self,height):
                self.height = height

        def Set_position(self,position):
                self.posx = position[0]
                self.posy = position[1]

    class Bax():
        def __init__(self,surf,position,max_size,min_size,start_size,size_delta,size_delta2,color,type='c',start_rad=10,rad_delta=0,zikl=False):
            self.pos = position
            self.max_size = max_size
            self.min_size = min_size
            self.start_size = start_size
            self.ss = self.start_size
            self.size_delta = size_delta
            self.size_delta2 = size_delta2
            self.sd2 = self.size_delta2

            self.start_rad = start_rad
            self.sr = self.start_rad
            self.rad_delta = rad_delta

            self.zikl = zikl


            self.color = color
            self.type = type
            self.surf = surf
            

        def Render(self):
            if self.type == 'c':
                if self.start_rad>0:
                    self.surf.GL.Circle(self.color,self.pos,self.start_size,self.start_rad,'s','D')
            elif self.type == 'r':
                if self.start_rad>0:
                    self.surf.GL.Rect(self.color,[self.pos[0]-self.start_size/2,self.pos[1]-self.start_size/2],[self.start_size,self.start_size],self.start_rad,'s','D')

        def Focus(self):
            self.start_rad+=self.rad_delta
            
            self.size_delta2+=self.sd2
            if self.start_size<=self.max_size and self.start_size>self.min_size:
                self.start_size+=self.size_delta+self.size_delta2
            

            if self.zikl:
                if self.start_size<self.min_size or self.start_size>self.max_size:
                    self.start_size = self.ss
                    self.size_delta2 = self.sd2
                    self.start_rad = self.sr