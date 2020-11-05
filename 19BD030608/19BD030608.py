import pygame,sys,time,random,pika,json,uuid
from threading import Thread

pygame.init()
window = pygame.display.set_mode((800,600))
screen = pygame.Surface((800,600))
pygame.display.set_caption("Tank")

global done 
done = False
global hello
hello = False
global intl 
intl = False

'''Menu'''

class Menu:
    def __init__(self,lists = [360,200,u"Write",(50,250,30),(250,30,250)]):
        self.lists = lists
    
    def render(self,surf,font,num_list):
        for i in self.lists:
            if num_list == i[5]:
                surf.blit(font.render(i[2],1,i[4]),(i[0],i[1]))
            else:
                surf.blit(font.render(i[2],1,i[3]),(i[0],i[1]))
    
    def menu(self):
        font_menu = pygame.font.SysFont("algerian",50)
        pygame.key.set_repeat(0,0)
        pygame.mouse.set_visible(True)
        category = 0
        okey = True
        
        while okey:
            screen.fill((70,50,130))
            pd = pygame.mouse.get_pos()
            for i in self.lists:
                if pd[0]>i[0] and pd[0]<i[0]+155 and pd[1]>i[1] and pd[1]<i[1]+50:
                    category = i[5]
            self.render(screen,font_menu,category)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        sys.exit()
                    if e.key == pygame.K_UP:
                        if category > 0:
                            category-=1
                    if e.key == pygame.K_DOWN:
                        if category < len(self.lists)-1:
                            category+=1
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if category == 0:
                        global done
                        done = True
                        okey = False
                    if category == 1:
                        global hello
                        done = False
                        hello = True
                        okey = False
                    if category == 2:
                        global intl
                        done = False
                        hello = False
                        intl = True
                        okey = False
                    if category == 3:
                        sys.exit()

            window.blit(screen,(0,0)) 
            pygame.display.flip()    
            
lists = [(280,180,u"Single Player",(250,30,25),(170,250,30),0),
          (280,250,u"Multiplayer",(250,30,25),(170,250,30),1),
          (280,320,u"Multiplayer AI",(250,30,25),(170,250,30),2),
          (280,390,u"Quit",(250,30,25),(170,250,30),3)]

game = Menu(lists)       
game.menu()


'''Single Player'''

fps = pygame.time.Clock()
pygame.mixer.music.load("C:\\Users\\user\\Desktop\\19BD030608\\sounds\\fon.wav")
pygame.mixer.music.play(-1,0.0)
pos = pygame.mixer.Sound("C:\\Users\\user\\Desktop\\19BD030608\\sounds\\positive.wav")
neg = pygame.mixer.Sound("C:\\Users\\user\\Desktop\\19BD030608\\sounds\\negativ.wav")
boom = pygame.mixer.Sound("C:\\Users\\user\\Desktop\\19BD030608\\sounds\\vzriv.wav")

class Tank1(object):
    def __init__(self,window):
        self.x1 = 100
        self.y1 = 200
        self.speed = 4
        self.window = window
        self.img = pygame.image.load("C:\\Users\\user\\Desktop\\19BD030608\\img\\enemy.png")
        self.orimg = self.img

    def move(self,dir_t1):
        if dir_t1 == "UP":
            self.orimg = pygame.transform.rotate(self.img,0)
            self.y1-=4
        elif dir_t1 == "DOWN":
            self.orimg = pygame.transform.rotate(self.img,180)
            self.y1+=4
        elif dir_t1 =="LEFT":
            self.orimg = pygame.transform.rotate(self.img,90)
            self.x1-=4
        elif dir_t1 =="RIGHT":
            self.orimg = pygame.transform.rotate(self.img,-90)
            self.x1+=4

    def draw(self):
        self.window.blit(self.orimg,(self.x1,self.y1))

    def range(self):
        if self.x1 >= 768:
            self.x1 = 0
        elif self.x1 <= 0:
            self.x1 = 768
        elif self.y1 >= 608:
            self.y1 = 0
        elif self.y1 <= 0:
            self.y1 = 608        

