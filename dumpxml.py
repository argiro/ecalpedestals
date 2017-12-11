import subprocess


#dump a bunch of iovs

runs= [303838,303885,303948]


iov_pcl = ['08c0b2627475e9651ebc8041bb61349577de517a',
           '5a29a61474d26703ffe675100c0737ad250af5d4',
           '26c68f5f342acda6b1d324bb8ed2d1f423e00f88']



for iov in iov_pcl:

    with  open('xml/'+iov+'.xml','w') as out:
        subprocess.call(['conddb','dump',iov],stdout=out )

    
