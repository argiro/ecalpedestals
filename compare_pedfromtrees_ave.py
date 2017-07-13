from EcalDetId import *
from array import array


kBarrelSize = 61200
kEndcapSize = 2*7324
 

def readtree(ttreefile, firstentry=0, lastentry =-1):
     """ Read from TTree and return a list of arrays containing peds, rms"""
     from ROOT import TFile, TTree

     f     = TFile(ttreefile)
     ttree = f.Get('T')

     pedslist = []
     rmslist  = []

     last = lastentry
     if lastentry <0: last = ttree.GetEntries()

     for ievent in range(firstentry, last): 

          ttree.GetEntry(ievent)
          pedstmp = array('f',ttree.ped)
          pedslist.append(pedstmp)

          rmstmp = array('f',ttree.pedrms)
          rmslist.append(rmstmp)

          
     return pedslist,rmslist     


def takeaverage(pedslist,rmslist):
     """ average over events in TTree"""
     peds_ave    = array('f',[0.0]*(kBarrelSize+kEndcapSize) )
     pedrms_ave  = array('f',[0.0]*(kBarrelSize+kEndcapSize) )

     nentries    = array('f',[0.0]*(kBarrelSize+kEndcapSize))
     nentriesrms = array('f',[0.0]*(kBarrelSize+kEndcapSize))

     for idx in range(kBarrelSize+kEndcapSize):
          for entry in pedslist:
               if entry[idx]>0:
                    peds_ave[idx] = peds_ave[idx]+ entry[idx]
                    nentries[idx] +=1

     for idx in range(kBarrelSize+kEndcapSize):
          if nentries[idx] >0 :
               peds_ave[idx] = peds_ave[idx]/ nentries[idx]
          else :
               peds_ave[idx] = -99
               
     for idx in range(kBarrelSize+kEndcapSize):
          for entry in rmslist:
               if entry[idx]>0:
                    pedrms_ave[idx] = pedrms_ave[idx]+ entry[idx]
                    nentriesrms[idx] +=1

     for idx in range(kBarrelSize+kEndcapSize):
          if nentriesrms[idx] >0 :
               pedrms_ave[idx] = pedrms_ave[idx]/ nentriesrms[idx]
          else :
               pedrms_ave[idx] = -99
               

     return peds_ave, pedrms_ave          



