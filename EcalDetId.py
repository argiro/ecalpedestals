from bisect import bisect_right

channelMap = {}
statusMapEB  = {}        
statusMapEE  = {}        


with open('EE.txt') as f:
    next(f)
    for line in f:
        ix = int(line.split()[4])
        iy = int(line.split()[5])
        iz = int(line.split()[3])
        detid =int(line.split()[0])
        channelMap[(ix,iy,iz)] = detid

with open('BadChannels.txt') as f:    
    for line in f:
        sline = line.split()
        if sline[0] == "EB":
            hashid = int(sline[1])
            statusMapEB[hashid]= int(sline[2])
        if sline[0] == "EE":
            hashid = int(sline[1])
            statusMapEE[hashid]= int(sline[2])

def channelStatusEB(hashid):
    
    result = statusMapEB.get(hashid)
    if result is None:
        return 0
    else : 
        return result

def channelStatusEE(hashid):

    result = statusMapEE.get(hashid)
    if result is None:
        return 0
    else : 
        return result

class EBDetId:

    def __init__(self, id=0):
        self.id = id

    def fromEtaPhi(self,ieta,iphi):
        det =  3
        subdet = 1
        self.id = ((det&0xF)<<28)|((subdet&0x7)<<25)
        self.id |=  ((0x10000|(ieta<<9)) if ieta>0 else  ((-ieta)<<9))  | (iphi&0x1FF)

    def fromHashedId(self, hashedId):
          if hashedId <0 or hashedId > 2*360*85 : 
              raise IndexError('Invalid hash '+ str(hashedId))

          pseudo_eta = int(hashedId/360) - 85
          self.fromEtaPhi(pseudo_eta if pseudo_eta<0 else pseudo_eta+1, hashedId%360+1) 
         

    def zside(self) :
        return 1 if self.id&0x10000 else -1 

    def ietaAbs(self) :
        return (self.id>>9)&0x7F
    def ieta(self):
        return self.ietaAbs() * self.zside()

    def iphi(self):
        return self.id&0x1FF

    def hashedIndex(self):
        return (85 + (self.ieta()-1 if self.ieta()>0 else  -1*self.ietaAbs()) )*360 + self.iphi()-1

    def rawId(self):
        return self.id

    @staticmethod
    def sizeforDenseIndex():
        return 61200

