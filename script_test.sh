export MASTER_ADDR='localhost'  # Adjust this to the IP as required
export MASTER_PORT=29800  # Ensure this port is available
python -m torch.distributed.launch --nproc_per_node=1 --master_addr $MASTER_ADDR --master_port $MSTER_PORT main_challenge.py -cfg ./configs/config_challenge_test.yaml --output ./work_dirs/
python merge_results.py
