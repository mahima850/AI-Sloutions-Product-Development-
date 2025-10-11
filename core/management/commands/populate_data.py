from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify
from datetime import date, time, timedelta
import random

from core.models import *

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Populating database with sample data...')
        
        # Create site settings
        self.create_site_settings()
        
        # Create users
        self.create_users()
        
        # Create about us
        self.create_about_us()
        
        # Create team members
        self.create_team_members()
        
        # Create solutions
        self.create_solutions()
        
        # Create blog posts
        self.create_blog_posts()
        
        # Create articles
        self.create_articles()
        
        # Create events
        self.create_events()
        
        # Create gallery items
        self.create_gallery_items()
        
        # Create feedback
        self.create_feedback()
        
        self.stdout.write(self.style.SUCCESS('Successfully populated database!'))

    def create_site_settings(self):
        settings, created = SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': 'AI-Solution',
                'site_description': 'Empowering Businesses with AI',
                'contact_email': 'info@ai-solution.com',
                'contact_phone': '+1 (555) 123-4567',
                'address': '123 AI Street, Tech City, TC 12345',
                'social_facebook': 'https://facebook.com/aisolution',
                'social_twitter': 'https://twitter.com/aisolution',
                'social_linkedin': 'https://linkedin.com/company/aisolution',
                'social_instagram': 'https://instagram.com/aisolution',
                'chatbot_enabled': True,
                'maintenance_mode': False,
            }
        )
        if created:
            self.stdout.write('Created site settings')

    def create_users(self):
        # Create admin user
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@ai-solution.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write('Created admin user')

        # Create editor users
        editors = [
            {'username': 'john_doe', 'first_name': 'John', 'last_name': 'Doe', 'email': 'john@ai-solution.com'},
            {'username': 'jane_smith', 'first_name': 'Jane', 'last_name': 'Smith', 'email': 'jane@ai-solution.com'},
        ]
        
        for editor_data in editors:
            user, created = User.objects.get_or_create(
                username=editor_data['username'],
                defaults={
                    'email': editor_data['email'],
                    'first_name': editor_data['first_name'],
                    'last_name': editor_data['last_name'],
                    'role': 'editor',
                    'is_staff': True,
                }
            )
            if created:
                user.set_password('editor123')
                user.save()
                self.stdout.write(f'Created editor user: {user.username}')

    def create_about_us(self):
        about, created = AboutUs.objects.get_or_create(
            pk=1,
            defaults={
                'title': 'About AI-Solution',
                'company_background': 'AI-Solution was founded in 2019 with a mission to democratize artificial intelligence and make it accessible to businesses of all sizes. Our team of expert data scientists, engineers, and AI researchers work tirelessly to develop cutting-edge solutions that solve real-world problems.',
                'mission': 'To empower businesses worldwide with intelligent AI solutions that drive innovation, efficiency, and sustainable growth.',
                'vision': 'To be the leading provider of AI solutions that transform industries and improve lives globally.',
                'values': 'Innovation, Integrity, Excellence, Customer Success, and Continuous Learning drive everything we do.',
                'founded_year': 2019,
                'employees_count': 150,
                'clients_count': 500,
                'countries_count': 25,
                'success_rate': 98,
                'updated_by': User.objects.get(username='admin'),
            }
        )
        if created:
            self.stdout.write('Created about us information')

    def create_team_members(self):
        team_data = [
            {
                'name': 'Dr. Sarah Johnson',
                'role': 'Chief Executive Officer',
                'bio': 'With over 15 years of experience in AI and machine learning, Dr. Johnson leads our vision of democratizing AI technology for businesses worldwide.',
                'email': 'sarah.johnson@ai-solution.com',
                'linkedin_url': 'https://linkedin.com/in/sarahjohnson',
                'order': 1,
            },
            {
                'name': 'Michael Chen',
                'role': 'Chief Technology Officer',
                'bio': 'Former Google AI researcher with expertise in deep learning and neural networks. Michael oversees our technical strategy and product development.',
                'email': 'michael.chen@ai-solution.com',
                'linkedin_url': 'https://linkedin.com/in/michaelchen',
                'order': 2,
            },
            {
                'name': 'Dr. Emily Rodriguez',
                'role': 'Head of Data Science',
                'bio': 'PhD in Computer Science from MIT, Emily leads our data science team and specializes in healthcare AI applications.',
                'email': 'emily.rodriguez@ai-solution.com',
                'linkedin_url': 'https://linkedin.com/in/emilyrodriguez',
                'order': 3,
            },
            {
                'name': 'David Kim',
                'role': 'VP of Engineering',
                'bio': 'Experienced software architect with a passion for building scalable AI platforms and robust infrastructure.',
                'email': 'david.kim@ai-solution.com',
                'linkedin_url': 'https://linkedin.com/in/davidkim',
                'order': 4,
            },
        ]
        
        for member_data in team_data:
            member, created = TeamMember.objects.get_or_create(
                name=member_data['name'],
                defaults=member_data
            )
            if created:
                self.stdout.write(f'Created team member: {member.name}')

    def create_solutions(self):
        solutions_data = [
            {
                'title': 'Healthcare AI Assistant',
                'description': 'Advanced AI-powered diagnostic assistance and patient management system for healthcare providers.',
                'category': 'healthcare',
                'icon': 'heart-pulse',
                'features': [
                    'Diagnostic image analysis',
                    'Patient risk assessment',
                    'Treatment recommendation',
                    'Drug interaction checking',
                    'Electronic health records integration'
                ],
                'is_featured': True,
                'order': 1,
            },
            {
                'title': 'Financial Fraud Detection',
                'description': 'Real-time fraud detection and prevention system using advanced machine learning algorithms.',
                'category': 'finance',
                'icon': 'shield-check',
                'features': [
                    'Real-time transaction monitoring',
                    'Anomaly detection',
                    'Risk scoring',
                    'Compliance reporting',
                    'Anti-money laundering'
                ],
                'is_featured': True,
                'order': 2,
            },
            {
                'title': 'Personalized Learning Platform',
                'description': 'AI-driven educational platform that adapts to individual learning styles and progress.',
                'category': 'education',
                'icon': 'book',
                'features': [
                    'Adaptive learning paths',
                    'Progress tracking',
                    'Performance analytics',
                    'Content recommendation',
                    'Assessment automation'
                ],
                'is_featured': True,
                'order': 3,
            },
            {
                'title': 'Smart Investment Advisor',
                'description': 'Intelligent portfolio management and investment advisory system for financial institutions.',
                'category': 'finance',
                'icon': 'graph-up',
                'features': [
                    'Portfolio optimization',
                    'Risk analysis',
                    'Market prediction',
                    'Automated trading',
                    'Regulatory compliance'
                ],
                'is_featured': False,
                'order': 4,
            },
            {
                'title': 'Medical Research Assistant',
                'description': 'AI-powered research tool for medical professionals and pharmaceutical companies.',
                'category': 'healthcare',
                'icon': 'microscope',
                'features': [
                    'Literature analysis',
                    'Drug discovery assistance',
                    'Clinical trial optimization',
                    'Research collaboration',
                    'Data synthesis'
                ],
                'is_featured': False,
                'order': 5,
            },
        ]
        
        admin_user = User.objects.get(username='admin')
        
        for solution_data in solutions_data:
            solution, created = Solution.objects.get_or_create(
                title=solution_data['title'],
                defaults={**solution_data, 'created_by': admin_user}
            )
            if created:
                self.stdout.write(f'Created solution: {solution.title}')

    def create_blog_posts(self):
        blog_data = [
            {
                'title': 'The Future of AI in Healthcare: Transforming Patient Care',
                'slug': 'future-ai-healthcare-transforming-patient-care',
                'excerpt': 'Explore how artificial intelligence is revolutionizing healthcare delivery, from diagnostic assistance to personalized treatment plans.',
                'content': '''Artificial Intelligence is fundamentally transforming the healthcare industry, offering unprecedented opportunities to improve patient outcomes and streamline medical processes.

## Diagnostic Revolution

AI-powered diagnostic tools are now capable of analyzing medical images with accuracy that often surpasses human specialists. From detecting early-stage cancers in radiology scans to identifying diabetic retinopathy in eye exams, AI is enabling earlier and more accurate diagnoses.

## Personalized Treatment

Machine learning algorithms can analyze vast amounts of patient data to recommend personalized treatment plans. This approach considers individual genetic profiles, medical history, and lifestyle factors to optimize therapeutic outcomes.

## Drug Discovery

AI is accelerating drug discovery processes that traditionally took decades. By analyzing molecular structures and predicting drug interactions, AI systems can identify promising compounds in a fraction of the time.

## Challenges and Opportunities

While the potential is enormous, implementing AI in healthcare requires careful consideration of privacy, regulatory compliance, and ethical implications. The future lies in collaborative approaches that combine AI capabilities with human expertise.''',
                'category': 'healthcare',
                'tags': ['AI', 'healthcare', 'diagnostics', 'personalized medicine'],
                'read_time': 8,
                'status': 'published',
                'is_featured': True,
            },
            {
                'title': 'AI in Finance: Beyond Fraud Detection',
                'slug': 'ai-finance-beyond-fraud-detection',
                'excerpt': 'Discover how artificial intelligence is reshaping the financial sector with applications beyond traditional fraud detection.',
                'content': '''The financial industry has been at the forefront of AI adoption, but the applications extend far beyond the well-known fraud detection systems.

## Algorithmic Trading

AI-powered trading systems can analyze market patterns, news sentiment, and economic indicators to make split-second trading decisions. These systems can process information at scales impossible for human traders.

## Risk Assessment

Machine learning models can evaluate credit risk more accurately by analyzing alternative data sources and behavioral patterns. This enables more inclusive lending while maintaining risk management standards.

## Customer Service

Intelligent chatbots and virtual assistants are transforming customer interactions, providing 24/7 support and personalized financial advice.

## Regulatory Compliance

AI systems help financial institutions stay compliant with ever-changing regulations by automatically monitoring transactions and generating compliance reports.

## The Road Ahead

As AI technology continues to evolve, we can expect even more innovative applications in areas like robo-advisory services, automated financial planning, and predictive analytics for investment strategies.''',
                'category': 'finance',
                'tags': ['AI', 'finance', 'trading', 'risk assessment'],
                'read_time': 6,
                'status': 'published',
                'is_featured': True,
            },
            {
                'title': 'Revolutionizing Education with Artificial Intelligence',
                'slug': 'revolutionizing-education-artificial-intelligence',
                'excerpt': 'Learn how AI is creating personalized learning experiences and transforming educational outcomes for students worldwide.',
                'content': '''Education is experiencing a paradigm shift as artificial intelligence technologies create more personalized, effective, and accessible learning experiences.

## Adaptive Learning

AI-powered platforms can adjust to individual learning styles, pace, and preferences. Students receive customized content and exercises that match their current understanding level.

## Intelligent Tutoring

Virtual tutors powered by AI can provide instant feedback, answer questions, and guide students through complex problems. These systems are available 24/7 and can adapt to different learning styles.

## Assessment and Analytics

AI can provide detailed analytics on student performance, identifying knowledge gaps and suggesting targeted interventions. This data-driven approach helps educators make informed decisions.

## Accessibility

AI technologies like speech recognition and natural language processing are making education more accessible to students with disabilities.

## Future Prospects

The integration of AI in education promises to create more engaging, effective, and equitable learning environments for students of all ages and backgrounds.''',
                'category': 'education',
                'tags': ['AI', 'education', 'personalized learning', 'adaptive systems'],
                'read_time': 7,
                'status': 'published',
                'is_featured': False,
            },
        ]
        
        authors = list(User.objects.filter(role__in=['admin', 'editor']))
        
        for blog_data_item in blog_data:
            post, created = BlogPost.objects.get_or_create(
                slug=blog_data_item['slug'],
                defaults={
                    **blog_data_item,
                    'author': random.choice(authors),
                    'published_at': timezone.now() - timedelta(days=random.randint(1, 30)),
                    'views_count': random.randint(50, 500),
                }
            )
            if created:
                self.stdout.write(f'Created blog post: {post.title}')

    def create_articles(self):
        articles_data = [
            {
                'title': 'AI in Healthcare: A Comprehensive Industry Report',
                'description': 'An in-depth analysis of artificial intelligence applications in healthcare, including market trends, challenges, and future opportunities.',
                'article_type': 'industry_report',
                'tags': ['healthcare', 'AI', 'market analysis', 'trends'],
                'read_time': 25,
                'is_featured': True,
            },
            {
                'title': 'Machine Learning Algorithms for Financial Risk Assessment',
                'description': 'Technical paper exploring various machine learning approaches for assessing financial risks and their practical implementations.',
                'article_type': 'research_paper',
                'tags': ['machine learning', 'finance', 'risk assessment', 'algorithms'],
                'read_time': 30,
                'is_featured': True,
            },
            {
                'title': 'Ethical AI Framework for Educational Technology',
                'description': 'White paper outlining ethical considerations and best practices for implementing AI in educational settings.',
                'article_type': 'white_paper',
                'tags': ['AI ethics', 'education', 'framework', 'best practices'],
                'read_time': 20,
                'is_featured': False,
            },
        ]
        
        authors = list(User.objects.filter(role__in=['admin', 'editor']))
        
        for article_data in articles_data:
            article, created = Article.objects.get_or_create(
                title=article_data['title'],
                defaults={
                    **article_data,
                    'author': random.choice(authors),
                    'published_at': timezone.now() - timedelta(days=random.randint(5, 60)),
                    'download_count': random.randint(10, 100),
                }
            )
            if created:
                self.stdout.write(f'Created article: {article.title}')

    def create_events(self):
        events_data = [
            {
                'title': 'AI Innovation Summit 2024',
                'description': 'Join industry leaders and AI experts for a comprehensive summit covering the latest innovations in artificial intelligence.',
                'event_type': 'conference',
                'date': date.today() + timedelta(days=30),
                'time': time(9, 0),
                'location': 'Convention Center, Tech City',
                'capacity': 500,
                'price': '$299',
                'speakers': ['Dr. Sarah Johnson', 'Michael Chen', 'Industry Expert 1', 'Industry Expert 2'],
                'agenda': [
                    'Opening Keynote: The Future of AI',
                    'Panel: AI in Healthcare',
                    'Workshop: Implementing AI Solutions',
                    'Networking Lunch',
                    'Panel: AI Ethics and Governance',
                    'Closing Remarks'
                ],
                'status': 'upcoming',
                'is_featured': True,
            },
            {
                'title': 'Machine Learning Workshop for Beginners',
                'description': 'Hands-on workshop introducing the fundamentals of machine learning for beginners and non-technical professionals.',
                'event_type': 'workshop',
                'date': date.today() + timedelta(days=15),
                'time': time(14, 0),
                'location': 'AI-Solution Training Center',
                'capacity': 50,
                'price': 'Free',
                'speakers': ['Dr. Emily Rodriguez', 'David Kim'],
                'agenda': [
                    'Introduction to Machine Learning',
                    'Hands-on Exercises',
                    'Case Studies',
                    'Q&A Session'
                ],
                'status': 'upcoming',
                'is_featured': True,
            },
            {
                'title': 'Healthcare AI Webinar Series',
                'description': 'Monthly webinar series focusing on AI applications in healthcare, featuring case studies and expert insights.',
                'event_type': 'webinar',
                'date': date.today() + timedelta(days=7),
                'time': time(11, 0),
                'location': 'Online',
                'capacity': 1000,
                'price': 'Free',
                'speakers': ['Dr. Sarah Johnson', 'Healthcare Expert'],
                'agenda': [
                    'Current State of Healthcare AI',
                    'Case Study: Diagnostic AI',
                    'Implementation Challenges',
                    'Live Q&A'
                ],
                'status': 'upcoming',
                'is_featured': False,
            },
        ]
        
        admin_user = User.objects.get(username='admin')
        
        for event_data in events_data:
            event, created = Event.objects.get_or_create(
                title=event_data['title'],
                defaults={**event_data, 'created_by': admin_user}
            )
            if created:
                self.stdout.write(f'Created event: {event.title}')

    def create_gallery_items(self):
        gallery_data = [
            {
                'title': 'AI Conference 2023 Opening Ceremony',
                'description': 'Opening ceremony of our annual AI conference with over 1000 attendees from around the world.',
                'category': 'conference',
                'event_date': date.today() - timedelta(days=90),
                'location': 'San Francisco, CA',
                'event_name': 'AI Innovation Conference 2023',
                'is_featured': True,
                'order': 1,
            },
            {
                'title': 'Healthcare AI Workshop',
                'description': 'Hands-on workshop demonstrating AI applications in healthcare with medical professionals.',
                'category': 'workshop',
                'event_date': date.today() - timedelta(days=60),
                'location': 'Boston, MA',
                'event_name': 'Healthcare AI Workshop Series',
                'is_featured': True,
                'order': 2,
            },
            {
                'title': 'AI-Solution Team Building Event',
                'description': 'Annual team building event bringing together our global team for collaboration and innovation.',
                'category': 'team_event',
                'event_date': date.today() - timedelta(days=45),
                'location': 'Lake Tahoe, CA',
                'event_name': 'Annual Team Retreat 2023',
                'is_featured': False,
                'order': 3,
            },
            {
                'title': 'Product Launch Demo',
                'description': 'Live demonstration of our latest AI healthcare solution to potential clients and partners.',
                'category': 'demo',
                'event_date': date.today() - timedelta(days=30),
                'location': 'New York, NY',
                'event_name': 'Healthcare AI Solution Launch',
                'is_featured': False,
                'order': 4,
            },
        ]
        
        admin_user = User.objects.get(username='admin')
        
        for gallery_data_item in gallery_data:
            item, created = GalleryItem.objects.get_or_create(
                title=gallery_data_item['title'],
                defaults={**gallery_data_item, 'uploaded_by': admin_user}
            )
            if created:
                self.stdout.write(f'Created gallery item: {item.title}')

    def create_feedback(self):
        feedback_data = [
            {
                'name': 'John Smith',
                'email': 'john.smith@techcorp.com',
                'company': 'TechCorp Industries',
                'rating': 5,
                'comment': 'AI-Solution transformed our healthcare operations with their diagnostic AI system. The accuracy and speed improvements have been remarkable.',
                'is_approved': True,
                'is_featured': True,
            },
            {
                'name': 'Maria Garcia',
                'email': 'maria.garcia@financeplus.com',
                'company': 'FinancePlus',
                'rating': 5,
                'comment': 'The fraud detection system has saved us millions in potential losses. The implementation was smooth and the support team is exceptional.',
                'is_approved': True,
                'is_featured': True,
            },
            {
                'name': 'Dr. Robert Wilson',
                'email': 'r.wilson@medicalcenter.org',
                'company': 'Central Medical Center',
                'rating': 4,
                'comment': 'Great AI solution for our hospital. The diagnostic assistance has improved our efficiency significantly.',
                'is_approved': True,
                'is_featured': True,
            },
            {
                'name': 'Sarah Thompson',
                'email': 'sarah.t@educorp.edu',
                'company': 'EduCorp University',
                'rating': 5,
                'comment': 'The personalized learning platform has revolutionized how we deliver education. Student engagement and outcomes have improved dramatically.',
                'is_approved': True,
                'is_featured': True,
            },
        ]
        
        admin_user = User.objects.get(username='admin')
        
        for feedback_item in feedback_data:
            feedback, created = Feedback.objects.get_or_create(
                email=feedback_item['email'],
                defaults={**feedback_item, 'approved_by': admin_user}
            )
            if created:
                self.stdout.write(f'Created feedback from: {feedback.name}')