class Tank2(object):
    def __init__(self,window):
        self.x2 = 600
        self.y2 = 480
        self.speed = 4
        self.window = window
        self.img = pygame.image.load("C:\\Users\\user\\Desktop\\19BD030608\\img\\tank0.png")
        self.orimg = self.img

    def move(self,dir_t2):
        if dir_t2 == "UP":
           self.orimg = pygame.transform.rotate(self.img,0)
           self.y2-=4
        elif dir_t2 == "DOWN":
           self.orimg = pygame.transform.rotate(self.img,180)
           self.y2+=4  
        elif dir_t2 == "LEFT":
           self.orimg = pygame.transform.rotate(self.img,90)
           self.x2-=4
        elif dir_t2 == "RIGHT":
           self.orimg = pygame.transform.rotate(self.img,-90)
           self.x2+=4 
        
    def draw(self):
        self.window.blit(self.orimg,(self.x2,self.y2))
    
    def range(self):
        if self.x2 >= 768:
            self.x2 = 0
        elif self.x2 <= 0:
            self.x2 = 768
        elif self.y2 >= 608:
            self.y2 = 0
        elif self.y2 <= 0:
            self.y2 = 608  

class Bullet(object):
    def __init__(self,window):
        self.x = -8
        self.y = -8
        self.size = 8
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.window = window
        self.strike = False
        self.speed = 19
        i=255
        j=245
        k=225
        self.color = (i,j,k) 

    def shoot(self,dir,x,y):
        self.x = x
        self.y = y
        self.strike = True
        if dir == "UP":
            self.x += 12
            self.up = True
        elif dir == "DOWN":
            self.x += 12
            self.y += 32 
            self.down = True
        elif dir == "LEFT":
            self.y += 12 
            self.left = True
        elif dir == "RIGHT":
            self.y += 12
            self.x += 32 
            self.right = True

    def move(self):
        if self.up:
            self.y -= self.speed
            if self.y <= 0:
                self.up = self.down = self.left = self.right = False
                self.strike = False
                return
        elif self.down:
            self.y += self.speed
            if self.y >= 640:
                self.up = self.down = self.left = self.right = False
                self.strike = False
            return
        elif self.left:
            self.x -= self.speed
            if self.x <= 0:
                self.up = self.down = self.left = self.right = False
                self.strike = False
                return
        elif self.right:
            self.x += self.speed
            if self.x >= 800:
                self.up = self.down = self.left = self.right = False
                self.strike = False
                return

    def draw(self):
        pygame.draw.circle(self.window, self.color, (self.x,self.y),4)

health1 = 3
health2 = 3
stena = pygame.image.load("C:\\Users\\user\\Desktop\\19BD030608\\img\\wall.png")

class STENA(object):
    def __init__(self,window):
        self.window = window
        self.sten = True
        self.stenas = []

    def plus(self):
        if len(self.stenas)<10 and self.sten:
            if len(self.stenas)==9:
                self.sten = False
            k = random.randrange(1,19)
            m = random.randrange(1,14)
            self.stenas.append(pygame.Rect(k*40,m*40,35,35))

    def udar(self):
        for k in self.stenas[:]:
            if k.colliderect(pygame.Rect(tank1.x1,tank1.y1,40,40)):
                global health1
                global health2
                health1-=1
                self.stenas.remove(k)
                if health1 <= 0:
                    global ok
                    ok = True
                    Tank1win()
                    window.blit(pygame.image.load("C:\\Users\\user\\Desktop\\19BD030608\\img\\gameover1.png"),(260,200)) 
                    pygame.display.flip()
                    time.sleep(4)
                    pygame.key.set_repeat(1,1)
                    pygame.mouse.set_visible(False)
                    health1 = 3
                    health2 = 3
                    game.menu()
                
            elif k.colliderect(pygame.Rect(tank2.x2,tank2.y2,40,40)):
                health2-=1
                self.stenas.remove(k)
                if health2 <= 0:
                    ok = True
                    Tank2win()
                    window.blit(pygame.image.load("C:\\Users\\user\\Desktop\\19BD030608\\img\\gameover1.png"),(260,200)) 
                    pygame.display.flip()
                    time.sleep(4)
                    pygame.key.set_repeat(1,1)
                    pygame.mouse.set_visible(False)
                    health1 = 3
                    health2 = 3
                    game.menu()
                
            elif k.colliderect(pygame.Rect(bullet1.x,bullet1.y,10,10)):
                boom.play()
                bullet1.x = bullet1.y=-100
                self.stenas.remove(k)
                bullet1.strike = False
            elif k.colliderect(pygame.Rect(bullet2.x,bullet2.y,10,10)):
                boom.play()
                bullet2.x=bullet2.y=-100
                self.stenas.remove(k)
                bullet2.strike = False  

    def draw(self,stena):
        for k in self.stenas[:]:
            self.window.blit(stena,(k.x,k.y))

