from PIL import Image, ImageDraw, ImageOps, ImageFilter
from random import *
import math

F_Blur = {
    (-2,-2):2,(-1,-2):4,(0,-2):5,(1,-2):4,(2,-2):2,
    (-2,-1):4,(-1,-1):9,(0,-1):12,(1,-1):9,(2,-1):4,
    (-2,0):5,(-1,0):12,(0,0):15,(1,0):12,(2,0):5,
    (-2,1):4,(-1,1):9,(0,1):12,(1,1):9,(2,1):4,
    (-2,2):2,(-1,2):4,(0,2):5,(1,2):4,(2,2):2,
}
F_SobelX = {(-1,-1):1,(0,-1):0,(1,-1):-1,(-1,0):2,(0,0):0,(1,0):-2,(-1,1):1,(0,1):0,(1,1):-1}
F_SobelY = {(-1,-1):1,(0,-1):2,(1,-1):1,(-1,0):0,(0,0):0,(1,0):0,(-1,1):-1,(0,1):-2,(1,1):-1}


def appmask(IM,masks):
    PX = IM.load()
    w,h = IM.size
    NPX = {}
    for x in range(0,w):
        for y in range(0,h):
            a = [0]*len(masks)
            for i in range(len(masks)):
                for p in masks[i].keys():
                    if 0<x+p[0]<w and 0<y+p[1]<h:
                        a[i] += PX[x+p[0],y+p[1]] * masks[i][p]
                if sum(masks[i].values())!=0:
                    a[i] = a[i] / sum(masks[i].values())
            NPX[x,y]=int(sum([v**2 for v in a])**0.5)
    for x in range(0,w):
        for y in range(0,h):
            PX[x,y] = NPX[x,y]

