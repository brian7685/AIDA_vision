

echo CU vision begin...


# mkdir dry_jpg

cd /app/swig 
# python ldcc.py \
# /input/data/jpg/jpg/ \
# dry_jpg/
# $1 = /input
# $2 = /output
INPUT=$1
OUTPUT=$2
echo Create list...

python create_list.py \
${INPUT}/data/jpg \
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

sudo chmod 777 ${OUTPUT}
sudo chmod 777 ${OUTPUT}/WORKING

if ls ${OUTPUT}/WORKING/en/ltf/* >/dev/null 2>&1; then
    python core_graph_21_tmp.py \
    swig_final_dry.p \
    ${INPUT}/docs/parent_children.tab \
    ${OUTPUT}/WORKING/cu_text/output/en \
    ${OUTPUT}/WORKING/cu_vision/output/en
fi

if ls ${OUTPUT}/WORKING/es/ltf/* >/dev/null 2>&1; then
    python core_graph_21_tmp.py \
    swig_final_dry.p \
    ${INPUT}/docs/parent_children.tab \
    ${OUTPUT}/WORKING/cu_text/output/es \
    ${OUTPUT}/WORKING/cu_vision/output/es
fi

if ls ${OUTPUT}/WORKING/ru/ltf/* >/dev/null 2>&1; then
    python core_graph_21_tmp.py \
    swig_final_dry.p \
    ${INPUT}/docs/parent_children.tab \
    ${OUTPUT}/WORKING/cu_text/output/ru \
    ${OUTPUT}/WORKING/cu_vision/output/ru
fi

echo CU merge graph end ..

echo remove temp file ..
rm dry_jpg.txt
rm results.json
rm swig_final_dry.json
rm swig_final_dry.p

