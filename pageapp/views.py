from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView, FormView
from django.views.generic.base import View
from .models import Article
from django.utils import timezone
from .form import ContactForm, ArticleForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic.dates import YearArchiveView, MonthArchiveView, WeekArchiveView, DayArchiveView, \
    TodayArchiveView
import csv
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date
from django.core.mail import send_mail
from rest_framework import generics
from .serializers import *
from rest_framework import permissions
from rest_framework import viewsets


class ArticleAPIView(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Article.objects.all()
    serializer_class = ArticleModelSerializer


#class ArticleListAPIView(generics.ListCreateAPIView):
#    queryset = Article.objects.all()
#    serializer_class = ArticleModelSerializer


#class ArticleUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
#    permission_classes = (permissions.IsAdminUser,)
#    queryset = Article.objects.all()
#    serializer_class = ArticleModelSerializer


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'pageapp/article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class ArticleListView(ListView):
    model = Article
    template_name = 'pageapp/articlelist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


# class ContactView(FormView):
#    template_name = 'pageapp/contact.html'
#    form_class = ContactForm
#    success_url = '/thanks/'

#    def form_valid(self, form):
#        form.send_email()
#        super().form_valid(form)


class CreateArticle(SuccessMessageMixin, CreateView):
    model = Article
    form_class = ArticleForm
    # fields = '__all__'
    template_name = 'pageapp/article-create.html'
    success_message = 'Article was added successfully'


class UpdateArticle(SuccessMessageMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    # fields = ['headline', 'content']
    template_name_suffix = '_update_form'
    success_message = 'Article was updated successfully'


class DeleteArticle(SuccessMessageMixin, DeleteView):
    model = Article
    template_name = 'pageapp/article_delete.html'
    success_url = reverse_lazy('article-list')
    success_message = 'Article was deleted successfully'


class ArticleYearArchive(YearArchiveView):
    template_name = 'pageapp/article_year.html'
    queryset = Article.objects.all()
    date_field = 'pub_date'
    make_object_list = True
    allow_future = True


class ArticleMonthArchive(MonthArchiveView):
    template_name = 'pageapp/article_month.html'
    queryset = Article.objects.all()
    date_field = 'pub_date'
    allow_future = True


class ArticleWeekArchive(WeekArchiveView):
    template_name = 'pageapp/article_week.html'
    queryset = Article.objects.all()
    date_field = 'pub_date'
    week_format = "%W"
    allow_future = True


class ArticleDayArchive(DayArchiveView):
    template_name = 'pageapp/article_day.html'
    queryset = Article.objects.all()
    date_field = 'pub_date'


def get_name(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']
            recipients = ['zayerwali12@gmail.com']
            if cc_myself:
                recipients.append(sender)
                send_mail(subject, message, sender, recipients)
            return HttpResponseRedirect('/thanks/')
    else:
        form = ContactForm()
        return render(request, 'pageapp/article_form.html', {'form': form})


class CSVGenerate(View):

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="articles.csv"'
        writer = csv.writer(response)
        writer.writerow(['headline', 'content', 'pub_date', 'article_created', 'modified_on'])
        articles = Article.objects.all()
        for art in articles:
            print(art.article_created.strftime("%Y-%m-%d %H:%M"))
            print(art.article_created.strftime("%b/%d/%Y %H:%M"))
            writer.writerow([art.headline, art.content, art.pub_date, art.article_created.strftime("%b/%d/%Y %H:%M"),
                             art.modified_on.strftime("%b/%d/%Y %H:%M")])
        return response


class CSVToday(View):

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="articlestoday.csv"'
        writer = csv.writer(response)
        writer.writerow(['headline', 'content', 'pub_date', 'article_created', 'modified_on'])
        today = date.today()
        articles = Article.objects.filter(article_created__date=today)
        for art in articles:
            writer.writerow([art.headline, art.content, art.pub_date, art.article_created.strftime("%b/%d/%Y %H:%M"),
                             art.modified_on.strftime("%b/%d/%Y %H:%M")])
        return response
