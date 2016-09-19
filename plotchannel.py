import glob
from array import array
from EcalDetId import EBDetId, EEDetId
import ROOT
from ROOT import TChain, TFile, TCanvas, TGraph, TGraphErrors,TMultiGraph,TPaveLabel


usemergedfile = True

basedir = './new'
rfiles = glob.glob(basedir+'/pedestals_fed???_??????_??????.root')

mergedfile = 'pedestals_273186_279728.root'

if usemergedfile:
    rfile = TFile(mergedfile)
    t= rfile.Get('peds')
 
else :
    t = TChain('peds')
    for f in rfiles: 
        t.Add(f)

def plotchannel(etax, phiy, z=0):
    """When z =0 plot EB in eta,phi coordinates, else plot EE in x,y,z coord"""

    kEBChannels = 61200
    idx =0

    if z==0:

        eb = EBDetId()
        eb.fromEtaPhi(etax,phiy)
        idx = eb.hashedIndex()
    else:
        ee = EEDetId()
        ee.fromXYZ(etax,phiy,z)
        idx = ee.hashedIndex() + kEBChannels
   
    runids = array('f')
    times  = array('f')
    means12  = array('f')
    rmss12   = array('f')

    
    for event in t:
        
        means12.append(t.lped[idx])
        rmss12.append(t.lpedrms[idx])
      
        runids.append(t.run)
        times.append(t.timestamp)
        
    zeroes = array('f',[0.0] *len(runids))

    c=TCanvas()
    m = TMultiGraph()



    g12 = TGraphErrors(len(times),times,means12,zeroes,rmss12)  
    #g6 = TGraphErrors(len(runids),times,means6,zeroes,rmss6)  
    #g1 = TGraphErrors(len(runids),times,means1,zeroes,rmss1)  
    
    g12.SetMarkerStyle(20)
    #g6.SetMarkerStyle(21)
    #g6.SetMarkerColor(ROOT.kRed)
    #g1.SetMarkerStyle(22)
    #g1.SetMarkerColor(ROOT.kGreen)


    m.Add(g12)
    #m.Add(g6)
    #m.Add(g1)
    m.Draw('ap')
    m.GetXaxis().SetTitle('date')
    m.GetXaxis().SetTimeDisplay(1)
    m.GetXaxis().SetTimeFormat("%d.%m")
    m.GetYaxis().SetTitle('ADC')
    m.GetYaxis().SetRangeUser(180,220)
    #m.GetYaxis().SetRangeUser(0,400)

    if z ==0:
        label= 'ieta= '+str(etax)+' iphi= '+str(phiy)
    else :
        label= 'ix= '+str(etax)+' iy= '+str(phiy)+ ' iz='+str(z)

    l=TPaveLabel(0.15,0.92,0.35,0.97,label,'ndc')
    l.SetLineStyle(0)
    l.SetFillColor(0)
    l.SetBorderSize(0)
    l.Draw()

    l1 = TPaveLabel(0.53,0.92,0.60,0.97,'G12','ndc')
    l2 = TPaveLabel(0.60,0.92,0.65,0.97,'G6','ndc')
    l2.SetTextColor(ROOT.kRed)
    l3 = TPaveLabel(0.65,0.92,0.70,0.97,'G1','ndc')
    l3.SetTextColor(ROOT.kGreen)

    for li in l1,l2,l3:
         li.SetLineStyle(0)
         li.SetFillColor(0)
         li.SetBorderSize(0)
         li.Draw()

    #g.Draw('ap')
    #g.SetMarkerStyle(20)
    outfile= 'ch_'+str(etax)+'_'+str( phiy)+'_'+str( z)     
    c.SaveAs(outfile+'.png')   
    c.SaveAs(outfile+'.root')   


plotchannel(-20,20)

#plotchannel(50,50,-1)
