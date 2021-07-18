from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.views import PasswordChangeView

from django.contrib import messages
from .forms import UserRegisterForm,PostForm,EditForm,EditProfileForm,PasswordChangingForm,ProfilePageForm,CommentForm
from django.views import generic
from .models import Post,Category,Profile,Comment
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy,reverse
from django.http import HttpResponseRedirect

from django.conf import settings
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

# Create your views here.


class PostView(ListView):
	model=Post
	template_name='posts.html'
	ordering=['-id']

	def get_context_data(self, *args, **kwargs):
		cat_menu=Category.objects.all()
		context=super(PostView,self).get_context_data(*args,**kwargs)
		context["cat_menu"]=cat_menu
		return context


class ArticleDetailView(DetailView):
	model=Post
	template_name='articles_detail.html'

	def get_context_data(self, *args, **kwargs):
      	    cat_menu=Category.objects.all()
      	    context=super(ArticleDetailView,self).get_context_data(*args,**kwargs)
      	    stuff=get_object_or_404(Post, id=self.kwargs['pk'])
      	    total_likes=stuff.total_likes()
      	    liked=False
      	    if stuff.likes.filter(id=self.request.user.id).exists():
                    liked=True

      	    context["cat_menu"]=cat_menu
      	    context["total_likes"]=total_likes
      	    context["liked"]=liked
      	    return context


class AddPostView(CreateView):
	model=Post
	form_class=PostForm
	template_name='add_post.html'
	#fields='__all__'

	def get_context_data(self, *args, **kwargs):
		cat_menu=Category.objects.all()
		context=super(AddPostView,self).get_context_data(*args,**kwargs)
		context["cat_menu"]=cat_menu
		return context


class UpdatePostView(UpdateView):
	model=Post
	form_class=EditForm
	template_name='update_post.html'

	def get_context_data(self, *args, **kwargs):
		cat_menu=Category.objects.all()
		context=super(UpdatePostView,self).get_context_data(*args,**kwargs)
		context["cat_menu"]=cat_menu
		return context



class DeletePostView(DeleteView):
	model=Post
	template_name='delete_post.html'
	success_url=reverse_lazy('posts')

	def get_context_data(self, *args, **kwargs):
		cat_menu=Category.objects.all()
		context=super(DeletePostView,self).get_context_data(*args,**kwargs)
		context["cat_menu"]=cat_menu
		return context


class UserEditView(generic.UpdateView):
	 form_class=EditProfileForm
	 template_name='edit_profile.html'
	 success_url=reverse_lazy('profile')
	 

	 def get_object(self):
	 	return self.request.user


class PasswordsChangeView(PasswordChangeView):
	form_class=PasswordChangingForm
	#form_class=PasswordChangeForm
	success_url=reverse_lazy('password_success')


class ShowProfilePageView(DetailView):
	model=Profile
	template_name='Sblogs/user_profile.html'

	def get_context_data(self, *args, **kwargs):
      	    #users=Profile.objects.all()
      	    context=super(ShowProfilePageView,self).get_context_data(*args,**kwargs)
      	    page_user=get_object_or_404(Profile,id=self.kwargs['pk'])
      	    context["page_user"]=page_user
      	    return context


class EditProfilePageView(generic.UpdateView):
	model=Profile
	template_name='Sblogs/edit_profile_page.html'
	fields=['bio','profile_pic','website_url','facebook_url','twitter_url','instagram_url','linkedin_url']
	success_url=reverse_lazy('home')


class CreateProfilePageView(CreateView):
	model=Profile
	form_class=ProfilePageForm
	template_name='Sblogs/create_user_profile_page.html'
	#fields='__all__'

	def form_valid(self,form):
		form.instance.user=self.request.user
		return super().form_valid(form)


class AddCommentView(CreateView):
    model=Comment
    form_class=CommentForm
    template_name='Sblogs/add_comment.html'
     
    #fields='__all__'
    def form_valid(self,form):
        form.instance.post_id=self.kwargs['pk']
        return super().form_valid(form)

    success_url=reverse_lazy('posts')





def password_success(request):
	return render(request,'Sblogs/password_success.html',{})
	 
def home(request):
	return render(request, 'Sblogs/home.html')


def register(request):
	if request.method=="POST":
	    form=UserRegisterForm(request.POST)
	    if form.is_valid():
	    	form.save()
	    	username=form.cleaned_data.get('username')
	    	messages.success(request,f'Hi {username} your account was created successfully')
	    	return redirect('home')
	else:
		form=UserRegisterForm()
	return render(request, 'Sblogs/register.html',{'form':form})



def CategoryView(request,cats):
	category_posts=Post.objects.filter(category=cats.replace('-', ' '))
	return render(request, 'Sblogs/categories.html', {'cats':cats.replace('-', ' ').title(), 'category_posts':category_posts})

def LikeView(request,pk):
    post=get_object_or_404(Post,id=request.POST.get('post_id'))
    liked=False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked=False
    else:
        post.likes.add(request.user)
        liked=True
    return HttpResponseRedirect(reverse('articles_detail', args=[str(pk)]))


def search(request):
	query=request.GET['query']
	object_list=Post.objects.filter(title__icontains=query)
	if object_list.exists():
	    params={'object_list':object_list}
	    return render(request,'Sblogs/search.html',params)
	else:
		messages.info(request,'Search results not found')
		return redirect('home')
	#return HttpResponse('This is Search')



# Mailchimp Settings
api_key = settings.MAILCHIMP_API_KEY
server = settings.MAILCHIMP_DATA_CENTER
list_id = settings.MAILCHIMP_EMAIL_LIST_ID


# Subscription Logic
def subscribe(email):
    """
     Contains code handling the communication to the mailchimp api
     to create a contact/member in an audience/list.
    """

    mailchimp = Client()
    mailchimp.set_config({
        "api_key": api_key,
        "server": server,
    })

    member_info = {
        "email_address": email,
        "status": "subscribed",
    }

    try:
        response = mailchimp.lists.add_list_member(list_id, member_info)
        print("response: {}".format(response))
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))




# Views here.
def subscription(request):
    if request.method == "POST":
        email = request.POST['email']
        subscribe(email)                    # function to access mailchimp
        messages.success(request, "Email received. thank You! ") # message

    return render(request, "Sblogs/home.html")

