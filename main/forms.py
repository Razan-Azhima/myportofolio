from django.forms import ModelForm, TextInput, Textarea, URLInput, Select

from main.models import Education, Skill

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