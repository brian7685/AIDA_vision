from rdflib import Graph, plugin, URIRef, Literal, BNode, RDF
from rdflib.serializer import Serializer
from rdflib.namespace import SKOS
import rdflib
import pickle
import os
import pprint
import sys
from pqdm.processes import pqdm
from pathlib import Path
sys.path.append("AIDA-Interchange-Format/python/")

from aida_interchange import aifutils
from aida_interchange.bounding_box import Bounding_Box
from aida_interchange.rdf_ontologies import ldc_ontology_m36, interchange_ontology
from io import BytesIO
from collections import defaultdict
#c = 'ttl'
event_co_path = sys.argv[1] #'event_info_eval.pickle'
tab_path = sys.argv[2] #uiuc_event.p
#event_text_path = sys.argv[3] #'event_info_eval.pickle'

out_ttl = sys.argv[4] #imSitu_36.p
#Path(out_ttl).mkdir(parents=True, exist_ok=True)

Path(out_ttl).mkdir(parents=True, exist_ok=True)
txt_mention_ttl_path = sys.argv[3]#'/home/brian/AIDA/dry_run_2021/output_ttl_en'
#merged_graph_path = sys.argv[6]#'/home/brian/AIDA/dry_run_2021/output_cu_ttl'


txt_mention_ttl_list = set([f.split('.')[0] for f in os.listdir(txt_mention_ttl_path)])
txt_mention_ttl_list = sorted(txt_mention_ttl_list)

pp = pprint.PrettyPrinter(indent=4)
event_co = pickle.load(open(event_co_path,'rb'))
event_text = {}#pickle.load(open(event_text_path,'rb'))
event_co2 = {}
for x,y in event_co.items():
	event_co2[x.replace('.jpg','')] = y
event_co = event_co2
#tab_path ='/dvmm-filer2/projects/AIDA/data/ldc_eval_m18/LDC2019E42_AIDA_Phase_1_Evaluation_Source_Data_V1.0/docs/parent_children.sorted.tab'
with open(tab_path,'r') as f:
	lines = f.readlines()
	lines = [line.split() for line in lines]
parent_dict = {}
child_dict = {}
for line in lines[1:]:
	#print(line)
	if len(line)<1:
		print('end')
		continue
	parent_id = line[2]
	child_id = line[3]#+line[5]
	# child_id = child_id.replace('.ldcc','')
	# if 'jpg' not in line[5]:
	# 	continue
	##updating parent_dict
	if parent_id in parent_dict:
		parent_dict[parent_id].update([child_id])
	else:
		parent_dict[parent_id] = set([child_id])
#print(ldc_ontology_m36.PER)
#print(ldc_ontology_m36.Life.Die.DeathCausedByViolentEvents_Victim)
#print(parent_dict)
m36_url = 'https://raw.githubusercontent.com/NextCenturyCorporation/AIDA-Interchange-Format/master/java/src/main/resources/com/ncc/aif/ontologies/LDCOntologyM36#'
"""
mapping = {
	"Conflict.Attack":ldc_ontology_m36.Conflict.Attack,
	"Conflict.Demonstrate.MarchProtestPoliticalGathering":ldc_ontology_m36.Conflict.Demonstrate.MarchProtestPoliticalGathering,
	"Contact.Collaborate.Meet":ldc_ontology_m36.Contact.Collaborate.Meet,
	"Contact.CommitmentPromiseExpressIntent.Correspondence":ldc_ontology_m36.Contact.CommitmentPromiseExpressIntent.Correspondence,
	"Contact.MediaStatement.Broadcast":ldc_ontology_m36.Contact.MediaStatement.Broadcast,
	"Movement.TransportArtifact":ldc_ontology_m36.Movement.TransportArtifact,
	"Movement.TransportPerson.PreventEntry":ldc_ontology_m36.Movement.TransportPerson.PreventEntry,
	"Movement.TransportPerson.SelfMotion":ldc_ontology_m36.Movement.TransportPerson.SelfMotion,
	"Transaction.TransferMoney":ldc_ontology_m36.Transaction.TransferMoney,
	"Transaction.Transaction":ldc_ontology_m36.Transaction.Transaction,
	"ArtifactExistence.DamageDestroy":ldc_ontology_m36.ArtifactExistence.DamageDestroy,
	"Diaster.AccidentCrash":ldc_ontology_m36.Diaster.AccidentCrash,
	"Government.Vote.CastVote":ldc_ontology_m36.Government.Vote.CastVote,
	"Justice.ArrestJailDetain":ldc_ontology_m36.Justice.ArrestJailDetain
}
"""
def bb_intersection_over_union(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    # compute the area of intersection rectangle
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)
    #iou = interArea / float(boxBArea)

    # return the intersection over union value
    return iou
