# Image Classification
```
pip install om_simple
```

## Data Preparation

```
{dataset name}/
├── train/
│   ├── {class1}/
│   ├── {class2}/
│   ├── ...
└── val/
    ├── {class1}/
    ├── {class2}/
    ├── ...
```

## Example Code
```python
from om_simple.img_class import ImageClassification
from om_simple.tools.utils import is_blur


# Simple Classification
X = ImageClassification("epoch019.ckpt")
z = X.predict(images=["sample.jpg"]*1000)


# Blur detection
print (is_blur("sample.jpg"))
```


## Training Simple Image Classification
Simple implementation with everything in a single file ([train.py](./train.py))

Specify the dataset root directory containing the `train` and `val` directories.

```
python train.py -d {dataset name}
```

You can use most of the models in the [timm](https://github.com/rwightman/pytorch-image-models) by specifying `--model-name` directly.

```
usage: train.py [-h] --dataset DATASET [--outdir OUTDIR]
                [--model-name MODEL_NAME] [--img-size IMG_SIZE]
                [--epochs EPOCHS] [--save-interval SAVE_INTERVAL]
                [--batch-size BATCH_SIZE] [--num-workers NUM_WORKERS]
                [--gpu-ids GPU_IDS [GPU_IDS ...] | --n-gpu N_GPU]
                [--seed SEED]

Train classifier.

optional arguments:
  -h, --help            show this help message and exit
  --dataset DATASET, -d DATASET
                        Root directory of dataset
  --outdir OUTDIR, -o OUTDIR
                        Output directory
  --model-name MODEL_NAME, -m MODEL_NAME
                        Model name (timm)
  --img-size IMG_SIZE, -i IMG_SIZE
                        Input size of image
  --epochs EPOCHS, -e EPOCHS
                        Number of training epochs
  --save-interval SAVE_INTERVAL, -s SAVE_INTERVAL
                        Save interval (epoch)
  --batch-size BATCH_SIZE, -b BATCH_SIZE
                        Batch size
  --num-workers NUM_WORKERS, -w NUM_WORKERS
                        Number of workers
  --gpu-ids GPU_IDS [GPU_IDS ...]
                        GPU IDs to use
  --n-gpu N_GPU         Number of GPUs
  --seed SEED           Seed
```

