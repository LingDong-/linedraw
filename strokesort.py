from random import *
from PIL import Image, ImageDraw, ImageOps
from util import *


def sortlines(lines):
    print("optimizing stroke sequence...")
    clines = lines[:]
    slines = [clines.pop(0)]
    while clines != []:
        x,s,r = None,1000000,False
        for l in clines:
            d = distsum(l[0],slines[-1][-1])
            dr = distsum(l[-1],slines[-1][-1])
            if d < s:
                x,s,r = l[:],d,False
            if dr < s:
                x,s,r = l[:],s,True

        clines.remove(x)
        if r == True:
            x = x[::-1]
        slines.append(x)
    return slines

def visualize(lines):
    import turtle
    wn = turtle.Screen()
    t = turtle.Turtle()
    t.speed(0)
    t.pencolor('red')
    t.pd()
    for i in range(0,len(lines)):
        for p in lines[i]:
            t.goto(p[0]*640/1024-320,-(p[1]*640/1024-320))
            t.pencolor('black')
        t.pencolor('red')
    turtle.mainloop()

if __name__=="__main__":
    import linedraw
    #linedraw.draw_hatch = False
    lines = linedraw.sketch("Lenna")
    #lines = sortlines(lines)
    visualize(lines)