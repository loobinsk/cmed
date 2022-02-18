# -*- coding: utf-8 -*-
import logging
import os
import random
import string

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.middleware.csrf import get_token
from PIL import Image
from django.conf import settings

from library.models import Graduate, Title, School
from medtus.models import Specialities, Countries, Towns
from account.models import Category, Aword


logger = logging.getLogger(__name__)
size = 128, 128


class PictureForm(forms.Form):
    avatar = forms.FileField(label='Select a file')


class RegisterStep3Form(forms.ModelForm):
    proper_requests = {
        'question1': '2',
        'question2': '3',
        'question3': '2',
        'question4': '2',
        'question5': '2',
        'question6': '5',
        'question7': '4',
        'question8': '2',
        'question9': '1',
        'question10': '4',
        'question11': '5',
        'question12': '2',
        'question13': '5',
        'question14': '3',
    }
    error = ''

    questions_count = 1

    def render(self, request):
        csrf_token_value = get_token(request)

        questions = self.proper_requests.keys()
        random.shuffle(questions)

        return render_to_string("account/forms/registerformstep3.html",{
                                    'csrf_token_value': csrf_token_value,
                                    'error': self.error,
                                    'questions': questions[:self.questions_count]
                                })

    def is_valid(self, request):
        result = True
        correct_answers = 0
        for k, v in self.proper_requests.iteritems():
            if k in self.data:
                if v == self.data[k]:
                    correct_answers += 1

        if correct_answers != self.questions_count:
            self.error = u'<span class="inform-error form-errors" style="display: block;">Вы неправильно ответили на вопросы!!!</span>'
            result = False

        return result

    class Meta:
        model = User
        fields = []


class RegisterStep2Form(forms.ModelForm):
    mandatory_fields = {'surname': u'Поле Имя не заполнено', 'firstname': u'Поле Отчество не заполнено',
                        'lastname': u'Поле Фамилия не заполнено',
                        'spec_id': u'Поле Основная специальность не заполнено', 'country': u'Поле Страна не заполнено',
                        'town': u'Поле Город не заполнено', 'organization': u'Поле организация не заполнено'}
    allfields = {'surname': '', 'firstname': '', 'lastname': '', 'avatar': '', 'sex': '', 'birthday': '', 'spec_id': '',
                 'experience': '', 'addspeciality': '', 'addexperience': '', 'graduate': '', 'dissertation': '',
                 'title': '', 'addtitle': '', 'category': '', 'awords': '', 'organization': '', 'job': '', 'site': '',
                 'school': '', 'graduate_year': '', 'faculty': '', 'cathedra': '', 'country': '', 'town': '',
                 'phone_number': '', 'phone_visible': '', 'ICQ_Skype': '', 'social': '', 'no_found_school': ''}
    error = ""

    def handle_uploaded_file(self, f):
        try:
            path = os.path.join(settings.MEDIA_ROOT, 'profile_images')
            logger.log(logging.DEBUG, u'media/profile_images/{0}'.format(f.name))
            try:
                fileName, fileExtension = os.path.splitext(f.name.encode("ascii"))
            except:
                fileName, fileExtension = os.path.splitext(f.name)
            fname = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
            fname = fname + fileExtension
            with open(os.path.join(path, fname), 'wb+') as destination:
                logger.log(logging.DEBUG, os.path.join(path, fname))
                for chunk in f.chunks():
                    destination.write(chunk)
            outfile = os.path.join(path, u'thumb_{0}'.format(fname))
            im = Image.open(os.path.join(path, fname))
            im.thumbnail(size)
            im.save(outfile, "JPEG")
            return fname
        except:
            return False

    def is_valid(self, request):
        if not self.mandatory_valid():
            return False

        sex_field = forms.CharField(required=False)
        try:
            sex_field.clean(self.data.get('sex'))
        except ValidationError:
            self.error = u'<span class="inform-error form-errors" style="display: block;">Пол указан неверно</span>'
            return False


        df = forms.DateField(required=False, input_formats=['%d %m %Y'])
        try:
            df.clean(self.data['birthday'])
        except:
            self.error = u'<span class="inform-error form-errors" style="display: block;">Дата рождения введена неверно</span>'
            return False



        self.readfields()
        if 'phone_visible' in self.data:
            self.allfields['phone_visible'] = 'no_visible'
        else:
            self.allfields['phone_visible'] = 'visible'
        if 'avatar' in request.FILES:
            picture_form = PictureForm(request.POST, request.FILES)
            if picture_form.is_valid():
                file_uploaded = self.handle_uploaded_file(request.FILES['avatar'])
                if file_uploaded:
                    self.allfields['avatar'] = u'profile_images/{0}'.format(file_uploaded)
                else:
                    self.error = u'<span class="inform-error form-errors" style="display: block;">При загрузке картинки произошла ошибка</span>'
                    return False
            else:
                self.error = u'<span class="inform-error form-errors" style="display: block;">{0}</span>'.format(
                    picture_form.errors)
                return False
        for k, v in self.allfields.iteritems():
            request.session[k] = v
        return True

    def readfields(self):
        for k, v in self.allfields.iteritems():
            if k in self.data:
                self.allfields[k] = self.data[k]
            else:
                self.allfields[k] = ''

    def getTown(self, country):
        return Towns.objects.filter(country_id__name=country)

    def mandatory_valid(self):
        cf = forms.CharField()
        for k, v in self.mandatory_fields.iteritems():
            try:
                cf.clean(self.data[k])
                if self.data[k] == '0':
                    raise
            except:
                self.error = u'<span class="inform-error form-errors" style="display: block;">' + v + '</span>'
                return False
        return True

    def render(self, request):
        csrf_token_value = get_token(request)
        if request.session.get('country'):
            country = request.session.get('country')
        else:
            request.session['country'] = 0
            country = 0
        template_key_value = {'csrf_token_value': csrf_token_value,
                              'spec_list': Specialities.objects.all().order_by('name'),
                              'addspeciality_list': Specialities.objects.all().order_by('name'),
                              'graduate_list': Graduate.objects.all(),
                              'title_list': Title.objects.all(),
                              'school_list': School.objects.all(),
                              'country_list': Countries.objects.all(),
                              'category_list': Category.objects.all(),
                              'awords_list': Aword.objects.all(),
                              'town_list': Towns.objects.filter(country_id=country), 'error': self.error}
        for k, v in self.allfields.iteritems():
            if request.session.get(k):
                template_key_value[k] = request.session.get(k, '')

        return render_to_string("account/forms/registerformstep2.html", template_key_value)

    class Meta:
        model = User
        fields = []


