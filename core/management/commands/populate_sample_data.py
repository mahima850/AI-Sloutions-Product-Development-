from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify
from datetime import date, timedelta
import random

from core.models import (
    AboutUs, TeamMember, Solution, ContactInquiry, Feedback, 
    BlogPost, Article, GalleryItem, Event, SiteSettings
)

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the database with sample data for AI-Solution'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data for AI-Solution...')

        # Create superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@ai-solution.com',
                password='admin123',
                first_name='AI-Solution',
                last_name='Administrator',
                role='admin'
            )
            self.stdout.write(self.style.SUCCESS('✓ Created superuser (admin/admin123)'))

        # Create sample users
        users = []
        sample_users = [
            {'username': 'john_doe', 'email': 'john@ai-solution.com', 'first_name': 'John', 'last_name': 'Doe', 'role': 'editor'},
            {'username': 'jane_smith', 'email': 'jane@ai-solution.com', 'first_name': 'Jane', 'last_name': 'Smith', 'role': 'editor'},
            {'username': 'mike_wilson', 'email': 'mike@ai-solution.com', 'first_name': 'Mike', 'last_name': 'Wilson', 'role': 'viewer'},
        ]

        for user_data in sample_users:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'role': user_data['role'],
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)

        # Create Site Settings
        settings, created = SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': 'AI-Solution',
                'site_description': 'Empowering Businesses with AI',
                'contact_email': 'info@ai-solution.com',
                'contact_phone': '+1 (555) 123-4567',
                'address': '123 AI Street, Tech City, TC 12345, USA',
                'social_linkedin': 'https://linkedin.com/company/ai-solution',
                'social_twitter': 'https://twitter.com/aisolution',
                'chatbot_enabled': True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created site settings'))

        # Create About Us
        about_us, created = AboutUs.objects.get_or_create(
            pk=1,
            defaults={
                'title': 'About AI-Solution',
                'company_background': '''
                    <h3>Leading the AI Revolution</h3>
                    <p>Since our founding in 2019, AI-Solution has been at the forefront of artificial intelligence innovation, 
                    helping businesses across industries harness the transformative power of AI technology.</p>
                    
                    <p>Our team of world-class data scientists, engineers, and AI researchers work collaboratively to develop 
                    cutting-edge solutions that drive real business value. We believe that AI should be accessible, ethical, 
                    and beneficial for all organizations, regardless of size or industry.</p>
                    
                    <h4>Our Approach</h4>
                    <p>We combine deep technical expertise with industry knowledge to deliver AI solutions that are not just 
                    innovative, but practical and scalable. Our methodology focuses on understanding your unique challenges 
                    and creating tailored solutions that integrate seamlessly into your existing workflows.</p>
                ''',
                'mission': '''
                    <p><strong>To democratize artificial intelligence by making advanced AI solutions accessible, 
                    ethical, and beneficial for businesses of all sizes.</strong></p>
                    
                    <p>We strive to bridge the gap between cutting-edge AI research and practical business applications, 
                    ensuring that every organization can leverage the power of artificial intelligence to improve 
                    efficiency, drive innovation, and create value.</p>
                ''',
                'vision': '''
                    <p><strong>To create a world where AI enhances human potential and drives sustainable progress 
                    across all industries.</strong></p>
                    
                    <p>We envision a future where artificial intelligence works hand-in-hand with human creativity 
                    and expertise, enabling breakthrough innovations in healthcare, finance, education, and beyond. 
                    Our goal is to be the trusted partner that helps organizations navigate this AI-driven transformation.</p>
                ''',
                'values': '''
                    <ul>
                        <li><strong>Innovation:</strong> We continuously push the boundaries of what's possible with AI</li>
                        <li><strong>Ethics:</strong> We develop responsible AI that respects privacy and promotes fairness</li>
                        <li><strong>Collaboration:</strong> We work closely with clients to understand and solve their unique challenges</li>
                        <li><strong>Excellence:</strong> We deliver high-quality solutions that exceed expectations</li>
                        <li><strong>Transparency:</strong> We believe in open communication and explainable AI systems</li>
                    </ul>
                ''',
                'clients_count': 500,
                'countries_count': 25,
                'success_rate': 98,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created About Us content'))

        # Create Team Members
        team_members = [
            {
                'name': 'Dr. Sarah Chen',
                'role': 'Chief Executive Officer & Founder',
                'bio': '''<p>Dr. Sarah Chen is a visionary leader with over 15 years of experience in artificial intelligence 
                         and machine learning. She holds a Ph.D. in Computer Science from MIT and has published over 50 
                         research papers in top-tier AI conferences.</p>
                         <p>Before founding AI-Solution, Sarah led AI initiatives at Google and Microsoft, where she 
                         developed groundbreaking algorithms for natural language processing and computer vision.</p>''',
                'email': 'sarah.chen@ai-solution.com',
                'linkedin_url': 'https://linkedin.com/in/sarahchen',
                'order': 1,
            },
            {
                'name': 'Dr. Michael Rodriguez',
                'role': 'Chief Technology Officer',
                'bio': '''<p>Dr. Michael Rodriguez is a renowned AI researcher and engineer with expertise in deep learning, 
                         neural networks, and distributed systems. He earned his Ph.D. in Electrical Engineering from Stanford.</p>
                         <p>Michael has been instrumental in developing our core AI platform and has led the technical 
                         teams that have delivered solutions for Fortune 500 companies across multiple industries.</p>''',
                'email': 'michael.rodriguez@ai-solution.com',
                'linkedin_url': 'https://linkedin.com/in/michaelrodriguez',
                'order': 2,
            },
            {
                'name': 'Emma Thompson',
                'role': 'VP of Business Development',
                'bio': '''<p>Emma Thompson brings over 12 years of experience in business development and strategic partnerships 
                         in the technology sector. She has an MBA from Wharton and a background in consulting.</p>
                         <p>Emma has been key in establishing partnerships with leading healthcare, finance, and education 
                         organizations, helping them successfully implement AI solutions that drive measurable business impact.</p>''',
                'email': 'emma.thompson@ai-solution.com',
                'linkedin_url': 'https://linkedin.com/in/emmathompson',
                'order': 3,
            },
            {
                'name': 'Dr. James Kim',
                'role': 'Head of Research',
                'bio': '''<p>Dr. James Kim is a leading researcher in machine learning and AI ethics. He holds a Ph.D. in 
                         Computer Science from Carnegie Mellon and has been published in Nature, Science, and other 
                         prestigious journals.</p>
                         <p>James leads our research initiatives in responsible AI and ensures that all our solutions 
                         meet the highest standards of ethical AI development and deployment.</p>''',
                'email': 'james.kim@ai-solution.com',
                'linkedin_url': 'https://linkedin.com/in/jameskim',
                'order': 4,
            },
        ]

        for member_data in team_members:
            member, created = TeamMember.objects.get_or_create(
                name=member_data['name'],
                defaults=member_data
            )
            if created:
                self.stdout.write(f'✓ Created team member: {member.name}')

        # Create Solutions
        solutions = [
            {
                'title': 'AI-Powered Diagnostic Assistant',
                'description': 'Advanced machine learning algorithms that assist medical professionals in accurate diagnosis and treatment planning.',
                'detailed_content': '''
                    <h3>Revolutionizing Healthcare Diagnostics</h3>
                    <p>Our AI-Powered Diagnostic Assistant leverages state-of-the-art deep learning models to analyze medical images, 
                    patient data, and clinical histories to provide accurate diagnostic recommendations.</p>
                    
                    <h4>How It Works</h4>
                    <p>The system integrates seamlessly with existing hospital information systems and PACS (Picture Archiving and 
                    Communication Systems) to provide real-time analysis of:</p>
                    <ul>
                        <li>Medical imaging (X-rays, CT scans, MRIs)</li>
                        <li>Laboratory results and biomarkers</li>
                        <li>Patient medical history and symptoms</li>
                        <li>Clinical guidelines and best practices</li>
                    </ul>
                    
                    <h4>Clinical Validation</h4>
                    <p>Our diagnostic assistant has been validated in clinical trials across 15 major hospitals, showing a 94% 
                    accuracy rate in identifying key conditions and a 40% reduction in diagnostic time.</p>
                ''',
                'category': 'healthcare',
                'icon': 'heart-pulse',
                'features': [
                    'Real-time medical image analysis',
                    'Multi-modal data integration',
                    'Clinical decision support',
                    'HIPAA compliant security',
                    'Seamless EHR integration',
                    'Continuous learning algorithms'
                ],
                'benefits': [
                    'Improved diagnostic accuracy',
                    'Reduced time to diagnosis',
                    'Lower healthcare costs',
                    'Enhanced patient outcomes',
                    'Reduced physician burnout',
                    'Standardized care protocols'
                ],
                'use_cases': [
                    'Radiology image interpretation',
                    'Pathology analysis',
                    'Cardiology assessment',
                    'Emergency room triage',
                    'Rare disease detection',
                    'Treatment recommendation'
                ],
                'faqs': [
                    {
                        'question': 'How accurate is the diagnostic assistant?',
                        'answer': 'Our system achieves 94% accuracy in clinical trials, comparable to experienced specialists in many diagnostic scenarios.'
                    },
                    {
                        'question': 'Is the system HIPAA compliant?',
                        'answer': 'Yes, all patient data is encrypted and processed in compliance with HIPAA regulations and international privacy standards.'
                    },
                    {
                        'question': 'How does it integrate with existing systems?',
                        'answer': 'Our solution uses standard healthcare APIs (HL7 FHIR) to integrate seamlessly with most EHR systems and medical devices.'
                    }
                ],
                'is_featured': True,
                'order': 1,
            },
            {
                'title': 'Intelligent Fraud Detection System',
                'description': 'Real-time fraud detection and prevention using advanced machine learning and behavioral analytics.',
                'detailed_content': '''
                    <h3>Next-Generation Fraud Prevention</h3>
                    <p>Our Intelligent Fraud Detection System uses advanced machine learning algorithms and real-time behavioral 
                    analytics to identify and prevent fraudulent activities across all financial transactions.</p>
                    
                    <h4>Advanced Analytics Engine</h4>
                    <p>The system analyzes multiple data points in real-time:</p>
                    <ul>
                        <li>Transaction patterns and anomalies</li>
                        <li>User behavior and device fingerprinting</li>
                        <li>Geographic and temporal analysis</li>
                        <li>Network analysis and relationship mapping</li>
                    </ul>
                    
                    <h4>Proven Results</h4>
                    <p>Financial institutions using our system report a 95% reduction in successful fraud attempts 
                    and a 60% decrease in false positives, resulting in improved customer experience and significant cost savings.</p>
                ''',
                'category': 'finance',
                'icon': 'shield-check',
                'features': [
                    'Real-time transaction monitoring',
                    'Behavioral biometrics',
                    'Machine learning algorithms',
                    'Risk scoring engine',
                    'Automated case management',
                    'Customizable rule engine'
                ],
                'benefits': [
                    '95% fraud detection rate',
                    '60% reduction in false positives',
                    'Real-time prevention',
                    'Improved customer experience',
                    'Regulatory compliance',
                    'Significant cost savings'
                ],
                'use_cases': [
                    'Credit card fraud prevention',
                    'Account takeover protection',
                    'Payment fraud detection',
                    'Identity theft prevention',
                    'Money laundering detection',
                    'Insurance fraud identification'
                ],
                'faqs': [
                    {
                        'question': 'How fast is the fraud detection?',
                        'answer': 'Our system processes transactions in under 50 milliseconds, enabling real-time fraud prevention without impacting user experience.'
                    },
                    {
                        'question': 'Does it work with existing banking systems?',
                        'answer': 'Yes, our solution integrates with all major core banking systems and payment processors through secure APIs.'
                    },
                    {
                        'question': 'How does it handle false positives?',
                        'answer': 'Our advanced algorithms continuously learn from feedback, reducing false positives by 60% compared to traditional rule-based systems.'
                    }
                ],
                'is_featured': True,
                'order': 2,
            },
            {
                'title': 'Adaptive Learning Platform',
                'description': 'Personalized education technology that adapts to individual learning styles and pace for optimal outcomes.',
                'detailed_content': '''
                    <h3>Transforming Education Through AI</h3>
                    <p>Our Adaptive Learning Platform revolutionizes education by creating personalized learning experiences 
                    that adapt in real-time to each student's needs, learning style, and pace.</p>
                    
                    <h4>Intelligent Content Delivery</h4>
                    <p>The platform uses sophisticated AI algorithms to:</p>
                    <ul>
                        <li>Assess individual learning styles and preferences</li>
                        <li>Identify knowledge gaps and strengths</li>
                        <li>Recommend optimal learning paths</li>
                        <li>Provide personalized content and assessments</li>
                    </ul>
                    
                    <h4>Measurable Impact</h4>
                    <p>Educational institutions using our platform report a 35% improvement in student engagement, 
                    28% increase in learning outcomes, and 50% reduction in dropout rates.</p>
                ''',
                'category': 'education',
                'icon': 'book',
                'features': [
                    'Personalized learning paths',
                    'Real-time progress tracking',
                    'Adaptive content delivery',
                    'Performance analytics',
                    'Multi-media content support',
                    'Collaborative learning tools'
                ],
                'benefits': [
                    '35% increase in engagement',
                    '28% improvement in outcomes',
                    '50% reduction in dropout rates',
                    'Personalized learning experience',
                    'Teacher efficiency gains',
                    'Data-driven insights'
                ],
                'use_cases': [
                    'K-12 curriculum delivery',
                    'Higher education courses',
                    'Corporate training programs',
                    'Professional certification',
                    'Language learning',
                    'Skill development programs'
                ],
                'faqs': [
                    {
                        'question': 'How does the platform personalize learning?',
                        'answer': 'Our AI analyzes learning patterns, performance data, and preferences to create unique learning paths for each student.'
                    },
                    {
                        'question': 'Is it suitable for all age groups?',
                        'answer': 'Yes, our platform adapts content and interface design for learners from elementary school through professional development.'
                    },
                    {
                        'question': 'Can teachers customize the content?',
                        'answer': 'Absolutely. Teachers have full control over content creation, curriculum mapping, and assessment criteria.'
                    }
                ],
                'is_featured': True,
                'order': 3,
            },
        ]

        admin_user = User.objects.get(username='admin')
        for solution_data in solutions:
            solution, created = Solution.objects.get_or_create(
                title=solution_data['title'],
                defaults={**solution_data, 'created_by': admin_user}
            )
            if created:
                self.stdout.write(f'✓ Created solution: {solution.title}')

        # Create Blog Posts
        blog_posts = [
            {
                'title': 'The Future of AI in Healthcare: Transforming Patient Care',
                'slug': 'future-ai-healthcare-patient-care',
                'excerpt': 'Exploring how artificial intelligence is revolutionizing healthcare delivery and improving patient outcomes worldwide.',
                'content': '''
                    <p>Artificial Intelligence is reshaping the healthcare landscape in unprecedented ways. From diagnostic imaging 
                    to drug discovery, AI technologies are enabling healthcare providers to deliver more accurate, efficient, 
                    and personalized care to patients.</p>
                    
                    <h3>Key Areas of AI Impact</h3>
                    
                    <h4>1. Medical Imaging and Diagnostics</h4>
                    <p>AI-powered imaging systems can now detect diseases like cancer, cardiovascular conditions, and neurological 
                    disorders with accuracy that matches or exceeds human specialists. These systems can analyze thousands of 
                    images in minutes, providing rapid diagnosis that can be life-saving.</p>
                    
                    <h4>2. Drug Discovery and Development</h4>
                    <p>Traditional drug development can take 10-15 years and cost billions of dollars. AI is accelerating this 
                    process by identifying potential drug compounds, predicting their effects, and optimizing clinical trials.</p>
                    
                    <h4>3. Personalized Treatment Plans</h4>
                    <p>By analyzing vast amounts of patient data, AI can help create personalized treatment plans that consider 
                    individual genetic profiles, medical history, and lifestyle factors.</p>
                    
                    <h3>Challenges and Considerations</h3>
                    <p>While the potential is enormous, healthcare AI faces challenges including data privacy, regulatory 
                    compliance, and the need for clinical validation. Success requires careful collaboration between 
                    technologists and healthcare professionals.</p>
                    
                    <h3>Looking Ahead</h3>
                    <p>The future of healthcare AI looks bright, with emerging technologies like quantum computing and 
                    advanced neural networks promising even greater breakthroughs in medical care.</p>
                ''',
                'category': 'healthcare',
                'tags': ['AI', 'healthcare', 'diagnostics', 'future'],
                'read_time': 8,
                'status': 'published',
                'is_featured': True,
            },
            {
                'title': 'Machine Learning in Financial Services: Beyond Fraud Detection',
                'slug': 'machine-learning-financial-services',
                'excerpt': 'Discover how financial institutions are leveraging ML for risk assessment, algorithmic trading, and customer experience.',
                'content': '''
                    <p>While fraud detection often gets the spotlight, machine learning applications in financial services 
                    extend far beyond security. Financial institutions are using ML to transform every aspect of their 
                    operations, from customer service to investment strategies.</p>
                    
                    <h3>Credit Risk Assessment</h3>
                    <p>ML models can analyze thousands of variables to assess credit risk more accurately than traditional 
                    methods. This enables more inclusive lending while reducing default rates.</p>
                    
                    <h4>Alternative Data Sources</h4>
                    <ul>
                        <li>Social media activity patterns</li>
                        <li>Mobile phone usage data</li>
                        <li>E-commerce transaction history</li>
                        <li>Utility payment records</li>
                    </ul>
                    
                    <h3>Algorithmic Trading</h3>
                    <p>High-frequency trading systems use ML to identify market patterns and execute trades in microseconds. 
                    These systems can process news, social media sentiment, and market data simultaneously to make trading decisions.</p>
                    
                    <h3>Customer Experience Enhancement</h3>
                    <p>Chatbots and virtual assistants powered by natural language processing are handling routine customer 
                    inquiries, while recommendation engines suggest relevant financial products based on customer behavior.</p>
                    
                    <h3>Regulatory Compliance</h3>
                    <p>ML is helping financial institutions stay compliant with ever-changing regulations by automatically 
                    monitoring transactions and flagging potential violations.</p>
                ''',
                'category': 'finance',
                'tags': ['machine learning', 'fintech', 'trading', 'risk'],
                'read_time': 6,
                'status': 'published',
            },
            {
                'title': 'Personalized Learning: How AI is Revolutionizing Education',
                'slug': 'personalized-learning-ai-education',
                'excerpt': 'Examining the role of artificial intelligence in creating adaptive learning experiences for students of all ages.',
                'content': '''
                    <p>The traditional one-size-fits-all approach to education is being transformed by AI-powered personalized 
                    learning systems that adapt to individual student needs, learning styles, and pace.</p>
                    
                    <h3>Understanding Learning Styles</h3>
                    <p>AI systems can identify whether a student learns better through visual, auditory, or kinesthetic methods, 
                    and adjust content delivery accordingly. This personalization leads to improved comprehension and retention.</p>
                    
                    <h4>Adaptive Content Delivery</h4>
                    <p>Based on real-time assessment of student performance, AI can:</p>
                    <ul>
                        <li>Provide additional practice problems for struggling concepts</li>
                        <li>Accelerate through mastered material</li>
                        <li>Offer alternative explanations and examples</li>
                        <li>Suggest optimal study schedules</li>
                    </ul>
                    
                    <h3>Teacher Support and Insights</h3>
                    <p>AI doesn't replace teachers; it empowers them with detailed analytics about student progress, 
                    identifies at-risk students early, and suggests intervention strategies.</p>
                    
                    <h3>Accessibility and Inclusion</h3>
                    <p>AI-powered tools are making education more accessible by providing real-time transcription, 
                    language translation, and adaptive interfaces for students with disabilities.</p>
                    
                    <h3>The Future of AI in Education</h3>
                    <p>Emerging technologies like virtual reality and natural language processing will create even more 
                    immersive and interactive learning experiences.</p>
                ''',
                'category': 'education',
                'tags': ['education', 'personalized learning', 'AI', 'students'],
                'read_time': 7,
                'status': 'published',
                'is_featured': True,
            },
        ]

        for blog_data in blog_posts:
            blog_post, created = BlogPost.objects.get_or_create(
                slug=blog_data['slug'],
                defaults={
                    **blog_data,
                    'author': admin_user,
                    'published_at': timezone.now() - timedelta(days=random.randint(1, 30)),
                    'views_count': random.randint(50, 500),
                }
            )
            if created:
                self.stdout.write(f'✓ Created blog post: {blog_post.title}')

        # Create Articles
        articles = [
            {
                'title': 'AI Adoption in Enterprise: A Comprehensive Guide',
                'description': '''<p>This comprehensive white paper provides enterprise leaders with a strategic framework 
                                 for successful AI adoption, including implementation roadmaps, ROI calculation methods, 
                                 and risk mitigation strategies.</p>''',
                'article_type': 'white_paper',
                'tags': ['enterprise', 'AI adoption', 'strategy'],
                'read_time': 25,
            },
            {
                'title': 'Healthcare AI Market Analysis 2024',
                'description': '''<p>An in-depth analysis of the healthcare AI market, including growth trends, 
                                 key players, regulatory landscape, and investment opportunities in the sector.</p>''',
                'article_type': 'market_analysis',
                'tags': ['healthcare', 'market analysis', 'AI'],
                'read_time': 20,
            },
            {
                'title': 'Ethical AI Development Framework',
                'description': '''<p>A technical paper outlining best practices for developing ethical AI systems, 
                                 including bias detection, fairness metrics, and responsible deployment strategies.</p>''',
                'article_type': 'framework_guide',
                'tags': ['ethics', 'AI development', 'framework'],
                'read_time': 30,
            },
        ]

        for article_data in articles:
            article, created = Article.objects.get_or_create(
                title=article_data['title'],
                defaults={**article_data, 'author': admin_user}
            )
            if created:
                self.stdout.write(f'✓ Created article: {article.title}')

        # Create Events
        events = [
            {
                'title': 'AI Innovation Summit 2024',
                'description': '''<p>Join industry leaders, researchers, and innovators for a comprehensive exploration 
                                 of the latest AI breakthroughs and their practical applications across industries.</p>
                                 <p>This summit features keynote presentations, panel discussions, and hands-on workshops 
                                 covering machine learning, natural language processing, computer vision, and AI ethics.</p>''',
                'event_type': 'conference',
                'date': date.today() + timedelta(days=45),
                'time': '09:00:00',
                'location': 'San Francisco Convention Center, CA',
                'capacity': 500,
                'price': '$299',
                'speakers': [
                    'Dr. Sarah Chen - AI-Solution CEO',
                    'Prof. Andrew Martinez - Stanford AI Lab',
                    'Lisa Wang - Google AI Research',
                    'Dr. James Thompson - MIT CSAIL'
                ],
                'agenda': [
                    '9:00 AM - Registration & Networking',
                    '10:00 AM - Opening Keynote: The Future of AI',
                    '11:30 AM - Panel: AI in Healthcare',
                    '1:00 PM - Lunch & Networking',
                    '2:00 PM - Workshop: Implementing AI in Business',
                    '4:00 PM - Closing Remarks & Next Steps'
                ],
                'status': 'upcoming',
                'is_featured': True,
            },
            {
                'title': 'Healthcare AI Workshop Series',
                'description': '''<p>A hands-on workshop designed for healthcare professionals looking to understand 
                                 and implement AI solutions in their practice.</p>
                                 <p>Participants will learn about diagnostic AI, predictive analytics, and patient 
                                 management systems through interactive sessions and case studies.</p>''',
                'event_type': 'workshop',
                'date': date.today() + timedelta(days=21),
                'time': '14:00:00',
                'location': 'Online Webinar',
                'capacity': 100,
                'price': 'Free',
                'speakers': [
                    'Dr. Michael Rodriguez - AI-Solution CTO',
                    'Dr. Patricia Lewis - Johns Hopkins Hospital',
                    'Mark Chen - Healthcare AI Specialist'
                ],
                'agenda': [
                    '2:00 PM - Introduction to Healthcare AI',
                    '2:30 PM - Case Study: Diagnostic Imaging',
                    '3:15 PM - Break',
                    '3:30 PM - Hands-on Demo',
                    '4:15 PM - Q&A Session',
                    '4:45 PM - Closing & Resources'
                ],
                'status': 'upcoming',
            },
        ]

        for event_data in events:
            event, created = Event.objects.get_or_create(
                title=event_data['title'],
                defaults={**event_data, 'created_by': admin_user}
            )
            if created:
                self.stdout.write(f'✓ Created event: {event.title}')

        # Create Gallery Items
        gallery_items = [
            {
                'title': 'AI Summit 2023 Keynote',
                'description': '''<p>Dr. Sarah Chen delivering the opening keynote at the 2023 AI Innovation Summit, 
                                 discussing the future of artificial intelligence in healthcare.</p>''',
                'category': 'conference',
                'event_date': date(2023, 10, 15),
                'location': 'San Francisco Convention Center',
                'event_name': 'AI Innovation Summit 2023',
                'is_featured': True,
            },
            {
                'title': 'Healthcare AI Demo Day',
                'description': '''<p>Live demonstration of our diagnostic AI assistant at the Healthcare Technology 
                                 Conference, showcasing real-time medical image analysis.</p>''',
                'category': 'demo',
                'event_date': date(2023, 9, 20),
                'location': 'Boston Medical Center',
                'event_name': 'HealthTech Conference 2023',
            },
            {
                'title': 'Team Innovation Workshop',
                'description': '''<p>Our research team collaborating on breakthrough algorithms for natural language 
                                 processing during our quarterly innovation workshop.</p>''',
                'category': 'team_event',
                'event_date': date(2023, 11, 5),
                'location': 'AI-Solution Headquarters',
                'event_name': 'Q4 Innovation Workshop',
            },
        ]

        for gallery_data in gallery_items:
            gallery_item, created = GalleryItem.objects.get_or_create(
                title=gallery_data['title'],
                defaults={**gallery_data, 'uploaded_by': admin_user}
            )
            if created:
                self.stdout.write(f'✓ Created gallery item: {gallery_item.title}')

        # Create Sample Feedback
        feedback_entries = [
            {
                'name': 'Dr. Jennifer Martinez',
                'email': 'j.martinez@cityhospital.com',
                'company': 'City General Hospital',
                'rating': 5,
                'comment': 'The AI diagnostic assistant has revolutionized our radiology department. We\'ve seen a 40% improvement in diagnosis speed and accuracy.',
                'is_approved': True,
                'is_featured': True,
            },
            {
                'name': 'Robert Kim',
                'email': 'r.kim@securebank.com',
                'company': 'SecureBank Financial',
                'rating': 5,
                'comment': 'AI-Solution\'s fraud detection system has saved us millions in prevented losses. The false positive rate is impressively low.',
                'is_approved': True,
                'is_featured': True,
            },
            {
                'name': 'Prof. Maria Garcia',
                'email': 'm.garcia@techuniversity.edu',
                'company': 'Tech University',
                'rating': 4,
                'comment': 'Our students are more engaged than ever with the adaptive learning platform. The personalization features are outstanding.',
                'is_approved': True,
            },
        ]

        for feedback_data in feedback_entries:
            feedback, created = Feedback.objects.get_or_create(
                email=feedback_data['email'],
                defaults=feedback_data
            )
            if created:
                self.stdout.write(f'✓ Created feedback from: {feedback.name}')

        self.stdout.write(
            self.style.SUCCESS('\n🎉 Successfully populated AI-Solution with sample data!')
        )
        self.stdout.write('📋 Summary:')
        self.stdout.write(f'  • Users: {User.objects.count()}')
        self.stdout.write(f'  • Solutions: {Solution.objects.count()}')
        self.stdout.write(f'  • Blog Posts: {BlogPost.objects.count()}')
        self.stdout.write(f'  • Articles: {Article.objects.count()}')
        self.stdout.write(f'  • Events: {Event.objects.count()}')
        self.stdout.write(f'  • Gallery Items: {GalleryItem.objects.count()}')
        self.stdout.write(f'  • Feedback Entries: {Feedback.objects.count()}')
        self.stdout.write(f'  • Team Members: {TeamMember.objects.count()}')
        self.stdout.write('\n🔐 Admin credentials: admin / admin123')