Oboi = STENA(window)
tank1 = Tank1(window)
tank2 = Tank2(window)
bullet1 = Bullet(window)
bullet2 = Bullet(window)
dir_t1 = ""
dir_t2 = ""
bullet1_dir = "UP"
bullet2_dir = "UP"

ok = False

def drawHealth1():
    global health1
    font = pygame.font.SysFont('smaller.fon', 28)
    text = font.render(f'Tank1 health = {health1}', 1, (200, 5, 225))
    window.blit(text, (620, 5))

def drawHealth2():
    global health2
    font = pygame.font.SysFont('smaller.fon', 28)
    text = font.render(f'Tank2 health = {health2}', 1, (100, 0, 225))
    window.blit(text, (30, 5))

def Tank1win():
    font = pygame.font.SysFont('smaller.fon', 48)
    text = font.render(f'Tank2 Win', 1, (200, 220, 180))
    if ok==True:
        window.blit(text, (80, 200))
        
def Tank2win():
    font = pygame.font.SysFont('smaller.fon', 48)
    text = font.render(f'Tank1 Win', 1, (200, 170, 190))
    if ok==True:
        window.blit(text, (600, 200))
        


while done:
    window.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game.menu()
                pygame.key.set_repeat(1,1)
                pygame.mouse.set_visible(False)
            if event.key == pygame.K_RETURN and not(bullet1.strike):
                bullet1.shoot(bullet1_dir,tank1.x1,tank1.y1)
                pos.play()
            if event.key == pygame.K_SPACE and not(bullet2.strike):
                bullet2.shoot(bullet2_dir, tank2.x2, tank2.y2)
                neg.play()
            if event.key == pygame.K_1:
                pygame.mixer.music.pause()
            if event.key == pygame.K_2:
                pygame.mixer.music.set_volume(0.5)
            if event.key == pygame.K_3:
                pygame.mixer.music.unpause()    
            if event.key == pygame.K_UP:
                dir_t1 = "UP"
                if dir_t1 == "UP":
                    bullet1_dir = "UP"
            if event.key == pygame.K_DOWN:
                dir_t1 = "DOWN"
                if dir_t1 == "DOWN":
                    bullet1_dir = "DOWN"
            if event.key == pygame.K_LEFT:
                dir_t1 = "LEFT"
                if dir_t1 == "LEFT":
                    bullet1_dir = "LEFT"
            if event.key == pygame.K_RIGHT:
                dir_t1 = "RIGHT"
                if dir_t1 == "RIGHT":
                    bullet1_dir = "RIGHT"
            if event.key == pygame.K_w:
                dir_t2 = "UP"
                if dir_t2 == "UP":
                    bullet2_dir = "UP"
            if event.key == pygame.K_s:
                dir_t2 = "DOWN"
                if  dir_t2 == "DOWN":
                    bullet2_dir = "DOWN" 
            if event.key == pygame.K_a:
                dir_t2 = "LEFT"
                if dir_t2 == "LEFT":
                    bullet2_dir = "LEFT" 
            if event.key == pygame.K_d:
                dir_t2 = "RIGHT"
                if dir_t2 == "RIGHT":
                    bullet2_dir = "RIGHT" 

    Oboi.plus()

    dist_t1_x = bullet2.x - tank1.x1 
    dist_t1_y = bullet2.y - tank1.y1

    if -8<=dist_t1_x<=32 and -8<=dist_t1_y<=32:
        boom.play()
        tank1.x1+=33
        tank1.y1+=33
        health1-=1
        if health1 <= 0:
            ok = True
            window.blit(pygame.image.load("C:\\Users\\user\\Desktop\\19BD030608\\img\\gameover1.png"),(260,200)) 
            Tank1win()
            time.sleep(4)
            pygame.display.flip()
            pygame.key.set_repeat(1,1)
            pygame.mouse.set_visible(False)
            health1 = 3
            health2 = 3
            game.menu()

    dist_t2_x = bullet1.x - tank2.x2
    dist_t2_y = bullet1.y - tank2.y2
    if -8<=dist_t2_x<=32 and -8<=dist_t2_y<=32:
        boom.play()
        tank2.x2+=33
        tank2.y2+=33
        health2-=1
        if health2 <= 0:
            ok = True
            window.blit(pygame.image.load("C:\\Users\\user\\Desktop\\19BD030608\\img\\gameover1.png"),(260,200)) 
            Tank2win()
            pygame.display.flip()
            time.sleep(4)
            pygame.key.set_repeat(1,1)
            pygame.mouse.set_visible(False)
            health1 = 3
            health2 = 3
            game.menu()

    if done == True:
        tank1.move(dir_t1)
        tank1.range()
        tank1.draw()
        bullet1.move()
        bullet1.draw()
        tank2.move(dir_t2)
        tank2.range()
        tank2.draw()
        bullet2.move()
        bullet2.draw()
        drawHealth1()
        drawHealth2()
        Oboi.udar()
        Oboi.draw(stena)
        pygame.display.update()
        fps.tick(30)
        pygame.display.flip()