def create_cluster(g, entity):
	clusterName = aifutils.make_cluster_with_prototype(g, \
		"http://www.columbia.edu/AIDA/DVMM/Clusters/EventArgument/RUN00010/JPG/"\
		+key+"/"+str(n),entity_dict[eid], system)

	aifutils.mark_as_possible_cluster_member(g, \
			entity,clusterName, score, system)

def link_to_obj(key, g, entity,bb):
    #system = aifutils.make_system_with_uri(g, "http://www.columbia.edu/AIDA/DVMM/Systems/Face/FaceNet")
    system = aifutils.make_system_with_uri(g,  "http://www.columbia.edu/AIDA/DVMM/Systems/Events/imSitu")
    person_label = ['/m/01g317','/m/04yx4','/m/03bt1vf','/m/01bl7v','/m/05r655','/m/04hgtk','/m/01bgsw']
    first_cluster = 1
    if key in OD_result.keys():
        for n in range(len(OD_result[key])):

            #print OD_result[key][n]['label']
            #if OD_result[key][n]['label'] in person_label:
                #print OD_result[key][n]['label']
            boxA = OD_result[key][n]['bbox']
            boxB = (int(bb[0]),int(bb[1]),int(bb[2]),int(bb[3]))
            IOA = bb_intersection_over_union(boxA, boxB)
            if IOA > 0.7: 

                eid = "http://www.columbia.edu/AIDA/DVMM/Entities/ObjectDetection/RUN00010/JPG/"+key+"/"+str(n)
                #print (entity_dic2[key])
                #print n
                if n in entity_dic2[key]:
                #if eid in entity_dict.keys():
                    score = IOA

                    #eid_list.append(eid)
                    if first_cluster == 1:

                        first_cluster = 0
                        clusterName = aifutils.make_cluster_with_prototype(g, \
                        "http://www.columbia.edu/AIDA/DVMM/Clusters/EventArgument/RUN00010/JPG/"\
                        +key+"/"+str(n),entity_dict[eid], system)

                    aifutils.mark_as_possible_cluster_member(g, \
                            entity,clusterName, score, system)

        #if first_cluster == 0:

        #    person_c_n+=1
    return g
