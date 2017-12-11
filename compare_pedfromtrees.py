from ROOT import TTree,TH1F,TCanvas,TFile,TH2D,TPaveStats
import ROOT
from EcalDetId import *
from array import array

f1 = TFile('ped.root')
f2 = TFile('laserntuple/ana_ped_stef.root')

t1 = f1.Get('t')
t2 = f2.Get('T')


heb = TH1F('meandiffEB','',100,-5,5)
hee = TH1F('meandiffEE','',100,-5,5)

heb.GetXaxis().SetTitle('ADC')
hee.GetXaxis().SetTitle('ADC')

t1.GetEntry(0)
t2.GetEntry(11)

peds1 = array('f',t1.ped) 
peds2 = array('f',t2.ped)

ebpeds1 = peds1[:61200]
eepeds1 = peds1[61200:]

ebpeds2 = peds2[:61200]
eepeds2 = peds2[61200:]

for idx in range(61200):
     if not channelStatusEB(idx): 
         heb.Fill(ebpeds1[idx] - ebpeds2[idx])

for idx in range(7324*2):
    if not channelStatusEE(idx): 
         hee.Fill(eepeds1[idx] - eepeds2[idx])

    
c = TCanvas()
c.Divide(1,2)
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

c.SaveAs('comp.root')



pmebd  = TH2D("meanebdiff","Pedestal Means Diff",360, 1., 361., 171, -85., 86.)
prebd  = TH2D("rmsebdiff","Pedestal RMS Diff",360, 1., 361., 171, -85., 86.)
pmeepd = TH2D("meaneepdiff","Pedestal Means Diff",100,1,101,100,1,101)
preepd = TH2D("rmseepdiff","Pedestal RMS Diff",100,1,101,100,1,101)
pmeemd = TH2D("meaneemdiff","Pedestal Means Diff",100,1,101,100,1,101)
preemd = TH2D("rmseemdiff","Pedestal RMS Diff",100,1,101,100,1,101)

for idx in range(61200):
    detid = EBDetId()
    detid.fromHashedId(idx)
    diff = ebpeds1[idx] - ebpeds2[idx]
    if channelStatusEB(idx)>0:
        pmebd.Fill(detid.iphi(),detid.ieta(), -9999)
    else:    
        pmebd.Fill(detid.iphi(),detid.ieta(), diff)
    if abs(diff)    > 5 and ebpeds2[idx] > -98:
        print 'ieta', detid.ieta(), 'iphi', detid.iphi(), 'iz', 'ped1',ebpeds1[idx], 'ped2',ebpeds2[idx]

#fill empty bins with low values
for ix in range(101):
    for iy in range(101):
        detid = EEDetId()
        if not detid.validDetId(ix,iy,1):
            pmeepd.Fill(ix,iy, -9999)
        if not detid.validDetId(ix,iy,-1):
            pmeemd.Fill(ix,iy, -9999)
        

for idx in range(7324*2):
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
        print 'ix', detid.ix(), 'iy', detid.iy(), 'iz', detid.zside(), 'ped1',eepeds1[idx], 'ped2',eepeds2[idx]

cc = TCanvas('cc','cc',1200,400)
cc.Divide(3,1)

cc.cd(1)
pmeemd.SetMinimum(-5)
pmeemd.SetMaximum(+5)
pmeemd.SetStats(0)
pmeemd.Draw("colz")
cc.cd(2)
pmebd.SetMinimum(-5)
pmebd.SetMaximum(+5)
pmebd.SetStats(0)
pmebd.Draw("colz")
cc.cd(3)
pmeepd.SetMinimum(-5)
pmeepd.SetMaximum(+5)
pmeepd.SetStats(0)
pmeepd.Draw("colz")

cc.SaveAs("diff2D.root")
