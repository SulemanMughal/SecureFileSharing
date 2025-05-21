# SecureFileSharing

A secure file sharing application built with Django and Python, designed to provide a platform for users to upload, encrypt, and share files safely.

## Objectives

* **Secure File Upload**: Allow users to upload files securely.
* **File Encryption**: Encrypt files before storing them to ensure data privacy.
* **Access Control**: Implement user authentication and authorization to control access to files.
* **User-Friendly Interface**: Provide an intuitive interface for users to interact with the application.([GitHub][1])

## Technologies Used

* **Frontend**:

  * ![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5\&logoColor=white) **HTML5**: For structuring the web pages.
  * ![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3\&logoColor=white) **CSS3**: For styling the web pages.
  * ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript\&logoColor=black) **JavaScript**: For adding interactivity to the web pages.

* **Backend**:

  * ![Python](https://img.shields.io/badge/Python-3776AB?logo=python\&logoColor=white) **Python**: For server-side scripting.
  * ![Django](https://img.shields.io/badge/Django-092D1F?logo=django\&logoColor=white) **Django**: A high-level Python web framework for rapid development.

* **Database**:

  * ![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite\&logoColor=white) **SQLite**: A lightweight database engine for storing application data.

* **File Encryption**:

  * **Cryptography Library**: For encrypting and decrypting files.([GitHub][2])

## Features

* **User Authentication**: Users can register, log in, and manage their profiles.
* **File Upload**: Users can upload files securely.
* **File Encryption**: Uploaded files are encrypted before storage.
* **File Sharing**: Users can share encrypted files with others.
* **Access Control**: Only authorized users can access certain files.
* **Responsive Design**: The application is responsive and works well on both desktop and mobile devices.([GitHub][1])

## Applications

This application is ideal for:

* **Individuals**: Looking to securely share personal files.
* **Businesses**: Needing a platform to share sensitive documents securely.
* **Developers**: Interested in learning about file encryption and secure file sharing.([The JetBrains Blog][3])

## Future Enhancements

To further enhance this project, consider implementing the following features:

* **Multi-File Upload**: Allow users to upload multiple files at once.
* **File Versioning**: Keep track of different versions of files.
* **File Expiry**: Set expiration dates for shared files.
* **Admin Panel**: Implement an admin panel for managing users and files.
* **Two-Factor Authentication**: Enhance security by requiring a second form of authentication.([GitHub][1], [GitHub][4])

## Installation

To set up the project on your local machine, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/SulemanMughal/SecureFileSharing.git
   cd SecureFileSharing
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**:

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**:

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

7. **Access the application**:
   Open a browser and go to `http://localhost:8000/`.

## Contributing

Contributions are welcome! If you would like to contribute to this project, feel free to fork the repository, make your changes, and submit a pull request.
