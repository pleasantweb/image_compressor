
from rest_framework import serializers
from .models import Upload

class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = ('id','uploaded_image','current_size','size_after','action','compress_percentage','orignal_size_x_y','resize_measure_x','resize_measure_y','will_be_delete_at')
