from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import timezone
import json
import random

from .forms import ContactForm, FeedbackForm, NewsletterForm, ArticleForm ,EventForm, GalleryItemForm
from .models import *

from django.shortcuts import render
from core.models import SiteSettings, AboutUs, Solution, Feedback, BlogPost
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

def home(request):
    """Homepage view"""
    
    # Load site settings with fallback defaults
    site_settings = SiteSettings.load() if hasattr(SiteSettings, 'load') else {
        'site_name': 'Default Site Name',
        'contact_email': 'info@default.com',
        'contact_phone': '+1234567890'
    }
    
    # Load About Us content with fallback
    about_us_obj = AboutUs.objects.first()
    about_us = {
        'title': about_us_obj.title if about_us_obj else 'About Us',
        'company_background': getattr(about_us_obj, 'company_background', 'No company background available.'),
        'mission': getattr(about_us_obj, 'mission', 'No mission statement available.'),
        'vision': getattr(about_us_obj, 'vision', 'No vision statement available.'),
        'values': getattr(about_us_obj, 'values', 'No values available.')
    }
    
    # Featured solutions (active only)
    featured_solutions = Solution.objects.filter(is_featured=True, is_active=True)[:3]
    
    # Approved and optionally featured testimonials
    testimonials = Feedback.objects.filter(is_approved=True).order_by('-created_at')[:4]
    
    # Recent published blog posts
    recent_blog_posts = BlogPost.objects.filter(status='published').order_by('-published_at')[:3]
    
    context = {
        'settings': site_settings,
        'about_us': about_us,
        'featured_solutions': featured_solutions,
        'testimonials': testimonials,
        'recent_blog_posts': recent_blog_posts,
    }
    
    return render(request, 'frontend/index.html', context)


def about(request):
    """About us page"""
    about_us = AboutUs.objects.first()
    team_members = TeamMember.objects.filter(is_active=True)
    
    context = {
        'about_us': about_us,
        'team_members': team_members,
        'settings': SiteSettings.load(),
    }
    
    return render(request, 'frontend/about.html', context)

def solutions(request):
    """Solutions page with filtering"""
    category = request.GET.get('category', '')
    
    queryset = Solution.objects.filter(is_active=True)
    
    if category:
        queryset = queryset.filter(category=category)
    
    solutions_list = queryset.order_by('order', 'title')
    categories = Solution.CATEGORY_CHOICES
    
    context = {
        'solutions': solutions_list,
        'categories': categories,
        'selected_category': category,
        'settings': SiteSettings.load(),
    }
    
    return render(request, 'frontend/solutions.html', context)

def solution_detail(request, solution_id):
    """Solution detail page"""
    solution = get_object_or_404(Solution, id=solution_id, is_active=True)
    related_solutions = Solution.objects.filter(category=solution.category, is_active=True).exclude(id=solution.id)[:3]
    
    context = {
        'solution': solution,
        'related_solutions': related_solutions,
        'settings': SiteSettings.load(),
    }
    
    return render(request, 'frontend/solution_detail.html', context)

def contact(request):
    """Contact page with form"""
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'settings': SiteSettings.load(),
    }
    
    return render(request, 'frontend/contact.html', context)

def blog(request):
    """Blog listing page"""
    category = request.GET.get('category', '')
    search = request.GET.get('search', '')
    
    queryset = BlogPost.objects.filter(status='published')
    
    if category:
        queryset = queryset.filter(category=category)
    
    if search:
        queryset = queryset.filter(
            Q(title__icontains=search) |
            Q(excerpt__icontains=search) |
            Q(content__icontains=search)
        )
    
    paginator = Paginator(queryset, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = BlogPost.CATEGORY_CHOICES
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category,
        'search_query': search,
        'settings': SiteSettings.load(),
    }
    
    return render(request, 'frontend/blog.html', context)

def blog_detail(request, slug):
    """Blog post detail page"""
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    
    post.views_count += 1
    post.save(update_fields=['views_count'])
    
    related_posts = BlogPost.objects.filter(category=post.category, status='published').exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'settings': SiteSettings.load(),
    }
    
    return render(request, 'frontend/blog_detail.html', context)

