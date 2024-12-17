# scraper_scimago
scraper_scimago


## Main Feature

Given codes a list of scientific fields in Scimago, returns the sorted collection of journal and conference papers that have those jointly. 


### SCIMAGO PARSER

To use scimago scraper, please add a novel config file in the ```configs/``` folder. Fill it with one or multiple disciplinary fields.


Please note that, the primary source of search will be computer science, always hard-coded in the main script, that should be runned as pobbile:

The config file could also be a empty dict, in that case, only computer science will be scraped. 


```
python main.py --config <name_config_file>.json
```


An example with macro class is:

```
python main.py --config configs/example_macro.json
```



An example with macro and micro class is:

```
python main.py --config configs/example_macro_micro.json
```


An example with sub code artificial intelligence is:

```
python main.py --config configs/example_macro.json --sub_area_computer_science_code 1702
```

Outputs are saved in ```outs/```