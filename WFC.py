import pygame
import math
import random
import os

width, height = 600,600
rows,colums = 10,10
screen  = pygame.display.set_mode((width,height))
running = True
ITERATIONS = 10
img_folder = os.path.dirname(__file__ )
img_folder += "/Imgs"

class tile():
    def __init__(self, image):
        
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(img_folder, image)), (height/colums, width/rows))
        self.weight = None
        self.nts = [[] for i in range(8)]

        

NoneTile = tile("Grass.png")
b = tile("Building1.png")
br = tile("Building1roof.png")
g = tile("Grass.png")
c = tile("CloudM.png")
cr = tile("CloudR.png")
cl = tile("CloudL.png")
s = tile("Sky.png")

TILELIST = [b,g,br,c,cr,cl,s]

class grid():
    def __init__(self,rows, colums, DefaultTile = NoneTile, useGroup = True ):
        self.rows = rows
        self.colums = colums
        if useGroup: self.array = [[DefaultTile]* colums for i in range(rows)]
        else: self.array = [[group(TILELIST) for i in range(colums)] for i in range(rows)]
        
    
    def listself(self):
        li = []
        for row in self.array:
            for i in row:
                li.append(i)
        return li
    
    def show(self):
        for row in range(self.rows):
            print([i for i in self.array[row]])

    def blit(self):
        for r, row in enumerate(self.array):
            for place, object in enumerate(row):
                if type(object) != group:
                    screen.blit(object.image, [place*height/self.colums, r*width/self.rows])

class group():
    def __init__(self, objects) -> None:
        self.objects = [i for i in objects]


def inarray(c, r, rows, colums):
    if r < 0 or c < 0: return False
    if r > rows - 1 or c > colums - 1: return False
    return True

def getNieghbors(obj,xx, yy ):
    runs = 0 
    for y in range(3):
        for x in range(3):
            if x - 1!= 0 or y -1 != 0: 
                if inarray(xx + x-1, yy + y-1, initmap.rows, initmap.colums):
                    if initmap.array[yy + y -1][xx + x-1] not in obj.nts[runs]:
                        obj.nts[runs].append(initmap.array[yy + y -1][xx + x-1])
                
                runs+= 1

    
initmap = grid(10, 10)
initmap.array = [[s,s,s,s,s,s,s,s,s,s],
                 [s,s,s,s,s,cl,c,cr,s,s],
                 [cl,c,c,cr,s,s,s,s,s,s],
                 [s,s,br,br,s,br,br,br,br,s],
                 [br,s,b,b,s,b,b,b,b,br],
                 [b,s,b,b,s,b,b,b,b,b],
                 [b,s,b,b,s,b,b,b,b,b],
                 [b,s,b,b,s,b,b,b,b,b],
                 [g,g,g,g,g,g,g,g,g,g],
                 [g,g,g,g,g,g,g,g,g,g],]


for y, row in enumerate(initmap.array):
    for x, i in enumerate(row):
        
        i.weight = initmap.listself().count(i)/(len(initmap.listself()) )
        getNieghbors(i, x, y)

TILEWEIGHTS = [i.weight for i in TILELIST]
print(TILEWEIGHTS)



print("CloudM: ", c)
print("CloudR: " ,cr)
print("cloud left: ", cl)
print("Sky: ", s)
print("building: ", b)
print("grass: ", g)
print("roof: ", br)
print(" ")




def hasNieghbors(obj, xx, yy):
    runs = 0
    for y in range(3):
        for x in range(3):
            if x - 1!= 0 or y -1 != 0: 

                if inarray(xx + x-1, yy + y-1, rows, colums):
                    
                    cobj = map.array[yy + y- 1][xx + x-1]
                    if type(cobj) == group:
                    
                        
                        foundobj = False
                        for objIncobj in cobj.objects:
                            if objIncobj in obj.nts[runs]: foundobj = True             
                        if not foundobj: return False      
                        
                        pass
                    else:
                     
                        if cobj not in obj.nts[runs]:
                            return False
                runs += 1
    return True
                
       
map = grid(rows,colums, group(TILELIST), False)






def checkFinished():
    for row in map.array:
        for i in row: 
            if type(i) == group: return True
    return False



def collapse():

    for iteratation in range(ITERATIONS):

        for y, row in enumerate(map.array):
            if iteratation == 1:
                y = rows - y - 1
            for x, i in enumerate(row):
                if iteratation == 1:
                    x = colums - x -1 
                    i = map.array[y][x]
                '''
                ri = i
                map.array[y][x] = NoneTile
                screen.fill((0,0,0))
                map.blit()
                                    
                pygame.display.flip()
                map.array[y][x] = ri                  
                '''
                if type(i) == group:
                    
                    for object in i.objects:
                        

                        if hasNieghbors(object, x, y ) == False:
                            
                            i.objects.remove(object)
                            
                            if len(i.objects) == 1: 

                                map.array[y][x] = i.objects[0]

    lowestEntropyGroup = None
    for y, row in enumerate(map.array):
        for x, i in enumerate(row):
            if type(i) == group:
                lowestloc = (y,x)
                lowestEntropyGroup = i
                lowest = len(i.objects)
    for y, row in enumerate(map.array):
        for x, i in enumerate(row):
            if type(i) == group:
                if len(i.objects) <= lowest:
                    lowestloc = (y,x)
                    lowestEntropyGroup = i
                    lowest = len(i.objects)
    
    if lowestEntropyGroup == None:
        pass
    else:
        map.array[lowestloc[0]][lowestloc[1]] = random.choices(lowestEntropyGroup.objects, [i.weight for i in lowestEntropyGroup.objects])[0]



# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):

    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


printProgressBar(0, rows*colums, prefix = 'Progress:', suffix = 'Complete', length = 50)
map.array[int(rows/2)][int(colums/2)] = random.choices(map.array[int(rows/2)][int(colums/2)].objects, [i.weight for i in map.array[int(rows/2)][int(colums/2)].objects] )[0]
#collapse()



while checkFinished():
    collapse()      
    finishedtiles = 0
    for row in map.array:
        for i in row: 
            if type(i) != group: finishedtiles += 1
            
    printProgressBar(finishedtiles, rows*colums, prefix = 'Progress:', suffix = 'Complete', length = 50)
    #sys.stdout.write("\033[F") #back to previous line 
    #sys.stdout.write("\033[K") #clear line 
    #print(round((1 - unfinishedtiles/(rows*colums)) * 100, 2), " Percent Completed" )



clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            mx/=width/colums
            mx = math.floor(mx)
            my/=height/rows
            my = math.floor(my)
            print(mx, my)
            if type(map.array[my][mx]) == group:
                print(map.array[my][mx].objects)
            else:
                print(map.array[my][mx])
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                collapse()


        

    screen.fill((0,0,0))
    map.blit()
    clock.tick(10)
    pygame.display.flip()