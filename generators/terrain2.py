from opensimplex.opensimplex import OpenSimplex
from random import randint

def initialize(world):
    f=open('worlds/'+world+'/seed','w')
    f.write(str(randint(-1000000000,1000000000)))
    f.close()

    f=open('worlds/'+world+'/seed2','w')
    f.write(str(randint(-1000000000,1000000000)))
    f.close()

def load(world):
    global noise, noise2
    noise = OpenSimplex(seed=int(open('worlds/'+world+'/seed').read()))
    noise2 = OpenSimplex(seed=int(open('worlds/'+world+'/seed2').read()))

def generate(cx,cy,cz):
    data=[]
    for z in xrange(cz*8,cz*8+8):
        for y in xrange(cy*8,cy*8+8):
            for x in xrange(cx*8,cx*8+8):
                if y < noise2.noise2d(x/96.,z/96.)*100:
                    data.append(blocks.Stone(x,y,z))
                elif y < noise.noise2d(x/128.,z/128.)*10:
                    data.append(blocks.Grass(x,y,z))
                else:
                    data.append(None)
    return data

def features(cx,cy,cz,world):
    pass
