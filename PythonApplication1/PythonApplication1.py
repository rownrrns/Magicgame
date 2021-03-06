import cv2
import numpy as np
from time import time
import random
import math
import pygame
from pygame.locals import *;
from math import sin, cos, atan2, sqrt, pi
from xml.dom import minidom
import socket
from threading import Thread
size = 250

WHITE = (255,255,255)
pad_width = 200
pad_height = 200
chr_width = 32
chr_height= 36
direction_change = 72
healer_direction_change = 72
behaviorCount = 0

def clientRecv():
    while True:
        p2_be = mserver.recv(1024)
        p2_be = p2_be.decode('utf-8')
        if p2_be == 'up':
            if healer_direction_change != 0:
                healer_direction_change = 0
            else:
                healer_y_change = -40
                healer_y += healer_y_change
                    
            if healer_motion_change == 32 or healer_motion_change == 64:
                healer_motion_change = 0
            elif motion_change == 0:
                healer_motion_change = 64
        elif p2_be == 'down':
            if healer_direction_change != 72:
                healer_direction_change = 72
            else:
                healer_y_change = 40
                healer_y += healer_y_change
                    
            if healer_motion_change == 32 or healer_motion_change == 64:
                healer_motion_change = 0
            elif motion_change == 0:
                healer_motion_change = 64
        elif p2_be == 'left':
            if healer_direction_change != 108:
                healer_direction_change = 108
            else:
                healer_x_change = -40
                healer_x += healer_x_change
                    
            if healer_motion_change == 32 or healer_motion_change == 64:
                healer_motion_change = 0
            elif motion_change == 0:
                healer_motion_change = 64
        elif p2_be == 'right':
            if healer_direction_change != 36:
                healer_direction_change = 36
            else:
                healer_x_change = 40
                healer_x += healer_x_change
                    
            if healer_motion_change == 32 or healer_motion_change == 64:
                healer_motion_change = 0
            elif motion_change == 0:
                healer_motion_change = 64
        elif p2_be == 'stay':
            healer_x_change = 0
            healer_y_change = 0
            healer_motion_change = 32
        else:
            p2_be = p2_be.split(',')
            if p2_be[3] == 'arrow':
                healer_skill_xyd.append([0,0,0,'arrow',0])
                shoot_skill(healer_x+5,healer_y+8,healer_skill_xyd,2)

            elif p2_be[3] == 'mine':
                healer_skill_xyd.append([0,0,0,'mine',0])
                shoot_skill(healer_x-4,healer_y-2,healer_skill_xyd,2)

            elif p2_be[3] == 'explosion':
                for i in range(8):
                    healer_skill_xyd.append([0,0,0,'explosion',0])
                shoot_skill(healer_x-6,healer_y-7,healer_skill_xyd,2)

            elif p2_be[3] == 'wind':
                healer_skill_xyd.append([0,0,0,'wind',0])
                healer_skill_xyd.append([0,0,0,'wind',0])
                healer_skill_xyd.append([0,0,0,'wind',0])
                shoot_skill(healer_x,healer_y,healer_skill_xyd,2)


    ##mserver.close()

def textObj(text, font):
    textSurface = font.render(text,True,(255,0,0))
    return textSurface,textSurface.get_rect()

def titleTextObj(text, font):
    textSurface = font.render(text,True,(0,0,0))
    return textSurface,textSurface.get_rect()

    

def myHp():
    global mage_health,healer_health,gamepad
    largeText = pygame.font.Font('freesansbold.ttf',15)
    TextSurf,TextRect= textObj("hp: " + str(int(mage_health)),largeText)
    TextRect.center = (30,10)
    gamepad.blit(TextSurf,TextRect)
    pygame.display.update()

def enemyHp():
    global mage_health,healer_health,gamepad
    largeText = pygame.font.Font('freesansbold.ttf',15)
    TextSurf,TextRect= textObj("hp: " + str(int(healer_health)),largeText)
    TextRect.center = (170,10)
    gamepad.blit(TextSurf,TextRect)
    pygame.display.update()

def back(x,y):
    global gamepad, background
    gamepad.blit(background, (x,y))

def mage(x,y,p,q):
    global gamepad, mage_m
    gamepad.blit(mage_m,(x,y), (p,q, 32,36))

def healer(x,y,p,q):
    global gamepad, healer_f
    gamepad.blit(healer_f,(x,y), (p,q,32,36))

def skill(x,y,d, skillname, skilltime):
    global gamepad,skill_arrow, skill_mine, skill_explosion, skill_wind, mage_m, healer_f,skill_mine2
    if skillname == 'arrow':
        skill_direction = pygame.transform.rotate(skill_arrow, 360 - 90*((d/36)-1))
        gamepad.blit(skill_direction, (x,y))
    elif skillname == 'mine':
        gamepad.blit(skill_mine, (x,y))
    elif skillname == 'mine2':
        gamepad.blit(skill_mine2, (x,y))
    elif skillname == 'explosion':
        size = 47
        read_x = 0
        read_y = 16
        if skilltime < 4:
            gamepad.blit(skill_explosion,(x,y), (read_x + 0*size,read_y , size,size))
        elif skilltime < 8:
            gamepad.blit(skill_explosion,(x,y), (read_x + 1*size,read_y , size,size))
        elif skilltime < 12:
            gamepad.blit(skill_explosion,(x,y), (read_x + 2*size,read_y , size,size))
        elif skilltime < 16:
            gamepad.blit(skill_explosion,(x,y), (read_x + 3*size,read_y , size,size))
        elif skilltime < 20:
            gamepad.blit(skill_explosion,(x,y), (read_x + 4*size,read_y , size,size))
        elif skilltime < 26:
            gamepad.blit(skill_explosion,(x,y), (read_x + 0*size,read_y+size , size,size))
        elif skilltime < 32:
            gamepad.blit(skill_explosion,(x,y), (read_x + 1*size,read_y+size , size,size))
        elif skilltime < 38:
            gamepad.blit(skill_explosion,(x,y), (read_x + 2*size,read_y+size , size,size))
        elif skilltime < 44:
            gamepad.blit(skill_explosion,(x,y), (read_x + 3*size,read_y+size , size,size))
        elif skilltime < 50:
            gamepad.blit(skill_explosion,(x,y), (read_x + 4*size,read_y+size , size,size))
    elif skillname == 'wind':
        if skilltime < 20:
            gamepad.blit(skill_wind,(x,y), (0, 0, 32,38))
        elif skilltime < 40:
            gamepad.blit(skill_wind,(x,y), (32, 0, 32,38))
        elif skilltime < 60:
            gamepad.blit(skill_wind,(x,y), (64, 0, 32,38))
        elif skilltime < 80:
            gamepad.blit(skill_wind,(x,y), (96, 0, 32,38))

