class EndcapRing():

    def __init__(self):
        self.ringmap = {}
        f = open("endcaprings.dat")
        for line in f:
            ix = int(line.split()[0])
            iy = int(line.split()[1])
            ir = int(line.split()[2])
            self.ringmap[(ix,iy)]=ir

    def ring(self,ix,iy):
        return self.ringmap[(ix,iy)]

#test
#er =EndcapRing()
#print er.ring(60,1)
