from glob import glob
import sys
infile = sys.argv[1]
outfile = sys.argv[2]
file1 = open(outfile,'w')
#for name in glob('/home/brian/facenet-master/datasets/m36_dry/m36_dry/*'):
#for name in glob('/home/brian/facenet-master/datasets/m18/m18/*'):
for name in glob(infile+'/*'):
	print(name)
	file1.write(name+'\n')