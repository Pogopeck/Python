import boto3
import pandas as pd

# Initialize Boto3 session
session = boto3.Session(
    aws_access_key_id='',
    aws_secret_access_key='',
    region_name='us-east-1'
)

textract = session.client('textract')

# Path to your image file
image_path = 'ss_dmo_ocr.png'

# Read the image file
with open(image_path, 'rb') as image_file:
    image_bytes = image_file.read()

# Call Textract to analyze the document and extract the table
response = textract.analyze_document(
    Document={'Bytes': image_bytes},
    FeatureTypes=['TABLES']
)

# Function to extract table data from Textract response
def extract_table_data(blocks):
    cells = {}
    for block in blocks:
        if block['BlockType'] == 'CELL':
            row_index = int(block['RowIndex'])
            col_index = int(block['ColumnIndex'])

            cell_text = ""
            if 'Relationships' in block:
                for rel in block['Relationships']:
                    if rel['Type'] == 'CHILD':
                        for child_id in rel['Ids']:
                            child_block = next((b for b in blocks if b['Id'] == child_id), None)
                            if child_block and child_block['BlockType'] == 'WORD':
                                cell_text += child_block.get('Text', '') + " "

            cell_text = cell_text.strip()
            cells[(row_index, col_index)] = cell_text

    return cells

# Extract table data
table_cells = extract_table_data(response['Blocks'])

# Reconstruct the table
max_row = max(row for row, _ in table_cells.keys())
max_col = max(col for _, col in table_cells.keys())

table_data = []
for row in range(1, max_row + 1):
    row_data = []
    for col in range(1, max_col + 1):
        row_data.append(table_cells.get((row, col), ''))
    table_data.append(row_data)

# Convert to DataFrame
df = pd.DataFrame(table_data[1:], columns=table_data[0])

# Print the DataFrame
print(df)

# Save as CSV
#df.to_csv('output.csv', index=False)

# Save as Excel
df.to_excel('output.xlsx', index=False)
