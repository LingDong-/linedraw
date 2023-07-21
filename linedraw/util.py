def midpt(*args):
    xs,ys = 0,0
    for p in args:
        xs += p[0]
        ys += p[1]
    return xs/len(args),ys/len(args)

def distsum(*args):
    return sum([ ((args[i][0]-args[i-1][0])**2 + (args[i][1]-args[i-1][1])**2)**0.5 for i in range(1,len(args))])
