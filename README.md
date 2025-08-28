# Purpose
**WarbandAssistant** monitors the gameplay of *Mount & Blade: Warband* by capturing the player's screen and extracting key information. The project stores this data alongside the game save files and can display it on the game screen, effectively extending the in-game interface capabilities.

# Requirements
- **OS:** Linux  
- **Screen Resolution:** 1920x1080  
- **Python version:** 3.10 or higher  

# How to run
Launch the assistant script:

```bash
$ waraband_assistant.py
```
Use the `--help` option to view available CLI commands:
```
$ waraband_assistant.py --help
```
# Features

## Recognized Information
- Recognizes **Title** on the **Dialog Screen**
- Recognizes **Relation** and **Morale** on the **Dialog Screen**  
- Detects **Lord personalities** based on **Dialog Screen** with:
  - Intro dialogs of Lords
  - Private dialogs with Lords
  - Gossip from villagers or townspeople
- Recognizes the **in-game Date** on the **Map Screen**
  
# Datasets
You need to set a datasets path for the following purposes:

1. Filling datasets with parser results (use `-ds` option).

2. Running Tox tests.

To set the datasets path, edit the datasets option in `path_conf.json`:
```json
{
  "datasets": "/path/to/a/datasets/directory"
}
```
You can use the [Warband Assistant Datasets](https://www.kaggle.com/datasets/pkovshov/warband-assistant-datasets) on [Kaggle](https://www.kaggle.com) to test that OCR works correctly.

Download and unzip it, then set the path to the datasets directory in path_conf.json.
