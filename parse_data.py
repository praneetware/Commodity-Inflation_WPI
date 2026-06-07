import csv
import json
import re

csv_filename = "239ac3d0-f08d-40d0-b03c-9b7a426a62d5.csv"
html_filename = "india_wpi_dashboard.html"

# 1. Read and parse the CSV items
raw_data = []
with open(csv_filename, mode='r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    
    for row in reader:
        if not row:
            continue
        name = row[0]
        code = row[1]
        try:
            weight = float(row[2])
        except ValueError:
            weight = 0.0
            
        # Extract indices and parse null values accurately
        indices = []
        for val in row[3:]:
            val = val.strip()
            if val == "" or val.lower() == "null" or val == "—":
                indices.append(None)
            else:
                try:
                    indices.append(float(val))
                except ValueError:
                    indices.append(None)
                    
        raw_data.append([name, code, weight, indices])

# 2. Format as a clean JavaScript variable array string
js_array_string = "const RAW = " + json.dumps(raw_data) + ";"

# 3. Inject it back into the HTML file replacing the old stubbed array
with open(html_filename, mode='r', encoding='utf-8') as f:
    html_content = f.read()

# Replace everything from 'const RAW=[' to '];' cleanly using Regex
pattern = r"const RAW\s*=\s*\[.*?(?=\s*// ==========================================|\s*const |\s*function |\s*let |\s*document\.|\s*</script>)"
# Alternatively, replace standard target block safely:
html_content_updated = re.sub(r"const RAW\s*=\s*\[[\s\S]*?\];", js_array_string, html_content)

with open(html_filename, mode='w', encoding='utf-8') as f:
    f.write(html_content_updated)

print("Successfully injected all commodities data directly into your HTML file!")