def draw_skill(x,y,enemy_x,enemy_y,skillxyd):
    global gamepad, mage_m, clock, background
    damage = 0
    if len(skillxyd)!=0:
        for i, bxyd in enumerate(skillxyd):
            if bxyd[3] == 'arrow':
                if bxyd[0] > enemy_x and bxyd[0] < enemy_x + 32 and bxyd[1] > enemy_y and bxyd[1] < enemy_y + 36:
                        damage += 5
                        skillxyd.remove(bxyd)
                elif bxyd[2] == 36:#direction
                    bxyd[0] += 5
                    skillxyd[i][0] = bxyd[0]
                    if bxyd[0] >= 200:
                        skillxyd.remove(bxyd)
                elif bxyd[2] == 108:
                    bxyd[0] -= 5
                    skillxyd[i][0] = bxyd[0]
                    if bxyd[0] <= 0:
                        skillxyd.remove(bxyd)
                elif bxyd[2] == 0:
                    bxyd[1] -= 5
                    skillxyd[i][1] = bxyd[1]
                    if bxyd[1] >= 200:
                        skillxyd.remove(bxyd)
                elif bxyd[2] == 72:
                    bxyd[1] += 5
                    skillxyd[i][1] = bxyd[1]
                    if bxyd[1] <= 0:
                        skillxyd.remove(bxyd)
            elif bxyd[3] == 'mine' or bxyd[3] == 'mine2':
                if bxyd[0]+20 > enemy_x and bxyd[0]+20 < enemy_x + 32 and bxyd[1]+20 > enemy_y and bxyd[1]+20 < enemy_y + 36:
                        damage += 6
                        skillxyd.remove(bxyd)
                if bxyd[4] > 600:
                    skillxyd.remove(bxyd)

            elif bxyd[3] == 'explosion':
                if bxyd[0]+20 > enemy_x and bxyd[0]+20 < enemy_x + 32 and bxyd[1]+20 > enemy_y and bxyd[1]+20 < enemy_y + 36:
                        damage += 0.5
                        #skillxyd.remove(bxyd)
                if bxyd[4] > 50:
                    skillxyd.remove(bxyd)

            elif bxyd[3] == 'wind':
                if bxyd[0]+20 > enemy_x and bxyd[0]+20 < enemy_x + 32 and bxyd[1]+20 > enemy_y and bxyd[1]+20 < enemy_y + 36:
                        damage += 3
                        skillxyd.remove(bxyd)
                elif bxyd[4] > 60:
                    if bxyd[2] == 36:
                        bxyd[0] += 5
                        skillxyd[i][0] = bxyd[0]
                        if bxyd[0] >= 200:
                            skillxyd.remove(bxyd)
                    elif bxyd[2] == 108:
                        bxyd[0] -= 5
                        skillxyd[i][0] = bxyd[0]
                        if bxyd[0] <= 0:
                            skillxyd.remove(bxyd)
                    elif bxyd[2] == 0:
                        bxyd[1] -= 5
                        skillxyd[i][1] = bxyd[1]
                        if bxyd[1] >= 200:
                            skillxyd.remove(bxyd)
                    elif bxyd[2] == 72:
                        bxyd[1] += 5
                        skillxyd[i][1] = bxyd[1]
                        if bxyd[1] <= 0:
                            skillxyd.remove(bxyd)
                if bxyd[4] > 100:
                    skillxyd.remove(bxyd)
        for bx, by, bd, bn, bt in skillxyd:
            skill(bx,by, bd, bn,bt)
    return damage

def shoot_skill(x,y, skillxy, player):
    global direction_change, healer_direction_change

    check = True
    if skillxy[len(skillxy)-1][3] == 'mine' or skillxy[len(skillxy) - 1][3] == 'mine2':
        skillxy[len(skillxy)-1]=[x,y,0, skillxy[len(skillxy)-1][3], 0]
        #mserver.send(str( skillxy[len(skillxy)-1]).encode('utf-8'))
    elif skillxy[len(skillxy)-1][3] == 'explosion':
        count = 0
        for i in range(3):
            for j in range(3):
                if i != 1 or j != 1:
                    count+=1
                    skillxy[len(skillxy)-count]=[x+40*(i-1),y+40*(j-1),0, skillxy[len(skillxy)-1][3], 0]
                    #mserver.send(str( skillxy[len(skillxy)-count]).encode('utf-8'))
    elif skillxy[len(skillxy)-1][3] == 'arrow':
        if(player == 1):
            skillxy[len(skillxy)-1]=[x,y,direction_change, skillxy[len(skillxy)-1][3],0]
            #mserver.send(str( skillxy[len(skillxy)-1]).encode('utf-8'))
        elif player == 2:
            skillxy[len(skillxy)-1]=[x,y,healer_direction_change, skillxy[len(skillxy)-1][3],0]
            #mserver.send(str( skillxy[len(skillxy)-1]).encode('utf-8'))
    elif skillxy[len(skillxy)-1][3] == 'wind':
        if player == 1:
            k =direction_change
        elif player == 2:
            k = healer_direction_change
        if k == 0:
            skillxy[len(skillxy)-1]=[x-40,y-40,k, skillxy[len(skillxy)-1][3],0]
            #mserver.send(str( skillxy[len(skillxy)-1]).encode('utf-8'))
            skillxy[len(skillxy)-2]=[x,y-40,k, skillxy[len(skillxy)-1][3],0]
            #mserver.send(str( skillxy[len(skillxy)-2]).encode('utf-8'))
            skillxy[len(skillxy)-3]=[x+40,y-40,k, skillxy[len(skillxy)-1][3],0]
            #mserver.send(str( skillxy[len(skillxy)-3]).encode('utf-8'))
        elif k == 36:
            skillxy[len(skillxy)-1]=[x+40,y-40,k, skillxy[len(skillxy)-1][3],0]
            #mserver.send(str( skillxy[len(skillxy)-1]).encode('utf-8'))
            skillxy[len(skillxy)-2]=[x+40,y,k, skillxy[len(skillxy)-1][3],0]
            #mserver.send(str( skillxy[len(skillxy)-2]).encode('utf-8'))
            skillxy[len(skillxy)-3]=[x+40,y+40,k, skillxy[len(skillxy)-1][3],0]
            #mserver.send(str( skillxy[len(skillxy)-3]).encode('utf-8'))
        elif k == 72:
            skillxy[len(skillxy)-1]=[x-40,y+40,k, skillxy[len(skillxy)-1][3],0]
            #mserver.send(str( skillxy[len(skillxy)-1]).encode('utf-8'))
            skillxy[len(skillxy)-2]=[x,y+40,k, skillxy[len(skillxy)-1][3],0]
            #mserver.send(str( skillxy[len(skillxy)-2]).encode('utf-8'))
            skillxy[len(skillxy)-3]=[x+40,y+40,k, skillxy[len(skillxy)-1][3],0]
            #mserver.send(str( skillxy[len(skillxy)-3]).encode('utf-8'))
        elif k == 108:
            skillxy[len(skillxy)-1]=[x-40,y-40,k, skillxy[len(skillxy)-1][3],0]
            #mserver.send(str( skillxy[len(skillxy)-1]).encode('utf-8'))
            skillxy[len(skillxy)-2]=[x-40,y,k, skillxy[len(skillxy)-1][3],0]
            #mserver.send(str( skillxy[len(skillxy)-2]).encode('utf-8'))
            skillxy[len(skillxy)-3]=[x-40,y+40,k, skillxy[len(skillxy)-1][3],0]
            #mserver.send(str( skillxy[len(skillxy)-3]).encode('utf-8'))

