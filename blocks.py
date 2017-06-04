from random import random, randint, randrange

def cmult((r,g,b),f):
    return r*f,g*f,b*f

class Block:
    name='block'
    transparent=False
    invent_color = (0,0,0)
    
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        if isinstance(self.x,float) or isinstance(self.y,float) or isinstance(self.z,float):
            raise StandardError('FOUL PLAY!')

        self.spec_init()

    def spec_init(self):
        self.color = (0,0,0)

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

    def get_colors(self,top=True,bottom=True,left=True,right=True,front=True,back=True):
        return ((cmult(self.color,0.5)*4)if back else ()) + \
               ((cmult(self.color,0.7)*4)if front else ()) + \
               ((cmult(self.color,0.6)*4)if left else ()) + \
               ((cmult(self.color,0.8)*4)if right else ()) + \
               ((cmult(self.color,0.3)*4)if bottom else ()) + \
               ((cmult(self.color,1.0)*4)if top else ())

class Grass(Block):
    name='grass'
    invent_color = (0.0,0.5,0.0)
    def spec_init(self):
        self.color = (0+random()*0.1,0.5+random()*0.1,0+random()*0.1)

class Stone(Block):
    name='stone'
    invent_color = (0.3,0.3,0.3)
    def spec_init(self):
        self.color = (0.3,0.3,0.3)

class Trunk(Block):
    name = 'trunk'
    invent_color = 0.5,0.3,0.0
    def spec_init(self):
        self.color = (0.5,0.3,0.0)

class Cloth(Block):
    name = '*_cloth'
    invent_color = 0.2,0.2,0.2
    def spec_init(self): self.color = self.invent_color

class RedCloth(Cloth):
    name = 'red_cloth'
    invent_color = 0.6,0.05,0.05

class GreenCloth(Cloth):
    name = 'green_cloth'
    invent_color = 0.05,0.6,0.05

class OrangeCloth(Cloth):
    name = 'orange_cloth'
    invent_color = 0.6, 0.25, 0.05

class YellowCloth(Cloth):
    name = 'yellow_cloth'
    invent_color = 0.6,0.6,0.05

class BlueCloth(Cloth):
    name = 'blue_cloth'
    invent_color = 0.05,0.05,0.6

class Marble(Block):
    name = 'marble'
    invent_color = 0.9,0.8,0.8
    def spec_init(self): self.color = 0.9,0.8,0.8

class Cuboids(Block):
    name = 'cuboids'
    cubes = ((0,0,0,0.5,0.5,0.5))
    transparent = True
    def get_vertices(self,**kwargs):
        data = ()
        for cube in self.cubes:
            data += (
                
                ) #TODO: Finish

names = {
    'block': Block,
    'grass': Grass,
    'stone': Stone,
    'trunk': Trunk,
    '*_cloth': Cloth,
    'red_cloth': RedCloth,
    'orange_cloth': OrangeCloth,
    'yellow_cloth': YellowCloth,
    'green_cloth': GreenCloth,
    'blue_cloth': BlueCloth,
    'marble': Marble,
    }

blocks = [
    Block,
    Grass,
    Stone,
    Trunk,
    RedCloth,
    OrangeCloth,
    YellowCloth,
    GreenCloth,
    BlueCloth,
    Marble
    ]
