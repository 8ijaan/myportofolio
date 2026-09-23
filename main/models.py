import uuid

from django.contrib.auth.models import User
from django.db import models


class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ("internship", "Internship"),
        ("research", "Research"),
        ("volunteer", "Volunteer"),
        ("part-time", "Part-Time"),
        ("full-time", "Full-Time"),
        ("freelance", "Freelance"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=EXPERIENCE_CHOICES,
        default="full-time",
    )
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        return self.ended_at is None

    def logo_url(self):
        return f"/static/img/experience/{self.title.lower().replace(' ', '_')}.svg"

class Skill(models.Model): 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
            return self.name
        
    def logo_url(self):
        return f"/static/img/skills/{self.name.lower()}.svg"

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    tech_stack = models.CharField(max_length=255)
    project_url = models.URLField(blank=True)
    project_image_url = models.URLField(blank=True, max_length=500)
    starred_by = models.ManyToManyField(
        User, related_name="starred_projects", blank=True
    )

    def __str__(self):
        return self.title


# Here is what each part does:

# models.Model is Django’s base class for database-backed models.
# EXPERIENCE_CHOICES limits category to a known set of values.
# id creates a UUID primary key automatically.
# title stores a short title, up to 255 characters.
# description stores longer text about the experience.
# category stores one value from EXPERIENCE_CHOICES and defaults to full-time.
# thumbnail stores an optional image URL.
# started_at records when the row is created.
# ended_at may be left empty for an ongoing experience.
# __str__() gives each object a readable string representation.
# is_ongoing returns True when ended_at is empty.