class Template:
    def __init__(self, name, points):
        self.points = points
        self.name = name

    def prepare(self):
        self.points = resample(self.points, 64)
        self.points = rotate_to_zero(self.points)
        self.points = scale_to_square(self.points,250)
        self.points = translate_to_origin(self.points)

templates = []
#templates.append(Template("triangle", [[137,139],[135,141],[133,144],[132,146],[130,149],[128,151],[126,155],[123,160],[120,166],[116,171],[112,177],[107,183],[102,188],[100,191],[95,195],[90,199],[86,203],[82,206],[80,209],[75,213],[73,213],[70,216],[67,219],[64,221],[61,223],[60,225],[62,226],[65,225],[67,226],[74,226],[77,227],[85,229],[91,230],[99,231],[108,232],[116,233],[125,233],[134,234],[145,233],[153,232],[160,233],[170,234],[177,235],[179,236],[186,237],[193,238],[198,239],[200,237],[202,239],[204,238],[206,234],[205,230],[202,222],[197,216],[192,207],[186,198],[179,189],[174,183],[170,178],[164,171],[161,168],[154,160],[148,155],[143,150],[138,148],[136,148]]))
#templates.append(Template("x", [[87,142],[89,145],[91,148],[93,151],[96,155],[98,157],[100,160],[102,162],[106,167],[108,169],[110,171],[115,177],[119,183],[123,189],[127,193],[129,196],[133,200],[137,206],[140,209],[143,212],[146,215],[151,220],[153,222],[155,223],[157,225],[158,223],[157,218],[155,211],[154,208],[152,200],[150,189],[148,179],[147,170],[147,158],[147,148],[147,141],[147,136],[144,135],[142,137],[140,139],[135,145],[131,152],[124,163],[116,177],[108,191],[100,206],[94,217],[91,222],[89,225],[87,226],[87,224]]));
#templates.append(Template("rectangle", [[78,149],[78,153],[78,157],[78,160],[79,162],[79,164],[79,167],[79,169],[79,173],[79,178],[79,183],[80,189],[80,193],[80,198],[80,202],[81,208],[81,210],[81,216],[82,222],[82,224],[82,227],[83,229],[83,231],[85,230],[88,232],[90,233],[92,232],[94,233],[99,232],[102,233],[106,233],[109,234],[117,235],[123,236],[126,236],[135,237],[142,238],[145,238],[152,238],[154,239],[165,238],[174,237],[179,236],[186,235],[191,235],[195,233],[197,233],[200,233],[201,235],[201,233],[199,231],[198,226],[198,220],[196,207],[195,195],[195,181],[195,173],[195,163],[194,155],[192,145],[192,143],[192,138],[191,135],[191,133],[191,130],[190,128],[188,129],[186,129],[181,132],[173,131],[162,131],[151,132],[149,132],[138,132],[136,132],[122,131],[120,131],[109,130],[107,130],[90,132],[81,133],[76,133]]));
templates.append(Template("circle", [[127,141],[124,140],[120,139],[118,139],[116,139],[111,140],[109,141],[104,144],[100,147],[96,152],[93,157],[90,163],[87,169],[85,175],[83,181],[82,190],[82,195],[83,200],[84,205],[88,213],[91,216],[96,219],[103,222],[108,224],[111,224],[120,224],[133,223],[142,222],[152,218],[160,214],[167,210],[173,204],[178,198],[179,196],[182,188],[182,177],[178,167],[170,150],[163,138],[152,130],[143,129],[140,131],[129,136],[126,139]]));
#templates.append(Template("check", [[91,185],[93,185],[95,185],[97,185],[100,188],[102,189],[104,190],[106,193],[108,195],[110,198],[112,201],[114,204],[115,207],[117,210],[118,212],[120,214],[121,217],[122,219],[123,222],[124,224],[126,226],[127,229],[129,231],[130,233],[129,231],[129,228],[129,226],[129,224],[129,221],[129,218],[129,212],[129,208],[130,198],[132,189],[134,182],[137,173],[143,164],[147,157],[151,151],[155,144],[161,137],[165,131],[171,122],[174,118],[176,114],[177,112],[177,114],[175,116],[173,118]]));
#templates.append(Template("caret", [[79,245],[79,242],[79,239],[80,237],[80,234],[81,232],[82,230],[84,224],[86,220],[86,218],[87,216],[88,213],[90,207],[91,202],[92,200],[93,194],[94,192],[96,189],[97,186],[100,179],[102,173],[105,165],[107,160],[109,158],[112,151],[115,144],[117,139],[119,136],[119,134],[120,132],[121,129],[122,127],[124,125],[126,124],[129,125],[131,127],[132,130],[136,139],[141,154],[145,166],[151,182],[156,193],[157,196],[161,209],[162,211],[167,223],[169,229],[170,231],[173,237],[176,242],[177,244],[179,250],[181,255],[182,257]]));
#templates.append(Template("question", [[104,145],[103,142],[103,140],[103,138],[103,135],[104,133],[105,131],[106,128],[107,125],[108,123],[111,121],[113,118],[115,116],[117,116],[119,116],[121,115],[124,116],[126,115],[128,114],[130,115],[133,116],[135,117],[140,120],[142,121],[144,123],[146,125],[149,127],[150,129],[152,130],[154,132],[156,134],[158,137],[159,139],[160,141],[160,143],[160,146],[160,149],[159,153],[158,155],[157,157],[155,159],[153,161],[151,163],[146,167],[142,170],[138,172],[134,173],[132,175],[127,175],[124,175],[122,176],[120,178],[119,180],[119,183],[119,185],[120,190],[121,194],[122,200],[123,205],[123,211],[124,215],[124,223],[124,225]]));

