# Goal
This small project take a CSV file as input, parse it, perform computations and export a new CSV file.
--> Transform DeltaP Pitot measure as wind speed measure

# How to run
**Requirements:**
- Must have python3 installed

**Install dependencies:**
- Run `python3 -m pip install -r requirements.txt` from project root.

**Previous verifications**
- Verify your program parameters (correction and head Pitot coeff., Rho value) in main.py
- be sure the csv separator is a tab or change the separator parameter in line 16 of main.py
- be sure each input csv files name is "U10h" and the altitude of the measure or change it on line 31 of main.py 

**Launch the program:**
- Run `python3 main.py` from project root.

# Tests
Project use `nose` to run the tests. Just do:
- `nosetests` from project root.

# Todo
- [ ] Export the parameters as *.csv fil with the export file