def articles(request):
    """Articles page"""
    article_type = request.GET.get('type', '')
    queryset = Article.objects.all()
    
    if article_type:
        queryset = queryset.filter(article_type=article_type)
    
    paginator = Paginator(queryset, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    types = Article.ARTICLE_TYPE_CHOICES  # <- fixed
    
    context = {
        'page_obj': page_obj,
        'types': types,
        'selected_type': article_type,
        'settings': SiteSettings.load(),
    }
    
    return render(request, 'frontend/articles.html', context)


def add_article(request):
    """Add article page"""
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('article_list')
    else:
        form = ArticleForm()
    
    return render(request, 'add_article.html', {'form': form})

def article_list(request):
    """List all articles"""
    articles = Article.objects.filter(status='published')
    return render(request, 'core/article_list.html', {'articles': articles})

def article_detail(request, pk):
    """Display a single article"""
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'core/article_detail.html', {'article': article})

def event_list(request):
    """List all events"""
    events = Event.objects.filter(status='upcoming')
    return render(request, 'core/event_list.html', {'events': events})

def gallery(request):
    """Gallery page"""
    category = request.GET.get('category', '')
    queryset = GalleryItem.objects.all()
    
    if category:
        queryset = queryset.filter(category=category)
    
    gallery_items = queryset.order_by('-event_date', 'order')
    categories = GalleryItem.CATEGORY_CHOICES
    
    context = {
        'gallery_items': gallery_items,
        'categories': categories,
        'selected_category': category,
        'settings': SiteSettings.load(),
    }
    
    return render(request, 'frontend/gallery.html', context)

def events(request):
    """Events page"""
    event_type = request.GET.get('type', '')
    status = request.GET.get('status', 'upcoming')
    
    queryset = Event.objects.all()
    
    if event_type:
        queryset = queryset.filter(event_type=event_type)
    
    if status:
        queryset = queryset.filter(status=status)
    
    events_list = queryset.order_by('date', 'time')
    types = Event.TYPE_CHOICES
    statuses = Event.STATUS_CHOICES
    
    context = {
        'events': events_list,
        'types': types,
        'statuses': statuses,
        'selected_type': event_type,
        'selected_status': status,
        'settings': SiteSettings.load(),
    }
    
    return render(request, 'frontend/events.html', context)

