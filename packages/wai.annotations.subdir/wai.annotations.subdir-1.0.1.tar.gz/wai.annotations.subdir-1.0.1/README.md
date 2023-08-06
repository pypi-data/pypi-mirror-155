# wai-annotations-subdir
wai.annotations module for managing image classification annotations with sub-directories corresponding to labels.

The manual is available here:

https://ufdl.cms.waikato.ac.nz/wai-annotations-manual/

## Plugins

### FROM-SUBDIR-AC
Reads audio files from sub-directories named after their class labels.

#### Domain(s):
- **Audio classification domain**

#### Options:
```
usage: from-subdir-ac [-I FILENAME] [-i FILENAME] [-N FILENAME] [-n FILENAME] [-o FILENAME]
                      [--seed SEED]

optional arguments:
  -I FILENAME, --inputs-file FILENAME
                        Files containing lists of input files (can use glob syntax) (default: [])
  -i FILENAME, --input FILENAME
                        Input files (can use glob syntax) (default: [])
  -N FILENAME, --negatives-file FILENAME
                        Files containing lists of negative files (can use glob syntax) (default: [])
  -n FILENAME, --negative FILENAME
                        Files that have no annotations (can use glob syntax) (default: [])
  -o FILENAME, --output-file FILENAME
                        optional file to write read filenames into (default: None)
  --seed SEED           the seed to use for randomisation (default: None)
```


### FROM-SUBDIR-IC
Reads images from sub-directories named after their class labels.

#### Domain(s):
- **Image Classification Domain**

#### Options:
```
usage: from-subdir-ic [-I FILENAME] [-i FILENAME] [-N FILENAME] [-n FILENAME] [-o FILENAME]
                      [--seed SEED]

optional arguments:
  -I FILENAME, --inputs-file FILENAME
                        Files containing lists of input files (can use glob syntax) (default: [])
  -i FILENAME, --input FILENAME
                        Input files (can use glob syntax) (default: [])
  -N FILENAME, --negatives-file FILENAME
                        Files containing lists of negative files (can use glob syntax) (default: [])
  -n FILENAME, --negative FILENAME
                        Files that have no annotations (can use glob syntax) (default: [])
  -o FILENAME, --output-file FILENAME
                        optional file to write read filenames into (default: None)
  --seed SEED           the seed to use for randomisation (default: None)
```


### TO-SUBDIR-AC
Writes audio files to sub-directories named after their class labels.

#### Domain(s):
- **Audio classification domain**

#### Options:
```
usage: to-subdir-ac -o PATH [--split-names SPLIT NAME [SPLIT NAME ...]]
                    [--split-ratios RATIO [RATIO ...]]

optional arguments:
  -o PATH, --output PATH
                        the directory to store the class directories in (default: None)
  --split-names SPLIT NAME [SPLIT NAME ...]
                        the names to use for the splits (default: [])
  --split-ratios RATIO [RATIO ...]
                        the ratios to use for the splits (default: [])
```


### TO-SUBDIR-IC
Writes images to sub-directories named after their class labels.

#### Domain(s):
- **Image Classification Domain**

#### Options:
```
usage: to-subdir-ic -o PATH [--split-names SPLIT NAME [SPLIT NAME ...]]
                    [--split-ratios RATIO [RATIO ...]]

optional arguments:
  -o PATH, --output PATH
                        the directory to store the class directories in (default: None)
  --split-names SPLIT NAME [SPLIT NAME ...]
                        the names to use for the splits (default: [])
  --split-ratios RATIO [RATIO ...]
                        the ratios to use for the splits (default: [])
```
