import glob
import os,sys
#from  multiprocessing import Process
from EcalDetId import EBDetId,EEDetId
from ElectronicsMapping import ElectronicsMapping
from array import array
from ROOT import TTree,TFile

def fillpedestals(filename,fed):
    
    
    em = ElectronicsMapping()

    file = open(filename)
    lines = file.readlines()

    for line in lines[2:]:
        if len(line) <10 : break
        channel = int(line.split()[1])   
        rawid   = em.detidFromElecmapping(fed,channel)

        subdetid = (rawid>>25) & 0x7
        
        if subdetid == 1:
            detid = EBDetId(rawid)
        elif subdetid ==2:    
            detid = EEDetId(rawid)
            
        else:
            print 'ERROR: invalid subdet',subdetid
            sys.exit(1)

        idx = detid.hashedIndex()
        if subdetid ==2 : idx+=EBDetId.sizeforDenseIndex()

        ped[idx]        = float(line.split()[17])
        pedrms[idx]     = float(line.split()[18]) 
        

def readheader(filename):
    
     curfile = open(filename)

     header = curfile.readline() 
     
     run[0]       = int(header.split()[0])
     timestamp[0] = int(header.split()[3])
     bfield[0]    = float(header.split()[10])

    


def isSequenceComplete(filename):
    
    feds = range(601,655)
    for fed in feds:
        f = filename.replace(str(feds[0]),str(fed))
        if not os.path.isfile(f) : return False
        
    return True    
        

def processrun(runno):

    dstdir = '/data/argiro/laserdst/dst.merged.matacq1.3.2017/'
    paddedrunno = '{:08d}'.format(runno)
    firstfedfiles = glob.glob(dstdir+'/'+str(feds[0])+'/'+'dst'+paddedrunno+'*'+str(color)+'*')



    rfile= TFile('laspedestals_'+str(runno)+'.root','recreate')
    tree = TTree('T','pedestals')
    
    tree.Branch('timestamp',timestamp,'timestamp/I')
    tree.Branch('run',run,'run/I')
    tree.Branch('ped',ped,'ped['+str(nchs)+']/F')
    tree.Branch('pedrms',pedrms,'pedrms['+str(nchs)+']/F')
    
    tree.Branch('bfield',bfield,'bfield/F')

    for f in firstfedfiles:
        
        if not isSequenceComplete(f): continue

        dirname  = os.path.dirname(f)
        basename = os.path.basename(f)

        runstr = str(runno)
        seqid = basename.split('.')[0]

      


        print "Processing Run ", runno
        readheader(f)

        for fed in feds:

            curfile = dirname.replace(str(feds[0]),str(fed)) +'/'+basename
            print curfile,fed
            fillpedestals(curfile,fed)


        tree.Fill()    
    tree.Write()

#runs = [303838,303885,303948,303832, 303825, 303824, 303819,303818, 303817,303795, 303794, 303793, 303790]
#runs = [303838,303885,303948]

runs = [303838,303885,303948,303832, 303825, 303824, 303819,303818, 303817,303795, 303794, 303793, 303790,303838,303885,303948]

nchs = 75848
color = 447

timestamp = array('i',[0]) 
run     = array('i',[0])
bfield  = array('f',[0])
ped     = array('f',[0.0]*nchs)
pedrms  = array('f',[0.0]*nchs)
        
feds = range(601,655)

for r in runs:
    processrun(r)
#processrun(303832)
