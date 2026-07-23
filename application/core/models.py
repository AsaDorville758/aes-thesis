from django.db import models

class Essay(models.Model):
    class ESSAY_STATUS(models.TextChoices):
        WAITING = 'waiting', 'Waiting to be processed'
        ACCEPTED ='accepted', 'Accepted for processing'
        REJECTED = 'rejected', 'Requires manual processing'

    student_id = models.CharField(
        max_length=10,
    )
    prompt = models.CharField(
        max_length=48
    )
    original_text = models.TextField()
    processed_text = models.TextField()
    date_uploaded = models.DateTimeField(
        auto_now_add=True
    )
    status = models.CharField(
        max_length=8,
        choices=ESSAY_STATUS.choices,
        default=ESSAY_STATUS.WAITING
    )
    def __str__(self):
        return f"""student id: {self.student_id}, prompt: {self.prompt}
            text: {self.processed_text[:30]}, date_uploaded: {self.date_uploaded}"""

class Feature(models.Model):
    essay = models.OneToOneField(
        Essay, 
        on_delete=models.CASCADE
    )
    word_count = models.PositiveSmallIntegerField()
    sentence_count = models.PositiveSmallIntegerField()
    avg_sentence_length = models.DecimalField(
        max_digits=3,
        decimal_places=1
    )
    lexical_diversity = models.DecimalField(max_digits=3,decimal_places=1)
    def __str__(self):
        return f"""word count:{self.word_count}, sentence count: {self.sentence_count}, 
            average senence length: {self.avg_sentence_length}"""

class Score(models.Model):
    essay = models.OneToOneField(
        Essay, 
        on_delete=models.CASCADE
    )
    composition = models.DecimalField(max_digits=3,decimal_places=1)
    grammar = models.DecimalField(max_digits=3,decimal_places=1)
    vocabulary = models.DecimalField(max_digits=3,decimal_places=1)
    spelling = models.DecimalField(max_digits=3,decimal_places=1)
    comprehension = models.DecimalField(max_digits=3,decimal_places=1)
    holistic = models.DecimalField(max_digits=3,decimal_places=1)
    def __str__(self):
        return f"""composition:{self.composition}, grammar: {self.grammar}, 
            vocabulary: {self.vocabulary}, spelling: {self.spelling},
                comprehension: {self.comprehension}, holistic: {self.holistic}"""
    
class Metric(models.Model):
    essay = models.OneToOneField(
        Essay,
        on_delete=models.CASCADE
    )
    transcription_confidence= models.DecimalField(max_digits=4,decimal_places=3)
    character_error_rate = models.DecimalField(max_digits=4,decimal_places=3)
    word_error_rate = models.DecimalField(max_digits=4,decimal_places=3)
    def __str__(self):
        return f"""transcription confidence:{self.transcription_confidence},
            cer: {self.character_error_rate}, wer: {self.word_error_rate}"""
    
class Submission(models.Model):
    class SUBMISSION_TYPES(models.TextChoices):
        HANDWRITTEN = 'HW', 'Handwritten'
        SPOKEN = 'SP', 'Spoken'
        TYPED = 'TY', 'Typed'

    essay = models.OneToOneField(
        Essay, 
        on_delete=models.CASCADE
    )
    type= models.CharField(
        max_length=2,
        choices=SUBMISSION_TYPES.choices,
        default=SUBMISSION_TYPES.TYPED
    )
    file = models.FileField(
        upload_to="submissions/"
    )    
    def __str__(self):
        return f"""essay_id:{self.essay}, type:{self.type}, """
    