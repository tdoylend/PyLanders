import pyglet
from pyglet.gl import *
from random import *
from pyglet.window import key
from math import *
import os
import cPickle as pickle
#from opensimplex.opensimplex import OpenSimplex

OFFSETS = []
for z in xrange(-2,3):
    for y  in xrange(-1,2):
        for x in xrange(-2,3):
            OFFSETS.append((x,y,z))

SKY_COLOR = 0.45, 0.7, 1.0

def cmult((r,g,b),f):
    return r*f,g*f,b*f

def sign(n):
    return -1 if n < 0 else 1


class Block:
    name='block'
    transparent=False
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        if isinstance(self.x,float) or isinstance(self.y,float) or isinstance(self.z,float):
            raise StandardError('FOUL PLAY!')

        self.spec_init()

    def save_data(self):
        return self.x,self.y,self.z

    def get_selectbox_vertices(self,scale=0.502):
        return (self.x - scale, self.y - scale, self.z - scale, #BACK
                self.x + scale, self.y + scale, self.z - scale,
                self.x + scale, self.y - scale, self.z - scale,
                self.x - scale, self.y + scale, self.z - scale,

                self.x + scale, self.y - scale, self.z - scale, #RIGHT
                self.x + scale, self.y + scale, self.z + scale,
                self.x + scale, self.y - scale, self.z + scale,
                self.x + scale, self.y + scale, self.z - scale,

                self.x - scale, self.y + scale, self.z - scale, #TOP
                self.x + scale, self.y + scale, self.z + scale,
                self.x + scale, self.y + scale, self.z - scale,
                self.x - scale, self.y + scale, self.z + scale,

                self.x - scale, self.y - scale, self.z - scale, #LEFT
                self.x - scale, self.y + scale, self.z - scale,
                self.x - scale, self.y - scale, self.z + scale,
                self.x - scale, self.y + scale, self.z + scale,

                self.x + scale, self.y - scale, self.z + scale, #FRONT
                self.x - scale, self.y - scale, self.z + scale,
                self.x + scale, self.y + scale, self.z + scale,
                self.x - scale, self.y + scale, self.z + scale,

                self.x - scale, self.y + scale, self.z - scale, #WALTZ
                self.x - scale, self.y - scale, self.z - scale,

                self.x + scale, self.y - scale, self.z + scale,
                self.x + scale, self.y - scale, self.z - scale,
                self.x - scale, self.y - scale, self.z + scale,
                self.x - scale, self.y - scale, self.z - scale,

                self.x + scale, self.y - scale, self.z - scale
                )

    def get_vertices(self,top=True,bottom=True,left=True,right=True,back=True,front=True,scale=0.5):
        #Assumes GL_QUADS
        return ((self.x - scale, self.y - scale, self.z - scale,   #BACK
                self.x + scale, self.y - scale, self.z - scale,
                self.x + scale, self.y + scale, self.z - scale,
                self.x - scale, self.y + scale, self.z - scale) if back else ()) + \
                ((self.x - scale, self.y - scale, self.z + scale,   #FRONT
                self.x + scale, self.y - scale, self.z + scale,
                self.x + scale, self.y + scale, self.z + scale,
                self.x - scale, self.y + scale, self.z + scale) if front else ()) + \
                ((self.x - scale, self.y - scale, self.z - scale,   #LEFT
                self.x - scale, self.y - scale, self.z + scale,
                self.x - scale, self.y + scale, self.z + scale,
                self.x - scale, self.y + scale, self.z - scale) if left else ()) + \
                ((self.x + scale, self.y - scale, self.z - scale,   #RIGHT
                self.x + scale, self.y - scale, self.z + scale,
                self.x + scale, self.y + scale, self.z + scale,
                self.x + scale, self.y + scale, self.z - scale) if right else ()) + \
                ((self.x - scale, self.y - scale, self.z - scale,   #BOTTOM
                self.x + scale, self.y - scale, self.z - scale,
                self.x + scale, self.y - scale, self.z + scale,
                self.x - scale, self.y - scale, self.z + scale) if bottom else ()) + \
                ((self.x - scale, self.y + scale, self.z - scale,   #TOP
                self.x + scale, self.y + scale, self.z - scale,
                self.x + scale, self.y + scale, self.z + scale,
                self.x - scale, self.y + scale, self.z + scale) if top else ())             

    def get_colors(self):
        return cmult(self.color,0.5)*4 + \
               cmult(self.color,0.7)*4 + \
               cmult(self.color,0.6)*4 + \
               cmult(self.color,0.8)*4 + \
               cmult(self.color,0.3)*4 + \
               cmult(self.color,1.0)*4

