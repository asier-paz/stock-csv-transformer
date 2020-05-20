# Stock CSV Transformer
This script transforms a CSV with historic price data from Yahoo! Finance into a CSV with retrospective day-to-day change absolute difference.

# Running the script
The script can be executed just as you would execute any other python script.

`
python main.py <file_to_transform> [from_date] [to_date]
`

The script generates a file named `<file_to_transform>_converted.csv`

# Examples
The repository includes a few example origin CSV files to be transformed in the __example-files__ directory.