from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from .models import *  # Assuming all models are imported correctly

# Contact Form
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactInquiry
        fields = ['name', 'email', 'phone', 'company', 'country', 'job_title', 'message', 'attachment']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your.email@company.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 (555) 123-4567'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Company Name'}),
            'country': forms.Select(attrs={'class': 'form-select'}),
            'job_title': forms.Select(attrs={'class': 'form-select'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Tell us about your project and how we can help...'}),
            'attachment': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx,.txt'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('phone', css_class='form-group col-md-6 mb-0'),
                Column('company', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('country', css_class='form-group col-md-6 mb-0'),
                Column('job_title', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'message',
            'attachment',
            HTML('<small class="form-text text-muted">Supported formats: PDF, DOC, DOCX, TXT (Max 10MB)</small>'),
            Submit('submit', 'Send Message', css_class='btn btn-primary btn-lg w-100 mt-3')
        )

# Custom User Creation Form
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'role']  # Add fields as needed

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

# Feedback Form
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'company', 'rating', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your.email@company.com'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name (Optional)'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tell us about your experience with our AI solutions...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'company',
            'rating',
            'comment',
            Submit('submit', 'Submit Feedback', css_class='btn btn-primary w-100 mt-3')
        )

# Newsletter Form
class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['email', 'name']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name (Optional)'}),
        }

# Solution Form
class SolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        fields = [
            'title',
            'description',
            'detailed_content',
            'category',
            'icon',
            'features',
            'benefits',
            'use_cases',
            'faqs',
            'image',
            'is_featured',
            'is_active',
            'order',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Solution Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Short Description'}),
            'detailed_content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Detailed Content (HTML allowed)'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bootstrap Icon Name'}),
            'features': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter features as JSON list'}),
            'benefits': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter benefits as JSON list'}),
            'use_cases': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter use cases as JSON list'}),
            'faqs': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter FAQs as JSON list of dicts'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Crispy Forms helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            'title',
            'description',
            'detailed_content',
            'category',
            'icon',
            'features',
            'benefits',
            'use_cases',
            'faqs',
            'image',
            'is_featured',
            'is_active',
            'order',
            Submit('submit', 'Save Solution', css_class='btn btn-primary')
        )

# BlogPost Form
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        exclude = ['author']  # Exclude author
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Blog Title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Blog Content'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Short excerpt for the blog'}),
            'featured_image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'content',
            'category',
            'status',
            'excerpt',
            'featured_image',
            Submit('submit', 'Save Blog Post', css_class='btn btn-primary')
        )


# Article Form
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'excerpt', 'category', 'status', 'featured_image', 'author', 'is_featured', 'download_count']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Article Title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Article Content'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Article Excerpt'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'featured_image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'download_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'content',
            'excerpt',
            'category',
            'status',
            'featured_image',
            'download_count',
            'is_featured',
            Submit('submit', 'Save Article', css_class='btn btn-primary')
        )

# Custom User Creation Form (Updated)
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
# Event form
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'event_type', 'date', 'time', 'location',
                  'capacity', 'price', 'featured_image', 'speakers', 'agenda',
                  'status', 'is_featured', 'registration_url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'event_type': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'featured_image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'speakers': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'List of speakers as JSON'}),
            'agenda': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Agenda items as JSON'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'is_featured': forms.CheckboxInput(),
            'registration_url': forms.URLInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title', 'description', 'event_type', 'date', 'time', 'location',
            'capacity', 'price', 'featured_image', 'speakers', 'agenda',
            'status', 'is_featured', 'registration_url',
            Submit('submit', 'Save Event', css_class='btn btn-primary')
        )

# Gallery form
class GalleryItemForm(forms.ModelForm):
    class Meta:
        model = GalleryItem
        fields = ['title', 'description', 'image', 'category', 'event_date', 'location', 'event_name', 'is_featured']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'event_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'event_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_featured': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title', 'description', 'image', 'category', 'event_date', 'location', 'event_name', 'is_featured',
            Submit('submit', 'Save Gallery Item', css_class='btn btn-primary')
        )
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'article_type', 'content', 'excerpt', 'featured_image', 'status', 'is_featured']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Article Title'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category'}),
            'article_type': forms.Select(attrs={'class': 'form-select'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'featured_image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title', 'category', 'article_type', 'content', 'excerpt', 'featured_image', 'status', 'is_featured',
            Submit('submit', 'Save Article', css_class='btn btn-primary')
        )
class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'role', 'photo', 'bio', 'is_active']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Save Team Member'))
class AboutUsForm(forms.ModelForm):
    class Meta:
        model = AboutUs
        fields = ['company_background', 'founded_year', 'employees_count',
                  'clients_count', 'countries_count', 'mission', 'vision', 'values', 'success_rate']