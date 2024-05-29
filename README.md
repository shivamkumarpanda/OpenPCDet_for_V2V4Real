# LiDAR-Based Object Detection on Custom Data using OpenPCDet

This repository is an adapted version of the original [OpenPCDet](https://arxiv.org/abs/1812.04244) project. Our enhancements include customized configuration files and utility scripts to enable training on the custom [V2V4Real](https://github.com/ucla-mobility/V2V4Real) dataset using the PV_RCNN model.

## Prerequisites
1. Follow the official [installation guide](https://github.com/open-mmlab/OpenPCDet/blob/master/docs/INSTALL.md) to install OpenPCDet.
2. Go through the [Custom Dataset Tutorial](https://github.com/open-mmlab/OpenPCDet/blob/master/docs/CUSTOM_DATASET_TUTORIAL.md) to understand the steps involved.

## 1. Data Preparation
1. Download the V2V4Real Dataset in the Kitti format. Detailed information about the dataset is available [here](https://mobility-lab.seas.ucla.edu/v2v4real/).

    The `labels_kitti` directory contains object labels and their respective 3D box coordinates. Below is an example:
    ```
    [
    {
        "obj_id": "1",
        "obj_type": "Car",
        "psr": {
            "position": {
                "x": -20.232923334766838,
                "y": -0.010953035456623184,
                "z": -1.1805384281008844
            },
            "rotation": {
                "x": 0,
                "y": 0,
                "z": 0.07853981633974486
            },
            "scale": {
                "x": 3.9799348184967185,
                "y": 2.0622318234681405,
                "z": 1.6980521556897767
            }
        }
    }
    ]
    ```

2. Convert the `.json` annotation files into the `.txt` format required by the model. The format should be as follows:
    ```
    # format: [x y z dx dy dz heading_angle category_name]
    1.50 1.46 0.10 5.12 1.85 4.13 1.56 Vehicle
    5.54 0.57 0.41 1.08 0.74 1.95 1.57 Pedestrian
    ```

    To automate this conversion, run the following script:
    ```
    python myscripts/convert_json_to_txt.py <json_directory>
    ```

3. Divide the dataset into training and validation sets. Create an `ImageSets` directory under `/data/custom`. List the indices of the training data in `train.txt` and the indices of the validation data in `val.txt`.

    After these steps, your directory structure should look like this:
    ```
    OpenPCDet
    ├── data
    │   ├── custom
    │   │   ├── ImageSets
    │   │   │   ├── train.txt
    │   │   │   ├── val.txt
    │   │   ├── points
    │   │   │   ├── 000000.bin
    │   │   │   ├── 999999.bin
    │   │   ├── labels
    │   │   │   ├── 000000.txt
    │   │   │   ├── 999999.txt
    ├── pcdet
    ├── tools
    ```

4. Adjust the configuration file found at `/tools/cfgs/dataset_configs/custom_dataset.yaml`.

* Update the `POINT_CLOUD_RANGE` parameter to define the minimum and maximum values for the x, y, and z dimensions in the format [min_x, min_y, min_z, max_x, max_y, max_z]. You can use known values from the dataset or run the following script after setting the correct path for the LiDAR data files:
    ```
    python myscripts/point_cloud_range.py
    ```

* Set the `CLASS_NAMES` parameter to match the classes in your dataset. The V2V4Real dataset contains five classes, but we use only the `Car` class for training (Day 19, testoutput_CAV_data_2022-03-15-09-54-40_0, tesla).

* Define the `MAP_CLASS_TO_KITTI` parameter to map custom dataset classes to existing KITTI classes.

* (Important) Configure the `VOXEL_SIZE` parameter under `DATA_PROCESSOR / - NAME: transform_points_to_voxels / VOXEL_SIZE`. For PV-RCNN, the point cloud range and voxel size must satisfy these conditions to avoid dimension mismatch in model layers:
    1. The point cloud range along the z-axis divided by the voxel size should be 40.
    2. The point cloud range along the x&y-axis divided by the voxel size should be a multiple of 16.

    The final values for `POINT_CLOUD_RANGE` and `VOXEL_SIZE` are:
    ```
    POINT_CLOUD_RANGE: [-128, -128, -17, 128, 8, 15]
    VOXEL_SIZE: [0.1, 0.1, 0.8]
    ```

5. Generate the custom_info files by executing the following command:
    ```
    python -m pcdet.datasets.custom.custom_dataset create_custom_infos tools/cfgs/dataset_configs/custom_dataset.yaml
    ```

## 2. Training
1. Modify the model configuration file `pv_rcnn.yaml` located at `tools/cfgs/custom_models/pv_rcnn.yaml`.

* Set the path to the dataset configuration file:
    ```
    DATA_CONFIG:
        _BASE_CONFIG_: /path/to/OpenPCDet/tools/cfgs/dataset_configs/custom_dataset.yaml
    ```

* Update the `CLASS_NAMES` parameter:
    ```
    CLASS_NAMES: ['Car']
    ```

2. Execute the `train.py` script. Note that the batch size is set to 1 due to GPU memory limitations:
    ```
    python train.py --cfg_file cfgs/custom_models/pv_rcnn.yaml --batch_size 1
    ```

## 3. Inference
Use the provided `demo.py` script to visualize the inference results. Place the LiDAR files for inference in the `inference_data` directory:
    ```
    python tools/demo.py --cfg_file tools/cfgs/custom_models/pv_rcnn.yaml --data_path inference_data/ --ckpt output/custom_models/pv_rcnn/default/ckpt/checkpoint_epoch_80.pth
    ```

