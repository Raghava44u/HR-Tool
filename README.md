# HR-TOOL

## Overview
This project is an AI-based resume screening system that allows HR professionals to upload resumes and extract relevant information.

**HR Professionals** can upload multiple resumes, filter candidates based on specific criteria (experience, skills, certification, etc.), and download the shortlisted candidates.

## Features
  **Bulk Resume Upload (HR Mode)**:
  - Allows multiple resume uploads at once.
  - Provides filtering based on experience, skills, and certifications.
  - Shortlists candidates and allows downloading the filtered results.
- **Feedback & Job Suggestion System**
  - HR can provide feedback on resumes.
  - HR can suggest jobs for candidates.

## Installation & Requirements
### Prerequisites
Ensure you have the following installed:
- Python 3.12.5
- Flask
- Pandas
- NLTK
- PyPDF2
- Docx2txt
- Sklearn

### Installation Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/Raghava44u/HR-Tool.git
   cd HR-Tool
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the Flask application:
   ```sh
   python app.py
   ```
4. Open your browser and go to:
   ```
   http://127.0.0.1:5000
   ```

## How to Use
1. When you launch the application, it will ask to upload Resumes (**HR**).

2. **HR Mode**:
   - Upload multiple resumes at once.
   - Use the filtering options (skills, experience, certifications, etc.) to shortlist candidates.
   - Download the list of shortlisted candidates.

## Future Enhancements
- Implement AI-based scoring for resumes.
- Add more filtering options for HR professionals.
- Improve UI/UX for better user experience.

## Contribution
Feel free to contribute by creating a pull request or raising an issue.

**@Raghava4u**

