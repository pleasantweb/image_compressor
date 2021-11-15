from django.utils import timezone
import io
import sys
import random
import string
from .models import Upload
from .serializers import UploadSerializer
from rest_framework import viewsets
from PIL import Image
from rest_framework.response import Response
from rest_framework import status
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.parsers import FormParser,MultiPartParser
from rest_framework.views import APIView
# from celery.schedules import crontab
# from celery.task import periodic_task
# Create your views here.


# ------------------------------------------------------------------------------
        # Uploaded image details
def img_details(img):
    orignal_image = Image.open(img)
    uploaded_image_resolution = orignal_image.size
    img_format = orignal_image.format.lower()
    if img_format == 'jpeg':
        extension = 'jpg'
    else:
        extension = img_format
    return orignal_image,uploaded_image_resolution,extension,img_format

# ---------------------------------------------------------------------------
                # Final Image after work
def result_image(new_image,bef_res,aft_res,ext,img_format):
    st = string.ascii_letters
    ar=[]
    for i in range(10):
        ar.insert(i,random.choice(st))
    random_name = ''.join(ar)
    result_imgae = InMemoryUploadedFile(new_image,'ImageField',f"img_{random_name}_compressod.{ext}",f'image/{img_format}',sys.getsizeof(new_image),None)
    return bef_res,aft_res,result_imgae 


# ---------------------------------------------------------------------------
                #  Compress / Resize image
def compress_resize(image_uploaded,work,percentage=None,x=None,y=None):
    orignal_image,uploaded_image_resolution,extension,img_format = img_details(image_uploaded)
    out = io.BytesIO()
    if work == 'compress':
        xx,yy = orignal_image.size
        compressed_x =int(xx/100 * int(percentage))
        compressed_y = int(yy/100 * int(percentage ))
        new_image = orignal_image.resize((compressed_x,compressed_y))
    else:
        new_image = orignal_image.resize((int(x),int(y)))
    new_image_resolution = new_image.size
    new_image.save(out,format=img_format,quality=50)
    out.seek(0)
    uploaded_image_resolution, new_image_resolution,result_imgae = result_image(out,uploaded_image_resolution,new_image_resolution,extension,img_format)
    return uploaded_image_resolution, new_image_resolution,result_imgae
   

# --------------------------------------------------------------------------
        #    Upload model view set
class UploadModelViewSet(viewsets.ModelViewSet):
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer
    parser_classes = [FormParser,MultiPartParser]

    def create(self,request):   
        data = {
            'current_size':'',
            'uploaded_image':[],
            'action':'',
            'size_after':'',
            'resize_measure_x':'',
            'resize_measure_y':'',
            'orignal_size_x_y':''  
        }
        image_posted = request.FILES['uploaded_image']
        action = request.data.get('action')
        
        if  image_posted.size < 999999:
            data['current_size'] = f"{round(image_posted.size/1024,2)} kb"
        else:
            data['current_size'] = f"{round(image_posted.size/1048576,2)} mb"

        data['action'] = action
        
        if action == 'compress':
            compress_percentage = request.data.get('compress_percentage')
            old_resolution, new_resolution, result_image = compress_resize(image_posted,'compress',percentage=compress_percentage)         
        else:
            resize_measure_x = request.data.get('resize_measure_x')
            resize_measure_y = request.data.get('resize_measure_y')
            old_resolution,new_resolution,result_image = compress_resize(image_posted,'resize',x=resize_measure_x,y=resize_measure_y)
           
        old_x,old_y = old_resolution
        data['orignal_size_x_y'] = f"{old_x} * {old_y}"
        new_x,new_y = new_resolution
        data['resize_measure_x'] = new_x
        data['resize_measure_y'] = new_y

        data['uploaded_image'] =result_image
        
        if result_image.size < 999999:
            data['size_after'] = f"{round(result_image.size/1024,2)} kb"
        else:
            data['size_after'] = f"{round(result_image.size/1048576,2)} mb"
       
        serializer = UploadSerializer(data = data)
        if serializer.is_valid():
            new_img_save =serializer.save()
            id = new_img_save.id
            return Response({'img_id':id,'message':'Image compressed/resize successfully'},status=status.HTTP_201_CREATED)
        return Response({'message':'Somethin went wrong while posting your article'},status=status.HTTP_400_BAD_REQUEST)

    
# --------------------------------------------------------------------------
                # Delete old photos
class DeleteOldPhotosView(APIView):
    def delete(self,request,format=None):
        old_items =Upload.objects.filter(will_be_delete_at__lt =  timezone.now() )
        old_items.delete()
        return Response({'success':'Old photos deleted successfully'})
