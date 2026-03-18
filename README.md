# Aquatic Microplastic Detector

A field-deployable imaging system for detecting and classifying microplastics in aquatic environments using advanced AI and computer vision technology.

## Overview

This project implements a Django-based web application that leverages YOLOv8 deep learning models to automatically detect and classify microplastics in water samples. The system is designed for easy deployment in the field and provides real-time detection with multiple image processing visualizations.

## Team
----------------------------------
| Name           | Roll Number   |
|----------------|---------------|
| Muffasir Mehdi | 160922748038  |
| Mohd. Fazal    | 160922748051  |
| Shaik Arif     | 160922748003  |
| Mohd. Najmee   | 160922748035  |
----------------------------------
Project Guide : 
Co-Guide / HoD : Dr. Abdul Rasool MD, Associate Professor & Head of Department CSE(AIML)
Institute: Lords Institute of Engineering and Techno

## Features

- **Real-time Microplastic Detection**: YOLOv8 model-based detection with high accuracy
- **Microplastic Classification**: Identifies four types of microplastics:
  - Fibers
  - Films
  - Fragments
  - Pellets
- **Multiple Image Processing Outputs**:
  - Detection visualization with bounding boxes
  - Hologram image (cool colormap overlay)
  - Reconstruction image (enhanced contrast and sharpness)
  - Segmentation visualization (pseudo-color)
- **User Management System**: User registration and authentication
- **Admin Dashboard**: View and manage registered users
- **Web-based Interface**: Easy-to-use Django web application

## Technical Stack

- **Framework**: Django 4.2
- **Deep Learning**: YOLOv8 (ultralytics 8.4.21)
- **Machine Learning**: PyTorch 2.10.0, TorchVision 0.25.0
- **Image Processing**: OpenCV 4.13.0.92, Pillow 12.1.1
- **Numerical Computing**: NumPy 2.4.3
- **Database**: SQLite (default Django database)
- **Python Version**: 3.10+

## Installation

### Prerequisites

- Python 3.10 or higher
- Git
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone https://github.com/MUFFASIR289/Aquatic-Microplastic-Detector.git
cd Aquatic-Microplastic-Detector
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment

**On Windows:**
```bash
.\venv\Scripts\Activate.ps1
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install Django==4.2 ultralytics torch torchvision opencv-python numpy pillow requests PyYAML
```

Or use the requirements file if available:
```bash
pip install -r requirements.txt
```

### Step 5: Apply Database Migrations

```bash
python manage.py migrate
```

### Step 6: Run the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000/`

## Usage

### Admin Dashboard

1. Navigate to `http://localhost:8000/AdminLogin`
2. Default credentials:
   - Username: `admin`
   - Password: `admin`
3. View and manage registered users

### User Registration

1. Go to `http://localhost:8000/UserRegistrations`
2. Fill in the registration form with:
   - Name
   - Login ID
   - Password
3. Submit to create account

### Microplastic Detection

1. Access `http://localhost:8000/` (Home page)
2. Click on "Upload Image" or navigate to `http://localhost:8000/upload`
3. Select an image file containing water sample
4. Submit for detection
5. View results:
   - Detection image with bounding boxes
   - Count of each microplastic type
   - Additional visualization outputs

## Project Structure

```
Aquatic-Microplastic-Detector/
├── manage.py                    # Django management script
├── db.sqlite3                   # SQLite database
├── venv/                        # Virtual environment folder
│
├── microplastic_detection_django/    # Main Django project
│   ├── settings.py              # Project settings
│   ├── urls.py                  # URL configuration
│   ├── views.py                 # Main views
│   ├── wsgi.py                  # WSGI configuration
│   └── asgi.py                  # ASGI configuration
│
├── detection/                   # Detection app
│   ├── models.py                # Database models
│   ├── views.py                 # Detection views and logic
│   ├── urls.py                  # Detection URL patterns
│   ├── migrations/              # Database migrations
│   └── templates/               # Detection templates
│
├── admins/                      # Admin app
│   ├── models.py                # Admin models
│   ├── views.py                 # Admin views
│   └── migrations/              # Database migrations
│
├── templates/                   # HTML templates
│   ├── index.html               # Home page
│   ├── AdminLogin.html          # Admin login
│   ├── UserLogin.html           # User login
│   ├── UserRegistrations.html   # User registration
│   ├── upload.html              # Image upload page
│   ├── upload_success.html      # Detection results
│   ├── admins/                  # Admin templates
│   └── users/                   # User templates
│
├── media/                       # Uploaded images and results
├── staticfiles/                 # Static files (CSS, JS, images)
├── images/                      # Sample/test images
│
├── microplastic-detection-yolo8m.pt    # YOLOv8 model
├── t29.pt                       # Alternative model
│
└── README.md                    # This file
```

## Models

### ImageUpload Model
- Stores uploaded image information
- Tracks image path and filename

### UserRegistrationModel
- User registration data
- Fields: name, login ID, password, status, registration timestamp
- Used for user authentication and management

## Configuration

### Important Settings (microplastic_detection_django/settings.py)

- **DEBUG**: Set to `False` for production
- **ALLOWED_HOSTS**: Add your domain/IP addresses for production
- **MEDIA_ROOT**: Directory for uploaded images
- **MEDIA_URL**: URL path for accessing media files
- **INSTALLED_APPS**: Includes 'detection' and 'admins' apps

## YOLOv8 Model

The project uses pre-trained YOLOv8 models:
- **microplastic-detection-yolo8m.pt**: YOLOv8m custom trained on microplastic dataset
- Alternative models can be substituted by updating the model path in `detection/views.py`

### Classes:
- 0: Fibers
- 1: Films
- 2: Fragments
- 3: Pellets

## Development

### Create Admin User (for Django admin panel)

```bash
python manage.py createsuperuser
```

### Collect Static Files

```bash
python manage.py collectstatic
```

### Make Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Troubleshooting

### Model not found error
- Ensure `microplastic-detection-yolo8m.pt` is in the project root directory

### Permission denied on Windows
- If you get execution policy error, run:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

### Module import errors
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
- Restart the development server

### MEDIA files not displaying
- Check `MEDIA_ROOT` and `MEDIA_URL` in settings.py
- Ensure media folder has proper permissions

## Performance Considerations

- Image preprocessing may take time depending on resolution
- YOLOv8 inference time varies with image size and hardware
- For production deployment, consider using GPU acceleration
- Implement caching for frequently used models

## Security Notes

⚠️ **Important for Production:**
1. Change `SECRET_KEY` in settings.py
2. Set `DEBUG = False`
3. Change admin credentials from default
4. Use environment variables for sensitive data
5. Implement proper authentication middleware
6. Use HTTPS in production
7. Add CSRF protection validation

## Future Enhancements

- Real-time video stream processing
- GPU support optimization
- Mobile app integration
- Cloud storage integration
- Advanced analytics dashboard
- Batch processing capabilities
- Export detection reports

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open source and available under the MIT License.

## Contact

For questions and support, please contact:
- GitHub: [@MUFFASIR289](https://github.com/MUFFASIR289)

## Acknowledgments

- YOLOv8 by Ultralytics
- PyTorch team
- OpenCV community
- Django community

---

**Last Updated**: March 2026

**Project Status**: Active Development
