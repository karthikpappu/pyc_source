# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/anders/work/python/teachrecovery/quizblock_random/views.py
# Compiled at: 2015-01-05 09:47:29
from models import Quiz, Question, QuizRandom
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from quizblock.models import Answer

class EditQuizRandomView(DetailView):
    model = QuizRandom


class DeleteQuestionRandomView(DeleteView):
    model = Question

    def get_success_url(self):
        quiz = self.object.quiz
        return reverse('edit-quiz-random', args=[quiz.id])


class DeleteAnswerRandomView(DeleteView):
    model = Answer

    def get_success_url(self):
        question = self.object.question
        return reverse('edit-question-random', args=[question.id])


class ReorderItemsView(View):

    def post(self, request, pk):
        parent = get_object_or_404(self.parent_model, pk=pk)
        keys = [ k for k in request.GET.keys() if k.startswith(self.prefix)
               ]
        keys.sort(key=lambda x: int(x.split('_')[1]))
        items = [ int(request.GET[k]) for k in keys if k.startswith(self.prefix)
                ]
        self.update_order(parent, items)
        return HttpResponse('ok')


class ReorderAnswersView(ReorderItemsView):
    parent_model = Question
    prefix = 'answer_'

    def update_order(self, parent, items):
        parent.update_answers_order(items)


class ReorderQuestionsView(ReorderItemsView):
    parent_model = Quiz
    prefix = 'question_'

    def update_order(self, parent, items):
        parent.update_questions_order(items)


class AddQuestionToQuizRandomView(View):

    def post(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        form = quiz.add_question_form(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
        return HttpResponseRedirect(reverse('edit-quiz-random', args=[quiz.id]))


class EditQuestionRandomView(View):
    template_name = 'quizblock_random/edit_question.html'

    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        return render(request, self.template_name, dict(question=question, answer_form=question.add_answer_form()))

    def post(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        form = question.edit_form(request.POST)
        question = form.save(commit=False)
        question.save()
        return HttpResponseRedirect(reverse('edit-question-random', args=[
         question.id]))


class AddAnswerToQuestionRandomView(View):
    template_name = 'quizblock_random/edit_question.html'

    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        form = question.add_answer_form()
        return render(request, self.template_name, dict(question=question, answer_form=form))

    def post(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        form = question.add_answer_form(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            if answer.label == '':
                answer.label = answer.value
            answer.save()
            return HttpResponseRedirect(reverse('edit-question-random', args=[
             question.id]))
        return render(request, self.template_name, dict(question=question, answer_form=form))


class EditAnswerRandomView(View):
    template_name = 'quizblock_random/edit_answer.html'

    def get(self, request, pk):
        answer = get_object_or_404(Answer, pk=pk)
        form = answer.edit_form()
        return render(request, self.template_name, dict(answer_form=form, answer=answer))

    def post(self, request, pk):
        answer = get_object_or_404(Answer, pk=pk)
        form = answer.edit_form(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.save()
            return HttpResponseRedirect(reverse('edit-answer-random', args=[
             answer.id]))
        return render(request, self.template_name, dict(answer_form=form, answer=answer))