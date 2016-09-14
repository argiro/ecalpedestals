class ElectronicsMapping:

    def __init__(self):
        
        self.detidIndexedMap = {}
        self.FedChIndexedMap = {}
        mapfile = open('map_elecId_detId.dat')

        for line in mapfile:
            fed  = int(line.split()[0])
            ch   = int(line.split()[1])
            detid= int(line.split()[2])
  
            self.detidIndexedMap[detid] = (fed,ch)
            self.FedChIndexedMap[(fed,ch)] = detid

    def detidFromElecmapping(self,fed,ch):
        return self.FedChIndexedMap[(fed,ch)]

    def FedChFromDetId(self,detid):
        return self.detidIndexedMap[detid]
