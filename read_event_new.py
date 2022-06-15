# %%
import pickle
import sys
import difflib
import pprint
pp = pprint.PrettyPrinter(indent=4)
import json
from collections import defaultdict


# grounding_result = sys.argv[1] #'event_info_eval.pickle'
# uiuc_event = sys.argv[2] #uiuc_event.p
# img_event = sys.argv[3] #imSitu_36.p
# parent_file = sys.argv[4]
# outfile = sys.argv[5]

# event = pickle.load(open(grounding_result,'rb'))

# # %%
# event_dic = pickle.load(open( uiuc_event, "rb" ) )
img_event = sys.argv[1] #imSitu_36.p
outfile = sys.argv[2]
# %%
img_result = json.load(open(img_event,'r'))
pickle.dump(img_result,open(outfile,'wb'))

# #print(img_result.keys())
# def get_overlap(s1, s2):
#     s = difflib.SequenceMatcher(None, s1, s2)
#     pos_a, pos_b, size = s.find_longest_match(0, len(s1), 0, len(s2)) 
#     return s1[pos_a:pos_a+size]

# #Image(filename='test.png')
# i=0
# cor = 0
# img_set = set()
# for x,ys in event.items():
#     #print(x)
#     data = x.split('.')[0]
#     jpg_title = x.replace('.ldcc','')
#     for y in ys:
#         if y['score']>0.5 and 'in the image' not in y['sentence']:
#             i+=1
#             if y['sentence'] in event_dic.keys() and jpg_title in img_result.keys():
                
#                 img_event = img_result[jpg_title]['event']  
#                 if 'PreventEntry' in img_event:
#                     continue
#                 img_e = img_event.split('.')[0]
                
#                 #print(event_dic[y['sentence']])
#                 text_s = set()
#                 event_l2n = {}
#                 for text_e in event_dic[y['sentence']]:
#                     #print('text event node: ',text_e[0])
#                     text_s.add(text_e[1])
#                     event_n2l = {text_e[0]:text_e[1]}
#                     event_n2arg = {text_e[0]:text_e[2]}
#                 for e_node, text_e in event_n2l.items():
#                     text_general = text_e.split('.')[0]
#                     #if img_e == text_general:
#                     if len(get_overlap(text_e,img_event))>12:
#                     #print('match')
                     
#                         if 'SelfMotion' in text_e:
#                             continue
#                         if data in img_set:
#                             continue
#                         #img_set.add(data)
#                         """
#                         print(x)
                        
#                         img_result[jpg_title].update({'event_co':e_node,'score':y['score']})
#                         print()
#                         print('img_event: ',img_result[jpg_title]['event'])
#                         print()
#                         print('score: ',img_result[jpg_title]['score'])
#                         pp.pprint(img_result[jpg_title]['arg_list'])
#                         """
#                         arg_dict_img = defaultdict(list)
#                         for arg in img_result[jpg_title]['arg_list']:
#                             #print(arg['arg_role'])
#                             role = arg['arg_role'].split('_')[-1]
#                             arg_dict_img[role].append(arg['arg_type'])
#                         """
#                         print('img arguments:')
#                         pp.pprint(arg_dict_img)
                        
                        
#                         img = Image(filename='img_data_m36/'+data+'.jpg', width=200)
#                         display(img)
#                         #print('image event: ',img_event)
                        
#                         if '_' in text_e:
#                             text_e = text_e.split('_')[0]
#                         print()
#                         print('sentence: ', y['sentence'])
#                         print()
#                         print('text event: ',text_e)
#                         arg_dict_txt = defaultdict(list)
#                         print('event node: ',e_node)
#                         for args in event_n2arg[e_node]:
#                             print()
#                             print('argument: ',args[1])
#                             print('arg_role:',args[0])
#                             print('arg_type:',args[3])
#                             role = args[0].split('_')[-1]
#                             arg_dict_txt[role].append(args[3])
#                         print()
#                         print('text arguments:')
#                         pp.pprint(arg_dict_txt)
#                         is_coreference = 1
#                         for x,y in arg_dict_img.items():
#                             if x=='Place':
#                                 continue
#                             print(x,y[0])
#                             print(arg_dict_txt[x])
#                             match=0
#                             if len(arg_dict_txt[x])==0:
#                                 match=1
#                             role_same=0
#                             for txt_role in arg_dict_txt[x]:
                                
#                                 if y[0] in txt_role:
#                                     match=1
#                                     role_same=1
#                                     #break
#                                 #if 
                                
#                             if match==0:
#                                 is_coreference=0
#                                 print('not coreference')
#                                 break
#                         """
#                         img_result[jpg_title].update({'event_co':e_node,'score':y['score']})
#                         #print('is coreference:', is_coreference)
#                         #print()
#                         #print('================================================================')
#                         #print()
#                         #cor+=1
#                         #"""
#                         #print(cor)
#                         #img_result[jpg_title].update({'event_co':e_node,'score':y['score']})
#                         #pp.pprint(img_result[jpg_title])
#                         """
#                         display(Image(filename='m18/m18/'+data+'.jpg', width=500))
#                         print('image event: ',img_result[data][0])
#                         print('text event: ',text_e)
#                         print()
#                         print('================================================================')
#                         print()
#                         cor+=1
#                         """
#     #break
    
#     #if i>100:
#     #    break
# #print(i)
# #print(cor)
# #pp.pprint(img_result)
# #print(len(img_result))
# from collections import defaultdict
# child = defaultdict(list)
# file5= open(parent_file, encoding="utf-8")
# i = 0
# lang = {}
# c2p = {}
# for line in file5:
#     i+=1
#     if i ==1:
#         continue
#     data = line.split()
#     child[data[2]].append(data[3])
#     c2p[data[3]]=data[2]
#     #print(data[7])
#     if data[7]=='eng':
#         lang[data[2]] = 'eng'
#     if data[7]=='rus':
#         lang[data[2]] = 'rus'
#     if data[7]=='spa':
#         lang[data[2]] = 'spa'

# i=0
# #print(img_result)
# for x,y in img_result.items():
    
#     img_id = x.split('.')[0]
#     if c2p[img_id] in lang.keys() and lang[c2p[img_id]] == 'rus':
#         #print('='*30)
#         #print(x,y)
#         #img = Image(filename='img_data_m36/'+x, width=200)
#         img_result[x].update({'event_lang':'rus'})
#         #display(img)
#         i+=1

#pickle.dump(img_result,open(outfile,'wb'))