'''Multiplayer'''

IP = '34.254.177.17'
PORT = 5672
VIRTUAL_HOST = 'dar-tanks'
USERNAME = 'dar-tanks'
PASSWORD = '5orPLExUYnyVYZg48caMpX'

pygame.init()
screen = pygame.display.set_mode((1050, 600))

class TankRpcClient:
    def __init__(self):
        self.connection  = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=IP,                                               
                port=PORT,
                virtual_host=VIRTUAL_HOST,
                credentials=pika.PlainCredentials(
                    username=USERNAME,
                    password=PASSWORD
                )
            )
        )
        self.channel = self.connection.channel()                    
        queue = self.channel.queue_declare(queue='',exclusive=True,auto_delete=True)  
        self.callback_queue = queue.method.queue 
        self.channel.queue_bind(exchange='X:routing.topic',queue=self.callback_queue)
        self.channel.basic_consume(queue=self.callback_queue,
                                   on_message_callback=self.on_response,
                                   auto_ack=True) 
    
        self.response= None    
        self.corr_id = None
        self.token = None
        self.tank_id = None
        self.room_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)
            print(self.response)

    def call(self, key, message={}):    
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='X:routing.topic',
            routing_key=key,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(message) 
        )
        while self.response is None:
            self.connection.process_data_events()

    def check_server_status(self): 
        self.call('tank.request.healthcheck')
        return self.response['status']== '200' 

    def obtain_token(self, room_id):
        message = {
            'roomId': room_id
        }
        self.call('tank.request.register', message)
        if 'token' in self.response:
            self.token = self.response['token']
            self.tank_id = self.response['tankId']
            self.room_id = self.response['roomId']
            return True
        return False

    def turn_tank(self, token, direction):
        message = {
            'token': token,
            'direction': direction
        }
        self.call('tank.request.turn', message)
    
    def sh_bullet(self, token):  
        message = {  
            'token': token  
        }  
        self.call('tank.request.fire', message)

