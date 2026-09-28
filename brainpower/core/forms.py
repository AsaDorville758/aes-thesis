from django.forms import ModelForm

from .models import Essay, Submission

class EssayForm (ModelForm):
    class Meta:
        model = Essay
        fields = [
            'student_id',
            'prompt',
            'text'
        ]
        labels = {
            'student_id':'Full Name',
            'prompt':'Topic',
            'text':'Type essay'
        }


class AudioForm (ModelForm):
    class Meta:
        model = Submission
        fields = [
            'student_id',
            'prompt',
            'file'
        ]
        labels = {
            'student_id':'Full Name',
            'prompt':'Topic',
            'file':'Recorded Essay(.wav)'
        }
