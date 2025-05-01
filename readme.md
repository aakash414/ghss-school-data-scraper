# Kerala DHSE Transfer Data Scraper

This Python script automates the process of scraping teacher transfer data from the official [DHSE Kerala Transfer Portal](https://dhsetransfer.kerala.gov.in/public/sd?type=general&code=) using Selenium. The data is collected district-wise and school-wise, and saved as individual CSV files.

## Features

- Automatically selects each district and its associated schools.
- Extracts teacher transfer details including:
  - Post
  - Teacher Name and ID
  - Appointment Order Date and Joining Date
  - Appointment Mode, Posting Status, Remarks
- Saves clean, well-structured CSV files for each district.

## Requirements

- Python 3.7 or higher
- Google Chrome installed
- ChromeDriver (must match your installed Chrome version)

### Python Packages

Install the required packages using pip:

```bash
pip install selenium pandas
```

## Usage

1. Clone this repository or download the script.
2. Ensure ChromeDriver is in your system PATH or placed in the working directory.
3. Run the script:

```bash
python dhseSchools.py
```

4. The script will:
   - Open the DHSE transfer website
   - Iterate through all available districts and schools
   - Scrape teacher transfer data
   - Save one CSV file per district in the `output/` directory

## Output Structure

Each district gets a separate `.csv` file saved in the `output/` folder:

```
output/
├── Alappuzha.csv
├── Ernakulam.csv
├── Kozhikode.csv
└── ...
```

### CSV Columns

- District
- School
- Post
- Teacher
- Teacher ID
- Appointment Order Date
- Joining Date
- Appointment Mode
- Posting Status
- Remarks

## Notes

- The script uses JavaScript event dispatching to handle dropdown selections because the website uses `chosen.js`.
- There is a 2-second delay between each dropdown selection to ensure the page updates correctly.
- If a district has no schools or a school has no data, the script will skip it and print a message.

## License

This project is provided for educational and non-commercial use. Please ensure your use complies with the site's terms of service.

```

```
