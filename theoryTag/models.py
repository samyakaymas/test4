from django.db import models
from django.core.validators import RegexValidator
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse

class Subject(models.Model):
    name = models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.name

class Chapter(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject,related_name="chapters",on_delete=models.CASCADE)
    class Meta:
        unique_together=('name','subject')
    def __str__(self):
        return self.name

class Concept(models.Model):
    name = models.CharField(max_length=100)
    chapter = models.ForeignKey(Chapter,related_name="concepts",on_delete=models.CASCADE)
    class Meta:
        unique_together=('name','chapter')
    def __str__(self):
        return self.name

class SubConcept(models.Model):
    name = models.CharField(max_length=100)
    concept = models.ForeignKey(Concept,related_name="subConcepts",on_delete=models.CASCADE)
    class Meta:
        unique_together=('name','concept')
    def __str__(self):
        return self.name
    def isTheory(self):
        return bool(len(self.Theory.all()))
    def get_theory_add_url(self):
        return reverse('add', kwargs={'subConceptId': self.pk})
    def get_theory_update_url(self):
        return reverse('theory-update',kwargs={'pk':self.Theory.all()[0].pk})
    def get_theory_view_url(self):
        return reverse('theory-details', kwargs={'pk': self.Theory.all()[0].pk})
DURATION_CHOICES=((i,i) for i in range(15,121,15))
DIFFICULTY_CHOICES=((i,i) for i in range(1,6))
IMPORTANCE_CHOICES=((i,i) for i in range(1,6))
TRICKY_CHOICES=(("YES","YES"),("NO","NO"))
TARGET_EXAM_CHOICES=TARGET_EXAM=(("IIT","IIT"),("NEET","NEET"))

class Theory(models.Model):
    userId=models.IntegerField(blank=True,null=True)
    subConcept=models.ForeignKey(SubConcept,related_name="Theory",on_delete=models.CASCADE)
    
    theory = RichTextUploadingField(null=True, blank=True)
    easyExampleQues1=RichTextUploadingField(null=True, blank=True)
    easyExampleSol1=RichTextUploadingField(null=True, blank=True)
    easyExampleQues2=RichTextUploadingField(null=True, blank=True)
    easyExampleSol2=RichTextUploadingField(null=True, blank=True)
    easyExampleQues3=RichTextUploadingField(null=True, blank=True)
    easyExampleSol3=RichTextUploadingField(null=True, blank=True)
    easyExampleQues4=RichTextUploadingField(null=True, blank=True)
    easyExampleSol4=RichTextUploadingField(null=True, blank=True)
    easyExampleQues5=RichTextUploadingField(null=True, blank=True)
    easyExampleSol5=RichTextUploadingField(null=True, blank=True)
    easyExampleQues6=RichTextUploadingField(null=True, blank=True)
    easyExampleSol6=RichTextUploadingField(null=True, blank=True)
    easyExampleQues7=RichTextUploadingField(null=True, blank=True)
    easyExampleSol7=RichTextUploadingField(null=True, blank=True)
    


    mediumExampleQues1=RichTextUploadingField(null=True, blank=True)
    mediumExampleSol1=RichTextUploadingField(null=True, blank=True)
    mediumExampleQues2=RichTextUploadingField(null=True, blank=True)
    mediumExampleSol2=RichTextUploadingField(null=True, blank=True)
    mediumExampleQues3=RichTextUploadingField(null=True, blank=True)
    mediumExampleSol3=RichTextUploadingField(null=True, blank=True)
    mediumExampleQues4=RichTextUploadingField(null=True, blank=True)
    mediumExampleSol4=RichTextUploadingField(null=True, blank=True)
    mediumExampleQues5=RichTextUploadingField(null=True, blank=True)
    mediumExampleSol5=RichTextUploadingField(null=True, blank=True)
    mediumExampleQues6=RichTextUploadingField(null=True, blank=True)
    mediumExampleSol6=RichTextUploadingField(null=True, blank=True)
    mediumExampleQues7=RichTextUploadingField(null=True, blank=True)
    mediumExampleSol7=RichTextUploadingField(null=True, blank=True)
    

    
    hardExampleQues1=RichTextUploadingField(null=True, blank=True)
    hardExampleSol1=RichTextUploadingField(null=True, blank=True)
    hardExampleQues2=RichTextUploadingField(null=True, blank=True)
    hardExampleSol2=RichTextUploadingField(null=True, blank=True)
    hardExampleQues3=RichTextUploadingField(null=True, blank=True)
    hardExampleSol3=RichTextUploadingField(null=True, blank=True)
    hardExampleQues4=RichTextUploadingField(null=True, blank=True)
    hardExampleSol4=RichTextUploadingField(null=True, blank=True)
    hardExampleQues5=RichTextUploadingField(null=True, blank=True)
    hardExampleSol5=RichTextUploadingField(null=True, blank=True)
    hardExampleQues6=RichTextUploadingField(null=True, blank=True)
    hardExampleSol6=RichTextUploadingField(null=True, blank=True)
    
    easyIntegerTypeQues1=RichTextUploadingField(null=True, blank=True)
    easyIntegerTypeSol1=RichTextUploadingField(null=True, blank=True)
    easyIntegerTypeQues2=RichTextUploadingField(null=True, blank=True)
    easyIntegerTypeSol2=RichTextUploadingField(null=True, blank=True)

    mediumIntegerTypeQues1=RichTextUploadingField(null=True, blank=True)
    mediumIntegerTypeSol1=RichTextUploadingField(null=True, blank=True)
    mediumIntegerTypeQues2=RichTextUploadingField(null=True, blank=True)
    mediumIntegerTypeSol2=RichTextUploadingField(null=True, blank=True)

    hardIntegerTypeQues1=RichTextUploadingField(null=True, blank=True)
    hardIntegerTypeSol1=RichTextUploadingField(null=True, blank=True)


    difficulty=models.IntegerField(null=False,choices=DIFFICULTY_CHOICES,default=1)
    importance=models.IntegerField(null=False,choices=IMPORTANCE_CHOICES,default=1)

    duration=models.IntegerField(null=False)
    prerequisites=models.ManyToManyField(SubConcept,related_name="prerequisiteOf",blank=True)
    summary=RichTextUploadingField(null=True, blank=True)
    mnemonics=RichTextUploadingField(null=True, blank=True)
    twinConcepts=models.ManyToManyField(SubConcept,related_name="twinConceptOf",blank=True)
    videoUrl=models.URLField(max_length=200, null=False)
    targetExam=models.CharField(max_length=100,null=False,choices=TARGET_EXAM_CHOICES)
    
    wowTheory=RichTextUploadingField(blank=True)
    wowQues=RichTextUploadingField(blank=True)
    wowReason=RichTextUploadingField(blank=True)
    def get_absolute_url(self):
        return reverse('theory-details', kwargs={'pk': self.pk})
    def get_update_url(self):
        return reverse('theory-update',kwargs={'pk':self.pk})

