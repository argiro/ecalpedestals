import glob
import os,sys
from  multiprocessing import Process
from EcalDetId import EBDetId,EEDetId
from ElectronicsMapping import ElectronicsMapping

from ROOT import TTree,TFile
from array  import array

#dstdir='/cmsecallaser/srv-ecal-laser-13/disk0/ecallaser/dst.merged.matacq1.2.2016'
dstdir='/cmsecallaser/srv-ecal-laser-13/disk0/ecallaser/dst.merged.matacq1.2'


def readpedestals(fed,runmin=273186,runmax=283408):
    """ make a TTree with all channels in the given run range"""
 

    nchs= 1700


    color = 447

    timestamp = array('i',[0]) 
    run     = array('i',[0])
    fedid   = array('i',[0])
    ped     = array('f',[0.0]*nchs)
    pedrms  = array('f',[0.0]*nchs)
    tpped   = array('f',[0.0]*nchs)
    tppedrms= array('f',[0.0]*nchs)
    lped    = array('f',[0.0]*nchs)
    lpedrms = array('f',[0.0]*nchs)
    bfield  = array('f',[0])

    rfile= TFile('pedestals_fed'+str(fed)+'_'+str(runmin)+'_'+str(runmax)+'.root','recreate')
    tree = TTree('peds','pedestals')
    
    tree.Branch('timestamp',timestamp,'timestamp/I')
    tree.Branch('run',run,'run/I')
    tree.Branch('fed',fedid,'fed/I')
    tree.Branch('ped',ped,'ped['+str(nchs)+']/F')
    tree.Branch('pedrms',pedrms,'pedrms['+str(nchs)+']/F')
    tree.Branch('tpped',tpped,'tpped['+str(nchs)+']/F')
    tree.Branch('tppedrms',tppedrms,'tppedrms['+str(nchs)+']/F')
    tree.Branch('lped',lped,'lped['+str(nchs)+']/F')
    tree.Branch('lpedrms',lpedrms,'lpedrms['+str(nchs)+']/F')
    tree.Branch('bfield',bfield,'bfield/F')

    fedid[0] = fed
       
    allfiles = glob.glob(dstdir+'/'+str(fed)+'/'+'*'+str(color)+'*')
    filelist=[]

    em        = ElectronicsMapping()  

    for f in allfiles:
        basename = os.path.basename(f)
        runstr = basename.split('.')[0] 
        runstr= runstr.replace('dst','')
        runno = int(runstr)
        if runno > runmin and runno < runmax:
            filelist.append(f)



    #nfiles = len(filelist)
    #i =0
    for f in filelist:
        #i+=1
        #print 'examine file ', i,'/',nfiles
        curfile = open(f)

        lines = curfile.readlines() 

        header = lines[0]
        run[0]       = int(header.split()[0])
        timestamp[0] = int(header.split()[3])
        bfield[0]    = float(header.split()[10])


        for line in lines[2:]:

            if len(line) <10 : break
            channel   = int(line.split()[1])   
            idx = channel
 
            ped[idx]        = float(line.split()[13])
            pedrms[idx]     = float(line.split()[14]) 
            tpped[idx]      = float(line.split()[15])
            tppedrms[idx]   = float(line.split()[16]) 
            lped[idx]       = float(line.split()[17])
            lpedrms[idx]    = float(line.split()[18])

        tree.Fill()    

    tree.Write()


# main

if __name__ == '__main__':

    _parallelProcessing_ = False
    #runmin=280255
    #runmax=280396
    runmin = 273186
    runmax = 283408

    ecalfeds = range(601,655)


    if _parallelProcessing_: # careful, could overload the laser farm
        jobs = []
        for fed in ecalfeds:
            p = Process(target=readpedestals,args = (fed,runmin,runmax))
            jobs.append(p)
            p.start()
    else:
        for fed in ecalfeds:
            print "Processing pedestals for FED ", fed
            readpedestals(fed,runmin,runmax)

    #readpedestals(650,runmin,runmax)