templates.append(Template("arrow", [[68,222],[70,220],[73,218],[75,217],[77,215],[80,213],[82,212],[84,210],[87,209],[89,208],[92,206],[95,204],[101,201],[106,198],[112,194],[118,191],[124,187],[127,186],[132,183],[138,181],[141,180],[146,178],[154,173],[159,171],[161,170],[166,167],[168,167],[171,166],[174,164],[177,162],[180,160],[182,158],[183,156],[181,154],[178,153],[171,153],[164,153],[160,153],[150,154],[147,155],[141,157],[137,158],[135,158],[137,158],[140,157],[143,156],[151,154],[160,152],[170,149],[179,147],[185,145],[192,144],[196,144],[198,144],[200,144],[201,147],[199,149],[194,157],[191,160],[186,167],[180,176],[177,179],[171,187],[169,189],[165,194],[164,196]]));
templates.append(Template("bracket", [[140,124],[138,123],[135,122],[133,123],[130,123],[128,124],[125,125],[122,124],[120,124],[118,124],[116,125],[113,125],[111,125],[108,124],[106,125],[104,125],[102,124],[100,123],[98,123],[95,124],[93,123],[90,124],[88,124],[85,125],[83,126],[81,127],[81,129],[82,131],[82,134],[83,138],[84,141],[84,144],[85,148],[85,151],[86,156],[86,160],[86,164],[86,168],[87,171],[87,175],[87,179],[87,182],[87,186],[88,188],[88,195],[88,198],[88,201],[88,207],[89,211],[89,213],[89,217],[89,222],[88,225],[88,229],[88,231],[88,233],[88,235],[89,237],[89,240],[89,242],[91,241],[94,241],[96,240],[98,239],[105,240],[109,240],[113,239],[116,240],[121,239],[130,240],[136,237],[139,237],[144,238],[151,237],[157,236],[159,237]]));

templates.append(Template("bracket", [[112,138],[112,136],[115,136],[118,137],[120,136],[123,136],[125,136],[128,136],[131,136],[134,135],[137,135],[140,134],[143,133],[145,132],[147,132],[149,132],[152,132],[153,134],[154,137],[155,141],[156,144],[157,152],[158,161],[160,170],[162,182],[164,192],[166,200],[167,209],[168,214],[168,216],[169,221],[169,223],[169,228],[169,231],[166,233],[164,234],[161,235],[155,236],[147,235],[140,233],[131,233],[124,233],[117,235],[114,238],[112,238]]));

#templates.append(Template("v", [[89,164],[90,162],[92,162],[94,164],[95,166],[96,169],[97,171],[99,175],[101,178],[103,182],[106,189],[108,194],[111,199],[114,204],[117,209],[119,214],[122,218],[124,222],[126,225],[128,228],[130,229],[133,233],[134,236],[136,239],[138,240],[139,242],[140,244],[142,242],[142,240],[142,237],[143,235],[143,233],[145,229],[146,226],[148,217],[149,208],[149,205],[151,196],[151,193],[153,182],[155,172],[157,165],[159,160],[162,155],[164,150],[165,148],[166,146]]));
#templates.append(Template("delete", [[123,129],[123,131],[124,133],[125,136],[127,140],[129,142],[133,148],[137,154],[143,158],[145,161],[148,164],[153,170],[158,176],[160,178],[164,183],[168,188],[171,191],[175,196],[178,200],[180,202],[181,205],[184,208],[186,210],[187,213],[188,215],[186,212],[183,211],[177,208],[169,206],[162,205],[154,207],[145,209],[137,210],[129,214],[122,217],[118,218],[111,221],[109,222],[110,219],[112,217],[118,209],[120,207],[128,196],[135,187],[138,183],[148,167],[157,153],[163,145],[165,142],[172,133],[177,127],[179,127],[180,125]]));
#templates.append(Template("left curly brace", [[150,116],[147,117],[145,116],[142,116],[139,117],[136,117],[133,118],[129,121],[126,122],[123,123],[120,125],[118,127],[115,128],[113,129],[112,131],[113,134],[115,134],[117,135],[120,135],[123,137],[126,138],[129,140],[135,143],[137,144],[139,147],[141,149],[140,152],[139,155],[134,159],[131,161],[124,166],[121,166],[117,166],[114,167],[112,166],[114,164],[116,163],[118,163],[120,162],[122,163],[125,164],[127,165],[129,166],[130,168],[129,171],[127,175],[125,179],[123,184],[121,190],[120,194],[119,199],[120,202],[123,207],[127,211],[133,215],[142,219],[148,220],[151,221]]));
#templates.append(Template("right curly brace", [[117,132],[115,132],[115,129],[117,129],[119,128],[122,127],[125,127],[127,127],[130,127],[133,129],[136,129],[138,130],[140,131],[143,134],[144,136],[145,139],[145,142],[145,145],[145,147],[145,149],[144,152],[142,157],[141,160],[139,163],[137,166],[135,167],[133,169],[131,172],[128,173],[126,176],[125,178],[125,180],[125,182],[126,184],[128,187],[130,187],[132,188],[135,189],[140,189],[145,189],[150,187],[155,186],[157,185],[159,184],[156,185],[154,185],[149,185],[145,187],[141,188],[136,191],[134,191],[131,192],[129,193],[129,195],[129,197],[131,200],[133,202],[136,206],[139,211],[142,215],[145,220],[147,225],[148,231],[147,239],[144,244],[139,248],[134,250],[126,253],[119,253],[115,253]]));
#templates.append(Template("pigtail", [[81,219],[84,218],[86,220],[88,220],[90,220],[92,219],[95,220],[97,219],[99,220],[102,218],[105,217],[107,216],[110,216],[113,214],[116,212],[118,210],[121,208],[124,205],[126,202],[129,199],[132,196],[136,191],[139,187],[142,182],[144,179],[146,174],[148,170],[149,168],[151,162],[152,160],[152,157],[152,155],[152,151],[152,149],[152,146],[149,142],[148,139],[145,137],[141,135],[139,135],[134,136],[130,140],[128,142],[126,145],[122,150],[119,158],[117,163],[115,170],[114,175],[117,184],[120,190],[125,199],[129,203],[133,208],[138,213],[145,215],[155,218],[164,219],[166,219],[177,219],[182,218],[192,216],[196,213],[199,212],[201,211]]));
templates.append(Template("star",
      [
         [75,250],[75,247],[77,244],[78,242],[79,239],[80,237],[82,234],
         [82,232],
         [84,229],
         [85,225],
         [87,222],
         [88,219],
         [89,216],
         [91,212],
         [92,208],
         [94,204],
         [95,201],
         [96,196],
         [97,194],
         [98,191],
         [100,185],
         [102,178],
         [104,173],
         [104,171],
         [105,164],
         [106,158],
         [107,156],
         [107,152],
         [108,145],
         [109,141],
         [110,139],
         [112,133],
         [113,131],
         [116,127],
         [117,125],
         [119,122],
         [121,121],
         [123,120],
         [125,122],
         [125,125],
         [127,130],
         [128,133],
         [131,143],
         [136,153],
         [140,163],
         [144,172],
         [145,175],
         [151,189],
         [156,201],
         [161,213],
         [166,225],
         [169,233],
         [171,236],
         [174,243],
         [177,247],
         [178,249],
         [179,251],
         [180,253],
         [180,255],
         [179,257],
         [177,257],
         [174,255],
         [169,250],
         [164,247],
         [160,245],
         [149,238],
         [138,230],
         [127,221],
         [124,220],
         [112,212],
         [110,210],
         [96,201],
         [84,195],
         [74,190],
         [64,182],
         [55,175],
         [51,172],
         [49,170],
         [51,169],
         [56,169],
         [66,169],
         [78,168],
         [92,166],
         [107,164],
         [123,161],
         [140,162],
         [156,162],
         [171,160],
         [173,160],
         [186,160],
         [195,160],
         [198,161],
         [203,163],
         [208,163],
         [206,164],
         [200,167],
         [187,172],
         [174,179],
         [172,181],
         [153,192],
         [137,201],
         [123,211],
         [112,220],
         [99,229],
         [90,237],
         [80,244],
         [73,250],
         [69,254],
         [69,252]
      ]));
