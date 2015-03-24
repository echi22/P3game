'''
Created on 05/03/2012

@author: facundoq
'''
from numpy import *
import pygame, random
from pygame import Color
import copy
from mimetypes import init
from copy_reg import constructor
import time


class Element():
    
    def __init__(self, value, calculated_value):
      self.value = value
      self.calculated_value = calculated_value
    def distance(self,e):
        return abs(self.value-e.value)
    def go_left(self, min):
        #return Element(self.value, max(min, self.calculated_value - self.delta()))
        self.calculated_value=max(min, self.calculated_value - self.delta())
    def go_right(self, max):
        #return Element(self.value, min(max, self.calculated_value + self.delta()))
        self.calculated_value=min(max, self.calculated_value + self.delta())   
    def delta(self):
        return 1
    
def update_elements(sd,updates):
    elements=sd.elements
    result = copy.deepcopy(sd.elements)
    for i in range(updates):
        x, y, z = random.randint(0,len(elements)-1), random.randint(0,len(elements)-1), random.randint(0,len(elements)-1)
        trio = [elements[x], elements[y], elements[z]]
        a,b=trio[1],trio[2]
        if (a.distance(b)<20):
            if a.value<b.value:
                b.go_left(sd.min)
                a.go_right(sd.max)
            if a.value>=b.value:
                a.go_left(sd.min)
                b.go_right(sd.max)
        elif (a.distance(b)<50):
            if a.value<b.value:
                a.go_left(sd.min)
                b.go_right(sd.max)
            if a.value>=b.value:
                b.go_left(sd.min)
                a.go_right(sd.max)
        
        #trio.sort(cmp=\lambda e:x)
#        dxy = abs(ex.value - ey.value)
#        dyz = abs(ey.value - ez.value)
#        dxz = abs(ex.value - ez.value)
#        
#        if(dxy < dyz and dxy < dxz):
#            ex.go_left(min)
            
    return elements
        

def draw_elements(sd,dc,screen,line_y):
    color = (0, 0, 0)
    pygame.draw.line(screen, color, (dc.horizontal_margin, line_y), (dc.width - dc.horizontal_margin, line_y), 4)
    for e in sd.elements:
        position = (e.calculated_value + (dc.width / 2), line_y)
        y = line_y - (30 + ((e.value - sd.min) * 100 / 1000))
        text_position = (e.calculated_value + (dc.width / 2), y)
        screen.blit(myFont.render(str(e.value), 0, (color)), text_position)
        colors = (e.value - sd.min) * 245 / (sd.max - sd.min)
        if (e.value > 0):
            color = (10 + colors, 10, 10)
        else:
            color = (10, 255 - colors, 10)    
        pygame.draw.circle(screen, color, position, 5, 3)

class SimulationData():
    def __init__(self,min,max):
        self.max=max
        self.min=min
        self.elements = [ Element(random.randint(min, max), random.randint(min, max)) for i in range(20) ]
        
class DisplayConfig():
    def __init__(self,width,height,horizontal_margin):
        self.width = width
        self.height=height
        self.horizontal_margin = horizontal_margin

if __name__ == '__main__':

    line_y = 250
    pygame.init()
    sd = SimulationData(-500,500)
    dc = DisplayConfig(1200,500,100);
    
    screen = pygame.display.set_mode([dc.width, dc.height])
    screen.fill([255, 255, 255])
    mainloop, x, y, color, fontsize, delta, fps = True, 25 , 0, (32, 32, 32), 35, 1, 30
    clock = pygame.time.Clock() # create clock object
    fontsize = 20
    myFont = pygame.font.SysFont("None", fontsize)
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    iterations=0
    start = time.time()


    while mainloop:
        iterations+=1
        tick_time = clock.tick(fps) # milliseconds since last frame
        elapsed = (time.time() - start)
        pygame.display.set_caption("press Esc to quit. Elapsed: %d s Iterations: %d. FPS: %.2f" % (elapsed,iterations,clock.get_fps()))
        
        screen.fill((255, 255, 255))
        draw_elements(sd,dc,screen,line_y)
        sd.elements = update_elements(sd,500)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False
        pygame.display.update()
