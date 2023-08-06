import numpy as np
import cmath
import math
import matplotlib.pyplot as plt

def getter(l:int,p:int):
  sin,cos,exp=np.sin,np.cos,np.exp
  pi=np.pi
  log=np.log10
  for i in range(0,l):
   # p=1#int(input("Enter number of iterations required to find array factor"))
    thi=np.arange(-pi,pi,pi/10000)
    phi=pi/2;
    af1=np.zeros(20000)
    f=np.array(np.ones(20000))    #([upperlimit-lowerlimit]/period) given for range of thetha values
    af2=[]
    hex=[]
    for x in range(1,p+1):
        for n in range(1,4*(4**(p-1))):
            phin = (n-1)*(phi)
            q=[]
            w=[]
            for i in np.arange(-pi,pi,pi/10000):
                a=exp(complex(0,(2**(x-1))*(2*pi*sin(i)))*(0.7*sin(phin)*sin(phi)))
                q.append(a.real)
            for i in range(len(q)):
                af1[i]=af1[i]+q[i]
        f=f*af1
    af2=(1/(4**x)*f)
    max_value=max(af2)
    af2=abs(af2)
    for i in range(0,len(f)):
       w=20*log(af2[i]/max_value)
       hex.append(w)
    for i in range(0,len(thi)):
        thi[i]=thi[i]*57.3
    plt.plot(thi,hex)
    plt.xlabel("theta")
    plt.ylabel("radiation pattern(dB)")