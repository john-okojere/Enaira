import email
from gc import get_objects
import sys
from django.shortcuts import redirect, render
from email.mime import image
from http.client import HTTPResponse
from django.shortcuts import render
from pathlib import Path
import face_recognition
import os
from PIL import Image
import urllib
import base64
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from accounts.forms import Transerform
from .models import Transfer, User, Image as Imagephoto
from django.shortcuts import get_object_or_404

BASE_DIR = Path(__file__).resolve().parent


@login_required
def Success(request):  
    return render(request, 's.html')


@login_required
def Failed(request):  
    return render(request, 'f.html')

@login_required
def verify_acccount(request):
    if request.method == 'POST':
        data = request.POST.dict()
        email = data.get("email")
        try:
            sender = get_object_or_404(User, email=email)
        except:
            messages.error(request, 'sender email does not exist')
            return redirect('/' )
        form = Transerform(request.POST)
        if form.is_valid():
            comment= form.save(commit=False)
            comment.receiver = request.user
            try:
                comment.sender = sender
            except:
                return redirect('/' )
            form = form.save()
            print(form.uid)
            return redirect('face_verify',comment.uid )
            
    else:
        form = Transerform()
    # if user:
    #     return redirect('face_verify', user.uid)
    return render(request, 'index.html', {'form':form})


@login_required
def verify_face(request, uid):
    try:
        transfer = get_object_or_404(Transfer, uid=uid)
        # user = transfer.receiver
        user = transfer.sender
    
        if(request.POST):
            data = request.POST.dict()
            image = data.get("image")
            try:
                format, imgstr = image.split(';base64,')
                print("format", format)
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext) # You can save this as file instance.
                file_name = Imagephoto.objects.create(image=data)
                print(file_name.uid)

                img =f'http://127.0.0.1:8000{user.image.url}'
                img2 =f'http://127.0.0.1:8000{file_name.image.url}'
                known_image = face_recognition.load_image_file(urllib.request.urlopen(img))
                unknown_image = face_recognition.load_image_file(urllib.request.urlopen(img2))
                
                image1_encoding = face_recognition.face_encodings(known_image)[0]
            except:
                messages.error(request, 'Verification Failed, Try again')
                return redirect('face_verify', user.uid)
            try:
                image2_encoding = face_recognition.face_encodings(unknown_image)[0]
            except IndexError as e:
                messages.error(request, 'Verification Failed, Try again')
                return redirect('face_verify', transfer.uid)

            results = face_recognition.compare_faces([image1_encoding], image2_encoding)
            print(results)
            if results[0] == True:
                return redirect('success')
            else:
                messages.error(request, 'Verification Failed, Try again')
                return redirect('face_verify', user.uid)
        data= {'user':user}
    except:
        messages.error(request, 'Verification Failed, Try again')
        return redirect('/')
    
    return render(request, 'face.html', data)


