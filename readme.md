# Audobon to Anki

This is an unofficial web scraper for importing the [Audubon bird guide](https://www.audubon.org/bird-guide) into Anki.

Please do not distribute the images or other content scraped using this script. They are under copywright.

## Usage

__Note:__ For now, the scraper only supports New England birds.

Clone the repository. 

Create a python virtual environment and install the dependencies from requirements.txt.

Run `birds.py` and wait for the script to finish.

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

A command line flag for different regions of birds.