# AJAX Views
@require_POST
def submit_feedback(request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    rating = request.POST.get("rating")
    comment = request.POST.get("comment")

    # Save to model
    from .models import Feedback
    Feedback.objects.create(
        name=name,
        email=email,
        rating=rating,
        comment=comment,
    )

    return JsonResponse({"success": True, "message": "Thanks for your feedback!"})

@require_http_methods(["POST"])
def newsletter_signup(request):
    """Newsletter signup via AJAX"""
    try:
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Successfully subscribed to our newsletter!'})
        return JsonResponse({'success': False, 'message': 'Please enter a valid email address.'})
    except Exception:
        return JsonResponse({'success': False, 'message': 'An error occurred. Please try again.'})

@require_http_methods(["POST"])
def chatbot_response(request):
    """Simple chatbot responses"""
    try:
        data = json.loads(request.body)
        message = data.get('message', '').lower()
        
        responses = {
             # ===== GREETINGS =====
            "hello": "Hello there! How can I assist you today?",
            "hi": "Hi! Welcome to AI-Solution. What would you like to know?",
            "hey": "Hello! How can I help you learn more about AI-Solution?",
            "good morning": "Good morning! How can I support you today?",
            "good afternoon": "Good afternoon! What can I do for you?",
            "good evening": "Good evening! How can I assist with your AI queries today?",
            "how are you": "I'm doing well, thank you for asking. How can I assist you today?",
            "can you help me": "Of course. Please tell me what kind of information you are looking for.",

            # ===== ABOUT COMPANY =====
            "what is ai-solution": "AI-Solution is a technology company specializing in developing AI-powered platforms for healthcare, finance, and education.",
            "tell me about ai-solution": "AI-Solution focuses on building intelligent systems that improve automation, analytics, and decision-making using artificial intelligence.",
            "what does ai-solution do": "We create AI-driven solutions that help businesses analyze data, automate operations, and improve performance.",
            "when was ai-solution founded": "AI-Solution was conceptualized as a modern AI development platform focused on integrating machine learning into business applications.",
            "where is ai-solution located": "AI-Solution is based in Nepal and collaborates with international partners on AI and data science projects.",
            "what is your mission": "Our mission is to make artificial intelligence accessible, transparent, and beneficial for all industries.",
            "what is your vision": "Our vision is to empower organizations through innovative, data-driven, and ethical AI solutions.",
            "what are your core values": "Our core values include innovation, transparency, teamwork, integrity, and user-centric design.",
            "what makes ai-solution unique": "AI-Solution stands out for its blend of practical implementation, academic rigor, and focus on real-world AI deployment.",

            # ===== SERVICES =====
            "what services do you offer": "We offer AI-based services for Healthcare, Finance, and Education, focusing on data analytics, automation, and predictive modeling.",
            "can you tell me about your healthcare services": "In healthcare, we develop diagnostic tools, patient management systems, and disease prediction models using deep learning.",
            "what do you offer in finance": "Our finance AI solutions include fraud detection, algorithmic trading, customer risk analysis, and financial forecasting.",
            "what are your education services": "We create AI-powered platforms for personalized learning, student performance tracking, and automated evaluation systems.",
            "which industries do you work with": "We work across healthcare, finance, education, and enterprise digital transformation sectors.",
            "do you provide custom ai solutions": "Yes, we design custom AI systems tailored to client needs and integrate them with existing infrastructures.",
            "do you provide consulting services": "Yes, we offer AI strategy consulting, technical advisory, and implementation support.",

            # ===== PROJECTS & PRODUCTS =====
            "can you tell me about your projects": "Our projects include predictive analytics tools, healthcare diagnostic systems, and automated learning platforms.",
            "what projects have you completed": "We have completed projects involving medical image classification, financial risk modeling, and academic data analytics.",
            "what are your main products": "Our main products include AI-powered data dashboards, smart prediction engines, and process automation modules.",
            "do you publish research papers": "Yes, we regularly publish research and technical documentation related to AI development and ethical data use.",
            "do you have case studies": "Yes, we maintain a portfolio of case studies highlighting real-world AI implementations for different clients.",

            # ===== CONTACT & SUPPORT =====
            "how can i contact you": "You can contact us through the website contact form or email us at info@ai-solution.com.",
            "how do i reach your team": "Please reach out through the contact section of our website. Our team will respond promptly.",
            "how do i get technical support": "For technical assistance, use the support form on our website to submit your issue.",
            "how can i give feedback": "We welcome your feedback. Please share it through our website feedback section.",
            "how can i report a bug": "You can report any issue by contacting our technical team through the contact form.",
            "do you provide customer support": "Yes, our support team is available to help you with technical and product-related queries.",
            "do you offer live chat support": "Currently, we provide chatbot and email-based support, with live chat planned for future updates.",

            # ===== PRICING & DEMO =====
            "what is your pricing": "Our pricing depends on the type of AI service, project scale, and customization requirements.",
            "how much do your services cost": "Costs vary depending on project complexity and the AI model involved. Please contact us for an estimate.",
            "do you have free trials": "We provide demo access for selected solutions upon request.",
            "can i book a demo": "Yes, you can schedule a live demonstration by contacting our team.",
            "how can i schedule a demo": "Please provide your contact information and preferred time to arrange a demo session.",
            "what are your payment options": "Payments can be made via bank transfer or online payment once the project proposal is confirmed.",
            "do you provide subscription plans": "Yes, we offer both one-time and subscription-based service models depending on client needs.",

            # ===== TEAM & CAREERS =====
            "who are in your team": "Our team consists of AI engineers, software developers, researchers, and data analysts with diverse expertise.",
            "do you have job openings": "Yes, we periodically open positions in AI, data science, and web development. Please check our careers section.",
            "how can i apply for a job": "You can apply by sending your CV and cover letter through the contact form or the careers email listed on our site.",
            "who leads the company": "AI-Solution is led by experienced developers and researchers with expertise in artificial intelligence and software design.",

            # ===== TECHNOLOGY & TOOLS =====
            "what technologies do you use": "We use Python, Django, TensorFlow, Keras, Bootstrap, and PostgreSQL to develop our systems.",
            "what programming languages do you use": "Our primary languages are Python and JavaScript, supported by SQL for database management.",
            "what is your tech stack": "Our stack includes Django for backend, Bootstrap for frontend, and MySQL or PostgreSQL for database operations.",
            "what ai techniques do you use": "We use supervised and unsupervised learning, neural networks, and NLP for various AI applications.",
            "do you use machine learning": "Yes, machine learning forms the foundation of most of our predictive and analytical solutions.",
            "do you use deep learning": "Yes, we apply deep learning for image recognition, diagnostics, and advanced data modeling.",
            "do you work with cloud technologies": "Yes, we deploy AI systems on AWS, PythonAnywhere, and Netlify for scalability and reliability.",
            "do you support mobile platforms": "Yes, we can integrate AI APIs with mobile applications and dashboards.",

            # ===== DEPLOYMENT & TESTING =====
            "how do you deploy your applications": "We deploy our applications on cloud platforms like PythonAnywhere, AWS, and Netlify for secure hosting.",
            "what is your testing process": "We perform unit testing, integration testing, and user acceptance testing to ensure software reliability.",
            "do you perform quality assurance": "Yes, all our systems undergo strict quality assurance and performance optimization.",
            "do you provide maintenance": "Yes, we offer post-deployment support, monitoring, and maintenance services.",

            # ===== DATA & PRIVACY =====
            "how do you handle data privacy": "We comply with data privacy standards and ensure that user data is encrypted and securely managed.",
            "do you store user data": "We store only the minimum required data necessary for application functionality, following privacy regulations.",
            "is my information secure": "Yes, we implement authentication, encryption, and access control to protect all user data.",
            "do you follow gdpr": "Yes, our data management practices are aligned with GDPR and related privacy standards.",

            # ===== COMPANY POLICIES =====
            "do you offer refunds": "Refunds are processed according to project agreements and service-level terms.",
            "do you provide documentation": "Yes, every project includes full documentation for setup, usage, and maintenance.",
            "do you sign nda": "Yes, we sign non-disclosure agreements to ensure confidentiality of client projects.",
            "do you offer long-term support": "Yes, we provide ongoing maintenance, monitoring, and feature updates based on client requirements.",

            # ===== GENERAL =====
            "thank you": "You're welcome. Is there anything else you would like to know?",
            "thanks": "You're welcome. Feel free to ask anything else.",
            "goodbye": "Goodbye. Thank you for visiting AI-Solution.",
            "bye": "Thank you for your time. Have a great day ahead.",
            "who are you": "I am the AI-Solution virtual assistant designed to answer your queries about our company and services.",
            "what can you do": "I can answer questions about AI-Solution, its services, projects, pricing, and technologies.",
            "are you a real person": "No, I am an AI chatbot built by the AI-Solution development team to assist visitors automatically."
        }
        
        response = "I'm sorry, I didn't understand that. Could you please rephrase your question or contact our support team?"
        
        for keyword, reply in responses.items():
            if keyword in message:
                response = reply
                break
        
        return JsonResponse({'success': True, 'response': response})
    except Exception:
        return JsonResponse({'success': False, 'response': 'Sorry, I encountered an error. Please try again.'})

def download_article(request, article_id):
    """Download article PDF"""
    article = get_object_or_404(Article, id=article_id)
    
    if article.pdf_file:
        article.download_count += 1
        article.save(update_fields=['download_count'])
        
        response = HttpResponse(article.pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{article.title}.pdf"'
        return response
    else:
        raise Http404("PDF file not found")

@require_http_methods(["POST"])
def event_registration(request, event_id):
    """Event registration via AJAX"""
    try:
        event = get_object_or_404(Event, id=event_id)
        
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        company = request.POST.get('company', '')
        
        registration, created = EventRegistration.objects.get_or_create(
            event=event,
            email=email,
            defaults={'name': name, 'phone': phone, 'company': company}
        )
        
        if created:
            return JsonResponse({'success': True, 'message': 'Successfully registered for the event!'})
        return JsonResponse({'success': False, 'message': 'You are already registered for this event.'})
    except Exception:
        return JsonResponse({'success': False, 'message': 'An error occurred. Please try again.'})
def add_event(request):
    """View for adding a new event."""
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user  # Set the current user as the creator
            event.save()
            messages.success(request, 'Event added successfully.')
            return redirect('event_list')  # Redirect to the event list after successful addition
    else:
        form = EventForm()

    return render(request, 'core/add_event.html', {'form': form})
def add_gallery_item(request):
    """View for adding a new gallery item."""
    if request.method == 'POST':
        form = GalleryItemForm(request.POST, request.FILES)
        if form.is_valid():
            gallery_item = form.save(commit=False)
            gallery_item.uploaded_by = request.user  # Assuming user uploads items
            gallery_item.save()
            messages.success(request, 'Gallery item added successfully.')
            return redirect('gallery_list')  # Redirect to the gallery list after successful addition
    else:
        form = GalleryItemForm()

    return render(request, 'core/add_gallery_item.html', {'form': form})
def about_us_view(request):
    about_us = AboutUs.objects.first()  # assuming only one AboutUs entry
    team_members = TeamMember.objects.filter(is_active=True)
    context = {
        'about_us': about_us,
        'team_members': team_members,
    }
    return render(request, 'about_us.html', context)
