from django.contrib import admin
from .models import StudentData, CompanyStudents, Company


admin.site.register(StudentData)

class CompanyStudentsAdmin(admin.StackedInline):
    model = CompanyStudents

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    inlines = [CompanyStudentsAdmin]

    class Meta:
       model = Company

@admin.register(CompanyStudents)
class CompanyStudentsAdmin(admin.ModelAdmin):
    pass
