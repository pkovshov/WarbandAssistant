# Purpose
**Warband Assistant** monitors gameplay in *Mount & Blade: Warband* by capturing the player's screen and extracting key information. 

In the future, it is planned to store this data alongside the game's save files and display it on the screen, effectively extending the in-game interface capabilities.

# Requirements
- **OS:** Linux  
- **Screen Resolution:** 1920x1080  
- **Python version:** 3.10 or higher  
- **Game interface language:** English (en), Russian (ru)

# Features

### Information Extraction
- Recognizes **Title** on the **Dialog Screen** for most character types:
  - Kings, Lords, Ladies, Heroes and Claimants
  - Town, Tavern and Village NPCs
  - Certain Quest Characters 
- Recognizes **Relation** and **Morale** on the **Dialog Screen**  
- Detects **Lord personalities** from the **Dialog Screen** using:
  - Intro dialogs of Lords
  - Private dialogs with Lords
  - Gossip from Villagers or Townspeople
- Recognizes the **in-game Date** on the **Map Screen**

### Supported Datasets
- Map calendars
- Dialog titles
- Dialog bodies
- Dialog relations


# How to run
To run **Warband Assistant**, launch `waraband_assistant.py` script:

```bash
$ waraband_assistant.py
```

## Screenshots bundle
If you want to try **Warband Assistant** without installing *Mount & Blade: Warband*, 
you can download [Screenshots. Mount & Blade: Warband](https://www.kaggle.com/datasets/pkovshov/screenshots-mount-and-blade-warband) from [Kaggle](https://www.kaggle.com).

**Note:** Use a _1920x1080_ screen resolutions and view screenshots in fullscreen mode.

## Command line arguments
All command line arguments are optional.

- **`--monitor`**, **`-m`** — Choose the monitor to capture (if you have more than one).

- **`--player`**, **`-p`** — Set the player name.

- **`-male`**, **`-female`** — Set the player's sex.

- **`-en`**, **`-ru`** — Choose the game interface language. 

If the game interface language is not set, **Warband Assistant** will try to load the value from `~/.mbwarband/language.txt`. If that fails, English (en) will be used as the default.

- `--datasets`, `-ds` — Pull recognized screenshot regions and extracted information into datasets.

You can select datasets by listing their aliases. If no aliases are provided, all datasets will be chosen.

See the **Datasets** section below for instructions on configuring the datasets directory path.

Use the `--help` option to view available dataset aliases.

- **`--help`** — Show help with the available options.

  
# Datasets
You need to set a datasets path for the following purposes:

1. Filling datasets with parser results (use `-ds` option).

2. Running Tox tests.

To set the datasets path, edit the `datasets` option in `path_conf.json`:
```json
{
  "datasets": "/path/to/a/datasets/directory"
}
```
You can use the [Warband Assistant Datasets](https://www.kaggle.com/datasets/pkovshov/warband-assistant-datasets) on [Kaggle](https://www.kaggle.com) to run the Tox tests.

Download and unzip it, then set the path to the extracted `datasets` directory in `path_conf.json`.

# Acknowledgements

Special thanks to [Sergii Karpenko](https://www.linkedin.com/in/sergii-karpenko-3660ba18/) for recommending the use of fuzzy string matching. 

This approach spared us the need to achieve 100% accuracy in optical character recognition.
