from flask import Flask, request, redirect, url_for, render_template
import qrcode
import os
import re

app = Flask(__name__)

# Set the directory to save the QR codes
QR_CODE_DIR = os.path.join('static', 'qr_codes')
if not os.path.exists(QR_CODE_DIR):
    os.makedirs(QR_CODE_DIR)  # Create the directory if it doesn't exist

@app.route('/')
def index():
    # Render the main page
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    data = request.form['data']  # Get the data from the form
    print(f"Received data: {data}")  # Debugging print

    # Generate the QR code
    qr_img = qrcode.make(data)

    # Sanitize the data for a safe filename
    # Replace characters that are invalid in filenames
    safe_data = re.sub(r'[<>:"/\\|?*]', '_', data)  # Replace invalid characters with underscores
    safe_data = re.sub(r'\s+', '_', safe_data)  # Replace spaces with underscores
    file_name = f"qr_{safe_data}.png"  # Create a safe filename
    file_path = os.path.join(QR_CODE_DIR, file_name)

    try:
        # Save the QR code image to the specified file path
        qr_img.save(file_path)
        print(f"QR code saved at: {file_path}")  # Debugging print
    except Exception as e:
        print(f"Error saving QR code: {e}")  # Print any error messages
        return "Error saving QR code.", 500  # Return a server error response

    # Redirect to index with the QR code filename
    return render_template('index.html', qr_code=file_name)

@app.route('/qr_image/<filename>')
def qr_image(filename):
    # Serve the saved QR code image
    return redirect(url_for('static', filename=f'qr_codes/{filename}'))

if __name__ == '__main__':
    app.run(debug=True)
