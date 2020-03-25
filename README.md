# Goal
This small project take a CSV file as input, parse it, perform computations and export a new CSV file.
--> Correct measures
--> Transform DeltaP Pitot measure as wind speed measure
--> Calculate Intensity and Pdyn ratio

You can use different models of data entries, and make specific computes
For now, you can choose :
--> pitot_measure for gradient measures, and calculate a speed gradient
--> wind_measure for test measurements, and calculate corrected or adjusted mean speed measurements

# How to run
**Requirements:**
- Must have python3 installed

**Install dependencies:**
- Run `python3 -m pip install -r requirements.txt` from project root.

**Previous verifications**
- Verify your program parameters (corrections on DeltaP mesures, head Pitot coeff. and Rho values) in main.py
- Indicate the place of your *.mat file if necessary
- Modify the prefix and extension file
- be sure the csv separator is a tab or change the separator parameter in CSVparser function in main.py
- You can choose to apply a real Rho value or a standard Rho value, check wich one is selected in tranformation_pipeline function in main.py
- Check the format of measures is conform with the model used in models > pitot_measure for example, or follow the instructions

**Launch the program:**
- Run `python3 main.py` from project root.
- Select all you data files
- Save the output file

# Tests
Project use `nose` to run the tests. Just do:
- `nosetests` from project root.

# Todo
- [ ]

