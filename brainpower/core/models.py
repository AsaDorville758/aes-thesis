from django.db import models

class Essay(models.Model):
    student_id = models.CharField(
        max_length=48,
    )
    prompt = models.CharField(
        max_length=48
    )
    text = models.TextField()
    uploaded_as = models.CharField(
        max_length=6,
        default='Text'

    )
    date_uploaded = models.DateTimeField(
        auto_now_add=True
    )
    def __str__(self):
        return f"""student id: {self.student_id}, prompt: {self.prompt}
            text: {self.text[:30]}, uploaded as: {self.upload_format}, date_uploaded: {self.date_uploaded}"""

class Feature(models.Model):
    essay = models.OneToOneField(
        Essay, 
        on_delete=models.CASCADE
    )
    word_count = models.PositiveSmallIntegerField()
    sentence_count = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"""word count:{self.word_count}, sentence count: {self.sentence_count}"""
    
class Score(models.Model):
    essay = models.OneToOneField(
        Essay, 
        on_delete=models.CASCADE
    )
    content = models.PositiveSmallIntegerField()
    organization = models.PositiveSmallIntegerField()
    word_choice = models.PositiveSmallIntegerField()
    sentence_fluency = models.PositiveSmallIntegerField()
    conventions = models.PositiveSmallIntegerField()
    def __str__(self):
        return f"""Content:{self.content}, Organisation: {self.organization}, 
            word_choice: {self.word_choice}, sentence_fluency: {self.sentence_fluency},
            conventions: {self.conventions}"""
   
class Submission(models.Model):
    student_id = models.CharField(
        max_length=48,
    )
    prompt = models.CharField(
        max_length=48
    )
    file = models.FileField(
        upload_to="./assets/audio_files"
    )  
    def __str__(self):
        return f"""Audio uploaded by:{self.student_id}"""  

    