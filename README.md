# AIDA_vision
```
docker pull brian271828/event-extraction:1.5
```

# The input folders are
1. LDC source data in /input
2. ttl folders from Columbia Text in /output/WORKING/cu_text/output/{en,es,ru}/.ttl
3. Output ttl folders from Columbia Vision in /output/WORKING/cu_vision/output/{en,es,ru}/.ttl


# Run the docker
```
INPUT=/home/brian/AIDA/dry_run_2021/data/LDC2021E11_AIDA_Phase_3_Practice_Topic_Source_Data_V2.0
OUTPUT=/home/brian/AIDA/dry_run_2021/docker_output
docker run \
-v ${INPUT}:/input \
-v ${OUTPUT}:/output \
-e CUDA_VISIBLE_DEVICES=0,1,2,3 --gpus=4 --shm-size=50gb -it [IMAGE ID] /bin/bash

user@76e2145094c8:/app$ ./docker_script_dry.sh /input /output
```
Five pid for testing visual component
In 'output_ttl_cond56_en' folder
L0C04AR3P
L0C04AKLF
L0C04AJZ0
L0C04AJ15
L0C04AHYZ

