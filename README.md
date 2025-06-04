# Million clandestine gravesites over southeastern China’s land surfaces revealed by satellite images

## System Requirements
To run this project, please ensure you have the necessary dependencies installed. All required packages and their versions are specified in the requirements.txt file.

You can install them using:
```
pip install -r requirements.txt
```

## Installation Guide
Follow the steps below to set up the project environment and get started:
#### Clone the repository:
```
git clone https://github.com/geospatialgroup/grave.git
cd grave
```
#### Create a virtual environment (optional):
```
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```
#### Install the required dependencies:
```
pip install -r requirements.txt
```
### Installation Time
The installation process usually takes around 5 to 15 minutes, depending on your internet speed and system performance. This includes downloading dependencies listed in requirements.txt and setting up the environment.

For GPU-enabled systems, installation of CUDA and related drivers may add extra time if not already installed.

## Demo and Instructions for Use
### 🔧 Training Options

#### Essential Parameters
| Parameter          | Description                          | Default     |
|--------------------|--------------------------------------|-------------|
| `--data`           | Dataset config file                  | coco.yaml   |
| `--cfg`            | Model configuration file             | yolo.yaml   |
| `--weights`        | Pretrained weights path              | ''          |
| `--epochs`         | Number of training epochs            | 100         |
| `--batch-size`     | Total batch size                     | 16          |
| `--imgsz`          | Input image size                     | 640         |
| `--device`         | Training device (cpu/cuda)           | '' (auto)   |
| `--workers`        | Data loading workers                 | 8           |

#### Advanced Options
| Parameter          | Description                          |
|--------------------|--------------------------------------|
| `--resume`         | Resume from last.pt                  |
| `--optimizer`      | Optimizer (SGD/Adam/AdamW/LION)      |
| `--cos-lr`         | Use cosine LR scheduler              |
| `--label-smoothing`| Label smoothing epsilon              |
| `--freeze`         | Freeze layers (e.g., --freeze 10)    |
| `--sync-bn`        | Use SyncBatchNorm (DDP mode)         |
| `--multi-scale`    | Vary image sizes (+/- 50%)           |

#### ⚙️ Hyperparameter Configuration

Default hyperparameters are in `data/hyps/hyp.scratch-high.yaml`. Key parameters:

```yaml
# Optimizer
lr0: 0.01       # Initial learning rate
lrf: 0.01       # Final learning rate (lr0 * lrf)
momentum: 0.937 # SGD momentum/Adam beta1
weight_decay: 0.0005  # Optimizer weight decay

# Loss
box: 0.05       # Box loss gain
cls: 0.5        # Class loss gain
obj: 1.0        # Object loss gain

# Augmentation
hsv_h: 0.015    # Image HSV-Hue augmentation
hsv_s: 0.7      # Image HSV-Saturation augmentation
hsv_v: 0.4      # Image HSV-Value augmentation
degrees: 0.0    # Image rotation (+/- deg)
```

### 🔄 Multi-GPU Training

#### Data Parallel (DP)
```bash
python train.py --device 0,1  # Uses 2 GPUs
```

#### Distributed Data Parallel (DDP)
```bash
python -m torch.distributed.run --nproc_per_node 2 train.py --device 0,1
```

#### 🧪 Hyperparameter Evolution

To evolve hyperparameters for 300 generations:
```bash
python train.py --evolve 300
```

This will:
1. Create `evolve.csv` with optimization results
2. Generate `hyp_evolve.yaml` with optimized parameters
3. Create evolution plots

#### 💾 Model Saving

Checkpoints are saved to `runs/train/exp/weights/`:
- `best.pt`: Best model (highest mAP)
- `last.pt`: Last model
- `epoch*.pt`: Periodic saves (if `--save-period` > 0)

### Prediction

#### Basic Detection
```bash
python detect.py --weights runs/train/yolov9-e3/weights/best.pt --source data/images --img-size 512
```

