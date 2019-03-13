from django.shortcuts import render

# Create your views here.
template_index = 'challenge/index.html'

def index(request, template=template_index):
	
	context = {}
	return render(request, template, context)


#https://wsvincent.com/django-user-authentication-tutorial-signup/
#Why use reverse_lazy instead of reverse I hope you’re asking? 
#The reason is that for all generic class-based views the urls are not loaded when the file is imported, 
#so we have to use the lazy form of reverse to load them later when they’re available.

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

class SignUp(generic.CreateView):
	form_class = UserCreationForm #you can create another class from UserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'signup.html'
	
#signup:
#https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
#extend form:
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    #last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Required. 150 characters or fewer. Letters, digits and @ . + - _ only.'
        self.fields['password1'].help_text = 'Your password cannot be too similar to your other personal information. Your password must contain at least 8 characters. Your password cannot be a commonly used password. Your password cannot be entirely numeric.'
        self.fields['password2'].help_text = 'Enter the same password as before, for verification.'
        self.fields['first_name'].label = 'Nickname'
		#for fieldname in ['username', 'password1', 'password2']:
        #    self.fields[fieldname].help_text = None
	
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password1', 'password2', ) #'last_name',

		
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        #print (User.objects.filter(email=email).count())
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        username = self.cleaned_data.get('username')
        if first_name and User.objects.filter(first_name=first_name).exclude(username=username).exists():
            raise forms.ValidationError(u'Nickname must be unique.')
        return first_name

from django.contrib.auth import login, authenticate
#from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
	
from django.views import generic
from .models import Contest, UserLeaderboard, Submission

class ContestListView(generic.ListView):
	model = Contest
	#template default challenge/contest_list.html
	context_object_name = 'contests' #name of context in file source_list.html
	def get_queryset(self):
		return Contest.objects.order_by('-creation_time')

class ContestDetailView(generic.DetailView):
    model = Contest
	#template default challenge/contest_detail.html
	
class ContestLBView(generic.DetailView):
	model = Contest
	template_name = 'challenge/contest_lb.html'
	def get_context_data(self, **kwargs):
		context = super(ContestLBView, self).get_context_data(**kwargs)
		context['lb']=UserLeaderboard.objects.filter(contest=context['contest'].id).order_by('-lb_score')
		#print(context['lb'].values('user_id','lb_score').order_by('-lb_score'))
		return context

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

#@login_required(login_url='/accounts/login/')
class ContestSubmitView(LoginRequiredMixin, generic.DetailView):
	login_url = '/accounts/login/'
	#redirect_field_name = next
	model = Contest
	template_name = 'challenge/contest_sub.html'
	def get_context_data(self, **kwargs):
		context = super(ContestSubmitView, self).get_context_data(**kwargs)
		context['submits']=Submission.objects.filter(contest=context['contest'].id, user=self.request.user).order_by('-sub_time')
		#print(context['submits'].values())
		#print(redirect_field_name)
		return context

#upload submission
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
class SubmitUploadForm(ModelForm):
	class Meta:
		model = Submission
		fields = ('sub_text', 'filepath', )
		#fields = ('filepath', )
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.form_id = 'id-exampleForm'
		self.helper.form_class = 'blueForms'
		self.helper.form_method = 'post'
		self.helper.form_action = 'submit_survey'
		self.helper.add_input(Submit('submit', 'Upload'))

		
#import task functions
from .tasks import check_submit
		
@login_required
def submit_upload(request, pk):
	contest = Contest.objects.get(id=pk)
	if request.method == 'POST':
		form = SubmitUploadForm(request.POST, request.FILES)
		if form.is_valid(): #!!!!!
			#print(form.fields['filepath'].__dir__())
			'''
			['max_length', 'allow_empty_file', 'required', 'label', 'initial', 'show_hidden_initial', 'help_text', 'disabled', 'label_suffix', 'localize', 'widget', 'error_messages', 'validators', '__module__', 'default_error_messages', '__init__', 'to_python', 'clean', 'bound_data', 'has_changed', '__doc__', '__slotnames__', 'hidden_widget', 'default_validators', 'empty_values', 'prepare_value', 'validate', 'run_validators', 'widget_attrs', 'get_bound_field', '__deepcopy__', '__dict__', '__weakref__', '__repr__', '__hash__', '__str__', '__getattribute__', '__setattr__', '__delattr__', '__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__', '__new__', '__reduce_ex__', '__reduce__', '__subclasshook__', '__init_subclass__', '__format__', '__sizeof__', '__dir__', '__class__']
			'''
			extend_form = form.save(commit=False)
			extend_form.user = request.user
			extend_form.contest = contest
			#!!!extend_form.filename = ?
			print(extend_form.filepath)
			# file is saved
			extend_form.save()
			submit_id = extend_form.id
			check_submit.delay(submit_id)
			return redirect('contest-submits', pk=pk)
	else:
		form = SubmitUploadForm()
	return render(request, 'challenge/contest_upload.html', {'form': form, 'contest' : contest})
