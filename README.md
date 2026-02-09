# Social Feed Experience

A full-stack social media feed application that allows users to create posts with text, images, and videos, and view them in a chronological feed.

## Live Demo

* Frontend (Vercel): https://social-feed-experience.vercel.app
* Backend API (Render): https://social-feed-experience-api.onrender.com/api/posts/

---

## Features

* Create posts with:

  * Text content
  * Multiple images
  * Multiple videos
* Media validation (file type and size limits)
* Chronological feed (latest posts first)
* Inline image preview and video playback
* Cloud media storage integration
* Responsive user interface

---

## Tech Stack

**Frontend**

* Vue 3 (Composition API)
* Axios for API requests
* Vite for build and development

**Backend**

* Python
* Django
* Django REST Framework

**Deployment**

* Frontend: Vercel
* Backend: Render

**Storage**

* Cloudinary (media hosting)

---

## Architecture Overview

Client (Vue) → REST API (Django) → Database & Cloud Storage

* Vue sends HTTP requests using Axios
* Django REST API handles post creation and retrieval
* Media files are uploaded to Cloudinary
* Posts and metadata are stored in the database

---

## Project Structure

```
Social-Feed-Experience/
│
├── Django/
│   ├── config/
│   ├── posts/
│   └── manage.py
│
├── Vue/
│   ├── src/
│   ├── components/
│   └── services/
│
└── README.md
```

---



Frontend runs at:
[http://localhost:5173](http://localhost:5173)

---

## Environment Variables

### Frontend (.env)

```
VITE_API_BASE_URL=https://your-render-url.onrender.com
```

### Backend

Configure environment variables for:

* Cloudinary credentials
* Allowed hosts
* CORS settings


---

## Key Learning Outcomes

* Built a full-stack application using Django and Vue
* Implemented file uploads with cloud storage
* Designed RESTful APIs and frontend integration
* Deployed production-ready applications on Render and Vercel

---

