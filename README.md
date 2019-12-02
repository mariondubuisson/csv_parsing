# Goal
This small project take a CSV file as input, parse it, perform computations and export a new CSV file.

# How to run
**Requirements:**
- Must have python3 installed

**Install dependencies:**
- Run `python3 -m pip install -r requirements.txt` from project root.

**Launch the program:**
- Run `python3 main.py` from project root.

# Tests
Project use `nose` to run the tests. Just do:
- `nosetests` from project root.

# Todo
- [ ] Add function to average and stdev in `lib.compute`
- [ ] Get filename on file upload
- [ ] Parse filename to extract altitude and store it in a variable
- [ ] In the end export a result csv with average and stdev by altitude