import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Setup Chrome driver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

# Open the site
driver.get("https://dhsetransfer.kerala.gov.in/public/sd?type=general&code=")
wait.until(EC.presence_of_element_located((By.ID, "district_selection")))

# Output folder for CSV files
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Get all valid districts (skip placeholder)
district_select = Select(driver.find_element(By.ID, "district_selection"))
district_options = [opt for opt in district_select.options if opt.get_attribute("value")]

# Loop through all districts
for district in district_options:
    district_value = district.get_attribute("value")
    district_name = district.text.strip()
    print(f"\n🔍 Processing District: {district_name}")

    # Set district using JS and trigger change
    driver.execute_script("""
        const select = document.getElementById('district_selection');
        select.value = arguments[0];
        const event = new Event('change', { bubbles: true });
        select.dispatchEvent(event);
    """, district_value)

    time.sleep(2)  # Wait for schools to load

    try:
        wait.until(EC.presence_of_element_located((By.ID, "district_institution")))
        school_select = Select(driver.find_element(By.ID, "district_institution"))
        school_options = [opt for opt in school_select.options if opt.get_attribute("value")]
    except:
        print(f"  [!] No schools found in {district_name}")
        continue

    district_data = []

    # Loop through schools in the district
    for school in school_options:
        school_value = school.get_attribute("value")
        school_name = school.text.strip()
        print(f"  🏫 School: {school_name}")

        # Set school using JS and trigger change
        driver.execute_script("""
            const select = document.getElementById('district_institution');
            select.value = arguments[0];
            const event = new Event('change', { bubbles: true });
            select.dispatchEvent(event);
        """, school_value)

        time.sleep(2)  # Wait for table data to load

        try:
            table_rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
            for row in table_rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) >= 9:
                    district_data.append({
                        "District": district_name,
                        "School": school_name,
                        "Post": cols[1].text.strip(),
                        "Teacher": cols[2].text.strip(),
                        "Teacher ID": cols[3].text.strip(),
                        "Appointment Order Date": cols[4].text.strip(),
                        "Joining Date": cols[5].text.strip(),
                        "Appointment Mode": cols[6].text.strip(),
                        "Posting Status": cols[7].text.strip(),
                        "Remarks": cols[8].text.strip()
                    })
        except Exception as e:
            print(f"    [!] Error scraping school '{school_name}': {e}")

    # Save CSV for this district
    if district_data:
        safe_name = "".join(c for c in district_name if c.isalnum() or c in (' ', '_')).strip().replace(" ", "_")
        filename = os.path.join(output_dir, f"{safe_name}.csv")
        pd.DataFrame(district_data).to_csv(filename, index=False)
        print(f"✅ Saved: {filename}")
    else:
        print(f"⚠️  No data to save for {district_name}")

driver.quit()
print("\n🎉 All done! Check the 'output' folder for district-wise CSVs.")