class TankConsumerClient(Thread):

    def __init__(self, room_id):
        super().__init__()
        self.connection  = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=IP,                                                
                port=PORT,
                virtual_host=VIRTUAL_HOST,
                credentials=pika.PlainCredentials(
                    username=USERNAME,
                    password=PASSWORD
                )
            )
        )
        self.channel = self.connection.channel()                      
        queue = self.channel.queue_declare(queue='',exclusive=True,auto_delete=True)
        event_listener = queue.method.queue
        self.channel.queue_bind(exchange='X:routing.topic',queue=event_listener,routing_key='event.state.'+room_id)
        self.channel.basic_consume(
            queue=event_listener,
            on_message_callback=self.on_response,
            auto_ack=True
        )
        self.response = None

    def on_response(self, ch, method, props, body):
        self.response = json.loads(body)
        #print(self.response)

    def run(self):
        self.channel.start_consuming()

UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'

MOVE_KEYS = {
    pygame.K_w: UP,
    pygame.K_a: LEFT,
    pygame.K_s: DOWN,
    pygame.K_d: RIGHT
}

def draw_tank(x, y, width, height, direction,colour):
    tank_c = (x + int(width / 2), y + int(width / 2))
    pygame.draw.rect(screen, colour,(x, y, width, width), 2)
    pygame.draw.circle(screen, colour, tank_c, int(width / 2))

def mybullet(x, y, width, height, direction, color ): 
    pygame.draw.rect(screen, color, (x, y, width, height))

def game_start():
    loop = True
    font = pygame.font.Font('freesansbold.ttf', 32)
    panelfont = pygame.font.SysFont("Bahnschrift",18)
    welcome = pygame.font.SysFont("Bahnschrift",48)
    aboutgame = pygame.font.SysFont("Ink Free",28)
    gamerule = pygame.font.SysFont("Ink Free",26)
    mainrule = pygame.font.SysFont('Ink Free',22)
    goodluck = pygame.font.SysFont("Ink Free",28)
    while loop:
        screen.fill((0, 0, 0))
        if len(event_client.response["losers"])> 0:
            for a in event_client.response["losers"]:
                if a["tankId"]==client.tank_id:  
                    screen.blit(pygame.image.load("C:\\Users\\user\\Desktop\\19BD030608\\img\\gameover1.png"),(360,200))
                    losing = font.render('--You Lose!!!',True,(255,255,0))
                    screen.blit(losing,(100,252))
                    pygame.display.flip()
                    time.sleep(5)
                    pygame.key.set_repeat(1,1)
                    pygame.mouse.set_visible(False)
                    game.menu() 
                    #loop = False    
        if len(event_client.response["winners"])> 0:
            for a in event_client.response["winners"]:
                if a["tankId"]==client.tank_id:  
                    screen.blit(pygame.image.load("C:\\Users\\user\\Desktop\\19BD030608\\img\\gameover1.png"),(360,200))
                    winning = font.render('--You Win!!!',True,(255,0,250))
                    screen.blit(winning,(100,252))
                    pygame.display.flip()
                    time.sleep(5)
                    pygame.key.set_repeat(1,1)
                    pygame.mouse.set_visible(False)
                    game.menu()
                    #loop = False    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.key.set_repeat(1,1)
                    pygame.mouse.set_visible(False)
                    game.menu()
                    #loop = False
                if event.key in MOVE_KEYS:
                    client.turn_tank(client.token, MOVE_KEYS[event.key])
                if event.key == pygame.K_SPACE: 
                    pos.play()
                    client.sh_bullet(client.token)  
                  

        try:
            remaining_time = event_client.response['remainingTime']
            timet = font.render('Remaining Time: {}'.format(remaining_time), True, (55, 255, 25))
            timetRect = timet.get_rect()
            timetRect.center = (490, 100)
            screen.blit(timet,timetRect)
            welcomes = welcome.render("WELCOME TO MULTIPLAYER MODE", True, (155, 55, 255))
            screen.blit(welcomes,(100,20))
            aboutgames = aboutgame.render('---About Game---',True,(255,255,0))
            screen.blit(aboutgames,(800,452))
            gamerules = gamerule.render('--Game Rule--',True,(0,255,255))
            screen.blit(gamerules,(815,490))
            mainrules = mainrule.render("You need to score maximum point and Win!!!",True,(120,20,120))
            screen.blit(mainrules,(800,520))
            goodlucks = goodluck.render("!!!Good Luck!!!",True,(80,80,80))
            screen.blit(goodlucks,(800,562))
            hits = event_client.response['hits']
            bullets = event_client.response['gameField']['bullets']
            winners = event_client.response['winners']
            tanks = event_client.response['gameField']['tanks']
            tanks = sorted(tanks, key=lambda sc: sc['score'], reverse=True)
            px = 800
            py = 80
            
            for tank in tanks:
                tank_x = tank['x']
                tank_y = tank['y']
                tank_width = tank['width']
                tank_height = tank['height']
                tank_direction = tank['direction']
                tank_health = tank['health']
                tank_score = tank['score']
                if tank['id'] == client.tank_id:
                    paneltext = panelfont.render("id: {}".format(tank['id'])+" score: {}".format(tank['score'])+ " health: {}".format(tank['health']), True, (245, 10, 25))
                    screen.blit(paneltext, (px, 80)) 
                else:
                    py+=20
                    paneltext = panelfont.render("id: {}".format(tank['id'])+" score: {}".format(tank['score'])+ " health: {}".format(tank['health']), True, (255, 255, 255))
                    screen.blit(paneltext, (px, py))
                if tank['id'] == client.tank_id:
                    draw_tank(tank_x, tank_y, tank_width, tank_height, tank_direction,(25,205,255))
                else:
                    draw_tank(tank_x, tank_y, tank_width, tank_height, tank_direction,(1,56,10))
            
            for bullet in bullets: 
                bullet_x = bullet['x'] 
                bullet_y = bullet['y'] 
                bullet_width = bullet['width'] 
                bullet_height = bullet['height'] 
                bullet_direction = bullet['direction'] 
                if bullet['owner'] == client.tank_id: 
                    mybullet(bullet_x, bullet_y, bullet_width, bullet_height, bullet_direction, (133, 25, 100) ) 
                else: 
                    mybullet(bullet_x, bullet_y, bullet_width, bullet_height, bullet_direction, (160, 100, 25) )    
        except Exception as e:
            pass
        pygame.display.flip()
    
    client.connection.close()
    pygame.quit()

