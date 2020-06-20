from django.forms import ModelForm,Form
from django import forms
from .models import *

from ckeditor_uploader.widgets import CKEditorUploadingWidget
class TheoryTagForm(ModelForm):
    prerequisiteHiddenField=forms.CharField(widget=forms.HiddenInput(),required=False)
    twinConceptprerequisiteHiddenField=forms.CharField(widget=forms.HiddenInput(),required=False)
    class Meta:
        model=Theory
        exclude=["userId","subConcept"]
        widgets = {'userId': forms.HiddenInput(),'subConcept':forms.HiddenInput(),'difficulty':forms.RadioSelect(attrs={'class': 'inline'} ) ,'importance':forms.RadioSelect(attrs={'class': 'inline'} )}
        labels = {
            'easyExampleQues1':'Easy Question 1',
            'easyExampleSol1':'Easy Solution 1',
            'easyExampleQues2':'Easy Question 2',
            'easyExampleSol2':'Easy Solution 2',
            'easyExampleQues3':'Easy Question 3',
            'easyExampleSol3':'Easy Solution 3',
            'easyExampleQues4':'Easy Question 4',
            'easyExampleSol4':'Easy Solution 4',
            'easyExampleQues5':'Easy Question 5',
            'easyExampleSol5':'Easy Solution 5',
            'easyExampleQues6':'Easy Question 6',
            'easyExampleSol6':'Easy Solution 6',
            'easyExampleQues7':'Easy Question 7',
            'easyExampleSol7':'Easy Solution 7',

            'mediumExampleQues1':'Medium Question 1',
            'mediumExampleQues2':'Medium Question 2',
            'mediumExampleQues3':'Medium Question 3',
            'mediumExampleQues4':'Medium Question 4',
            'mediumExampleQues5':'Medium Question 5',
            'mediumExampleQues6':'Medium Question 6',
            'mediumExampleQues7':'Medium Question 7',
            'mediumExampleSol1':'Medium Solution 1',
            'mediumExampleSol2':'Medium Solution 2',
            'mediumExampleSol3':'Medium Solution 3',
            'mediumExampleSol4':'Medium Solution 4',
            'mediumExampleSol5':'Medium Solution 5',
            'mediumExampleSol6':'Medium Solution 6',
            'mediumExampleSol7':'Medium Solution 7',

            'hardExampleQues1':'Hard Question 1',
            'hardExampleQues2':'Hard Question 2',
            'hardExampleQues3':'Hard Question 3',
            'hardExampleQues4':'Hard Question 4',
            'hardExampleQues5':'Hard Question 5',
            'hardExampleQues6':'Hard Question 6',
            'hardExampleSol1':'Hard Solution 1',
            'hardExampleSol2':'Hard Solution 2',
            'hardExampleSol3':'Hard Solution 3',
            'hardExampleSol4':'Hard Solution 4',
            'hardExampleSol5':'Hard Solution 5',
            'hardExampleSol6':'Hard Solution 6',

            'easyIntegerTypeQues1':'Easy Integer Type Question 1',
            'easyIntegerTypeQues2':'Easy Integer Type Question 2',
            'mediumIntegerTypeQues1':'Medium Integer Type Question 1',
            'mediumIntegerTypeQues2':'Medium Integer Type Question 2',
            'hardIntegerTypeQues1':'Hard Integer Type Question 1',
            'easyIntegerTypeSol1':'Easy Integer Type Solution 1',
            'easyIntegerTypeSol2':'Easy Integer Type Solution 2',
            'mediumIntegerTypeSol1':'Medium Integer Type Solution 1',
            'mediumIntegerTypeSol2':'Medium Integer Type Solution 2',
            'hardIntegerTypeSol1':'Hard Integer Type Solution 1',
            'duration':'Duration in minutes',
            'twinConcepts':'Twin Concepts',
            'videoUrl':'Video URL',
            'targetExam':'Target Exam',

            'wowTheory':'Wow Theory',
            'wowQues':'Wow Question',
            'wowReason':'Wow Reason',
        }

# class PaperForm(ModelForm):
#     class Meta:
#         model=Paper
#         exclude=["userId","chapter"]
TRICKY_CHOICES=(("YES","YES"),("NO","NO"))
class QuesTagForm(Form):
    def __init__(self, *args, **kwargs):
        self.n = kwargs.pop('n')
        self.chapter=kwargs.pop('chapter')
        super().__init__(*args, **kwargs)
        for i in range(1,self.n+1):
            DIFFICULTY_CHOICES=((i,i) for i in range(1,6))
            CONCEPT_CHOICES = [("","-------")]
            CONCEPT_CHOICES.extend([(i.pk,i.name) for i in self.chapter.concepts.all()])
            CONCEPT_CHOICES = tuple(CONCEPT_CHOICES)
            ERROR_CHOICES=(("NO","NO"),("YES","YES"))
            self.fields['error'+str(i)]=forms.ChoiceField(choices=ERROR_CHOICES,label="Error")
            self.fields['diff'+str(i)] = forms.ChoiceField(choices=DIFFICULTY_CHOICES,required=False,label="Difficulty")
            self.fields['concept'+str(i)]=forms.ChoiceField(choices=CONCEPT_CHOICES,required=False,label="Concepts")
            self.fields['subConcept'+str(i)]=forms.ChoiceField(required=False,label="Subconcepts")
            self.fields['conceptHidden'+str(i)]=forms.CharField(widget=forms.HiddenInput(),required=False)
            self.fields['subConceptHidden'+str(i)]=forms.CharField(widget=forms.HiddenInput(),required=False)
            self.fields['rough'+str(i)]=forms.CharField(widget=forms.HiddenInput(),required=False)
            
            
class CrossConceptForm(Form):
    def __init__(self, *args, **kwargs):
        self.n1 = kwargs.pop('n1')
        self.n2 = kwargs.pop('n2')
        super().__init__(*args, **kwargs)
        for i in range(1,self.n1+1):
            self.fields['q'+str(i)] = forms.CharField(widget=CKEditorUploadingWidget,required=False,label="Multiple Choice Question"+str(i))
            self.fields['a'+str(i)] = forms.CharField(required=False,label="Answer")
            self.fields['concept'+str(i)] = forms.CharField(widget=forms.HiddenInput(),label="concept",required=False)
            self.fields['subconcept'+str(i)] = forms.CharField(widget=forms.HiddenInput(),label="subconcept",required=False)
        for i in range(self.n1+1,self.n1+self.n2+1):
            self.fields['q'+str(i)] = forms.CharField(widget=CKEditorUploadingWidget,required=False,label="Integer Question"+str(i-self.n1))
            self.fields['a'+str(i)] = forms.IntegerField(required=False,label="Answer")
            self.fields['concept'+str(i)] = forms.CharField(widget=forms.HiddenInput(),label="concept",required=False)
            self.fields['subconcept'+str(i)] = forms.CharField(widget=forms.HiddenInput(),label="subconcept",required=False)

