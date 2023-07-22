#Perlin Noise
#Based on Javascript from p5.js (https://github.com/processing/p5.js/blob/master/src/math/noise.js)

import math
import random

PERLIN_YWRAPB = 4
PERLIN_YWRAP = 1<<PERLIN_YWRAPB
PERLIN_ZWRAPB = 8
PERLIN_ZWRAP = 1<<PERLIN_ZWRAPB
PERLIN_SIZE = 4095

perlin_octaves = 4
perlin_amp_falloff = 0.5

def scaled_cosine(i):
    return 0.5*(1.0-math.cos(i*math.pi))

perlin = None

def noise(x,y=0,z=0):
    global perlin
    if perlin == None:
        perlin = []
        for i in range(0,PERLIN_SIZE+1):
            perlin.append(random.random())
    if x<0:x=-x
    if y<0:y=-y
    if z<0:z=-z
    
    xi,yi,zi = int(x),int(y),int(z)
    xf = x-xi
    yf = y-yi
    zf = z-zi
    rxf = ryf = None
    
    r = 0
    ampl = 0.5
    
    n1 = n2 = n3 = None
    for o in range(0,perlin_octaves):
        of=xi+(yi<<PERLIN_YWRAPB)+(zi<<PERLIN_ZWRAPB)

        rxf = scaled_cosine(xf)
        ryf = scaled_cosine(yf)

        n1  = perlin[of&PERLIN_SIZE]
        n1 += rxf*(perlin[(of+1)&PERLIN_SIZE]-n1)
        n2  = perlin[(of+PERLIN_YWRAP)&PERLIN_SIZE]
        n2 += rxf*(perlin[(of+PERLIN_YWRAP+1)&PERLIN_SIZE]-n2)
        n1 += ryf*(n2-n1)

        of += PERLIN_ZWRAP
        n2  = perlin[of&PERLIN_SIZE]
        n2 += rxf*(perlin[(of+1)&PERLIN_SIZE]-n2)
        n3  = perlin[(of+PERLIN_YWRAP)&PERLIN_SIZE]
        n3 += rxf*(perlin[(of+PERLIN_YWRAP+1)&PERLIN_SIZE]-n3)
        n2 += ryf*(n3-n2)

        n1 += scaled_cosine(zf)*(n2-n1)

        r += n1*ampl
        ampl *= perlin_amp_falloff
        xi<<=1
        xf*=2
        yi<<=1
        yf*=2
        zi<<=1
        zf*=2
        
        if (xf>=1.0): xi+=1; xf-=1
        if (yf>=1.0): yi+=1; yf-=1
        if (zf>=1.0): zi+=1; zf-=1      
    return r
        
def noiseDetail(lod, falloff):
    if lod>0:perlin_octaves=lod
    if falloff>0:perlin_amp_falloff=falloff 
    
    
class LCG():
    def __init__(self):
        self.m = 4294967296.0
        self.a = 1664525.0
        self.c = 1013904223.0   
        self.seed = self.z = None
    def setSeed(self,val=None):
        self.z = self.seed = (math.random()*self.m if val == None else val) >> 0
    def getSeed(self):
        return self.seed
    def rand(self):
        self.z = (self.a * self.z + self.c) % self.m
        return self.z/self.m        
        
    
def noiseSeed(seed):
    lcg = LCG()
    lcg.setSeed(seed)
    perlin = []
    for i in range(0,PERLIN_SIZE+1):
        perlin.append(lcg.rand())
        
        