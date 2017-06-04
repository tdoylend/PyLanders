def initialize(world):
    pass

def generate(cx,cy,cz):
    data=[]
    for z in xrange(cz*8,cz*8+8):
        for y in xrange(cy*8,cy*8+8):
            for x in xrange(cx*8,cx*8+8):
                if y == -3:
                    data.append(blocks.Grass(x,y,z))
                elif y < -3:
                    data.append(blocks.Stone(x,y,z))
                else:
                    data.append(None)
    return data


def load(world):
    pass

def features(cx,cy,cz,world): pass
