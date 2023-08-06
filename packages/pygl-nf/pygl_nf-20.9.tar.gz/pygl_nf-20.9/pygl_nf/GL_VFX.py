from pygl_nf.GL_MATH import Vec2_, Math_
from pygl_nf import GL_MATH
import random 
from copy import copy
from pygl_nf.GL import Text_
from pygl_nf.GL import Color_
from pygl_nf import GL
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
                        vector_speed = [0,0],
                        size_deller = 1,
                        return_size=False,
                        size_resize = True,
                        particle_count = 5,
                        max_particle = 300,
                        dell_count = 100,
                        gravity=[0,0],
                        life_time = 200,
                        life_dell_count = 5,
                        life_delta = 0.01,
                        spawn_time = 1,
                        spawn_delta = 1,
                        image_rotating = False,
                        image_rotating_delta = 1,
                        randomig_iamge = False,
                        lighting = False,
                        lighting_color = (20,20,20),
                        light_radius_resize = False,
                        light_radius = 10,
                        light_radius_clip_in_shape_rad = False,
                        light_alpha = 255,
                        light_color_dispers = 200,
                        coed_part_lines = False,
                        coed_part_lines_centered = False,
                        coed_part_lines_add = 0,
                        coed_part_lines_save_end_pos = False,
                        rotate_in_center = False,
                        rotating_in_center_angle = 0,
                        rotate_gravity = False,
                        rotating_gravity_angle = 0,
                        image_rotate_in_position = False,
                        image_rotate_in_vector = False,
                        image_rotate_in_position_angle = 0
                        ) -> None:
                
                self.start_render = True
                self.start_emit = True
                self.start_focus = True
                self.start_delete = True
                self.rotating_gravity_angle = rotating_gravity_angle
                self.rotate_gravity = rotate_gravity
                self.rotating_in_center_angle = rotating_in_center_angle
                self.rotate_in_center = rotate_in_center
                self.light_color_dispers = light_color_dispers
                self.coed_part_lines_save_end_pos = coed_part_lines_save_end_pos ; self.end_line_pos = []
                self.coed_part_lines_add = coed_part_lines_add
                self.coed_part_lines_centered  = coed_part_lines_centered
                self.soed_part_lines = coed_part_lines
                self.light_alpha = light_alpha
                self.light_radius_clip_in_shape_rad = light_radius_clip_in_shape_rad
                self.light_radius_resize = light_radius_resize
                self.light_radius = light_radius
                self.lighting = lighting
                self.lighting_color = lighting_color
                self.image_rotate_in_position = image_rotate_in_position
                self.image_rotate_in_vector = image_rotate_in_vector
                self.image_rotate_in_position_angle = image_rotate_in_position_angle
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
                self.gravity = Vec2_(gravity)
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
                self.end_mouse_pos = 0

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




                self.id = random.randint(1,1000000000)
                
        
        def mult(self,num):
            if num<=0:
                num = 0
            return num

        def Set_move_point(self,pos,speed=100,move_radius=100,move_radius_delta_x=4,move_radius_delta_y=4):
                self.move_point = pos
                self.move_point_set = True
                self.move_point_speed = speed
                self.move_radius = move_radius
                self.move_radius_delta_x = move_radius_delta_x
                self.move_radius_delta_y = move_radius_delta_y

        def Emiter(self):
            if self.start_emit:
                self.time+=self.spawn_delta
                if self.time%self.spawn_time==0:
                    self.end_line_pos = [self.posx,self.posy]
                    for i in range(self.partcle_count):
                        pos = Vec2_([
                            random.randint(self.posx,self.posx+self.width),
                            random.randint(self.posy,self.posy+self.height)
                        ])
                        
                        self.cirkul_spee = Vec2_([
                            random.randint(-10000,10000)/10000*self.circle_speed,
                            random.randint(-10000,10000)/10000*self.circle_speed
                        ])
                        
                        self.vector_spee = Vec2_(self.vector_speed)
                        
                        if self.shape != 'i':
                            if self.color_randoming == True and type(self.shape_color)==list and len(self.shape_color)>1:
                                color = self.shape_color[random.randint(0,len(self.shape_color)-1)]
                            else:
                                color = self.shape_color[self.color_index]
                            if self.shape_color == 'r':
                                color =Color_._rgb('r','r','r').COLOR
                            particle = [pos,self.cirkul_spee,self.shape_widt,self.vector_spee,self.life_time,color,0]
                                        
                        else:
                            color = None
                            if self.image_rotating:
                                rotate = random.randint(-self.image_rotating_delta,self.image_rotating_delta)
                            else:
                                rotate = 0
                            
                            if self.randoming_image:
                                ri = random.randint(0,len(self.img)-1)
                                img = self.img[ri]
                                
                                rect = self.img[ri].img.get_rect(center = pos.vector.xy)
                                particle = [pos,self.cirkul_spee,self.shape_widt,self.vector_spee,self.life_time,color,rotate,0,rect,img]
                            else:
                                rect = self.img.img.get_rect(center = pos.vector.xy)
                                particle = [pos,self.cirkul_spee,self.shape_widt,self.vector_spee,self.life_time,color,rotate,0,rect]

                        

                        self.particles.append(particle)

        def Render(self):
            if self.start_render:
                for i in range(len(self.particles)):

                    





                    if self.shape == 'r':

                        self.surf.GL.Rect(self.particles[i][5],[self.particles[i][0].vector.x-self.particles[i][2]/2,self.particles[i][0].vector.y-self.particles[i][2]/2],[self.particles[i][2],self.particles[i][2]],0,'s','D')
                    elif self.shape == 'c':

                        self.surf.GL.Circle(self.particles[i][5],self.particles[i][0].vector.xy,self.particles[i][2],0,'s','D')
                    elif self.shape == 'i':
                        if self.randoming_image:
                            
                            image = copy(self.particles[i][9])
                        else:
                            image = copy(self.img)
                        
                        
                        image.Set_pos([self.particles[i][0].vector.x-self.particles[i][2]/2,self.particles[i][0].vector.y-self.particles[i][2]/2])
                        if self.particles[i][2]>0:
                            image.Scale([self.particles[i][2],self.particles[i][2]])
                            new_image = pygame.transform.rotate(image.img,self.particles[i][7])
                            self.particles[i][8] = new_image.get_rect(center=[self.particles[i][8].center[0]+self.particles[i][0].vector.x-self.particles[i][8].center[0],self.particles[i][8].center[1]+self.particles[i][0].vector.y-self.particles[i][8].center[1]])
                            
                            
                            
                            self.surf.screen.blit(new_image,self.particles[i][8])


                    if self.lighting:
                        
                        if self.light_radius_resize:
                            s1 = GL.Surfases_([self.particles[i][2]*4,self.particles[i][2]*4],[self.particles[i][0].vector.x-self.particles[i][2]*2,self.particles[i][0].vector.y-self.particles[i][2]*2],None,self.light_alpha,GL.S_Blend)
                            if self.lighting_color=='shape_color':self.surf.GL.Circle([self.mult(self.particles[i][5][0]-self.light_color_dispers),self.mult(self.particles[i][5][1]-self.light_color_dispers),self.mult(self.particles[i][5][2]-self.light_color_dispers)],[self.particles[i][2]*2,self.particles[i][2]*2],self.particles[i][2]*2,0,s1.screen,'D')
                            else:self.surf.GL.Circle(self.lighting_color,[self.particles[i][2]*2,self.particles[i][2]*2],self.particles[i][2]*2,0,s1.screen,'D')
                            s1.DRAW_(self.surf.screen)
                        else:
                            if not self.light_radius_clip_in_shape_rad:
                                s1 = GL.Surfases_([self.light_radius*2,self.light_radius*2],[self.particles[i][0].vector.x-self.light_radius,self.particles[i][0].vector.y-self.light_radius],None,self.light_alpha,GL.S_Blend)
                                if self.lighting_color=='shape_color':self.surf.GL.Circle([self.mult(self.particles[i][5][0]-self.light_color_dispers),self.mult(self.particles[i][5][1]-self.light_color_dispers),self.mult(self.particles[i][5][2]-self.light_color_dispers)],[self.light_radius,self.light_radius],self.light_radius,0,s1.screen,'D')  
                                else:self.surf.GL.Circle(self.lighting_color,[self.light_radius,self.light_radius],self.light_radius,0,s1.screen,'D')  
                                s1.DRAW_(self.surf.screen)
                            else:
                                s1 = GL.Surfases_([self.mult(self.particles[i][2]*2+self.light_radius*2),self.mult(self.particles[i][2]*2+self.light_radius*2)],[self.particles[i][0].vector.x-(self.light_radius+self.particles[i][2]),self.particles[i][0].vector.y-(self.light_radius+self.particles[i][2])],None,self.light_alpha,GL.S_Blend)
                                if self.lighting_color=='shape_color':self.surf.GL.Circle([self.mult(self.particles[i][5][0]-self.light_color_dispers),self.mult(self.particles[i][5][1]-self.light_color_dispers),self.mult(self.particles[i][5][2]-self.light_color_dispers)],[self.light_radius+self.particles[i][2],self.light_radius+self.particles[i][2]],self.light_radius+self.particles[i][2],0,s1.screen,'D')  
                                else:self.surf.GL.Circle(self.lighting_color,[self.light_radius+self.particles[i][2],self.light_radius+self.particles[i][2]],self.light_radius+self.particles[i][2],0,s1.screen,'D')  
                                s1.DRAW_(self.surf.screen)
        
                    if self.soed_part_lines:
                        if self.coed_part_lines_centered:
                            
                                self.surf.GL.Line(self.particles[i][5],self.particles[i][0].vector.xy,self.end_line_pos,int(self.particles[i][2]+self.coed_part_lines_add),'s','S','D')
                        else:
                            if len(self.particles)-i<len(self.particles):
                                self.surf.GL.Line(self.particles[i][5],self.particles[i][0].vector.xy,self.particles[i-1][0].vector.xy,int(self.particles[i][2]+self.coed_part_lines_add),'s','S','D')

        def Focus(self):
            if self.start_focus:
                if self.rotate_gravity:
                    self.gravity.Rotate(self.rotating_gravity_angle)
                for i in range(len(self.particles)):
                    if self.rotate_in_center:
                        self.particles[i][1].Rotate(self.rotating_in_center_angle)
                    
                    self.particles[i][1].vector += self.gravity.vector

                    if self.move_point_set:    
                        sx = -(self.particles[i][0].pos1[0]-self.move_point[0])/self.move_point_speed
                        sy = -(self.particles[i][0].pos1[1]-self.move_point[1])/self.move_point_speed
                        if GL_MATH.Math_().RAST(self.particles[i][0].vector.xy,self.move_point)<self.move_radius:
                            sx*=self.move_radius_delta_x
                            sy*=self.move_radius_delta_y
                        
                        sv = GL_MATH.Vec2_([sx,sy])
                        self.particles[i][0].vector += sv.vector
                    if self.image_rotating:
                        self.particles[i][7]+=self.particles[i][6]
                    
                        

                    self.particles[i][1].vector+=self.particles[i][3].vector
                    self.particles[i][0].vector += self.particles[i][1].vector

                    self.particles[i][4]-=self.life_delta
                    if self.size_resize:
                        if self.return_size:  
                            if self.particles[i][2]<=self.shape_max_size+10:
                                self.particles[i][2]+=self.size_deller
                        else:
                            self.particles[i][2]-=self.size_deller

                    if self.image_rotate_in_position:
                        center_pos = GL_MATH.Vec2_([self.posx-self.particles[i][0].vector.x,self.posy-self.particles[i][0].vector.y])
                        self.particles[i][7]=-int(self.particles[i][0].Angle_to(center_pos))+300

                    if self.image_rotate_in_vector:
                        
                        #speed_pos = GL_MATH.Vec2_([self.particles[i][1].vector.x+self.particles[i][0].vector.x,self.particles[i][1].vector.y+self.particles[i][0].vector.y])
                        self.particles[i][7]=-int(self.particles[i][0].Angle_to(self.particles[i][1]))+125
        def Xclean(self):
            if self.start_delete:
                for i in range(len(self.particles)):
                    if self.particles[i][1].vector.xy==[0,0]:
                        del self.particles[i]
                        break

                for i in range(len(self.particles)):
                    if self.surf.IN_WINDOW(self.particles[i][0].vector.xy):
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

        def Move(self,speed):
            self.posx+=speed[0]
            self.posy+=speed[1]
            
            for i in range(len(self.particles)):
                self.particles[i][0].vector.x+=speed[0]
                self.particles[i][0].vector.y+=-speed[1]
        
        def P(self):
            self.Emiter()
            self.Focus()
            self.Render()
            self.Xclean()

        def Get_data(self):
            print(f'''particle emmiter
| id {self.id},
| particle_count {len(self.particles)},
| rect [ x:{self.posx},y:{self.posy},w:{self.width},h:{self.height} ],
| shape [ type:'{self.shape}',size:{self.shape_widt} ],
| shape colors {self.shape_color},
| color randoming {self.color_randoming}
| color index {self.color_index}
| gravity {self.gravity.vector.xy},
| vector speed {self.vector_speed},
| circle speed {self.circle_speed},
| rotating in center [bool:{self.rotate_in_center},angle:{self.rotating_in_center_angle}],
| rotating gravity   [bool:{self.rotate_gravity},angle:{self.rotating_gravity_angle}],
| lightning {self.lighting},
    | light dispers {self.light_color_dispers},
    | light radius {self.light_radius},
    | light color [ {self.lighting_color} ],
    | light radius clip in shape radius {self.light_radius_clip_in_shape_rad},
    | light radius resize {self.light_radius_resize}


''')

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