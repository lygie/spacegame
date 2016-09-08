#http://www.codeskulptor.org/#user28_QWf9I1RBxa_190.py
#updated project incoporating fixed missile speed independent of ship speed
#http://www.codeskulptor.org/#user33_viHWOZdJTM_1.py

# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
explosion_group = set([])
started = False


rock = True

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def group_collide(group, other):
    global explosion_group, explosion_image, explosion_info, explosion_sound
    checkList = []
    collisionList = []
    numCollisions = 0
    for i in group:
        checkList.append(i) #just copying the set 'group'
            
    for item in checkList:
        if item.collide(other):
            an_explosion = Sprite(item.pos,[0,0],0,0,explosion_image, explosion_info, explosion_sound)
            explosion_group.add(an_explosion)
            group.remove(item)
            numCollisions += 1
             
    return numCollisions

# Ship class
class Ship:
    global shpos, missile, a_missile, forward
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.c = 0.03
        self.misspos = [5,5]
        self.forward = angle_to_vector(self.angle)
        
    def draw(self,canvas):
        global shpos, forward
            
        if self.pos[0] >= 800:
            self.pos[0] = 0
        if self.pos[0] <0:
            self.pos[0] = 800
        if self.pos[1] >= 600:
            self.pos[1] = 0
        if self.pos[1] <0:
            self.pos[1] = 600    
            
        canvas.draw_image(ship_image,ship_info.get_center(),ship_info.get_size(),self.pos,ship_info.get_size(),self.angle)
          
    
    def update(self):
        self.forward = angle_to_vector(self.angle)
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        
        self.angle += self.angle_vel
        
        self.vel[0] *= (1-self.c)
        self.vel[1] *= (1-self.c)
            
        if self.thrust:
            self.vel[0] += .4*self.forward[0]
            self.vel[1] += .4*self.forward[1]
    def angle_vel_dec(self):
        self.angle_vel -= .1
    def angle_vel_inc(self):
        self.angle_vel += .1
    def ship_get_radius(self):
        return self.radius
    def ship_get_position(self):
        return self.pos
    def shoot(self):
        missForward = [self.forward[0], self.forward[1]]
        missVel = [self.vel[0], self.vel[1]]
       
        
        a_missile = Sprite([-1,-1], [0,0], 0, 0, missile_image, missile_info, missile_sound)

        
        a_missile.pos = [self.pos[0]+ship_info.get_radius()*self.forward[0] + self.vel[0], self.pos[1]+ship_info.get_radius()*self.forward[1] + self.vel[1]]
        a_missile.vel = [5*self.forward[0],5*self.forward[1]]
        a_missile.age = 0
        missile_group.add(a_missile)

        
# Sprite class
class Sprite:
    global shpos, missile, ship_info, forward, my_ship, a_rock, rock
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        self.misspos = [5,5]
        
        self.misspos[0] = my_ship.pos[0]+ship_info.get_radius()*my_ship.forward[0] + self.vel[0]
        self.misspos[1] = my_ship.pos[1]+ship_info.get_radius()*my_ship.forward[1] + self.vel[1]
        
        
        
       # if sound:
       #     sound.rewind()
       #     sound.play()
   
    def draw(self, canvas):
        global rock, a_missile, a_rock, rock_group, missile_group

        if self.pos[0] >= 800:
            self.pos[0] = 0
        if self.pos[0] <0:
            self.pos[0] = 800
        if self.pos[1] >= 600:
            self.pos[1] = 0
        if self.pos[1] <0:
            self.pos[1] = 600
           
        if self.animated:    
            canvas.draw_image(explosion_image, [(self.age%24)*64,64],explosion_info.get_size(),[self.pos[0],self.pos[1]], explosion_info.get_size())
        
        
        
        else:
            if self.lifespan <85:
                
                canvas.draw_image(missile_image,missile_info.get_center(),missile_info.get_size(),[self.pos[0],self.pos[1]] ,missile_info.get_size())
            else:
           
                canvas.draw_image(asteroid_image, asteroid_info.get_center(), asteroid_info.get_size(),[self.pos[0], self.pos[1]],asteroid_info.get_size(), self.angle)
          
        
        
        
            
            
    def sprite_get_radius(self):
        return self.radius
    def sprite_get_position(self):
        return self.pos
        
    def update(self):
        
        if self.age < 85:    
            self.age += 1
        
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle += self.angle_vel        
#        a_rock.pos[0] += a_rock.vel[0]
#        a_rock.pos[1] += a_rock.vel[1]
#        
#        a_rock.angle += a_rock.angle_vel
        
    def collide(self, other):
        if (abs(dist(self.pos, other.pos))<=(self.radius+other.radius)):
            return True
        else:
            return False
        
    
        
        
