
from pedutils import *


if __name__ == "__main__":

    import argparse

    p = argparse.ArgumentParser(description='compare pedestals stored in two TTrees, by averaging over entries')
    
    p.add_argument('tree1', help="first root tree")
    p.add_argument('tree2', help="second root tree")
    p.add_argument('-f1', dest='firstentry1', help="first entry in first root tree",type=int,default=0)
    p.add_argument('-l1', dest='lastentry1',  help="last entry in  first  root tree",type=int, default=-1)
    p.add_argument('-f2', dest='firstentry2', help="first entry in 2nd root tree",type=int,default=0)
    p.add_argument('-l3', dest='lastentry2',  help="last entry in  2nd  root tree",type=int, default=-1)
    p.add_argument('-o',  dest='outprefix',   help="output prefix", default = "compare_pedestals")


    args = p.parse_args()
    
    pedslist1,rmslist1 = readtree(args.tree1,args.firstentry1,args.lastentry1) 
    pedslist2,rmslist2 = readtree(args.tree2,args.firstentry2,args.lastentry2)

    peds1,pedsrms1 =  takeaverage(pedslist1,rmslist1)
    peds2,pedsrms2 =  takeaverage(pedslist2,rmslist2)

  


    makeplots(peds1,peds2,pedsrms1,pedsrms2,outprefix=args.outprefix)


 
  


  
# example
#python pedestalsxml2root.py ../ecalpedPCL/476a2a1a515ab12bf10a2064575a005e781327b5.dat ped296115.root
#python compare_pedfromtrees_ave.py ped296173.root laserntuple/ana_ped_stef.root -f2 1 -o test
