# UTM converter
Application to convert various formats of coordinates.


## Running the Application
```bash
pip install -r requirements.txt
python main.py
```
This will load the GUI for the desktop application.

## GUI Specification

### Input formats
GUI takes input in csv where each row contains a coordinate in the following format.
The separator for csv can be chosen from the following `',', ';', '\t'`

- Lat-Lon format: `latitude, logitude`
```
51.24,12.41
22.11,54.71
66.53,33.27
```
- UTM format: `easting, northing, zone_number, zone_letter`
```
319213.19,5679701.59,33,U
263761.60,2446780.06,40,Q
511999.49,7379013.32,36,W
```

