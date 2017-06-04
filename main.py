import os
import imp
from util import yn, Box
from game import Game
import pyglet

wide_range = (-4,5)
do_wide = yn(
    'Do you wish to load more chunks? This is recommended\nonly if you are using pypy and/or a powerful computer. '
)
deletion_range = 10 if do_wide else 5
OFFSETS = []
for z in xrange(*wide_range):
    for y  in xrange(*wide_range):
        for x in xrange(*wide_range):
            OFFSETS.append((x,y,z))

CLOSE_OFFSETS = []
for z in xrange(-1,2):
    for y in xrange(-1,2):
        for x in xrange(-1,2):
            CLOSE_OFFSETS.append((x,y,z))
            OFFSETS.remove((x,y,z))

offset_information = Box(
    do_wide=do_wide,
    wide=OFFSETS,
    close=CLOSE_OFFSETS,
    deletion_range=deletion_range
)

if not os.path.isdir('worlds'):
    os.mkdir('worlds')

world = raw_input('Pick your world: ')

if world not in os.listdir('worlds'):
    print 'Creating the world...'
    os.mkdir('worlds/'+world)
    gen_list = filter(lambda n: not n.startswith('_'),
                      [os.path.splitext(n)[0] for n in os.listdir('generators')]
                      )
    print 'Available generators: ',', '.join(gen_list)
    generator = raw_input('Select a generator: ') +'.py'
    open('worlds/'+world+'/generator','w').write(generator)
    generator = imp.load_source('generator','generators/'+generator)
    generator.initialize(world)
else:
    generator = imp.load_source('generator','generators/'+open('worlds/'+world+'/generator').read())

generator.load(world)

game = Game(world,generator,offset_information)

pyglet.app.run()
