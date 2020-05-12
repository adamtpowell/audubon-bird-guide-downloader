# Audubon Bird Guide Downloader

This is an unofficial web scraper for downloading files from the [Audubon bird guide](https://www.audubon.org/bird-guide). It also supplies a file for import into Anki.

Please do not distribute the images or other content scraped using this script.

## Why?

If you want a lot of photos and illustrations of birds for personal purposes, if you want bird recordings for personal purposes, or you want to learn about birds with Anki or other software.

## Usage

Clone the repository.

Create a python virtual environment and install the dependencies from `requirements.txt`:

```bash
python3 -m venv .venv # Use your preferred python3
source ./.venv/bin/activate # The command may vary based on your OS and shell
python -m pip install -r requirements.txt # Now you can just use python since you are in the venv
```

If there are no errors when installing the dependencies, you can now run the script.

To save all birds in the guide:

```bash
python birds.py
```

If you want only birds from a given region, use one of the following:

```bash
python birds.py "alaska and the north"
python birds.py "california"
python birds.py "eastern-canada"
python birds.py "florida"
python birds.py "great-lakes"
python birds.py "mid-atlantic"
python birds.py "new-england"
python birds.py "northwest"
python birds.py "plains"
python birds.py "rocky-mountains"
python birds.py "southeast"
python birds.py "southwest"
python birds.py "texas"
python birds.py "western-canada"
```

The script saves media into `output/media` and an Anki compatible tab-seperated file into `output/birds`.

## Loading into Anki

When the script finishes, copy all of the files in `output/media` to your anki `collections.media` folder.

Create a new deck and card type, with the following fields:

```
Common Name
Scientific Name
Drawing
Photograph 1
Photograph 2
...
Photograph 9
Photograph 10
Call 1 Audio
Call 1 Label
Call 2 Audio
Call 2 Label
...
Call 10 Audio
Call 10 Label
```

Then, open Anki and click `Import File`. Select `output/birds.txt` when prompted for a file. Make sure that you select "allow HTML in fields", or the images will not import.