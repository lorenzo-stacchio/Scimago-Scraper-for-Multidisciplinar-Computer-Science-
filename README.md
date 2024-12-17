# Scimago Scraper for Multidisciplinar Journal (with respect To Computer Science)
scraper_scimago


## Main Feature

Given codes a list of scientific fields in Scimago, returns the sorted collection of journal and conference papers that have those jointly. 


## Instructions

To use scimago scraper, please add a novel config file in the ```configs/``` folder. Fill it with one or multiple disciplinary fields.


Please note that, the primary source of search will be computer science, always hard-coded in the main script, that should be runned as pobbile:

This is hard-coded into ```main.py```, in the variable  ```pivot_area_code```.


## Examples

```
python main.py --config <name_config_file>.json
```


An example with macro class ("Earth and Planetary Sciences") is:

```
python main.py --config configs/example_macro.json
```



An example with both macro and micro classes ("Earth and Planetary Sciences" -> "Computers in Earth Sciences") is:

```
python main.py --config configs/example_macro_micro.json
```


An example with both macro and micro classes ("Computer Science" -> "Artificial intelligence") is:

```
python main.py --config configs/example_macro.json --sub_area_computer_science_code 1702
```

Outputs are saved in ```outs/```

## TODOs

- [ ] Make the scaper modular with respect to any tuple of Scimago classifications; 