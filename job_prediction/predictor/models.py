from django.db import models

class JobData(models.Model):
    emp_id = models.CharField(max_length=100, unique=True, default='EMP000000')
    job_title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    experience_required = models.CharField(max_length=100)
    job_type = models.CharField(max_length=50)  
    industry = models.CharField(max_length=100)
    skills_required = models.TextField()
    education_level = models.CharField(max_length=100)
    remote_option = models.BooleanField(default=False)
    posted_date = models.DateField(null=True, blank=True)
    
    # Add more fields based on your dataset columns
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'job_dataset_cleaned'
        verbose_name = 'Job Data'
        verbose_name_plural = 'Job Data'
    
    def __str__(self):
         return f"{self.emp_id} - {self.job_title} at {self.company}"