DIFFICULTY_CHOICES1=((i,i) for i in range(1,6))
ERROR_CHOICES=(("NO","NO"),("YES","YES"))
class Ques(models.Model):
    chapter=models.ForeignKey(Chapter,related_name="Ques",on_delete=models.CASCADE)
    ques=RichTextUploadingField()
    ans=RichTextUploadingField()
    difficulty=models.IntegerField(null=False,choices=DIFFICULTY_CHOICES1,default=0)
    subConcept=models.ManyToManyField(SubConcept,related_name="questions",blank=True)
    error=models.CharField(max_length=30,null=False,choices=ERROR_CHOICES,default="NO")
    rated=models.BooleanField(default=False)
    def get_absolute_url(self):
        return reverse('list-ques')
    def get_update_url(self):
        return reverse('ques-update',kwargs={'pk':self.pk})
# class Paper(models.Model):
#     easyPaperQues=RichTextUploadingField(null=True,blank=True)
#     easyPaperSol=RichTextUploadingField(null=True,blank=True)
#     mediumPaperQues=RichTextUploadingField(null=True,blank=True)
#     mediumPaperSol=RichTextUploadingField(null=True,blank=True)
#     hardPaperQues=RichTextUploadingField(null=True,blank=True)
#     hardPaperSol=RichTextUploadingField(null=True,blank=True)
#     chapter=models.ForeignKey(Chapter,related_name="Paper",on_delete=models.CASCADE)
#     userId=models.IntegerField(blank=True,null=True)
#     def get_absolute_url(self):
#         return reverse('paper-list')
#     def get_update_url(self):
#         print(24141414114       )
#         return reverse('paper-update',kwargs={'pk':self.pk})

class CrossConcept(models.Model):
    userId = models.IntegerField(blank=True,null=True)
    question_no = models.IntegerField(blank=True,null=True)
    question = RichTextUploadingField(null=True,blank=True)
    answer = RichTextUploadingField(null=True,blank=True)
    subconcepts=models.ManyToManyField(SubConcept,related_name="subconceptsof",blank=True)
    class Meta:
        unique_together = (("userId", "question_no"))

