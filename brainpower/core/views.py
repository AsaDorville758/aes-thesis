
from django.shortcuts import render, redirect
from .forms import EssayForm, AudioForm
from .models import Essay, Feature, Score
from core.services.essay_editor import EssayEditor
from core.services import deberta
from core.services import whisper


def index(request):

    essay_form = EssayForm(prefix="essay")
    audio_form = AudioForm(prefix="audio")

    return render(
        request,
        'core/index.html',
        {
            'essay_form': essay_form,
            'audio_form': audio_form,
        }
    )

def submit_essay(request):

    if request.method == 'POST':

        # POST data submitted, process data
        if "submit_essay" in request.POST:

            essay_form = EssayForm(data=request.POST, prefix="essay")

            if essay_form.is_valid():

                # Extract field data
                essay_text = essay_form.cleaned_data['text']
                essay_prompt = essay_form.cleaned_data['prompt']
                student_id = essay_form.cleaned_data['student_id']

                # Initialise EssayEditor object
                ee_obj = EssayEditor(essay_text)

                essay = Essay.objects.create(
                    student_id=student_id,
                    prompt=essay_prompt,
                    uploaded_as='Text',
                    text=ee_obj.get_text()
                )

                features = Feature.objects.create(
                    essay=essay,
                    word_count=ee_obj.get_word_count(),
                    sentence_count=ee_obj.get_sentence_count(),
                )

                trait_scores = deberta.score_essay(ee_obj.get_text())

                scores = Score.objects.create(
                    essay=essay,
                    content=trait_scores['content'],
                    organization=trait_scores['organization'],
                    word_choice=trait_scores['word_choice'],
                    sentence_fluency=trait_scores['sentence_fluency'],
                    conventions=trait_scores['conventions'],
                )

                composite_score = 0

                for _, value in trait_scores.items():
                    composite_score = composite_score + value

                return render(
                    request,
                    'core/evaluation.html',
                    {
                        'student_name': student_id,
                        'essay': ee_obj,
                        'uploaded_as': 'Text',
                        'features': features,
                        'trait_scores': scores,
                        'composite_score': f"{composite_score}/30"
                    }
                )

        elif "submit_audio" in request.POST:

            audio_form = AudioForm(
                request.POST,
                request.FILES,
                prefix='audio'
            )

            if audio_form.is_valid():

                audio_instance = audio_form.save()
                audio_path = audio_instance.file.path

                output = whisper.transcribe_audio(audio_path)

                essay_prompt = audio_form.cleaned_data['prompt']
                student_id = audio_form.cleaned_data['student_id']

                # Initialise EssayEditor object
                ee_obj = EssayEditor(output['Output'].get_text())

                essay = Essay.objects.create(
                    student_id=student_id,
                    prompt=essay_prompt,
                    uploaded_as='Audio',
                    text=ee_obj.get_text()
                )

                features = Feature.objects.create(
                    essay=essay,
                    word_count=ee_obj.get_word_count(),
                    sentence_count=ee_obj.get_sentence_count(),
                )

                # Use transcription quality gate
                if output['Scoring_Method'] != 'Manual':

                    trait_scores = deberta.score_essay(ee_obj.get_text())

                    scores = Score.objects.create(
                        essay=essay,
                        content=trait_scores['content'],
                        organization=trait_scores['organization'],
                        word_choice=trait_scores['word_choice'],
                        sentence_fluency=trait_scores['sentence_fluency'],
                        conventions=trait_scores['conventions'],
                    )

                    composite_score = 0

                    for _, value in trait_scores.items():
                        composite_score = composite_score + value

                    context = {
                        'essay': ee_obj,
                        'trait_scores': scores,
                        'features': features,
                        'uploaded_as': 'Audio',
                        'student_name': student_id,
                        'composite_score': f"{composite_score}/30"
                    }

                else:

                    context = {
                        'essay': ee_obj,
                        'features': features,
                        'uploaded_as': 'Audio',
                        'student_name': student_id,
                        'manual_scoring': True
                    }

                return render(
                    request,
                    'core/evaluation.html',
                    context
                )

    return redirect('core:index')

