# BrainPower

## Multimodal Automated Essay Scoring System

BrainPower is a hybrid, multimodal Automated Essay Scoring (AES) application developed to assist human assessment of student essays.

The application accepts either **typed essays** or **spoken essays recorded as audio**. Spoken essays are converted into text using Faster-Whisper before being processed by a fine-tuned DeBERTa model.

The DeBERTa model produces scores for five essay traits:

* Content
* Organization
* Word Choice
* Sentence Fluency
* Conventions

BrainPower is designed as an **assessment support tool**. The system provides automated scores and processing information while retaining the human assessor in the assessment process.

---

# Features

* Submit typed essays through a web interface.
* Submit audio recordings of spoken essays.
* Transcribe audio locally using Faster-Whisper.
* Normalise essay text before scoring.
* Calculate word and sentence counts.
* Score essays using a fine-tuned DeBERTa-v3-base model.
* Produce five trait-level essay scores.
* Store essay and scoring information using Django and SQLite.
* Display evaluation results through a web interface.

---

# System Pipeline

For typed essays:

```text
Typed Essay
     │
     ▼
Text Normalisation
     │
     ▼
Feature Extraction
     │
     ▼
DeBERTa
     │
     ▼
Five Trait Scores
     │
     ▼
Django Database
     │
     ▼
Evaluation Page
```

For audio essays:

```text
Audio Recording
     │
     ▼
Faster-Whisper
     │
     ▼
Transcript
     │
     ▼
Text Normalisation
     │
     ▼
Feature Extraction
     │
     ▼
DeBERTa
     │
     ▼
Five Trait Scores
     │
     ▼
Django Database
     │
     ▼
Evaluation Page
```

All processing is performed locally after the required models have been downloaded.

---

# Technologies

BrainPower uses:

* Python 3.11
* Django 5.2
* PyTorch
* Hugging Face Transformers
* DeBERTa-v3-base
* Faster-Whisper
* librosa
* NLTK
* NumPy
* jiwer
* SQLite

---

# Requirements

## Software

The recommended environment is:

* Python 3.11
* Windows 10/11 or another Python-compatible operating system
* Git
* An NVIDIA GPU with CUDA support is recommended for practical inference performance.

BrainPower was developed and tested using an NVIDIA GPU with CUDA-enabled PyTorch.

## Hardware

GPU acceleration is recommended because both speech recognition and DeBERTa inference are computationally intensive.

The development system used:

* NVIDIA GTX 1660 SUPER
* 6 GB VRAM
* 32 GB system RAM

A CPU-only installation may be possible, but inference will be slower.

---

# Installation

## 1. Clone the repository

Clone the BrainPower repository:

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd BrainPower
```

If the Django project is contained inside the `application` directory:

```bash
cd application
```

---

## 2. Create a virtual environment

BrainPower was developed using Python 3.11.

On Windows:

```bash
py -3.11 -m venv env
```

Activate the virtual environment:

```bash
env\Scripts\activate
```

On macOS/Linux:

```bash
python3.11 -m venv env
source env/bin/activate
```

---

# 3. Install PyTorch

BrainPower uses PyTorch for DeBERTa inference.

The development environment used a CUDA-enabled PyTorch installation:

```text
PyTorch 2.11.0
CUDA 12.8 build
```

The exact PyTorch installation command depends on the user's operating system and GPU/CUDA configuration.

Install the appropriate PyTorch build for your system using the official PyTorch installation instructions before continuing.

Verify the installation:

```python
import torch

print(torch.__version__)
print(torch.cuda.is_available())
```

For a CUDA-enabled installation, the second command should return:

```text
True
```

If it returns `False`, PyTorch is installed but cannot currently access a CUDA-compatible GPU.

---

# 4. Install BrainPower dependencies

From the directory containing `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

# 5. Install the NLTK resource

BrainPower uses NLTK's `punkt_tab` tokenizer data.

Run:

```bash
python
```

Then:

```python
import nltk
nltk.download("punkt_tab")
```

Exit Python:

```python
exit()
```

---

# 6. DeBERTa model

BrainPower uses a fine-tuned DeBERTa-v3-base model trained using the ASAP 1.0 Prompt 1 essay data.

The model is hosted on Hugging Face:

**asadorville/brainpower-deberta-asap1-prompt1**

The model can be accessed through the Hugging Face Hub:

https://huggingface.co/marcusjonas/brainpower-deberta-asap1-prompt1

The model does not need to be committed to the GitHub repository.

When the application loads the model using Hugging Face Transformers, the required model files can be downloaded and cached locally.

The model produces five outputs:

```text
Content
Organization
Word Choice
Sentence Fluency
Conventions
```

The original ASAP holistic score is not used by the BrainPower scoring model.

---

# 7. Faster-Whisper

BrainPower uses Faster-Whisper for spoken essay transcription.

The application uses the **Whisper medium** model.

When the Whisper model is first loaded, the required model files may need to be downloaded. An internet connection is therefore required during the initial model setup unless the model has already been downloaded and cached.

The audio processing pipeline is:

```text
Audio File
    ↓
Faster-Whisper Medium
    ↓
Transcript
    ↓
EssayEditor
    ↓
Normalised Text
    ↓
DeBERTa
```

---

# 8. Django database

Navigate to the directory containing `manage.py`.

Run:

```bash
python manage.py migrate
```

This creates the required Django database tables.

BrainPower uses SQLite for the application database.

---

# 9. Start BrainPower

Start the Django development server:

```bash
python manage.py runserver
```

Open a web browser and navigate to:

```text
http://127.0.0.1:8000/
```

---

# Using BrainPower

## Typed Essay

To submit a typed essay:

1. Open the BrainPower web interface.
2. Enter the student information.
3. Enter the essay prompt.
4. Enter the essay text.
5. Submit the essay.
6. BrainPower normalises the text and extracts basic features.
7. The essay is passed to the DeBERTa scoring model.
8. The five trait scores are displayed on the evaluation page.

The original essay text is retained separately from the normalised text used during processing.

---

## Audio Essay

To submit an audio essay:

1. Open the BrainPower web interface.
2. Enter the required student information.
3. Select the audio submission option.
4. Select the recorded essay file.
5. Submit the file.
6. Faster-Whisper transcribes the recording.
7. The transcript is processed by the essay editor.
8. The processed transcript is passed to DeBERTa.
9. The five trait scores are displayed on the evaluation page.

---

# Essay Scoring

The DeBERTa model generates five trait predictions:

| Trait            | Description                                         |
| ---------------- | --------------------------------------------------- |
| Content          | The essay's development and relevance of ideas      |
| Organization     | The structure and organisation of ideas             |
| Word Choice      | The effectiveness and appropriateness of vocabulary |
| Sentence Fluency | The structure and flow of sentences                 |
| Conventions      | The use of standard writing conventions             |

Scores are generated independently for each trait.

The application does not store a separate holistic DeBERTa score. A composite score can instead be calculated from the trait scores when required.

---

# Audio Transcription Evaluation

The accuracy of automatic speech transcription can be evaluated using:

### Word Error Rate (WER)

WER measures the number of word-level errors between a reference transcription and the generated transcription.

### Character Error Rate (CER)

CER measures the number of character-level errors between the reference and generated transcripts.

BrainPower uses `jiwer` to calculate these metrics during transcription evaluation.

---

# Project Structure

The main project structure is:

```text
BrainPower/
│
├── application/
│   │
│   ├── brainpower/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── ...
│   │
│   ├── core/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   │
│   │   ├── services/
│   │   │   ├── whisper.py
│   │   │   ├── deberta.py
│   │   │   └── essay_editor.py
│   │   │
│   │   └── templates/
│   │       └── core/
│   │
│   ├── manage.py
│   └── db.sqlite3
│
├── requirements.txt
└── README.md
```

The exact structure may change as the project develops.

---

# Models

## DeBERTa

BrainPower uses a fine-tuned:

```text
microsoft/deberta-v3-base
```

model hosted as:

```text
marcusjonas/brainpower-deberta-asap1-prompt1
```

The model was fine-tuned for five regression outputs corresponding to the five essay traits.

## Faster-Whisper

Faster-Whisper is used to convert spoken essays into text.

The medium model is used for English speech recognition.

---

# Local Processing and Privacy

The AI processing performed by BrainPower is designed to run locally.

After the required Python packages and models have been downloaded, essay processing does not require sending the essay text or audio recording to an external scoring service.

The DeBERTa model is obtained from Hugging Face during setup and cached locally.

The Faster-Whisper model is likewise downloaded and used locally.

---

# Troubleshooting

## `torch.cuda.is_available()` returns `False`

Check that:

* An NVIDIA GPU is installed.
* The NVIDIA driver is installed.
* A CUDA-compatible PyTorch build is installed.
* The correct Python virtual environment is active.

BrainPower can potentially run without GPU acceleration, but inference may be significantly slower.

---

## Hugging Face model cannot be downloaded

Check that:

* The computer has an internet connection.
* The Hugging Face model repository is accessible.
* The model name is entered correctly.

The required model is:

```text
marcusjonas/brainpower-deberta-asap1-prompt1
```

---

## NLTK reports that `punkt_tab` is missing

Run:

```python
import nltk
nltk.download("punkt_tab")
```

---

## Django cannot find the database tables

Run:

```bash
python manage.py migrate
```

---

# Requirements File

The main runtime dependencies are listed in `requirements.txt`.

The project does not require the complete development environment used to build BrainPower. Development-only packages such as Jupyter, Matplotlib, pandas, PaddleOCR and related experimentation packages are therefore not required to run the application.

---

# Project Purpose

BrainPower was developed as a university final project exploring the orchestration of multiple AI models to achieve a common goal: providing an accessible and multimodal automated essay scoring system.

The project combines:

* speech recognition,
* natural language processing,
* transformer-based essay scoring,
* feature extraction,
* database storage,
* and a web-based user interface

into a single application.

The intended role of BrainPower is to **assist human assessment rather than replace human assessors**.

