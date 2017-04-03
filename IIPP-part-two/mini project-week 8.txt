# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
 
WIDTH = 800
HEIGHT = 600
time = 0
ANGLE_VEL_INC = 0.06
score =0
lives = 3
 
 
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
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

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

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# Ship class
class Ship:
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
        
    def shoot(self):
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0],self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0],self.vel[1] + 6 * forward[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius    
    
    def thrusters_on(self):
        self.thrust = True
        ship_thrust_sound.play()
           
    def thrusters_off(self):
        self.thrust = False
        ship_thrust_sound.rewind()
            
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0]*3, self.image_center[1]], self.image_size, self.pos,self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, [self.image_center[0], self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)      
            
    def update(self):    
        self.pos[0] = (self.pos[0] + self.vel[0])%WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1])%HEIGHT
        forward = angle_to_vector(self.angle) 
        self.angle += self.angle_vel
        
        # acceleration in direction of forward vector
        acceleration_factor = 0.15
        if self.thrust:
            self.vel[0] += forward[0] * acceleration_factor
            self.vel[1] += forward[1] * acceleration_factor     
            
        # friction update
        friction_factor = 0.02
        self.vel[0] *= (1 - friction_factor)
        self.vel[1] *= (1 - friction_factor)
    
# Sprite class
class Sprite:
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
        if sound:
            sound.rewind()
            sound.play()
            
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def collide(self, other_object):
        return dist(self.pos, other_object.get_position()) <= self.get_radius() + other_object.get_radius()
        
    def draw(self, canvas):
        global time
        if self.animated:
            center = self.image_center
            canvas.draw_image(self.image, (center[0] + self.age * self.image_size[0], center[1]), self.image_size,self.pos, self.image_size)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.age += 1
    
def new_game():
    global difficulty, show_splash, rock_group, start, lives 
    show_splash = True
    start = False
    rock_group = set([])    
    soundtrack.play()
    difficulty = 1
         
def click(pos):
    global show_splash, start, score, lives
    if 200 < pos[0]< 600 and 150 < pos[1] <450:
        show_splash = False
        start = True
        score = 0
        lives = 3        
       
def process_sprite_group(sprite_group, canvas):
    for sprite in set(sprite_group):
        sprite.draw(canvas)
        sprite.update()
        if sprite.age >= sprite.lifespan:
            sprite_group.remove(sprite)
              
def group_collide(group, ship):
    global lives 
    for obj in set(group):
        if obj.collide(ship):
            explosion = Sprite(ship.pos, ship.vel, 0, 0, explosion_image, explosion_info, explosion_sound)  
            explosion_group.add(explosion)
            explosion_sound.play()
            lives -= 1
            group.remove(obj)
            
def group_group_collide(group1, group2):
    global score, difficulty, lives 
    for obj1 in set(group1):
        for obj2 in set(group2):
            if obj1.collide(obj2):
                explosion = Sprite(obj1.pos, obj1.vel, 0, 0, explosion_image, explosion_info, explosion_sound)
                explosion_group.add(explosion)
                explosion_sound.play()
                group1.remove(obj1)
                score += 1
                difficulty += 0.1                
       
def draw(canvas):
    global time, show_splash, start, lives 
   
    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    # draw and update ship and sprites
    my_ship.draw(canvas)
    my_ship.update()
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    group_collide(rock_group, my_ship)
    group_group_collide(rock_group, missile_group) 
    
    # draw text 
    canvas.draw_text("Lives ", [WIDTH*.05, 50], 20, 'White')
    canvas.draw_text("Score ", [WIDTH*.9, 50], 20, 'White')
    canvas.draw_text(str(lives), [WIDTH*.05, 70], 20, 'White')
    canvas.draw_text(str(score), [WIDTH*.9, 70], 20, 'White')  
    
    # show splash screen
    if show_splash:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH/2, HEIGHT/2], [WIDTH/2, HEIGHT/2])
        start = False        
    # restarts the game
    if lives==0:
        new_game()
   
# timer handler that spawns a rock    
def rock_spawner():
    global start
    if start == True:
        a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
        a_rock.pos = [random.randrange(WIDTH), random.randrange(HEIGHT)] 
        if dist(a_rock.pos, my_ship.pos) > 100:
            if len(rock_group) < 12:
                rock_group.add(a_rock) 
                angle_lower = -0.05 
                angle_upper = 0.06
                rang_vel = angle_upper -  angle_lower      
                lower = -0.3 
                lower *= difficulty
                upper = 0.4 
                upper *= difficulty
                range_vel = upper -lower
                a_rock.angle_vel = random.random() * rang_vel + angle_lower
                a_rock.vel = [random.random()*range_vel + lower ,random.random()*range_vel + lower]
                          
def keydown(key):
    if simplegui.KEY_MAP["right"] == key:
        my_ship.angle_vel += ANGLE_VEL_INC    
    if simplegui.KEY_MAP["left"] == key:
        my_ship.angle_vel -= ANGLE_VEL_INC
    if simplegui.KEY_MAP["up"] == key:
        my_ship.thrusters_on()
    if simplegui.KEY_MAP["down"] == key:
        my_ship.thrusters_on()
    if simplegui.KEY_MAP["space"] == key:
         my_ship.shoot()
           
def keyup(key):
    global thruster, angle_vel
    if simplegui.KEY_MAP["right"] == key:
        my_ship.angle_vel = 0      
    if simplegui.KEY_MAP["left"] == key:
        my_ship.angle_vel = 0        
    if simplegui.KEY_MAP["up"] == key:
        my_ship.thrusters_off() 
    if simplegui.KEY_MAP["down"] == key:
        my_ship.thrusters_off()
        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and sprites
 
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
new_game()