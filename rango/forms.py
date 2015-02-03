from django import forms
from rango.models import Page, Category, ProfilUser
from django.contrib.auth.models import User

class categoryform(forms.ModelForm):
	name= forms.CharField(max_length=128, help_text="enter category's name")
	views= forms.IntegerField(widget=forms.HiddenInput(),initial=0)
	likes= forms.IntegerField(widget=forms.HiddenInput(),initial=0)
	class Meta:
		model = Category
class pageform(forms.ModelForm):
	title= forms.CharField(max_length=128, help_text="enter page title")
	url= forms.URLField(max_length= 200, help_text="please enter url")
	views= forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	class Meta:
		model = Page
		fields=('title', 'url','views')
class userform(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = User
		fields=('username','password','email')
class profiluserform(forms.ModelForm):
	class Meta:
		model= ProfilUser
		fields=('website','picture')
