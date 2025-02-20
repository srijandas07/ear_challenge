# ViFi-CLIP Baseline for Elderly Action Recognition (EAR) Challenge


   
# Model Zoo
NOTE: All models in our experiments below uses publicly available ViT/B-16 based CLIP model.

## Installation 
For installation and other package requirements, please follow the instructions below :
```
# Create a conda environment
conda create -y -n vclip python=3.7
# Activate the environment
conda activate vclip
# Install requirements
pip install -r requirements.txt
pip install torch===1.8.1+cu111 torchvision===0.9.1+cu111 -f https://download.pytorch.org/whl/torch_stable.html
git clone -b 22.04-dev https://github.com/NVIDIA/apex
cd apex
pip install -v --disable-pip-version-check --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" ./
```
## Data preparation
Please follow the instructions at [DATASETS.md](https://github.com/muzairkhattak/ViFi-CLIP/blob/main/docs/DATASETS.md) to prepare all datasets.
We concatenate the csv files of ETRI and Toyota Smarthome datasets for training the model.
For testing -> we create a csv file with video name and a dummy class label column. 

Before, training or testing the model, please crop the human bounding boxes in the video. Update the input video directory and the output cropped video directory in script_crop.sh.
```
./script_crop.sh
```

**Note:**
- Following the ViFi-CLIP paper, we also recommend keeping the total batch size as mentioned in respective config files. Please use `--accumulation-steps` to maintain the total batch size. Specifically, here the effective total batch size is 8(`GPUs_NUM`) x 4(`TRAIN.BATCH_SIZE`) x 16(`TRAIN.ACCUMULATION_STEPS`) = 512.
- After setting up the dataset, only argument in the config file that should be specified is data path. All other settings in config files are pre-set.


# Training 
For all experiments shown in above tables, we provide config files in `configs` folder. 
```
./script_train.sh 
```

# Evaluating models
To evaluate the trained model on the challenge dataset, please use the correct config (config_challenge_test.yaml) and corresponding model weights (work_dirs/challenge_baseline_new/best.pth).
```
./script_test.sh
```
Make sure to update the val.csv file. It contains the location of the videos and a dummy videos label ('0').
The test scipt will output a file output.csv which is to be used for model evaluation.

## Contact
If you have any questions, please create an issue on this repository.


# Citation
If you use our approach (code, or the model) in your research, please consider citing ViFiCLIP and SKI-Models:
```
@inproceedings{tobeupdated,
    title={ViFi-CLIP Baseline for Elderly Action Recognition (EAR) Challenge},
    author={Srijan Das},
    year={2025}
}
```

# Acknowledgements
Our code is based on [ViFiCLIP's repository](https://github.com/muzairkhattak/ViFi-CLIP) and [SKI-Model's repository](https://github.com/thearkaprava/SKI-Models). We sincerely thank the authors for releasing their code. If you use our model and code, please consider citing ViFiCLIP and SKI-Models as well.
