# NFC Tag Finder

A comprehensive lost-and-found solution using NFC tags to help reunite lost items with their owners.

## Overview

NFC Tag Finder is a web application that allows users to:

1. **Register NFC tags** with their contact information
2. **Find owners** of lost items by scanning NFC tags
3. **Securely connect** finders with owners without exposing personal information

The system uses pre-authorized NFC tags that, when attached to valuable items, provide a simple way for honest finders to contact the owner when an item is lost.

## How It Works

### For Tag Owners

1. **Purchase an authorized NFC tag** from our system
2. **Register the tag** by scanning it with your smartphone
3. **Enter your contact information** (name, email, phone)
4. **Attach the tag** to your valuable item (keys, laptop, luggage, etc.)

### For Finders

1. **Scan the NFC tag** on a found item using any NFC-enabled smartphone
2. **Submit your contact information** and a message to the owner
3. **The owner will be notified** and can contact you to arrange return

## Features

- **Secure Contact Exchange**: Personal information is never publicly exposed
- **No App Required**: Works with any smartphone that can read NFC tags
- **Pre-authorized Tags**: Only authorized tags can be registered in the system
- **Simple Registration**: Quick and easy process for tag owners
- **Responsive Design**: Works on all devices and screen sizes

## Technical Architecture

The application is built with:

- **Flask**: Python web framework for the backend
- **Firebase/Firestore**: For data storage and retrieval
- **Bootstrap**: For responsive frontend design
- **NFC Technology**: For tag scanning and identification

### Data Collections

- **authorized_tags**: Pre-approved tags that can be registered
- **registered_tags**: Tags that have been claimed by owners
- **notifications**: Finder submissions when someone finds a tag

## Setup and Installation

### Prerequisites

- Python 3.12+
- Pipenv for dependency management
- Firebase account with Firestore database
- Firebase service account credentials

### Environment Setup

1. Clone the repository:
   ```
   git clone <your-repository-url>
   cd nfc-tag-app
   ```

2. Install pipenv if you haven't already:
   ```
   pip install pipenv
   ```

3. Install dependencies:
   ```
   pipenv install
   ```

4. Create a `.env` file in the project root with the following variables:
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   FIREBASE_SERVICE_ACCOUNT_PATH=path/to/your/serviceAccountKey.json
   FIREBASE_DB_ID=your-firebase-db-id
   SECRET_KEY=your-secret-key
   ```

### Running the Application

1. Start the Flask development server:
   ```
   pipenv run flask run
   ```
   
   Or use the provided makefile:
   ```
   make run
   ```

2. Access the application at `http://localhost:5000`

## Admin Tools

The application includes admin tools for managing NFC tags:

### Tag Manager

Located in `admin_tools/tag_manager.py`, this tool allows administrators to:

- Register new authorized tags
- List all authorized tags in the system
- Batch register tags from a file

To use the admin tools:

```
pipenv run python admin_tools/tag_manager.py
```

## Deployment

The application can be deployed to any hosting service that supports Python applications:

1. Set up the required environment variables on your hosting platform
2. Configure your web server (Nginx, Apache, etc.)
3. Use a WSGI server like Gunicorn or uWSGI

## Security Considerations

- All communication between the application and Firebase is secured
- User data is protected and only shared when necessary
- NFC tags are pre-authorized to prevent abuse

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue on this repository.