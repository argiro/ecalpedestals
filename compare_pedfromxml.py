from PedestalsFromXML import readxml
from pedutils import *


if __name__ == "__main__":

    import argparse

    p = argparse.ArgumentParser(description='compare pedestals stored in two TTrees, by averaging over entries')
    
    p.add_argument('file1', help="first xml file")
    p.add_argument('file2', help="second xml file")    
    p.add_argument('-o',  dest='outprefix',   help="output prefix", default = "compare_pedestals_xml")


    args = p.parse_args()
    
    peds1,rms1 = readxml(args.file1) 
    peds2,rms2 = readxml(args.file2)
  


    makeplots(peds1,peds2,rms1,rms2,outprefix=args.outprefix)


 
  


  
# example
#python pedestalsxml2root.py ../ecalpedPCL/476a2a1a515ab12bf10a2064575a005e781327b5.dat ped296115.root
#python compare_pedfromtrees_ave.py ped296173.root laserntuple/ana_ped_stef.root -f2 1 -o test
