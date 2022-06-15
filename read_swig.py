import pickle
import sys
from glob import glob
import json
infile = sys.argv[1]
outfile = sys.argv[2]

Attack = ['attacking']# 'hitting', 'kicking', 'striking']
Protest = ['protesting','marching']
Meet = ['interviewing','talking','discussing','gathering']#,'shaking']
Correspondence = ['calling','communicating','dialing','phoning', 'telephoning']
Broadcast = ['speaking']
TransportPerson = ['Commuting','boarding','disembarking','landing','taxiing']
PreventEntry = ['blocking']#,'guarding']
SelfMotion = [ 'riding', 'driving', 'biking','piloting','steering','boating']
TransferMoney = ['paying']
Transaction	= ['selling']
DamageDestroy = ['breaking', 'destroying']
AccidentCrash = ['crashing']
CastVote = ['voting']
ArrestJailDetain = ['detaining']

#img_result = pickle.load( open( infile, "rb" ) )

with open('arg_map.json', "r") as read_file:
    print("Converting JSON encoded data into Python dictionary")
    mapping = json.load(read_file)

with open('type_mapping.json', "r") as read_file:
    print("Converting JSON encoded data into Python dictionary")
    type_map = json.load(read_file)

with open('name2label.json', "r") as read_file:
    print("Converting JSON encoded data into Python dictionary")
    name2label = json.load(read_file)

with open('SWiG_jsons/imsitu_space.json', "r") as read_file:
    print("Converting JSON encoded data into Python dictionary")
    swig = json.load(read_file)
for x,y in swig.items():
	print(x)
	#print(y)
	break

print(swig['nouns']['n08524735']['gloss'][0])
print(swig['verbs']['admiring']['order'])


img_result = {}
with open(infile, "r") as read_file:
    print("Converting JSON encoded data into Python dictionary")
    developer = json.load(read_file)

i=0
def print_arg(verb, nouns, boxes):
	n_c = 0
	#swig_dic = {}
	print('verb: '+verb)
	arg_list = []
	for n in nouns:
		#need arg here
		arg_role = swig['verbs'][verb]['order'][n_c]
		if arg_role not in mapping[verb].keys():
			continue
		if n!= '' :
			arg_label = swig['nouns'][n]['gloss'][0]
			#print(mapping[verb][arg_role]+': '+arg_label)
			
		else:
			arg_label = ''
			#print(mapping[verb][arg_role]+': '+'')
		if arg_label in name2label.keys():
			arg_list.append({'arg_role':mapping[verb][arg_role],'arg_label':arg_label,'bbox':boxes[n_c],'arg_type':name2label[arg_label]})
		else:
			arg_list.append({'arg_role':mapping[verb][arg_role],'arg_label':arg_label,'bbox':boxes[n_c],'arg_type':""})
		n_c+=1
	#swig_dic = {'verb':verb,''}
	print(arg_list)
	print()
	return arg_list
"""
for x,y in developer.items():
	if y['verb'] in Attack:
		print(x)
		print(y['verb'])
		print_arg(y['verb'],y['nouns'])

		for b in y['boxes']:
			print(b)
		print()
	i+=1
	#if i>3:
	#	break
#for name in glob(infile+'/*'):
"""
img_result_aida = {}
count=0
#"""
for x,y in developer.items():
	#print(x)
	x = x.split('.')[0]
	verb = y['verb']
	nouns = y['nouns']
	boxes = y['boxes']
	if verb in Attack:
		arg_list = print_arg(verb, nouns, boxes)
		img_result_aida[x] = ({'event':'Conflict.Attack','arg_list':arg_list})

	if verb in Protest:
		arg_list = print_arg(verb, nouns, boxes)
		img_result_aida[x] = ({'event':'Conflict.Demonstrate.MarchProtestPoliticalGathering','arg_list':arg_list})

	if verb in Meet:
		arg_list = print_arg(verb, nouns, boxes)
		img_result_aida[x] = ({'event':'Contact.Collaborate.Meet','arg_list':arg_list})

	if verb in Correspondence:
		arg_list = print_arg(verb, nouns, boxes)
		img_result_aida[x] = ({'event':'Contact.CommitmentPromiseExpressIntent.Correspondence','arg_list':arg_list})

	if verb in Broadcast:
		arg_list = print_arg(verb, nouns, boxes)
		img_result_aida[x] = ({'event':'Contact.MediaStatement.Broadcast','arg_list':arg_list})

	if verb in TransportPerson:
		arg_list = print_arg(verb, nouns, boxes)
		img_result_aida[x] = ({'event':'Movement.TransportPerson','arg_list':arg_list})

	if verb in PreventEntry:
		arg_list = print_arg(verb, nouns, boxes)
		img_result_aida[x] = ({'event':'Movement.TransportPerson.PreventEntry','arg_list':arg_list})

	if verb in SelfMotion:
		arg_list = print_arg(verb, nouns, boxes)
		img_result_aida[x] = ({'event':'Movement.TransportPerson.SelfMotion','arg_list':arg_list})

	if verb in TransferMoney:
		arg_list = print_arg(verb, nouns, boxes)
		img_result_aida[x] = ({'event':'Transaction.TransferMoney','arg_list':arg_list})

	if verb in Transaction:
		arg_list = print_arg(verb, nouns, boxes)
		img_result_aida[x] = ({'event':'Transaction.Transaction','arg_list':arg_list})

	if verb in DamageDestroy:
		arg_list = print_arg(verb, nouns, boxes)
		img_result_aida[x] = ({'event':'ArtifactExistence.DamageDestroy','arg_list':arg_list})

	if verb in AccidentCrash:
		arg_list = print_arg(verb, nouns, boxes)
		img_result_aida[x] = ({'event':'Disaster.AccidentCrash','arg_list':arg_list})

	if verb in CastVote:
		arg_list = print_arg(verb, nouns, boxes)
		img_result_aida[x] = ({'event':'Government.Vote.CastVote','arg_list':arg_list})

	if verb in ArrestJailDetain:
		arg_list = print_arg(verb, nouns, boxes)
		img_result_aida[x] = ({'event':'Justice.ArrestJailDetain.ArrestJailDetain','arg_list':arg_list})
#""" 
#pickle.dump(img_result_aida, open(outfile, "wb" ) )
json.dump(img_result_aida, open(outfile, "w" ) )