class Grass(Block):
    name='grass'
    def spec_init(self):
        self.color = (0+random()*0.1,0.5+random()*0.1,0+random()*0.1)

class Stone(Block):
    name='stone'
    def spec_init(self):
        self.color = (0.3,0.3,0.3)

class Trunk(Block):
    name = 'trunk'
    def spec_init(self):
        self.color = (0.5,0.3,0.0)

names = {
    'block': Block,
    'grass': Grass,
    'stone': Stone,
    'trunk': Trunk,
    }

class Chunk:
    def __init__(self,position,initial_data=[None]*512):
        self.grid = initial_data
        self.position = position
        self.recompile()

    def set_block(self,x,y,z,block):
        self.grid[z * 64 + y * 8 + x] = block
        self.recompile()

    def get_block(self,x,y,z):
        return self.grid[z*64 + y * 8 + x]

    def recompile(self):
        vertices = []
        colors = []
        for z in xrange(8):
            for y in xrange(8):
                for x in xrange(8):
                    block = self.grid[z*64+y*8+x]
                    if block is not None:
                        vertices.extend(block.get_vertices())
                        colors.extend(block.get_colors())

        #print vertices
        #print colors

        if not vertices:
            self.list = None
        else:
            self.list = pyglet.graphics.vertex_list(len(vertices)//3,
                                                    ('v3f',vertices),
                                                    ('c3f',colors)
                                                    )

    def draw(self):
        if not self.list:
            pass
        else:
            self.list.draw(GL_QUADS)

class Player:
    def __init__(self,x,y,z):
        self.x,self.y,self.z = x,y,z
        self.angle_y = 0
        self.angle_x = 0
        self.vel_y = 0
        self.current_block = Stone

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
            
