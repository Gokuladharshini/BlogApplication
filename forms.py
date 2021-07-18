from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from django import forms
from .models import Post,Category,Profile,Comment

choices=Category.objects.all().values_list('name','name')

choice_list=[]
for item in choices:
	choice_list.append(item)

class UserRegisterForm(UserCreationForm):
	email=forms.EmailField()
	first_name=forms.CharField()
	last_name=forms.CharField()

	class Meta():
		model=User
		fields=['username','first_name','last_name','email','password1','password2']


class PostForm(forms.ModelForm):
	class Meta():
		model=Post
		fields=('title','author','category','body','snippet','header_image')

		widgets ={
		    'title':forms.TextInput(attrs={'class': 'form-control'}),
		    'author':forms.TextInput(attrs={'class': 'form-control','value':'','id':'aut_id','type':'hidden'}),
		    #'author':forms.Select(attrs={'class': 'form-control'}),
		    'category':forms.Select(choices=choice_list,attrs={'class': 'form-control'}),
		    'body':forms.Textarea(attrs={'class': 'form-control'}),
		    'snippet':forms.Textarea(attrs={'class': 'form-control','placeholder':'This will be your header snippet'}),
		}

class EditForm(forms.ModelForm):
	class Meta:
		model=Post
		fields=('title','body','snippet','header_image')

		widgets ={
		    'title':forms.TextInput(attrs={'class': 'form-control'}),
		    'body':forms.Textarea(attrs={'class': 'form-control'}),
		    'snippet':forms.Textarea(attrs={'class': 'form-control'}),
		}

class EditProfileForm(UserChangeForm):
	email=forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
	first_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
	last_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
	username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
	
	class Meta:
		model=User
		fields=('username','first_name','last_name','email')


class PasswordChangingForm(PasswordChangeForm):
	old_password=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','type':'password'}))
	new_password1=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
	new_password2=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))

	class Meta:
		model=User
		fields=('old_password','new_password1','new_password2','email')


class ProfilePageForm(forms.ModelForm):
	
    class Meta:
	    model=Profile
	    fields=('bio','profile_pic','website_url','facebook_url','twitter_url','instagram_url','linkedin_url')
	    widgets={
	        'bio':forms.Textarea(attrs={'class': 'form-control'}),
		    #'profile_pic':forms.TextInput(attrs={'class': 'form-control'}),
		    'website_url':forms.TextInput(attrs={'class': 'form-control'}),
		    'facebook_url':forms.TextInput(attrs={'class': 'form-control'}),
		    'twitter_url':forms.TextInput(attrs={'class': 'form-control'}),
		    'instagram_url':forms.TextInput(attrs={'class': 'form-control'}),
		    'linkedin_url':forms.TextInput(attrs={'class': 'form-control'}),

	    }

class CommentForm(forms.ModelForm):
	class Meta:
		model=Comment
		fields=('name','body')

		widgets ={
		    'name':forms.TextInput(attrs={'class': 'form-control'}),
		    'body':forms.Textarea(attrs={'class': 'form-control'}),
		}