def average(xs): return sum(xs) / len(xs)

def resample(points, n):#{{{
    I = pathlength(points) / float(n-1)
    D = 0
    newPoints = [points[0]]
    i = 1
    while i<len(points):
        p_i = points[i]
        d = distance(points[i-1], p_i)
        if (D + d) >= I:
            qx = points[i-1][0] + ((I-D) / d) * (p_i[0] - points[i-1][0])
            qy = points[i-1][1] + ((I-D) / d) * (p_i[1] - points[i-1][1])
            newPoints.append([qx,qy])
            points.insert(i, [qx,qy])
            D = 0
        else: D = D + d
        i+=1
    return newPoints#}}}

def pathlength(points):#{{{
    d = 0
    for i,p_i in enumerate(points[:len(points)-1]):
        d += distance(p_i, points[i+1])
    return d#}}}

def distance(p1, p2): return float(sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2))

def centroid(points): return float(average([float(i[0]) for i in points])), float(average([float(i[1]) for i in points]))

def rotate_to_zero(points):#{{{
    cx, cy = centroid(points)
    theta = atan2(cy - points[0][1], cx - points[0][0])
    newPoints = rotate_by(points, -theta)
    return newPoints#}}}

def rotate_by(points, theta):#{{{
    cx, cy = centroid(points)
    newpoints = []
    cos_p, sin_p = cos(theta), sin(theta)
    for p in points:
        qx = (p[0] - cx) * cos_p - (p[1] - cy) * sin_p + cx
        qy = (p[0] - cx) * sin_p + (p[1] - cy) * cos_p + cy
        newpoints.append([qx,qy])
    return newpoints#}}}

def bounding_box(points): #{{{
    minx, maxx = min((p[0] for p in points)), max((p[0] for p in points))
    miny, maxy = min((p[1] for p in points)), max((p[1] for p in points))
    return minx, miny, maxx-minx, maxy - miny #}}}

def scale_to_square(points, size):#{{{
    min_x, min_y, w, h = bounding_box(points)
    newPoints = []
    for p in points:
        qx = p[0] * (float(size) / w )
        qy = p[1] * (float(size) / h )
        newPoints.append([qx,qy])
    return newPoints#}}}

def translate_to_origin(points):#{{{
    cx, cy = centroid(points)
    newpoints = []
    for p in points:
        qx, qy = p[0] - cx , p[1] - cy
        newpoints.append([qx,qy])
    return newpoints#}}}

psi = .5 * (-1 + sqrt(5.))
def distance_at_best_angle(points, T, ta, tb, td):#{{{
    x1 = psi * ta + (1-psi)*tb
    f1 = distance_at_angle(points, T, x1)
    x2 = (1-psi)*ta + psi*tb
    f2 = distance_at_angle(points, T, x2)
    while abs(tb - ta) > td:
        if f1 < f2:
            tb,x2,f2 = x2, x1, f1
            x1 = psi*ta + (1-psi)*tb
            f1 = distance_at_angle(points, T, x1)
        else:
            ta,x1,f1 = x1, x2, f2
            x2 = (1 - psi)*ta + psi*tb
            f2 = distance_at_angle(points, T, x2)
    return min(f1, f2)#}}}

def distance_at_angle(points, T, theta):#{{{
    newpoints = rotate_by(points, theta)
    d = pathdistance(newpoints, T)
    return d#}}}

def pathdistance(a,b):#{{{
    d = 0
    for ai, bi in zip(a,b):
        d += distance(ai, bi)
    return d / len(a)#}}}

def recognize(points, templates):#{{{
    b = float("inf")
    #theta = pi / 4 #45 degrees
    theta = 45.
    #t_d = 2 * (pi / 180)
    t_d = 2.
    Tp = None
    num = 0
    for i,T in enumerate(templates):
        Tpoints = T.points
        d = distance_at_best_angle(points, Tpoints, -theta, theta, t_d)
        print ("comparing with: ", T.name, "score: ", d)
        if d < b:
            print(b, d, T.name) 
            b = d
            Tp = T
    return Tp, 1-(b/(0.5 * sqrt(size*size * 2)))
#}}}

def classify(candidate_points,templates, screen, debug=False):#{{{
    np = resample(candidate_points,64)
    np = rotate_to_zero(np)
    if debug: plot(np, (255,0,0), screen)
    np = scale_to_square(np, size)
    if debug: plot(np, (255,0,255), screen)
    np = translate_to_origin(np)
    if debug: plot(np, (0,255,255), screen)
    template, score = recognize(np, templates)
    return template#}}}
    
def plot(points, color, screen, size=1):#{{{
    for p in points:
        pygame.draw.circle(screen,color, p, 1);
        pygame.display.flip()#}}}

def load_template(xmlfile):#{{{   Returns a set of points loaded from xml file
    points = []
    p_xml = minidom.parse(open(xmlfile,'r'))
    for tag in p_xml.getElementsByTagName("Point"):
        points.append([int(tag.attributes['X'].value), int(tag.attributes['X'].value)])
    return points#}}}

#initializing font for puttext

mage_health = 100
healer_health = 100
pygame.init()
gamepad = pygame.display.set_mode((pad_width,pad_height))
pygame.display.set_caption("Magic")
mage_m = pygame.image.load('mage_m.png')
healer_f = pygame.image.load('healer_f.png')
background = pygame.image.load('stage.png')
skill_arrow = pygame.image.load('flame_hrise.png')
skill_arrow = pygame.transform.scale(skill_arrow,(25,20))
skill_mine = pygame.image.load('mine.png')
skill_mine = pygame.transform.scale(skill_mine, (40,40))
skill_mine2 = pygame.image.load('mine2.png')
skill_mine2 = pygame.transform.scale(skill_mine2,(40,40))
skill_explosion = pygame.image.load('explosions.png')
skill_explosion = pygame.transform.scale(skill_explosion, (250,125))
skill_wind = pygame.image.load('whirlwind.png')
skill_wind = pygame.transform.scale(skill_wind, (128, 38))
clock = pygame.time.Clock()

###########game Intro###########
intro = True

