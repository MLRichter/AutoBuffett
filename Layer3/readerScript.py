__author__ = 'matsrichter'

import benchmark_reader as fxr
#import fxr_dummy as fxr
#import sine_reader #as fxr
import matplotlib.pyplot as mpl

liste = list()
reader = fxr.FX_Reader(6)
dates = list()
while(True):
   #print(reader.readPrice())
    try:
        tmp = reader.readPrice()
        d = tmp[2]
        p = tmp[0]
        liste.append(p)
        dates.append(d)
    except:
        break
date_len = len(dates)
print date_len
size = len(dates)/10
label = list()
for i in range(0,len(dates),size):
    label.append(dates[i])
mpl.xticks(range(0,len(dates),size),label,rotation=45)
mpl.grid(True)
#mpl.ylim((0,1.5))
mpl.xlabel("Zeit")
mpl.ylabel("Preis")
mpl.plot(range(len(dates)),liste)
mpl.show()

    