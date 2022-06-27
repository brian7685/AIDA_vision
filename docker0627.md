INPUT=/home/brian/AIDA/dry_run_2021/data/LDC2021E11_AIDA_Phase_3_Practice_Topic_Source_Data_V2.0
OUTPUT=/home/brian/AIDA/dry_run_2021/docker_output
docker run \
-v ${INPUT}:/ldc_root \
-v ${OUTPUT}:/output_root \
-e CUDA_VISIBLE_DEVICES=0,1,2,3 --gpus=4 --shm-size=50gb -it 2aada310ff65 /bin/bash

user@76e2145094c8:/app$ ./docker_script_dry.sh ldc_root output_root