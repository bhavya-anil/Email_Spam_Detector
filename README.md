# Email Spam Detector

This is a simple Flask-based web application designed to detect whether an email message is spam or not.

## Features

- Web form for submitting email text
- Spam classification logic (likely using a pre-trained model or keyword matching)
- HTML template for user interface

## Structure

- `app.py`: Main Flask application
- `templates/index.html`: Frontend form and results display

## Setup

1. Ensure you have Python 3 installed.
2. Install dependencies (e.g., Flask) with:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open a browser at `http://127.0.0.1:5000` and use the form to test email text.

## Notes

- This project is for demonstration/learning purposes.
- Customize the detection logic in `app.py` as needed.

## Demo Interface

![Email Spam Detector UI](https://user-images.githubusercontent.com/bhavya-anil/Email_Spam_Detector/main/Demo.png)

The web UI features an **AI-powered analysis** section where users can paste any email content and let the system determine whether it’s spam or not. Buttons are provided to try legitimate, spam, and phishing samples, and a smart reply is generated for non-spam messages. The verdict (e.g. “Spam Detected”) is shown along with reasoning to help users understand the decision.