if hello == True:
    client = TankRpcClient()
    client.check_server_status()
    client.obtain_token('room-5')
    event_client = TankConsumerClient('room-5')
    event_client.start()
    game_start()

''' AI MODE '''

IP = '34.254.177.17'
PORT = 5672
VIRTUAL_HOST = 'dar-tanks'
USERNAME = 'dar-tanks'
PASSWORD = '5orPLExUYnyVYZg48caMpX'

pygame.init()
screen = pygame.display.set_mode((1050, 600))

class TankRpcClient:
    def __init__(self):
        self.connection  = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=IP,                                               
                port=PORT,
                virtual_host=VIRTUAL_HOST,
                credentials=pika.PlainCredentials(
                    username=USERNAME,
                    password=PASSWORD
                )
            )
        )
        self.channel = self.connection.channel()                    
        queue = self.channel.queue_declare(queue='',exclusive=True,auto_delete=True)  
        self.callback_queue = queue.method.queue 
        self.channel.queue_bind(exchange='X:routing.topic',queue=self.callback_queue)
        self.channel.basic_consume(queue=self.callback_queue,
                                   on_message_callback=self.on_response,
                                   auto_ack=True) 
    
        self.response= None    
        self.corr_id = None
        self.token = None
        self.tank_id = None
        self.room_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)
            print(self.response)

    def call(self, key, message={}):    
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='X:routing.topic',
            routing_key=key,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(message) 
        )
        while self.response is None:
            self.connection.process_data_events()

    def check_server_status(self): 
        self.call('tank.request.healthcheck')
        return self.response['status']== '200' 

    def obtain_token(self, room_id):
        message = {
            'roomId': room_id
        }
        self.call('tank.request.register', message)
        if 'token' in self.response:
            self.token = self.response['token']
            self.tank_id = self.response['tankId']
            self.room_id = self.response['roomId']
            return True
        return False

    def turn_tank(self, token, direction):
        message = {
            'token': token,
            'direction': direction
        }
        self.call('tank.request.turn', message)
    
    def sh_bullet(self, token):  
        message = {  
            'token': token  
        }  
        self.call('tank.request.fire', message)

