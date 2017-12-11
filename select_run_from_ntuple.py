
# Read pedestals fom xml and make a TTree
#
#

def selectRuns(infile,runs):

    from array import array
    from ROOT import TTree,TFile    
    

    nchs = 75848
    ped    = array('f',[0.0]*nchs)
    pedrms = array('f',[0.0]*nchs)

    sfile = TFile(infile)
    stree = sfile.Get('T')

    for r in runs :

        outfile = 'run_'+str(r)+'.root'
    
        tfile = TFile(outfile,'recreate') 
        t = TTree('T','T')
    
        t.Branch('ped',ped,'ped['+str(nchs)+']/F')
        t.Branch('pedrms',pedrms,'pedrms['+str(nchs)+']/F')

        for event in stree:
            ped = stree.ped
            pedrms = stree.pedrms

            if stree.run ==r:
                t.Fill()



        tfile.cd()
        t.Write()                                


if __name__ == "__main__":

    # import argparse

    # p = argparse.ArgumentParser(description='Read pedestals fom xml and make a TTree')
    
    # p.add_argument('infile', help="input xml file")
    # p.add_argument('outfile',help="output root file")

    # args = p.parse_args()
    
    # makeTree(args.infile,args.outfile)

    runs = []
    fname = 'PedHist.root'
    runs = [303790,303794,303795,303817,303818,303819,303824,303825,303832,303838,303885,303948]
    selectRuns(fname,runs)
