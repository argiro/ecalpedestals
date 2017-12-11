
# Read pedestals fom xml and make a TTree
#
#

def makeTree(infile,outfile):

    from array import array
    from ROOT import TTree,TFile    
    from PedestalsFromXML import readxml

    nchs = 75848
    ped    = array('f',[0.0]*nchs)
    pedrms = array('f',[0.0]*nchs)

  
    tfile = TFile(outfile,'recreate') 
    t = TTree('T','T')
    t.Branch('ped')
    t.Branch('ped',ped,'ped['+str(nchs)+']/F')
    t.Branch('pedrms',pedrms,'pedrms['+str(nchs)+']/F')

    #pedv,rmsv = readxml('../ecalpedPCL/4a7e20d222bf46ec4147f86814e3f3a0b9bdeab7.dat')
    pedv,rmsv = readxml(infile)

    for i in range(len(ped)) : ped[i] = pedv[i] 
    for i in range(len(ped)) : pedrms[i] = rmsv[i] 

    t.Fill()



    tfile.cd()
    t.Write()                                


if __name__ == "__main__":

    import argparse

    p = argparse.ArgumentParser(description='Read pedestals fom xml and make a TTree')
    
    p.add_argument('infile', help="input xml file")
    p.add_argument('outfile',help="output root file")

    args = p.parse_args()
    
    makeTree(args.infile,args.outfile)
