from django.forms import ModelForm, TextInput, Textarea, URLInput, Select, DateTimeInput

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
            "thumbnail": "Thumbnail",
            "ended_at": "Berakhir pada",
        }

        widgets = {
            "title": Textarea(
                attrs={
                    "placeholder": "-",
                    "row": 3,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "-",
                    "row": 3,
                }
            ),
            "category": Select(),
            "thumbnail": Textarea(
                attrs={
                    "placeholder": "https://drive.google.com/file/...",
                    "maxlength": 255,
                }
            ),
            "ended_at": DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "placeholder": "-",
                }
            ),
        }