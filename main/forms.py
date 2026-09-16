from django.forms import ModelForm, TextInput, Textarea, URLInput

from main.models import Education

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