from glob import glob
import sys
try:
    import Image
except ImportError:
    from PIL import Image
#from PIL import UnidentifiedImageError

infile = sys.argv[1]
outfile = sys.argv[2]
file1 = open(outfile,'w')
#for name in glob('/home/brian/facenet-master/datasets/m36_dry/m36_dry/*'):
#for name in glob('/home/brian/facenet-master/datasets/m18/m18/*'):
for name in glob(infile+'/*'):
	
	#data = name.split('.')
	if '.jpg' not in name:#data[-2]!='jpg':
		continue 

	try:
		img = Image.open(name)
		file1.write(name+'\n')
		print(name)
	except:
		print('error file:', name)