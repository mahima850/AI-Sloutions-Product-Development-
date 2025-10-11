from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from tinymce.models import HTMLField
from django.apps import apps  # Importing apps to avoid circular imports
from tinymce.models import HTMLField  # If you're using TinyMCE for rich text
from django.contrib.auth import get_user_model
# Custom User model
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('viewer', 'Viewer'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')
    phone = models.CharField(max_length=20, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def has_admin_access(self):
        return self.role in ['admin', 'editor']

# Site Settings model
class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default="AI-Solution")
    logo = models.ImageField(upload_to='settings/', blank=True, null=True)
    favicon = models.ImageField(upload_to='settings/', blank=True, null=True)
    contact_email = models.EmailField(max_length=254, blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True,
                                      related_name='site_settings_updated_by')

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name

    # Ensure only one instance exists
    def save(self, *args, **kwargs):
        # Allow only one instance of SiteSettings to exist
        if not self.pk and SiteSettings.objects.exists():
            raise ValueError('There can be only one SiteSettings instance')
        return super().save(*args, **kwargs)

    # Load method to retrieve the SiteSettings instance
    @classmethod
    def load(cls):
        return cls.objects.first()  # Assumes only one instance of SiteSettings should exist

# Activity Log model
class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Created'),
        ('update', 'Updated'),
        ('delete', 'Deleted'),
        ('view', 'Viewed'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    content_type = models.CharField(max_length=50)
    object_id = models.PositiveIntegerField()
    object_repr = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} {self.action} {self.content_type} at {self.timestamp}"

# About Us model
class AboutUs(models.Model):
    title = models.CharField(max_length=200, default="About AI-Solution")
    company_background = HTMLField()
    mission = HTMLField()
    vision = HTMLField()
    values = HTMLField(blank=True)
    founded_year = models.PositiveIntegerField(default=2019)
    employees_count = models.PositiveIntegerField(default=50)
    clients_count = models.PositiveIntegerField(default=500)
    countries_count = models.PositiveIntegerField(default=25)
    success_rate = models.PositiveIntegerField(default=98, validators=[MinValueValidator(0), MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name = "About Us"
        verbose_name_plural = "About Us"
    
    def __str__(self):
        return self.title

# Solution model
class Solution(models.Model):
    CATEGORY_CHOICES = [
        ('healthcare', 'Healthcare'),
        ('finance', 'Finance'),
        ('education', 'Education'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    detailed_content = HTMLField(help_text="Rich text content for solution details", blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    icon = models.CharField(max_length=50, help_text="Bootstrap icon name")
    features = models.JSONField(default=list, help_text="List of features")
    benefits = models.JSONField(default=list, help_text="List of benefits")
    use_cases = models.JSONField(default=list, help_text="List of use cases")
    faqs = models.JSONField(default=list, help_text="List of FAQs (dict with 'question' and 'answer')")
    image = models.ImageField(upload_to='solutions/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['order', 'title']
    
    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

    # Use lazy import for related models to avoid circular imports
    def get_related_articles(self):
        Article = apps.get_model('core', 'Article')
        return Article.objects.filter(category=self.category)

# Contact Inquiry model
class ContactInquiry(models.Model):
    COUNTRY_CHOICES = [
        ('US', 'United States'),
        ('CA', 'Canada'),
        ('UK', 'United Kingdom'),
        ('DE', 'Germany'),
        ('FR', 'France'),
        ('AU', 'Australia'),
        ('JP', 'Japan'),
        ('KR', 'South Korea'),
        ('SG', 'Singapore'),
        ('IN', 'India'),
        ('BR', 'Brazil'),
        ('MX', 'Mexico'),
        ('NP', 'Nepal'),
        ('OTHER', 'Other'),
    ]
    
    JOB_TITLE_CHOICES = [
        ('ceo', 'CEO/President'),
        ('cto', 'CTO/VP Technology'),
        ('director', 'IT Director'),
        ('scientist', 'Data Scientist'),
        ('engineer', 'Software Engineer'),
        ('manager', 'Product Manager'),
        ('analyst', 'Business Analyst'),
        ('consultant', 'Consultant'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=10, choices=COUNTRY_CHOICES, blank=True)
    job_title = models.CharField(max_length=20, choices=JOB_TITLE_CHOICES, blank=True)
    message = models.TextField()
    attachment = models.FileField(upload_to='inquiries/', blank=True, null=True)
    is_read = models.BooleanField(default=False)
    is_responded = models.BooleanField(default=False)
    response_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Inquiry from {self.name} - {self.company}"

# Feedback model
class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    company = models.CharField(max_length=100, blank=True)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='feedback_avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Feedback from {self.name} - {self.rating} stars"

# BlogPost model
class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    CATEGORY_CHOICES = [
        ('healthcare', 'Healthcare'),
        ('finance', 'Finance'),
        ('education', 'Education'),
        ('technology', 'Technology'),
        ('ethics', 'Ethics'),
        ('tutorial', 'Tutorial'),
        ('news', 'News'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    excerpt = models.TextField(max_length=300)
    content = HTMLField()
    author = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    tags = models.JSONField(default=list)
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    read_time = models.PositiveIntegerField(default=5, help_text="Estimated read time in minutes")
    views_count = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

# Event model
class Event(models.Model):
    TYPE_CHOICES = [
        ('conference', 'Conference'),
        ('workshop', 'Workshop'),
        ('webinar', 'Webinar'),
        ('showcase', 'Showcase'),
        ('symposium', 'Symposium'),
    ]
    
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=200)
    description = HTMLField()
    event_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    capacity = models.PositiveIntegerField()
    price = models.CharField(max_length=50, default='Free')
    featured_image = models.ImageField(upload_to='events/', blank=True, null=True)
    speakers = models.JSONField(default=list)
    agenda = models.JSONField(default=list)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='upcoming')
    is_featured = models.BooleanField(default=False)
    registration_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['date', 'time']
    
    def __str__(self):
        return f"{self.title} - {self.date}"

# GalleryItem model
class GalleryItem(models.Model):
    CATEGORY_CHOICES = [
        ('conference', 'Conference'),
        ('product_launch', 'Product Launch'),
        ('workshop', 'Workshop'),
        ('symposium', 'Symposium'),
        ('team_event', 'Team Event'),
        ('demo', 'Demo'),
        ('tour', 'Tour'),
        ('award', 'Award'),
        ('partnership', 'Partnership'),
    ]
    
    title = models.CharField(max_length=200)
    description = HTMLField()
    image = models.ImageField(upload_to='gallery/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    event_date = models.DateField()
    location = models.CharField(max_length=200)
    event_name = models.CharField(max_length=200)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['-event_date', 'order']
    
    def __str__(self):
        return f"{self.title} - {self.event_date}"

# EventRegistration model
class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    special_requirements = models.TextField(blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=True)
    attended = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['event', 'email']
        ordering = ['-registration_date']
    
    def __str__(self):
        return f"{self.name} - {self.event.title}"

# Newsletter model
class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
# Article model
User = get_user_model()

class Article(models.Model):
    ARTICLE_TYPE_CHOICES = [
        ('industry_report', 'Industry Report'),
        ('research_paper', 'Research Paper'),
        ('white_paper', 'White Paper'),
        ('technical_paper', 'Technical Paper'),
        ('market_analysis', 'Market Analysis'),
        ('framework_guide', 'Framework Guide'),
    ]
    
    title = models.CharField(max_length=200)
    content = HTMLField()  # If using rich text (TinyMCE)
    excerpt = models.TextField()  # Short summary or excerpt of the article
    category = models.CharField(max_length=100)  # You can use a choice field or ForeignKey to a Category model
    status = models.CharField(max_length=20, choices=[('draft', 'Draft'), ('published', 'Published')], default='draft')
    article_type = models.CharField(max_length=50, choices=ARTICLE_TYPE_CHOICES, default='industry_report')
    author = models.CharField(max_length=100, blank=True)
    featured_image = models.ImageField(upload_to='articles/', blank=True, null=True)  # Optional featured image
    published_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)  # Flag for featured articles
    download_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-published_at']  # Newest articles first

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        """Returns the URL for the article detail page."""
        return reverse('article_detail', kwargs={'pk': self.pk})

    def increment_download_count(self):
        """Method to increment the download count."""
        self.download_count += 1
        self.save(update_fields=['download_count'])

    def save(self, *args, **kwargs):
        """Override save method to set the published date on published articles."""
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='team/', blank=True, null=True)
    email = models.EmailField(blank=True)
    linkedin_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='team/', blank=True, null=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name
