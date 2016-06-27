__author__ = 'matsrichter'
import numpy as np
import csv

#DUMMY READER FOR FOREX INDICES

class FX_Reader:
    #@input timested  time between ticks in seconds
    def __init__(self, time_step = 1):
        self.q = self.iterate()
        self.time_step = time_step
        self.tstep = 0

    def readPrice(self):
        if(self.time_step == 1):
            return self.q.next()
        else:
            for i in range(self.time_step-1):
                self.q.next()
            return self.q.next()

    def iterate(self):
            with open('Historical2001.csv','rb') as f:
                reader = csv.reader(f)
                tstep = 0
                try:
                    for row in reader:
                        #print(row)
                        tstep += 1
                        #if(tstep%2 == 0):
                            #continue
                        date = str(row[0])
                        date = date[:4]+'.'+date[4:6]+'.'+date[6:8]
                        
                        yield (float(row[1]), 1/float(row[2]),date)
                except:
                    f.close()
                    print "HI"
                    raise IOError