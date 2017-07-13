import xml.etree.cElementTree as et
from array import array

def readxml(filename):

    tree = et.parse(filename)
    root = tree.getroot()
    
    ped = []
    rms = []
    
    for item in root.iter('item'):
        pedv = float(item.find('mean-x12').text)
        rmsv = float(item.find('rms-x12').text)
        ped.append(pedv)
        rms.append(rmsv)
        

    return array('f',ped),array('f',rms)        


#readxml('../ecalpedPCL/4a7e20d222bf46ec4147f86814e3f3a0b9bdeab7.dat')

