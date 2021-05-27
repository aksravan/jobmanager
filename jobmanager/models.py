from django.db import models


class Company(models.Model):
    company_name = models.CharField(default=None, max_length=100, unique=True)
    usrname = models.CharField(default=None, max_length=50, null=True, unique=True)
    requirements = models.TextField(default=None, max_length=2000)

    def __str__(self):
        return self.company_name

class CompanyStudents(models.Model):
    company = models.ForeignKey(
        Company, default=None, on_delete=models.CASCADE)
    student_id = models.CharField(default=None, max_length=100)
    isselected = models.BooleanField(default=False)

    def __str__(self):
        return self.student_id

# changing the resume name
def uploadhere(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.name, instance.roll_no, ext)
    return 'static/files/{0}'.format(filename)

semchoices = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
]

class StudentData(models.Model):
    name = models.CharField(max_length=70)
    roll_no = models.CharField(max_length=20, unique=True)
    semester = models.IntegerField(choices=semchoices)
    email = models.EmailField(max_length=100)
    college = models.CharField(max_length=100)
    github = models.URLField(
        default=None, max_length=100, null=True, blank=True)
    resume = models.FileField(upload_to=uploadhere)

    def __str__(self):
        return self.roll_no