#### Webcam Detection
```bash
python detect.py --source 0 --view-img
```

#### 🛠 Usage

##### Basic Commands
| Command | Description |
|---------|-------------|
| `--weights` | Path to model weights |
| `--source` | Input source (file/dir/URL/webcam) |
| `--img-size` | Inference size (default: 512) |
| `--conf-thres` | Confidence threshold (default: 0.53) |
| `--view-img` | Display results |
| `--save-txt` | Save results as text files |

#### Examples

***Detect images in a folder:***
```bash
python detect.py --source data/images --weights best.pt
```

***Real-time webcam detection:***
```bash
python detect.py --source 0 --view-img --weights best.pt
```

***Video detection with custom confidence:***
```bash
python detect.py --source input.mp4 --conf-thres 0.6 --weights best.pt
```

#### ⚙ Configuration

Modify `data.yaml` to configure:
- Class names
- Dataset paths
- Training parameters

#### 📊 Results

Results are saved to `runs/detect/exp` by default, containing:
- Annotated images/videos
- Text files with detection coordinates
- Cropped objects (if enabled)

### Verification

#### Basic Validation
```bash
python val.py --weights yolov9.pt --data coco.yaml --batch-size 32 --device 0
```

#### Speed Benchmark
```bash
python val.py --task speed --data coco.yaml --weights yolov9.pt --batch-size 1
```

#### 🛠 Basic Usage

##### Command Structure
```bash
python val.py --weights [MODEL_PATH] --data [DATASET_YAML] --batch-size [BATCH_SIZE] --device [DEVICE]
```

#### Common Examples

***Validate on COCO dataset:***
```bash
python val.py --weights yolov9.pt --data data/coco.yaml --img 640 --batch 32
```

***Test model speed:***
```bash
python val.py --task speed --data data/coco.yaml --weights yolov9.pt --img 640 --batch 1
```

***Validate with custom dataset:***
```bash
python val.py --weights best.pt --data data/custom.yaml --img 512
```

### ⚙ Advanced Options

#### Key Parameters
| Parameter | Default | Description |
|-----------|---------|-------------|
| `--weights` | `yolo.pt` | Model weights path |
| `--data` | `data/coco.yaml` | Dataset configuration file |
| `--batch-size` | 32 | Validation batch size |
| `--imgsz` | 640 | Inference size (pixels) |
| `--conf-thres` | 0.001 | Confidence threshold |
| `--iou-thres` | 0.7 | NMS IoU threshold |
| `--task` | `val` | Task to run (val/test/speed/study) |
| `--device` | `cpu` | Device to use (cpu or 0,1,2,3) |
| `--save-json` | False | Save COCO-JSON results |
| `--save-txt` | False | Save results as TXT files |

#### Full Configuration Example
```bash
python val.py \
    --weights runs/train/exp/weights/best.pt \
    --data data/custom.yaml \
    --batch-size 16 \
    --imgsz 512 \
    --conf-thres 0.01 \
    --iou-thres 0.6 \
    --device 0 \
    --save-txt \
    --save-json \
    --name custom_val
```

#### 📊 Output Interpretation

Results are saved to `runs/val/exp` by default and include:

1. **Metrics Output**:
   ```
   Class      Images  Instances      P      R   mAP50  mAP50-95
   all         5000      36380   0.55   0.49    0.51      0.35
   person      5000       4692   0.61   0.55    0.58      0.41
   car         5000       4372   0.72   0.63    0.67      0.48
   ```

2. **Output Files**:
   - `labels/`: Per-image detection results (TXT format)
   - `val_batchX_pred.jpg`: Sample detection visualizations
   - `confusion_matrix.png`: Classification performance
   - `predictions.json`: COCO-format results (if enabled)

3. **Speed Metrics**:
   ```
   Speed: 2.1ms pre-process, 5.3ms inference, 1.2ms NMS per image at shape (32, 3, 640, 640)
   ```



