# Author Name Disambiguation with Document Representation Learning and Knowledge Graph Embeddings

## Prerequisites:
- BLINK entity extractor
- Biggraph pretrained model https://torchbiggraph.readthedocs.io/en/latest/pretrained_embeddings.html

## Hardware
Tested on the following configuration:
- Ubuntu 18.04 and CUDA 10.1
- 64G RAM
- 500G SSD
- 4x GeForce GTX TITAN X

## How to run
- Place RESCS files in /input

```
# set environment in /disambiguation
cd $project_path/disambiguation
export PYTHONPATH="$project_path/disambiguation:$PYTHONPATH"

# convert files from /input to required format
python rescs_to_disambig.py

# extract entities from texts in BLINK, then store their embeddings using
python integrate_entities.py

# preprocess data: required for training and applying the model
python disambiguation/scripts/preprocessing.py

# train global model: save and reuse
python disambiguation/global_/gen_train_data.py
python disambiguation/global_/global_model.py

# local model: document network as input to GAE representation learning
python disambiguation/global_/prepare_local_data.py
python disambiguation/local/gae/train.py
python disambiguation/cluster_size/count.py
```