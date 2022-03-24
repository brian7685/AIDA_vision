# AIDA_vision

docker pull brian271828/event-extraction:0.8

# The input folders are
1. LDC source data
2. ttl folders with contains output_ttl_cond56_en,output_ttl_cond56_es,output_ttl_cond56_ru,output_ttl_cond7_en,output_ttl_cond7_es,output_ttl_cond7_ru
3. Output ttl folder


# For dry run

docker run \
-v /home/brian/AIDA/dry_run_2021/data/LDC2021E11_AIDA_Phase_3_Practice_Topic_Source_Data_V2.0:/app/LDC_data \
-v /home/brian/AIDA/dry_run_2021/uiuc_out/0302/v3:/app/input_ttl_folder \
-v /home/brian/AIDA/docker:/app/docker_out \
-e CUDA_VISIBLE_DEVICES=0,1,2,3 --gpus=4 --shm-size=50gb -it [IMAGE ID] /bin/bash

user@76e2145094c8:/app$ ./docker_script_dry.sh

# Five pid for testing visual component
output_ttl_cond56_en
L0C04AR3P
L0C04AKLF
L0C04AJZ0
L0C04AJ15
L0C04AHYZ

# For eval

docker run \
-v /home/brian/dvmm-filler2/projects/AIDA/data/LDC2022R02_AIDA_Phase3_Evaluation_Source_Data_V1.0:/app/LDC_data \
-v /home/brian/AIDA/dry_run_2021/uiuc_out/0306/output_ttls:/app/input_ttl_folder \
-v /home/brian/AIDA/docker:/app/docker_out \
-e CUDA_VISIBLE_DEVICES=0,1,2,3 --gpus=4 --shm-size=50gb -it [IMAGE ID] /bin/bash

user@76e2145094c8:/app$ ./docker_script.sh
