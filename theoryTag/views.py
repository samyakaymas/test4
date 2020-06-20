from django.shortcuts import render, redirect , reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import ListView,CreateView, UpdateView,DetailView
from .models import *
from .forms import *
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

class TheoryCreateView(CreateView):
    def get(self,request, *args, **kwargs):
        if not request.user.can_add_theory:
            return render(request,"theoryTag/401.html")
        return super().get(request, *args, **kwargs)
    model=Theory
    form_class=TheoryTagForm
    success_url='/theory/showTheory'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject']=get_user_model().objects.get(pk=self.request.user.id).subject.name
        context['chapter']=Chapter.objects.get(pk=get_user_model().objects.get(pk=self.request.user.id).chapter.id).name
        return super().get_context_data(**kwargs)
    def form_valid(self, form):
        userId=self.request.user.id
        self.object = form.save(commit=False)
        print(form.cleaned_data["prerequisiteHiddenField"].split(","))
        l=[int(i) for i in form.cleaned_data["prerequisiteHiddenField"].split(",") if len(i)>0]
        l1=[int(i) for i in form.cleaned_data["twinConceptprerequisiteHiddenField"].split(",") if len(i)>0]
        prerequisites=SubConcept.objects.filter(pk__in=l)
        twinConcepts=SubConcept.objects.filter(pk__in=l1)

        print(self.kwargs.get('subConceptId'))
        self.object.subConcept=SubConcept.objects.get(pk=self.kwargs.get('subConceptId'))
        self.object.userId = userId
        self.object.save()
        self.object.prerequisites.set(prerequisites)
        self.object.twinConcepts.set(twinConcepts)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class TheoryListView(ListView):
    def get(self,request, *args, **kwargs):
        if not request.user.can_see_theory:
            return render(request,"theoryTag/401.html")
        return super().get(request, *args, **kwargs)
    model=Theory
    def get_queryset(self):
        userId = self.request.user.id
        print(userId)
        return Theory.objects.filter(userId=userId)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        userChapter=Chapter.objects.get(pk=get_user_model().objects.get(pk=self.request.user.id).chapter.id)
        context['chapter']=userChapter
        return context

class TheoryDetailView(DetailView):
    def get(self,request, *args, **kwargs):
        if not request.user.can_see_theory:
            return render(request,"theoryTag/401.html")
        return super().get(request, *args, **kwargs)
    model = Theory

class TheoryUpdateView(UpdateView):
    def get(self,request, *args, **kwargs):
        if not request.user.can_edit_theory:
            return render(request,"theoryTag/401.html")
        return super().get(request, *args, **kwargs)
    model = Theory
    form_class=TheoryTagForm
    pk_url_kwarg = 'pk'
    success_url = '/theory/showTheory'
    def form_valid(self, form):
        self.object = form.save(commit=False)
        l=[int(i) for i in form.cleaned_data["prerequisiteHiddenField"].split(",") if len(i)>0]
        l1=[int(i) for i in form.cleaned_data["twinConceptprerequisiteHiddenField"].split(",") if len(i)>0]
        prerequisites=SubConcept.objects.filter(pk__in=l)
        twinConcepts=SubConcept.objects.filter(pk__in=l1)
        self.object.prerequisites.set(prerequisites)
        self.object.twinConcepts.set(twinConcepts)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
  
class QuesUpdateView(UpdateView):
    model = Ques
    form_class = QuesTagForm
    pk_url_kwarg = 'pk'
    success_url = '/theory/showQues'
    def form_valid(self, form):
        self.object=form.save(commit=False)
        self.object.rated=True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

@login_required()
def QuesTagUpdate(request):
    if not request.user.can_add_tag:
        return render(request,"theoryTag/401.html")
    userChapter=Chapter.objects.get(pk=get_user_model().objects.get(pk=request.user.id).chapter.id)
    if request.method=="POST":
        form = QuesTagForm(request.POST,n=len(userChapter.Ques.all()),chapter=userChapter)
        form.is_valid()
        questions=userChapter.Ques.all()
        for i in range(1,form.n+1):
            obj=Ques.objects.get(pk=questions[i-1].pk)
            obj.difficulty=form.cleaned_data.get("diff"+str(i))
            obj.error=form.cleaned_data.get("error"+str(i))
            l=[int(i) for i in form.cleaned_data.get("subConceptHidden"+str(i)).split(",") if len(i)>0]
            subConcept=SubConcept.objects.filter(pk__in=l)
            print(subConcept)
            obj.subConcept.set(subConcept)  
            obj.save()
        return redirect('/theory')
    i=0
    context={}
    questions=[]
    answers=[]
    for ques in userChapter.Ques.all():
        i+=1
        questions.append(ques.ques)
        answers.append(ques.ans)
        context['diff'+str(i)]=ques.difficulty
        context['error'+str(i)]=ques.error
        context['subConceptHidden'+str(i)]=','.join([str(i.pk) for i in ques.subConcept.all()])
        context['conceptHidden'+str(i)]=','.join([str(i.name) for i in ques.subConcept.all()])
    form = QuesTagForm(n=i,chapter=userChapter,initial=context)
    return render(request,'theoryTag/QuesTag.html',{'form':form,'n':i,'ques':questions,'ans':answers})