class RegisterStep1Form(forms.ModelForm):
    username = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter a password.")
    agreed = forms.CheckboxInput()    
    error = ''

    def render(self, request):
        csrf_token_value = get_token(request)
        return render_to_string("account/forms/registerformstep1.html",
                                {'csrf_token_value': csrf_token_value, 'error_placeholder': self.error})

    def pass_valid(self, password):
        import re
        #p = re.compile()
        if re.search(ur'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d\w\W]{8,}$', password) is None:
            self.error = u'<span class="inform-error">Пароль должен содержать не менее 8 символов<br>(большие и маленькие буквы и цифры)</span>'+password
            return False

        return True


    def is_valid(self, request):
        ef = forms.EmailField()
        try:
            ef.clean(self.data['email'])
        except:
            self.error = u'<span class="inform-error">Электронный адрес введен неверно!!!</span>'
            return False

        from account.models import MyUser
        if MyUser.objects.filter(email=self.data['email']).exists():
            self.error = u'<span class="inform-error">Такой электронный адрес уже существует!!!<br/>'
            self.error = self.error + u'<a href="/account/forgot/">Восстановить пароль</a></span>'
            return False

        if not self.pass_valid(self.data['password']):
            return False
        if self.data['password'] != self.data['confirm']:
            self.error = u'<span class="inform-error">Введенные пароли не совпадают!!!</span>'
            return False


        if not self.data.get('agreed', False):
            self.error = u'<span class="inform-error">Необходимо согласие с правилами сайта!!!</span>'
            return False

        if not self.data.get('pd_agreed', False):
            self.error = u'<span class="inform-error">Необходимо согласие на обработку персональных данных!!!</span>'
            return False

        request.session['email'] = self.data['email']
        request.session['password'] = self.data['password']
        request.session['confirm'] = self.data['confirm']
        return True

    class Meta:
        model = User
        fields = []

