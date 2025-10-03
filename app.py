import os
import io
import re
import pytesseract
from flask import Flask, request, jsonify, render_template
from PIL import Image
from datetime import date

# --- Flask and Configuration Setup ---
app = Flask(__name__)
# The folder where uploaded files will be temporarily stored
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Define allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# --- Core Hackathon Logic: Structured Data Simulation ---

def get_mock_attendance_data(raw_text):
    """
    Mocks the result of complex CV/OCR, providing structured data 
    and implementing the Anomaly Detection logic required by PS-1.
    
    In a real application, this logic would use Computer Vision to find 
    table cells and extract these fields accurately. We are simulating 
    a reliable extraction process for the demo.
    """
    # 1. Define the student roster and expected attendance data
    # NOTE: You can change these names/numbers to match your college's data.
    MOCK_ROSTER = [
        ("2301", "Priya Sharma"),
        ("2302", "Rohit Patil"),
        ("2303", "Anjali Mehta"),
        ("2304", "Vikram Singh"),
        ("2305", "Sneha Kadam"),
        ("2306", "Kunal Desai"),
        ("2307", "Rani Iyer"),
    ]

    extracted_records = []
    anomaly_count = 0
    
    # Simulate a pattern that determines status and flags anomalies
    for roll_no, name in MOCK_ROSTER:
        # Check if the student's name is in the raw OCR text (simple presence simulation)
        is_present_in_ocr = re.search(re.escape(name.split()[-1]), raw_text, re.IGNORECASE)
        
        status = "Absent"
        anomaly = False
        notes = "No signature detected."

        if is_present_in_ocr:
            # If student name is found, simulate attendance status
            
            # --- ANOMALY DETECTION LOGIC (PS-1 Objective) ---
            
            # A. Anomaly 1: Suspicious Signature Mark (e.g., single letter 'X' or common dot)
            # This logic assumes finding a suspicious mark means the detected signature is suspect.
            if re.search(r'\b(X|x|\.)\b', raw_text): 
                status = "Proxy?"
                anomaly = True
                notes = "Suspicious mark detected; requires manual signature comparison."
            
            # B. Anomaly 2: Duplicate Entry Simulation (2306 signature detected twice)
            # This simulates detecting the same name/signature in multiple places.
            elif roll_no == "2306" and raw_text.count("Desai") > 1:
                status = "Signed"
                anomaly = True
                notes = "Duplicate signature/entry detected on sheet."
            
            # C. Clean Entry
            else:
                status = "Present"
                notes = "Signature/mark detected and validated."

        if anomaly:
            anomaly_count += 1
            
        extracted_records.append({
            "roll_no": roll_no,
            "name": name,
            "status": status,
            "anomaly_flag": anomaly,
            "notes": notes
        })

    # 2. Compile Summary Metrics
    total_students = len(MOCK_ROSTER)
    present_count = len([d for d in extracted_records if d['status'] == 'Present' or d['status'] == 'Signed'])
    
    summary = {
        "subject": "CS 405 - Computer Vision",
        "date": date.today().strftime("%Y-%m-%d"),
        "total_students": total_students,
        "present": present_count,
        "anomalies_flagged": anomaly_count
    }

    return extracted_records, summary


# --- Utility Functions ---

def allowed_file(filename):
    """Checks if a file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_file_and_get_ocr(image_file):
    """Handles the Tesseract/Pillow integration."""
    try:
        img = Image.open(image_file)
        # Use Page Segmentation Mode 6 (Assume a single uniform block of text)
        raw_text = pytesseract.image_to_string(img, lang='eng', config='--psm 6')
        return raw_text
    except pytesseract.TesseractNotFoundError:
        # Essential error handling for Tesseract dependency
        raise EnvironmentError("Tesseract OCR Engine Not Found. Please check installation steps in the README.")
    except Exception as e:
        raise RuntimeError(f"An error occurred during OCR: {e}")

# --- Routes ---

@app.route('/')
def index():
    """Renders the single-page HTML frontend."""
    # Renders the HTML file you saved as basic.html inside the 'templates' folder.
    return render_template('basic.html') 

@app.route('/upload', methods=['POST'])
def upload_file():
    """API endpoint to receive and process the uploaded attendance sheet."""
    
    # 1. Basic File Checks
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed. Only PNG, JPG, JPEG are accepted.'}), 400

    try:
        # 2. OCR Processing
        # Read file into memory stream for processing
        file_stream = io.BytesIO(file.read())
        raw_ocr = process_file_and_get_ocr(file_stream)

        # 3. Structured Data Extraction and Anomaly Flagging (Hackathon Logic)
        extracted_records, summary = get_mock_attendance_data(raw_ocr)

        # 4. Return the structured results
        return jsonify({
            'message': 'Structured extraction and anomaly check simulated successfully!',
            'filename': file.filename,
            'summary': summary, 
            'extracted_data': extracted_records,
            'raw_ocr_output': raw_ocr,
        }), 200
        
    except EnvironmentError as ee:
        # Catch Tesseract missing error
        return jsonify({
            'error': str(ee),
            'extracted_data': [{"roll_no": "ERROR", "name": "System Error", "status": "FAILED", "anomaly_flag": True, "notes": "Tesseract Missing. See README."}],
            'summary': {"anomalies_flagged": 100}
        }), 500
    except RuntimeError as re:
        # Catch general OCR processing errors
        return jsonify({
            'error': str(re),
            'extracted_data': [{"roll_no": "ERROR", "name": "System Error", "status": "FAILED", "anomaly_flag": True, "notes": "OCR Failed."}],
            'summary': {"anomalies_flagged": 100}
        }), 500
    except Exception as e:
        # Catch all other unexpected errors
        return jsonify({'error': f"An unexpected error occurred: {str(e)}"}), 500

# --- Server Execution ---
if __name__ == '__main__':
    app.run(debug=True)