def draw(canvas):
    global time, started, a_missile, my_ship, lives, score, missile_group, rock_group
    
    # animate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]], 
                                [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2], [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]], 
                                [1.25 * wtime, HEIGHT / 2], [2.5 * wtime, HEIGHT])

    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(rock_group, canvas)
    #a_rock.draw(canvas)
    
    
    #a_missile.draw(canvas)
    
    process_sprite_group(missile_group, canvas)
    
    
    canvas.draw_text("Score",[700,25],25,"White")
    canvas.draw_text("Lives",[25,25],25,'White')
    canvas.draw_text(str(lives), [90,25],25,'White')
    canvas.draw_text(str(score), [700,50],25,'White')
    # update ship and sprites
    my_ship.update()
    #a_rock.update()
    
    #a_missile.update()
            
    if group_collide(rock_group, my_ship ) > 0:
        lives -= 1
        my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

        
    if lives <= 0:
        started = False
        rock_group = set([])
        missile_group = set([])
        timer.stop()
        soundtrack.rewind()
        
    process_sprite_group(explosion_group, canvas)
    
    score += 100*group_group_collide(rock_group, missile_group) 
    
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH/2,HEIGHT/2], splash_info.get_size())
        
        
        
def keydown(key):
    global ship_info, my_ship, missile, forward, missile_group
    if key == simplegui.KEY_MAP['space']:
       if len(missile_group) < 3:
           missile_sound.play()
           my_ship.shoot() 
       print 'ship pos is:', my_ship.pos
       print my_ship.forward 
    if key == simplegui.KEY_MAP['left']:
        #my_ship.angle_vel += -.1
        my_ship.angle_vel_dec()
    if key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel_inc()
        #my_ship.angle_vel += .1
    if key == simplegui.KEY_MAP['up']:
        my_ship.thrust = True
        ship_info.center[0] = 135
        ship_thrust_sound.play()
def keyup(key):
    global ship_info, my_ship, missile
    if key == simplegui.KEY_MAP['up']:
        my_ship.thrust = False
        ship_thrust_sound.rewind()
        ship_info.center[0] = 45
    if key == simplegui.KEY_MAP['left']:
        my_ship.angle_vel = 0
    if key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel = 0  
    if key == simplegui.KEY_MAP['space']:
        missile_sound.rewind()

# timer handler that spawns a rock    
def rock_spawner():
    global a_rock, rock
    #a_rock = Sprite([WIDTH/3, HEIGHT/3], [1,1],random.random()*6.28,rockAngVel,asteroid_image, asteroid_info)

  
    if len(rock_group) <= 12:
        a_rock = Sprite([800*random.random(),600 *random.random()], [1.5*random.randrange(-50,50)/100,1.5*random.randrange(-50,50)/100], 6.28*random.random(), .15*random.randrange(-50,50)/100, asteroid_image, asteroid_info)
        rock_group.add(a_rock)
 


# working way to create a_rock
#    a_rock.pos = [800*random.random(), 600 *random.random()]
#    a_rock.vel = [1.5*random.randrange(-50,50)/100,1.5*random.randrange(-50,50)/100]
#    a_rock.ang = 6.28*random.random()
#    a_rock.angle_vel = .15*random.randrange(-50,50)/100
#
# working way to create a_rock    
    rock = True
def process_sprite_group(group, canvas):
    checkList = []
    for x in group:
        checkList.append(x)
    
    
    for i in checkList:
        if i.age >= 85 and i.lifespan < float('inf'):
            group.remove(i)
        
    for j in group:
        
        j.draw(canvas)
        j.update()

        
def group_group_collide(group1, group2):
    numCollisions2 = 0
    checkList = []
    a = 0
    for i in group1:
        a = numCollisions2
        numCollisions2 += group_collide(group2, i)
        if numCollisions2 > a:
            checkList.append(i)
            explosion_sound.play()
    for x in checkList:
        group1.remove(x)
    return numCollisions2    


def click(pos):
    global lives, score, started
    center = [WIDTH/2, HEIGHT/2]
    size = splash_info.get_size()
    inwidth = (center[0]-size[0]/2 <pos[0] < center[0]+size[0]/2)
    inheight = (center[1]-size[1]/2<pos[1]< center[1]+size[1]/2)
    if not started and inwidth and inheight:
        started = True
        lives = 3
        score = 0
        timer.start()
        soundtrack.play()
        
    
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
#a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
#a_rock = Sprite([-1, -1], [0, 0], 0, 0, asteroid_image, asteroid_info)

rock_group = set([])

#old missile a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)


# Known Working a_missile = Sprite([-1,-1], [0,0], 0, 0, missile_image, missile_info, missile_sound)

missile_group = set([])


# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)

#misstimer = simplegui.create_timer(2000.0, missile_spawner)
# get things rolling

timer.start()
frame.start()

#soundtrack.play()
