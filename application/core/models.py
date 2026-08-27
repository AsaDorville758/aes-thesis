from django.db import models

class Essay(models.Model):
    class ESSAY_STATUS(models.TextChoices):
        WAITING = 'waiting', 'Essay has not been evaluated as yet'
        PASS ='pass', 'Routed to transformer for scoring'
        FAIL = 'fail', 'Routed to human scorer for manual processing'

    student_id = models.CharField(
        max_length=10,
    )
    prompt = models.CharField(
        max_length=48
    )
    original_text = models.TextField()
    normalised_text = models.TextField()
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
            text: {self.normalised_text[:30]}, date_uploaded: {self.date_uploaded}"""

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
    # lexical_diversity = models.DecimalField(max_digits=3,decimal_places=1)
    def __str__(self):
        return f"""word count:{self.word_count}, sentence count: {self.sentence_count}, 
            average sentence length: {self.avg_sentence_length}"""
    
class Score(models.Model):
    essay = models.OneToOneField(
        Essay, 
        on_delete=models.CASCADE
    )
    content = models.PositiveSmallIntegerField()
    organisation = models.PositiveSmallIntegerField()
    word_choice = models.PositiveSmallIntegerField()
    sentence_fluency = models.PositiveSmallIntegerField()
    conventions = models.PositiveSmallIntegerField()
    holistic = models.DecimalField(max_digits=3,decimal_places=1)
    def __str__(self):
        return f"""Content:{self.content}, Organisation: {self.organisation}, 
            word_choice: {self.word_choice}, sentence_fluency: {self.sentence_fluency},
            conventions: {self.conventions}, Score: {self.holistic}"""

class Metric(models.Model):
    essay = models.OneToOneField(
        Essay,
        on_delete=models.CASCADE
    )
    avg_logprob = models.DecimalField(
        max_digits=4,
        decimal_places=3, 
        null=True,
        blank=True
        )
    compression_ratio = models.DecimalField(
        max_digits=4,
        decimal_places=3, 
        null=True,
        blank=True
        )
    avg_confidence_score = models.DecimalField(
        max_digits=4,
        decimal_places=3, 
        null=True,
        blank=True
        )
    def __str__(self):
        return f"""ASR Evaluation -(avg_logprob):{self.avg_logprob}, (compression ratio):{self.compression_ratio};
            OCR Evaluation - (average confidence score):{self.avg_confidence_score}"""
    
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
    