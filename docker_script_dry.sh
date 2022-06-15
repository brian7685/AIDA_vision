

#echo CU ldcc convert...
# mkdir dry_jpg

cd /app/swig 
# python ldcc.py \
# /input/data/jpg/jpg/ \
# dry_jpg/
 
echo Create list...

python create_list.py \
/input/data/jpg \
dry_jpg.txt

echo CU event predict..

CUDA_VISIBLE_DEVICES=0 python ./JSL/inference.py --verb-path weights/verb_check_26.pth.tar \
--jsl-path weights/JSL_27.pth \
--image-file dry_jpg.txt --batch-size 4

echo CU create graph..

python read_swig.py \
results.json \
swig_final_dry.json

python read_event_new.py \
swig_final_dry.json \
swig_final_dry.p

sudo chmod 777 /output
sudo chmod 777 /output/WORKING

python core_graph_21_tmp.py \
swig_final_dry.p \
/input/docs/parent_children.tab \
/output/WORKING/cu_text/output/en \
/output/WORKING/cu_vision/output/en

python core_graph_21_tmp.py \
swig_final_dry.p \
/input/docs/parent_children.tab \
/output/WORKING/cu_text/output/es \
/output/WORKING/cu_vision/output/es

python core_graph_21_tmp.py \
swig_final_dry.p \
/input/docs/parent_children.tab \
/output/WORKING/cu_text/output/ru \
/output/WORKING/cu_vision/output/ru

echo CU merge graph end ..

echo remove temp file ..
rm dry_jpg.txt
rm results.json
rm swig_final_dry.json
rm swig_final_dry.p