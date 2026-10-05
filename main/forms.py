

from django.forms.models import ModelForm
from main.models import Experience, Project
from django.forms import TextInput, Textarea, URLInput
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags



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
                    "placeholder": "https://drive.google.com/image_url?id=...&sz=w1000",
                }
            ),
        }

        def clean_title(self):
            title = strip_tags(self.cleaned_data["title"]).strip()
            if not title:
                raise ValidationError("Project name can't contain only HTML tags.")
            return title

        def clean_tech_stack(self):
            return strip_tags(self.cleaned_data["tech_stack"]).strip()

        def clean_description(self):
            return strip_tags(self.cleaned_data["description"]).strip()

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "experience_image_url",
            "ended_at",
        ]

        labels = {
            "title": "Nama Pengalaman",
            "description": "Deskripsi Pengalaman",
            "category": "Kategori",
            "experience_image_url": "URL Image pengalaman",
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
            "experience_image_url": URLInput(
                attrs={
                    "placeholder": "https://example.com/image_url.jpg",
                }
            ),
            "ended_at": TextInput(
                attrs={
                    "placeholder": "2026-12-31",
                }
            ),
        }