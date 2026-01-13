📦 CAD Inventory Management System
🔹 Overview

The CAD Inventory Management System is a Python-based application that helps manage, store, and search CAD models efficiently.
It is designed to maintain an organized inventory of CAD files and enables users to upload, manage, and analyze CAD models for easy retrieval.

This system is useful for:

Engineering design teams

Manufacturing companies

CAD model databases

Academic research projects

🔹 Features

Upload and store CAD model files

Maintain structured inventory of CAD models

Process CAD files for analysis and comparison

Simple web-based interface

Backend powered by Python

🔹 Project Structure
cad-inventory-management-system/
│
├── app.py              # Web application entry point
├── main.py             # Main execution file
├── requirements.txt   # Python dependencies
├── README.md          # Project documentation
│
├── src/                # Core project logic
├── static/             # CSS, JS, images
├── templates/          # HTML templates
├── uploads/            # Uploaded CAD files (ignored in git)
├── data/               # Processed data (ignored in git)
└── results/            # Output results (ignored in git)

🔹 How the System Works

User uploads CAD model files through the web interface

The system stores files in the upload directory

The backend processes the CAD models

Model data is extracted and stored

The inventory system manages all models

Users can search, view, and compare models

The system can later be extended with:

Shape comparison algorithms

Feature extraction

Similarity search using ML

🔹 Technology Stack

Python

Flask (Web Framework)

HTML, CSS, JavaScript

NumPy, OpenCV (if used for processing)

CAD file parsers

🔹 Environment Setup
1️⃣ Create Virtual Environment
python -m venv venv


Activate:

Windows

venv\Scripts\activate


Linux / Mac

source venv/bin/activate

2️⃣ Install Dependencies
pip install -r requirements.txt

🔹 Run the Application
python app.py


or

python main.py


Then open browser and go to:

http://127.0.0.1:5000

🔹 Future Scope

CAD model similarity search

Feature-based classification

3D visualization

Machine learning based matching

Cloud deployment

🔹 Author

Gowtham Royal
Mechanical Engineer | CAD | Python | ML

GitHub: https://github.com/gowthy18

✅ Conclusion

This project demonstrates a complete workflow for building a CAD inventory system using Python and web technologies.
It is scalable and can be extended into a full CAD model management platform
