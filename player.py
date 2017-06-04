from pyglet.gl import glRotated, glTranslated
from math import sin, cos, radians

class Player:
    def __init__(self,x,y,z,current_block):
        self.x,self.y,self.z = x,y,z
        self.angle_y = 0
        self.angle_x = 0
        self.vel_y = 0
        self.current_block = current_block
        
    def transform(self):
        #glLoadIdentity()
        glRotated(-self.angle_x,1,0,0)
        glRotated(-self.angle_y,0,1,0)
        glTranslated(-self.x,-self.y,-self.z)
        
    def apply_motion(self,world,amount,angle=0):
        old_position = self.x,self.y,self.z
        self.x -= sin(radians(self.angle_y+angle)) * amount
        #if world.get_block(*world.as_ints(self.x,self.y,self.z)):
        #    self.x,self.y,self.z = old_position
        self.z -= cos(radians(self.angle_y+angle)) * amount
        #if world.get_block(*world.as_ints(self.x,self.y,self.z)):
        #    self.x,self.y,self.z = old_position
