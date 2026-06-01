# 🎨 3D Dark Art — Order Form | Complete Deployment Guide

## ✅ What's New in This Version

✨ **Professional Dark Theme** with your Brand Logo  
✨ **Animated Background Slideshow** with your 10 product images  
✨ **Complete Order Form** with all customer details  
✨ **Google Sheets Integration** — saves all orders automatically  
✨ **Success Screen** with order summary & Instagram CTA  
✨ **Mobile Responsive** — works perfectly on any device  

---

## 📁 Your Project Files

```
customer_data_project/
├── server.py                    ← Flask backend
├── requirements.txt             ← Python dependencies
├── Procfile                     ← For Render.com
├── DEPLOYMENT_GUIDE.md          ← This file
├── credentials.json             ← Your Google API key (keep secret!)
└── static/
    ├── index.html               ← Your form
    ├── Brand_Logo.png           ← Your brand logo
    └── [10 product images]      ← Your wall art samples
```

---

## 🚀 LOCAL TESTING (Your PC)

### Step 1 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Run the Server
```bash
python server.py
```

You'll see:
```
 🎨 3D Dark Art — Order Form Server
 🌐 Local:    http://localhost:5000
```

### Step 3 — Open in Browser
- **Your PC**: http://localhost:5000
- **Phone (same WiFi)**: http://YOUR_PC_IP:5000
  - Find your IP: Open CMD → type `ipconfig` → look for IPv4 Address

---

## ☁️ DEPLOY TO RENDER.COM (24/7 Live)

### Prerequisites
1. GitHub account (free at github.com)
2. Render.com account (free at render.com)

### Step 1 — Upload to GitHub

1. Go to github.com → **New Repository**
2. Name: `3d-dark-art-form`
3. Upload these files:
   - `server.py`
   - `requirements.txt`
   - `Procfile`
   - `static/index.html`
   - `static/Brand_Logo.png`
   - `static/Product_1_*.png` (all 10 images)
   - `static/*.jpeg` (all product images)

**⚠️ DO NOT upload `credentials.json`** — we'll add it as environment variable instead.

### Step 2 — Create Environment Variable

Open `credentials.json` and copy **ALL** its contents (Ctrl+A → Ctrl+C).

### Step 3 — Deploy on Render

1. Go to render.com → Sign up (free)
2. Dashboard → **New** → **Web Service**
3. Connect your GitHub repo
4. Fill in:
   - **Name**: 3d-dark-art-form
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn server:app`

5. Click **Advanced** → **Add Environment Variable**:
   - **Key**: `GOOGLE_CREDENTIALS`
   - **Value**: Paste your full `credentials.json` contents here

6. Click **Create Web Service** → Wait 2-3 minutes

### Step 4 — Share Your Live Link

Render gives you a link like:
```
https://3d-dark-art-form-xxxx.onrender.com
```

**Send this to your customers!** ✅

---

## 📊 What Gets Saved to Google Sheets

When a customer submits the form, this data saves automatically:

| Column | Example |
|---|---|
| Order ID | ORD-7429 |
| Full Name | Amit Kumar |
| Wall Art Type | Personal |
| Size | 2x2 ft |
| Budget | 5000 |
| Address | 123 Main St, Delhi |
| Pin Code | 110001 |
| State | Delhi |
| Phone No. | 9876543210 |
| Alternate Phone | 9123456789 |
| Submitted At | 2024-06-02 14:35:22 |

---

## 🔧 Troubleshooting

### Form not submitting?
- ✅ Check: Is `server.py` running?
- ✅ Check: Is `credentials.json` in the project folder?
- ✅ Check: Did you share your Google Sheet with the service account email?

### Background images not showing?
- ✅ All 10 images must be in `static/` folder
- ✅ Filenames must match exactly (case-sensitive on Linux/Render)

### Getting 404 on Render?
- ✅ Wait 3+ minutes for deployment to complete
- ✅ Check build logs for errors in Render dashboard

---

## 📱 Features

✅ **Auto-generated Order IDs** (ORD-XXXX)  
✅ **Form Validation** (10-digit phone, 6-digit pin, all required fields)  
✅ **Success Screen** with order summary  
✅ **Instagram Link** to your profile  
✅ **Dark Professional Theme** with luxury branding  
✅ **Mobile Responsive** (works perfect on phones)  
✅ **Real-time Submission** to Google Sheets  

---

## 💡 Next Steps

1. **Test locally** → `python server.py` → fill the form
2. **Deploy to Render** → Share link with customers
3. **Monitor Google Sheets** → Orders appear in real-time
4. **Track Orders** → Use Order IDs to follow up

---

## 📞 Support

If anything doesn't work:
1. Check all image filenames are correct
2. Verify Google API credentials are set up
3. Ensure all environment variables are added on Render
4. Check Render build logs for errors

Good luck! 🎨
