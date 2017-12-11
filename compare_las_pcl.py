
runs = [303790,
        303794,
        303795,
        303817,
        303819,
        303824,
        303825,
        303832,
        303838,
        303885,
        303948]

iov_pcl = ['6d8098b44bdf375091b180759c5b20e978b0b315',
           'dcd14af724acf98f556bfae0f1fc8a72b7ab398f',
           '5e963132b073fc66310efd39ec8bc49f9c771cba',
           '6740edfa3c30afeabfeb81d55e8765f22df6efe2',
           'fad31a46709c8a45a8c623318fd3b692f473b707',
           'f2b752716ecc720b6ce7cd56fe1c26d5b1a91799',
           'c53db9e687575805db4774a37539702e30705f8c',
           '52c71d003c29d1f701750bb7c0225a2c561b7db8',
           '08c0b2627475e9651ebc8041bb61349577de517a',
           '5a29a61474d26703ffe675100c0737ad250af5d4',
           '26c68f5f342acda6b1d324bb8ed2d1f423e00f88']

#my extraction from dst
iov_las = ['laspedestals_303790.root',
           'laspedestals_303794.root',                        
           'laspedestals_303795.root',
           'laspedestals_303817.root',                                       
           'laspedestals_303819.root',
           'laspedestals_303824.root',
           'laspedestals_303825.root',                                       
           'laspedestals_303832.root',
           'laspedestals_303838.root',
           'laspedestals_303885.root',
           'laspedestals_303948.root']

# Jean's extraction plus my division in runs

#iov_las = ['run_303790.root',
#           'run_303794.root',
#           'run_303795.root',
#           'run_303817.root',
#           'run_303819.root',
#           'run_303824.root',
#           'run_303825.root',
#           'run_303832.root',
#           'run_303838.root',
#           'run_303885.root',
#           'run_303948.root',
#    ]




from PedestalsFromXML import readxml
from pedutils import *

    

for run,iovpcl,iovleg in zip(runs,iov_pcl,iov_las):

    print 'Processing files', iovpcl, iovleg
    
    peds1,rms1 = readxml('xml/'+str(iovpcl)+'.xml') 
    pedsl2,rmsl2 = readtree(iovleg)     


    peds2,rms2 =  takeaverage(pedsl2,rmsl2)
    makeplots(peds1,peds2,rms1,rms2,outprefix='run_'+str(run))
