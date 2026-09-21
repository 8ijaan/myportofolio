

from django.forms.models import ModelForm
from main.models import Experience, Project
from django.forms import TextInput, Textarea, URLInput



class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "project_url": "URL Proyek",
            "project_image_url": "URL Gambar Proyek",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Tell us about your project",
                    "rows": 3,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/kakBurhan/burhanquestv4",
                }
            ),
            "project_image_url": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "ended_at",
        ]

        labels = {
            "title": "Nama Pengalaman",
            "description": "Deskripsi Pengalaman",
            "category": "Kategori",
            "thumbnail": "Thumbnail",
            "ended_at": "Diakhiri Pada",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Staff of Software Engineering Academy 2026",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Tell us about your experience",
                    "rows": 3,
                }
            ),
            "category": TextInput(
                attrs={
                    "placeholder": "part-time",
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://example.com/thumbnail.jpg",
                }
            ),
            "ended_at": TextInput(
                attrs={
                    "placeholder": "2026-12-31",
                }
            ),
        }