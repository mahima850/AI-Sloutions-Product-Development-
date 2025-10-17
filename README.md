# 🧠 AI-Solution – Full-Stack Django Web Application  

**Author:** Mahima Saru  
**Course:** CET333 Product Development  
**Programme:** BSc (Hons) Computer Systems Engineering  
**Institution:** International School of Management and Technology  

---

## 📘 Overview  

**AI-Solution** is a full-stack Django-based web application designed for a fictional company delivering **AI-powered tools** across Healthcare, Finance, and Education industries.  
The project demonstrates a modular, database-driven system capable of managing company solutions, blogs, events, galleries, and feedback, while supporting secure contact and inquiry submissions.  

Developed using **Django 5.x**, **Python 3.x**, **Bootstrap 5**, and **MySQL**, the project emphasizes performance, scalability, and responsiveness. It serves as a comprehensive academic demonstration of full-stack software engineering principles.

---

## ⚙️ Features  

### 🌐 User Features
- Responsive, mobile-friendly design using Bootstrap 5.
- Hero section with tagline “Empowering Businesses with AI”.
- Navigation bar linking to all sections: Home, About, Solutions, Blog, Articles, Events, Gallery, Feedback, and Contact.
- Solutions showcase with filterable industry cards (Healthcare, Finance, Education).
- Blog and Articles for AI news, tutorials, and research.
- Gallery of promotional and event photos with captions.
- Event management for past and upcoming activities.
- Contact form with file upload and inquiry tracking.
- Feedback system with star ratings and comment moderation.
- Integrated chatbot answering FAQs about AI-Solution services.

### 🔐 Admin Features
- Secure authentication and password hashing.
- CRUD operations (Add/Edit/Delete/Search) across all modules:
  - Solutions  
  - Blogs & Articles  
  - Events  
  - Gallery  
  - Feedback  
  - Inquiries  
- Feedback moderation (Approve/Reject).
- CSV export for inquiries and feedback.
- Dynamic admin dashboard for managing all website content.
- Role-based access (Admin, Editor, Viewer).
- Change password and profile management.

---

## 🧩 System Architecture  

**Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript  
**Backend:** Django 5.x (Python 3.x)  
**Database:** SQLite (development) → MySQL (production)  
**Hosting:** PythonAnywhere (backend) + optional Netlify (static assets)  

**Architecture Highlights:**  
- MVC-inspired Django MVT pattern  
- Django ORM for database interaction  
- Template inheritance for reusable frontend components  
- REST-ready endpoints for chatbot and data export  

---

## 🧠 Core Functionalities  

| Module | Description |
|--------|--------------|
| **About Us** | Editable mission, vision, and team details. |
| **Solutions** | CRUD with images, active toggle, and filter categories. |
| **Blog/Articles** | Publish, edit, delete posts with TinyMCE editor. |
| **Gallery** | Upload event images with captions and featured flags. |
| **Events** | Create upcoming/past events with date, time, and description. |
| **Contact** | Inquiry form with validation and file upload. |
| **Feedback** | Star rating, comment approval, and moderation. |
| **Chatbot** | Keyword-based auto-response system for FAQs. |

---

## 🧰 Tools and Dependencies  

| Tool / Library | Purpose |
|----------------|----------|
| **Django 5.x** | Web framework |
| **Python 3.10+** | Backend logic |
| **Bootstrap 5** | Frontend responsiveness |
| **MySQL** | Relational database |
| **Crispy Forms** | Better form styling |
| **Pillow** | Image handling |
| **TinyMCE** | Rich text editor |
| **Django Filter** | Data filtering |
| **python-decouple** | Environment variable management |
| **pymysql** | MySQL driver |
| **Gunicorn / WSGI** | Production server |
| **Git + GitHub** | Version control |

---

## 💻 Installation Guide  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/mahimasaru/ai-solution.git
