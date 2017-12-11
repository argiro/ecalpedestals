import sys,getopt
from EcalDetId import EBDetId
from EcalDetId import EEDetId 
from ROOT import *

#def main(argv):
def main():
   inputfile = ''
   outputfile = ''
   etax=-9999
   phiy=-9999
   hash=-9999
   location='EB'
   z=-9999
   run=0
   helpmessage= '- usage: ReadPlots -i <inputfile> -o <outputfile> --r <Run Number> --etax <etha> --phiy <phi> --zeta <zeta> [--hash <hash>] --location <EB/EE>. \n - If location==EB, etax and phiy are expressed in eta, phi coordinates. \n - If location==EE, etax phiy are expressed in x,y coordinates, and z is required. \n - Default location: EB. \n - Instead using etax, etay, you can use hash '

   try:
      opts, args = getopt.getopt(sys.argv[1:],"h:i:o:r:e:p:z:a:l",["help","ifile=","ofile=","run=","etax=","phiy=","zeta=","hash=","location="])
   except getopt.GetoptError:
      print helpmessage
      sys.exit(2)
   for opt, arg in opts:
      if opt in ("-h", "--help"):
         print helpmessage
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      elif opt in ("-r","--run"):
         run=int(arg)
      elif opt in ("-e","--etax"):
          etax = int(arg)
      elif opt in ("-t","--phiy"):
          phiy = int(arg)
      elif opt in ("z","--zeta"):
          z=int(arg)
      elif opt in ("-a","--hash"):
          hash = int(arg)
      elif opt in ("-l","--location"):
          location = arg
    
   if(run==0):
      print "error: missing run number"
      print helpmessage
      sys.exit(2)
        
  
   f = TFile(inputfile)
   
#When z =0 plot EB in eta,phi coordinates, else plot EE in x,y,z coord
   kEBChannels = 61200
 
   idx = 0
   error=0
   if(hash==-9999):
      if location=="EB":
         if(etax==-9999):
            print "error: missing eta"
            print helpmessage
            error=1
         if(phiy==-9999):
            print "error: missing phi"
            print helpmessage
            error=1
            
         if(error==1): sys.exit(2)
         eb = EBDetId()
         eb.fromEtaPhi(etax,phiy)
         idx = eb.hashedIndex()
         
      else:
         if(etax==-9999):
              print "error: missing x"
              error=1
         if(phiy==-9999):
              print "error: missing y"
              error=1
         if(z==-9999):
              print "error: missing z"
              error=1
         if(error==1):
             sys.exit(2)
             print helpmessage
         ee = EEDetId()
         ee.fromXYZ(etax,phiy,z)
         idx = ee.hashedIndex() 
    
   else:
      idx=hash
   
       
   print "hash: ",idx
   MSValue=idx/100
   
   if location=="EB":
       path = "DQMData/Run %d/AlCaReco/Run summary/EcalPedestalsPCL/%s/%d/eb_%d" %(run,location,MSValue,idx)
   elif location=="EE":
       path = "DQMData/Run %d/AlCaReco/Run summary/EcalPedestalsPCL/%s/%d/ee_%d" %(run,location,MSValue,idx)
       
   print "looking for histo: "+path
   canvas = TCanvas('canvas', '', 500, 500)
 
   hist = f.Get(path)
   hist.Draw()
   canvas.Update()
   gApplication.Run()
 #  t1=TFile(outputfile,"RECREATE")
 #  hist.Write();
   
if __name__ == "__main__":
#   main(sys.argv[1:])
  main()
