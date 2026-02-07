# Research Project Submission App

This is a simple Flask web application that allows users to submit a research project description along with relevant files (e.g., papers, datasets, notes). The long-term goal of this project is to assist researchers not only in managing project materials, but also in identifying relevant funding opportunities by automatically matching project descriptions to external grant programs.

## Features

- Project title and description input
- Multiple file uploads
- Basic file type validation

## Planned Features

- **Grant Matching**
  - Given a research project description and uploaded materials, the system will identify relevant grants that the researcher may be eligible to apply for.
  - Grant recommendations may be based on keywords, research area, eligibility criteria, and funding agency priorities.

## Tech Stack

- Python
- Flask
- HTML / CSS

## Project Structure

WIP

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd project
```
### 2. Create and activate a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```
### 3. Install dependencies
```bash
pip install flask werkzeug
```
### 4. Run the application
```bash
python app.py
```

The app will be available at:

http://127.0.0.1:5000

## Usage

Open the app in your browser

Enter a project title and description

Upload any relevant files

Submit the form

Researchr will automatically search for grants that are available and fit your project!

## Configuration
Allowed file types can be modified in app.py:

ALLOWED_EXTENSIONS = {"pdf", "docx", "csv", "txt"}

## Future Improvements

- Grant discovery and recommendation system
- Database integration for projects and users
- User authentication and authorization
- Improved file management (per-project folders, cloud storage)
- Advanced search and filtering for grants
- Deployment and scalability improvements