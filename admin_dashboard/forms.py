from django import forms
from core.models import Solution, BlogPost, CustomUser, TeamMember
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from crispy_forms.bootstrap import PrependedText, AppendedText


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
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Solution Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Short description'}),
            'detailed_content': TinyMCE(attrs={'cols': 80, 'rows': 10}),  # Rich text editor
            'category': forms.Select(attrs={'class': 'form-select'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bootstrap icon name'}),
            'features': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter features as JSON list'}),
            'benefits': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter benefits as JSON list'}),
            'use_cases': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter use cases as JSON list'}),
            'faqs': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter FAQs as JSON list of dicts'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
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
            Submit('submit', 'Save Solution', css_class='btn btn-primary')
        )


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'category', 'status', 'excerpt', 'featured_image']
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


class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            Submit('submit', 'Create User', css_class='btn btn-primary')
        )
class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'role', 'photo', 'bio', 'is_active']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Save Team Member'))