class EEDetId:


    def __init__( self, id=0):
        self.id = id
        self.kxf = [41,  51,  41,  51,  41,  51,  36,  51,  36,  51,
                    26,  51,  26,  51,  26,  51,  21,  51,  21,  51,
                    21,  51,  21,  51,  21,  51,  16,  51,  16,  51,
                    14,  51,  14,  51,  14,  51,  14,  51,  14,  51,
                    9,  51,   9,  51,   9,  51,   9,  51,   9,  51,
                    6,  51,   6,  51,   6,  51,   6,  51,   6,  51,
                    6,  51,   6,  51,   6,  51,   6,  51,   6,  51,
                    4,  51,   4,  51,   4,  51,   4,  51,   4,  56,
                    1,  58,   1,  59,   1,  60,   1,  61,   1,  61,
                    1,  62,   1,  62,   1,  62,   1,  62,   1,  62,
                    1,  62,   1,  62,   1,  62,   1,  62,   1,  62,
                    1,  61,   1,  61,   1,  60,   1,  59,   1,  58,
                    4,  56,   4,  51,   4,  51,   4,  51,   4,  51,
                    6,  51,   6,  51,   6,  51,   6,  51,   6,  51,
                    6,  51,   6,  51,   6,  51,   6,  51,   6,  51,
                    9,  51,   9,  51,   9,  51,   9,  51,   9,  51,
                    14,  51,  14,  51,  14,  51,  14,  51,  14,  51,
                    16,  51,  16,  51,  21,  51,  21,  51,  21,  51,
                    21,  51,  21,  51,  26,  51,  26,  51,  26,  51,
                    36,  51,  36,  51,  41,  51,  41,  51,  41,  51
                    ]
 
        self.kdi =[     0,   10,   20,   30,   40,   50,   60,   75,   90,  105,
                        120,  145,  170,  195,  220,  245,  270,  300,  330,  360,
                        390,  420,  450,  480,  510,  540,  570,  605,  640,  675,
                        710,  747,  784,  821,  858,  895,  932,  969, 1006, 1043,
                        1080, 1122, 1164, 1206, 1248, 1290, 1332, 1374, 1416, 1458,
                        1500, 1545, 1590, 1635, 1680, 1725, 1770, 1815, 1860, 1905,
                        1950, 1995, 2040, 2085, 2130, 2175, 2220, 2265, 2310, 2355,
                        2400, 2447, 2494, 2541, 2588, 2635, 2682, 2729, 2776, 2818,
                        2860, 2903, 2946, 2988, 3030, 3071, 3112, 3152, 3192, 3232,
                        3272, 3311, 3350, 3389, 3428, 3467, 3506, 3545, 3584, 3623,
                        3662, 3701, 3740, 3779, 3818, 3857, 3896, 3935, 3974, 4013,
                        4052, 4092, 4132, 4172, 4212, 4253, 4294, 4336, 4378, 4421,
                        4464, 4506, 4548, 4595, 4642, 4689, 4736, 4783, 4830, 4877,
                        4924, 4969, 5014, 5059, 5104, 5149, 5194, 5239, 5284, 5329,
                        5374, 5419, 5464, 5509, 5554, 5599, 5644, 5689, 5734, 5779,
                        5824, 5866, 5908, 5950, 5992, 6034, 6076, 6118, 6160, 6202,
                        6244, 6281, 6318, 6355, 6392, 6429, 6466, 6503, 6540, 6577,
                        6614, 6649, 6684, 6719, 6754, 6784, 6814, 6844, 6874, 6904,
                        6934, 6964, 6994, 7024, 7054, 7079, 7104, 7129, 7154, 7179,
                        7204, 7219, 7234, 7249, 7264, 7274, 7284, 7294, 7304, 7314
                        ]


        
    def validDetId(self,ix,iy,iz):
        if channelMap.get((ix,iy,iz)) is None:
            return False
        return True

    def fromXYZ(self,ix,iy,iz):
        det =  3
        subdet = 2
        self.id = ((det&0xF)<<28)|((subdet&0x7)<<25)
        self.id |=  (iy&0x7f)|((ix&0x7f)<<7)| ( 0x4000 if iz >0 else 0)    

    def fromHashedId(self, hashedId):

          kEEhalf = 7324
          if hashedId > kEEhalf*2 or hashedId <0 :
              raise IndexError('Invalid hashed index '+ str(hashedId))

          hi = hashedId
          iz = -1 if hi < kEEhalf else  1  
          di =  hi% kEEhalf
          ii = bisect_right( self.kdi, di )  -1
          iy = int(1 + ii/2)  
          ix = self.kxf[ii] + di - self.kdi[ii]  
          self.fromXYZ( ix, iy, iz ) 


        


    def zside(self):
        return 1  if self.id&0x4000 else -1

    def ix(self):
        return (self.id>>7)&0x7F
    
    def iy(self):   
        return (self.id&0x7F)

    def hashedIndex(self):
        jd = int ( 2*( self.iy() - 1 ) + ( self.ix() - 1 )/50 ) ;
        return (  ( 7324 if self.zside() >0 else  0) + self.kdi[jd] + self.ix() - self.kxf[jd] ) ;

    def rawId(self):
        return self.id

    
#eb = EBDetId()
#eb.fromEtaPhi(24,83)
# hid=eb.hashedIndex()
# print 24,83,hid
# eb2 = EBDetId()
# eb2.fromHashedId(hid)
# print eb2.ieta(), eb2.iphi()


# ee = EEDetId()
# ee.fromXYZ(20,65,1)
# hid=ee.hashedIndex()
# print 20,65, hid
# ee2 = EEDetId()
# ee2.fromHashedId(hid)
# print ee2.ix(), ee2.iy()