print(event_co.keys())
#pp.pprint(event_co)
#for i,pid in enumerate(parent_dict):
def create_g(pid):
	#print(pid)
	g = Graph()
	g.bind('ldcOnt', ldc_ontology_m36.NAMESPACE)
	g.bind('aida', interchange_ontology.NAMESPACE)
	text_e_dic = {}
	event_co_n = 0
	has_event = 0
	try:
		turtle_path = os.path.join(txt_mention_ttl_path, pid+'.ttl')
		turtle_content = open(turtle_path).read()
		g.parse(data=turtle_content, format='n3')
		has_event=1
		print('text graph: ', pid)
	except:
		a=0
		return
		#print('no text: ',c_id)
	has_v_event=0
	for c_id in parent_dict[pid]: 
		#if c_id == 'L0C04ATPA':
		#	print('exist')
		#print()
		if c_id in event_co.keys():
			print('visual event',c_id)
			#if 'event_lang' in event_co[c_id].keys():
			#if 'event_co' in event_co[c_id].keys():
			has_event=1
			has_v_event=1
			#print(pid)
			#pp.pprint(event_co[c_id])
			#print('event_text',event_text.keys())
			img_id = c_id.split('.')[0]
			system = aifutils.make_system_with_uri(g,  "http://www.columbia.edu/AIDA/DVMM/Systems/Events/imSitu")

			if pid in event_text.keys():
				type2eid = {}
				for e in event_text[pid]:
					type2eid[e[1]]=e[0]
				#print('type2eid',type2eid)
				
				
				#print('event',event_co[c_id]['event'])
				if event_co[c_id]['event'] in type2eid.keys():
					print('match',event_co[c_id]['event'],type2eid.keys())
					#text_e = event_text[pid]
					#print(text_e)
					text_e = type2eid[event_co[c_id]['event']]
					aref = URIRef(text_e)
					if text_e not in text_e_dic.keys():

						clusterName = aifutils.make_cluster_with_prototype(g, \
						"http://www.columbia.edu/AIDA/DVMM/Clusters/EventCoreference/RUN00010/JPG/"\
						+img_id+"/"+str(event_co_n),aref, system)
						event_co_n+=1
						text_e_dic[text_e] = clusterName
						#text_e_set.add(text_e)
					score = 0.9#event_co[c_id]['score']

			

			event = aifutils.make_event(g, \
			"http://www.columbia.edu/AIDA/DVMM/Events/imSitu/RUN00010/JPG/"+img_id+'/'\
				+event_co[c_id]['event'], system)
			
			# mark the event as a Personnel.Elect event; type is encoded separately so we can express
			# uncertainty about type
			aref = URIRef(m36_url+event_co[c_id]['event'])
			type_assertion = aifutils.mark_type(g, "http://www.columbia.edu/AIDA/DVMM/TypeAssertion/imSitu/RUN00010/JPG/"+img_id+'/'\
				+event_co[c_id]['event'], event, aref, system, 1.0)


			bb2 = Bounding_Box((0, 0), (500, 500))
			justif = aifutils.mark_image_justification(g, [event, type_assertion], c_id, bb2, system, 1)
			aifutils.add_source_document_to_justification(g, justif, pid)
			aifutils.mark_informative_justification(g, event, justif) 

			clusterName = aifutils.make_cluster_with_prototype(g, \
			"http://www.columbia.edu/AIDA/DVMM/Clusters/Events/imSitu/RUN00010/JPG/"+img_id+'/'\
				+event_co[c_id]['event'],event, system)
			score = 0.99
			aifutils.mark_as_possible_cluster_member(g, \
				event,clusterName, score, system)

			#"""
			# create the two entities involved in the event
			arg_set = set()
			for arg in event_co[c_id]['arg_list']:
				#print('arg_role',arg['arg_role'])
				
				bb = arg['bbox'] 
				print('bb',bb)   
				if bb != None and arg['arg_type']!='':
					role = arg['arg_role'].split('_')[-1] 
				
					#arg_dict_img[role].append()
					aref = URIRef(m36_url+arg['arg_type'])
					arg_role_ent = aifutils.make_entity(g, \
						"http://www.columbia.edu/AIDA/DVMM/EventEntity/imSitu/RUN00010/JPG/"+\
						img_id+'/'+arg['arg_role'], system)
					if arg['arg_role'] not in arg_set:
						arg_set.add(arg['arg_role'])
					else:
						continue
					type_assertion = aifutils.mark_type(g, \
						"http://www.columbia.edu/AIDA/DVMM/TypeAssertion/EventEntity/imSitu/RUN00010/JPG/"+img_id+'/'\
					+arg['arg_role'], arg_role_ent, aref, system, 1.0)
					print('arg_role_ent',arg_role_ent)
					bb2 = Bounding_Box((bb[0], bb[1]), (bb[2], bb[3]))
					justif = aifutils.mark_image_justification(g, [arg_role_ent, type_assertion], c_id, bb2, system, 1)
					print('justif',justif)
					aifutils.add_source_document_to_justification(g, justif, pid)
					aifutils.mark_informative_justification(g, arg_role_ent, justif)
					#g = link_to_obj(img_id,g,arg_role_ent, bb)
					clusterName = aifutils.make_cluster_with_prototype(g, \
					"http://www.columbia.edu/AIDA/DVMM/Clusters/EventEntity/imSitu/RUN00010/JPG/"+img_id+'/'\
					+arg['arg_role'],arg_role_ent, system)
					score = 0.99
					aifutils.mark_as_possible_cluster_member(g, \
						arg_role_ent,clusterName, score, system)


					aref = URIRef(m36_url+arg['arg_role'])
					#aifutils.mark_as_argument(g, event, aref, arg_role_ent, system, 1)
			#print()
			if pid in event_text.keys():
				if event_co[c_id]['event'] in type2eid.keys():
					aifutils.mark_as_possible_cluster_member(g, \
						event,text_e_dic[text_e], score, system)
			# else:
			# 	has_event=1
			# 	img_id = c_id.split('.')[0]
			# 	system = aifutils.make_system_with_uri(g,  "http://www.columbia.edu/AIDA/DVMM/Systems/Events/imSitu")

			# 	event = aifutils.make_event(g, "http://www.columbia.edu/AIDA/DVMM/Events/imSitu/RUN00010/JPG/"+img_id+'/'\
			# 		+event_co[c_id]['event'], system)
				
			# 	# mark the event as a Personnel.Elect event; type is encoded separately so we can express
			# 	# uncertainty about type
			# 	aref = URIRef(m36_url+event_co[c_id]['event'])
			# 	type_assertion = aifutils.mark_type(g, \
			# 		"http://www.columbia.edu/AIDA/DVMM/TypeAssertion/imSitu/RUN00010/JPG/"+img_id+'/'\
			# 		+event_co[c_id]['event'], event, aref, system, 1.0)



			# 	bb2 = Bounding_Box((0, 0), (500, 500))
			# 	justif = aifutils.mark_image_justification(g, [event, type_assertion], c_id, bb2, system, 1)
			# 	aifutils.add_source_document_to_justification(g, justif, pid)
			# 	aifutils.mark_informative_justification(g, event, justif) 
			# 	#"""
			# 	# create the two entities involved in the event
			# 	for arg in event_co[c_id]['arg_list']:
			# 		#print(arg['arg_role'])
					
			# 		bb = arg['bbox']  

			# 		if bb != None and arg['arg_type']!='':
			# 			role = arg['arg_role'].split('_')[-1] 
					
			# 			#arg_dict_img[role].append()
			# 			aref = URIRef(m36_url+arg['arg_type'])
			# 			arg_role_ent = aifutils.make_entity(g, \
			# 				"http://www.columbia.edu/AIDA/DVMM/EventEntity/imSitu/RUN00010/JPG/"+\
			# 				img_id+'/'+arg['arg_role'], system)
			# 			type_assertion = aifutils.mark_type(g, \
			# 				"http://www.columbia.edu/AIDA/DVMM/TypeAssertion/EventEntity/imSitu/RUN00010/JPG/"+img_id+'/'\
			# 			+arg['arg_role'], arg_role_ent, aref, system, 1.0)
			# 			bb2 = Bounding_Box((bb[0], bb[1]), (bb[2], bb[3]))
			# 			justif = aifutils.mark_image_justification(g, [arg_role_ent, type_assertion], c_id, bb2, system, 1)
			# 			aifutils.add_source_document_to_justification(g, justif, pid)
			# 			aifutils.mark_informative_justification(g, arg_role_ent, justif) 
			# 			#g = link_to_obj(img_id,g,arg_role_ent, bb)

			# 			aref = URIRef(m36_url+arg['arg_role'])
			# 			aifutils.mark_as_argument(g, event, aref, arg_role_ent, system, 1)
				#else:
				#	print(c_id)
				#	pp.pprint(event_co[c_id])
		
	#if not os.path.exists(out_ttl):
	#	os.makedirs(out_ttl)
	

	if has_v_event==1:
		print('pid',pid)
	if has_event==1:
		#print('has event')
		with open(out_ttl+'/'+pid+'.ttl', 'w') as fout:
			print('out_ttl',out_ttl+'/'+pid+'.ttl')
			serialization = BytesIO()
			# need .buffer because serialize will write bytes, not str
			g.serialize(destination=serialization, format='turtle')
			fout.write(serialization.getvalue().decode('utf-8'))
	#break
#print(parent_dict['IC001L4L5'][0])
#return parent_dict, child_dict
#
# for p in parent_dict.keys():
	
# 	# if 'L0C04APPZ' not in p:
# 	# 	continue
# 	print('p',p)
# 	create_g(p)
	#break
result = pqdm(parent_dict.keys(), create_g, n_jobs=96)
