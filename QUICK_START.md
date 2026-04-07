# Quick Start Guide - Coursera Course Downloader

## 🚀 Get Started in 3 Steps

### Step 1: Prepare Your Cookies

Close Microsoft Edge completely, then run:

```bash
python coursera_dl.py --save-edge-cookies coursera_cookies.txt
```

### Step 2: Download a Course

```bash
python coursera_dl.py "https://www.coursera.org/learn/YOUR-COURSE-NAME"
```

### Step 3: Find Your Downloaded Files

Files will be in: `./Downloads/YOUR-COURSE-NAME/`

---

## 📚 Common Commands

### Download a single course:
```bash
python coursera_dl.py "https://www.coursera.org/learn/data-analytics-foundations"
```

### Download with the main CLI and a cookie file:
```bash
python coursera_dl.py --cookies_file coursera_cookies.txt data-analytics-foundations
```

### Download to specific folder:
```bash
python coursera_dl.py "https://www.coursera.org/learn/python-basics" "./my_courses"
```

### Download multiple courses (Python script):
```python
from coursera_dl import download_coursera_course

courses = [
    "https://www.coursera.org/learn/course-1",
    "https://www.coursera.org/learn/course-2",
    "https://www.coursera.org/learn/course-3"
]

for course in courses:
    download_coursera_course(course)
```

---

## ✅ What You Get

Each course download includes:
- 📹 All video lectures (MP4)
- 📝 Subtitles (SRT) and transcripts (TXT)
- 📊 Practice materials (Excel, PDFs, datasets)
- 📖 HTML readings and instructions

---

## ❓ Troubleshooting

**Q: Cookies not found?**
```bash
python coursera_dl.py --save-edge-cookies coursera_cookies.txt
```

**Q: 403 Forbidden error?**
- Enroll in the course first
- Re-export your cookies

**Q: No files downloaded?**
- Close Edge browser
- Make sure you're enrolled
- Check cookie file is not empty

**Q: Download appears stuck on one file?**
- The downloader now enforces 30s timeout per file
- It retries once and then skips the file automatically
- Review failed URLs at the end of the run

---

## 📖 Full Documentation

- **Detailed Guide**: See `DOWNLOAD_GUIDE.md`
- **Cookie Help**: See `EDGE_COOKIES_README.md`
- **Main README**: See `README.md`

## 🎓 Example: Download Entire Certificate Program

```python
# download_data_analytics_certificate.py
from coursera_dl import download_coursera_course

# DeepLearning.AI Data Analytics Professional Certificate
courses = [
    "https://www.coursera.org/learn/data-analytics-foundations",
    "https://www.coursera.org/learn/python-for-data-analytics", 
    "https://www.coursera.org/learn/applied-statistics-for-data-analytics",
    "https://www.coursera.org/learn/data-io-and-preprocessing-with-python-and-sql"
]

print("Downloading DeepLearning.AI Data Analytics Certificate...")
for i, course in enumerate(courses, 1):
    print(f"\n[{i}/{len(courses)}] Downloading course...")
    download_coursera_course(course)
    
print("\n✓ All courses downloaded!")
```

Run it:
```bash
python download_data_analytics_certificate.py
```

---

**Happy Learning! 🎓**














































































