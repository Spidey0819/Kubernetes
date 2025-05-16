from flask import Flask, request, jsonify
import os
import csv
import io
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PERSISTENT_STORAGE_PATH = '/dhruv_PV_dir'

def clean_key(key):
    return key.strip().strip('\'"')

@app.route('/sum', methods=['POST'])
def calculate_sum():
    input_data = request.get_json()

    if not input_data or 'file' not in input_data or 'product' not in input_data:
        return jsonify({
            "file": None,
            "error": "Invalid JSON input."
        })

    file_name = input_data.get('file')
    product_details = input_data.get('product')

    file_path = os.path.join(PERSISTENT_STORAGE_PATH, file_name)

    product_sum = 0
    csv_format_valid = True
    products_array = []

    try:
        with open(file_path, 'r') as csvfile:

            csv_reader = csv.DictReader(csvfile)

            fieldnames = [clean_key(fieldname) for fieldname in csv_reader.fieldnames]

            if 'product' not in fieldnames or 'amount' not in fieldnames:
                return jsonify({
                    "file": file_name,
                    "error": "Input file not in CSV format."
                })

            for row in csv_reader:
                cleaned_row = {}
                for key, value in row.items():
                    cleaned_row[clean_key(key)] = value.strip()

                if 'product' not in cleaned_row or 'amount' not in cleaned_row:
                    csv_format_valid = False
                    break

                products_array.append(cleaned_row)

                if cleaned_row.get('product') == product_details:
                    try:
                        product_sum += int(cleaned_row.get('amount', 0))
                    except ValueError:
                        csv_format_valid = False
                        break

        if not csv_format_valid or len(products_array) == 0:
            return jsonify({
                "file": file_name,
                "error": "Input file not in CSV format."
            })

        return jsonify({
            "file": file_name,
            "sum": product_sum
        })

    except FileNotFoundError:
        return jsonify({
            "file": file_name,
            "error": "File not found."
        })
    except Exception as e:
        logger.error(f"Error processing the request: {str(e)}")
        return jsonify({
            "file": file_name,
            "error": "Error processing the request."
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6002, debug=False)
