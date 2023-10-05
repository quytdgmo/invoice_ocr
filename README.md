# Invoice Parsing using Document AI and ChatGPT

This repository demonstrates how to parse invoices using Google's Document AI and generate responses using ChatGPT. Follow the steps below to set up and run the application.

## Prerequisites

- Python 3.x installed on your system
- Google Cloud Project with Document AI API enabled
- ChatGPT API key
- Google Cloud Credentials JSON file

## Getting Started

### 1. Create Python Virtual Environment

```bash
python3 -m venv invoice_ocr
source invoice_ocr/bin/activate
```
### 2. Install Packages
Install the required packages using pip:
```bash
pip install -r requirements.txt
```
### 3. Update .env File
Create a .env file in the project directory and add the following information:

```env
PROJECT_ID=
PROCESSOR_LOCATION=
PROCESSOR_ID=
PROCESS_VERSION=
OPENAI_API_KEY=YOUR_CHATGPT_API_KEY
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/credentials.json
```
Replace PROJECT_ID, PROCESSOR_ID, PROCESSOR_LOCATION, PROCESS_VERSION with your Google Document AI Form Parser Processor information and OPENAI_API_KEY with your ChatGPT API key. Set the GOOGLE_APPLICATION_CREDENTIALS to the path of your Google Cloud Credentials JSON file.

### 4. Run the Application
Run the following command to start the application:

```bash
python app.py
```

This will start the application and allow you to parse invoices using Document AI and generate responses using ChatGPT.
Feel free to customize the application further as per your requirements.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
