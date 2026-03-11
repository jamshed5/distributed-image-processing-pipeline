# Distributed Image Processing Pipeline

**Real-Time Image Processing with Redpanda, Django, Celery & PostgreSQL**

This project demonstrates a robust end-to-end system for processing images in real-time. It supports batch processing, optional ML/LLM inference, and stores processed images in PostgreSQL with media files served via Django REST API.

---

## 🚀 Features

- Real-time message queue integration using Redpanda  
- Asynchronous batch processing with Celery for scalability  
- Persistent storage of processed images in PostgreSQL  
- Optional ML / LLM inference per image  
- Clean, maintainable, and extendable architecture  
- Exposes API endpoint `/api/images/` for processed images  

---

## ⚡ Pipeline Overview

1. **Producer** reads local images and publishes them to a Redpanda topic.  
2. **Django Consumer** listens to the topic and batches image paths.  
3. **Celery Workers** process images (resize, optional ML/LLM inference).  
4. **Processed images** are saved to PostgreSQL (via Django model) and media folder.  
5. **Frontend / API clients** fetch processed images via Django REST API.

---

## 📁 Project Structure (Illustrative)

```text
distributed-image-processing-pipeline/
│
├── producer_service/                 # Python scripts to send images to Redpanda
├── process_service/                 # Django app consuming from Redpanda
├── process_service/          # Django + Celery project
│   ├── settings.py
│   ├── urls.py
│   └── celery_app.py
├── process_images/           # Django app for processing images
│   ├── models.py
│   ├── tasks.py
│   └── admin.py
├── media/                    # Processed images stored here
├── docs/                     # Flow diagrams & architecture images
└── docker/                   # Optional Docker setup for services
```

---

## 🛠 Setup Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate
# Windows
venv\Scripts\activate

# Install dependencies
pip install -r producer_service/requirements.txt
pip install -r process_service/requirements.txt
```

---

## 🚀 Running with Docker

```bash
docker-compose -f docker/docker-compose.yml up -d
```

Stop services:
```bash
docker-compose -f docker/docker-compose.yml down
```

---

## 📤 Running the Producer

```bash
cd producer_service
python producer.py
```

---

## 📥 Running the Consumer

```bash
cd process_service
# Activate venv
venv\Scripts\activate
python manage.py consume_images
```

---

## ⚡ Running Celery Workers

```bash
cd process_service
# Activate venv
venv\Scripts\activate

# Worker 1
celery -A process_service.celery_app worker --loglevel=info -P solo -n worker1@%h
# Worker 2
celery -A process_service.celery_app worker --loglevel=info -P solo -n worker2@%h
```

---

## 🗄 Inspecting PostgreSQL in Docker

```bash
docker exec -it process_service_db_v2 psql -U postgres
```

Inside `psql`:
```sql
\l
\c <database>
\dt
SELECT * FROM process_images_processedimage;
\q
```

---

## 🔹 Accessing Processed Images via API

**Endpoint:**
```
http://127.0.0.1:8000/api/images/
```

```bash
curl http://127.0.0.1:8000/api/images/
```

---

## 📊 Extending This Pipeline

1. Automated Image Scraper  
2. Video Frame Extraction & Processing  
3. AI Image Classifier  
4. Face Recognition / Object Detection  
5. Automated Image Captioning (LLM)  
6. Content Moderation System  
7. Social Media Monitoring Tool  
8. Video Thumbnail Generator  
9. E-commerce Product Image Processor  
10. End-to-End Multimedia Data Pipeline

---

## 🖼 Demo

![Demo GIF](demo_gif/demo.gif)

---

## 💻 Git Usage

```bash
# Clone project
git clone <repo-url>
cd distributed-image-processing-pipeline

# Feature branch
git checkout -b feature/your-feature-name

# Commit changes
git add .
git commit -m "Describe your changes"
git push origin feature/your-feature-name
```

---

## ⚡ Hashtags for Sharing
```
#Python #Django #Celery #Redpanda #PostgreSQL #RealTimeProcessing #DataPipeline #ML #LLM #ImageProcessing #DevOps
```

