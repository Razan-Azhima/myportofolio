import uuid, re
from django.db import models

class Experience(models.Model):
    # Model Experience yang sudah Anda buat sebelumnya
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title
    
    @property
    def thumbnail_direct_url(self):
        if not self.thumbnail:
            return ""

        # Mengambil File ID dari berbagai format link Google Drive
        drive_pattern = r'(?:file/d/|id=|d/)([a-zA-Z0-9_-]{25,})'
        match = re.search(drive_pattern, self.thumbnail)

        if match:
            file_id = match.group(1)
            return f"https://lh3.googleusercontent.com/d/{file_id}"
        
        # Jika bukan link Google Drive (misal link gambar biasa), kembalikan URL asli
        return self.thumbnail
    
    @property
    def is_ongoing(self):
        return self.ended_at is None


class Achievement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)  # Contoh: "Nasional", "Kompetisi"
    year = models.CharField(max_length=10)        # Contoh: "2025"
    description = models.TextField()
    issuer = models.CharField(max_length=255, blank=True, null=True) # Contoh: "ITB"

    def __str__(self):
        return self.title


class Education(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    institution = models.CharField(max_length=255)     # Contoh: "Universitas Indonesia"
    degree_or_major = models.CharField(max_length=255) # Contoh: "Ilmu Komputer"
    faculty = models.CharField(max_length=255, blank=True, null=True) # Contoh: "Fakultas Ilmu Komputer"
    period = models.CharField(max_length=50)            # Contoh: "2024 – Sekarang"
    status = models.CharField(max_length=255)           # Contoh: "Mahasiswa Aktif (NPM: ...)"

    def __str__(self):
        return self.institution


class Skill(models.Model):
    SKILL_CATEGORY_CHOICES = [
        ('backend', 'Backend'),
        ('frontend', 'Frontend'),
        ('tools', 'Tools & Workflow'),
        ('other', 'Lainnya'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)            # Contoh: "Python / Django", "Git & GitHub"
    category = models.CharField(max_length=50, choices=SKILL_CATEGORY_CHOICES, default='backend')
    description = models.TextField()

    def __str__(self):
        return self.name

# put comments right next to the charfields so i don't forget like a dummy