class Game:
    def __init__(self,world):
        self.window = pyglet.window.Window(fullscreen=True)
        self.window.push_handlers(self)

        self.chunks = {}
        self.player = Player(0,0,0)

        self.window.set_exclusive_mouse(True)

        self.keys = key.KeyStateHandler()
        self.window.push_handlers(self.keys)

        pyglet.clock.schedule(self.update)

        glClearColor(0.3,0.5,1.0,1.0)

        self.off_number = 0

        self.key_listing = self.chunks.keys()

        self.world = world

        self.fps_display = pyglet.clock.ClockDisplay()

    def update(self,dt):
        self.motion_amount = dt * 5
        w=self.keys[key.W];a=self.keys[key.A];s=self.keys[key.S];d=self.keys[key.D]

        if self.keys[key.R]:
            self.player.y += self.motion_amount
        elif self.keys[key.F]:
            self.player.y -= self.motion_amount
        #old_position = self.player.x,self.player.y,self.player.z
        
        if w&a:
            self.player.apply_motion(self,self.motion_amount,45)
        elif w&d:
            self.player.apply_motion(self,self.motion_amount,-45)
        elif s&d:
            self.player.apply_motion(self,self.motion_amount,-135)
        elif s&a:
            self.player.apply_motion(self,self.motion_amount,135)
        elif w:
            self.player.apply_motion(self,self.motion_amount)
        elif s:
            self.player.apply_motion(self,self.motion_amount,180)
        elif a:
            self.player.apply_motion(self,self.motion_amount,90)
        elif d:
            self.player.apply_motion(self,self.motion_amount,-90)

        player_chunk = (int(self.player.x//8),int(self.player.y//8),int(self.player.z//8))

        self.off_number += 1
        self.off_number %= len(OFFSETS)
        off = OFFSETS[self.off_number]
        self.check_and_load(player_chunk[0]+off[0],player_chunk[1]+off[1],player_chunk[2]+off[2])

        if not self.key_listing:
            self.key_listing = self.chunks.keys()


        to_check = self.key_listing.pop()

        dx = to_check[0] - player_chunk[0]
        dy = to_check[1] - player_chunk[1]
        dz = to_check[2] - player_chunk[2]

        if sqrt(dx*dx+dy*dy+dz*dz) > 5:
            self.unload(*to_check)

    def unload(self,cx,cy,cz):
        data = []
        chunk = self.chunks[(cx,cy,cz)]
        for block in chunk.grid:
            if block:
                data.append((block.name,block.save_data()))
            else:
                data.append(None)
        f=open('worlds/'+self.world+'/'+str(cx)+' '+str(cy)+' '+str(cz),'wb')

        pickle.dump(data,f,-1)
        f.close()
        del self.chunks[(cx,cy,cz)]

    def check_and_load(self,cx,cy,cz):
        player_chunk = (cx,cy,cz)
        if player_chunk not in self.chunks:
            chunk_listing = os.listdir('worlds/'+self.world)
            if (str(cx)+' '+str(cy)+' '+str(cz)) in chunk_listing:
                data = []
                f = open('worlds/'+self.world+'/'+str(cx)+' '+str(cy)+' '+str(cz),'rb')
                d = pickle.load(f)
                f.close()
                for item in d:
                    if item is None:
                        data.append(None)
                    else:
                        data.append(names[item[0]](*item[1]))
                gen_features=False
            else:
                gen_features = True
                data = []
                for z in xrange(8):
                    for y in xrange(8):
                        for x in xrange(8):
                            if (player_chunk[1]*8+y) == -3:
                                #print player_chunk, x,y,z
                                data.append(Grass(player_chunk[0]*8+x,player_chunk[1]*8+y,player_chunk[2]*8+z))
                            #elif (player_chunk[1]*8+y) < -2:
                            #    data.append(Stone(player_chunk[0]*8+x,player_chunk[1]*8+y,player_chunk[2]*8+z))
                            else:
                                data.append(None)
            #print data
            self.chunks[player_chunk] = Chunk(player_chunk,data)
            if gen_features and not randint(0,3):
                if player_chunk[1] == 0:
                    tree = player_chunk[0]*8+randint(0,7),-2,player_chunk[2]*8+randint(0,7)
                    self.set_block(tree[0],tree[1],tree[2],Trunk(tree[0],tree[1],tree[2]))
                    self.set_block(tree[0],tree[1]+1,tree[2],Trunk(tree[0],tree[1]+1,tree[2]))
                    tree = (tree[0],tree[1]+3,tree[2])
                    for off_x in xrange(tree[0]-1,tree[0]+2):
                        for off_y in xrange(tree[1]-1,tree[1]+2):
                            for off_z in xrange(tree[2]-1,tree[2]+2):
                                self.set_block(off_x,off_y,off_z,Grass(off_x,off_y,off_z))
            
    def set_3d(self):
        width,height = self.window.width,self.window.height
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(65, width / float(height), .1, 1000)
        glMatrixMode(GL_MODELVIEW)

    def set_2d(self):
        width,height = self.window.width,self.window.height
        glViewport(0, 0, width, height)
        glMatrixMode(gl.GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)
        glMatrixMode(gl.GL_MODELVIEW)

    def set_block(self,x,y,z,block):
        chunk = (x//8,y//8,z//8)
        inner = (x%8, y%8, z%8 )

        if chunk not in self.chunks:
            self.check_and_load(*chunk)

        self.chunks[chunk].set_block(*inner,block=block)

    def get_block(self,x,y,z):
        chunk = (x//8,y//8,z//8)
        inner = (x%8, y%8, z%8 )

        if chunk not in self.chunks:
            return None
        else:
            return self.chunks[chunk].get_block(*inner)
        
    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        self.set_3d()
        self.player.transform()
        glEnable(GL_FOG)
        glFogi(GL_FOG_MODE, GL_LINEAR)
        glFogf(GL_FOG_START, 2.0)
        glFogf(GL_FOG_END, 40.0)
        glFogfv(GL_FOG_COLOR,(GLfloat*3)(0.3,0.5,1.0))
        
        for chunk in self.chunks.itervalues():
            chunk.draw()
        b = self.cast_ray()
        if b:
            glLineWidth(2.0)
##            #print b.x,b.y,b.z
            glColor3f(0,0,0)

            glBegin(GL_LINE_STRIP)
            v = b.get_selectbox_vertices()
            for index in xrange(0,len(v),3):
                glVertex3f(v[index],v[index+1],v[index+2])
            glEnd()
##            glVertex3f(b.x-scale,b.y+0.6,b.z-scale)
##            glVertex3f(b.x+scale,b.y+0.6,b.z-scale)
##            glVertex3f(b.x+scale,b.y+0.6,b.z+scale)
##            glVertex3f(b.x-scale,b.y+0.6,b.z+scale)
##            glEnd()
        glDisable(GL_FOG)
        self.set_2d()
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)
        glColor3f(1,1,1)
        glBegin(GL_LINES)
        cx,cy = self.window.width//2,self.window.height//2
        glVertex2f(cx-10,cy)
        glVertex2f(cx+10,cy)
        glVertex2f(cx,cy-10)
        glVertex2f(cx,cy+10)
        glEnd()
        self.fps_display.draw()

    def as_ints(self,x,y,z):
        return int(round(x)),int(round(y)),int(round(z))

    def cast_ray(self):
        vx = -sin(radians(self.player.angle_y)) * cos(radians(self.player.angle_x)) / 100.0
        vy = sin(radians(self.player.angle_x)) / 100.0
        vz = -cos(radians(self.player.angle_y)) * cos(radians(self.player.angle_x)) / 100.0
        #print vx,vy,vz
        px,py,pz = self.player.x,self.player.y,self.player.z

        for _ in xrange(1500):
            r= self.get_block(*self.as_ints(px,py,pz))
            if r:
                return r
            px += vx
            py += vy
            pz += vz
        return None

    def cast_to_side(self):
        vx = -sin(radians(self.player.angle_y)) * cos(radians(self.player.angle_x)) / 100.0
        vy = sin(radians(self.player.angle_x)) / 100.0
        vz = -cos(radians(self.player.angle_y)) * cos(radians(self.player.angle_x)) / 100.0
        #print vx,vy,vz
        px,py,pz = self.player.x,self.player.y,self.player.z

        for _ in xrange(1500):
            r= self.get_block(*self.as_ints(px,py,pz))
            if r:
                dx,dy,dz = (px-r.x,py-r.y,pz-r.z)
                if abs(dx) > max(abs(dy),abs(dz)):
                    return r.x+sign(dx),r.y,r.z
                elif abs(dy) > max(abs(dx),abs(dz)):
                    return r.x,r.y+sign(dy),r.z
                else:
                    return r.x,r.y,r.z+sign(dz)
                
            px += vx
            py += vy
            pz += vz
        return None
        
    def on_mouse_motion(self,x,y,dx,dy):
        self.player.angle_y -= dx *0.87 #NOTE: These are reserved.
        self.player.angle_x += dy *0.87
        self.player.angle_x = max(min(self.player.angle_x, 90),-90)

    def on_mouse_press(self,x,y,button,modifiers):
        if button == pyglet.window.mouse.LEFT:
            b = self.cast_ray()
            if b is not None:
                
                self.set_block(b.x,b.y,b.z,None)
        elif button == pyglet.window.mouse.RIGHT:
            b = self.cast_to_side()
            if b is not None:
                self.set_block(b[0],b[1],b[2],self.player.current_block(b[0],b[1],b[2]))

    def on_close(self):
        for chunk in self.chunks.keys():
            self.unload(*chunk)

if not os.path.isdir('worlds'):
    os.mkdir('worlds')

world = raw_input('Pick your world: ')

if world not in os.listdir('worlds'):
    print 'Creating the world...'
    os.mkdir('worlds/'+world)

game = Game(world)

pyglet.app.run()