class TankConsumerClient(Thread):

    def __init__(self, room_id):
        super().__init__()
        self.connection  = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=IP,                                                
                port=PORT,
                virtual_host=VIRTUAL_HOST,
                credentials=pika.PlainCredentials(
                    username=USERNAME,
                    password=PASSWORD
                )
            )
        )
        self.channel = self.connection.channel()                      
        queue = self.channel.queue_declare(queue='',exclusive=True,auto_delete=True)
        event_listener = queue.method.queue
        self.channel.queue_bind(exchange='X:routing.topic',queue=event_listener,routing_key='event.state.'+room_id)
        self.channel.basic_consume(
            queue=event_listener,
            on_message_callback=self.on_response,
            auto_ack=True
        )
        self.response = None

    def on_response(self, ch, method, props, body):
        self.response = json.loads(body)
        #print(self.response)

    def run(self):
        self.channel.start_consuming()

UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'

def draw_tank(x, y, width, height, direction,colour):
    tank_c = (x + int(width / 2), y + int(width / 2))
    pygame.draw.rect(screen, colour,(x, y, width, width), 2)
    pygame.draw.circle(screen, colour, tank_c, int(width / 2))

def mybullet(x, y, width, height, direction, color ): 
    pygame.draw.rect(screen, color, (x, y, width, height))