while intro:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    gamepad.fill(WHITE)
    startBackGround = pygame.image.load("sky.png")
    gamepad.blit(startBackGround,(0,0))
    largeText = pygame.font.Font('freesansbold.ttf',30)
    TextSurf,TextRect= titleTextObj("Magic Game",largeText)
    TextRect.center = ((pad_width/2),(pad_height)/2 - 50)
    gamepad.blit(TextSurf,TextRect)
    mouse = pygame.mouse.get_pos()
#######start button##############
    pygame.draw.rect(gamepad,(0,0,0),((pad_width/2)-30,(pad_height)/2 ,60,30),3)
    largeText = pygame.font.Font('freesansbold.ttf',15)
    TextSurf,TextRect= titleTextObj("Start",largeText)
    TextRect.center = ((pad_width/2),(pad_height)/2 + 15)
    gamepad.blit(TextSurf,TextRect)
#######exit button###############
    pygame.draw.rect(gamepad,(0,0,0),((pad_width/2)-30,(pad_height)/2 + 40 ,60,30),3)
    largeText = pygame.font.Font('freesansbold.ttf',15)
    TextSurf,TextRect= titleTextObj("Exit",largeText)
    TextRect.center = ((pad_width/2),(pad_height)/2 + 55)
    gamepad.blit(TextSurf,TextRect)
####mouse click event ######
    if event.type == MOUSEBUTTONDOWN:
        #####if click start button###########
        if(mouse[0] > (pad_width/2) - 30 and mouse[0] < (pad_width/2 -30 + 60) and mouse[1] > (pad_height)/2 and mouse[1] < (pad_height)/2 + 30):
            intro = False
        #######if click exit button############
        if(mouse[0] > (pad_width/2) - 30 and mouse[0] < (pad_width/2 -30 + 60) and mouse[1] > (pad_height)/2 + 40 and mouse[1] < (pad_height)/2 + 40 + 30):
            pygame.quit()
            quit()

    pygame.display.update()
    clock.tick(30)


###############tutorial################
tutorial = True

while tutorial:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    gamepad.fill(WHITE)
    startBackGround = pygame.image.load("tutorial.png")
    gamepad.blit(pygame.transform.scale(startBackGround, (pad_width, pad_height)), (0, 0))
    mouse = pygame.mouse.get_pos()

####mouse click event ######
    if event.type == MOUSEBUTTONDOWN:
        #####if click start button###########
        if(mouse[0] >= 0 and mouse[0] <= pad_width and mouse[1] >= 0 and mouse[1] <= (pad_height)):
            tutorial = False

    pygame.display.update()
    clock.tick(10)

tutorial = True
while tutorial:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    gamepad.fill(WHITE)
    startBackGround = pygame.image.load("tutorial2.png")
    gamepad.blit(pygame.transform.scale(startBackGround, (pad_width, pad_height)), (0, 0))
    mouse = pygame.mouse.get_pos()

####mouse click event ######
    if event.type == MOUSEBUTTONDOWN:
        #####if click start button###########
        if(mouse[0] >= 0 and mouse[0] <= pad_width and mouse[1] >= 0 and mouse[1] <= (pad_height)):
            tutorial = False

    pygame.display.update()
    clock.tick(10)

##mserver = socket.socket()
host = '143.248.132.114'
port = 80

##mserver.connect((host, port))

x = (pad_width /10)-16
y = (pad_height* 5/10) - 18
healer_x = (pad_width/10 * 9) -16
healer_y = (pad_height* 5/10) - 18 

x_change = 0
y_change = 0
healer_x_change = 0
healer_y_change = 0

motion_change = 32
direction_change = 72
healer_motion_change = 32
healer_direction_change = 72

skill_xyd = []
healer_skill_xyd = []

background_x = 0

back(background_x,0)
myHp()
enemyHp()
mage(x,y,motion_change,direction_change)
healer(healer_x,healer_y,healer_motion_change,healer_direction_change)
#Thread(target=clientRecv).start()
direction_memory = 0


font = cv2.FONT_HERSHEY_COMPLEX_SMALL
#loading apple image and making its mask to overlay on the video feed
apple = cv2.imread("Apple-Fruit-Download-PNG.png",-1)
apple_mask = apple[:,:,3]
apple_mask_inv = cv2.bitwise_not(apple_mask)
apple = apple[:,:,0:3]
# resizing apple images
apple = cv2.resize(apple,(20,20),interpolation=cv2.INTER_AREA)
apple_mask = cv2.resize(apple_mask,(20,20),interpolation=cv2.INTER_AREA)
apple_mask_inv = cv2.resize(apple_mask_inv,(20,20),interpolation=cv2.INTER_AREA)
#initilizing a black blank image
spell_book = cv2.imread("paper-with-sidebar-runes.png",-1)
book_mask = spell_book[:,:,3]
book_mask_inv = cv2.bitwise_not(book_mask)
spell_book = spell_book[:,:,0:3]
spell_book = cv2.resize(spell_book,(640,480),interpolation=cv2.INTER_AREA)
book_mask = cv2.resize(book_mask,(640,480),interpolation=cv2.INTER_AREA)
book_mask_inv = cv2.resize(book_mask_inv,(640,480),interpolation=cv2.INTER_AREA)
blank_img = np.zeros((480,640,3),np.uint8)
#capturing video from webcam
video = cv2.VideoCapture(0)
#kernels for morphological operations
kernel_erode = np.ones((4,4),np.uint8)
kernel_close = np.ones((15,15),np.uint8)
#for blue [99,115,150] [110,255,255]
#function for detecting red color
def detect_red(hsv):
    #lower bound for red color hue saturation value
    lower = np.array([136, 87, 111])  # 136,87,111
    upper = np.array([179, 255, 255])  # 180,255,255
    mask1 = cv2.inRange(hsv, lower, upper)
    lower = np.array([0, 110, 100])
    upper = np.array([3, 255, 255])
    mask2 = cv2.inRange(hsv, lower, upper)
    maskred = mask1 + mask2
    maskred = cv2.erode(maskred, kernel_erode, iterations=1)
    maskred = cv2.morphologyEx(maskred,cv2.MORPH_CLOSE,kernel_close)
    return maskred


#functions for detecting intersection of line segments.
def orientation(p,q,r):
    val = int(((q[1] - p[1]) * (r[0] - q[0])) - ((q[0] - p[0]) * (r[1] - q[1])))
    if val == 0:
        #linear
        return 0
    elif (val>0):
        #clockwise
        return 1
    else:
        #anti-clockwise
        return 2

def intersect(p,q,r,s):
    o1 = orientation(p, q, r)
    o2 = orientation(p, q, s)
    o3 = orientation(r, s, p)
    o4 = orientation(r, s, q)
    if(o1 != o2 and o3 != o4):
        return True

    return False

