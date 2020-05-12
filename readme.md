# Audobon to Anki

This is an unofficial web scraper for importing the [Audubon bird guide](https://www.audubon.org/bird-guide) into Anki.

Please do not distribute the images or other content scraped using this script. They are under copywright.

## Usage

Clone the repository. 

Create a python virtual environment and install the dependencies from requirements.txt.

To save all birds in the guide, run `birds.py` and wait for the script to finish.

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

## Loading into Anki

When the script finishes, copy all of the files in `output/media` to your anki `collections.media` folder.

Create a new deck and card type, with the following fields:

```
Common Name
Scientific Name
Drawing
Photograph
Call 1 Audio
Call 1 Label
Call 2 Audio
Call 2 Label
...
Call 10 Audio
Call 10 Label
```

Then, open Anki and click `Import File`. Select `output/birds.txt` when prompted for a file. Make sure that you select "allow HTML in fields", or the images will be garbled.

## Roadmap

* Importing multiple photographs