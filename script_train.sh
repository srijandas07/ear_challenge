
python -m torch.distributed.launch --nproc_per_node=8 main_train.py -cfg ./configs/config_challenge_train.yaml --output ./work_dirs/challenge_baseline_new/ --opts TEST.NUM_CLIP 1 TEST.NUM_CROP 1

