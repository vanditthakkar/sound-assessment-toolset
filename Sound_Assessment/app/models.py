from django.db import models
from django.forms import ModelForm

class TeacherFile(models.Model):
    num = models.IntegerField()
    file_upload = models.FileField(upload_to='teacher_file')

class StudentFile(models.Model):
    file_upload = models.FileField("Choose File",upload_to='student_file')
    name = models.CharField(max_length=100)


    def __str__(self):
        return "File"

class StudentFileForm(ModelForm):
    class Meta:
        model = StudentFile
        fields = ['file_upload']