def makeplots(peds1,peds2,pedsrms1,pedsrms2,outprefix):
     
    from ROOT import TTree,TH1F,TCanvas,TFile,TH2D,TPaveStats 
       
    ebpeds1 = peds1[:kBarrelSize]
    eepeds1 = peds1[kBarrelSize:]

    ebpeds2 = peds2[:kBarrelSize]
    eepeds2 = peds2[kBarrelSize:]
    
    ebpeds1rms = pedsrms1[:kBarrelSize]
    eepeds1rms = pedsrms1[kBarrelSize:]
    
    ebpeds2rms = pedsrms2[:kBarrelSize]
    eepeds2rms = pedsrms2[kBarrelSize:]

    c = TCanvas()
    c.Divide(2,2)
     
    heb = TH1F('meandiffEB','',100,-2.,2.5)
    hee = TH1F('meandiffEE','',100,-2.5,2.5)

    hebr = TH1F('rmsdiffEB','',100,-2.5,2.5)
    heer = TH1F('rmsdiffEE','',100,-2.5,2.5)


    for idx in range(61200):
         if not channelStatusEB(idx): 
              heb.Fill(ebpeds1[idx] - ebpeds2[idx])

    for idx in range(7324*2):
         if not channelStatusEE(idx): 
              hee.Fill(eepeds1[idx] - eepeds2[idx])


    for idx in range(61200):
         if not channelStatusEB(idx): 
              hebr.Fill(ebpeds1rms[idx] - ebpeds2rms[idx])
              
    for idx in range(7324*2):
         if not channelStatusEE(idx): 
              heer.Fill(eepeds1rms[idx] - eepeds2rms[idx])
          

    heb.GetXaxis().SetTitle('ADC')
    hee.GetXaxis().SetTitle('ADC')
    hebr.GetXaxis().SetTitle('ADC')
    heer.GetXaxis().SetTitle('ADC')
 
    c.cd(1)
    heb.Draw()
    c.Draw()
    stateb = heb.FindObject("stats")
    stateb.SetOptStat(111111)
    stateb.SetX1NDC(0.6)
    stateb.SetY1NDC(0.6)
    stateb.SetX2NDC(0.9)
    stateb.SetY2NDC(0.9)
    
    c.cd(2)
    hee.Draw()
    c.Draw()
    statee=hee.FindObject("stats")
    statee.SetOptStat(111111)
    statee.SetX1NDC(0.6)
    statee.SetY1NDC(0.6)
    statee.SetX2NDC(0.9)
    statee.SetY2NDC(0.9)

    c.cd(3)
    hebr.Draw()
    c.Draw()
    hebr.FindObject("stats").SetOptStat(111111)
    hebr.FindObject("stats").SetX1NDC(0.6)
    hebr.FindObject("stats").SetY1NDC(0.6)
    hebr.FindObject("stats").SetX2NDC(0.9)
    hebr.FindObject("stats").SetY2NDC(0.9)
    
    c.cd(4)
    heer.Draw()
    c.Draw()
    heer.FindObject("stats").SetOptStat(111111)
    heer.FindObject("stats").SetX1NDC(0.6)
    heer.FindObject("stats").SetY1NDC(0.6)
    heer.FindObject("stats").SetX2NDC(0.9)
    heer.FindObject("stats").SetY2NDC(0.9)
    

    c.SaveAs(outprefix+'.png')


    pmebd  = TH2D("meanebdiff","Pedestal Means Diff",360, 1., 361., 171, -85., 86.)
    prebd  = TH2D("rmsebdiff","Pedestal RMS Diff",360, 1., 361., 171, -85., 86.)
    pmeepd = TH2D("meaneepdiff","Pedestal Means Diff",100,1,101,100,1,101)
    preepd = TH2D("rmseepdiff","Pedestal RMS Diff",100,1,101,100,1,101)
    pmeemd = TH2D("meaneemdiff","Pedestal Means Diff",100,1,101,100,1,101)
    preemd = TH2D("rmseemdiff","Pedestal RMS Diff",100,1,101,100,1,101)

    for idx in range(kBarrelSize):
         detid = EBDetId()
         detid.fromHashedId(idx)
         diff = ebpeds1[idx] - ebpeds2[idx]
         if channelStatusEB(idx)>0:
              pmebd.Fill(detid.iphi(),detid.ieta(), -9999)
         else:    
              pmebd.Fill(detid.iphi(),detid.ieta(), diff)
         if abs(diff)    > 5 and ebpeds2[idx] > -98:
             print 'Large difference in ieta', detid.ieta(), 'iphi', detid.iphi(), 'iz', 'ped1',ebpeds1[idx], 'ped2',ebpeds2[idx]

     #fill empty bins with low values
    for ix in range(101):
         for iy in range(101):
              detid = EEDetId()
              if not detid.validDetId(ix,iy,1):
                   pmeepd.Fill(ix,iy, -9999)
              if not detid.validDetId(ix,iy,-1):
                   pmeemd.Fill(ix,iy, -9999)


    for idx in range(kEndcapSize):
         detid = EEDetId()
         detid.fromHashedId(idx)
         diff = eepeds1[idx] - eepeds2[idx]
         
         if detid.zside()  >0 : 
              if channelStatusEE(idx)>0:
                   pmeepd.Fill(detid.ix(),detid.iy(), -9999)
              else:
                   pmeepd.Fill(detid.ix(),detid.iy(), diff)
         else :
              if channelStatusEE(idx)>0:
                   pmeemd.Fill(detid.ix(),detid.iy(), -9999)
              else:
                   pmeemd.Fill(detid.ix(),detid.iy(), diff)

         if abs(diff)    > 5 and eepeds2[idx] > -98:
             print 'Large difference in ix', detid.ix(), 'iy', detid.iy(), 'iz', detid.zside(), 'ped1',eepeds1[idx], 'ped2',eepeds2[idx]

    cc = TCanvas('cc','cc',1200,400)
    cc.Divide(3,1)


    hmin = -2.5
    hmax = +2.5

    cc.cd(1)
    pmeemd.SetMinimum(hmin)
    pmeemd.SetMaximum(hmax)
    pmeemd.SetStats(0)
    pmeemd.Draw("colz")
    cc.cd(2)
    pmebd.SetMinimum(hmin)
    pmebd.SetMaximum(hmax)
    pmebd.SetStats(0)
    pmebd.Draw("colz")
    cc.cd(3)
    pmeepd.SetMinimum(hmin)
    pmeepd.SetMaximum(hmax)
    pmeepd.SetStats(0)
    pmeepd.Draw("colz")

    cc.SaveAs(outprefix+'-2D'+'.png')



if __name__ == "__main__":

    import argparse

    p = argparse.ArgumentParser(description='compare pedestals stored in two TTrees, by averaging over entries')
    
    p.add_argument('tree1', help="first root tree")
    p.add_argument('tree2', help="second root tree")
    p.add_argument('-f1', dest='firstentry1', help="first entry in first root tree",type=int,default=0)
    p.add_argument('-l1', dest='lastentry1',  help="last entry in  first  root tree",type=int, default=-1)
    p.add_argument('-f2', dest='firstentry2', help="first entry in 2nd root tree",type=int,default=0)
    p.add_argument('-l3', dest='lastentry2',  help="last entry in  2nd  root tree",type=int, default=-1)
    p.add_argument('-o',  dest='outprefix',   help="output prefix", default = "compare_pedestals.png")


    args = p.parse_args()
    
    pedslist1,rmslist1 = readtree(args.tree1,args.firstentry1,args.lastentry1) 
    pedslist2,rmslist2 = readtree(args.tree2,args.firstentry2,args.lastentry2)

    peds1,pedsrms1 =  takeaverage(pedslist1,rmslist1)
    peds2,pedsrms2 =  takeaverage(pedslist2,rmslist2)

  


    makeplots(peds1,peds2,pedsrms1,pedsrms2,outprefix=args.outprefix)


 
  


  