@login_required()
def loadSubConcepts1(request):
    conceptId = request.GET.get('concept')
    subConcepts=SubConcept.objects.filter(concept=Concept.objects.get(pk=conceptId))
    return render(request,"theoryTag/sub_concept_dropdown_list1.html",{'subConcepts':subConcepts})
# class PaperCreateView(CreateView):
#     model=Paper
#     form_class=PaperForm
#     success_url='paperList'
#     def form_valid(self, form):
#         userChapter=get_user_model().objects.get(pk=self.request.user.id).chapter.id
#         self.object=form.save(commit=False)
#         self.object.userId=self.request.user.id
#         self.object.chapter=Chapter.objects.get(pk=userChapter)
#         self.object.save()
#         return HttpResponseRedirect(self.get_success_url())
# class PaperListView(ListView):
#     model = Paper
# class PaperUpdateView(UpdateView):
#     model = Paper
#     form_class=PaperForm
#     pk_url_kwarg='pk'
#     success_url='paperList'

@login_required()
def CrossView(request):
    if not request.user.can_see_cross:
        return render(request,"theoryTag/401.html")
    userId = request.user.id
    cross = CrossConcept.objects.filter(userId=userId)
    return render(request,"theoryTag/crossview.html",context={'cross':cross})

@login_required()
def QuesTagView(request):
    if not request.user.can_see_tag:
        return render(request,"theoryTag/401.html")
    userId = request.user.id
    userChapter = get_user_model().objects.get(pk=userId).chapter
    ques = userChapter.Ques.all()
    return render(request,"theoryTag/questagview.html",context={'ques':ques})

@login_required()
def Cross(request):
    if not request.user.can_add_cross:
        return render(request,"theoryTag/401.html")
    userId = request.user.id
    userChapter = get_user_model().objects.get(pk=userId).chapter
    concepts = Concept.objects.filter(chapter=userChapter)
    conceptsid = [concept.id for concept in concepts]
    subconcepts = SubConcept.objects.filter(concept__in=conceptsid)
    n1 = max(1,len(subconcepts)//5)
    n2 = max(1,len(subconcepts)//20)
    if request.method=="POST":
        form = CrossConceptForm(request.POST,n1=n1,n2=n2)
        if form.is_valid():
            for i in range(1,form.n1+1):
                try:
                    quest = CrossConcept.objects.get(userId=userId,question_no=i)
                except ObjectDoesNotExist :
                    quest = CrossConcept()
                    quest.question_no = i
                    quest.userId = userId
                quest.question = form.cleaned_data.get('q'+str(i))
                quest.answer = form.cleaned_data.get('a'+str(i))
                quest.save()
                subconceptsids = [int(j) for j in form.cleaned_data["subconcept"+str(i)].split(",") if len(j)>0]
                subcs = SubConcept.objects.filter(pk__in=subconceptsids)
                quest.subconcepts.set(subcs)
                quest.save()
            for i in range(form.n1+1,form.n1+form.n2+1):
                try:
                    quest = CrossConcept.objects.get(userId=userId,question_no=i)
                except ObjectDoesNotExist:
                    quest = CrossConcept()
                    quest.question_no = i
                    quest.userId = userId
                quest.question = form.cleaned_data.get('q'+str(i))
                if form.cleaned_data.get('a'+str(i)) is not None:
                    quest.answer = str(form.cleaned_data.get('a'+str(i)))
                quest.save()
                subconceptsids = [int(j) for j in form.cleaned_data["subconcept"+str(i)].split(",") if len(j)>0]
                subcs = SubConcept.objects.filter(pk__in=subconceptsids)
                quest.subconcepts.set(subcs)
                quest.save()
        return redirect('/theory/cross')
    
    context = {}
    quests = CrossConcept.objects.filter(userId=userId)
    for obj in quests:
        i = obj.question_no
        context['q'+str(i)] = obj.question
        if i>n1:
            if obj.answer != None:
                context['a'+str(i)] = int(obj.answer)
                pass
            print(obj.answer)
        else:
            context['a'+str(i)] = obj.answer
        context['subconcept'+str(i)] = ",".join([str(s.id) for s in obj.subconcepts.all()])+","
    form = CrossConceptForm(n1=n1,n2=n2,initial=context)
    return render(request,'theoryTag/n_ques_form.html',{'form':form,'concepts':concepts,'subconcepts':subconcepts, 'quests':quests})

@login_required()
def loadSubConcepts(request):
    conceptId = request.GET.get('concept')
    subConcepts=SubConcept.objects.filter(concept=Concept.objects.get(pk=conceptId))
    return render(request,"theoryTag/sub_concept_dropdown_list.html",{'subConcepts':subConcepts})

@login_required()
def loadConcepts(request):
    userChapter=get_user_model().objects.get(pk=request.user.id).chapter.id
    chapterId = request.GET.get('chapter',userChapter)
    concepts=Concept.objects.filter(chapter=Chapter.objects.get(pk=chapterId))
    return render(request,"theoryTag/concept_dropdown_list.html",{'concepts':concepts})

@login_required()
def loadSubConceptName(request):
    subConceptId=request.GET.get('subConcept')
    subConcept=SubConcept.objects.get(pk=subConceptId)
    data={"subConceptName":subConcept.name}
    return JsonResponse(data)

@login_required()
def loadChapters(request):
    subjectId=request.GET.get('subject')
    subject=Subject.objects.get(pk=subjectId)
    return render(request,"theoryTag/chapter_dropdown_list.html",{"chapters":subject.chapters.all()})