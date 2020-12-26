import time
import board
import neopixel
import re
import math
import random

AMOUNT_OF_FIREWORKS = 0.05   # Percentage change of new firework each frame
GRAVITY = [0, 0.2]          # Speed in which the firework will fall
WIDTH_TREE = 200            # Width of tree 
HEIGHT_TREE = 300           # Height of tree 
AMOUNT_OF_DETAIL = 20       # Distance between firework and led, for which the Led will still light up

def xmaslight():
    #Read in data
    coordfilename = "Python/coords.txt"

    fin = open(coordfilename,'r')
    coords_raw = fin.readlines()

    coords_bits = [i.split(",") for i in coords_raw]

    coords = []

    for slab in coords_bits:
        new_coord = []
        for i in slab:
            new_coord.append(int(re.sub(r'[^-\d]','', i)))
        coords.append(new_coord)

        
    #set up the pixels (AKA 'LEDs')
    PIXEL_COUNT = len(coords) # this should be 500

    #pixels = neopixel.NeoPixel(board.D18, PIXEL_COUNT, auto_write=False)

    #array to keep all the firework objects
    fireworks = []
    # a buffer so it does not hit to extreme top or bottom of the tree
    buffer = 200
    
    # pause between cycles (normally zero as it is already quite slow)
    slow = 0

    while True:
        if (random.random() < AMOUNT_OF_FIREWORKS):
            fireworks.append(Firework())

        for i in reversed(range(len(fireworks))):
            f = fireworks[i]
            f.run()
            if f.done():
                del fireworks[i]
        time.sleep(slow)

        for firework in fireworks:
            for particle in firework.particles:
                for LED in range(len(coords)):
                    distance = math.sqrt((particle.location[0] - coords[LED][0])**2 + (particle.location[1]- coords[LED][1])**2 + (particle.location[2] - coords[LED][2])**2)
                    if distance < AMOUNT_OF_DETAIL:
                        pixels[LED] = firework.color

        # use the show() option as rarely as possible as it takes ages
        # do not use show() each time you change a LED but rather wait until you have changed them all
        pixels.show()  

class Firework:

    def __init__(self):
        self.hu = random.uniform(0, 255)
        self.firework = Particle([random.uniform(0,-WIDTH_TREE/2), random.uniform(0,WIDTH_TREE/2), random.uniform(0,HEIGHT_TREE/2)], self.hu)
        self.particles = []


    def done(self):
        if self.firework == None and not self.particles:
            return True
        else:
            return False


    def run(self):
        if self.firework is not None:
            self.firework.applyForce(GRAVITY)
            self.firework.update()

            if self.firework.explode():
                for i in range(750):
                    self.particles.append(Particle(self.firework.location, self.hu));   
                self.firework = None

        for i in reversed(range(len(self.particles))):
            p = self.particles[i]
            p.applyForce(GRAVITY)
            p.run()
            if p.isDead():
                del self.particles[i]


    def dead(self):
        if not self.particles:
            return True
        else:
            return False


class Particle:
    def __init__(self,x,y,z,h):
        self.hu = h
        self.acceleration = [0,0]
        self.velocity = [0, random(-25, -10), 0]
        self.location =  [x,y,z]
        self.seed = False
        self.lifespan = 255


    def __init__(self, l, h):
        self.hu = h
        self.color = [random.uniform(0,255),random.uniform(0,255),random.uniform(0,255)]
        self.acceleration = [0, 0,0]
        self.velocity = [random.uniform(-1,1),random.uniform(-1,1),random.uniform(-1,1)]
        random_number = random.uniform(8, 16)
        self.velocity[0] *= random_number
        self.velocity[1] *= random_number
        self.velocity[2] *= random_number
        self.location = [0,0,0]
        self.location[0] = l[0]
        self.location[1] = l[1]
        self.location[2] = l[2]
        self.lifespan = 255
        self.seed = True


    def applyForce(self,force):
        self.acceleration[0] += force[0]
        self.acceleration[1] += force[1]


    def run(self):
        self.update()


    def explode(self):
        if (self.seed and self.velocity[1] > 0):
            self.lifespan = 0
            return True

        return False


    def update(self):

        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]
        self.location[0] += self.velocity[0]
        self.location[1] += self.velocity[1]
        self.location[2] += self.velocity[2]
        if (self.seed):
            self.lifespan -= 5
            self.velocity[0] *= 0.9
            self.velocity[1] *= 0.9
            self.velocity[2] *= 0.9

        self.acceleration[0] *= 0
        self.acceleration[1] *= 0


    def isDead(self) :
        if (self.lifespan < 0):
            return True
        else:
            return False

xmaslight()

