from django.db import models


class Complain(models.Model):
    student_name = models.CharField(max_length=100, blank=True, null=True)
    student_id = models.CharField(max_length=20)
    problem_details = models.TextField()
    complain_image = models.ImageField(upload_to='complain_images/', blank=True, null=True)
    is_resolved = models.BooleanField(default=False)
    resolved_image = models.ImageField(upload_to='resolved_images/', blank=True, null=True)
    solution_details = models.TextField(blank=True, null=True, default="Pending")
    feedback_status = models.TextField(blank=True, null=True, default="Pending")
    submitted_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.student_name} - {self.student_id}"

