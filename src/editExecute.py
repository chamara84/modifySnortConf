import re
import time
import argparse
from docutils.parsers import null
from subprocess import check_output
import os, signal

def get_pid(name):
    return check_output(["pidof",name])
# Setup argument parser
parser = argparse.ArgumentParser()
parser.add_argument("snortconf")
parser.add_argument("modpath")

# Process arguments
args = parser.parse_args()

inpath = args.snortconf
moddatapath = args.modpath
        
#input file
fin = open(inpath, "r+",encoding='utf-8')


#data file to write the result to
fdata = open(moddatapath, "r+",encoding='utf-8')



data = fin.readlines()
fin.close()

        
modData = fdata.readlines()
fdata.close()
modDataListSet = []
modDataList = []

for line in modData:
    modDataList.append(line)
    if line.find("wait")!=-1:
        modDataListSet.append(modDataList.copy())
        modDataList.clear()

        
        #for each line in the input file


for num, line in enumerate(data):
    #print(line)    
    m = re.search('preprocessor\s+dnp3', line)
    if m!=None:
        print(line)
        for listEntry in modDataListSet:
            for element in listEntry:
                if element.find("wait")==-1:
                    splitElement = element.split()
                    searchExp = splitElement[0]+'\s+'+splitElement[1]+'\s+'+splitElement[2]+'\s+'+splitElement[3]+'\s+'+splitElement[4]+"\s+[0-9.]+\s*"
                    for num1, line in enumerate(data[num:]):
                        
                        m = re.search(searchExp , line)
                        if m!=None:
                            print(line)
                            if line.find("\\")!=-1:
                                data[num+num1] = element.replace("\n", "")+"  \\ \n"
                            else:
                                data[num+num1] = element.replace("\n", "")+" \n"
                else:
                    splitElement = element.split()
                    fout = open(inpath, "w")    
                    for line in data:
                        fout.write(line)

                    fout.close()
                    time.sleep(float(re.sub("[^0-9.]", "", splitElement[1])))
                    print(get_pid("snort")) 
                    pid = int(get_pid("snort"))
                    cmd = "sudo kill -SIGHUP %s" % pid
                    print(os.system(cmd))
                    #os.kill(int(get_pid("snort")), signal.SIGHUP)
                
              
                #read replace the string and write to output file
                #fout.write(line.replace('pyton', 'python'))
                #close input and output files
            
            
