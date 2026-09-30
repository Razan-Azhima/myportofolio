from django.forms import ModelForm, TextInput, Textarea, URLInput, Select, DateTimeInput
from django.db.models import ManyToManyField
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

from main.models import Education, Skill, Achievement, Experience

class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = [
            "institution",
            "degree_or_major",
            "faculty",
            "period",
            "status",
        ]

        labels = {
            "institution": "Tempat Pendidikan",
            "degree_or_major": "Prodi/Keminatan",
            "faculty": "Fakultas/Sekolah", 
            "period": "Periode",
            "status": "Status",
        }

        widgets = {
            "institution": TextInput(
                attrs={
                    "placeholder": "-",
                    "maxlength": 255,
                }
            ),
            "degree_or_major": Textarea(
                attrs={
                    "placeholder": "-",
                    "rows": 3,
                }
            ),
            "faculty": Textarea(
                attrs={
                    "placeholder": "-",
                    "rows": 3,
                }
            ),
            "period": TextInput(
                attrs={
                    "placeholder": "-",
                }
            ),
            "status": TextInput(
                attrs={
                    "placeholder": "-",
                }
            ),
        }

class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = [
            "category",
            "name",
            "description",
        ]
        
        labels = {
            "category": "Kategori",
            "name": "Nama",
            "description": "Deskripsi", 
        }

        widgets = {
            "category": Select(),
            "name": Textarea(
                attrs={
                    "placeholder": "-",
                    "row": 3,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "-",
                    "maxlength": 255,
                }
            ),
        }

class AchievementForm(ModelForm):
    class Meta:
        model = Achievement
        fields = [
            "title",
            "category",
            "year",
            "description",
            "issuer",
        ]
        
        labels = {
            "title": "Judul",
            "category": "Kategori",
            "year": "Tahun",
            "description": "Deskripsi", 
            "issuer": "Pengisu",
        }

        widgets = {
            "title": Textarea(
                attrs={
                    "placeholder": "-",
                    "row": 3,
                }
            ),
            "category": Textarea(
                attrs={
                    "placeholder": "-",
                    "row": 3,
                }
            ),
            "year": Textarea(
                attrs={
                    "placeholder": "-",
                    "maxlength": 4,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "-",
                    "maxlength": 255,
                }
            ),
            "issuer": Textarea(
                attrs={
                    "placeholder": "-",
                    "maxlength": 100,
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
            "title": "Judul",
            "description": "Deskripsi",
            "category": "Kategori",
            "thumbnail": "Thumbnail (URL gambar / link Google Drive)",
            "ended_at": "Berakhir pada (kosongkan jika masih berlangsung)",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "-",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "-",
                    "rows": 3,
                }
            ),
            "category": Select(),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/file/...",
                    "maxlength": 200,  # sesuai default max_length URLField
                }
            ),
            "ended_at": DateTimeInput(
                format="%Y-%m-%dT%H:%M",  # supaya nilai lama terisi di input datetime-local saat update
                attrs={
                    "type": "datetime-local",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ended_at"].input_formats = [
            "%Y-%m-%dT%H:%M",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
        ]

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Judul tidak boleh hanya berisi tag HTML.")
        return title

    def clean_description(self):
        description = strip_tags(self.cleaned_data["description"]).strip()
        if not description:
            raise ValidationError("Deskripsi tidak boleh hanya berisi tag HTML.")
        return description
