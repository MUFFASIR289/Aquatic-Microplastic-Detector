from django.shortcuts import render
from .models import ImageUpload
from django.core.files.storage import FileSystemStorage
from ultralytics import YOLO
from PIL import Image, ImageEnhance
import numpy as np
import cv2
import os
from django.conf import settings

model_path = 'microplastic-detection-yolo8m.pt'

def upload_image(request):
    if request.method == 'POST':
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)
        file_root, ext = os.path.splitext(filename)
        image_path = os.path.join(settings.MEDIA_ROOT, filename)

        try:
            # Load model and predict
            model = YOLO(model_path)
            pil_img = Image.open(image_path).convert('RGB')
            results = model.predict(pil_img)
            class_idx = results[0].boxes.cls.cpu().numpy().astype(int)

            # Count detections
            label_names = {0: 'Fibers', 1: 'Films', 2: 'Fragments', 3: 'Pallets'}
            label_counts = {}
            for label in class_idx:
                label_name = label_names.get(label, 'unknown')
                label_counts[label_name] = label_counts.get(label_name, 0) + 1

            # Save detection result
            res_plotted = results[0].plot()
            detected_img = Image.fromarray(res_plotted)
            detected_filename = f"{file_root}_detected.png"
            detected_output_path = os.path.join(settings.MEDIA_ROOT, detected_filename)
            detected_img.save(detected_output_path)
            detected_image_url = settings.MEDIA_URL + detected_filename

            ### ----------- HOLOGRAM IMAGE (Cool colormap overlay) -----------
            img_cv = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            heatmap = cv2.applyColorMap(gray, cv2.COLORMAP_OCEAN)
            hologram_filename = f"{file_root}_hologram.png"
            hologram_path = os.path.join(settings.MEDIA_ROOT, hologram_filename)
            cv2.imwrite(hologram_path, heatmap)
            hologram_image_url = settings.MEDIA_URL + hologram_filename

            ### ----------- RECONSTRUCTION IMAGE (Sharp + contrast) -----------
            recon_pil = pil_img.copy()
            recon_pil = ImageEnhance.Contrast(recon_pil).enhance(2.0)
            recon_pil = ImageEnhance.Sharpness(recon_pil).enhance(2.0)
            reconstruction_filename = f"{file_root}_reconstruction.png"
            reconstruction_path = os.path.join(settings.MEDIA_ROOT, reconstruction_filename)
            recon_pil.save(reconstruction_path)
            reconstruction_image_url = settings.MEDIA_URL + reconstruction_filename

            ### ----------- SEGMENTATION IMAGE (Pseudo-color simulation) -----------
            segmentation = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2GRAY)
            segmentation_color = cv2.applyColorMap(segmentation, cv2.COLORMAP_JET)
            segmentation_filename = f"{file_root}_segmentation.png"
            segmentation_path = os.path.join(settings.MEDIA_ROOT, segmentation_filename)
            cv2.imwrite(segmentation_path, segmentation_color)
            segmentation_image_url = settings.MEDIA_URL + segmentation_filename

            return render(request, 'upload_success.html', {
                'uploaded_file_url': uploaded_file_url,
                'detected_image_url': detected_image_url,
                'label_counts': label_counts,
                'prediction_time': 0,
                'hologram_image_url': hologram_image_url,
                'reconstruction_image_url': reconstruction_image_url,
                'segmentation_image_url': segmentation_image_url,
            })
        except Exception as e:
            return render(request, 'upload_success.html', {
                'uploaded_file_url': uploaded_file_url,
                'error_message': str(e)
            })

    return render(request, 'upload.html')



import os
from django.conf import settings
from django.shortcuts import render, redirect
from .models import UserRegistrationModel
from django.contrib import messages

def UserRegisterActions(request):
    if request.method == 'POST':
        user = UserRegistrationModel(
            name=request.POST['name'],
            loginid=request.POST['loginid'],
            password=request.POST['password'],
            mobile=request.POST['mobile'],
            email=request.POST['email'],
            locality=request.POST['locality'],
            address=request.POST['address'],
            city=request.POST['city'],
            state=request.POST['state'],
            status='waiting'
        )
        user.save()
        messages.success(request,"Registration successful!")
    return render(request, 'UserRegistrations.html') 


def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                data = {'loginid': loginid}
                print("User id At", check.id, status)
                return render(request, 'users/UserHomePage.html', {})
            else:
                messages.success(request, 'Your Account Not at activated')
                return render(request, 'UserLogin.html')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'UserLogin.html', {})

def UserHome(request):
    return render(request, 'users/UserHomePage.html', {})


def index(request):
    return render(request,"index.html")
