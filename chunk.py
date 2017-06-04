import pyglet

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
                        if (x == 0): left=True
                        elif self.get_block(x-1,y,z): left=False
                        else: left=True
                        if (x == 7): right=True
                        elif self.get_block(x+1,y,z): right=False
                        else: right=True
                        if (y == 0): bottom=True
                        elif self.get_block(x,y-1,z): bottom=False
                        else: bottom=True
                        if (y == 7): top=True
                        elif self.get_block(x,y+1,z): top=False
                        else: top=True
                        if (z == 0): back=True
                        elif self.get_block(x,y,z-1): back=False
                        else: back=True
                        if (z == 7): front=True
                        elif self.get_block(x,y,z+1): front=False
                        else: front=True
                        
                        vertices.extend(block.get_vertices(
                            left=left,
                            right=right,
                            top=top,
                            bottom=bottom,
                            back=back,
                            front=front
                        ))
                        colors.extend(block.get_colors(
                            left=left,
                            right=right,
                            top=top,
                            bottom=bottom,
                            back=back,
                            front=front
                        ))

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
            self.list.draw(pyglet.gl.GL_QUADS)