def game_start():
    loop = True
    font = pygame.font.Font('freesansbold.ttf', 32)
    panelfont = pygame.font.SysFont("Bahnschrift",18)
    welcome = pygame.font.SysFont("Bahnschrift",48)
    aboutgame = pygame.font.SysFont("Ink Free",28)
    gamerule = pygame.font.SysFont("Ink Free",26)
    mainrule = pygame.font.SysFont('Ink Free',22)
    goodluck = pygame.font.SysFont("Ink Free",28)
    while loop:
        screen.fill((0, 0, 0))
        if len(event_client.response["losers"])> 0:
            for a in event_client.response["losers"]:
                if a["tankId"]==client.tank_id:  
                    screen.blit(pygame.image.load("C:\\Users\\user\\Desktop\\19BD030608\\img\\gameover1.png"),(360,200))
                    losing = font.render('--You Lose!!!',True,(255,255,0))
                    screen.blit(losing,(100,252))
                    pygame.display.flip()
                    time.sleep(5)
                    pygame.key.set_repeat(1,1)
                    pygame.mouse.set_visible(False)
                    game.menu() 
                    #loop = False    
        if len(event_client.response["winners"])> 0:
            for a in event_client.response["winners"]:
                if a["tankId"]==client.tank_id:  
                    screen.blit(pygame.image.load("C:\\Users\\user\\Desktop\\19BD030608\\img\\gameover1.png"),(360,200))
                    winning = font.render('--You Win!!!',True,(255,0,250))
                    screen.blit(winning,(100,252))
                    pygame.display.flip()
                    time.sleep(5)
                    pygame.key.set_repeat(1,1)
                    pygame.mouse.set_visible(False)
                    game.menu()
                    #loop = False    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.key.set_repeat(1,1)
                    pygame.mouse.set_visible(False)
                    game.menu()
                    #loop = False
                 
                  
        try:
            remaining_time = event_client.response['remainingTime']
            timet = font.render('Remaining Time: {}'.format(remaining_time), True, (55, 255, 25))
            timetRect = timet.get_rect()
            timetRect.center = (490, 100)
            screen.blit(timet,timetRect)
            welcomes = welcome.render("WELCOME TO AI MODE", True, (155, 55, 255))
            screen.blit(welcomes,(200,20))
            aboutgames = aboutgame.render('---About Game---',True,(255,255,0))
            screen.blit(aboutgames,(800,452))
            gamerules = gamerule.render('--Game Rule--',True,(0,255,255))
            screen.blit(gamerules,(815,490))
            mainrules = mainrule.render("You need to score maximum point and Win!!!",True,(120,20,120))
            screen.blit(mainrules,(800,520))
            goodlucks = goodluck.render("!!!Good Luck!!!",True,(80,80,80))
            screen.blit(goodlucks,(800,562))
            hits = event_client.response['hits']
            bullets = event_client.response['gameField']['bullets']
            winners = event_client.response['winners']
            tanks = event_client.response['gameField']['tanks']
            tanks1 = event_client.response['gameField']['tanks']
            tanks = sorted(tanks, key=lambda sc: sc['score'], reverse=True)
            px = 800
            py = 80
            for tank in tanks:
                tank_x = tank['x']
                tank_y = tank['y']
                tank_width = tank['width']
                tank_height = tank['height']
                tank_direction = tank['direction']
                tank_health = tank['health']
                tank_score = tank['score']
                if tank['id'] == client.tank_id:
                    paneltext = panelfont.render("id: {}".format(tank['id'])+" score: {}".format(tank['score'])+ " health: {}".format(tank['health']), True, (245, 10, 25))
                    screen.blit(paneltext, (px, 80)) 
                else:
                    py+=20
                    paneltext = panelfont.render("id: {}".format(tank['id'])+" score: {}".format(tank['score'])+ " health: {}".format(tank['health']), True, (255, 255, 255))
                    screen.blit(paneltext, (px, py))
                if tank['id'] == client.tank_id:
                    draw_tank(tank_x, tank_y, tank_width, tank_height, tank_direction,(25,205,255))
                else:
                    draw_tank(tank_x, tank_y, tank_width, tank_height, tank_direction,(1,56,10))
            
            for tank in tanks:
                tank_x = tank['x']
                tank_y = tank['y']
                tank_width = tank['width']
                tank_height = tank['height']
                tank_direction = tank['direction']
                tank_health = tank['health']
                tank_score = tank['score']    
                if tank['id'] == client.tank_id:
                    for i in tanks1:
                        protivnik_x = i['x']
                        protivnik_y = i['y']
                        protivnik_direction = i['direction']
                        if i['id'] != client.tank_id:
                            if protivnik_x<tank['x'] and tank['x']-protivnik_x>95: 
                                client.turn_tank(myclient.token, LEFT) 
                            if protivnik_x>tank['x'] and protivnik_x-tank['x']>95:
                                client.turn_tank(client.token,RIGHT)
                            if protivnik_y<tank['y'] and tank['y']-protivnik_y>95: 
                                client.turn_tank(client.token, UP)  
                            if protivnik_y>tank['y'] and protivnik_y-tank['y']>95: 
                                client.turn_tank(client.token, DOWN) 
                            if protivnik_x in range(tank['x']-22,tank['x']+22) and abs(protivnik_y-tank['y'])>66: 
                                if protivnik_y<tank['y']: 
                                    client.turn_tank(client.token, UP)
                                    client.sh_bullet(client.token) 
                                else:
                                    client.turn_tank(client.token,DOWN)
                                    client.sh_bullet(client.token)
                            elif protivnik_y in range(tank['y']-22,tank['y']+22) and abs(protivnik_x-tank['x'])>66:
                                if protivnik_x < tank['x']:
                                    client.turn_tank(client.token, LEFT)
                                    client.sh_bullet(client.token) 
                                else:
                                    client.turn_tank(client.token, RIGHT)
                                    client.sh_bullet(client.token) 
                                
            for bullet in bullets: 
                bullet_x = bullet['x'] 
                bullet_y = bullet['y'] 
                bullet_width = bullet['width'] 
                bullet_height = bullet['height'] 
                bullet_direction = bullet['direction'] 
                if bullet['owner'] == client.tank_id: 
                    mybullet(bullet_x, bullet_y, bullet_width, bullet_height, bullet_direction, (133, 25, 100) ) 
                else: 
                    mybullet(bullet_x, bullet_y, bullet_width, bullet_height, bullet_direction, (160, 100, 25) )    
        except Exception as e:
            pass
        pygame.display.flip()
    
    client.connection.close()
    pygame.quit()

if intl == True:
    client = TankRpcClient()
    client.check_server_status()
    client.obtain_token('room-5')
    event_client = TankConsumerClient('room-5')
    event_client.start()
    game_start()