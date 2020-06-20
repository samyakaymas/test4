from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from . import views

urlpatterns=[

    path('',login_required(TemplateView.as_view(template_name="home.html"))),
    path("add/<int:subConceptId>",login_required(views.TheoryCreateView.as_view()),name="add"),
    path("ajax/load/subConcepts",views.loadSubConcepts,name="ajaxLoadSubConcepts"),
    path("ajax/load/subConcepts1",views.loadSubConcepts1,name="ajaxLoadSubConcepts1"),
    path("cross/",views.Cross,name="cross"),
    path("crossview/",views.CrossView,name="crossview"),
    # path("",views.index,name="index"),
    path("ajax/load/chapters",views.loadChapters,name="ajaxLoadChapters"),
    path("ajax/load/concepts",views.loadConcepts,name="ajaxLoadConcepts"),
    # path("addPaper",views.PaperCreateView.as_view(),name="paper-add"),
    # path("paperList",views.PaperListView.as_view(),name="paper-list"),
    # path("paperUpdate/<int:pk>",views.PaperUpdateView.as_view(),name="paper-update"),
    path('show/<int:pk>', login_required(views.TheoryDetailView.as_view()), name='theory-details'),
    path('update/<int:pk>',login_required(views.TheoryUpdateView.as_view()), name='theory-update'),
    path('QuesTag',views.QuesTagUpdate,name='Ques-Tag'),
    path('quesview/',views.QuesTagView,name='quesview'),
    # path('showQues',views.QuesListView.as_view(),name='list-ques' ),
    # path('quesUpdate/<int:pk>',views.QuesUpdateView.as_view(), name='ques-update'),
    path('showTheory',login_required(views.TheoryListView.as_view()), name='theory-list'),
    path('subConceptName',views.loadSubConceptName,name='subConcept-Name'),
]