#initilizing time (used for increasing the length of snake per second)
start_time = int(time())
# q used for intialization of points
q,snake_len,score,temp=0,200,0,1
# stores the center point of the red blob
point_x,point_y = 0,0
#bluePoint
# stores the points which satisfy the condition, dist stores dist between 2 consecutive pts, length is len of snake
last_point_x,last_point_y,dist,length= 0,0,0,0
# stores all the points of the snake body
points = []
# stores the length between all the points
list_len = []
# generating random number for placement of apple image
#random_x = random.randint(10,550)
#random_y = random.randint(10,400)
#used for checking intersections
a, b, c, d =[],[],[],[]
#main loop
#T = Template("Magic", points)

notEnd = True 
win = False
while notEnd:
    xr, yr, wr, hr = 0, 0, 0, 0
    _,frame = video.read()
    #fliping the frame horizontally.
    frame = cv2.flip(frame,1)
    # initilizing the accepted points so that they are not at the top left corner
    if(q==0 and point_x!=0 and point_y!=0):
        last_point_x = point_x
        last_point_y = point_y
        q=1
   


    #converting to hsv
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    maskred = detect_red(hsv)
    #finding contours
    _, contour_red, _ = cv2.findContours(maskred,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #drawing rectangle around the accepted blob
    try:
        for i in range (0,10):
            xr, yr, wr, hr = cv2.boundingRect(contour_red[i])
            if (wr*hr)>2000:
                break
    except:
        pass
   

    cv2.rectangle(frame, (xr, yr), (xr + wr, yr + hr), (0, 0, 255), 2)
    #making snake body
    point_x = int(xr+(wr/2))
    point_y = int(yr+(hr/2))
    #making blue body
    # finding distance between the last point and the current point
    dist = int(math.sqrt(pow((last_point_x - point_x), 2) + pow((last_point_y - point_y), 2)))
    last_point_x = point_x
    last_point_y = point_y
 
    if (point_x!=0 and point_y!=0 and dist>7):
        #if the point is accepted it is added to points list and its length added to list_len
        list_len.append(dist)
        length += dist
        points.append([point_x, point_y])

        score = 0
        point_x = 0
        point_y = 0
    
    #if length becomes greater then the expected length, removing points from the back to decrease length
    #if (length>=snake_len):
        #for i in range(len(list_len)):
            #length -= list_len[0]
            #list_len.pop(0)
            #points.pop(0)
            #if(length<=snake_len):
                #break
    #initializing blank black image
    #blank_img = cv2.imread("paper-with-sidebar-runes.png",-1)
    blank_img = np.zeros((480, 640, 3), np.uint8)
    frame = cv2.add(frame, blank_img)
    roi = frame[:,:]
    img_bg = cv2.bitwise_and(roi, roi, mask=book_mask_inv)
    img_fg = cv2.bitwise_and(spell_book, spell_book, mask=book_mask)
    dst = cv2.add(img_bg, img_fg)
    frame[:,:] = dst
    #drawing the lines between all the points
    for i,j in enumerate(points):
        if (i==0):
            continue
        cv2.line(blank_img, (points[i-1][0], points[i-1][1]), (j[0], j[1]), (255, 255 , 255), 5)
    cv2.circle(blank_img, (last_point_x, last_point_y), 5 , (10, 200, 150), -1)
    #if snake eats apple increase score and find new position for apple
    if  (last_point_x == point_x  and last_point_y == point_y):
        score +=1
        if score == 10:
            print("Stop event",len(points))
            if len(points) > 10:
                for t in templates: t.prepare()
                template_match = classify(points, templates,video)
                if template_match: 
                    if template_match.name == 'arrow':
                        skill_xyd.append([0,0,0,'arrow',0])
                        shoot_skill(x+5,y+8,skill_xyd,1)
                    elif template_match.name == 'circle':
                        skill_xyd.append([0,0,0,'mine',0])
                        shoot_skill(x-4,y-2,skill_xyd,1)
                    elif template_match.name == 'star':
                        for i in range(8):
                            skill_xyd.append([0,0,0,'explosion',0])
                        shoot_skill(x-6,y-7,skill_xyd,1)
                    elif template_match.name == 'bracket':
                        skill_xyd.append([0,0,0,'wind',0])
                        skill_xyd.append([0,0,0,'wind',0])
                        skill_xyd.append([0,0,0,'wind',0])
                        shoot_skill(x,y,skill_xyd,1)
                    print ("matched: ", template_match.name )
            points = []

    #up,left,right,down
    xy = [[300,10],[25,200],[580,200],[300,420]]
    #adding blank image to captured frame
    frame = cv2.add(frame,blank_img)
    #for i in xy:
     #   frame = cv2.add(frame,blank_img)
     #   #adding apple image to frame
     #   roi = frame[i[1]:i[1]+20, i[0]:i[0]+20]
     #   img_bg = cv2.bitwise_and(roi, roi, mask=apple_mask_inv)
     #   img_fg = cv2.bitwise_and(apple, apple, mask=apple_mask)
     #   dst = cv2.add(img_bg, img_fg)
      #  frame[i[1]:i[1] + 20, i[0]:i[0] + 20] = dst

    if(point_x>0 and point_x<640 and point_y>0 and point_y<60):
        points = []
        cv2.putText(frame, str("Up"), (250, 450), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
        if direction_memory != 'up':
            if direction_change != 0:
                direction_change = 0
            else:
                y_change = -40
                y += y_change

            if motion_change == 32 or motion_change == 64:
                motion_change = 0
            elif motion_change == 0:
                motion_change = 64
            direction_memory = 'up'
    elif(point_x>0 and point_x<60 and point_y>0 and point_y<480):
        points = []
        cv2.putText(frame, str("Left"), (250, 450), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
        if direction_memory != 'left':
            if direction_change != 108:
                direction_change = 108
            else:
                x_change = -40
                x += x_change

            if motion_change == 32 or motion_change == 64:
                motion_change = 0
            elif motion_change == 0:
                motion_change = 64
            direction_memory = 'left'
    elif(point_x>580 and point_x<640 and point_y>0 and point_y<480):
        points = []
        cv2.putText(frame, str("Right"), (250, 450), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

        if direction_memory != 'right':
            if direction_change != 36:
                direction_change = 36
            else:
                x_change = 40
                x += x_change

            if motion_change == 32 or motion_change == 64:
                motion_change = 0
            elif motion_change == 0:
                motion_change = 64
            direction_memory = 'right'
    elif(point_x>0 and point_x<640 and point_y>420 and point_y<480):
        points = []
        cv2.putText(frame, str("Down"), (250, 450), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
        if direction_memory != 'down':
            if direction_change != 72:
                direction_change = 72
            else:
                y_change = 40
                y += y_change

            if motion_change == 32 or motion_change == 64:
                motion_change = 0
            elif motion_change == 0:
                motion_change = 64
            direction_memory = 'down'
    else:
        direction_memory = 0
        x_change = 0
        y_change = 0
        motion_change = 32
    ##################player2 movement#######################
            ##0 -> 이동 , 1-> 공격 ### 공격/ 이동 랜덤으로 정함 
    
    if(behaviorCount == 0):
        behavior = random.randrange(0,2)  
        if(behavior == 0):

            ###player2 left
            if x < healer_x:
                if healer_direction_change != 108:
                    healer_direction_change = 108
                else:
                    healer_x_change = -40
                    healer_x += healer_x_change
                    
                if healer_motion_change == 32 or healer_motion_change == 64:
                    healer_motion_change = 0
                elif motion_change == 0:
                    healer_motion_change = 64

            ####player2 up 
            elif y < healer_y:
                if healer_direction_change != 0:
                    healer_direction_change = 0
                else:
                    healer_y_change = -40
                    healer_y += healer_y_change
                    
                if healer_motion_change == 32 or healer_motion_change == 64:
                    healer_motion_change = 0
                elif motion_change == 0:
                    healer_motion_change = 64

                    
            ###player2 right 
            elif x > healer_x:
                if healer_direction_change != 36:
                    healer_direction_change = 36
                else:
                    healer_x_change = 40
                    healer_x += healer_x_change
                    
                if healer_motion_change == 32 or healer_motion_change == 64:
                    healer_motion_change = 0
                elif motion_change == 0:
                    healer_motion_change = 64

            ###player2 down 
            elif y > healer_y:
                if healer_direction_change != 72:
                    healer_direction_change = 72
                else:
                    healer_y_change = 40
                    healer_y += healer_y_change
                    
                if healer_motion_change == 32 or healer_motion_change == 64:
                    healer_motion_change = 0
                elif motion_change == 0:
                    healer_motion_change = 64

        ###player2 skill
        
        if(behavior == 1):
            if(x == healer_x and y == healer_y):
                healer_skill_xyd.append([0,0,0,'mine2',0])
                shoot_skill(healer_x-4,healer_y-2,healer_skill_xyd,2)
            else:
                skillSelect = random.randint(0,2)
                if (abs(x - healer_x) > (pad_width /5) or abs(healer_y - y) > (pad_height /5)) and skillSelect == 0:
                    healer_skill_xyd.append([0,0,0,'arrow',0])
                    shoot_skill(healer_x+5,healer_y+8,healer_skill_xyd,2)

                elif (abs(x - healer_x) > (pad_width /10)*2 or abs(healer_y - y) > (pad_height /10)*2) and skillSelect == 1:
                    healer_skill_xyd.append([0,0,0,'mine2',0])
                    shoot_skill(healer_x-4,healer_y-2,healer_skill_xyd,2)

                elif abs(x - healer_x) <= (pad_width /10)*2 and abs(healer_y - y) <= (pad_height /10)*2 and skillSelect == 0:
                    for i in range(8):
                        healer_skill_xyd.append([0,0,0,'explosion',0])
                    shoot_skill(healer_x-6,healer_y-7,healer_skill_xyd,2)

                elif abs(x - healer_x) <= (pad_width /10)*2 and abs(healer_y - y) <= (pad_height /10)*2 and skillSelect == 1:
                    healer_skill_xyd.append([0,0,0,'wind',0])
                    healer_skill_xyd.append([0,0,0,'wind',0])
                    healer_skill_xyd.append([0,0,0,'wind',0])
                    shoot_skill(healer_x,healer_y,healer_skill_xyd,2)

        behaviorCount = 30
    else:
        behaviorCount -= 1
    #skill time check
    for i, bxy in enumerate(skill_xyd):
        if bxy[3] == 'mine' or bxy[3] == 'mine2':
            bxy[4] += 1
        elif bxy[3] == 'explosion':
            bxy[4] += 1
        elif bxy[3] == 'wind':
            bxy[4] += 1

    #player2 skill time check
    for i, bxy in enumerate(healer_skill_xyd):
        if bxy[3] == 'mine' or bxy[3] == 'mine2':
            bxy[4] += 1
        elif bxy[3] == 'explosion':
            bxy[4] += 1
        elif bxy[3] == 'wind':
            bxy[4] += 1

    #gamepad.fill(WHITE)
    if y >= 0 and y <= 200 and x >= 0 and x <= 200:
        back(background_x,0)
        myHp()
        enemyHp()
        mage(x,y,motion_change,direction_change)

    elif y < 0:
        y -= y_change
    elif y > 200:
        y -= y_change
    elif x < 0:
        x -= x_change
    elif x > 200:
        x -= x_change
        
    if healer_y >= 0 and healer_y <= 200 and healer_x >= 0 and healer_x <= 200:
        healer(healer_x,healer_y,healer_motion_change,healer_direction_change)

    elif healer_y < 0:
        healer_y -= healer_y_change
    elif healer_y > 200:
        healer_y -= healer_y_change
    elif healer_x < 0:
        healer_x -= healer_x_change
    elif healer_x > 200:
        healer_x -= healer_x_change
        
        
    healer_health -= draw_skill(x,y,healer_x,healer_y,skill_xyd)
    if(healer_health <= 0):
        notEnd = False
        win = True
    mage_health -= draw_skill(healer_x,healer_y,x,y,healer_skill_xyd)
    if(mage_health <= 0):
        notEnd = False
        win = False
    pygame.display.update()
    clock.tick(60)
    
    while notEnd == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gamepad.fill(WHITE)
        startBackGround = pygame.image.load("sky.png")
        gamepad.blit(startBackGround,(0,0))
        largeText = pygame.font.Font('freesansbold.ttf',30)
        TextSurf,TextRect
        if(win == True):
            TextSurf,TextRect= titleTextObj("You Win",largeText)
        else:
            TextSurf,TextRect = titleTextObj("You lose",largeText)
        TextRect.center = ((pad_width/2),(pad_height)/2 - 50)
        gamepad.blit(TextSurf,TextRect)

        pygame.display.update()
        clock.tick(30)
    # checking for snake hitting itself
    #if(len(points)>5):
        # a and b are the head points of snake and c,d are all other points
       # b = points[len(points)-2]
        #a = points[len(points)-1]
        #for i in range(len(points)-3):
         #   c = points[i]
         #  d = points[i+1]
          #  if(intersect(a,b,c,d) and len(c)!=0 and len(d)!=0):
           #     temp = 0
            #    break
        #if temp==0:
         #   break*

    cv2.imshow("frame",frame) 
    # increasing the length of snake 40px per second
    #if((int(time())-start_time)>1):
        #Snake_len += 40
        #start_time = int(time())
    key = cv2.waitKey(1)
    if key == 27:
        break

video.release()
cv2.destroyAllWindows()
#cv2.putText(frame, str("Game Over!"), (100, 230), font, 3, (255, 0, 0), 3, cv2.LINE_AA)
#cv2.putText(frame, str("Press any key to Exit."), (180, 260), font, 1, (255, 200, 0), 2, cv2.LINE_AA)
cv2.imshow("frame",frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

