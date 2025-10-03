1. cookies: https://microsoftedge.microsoft.com/addons/detail/cookieeditor/neaplmfkghagebokkhpjpoebhdledlfi
2. export Netscape copy to coursera_cookies.txt
3. python download_course.py "https://www.coursera.org/learn/dlai-data-storytelling/- python download_course.py "https://www.coursera.org/learn/ml-intro" "./Downloads" "./coursera_cookies.txt"

# Coursera Course Downloader - Quick Guide

This guide shows you how to easily download Coursera courses using the provided Python script.

## Prerequisites

1. **Python 3.x** installed
2. **Required packages** installed (see `requirements.txt`)
3. **Valid Coursera cookies** (for authentication)

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Your Cookies

You need a valid `CAUTH` cookie from your Coursera session. There are two ways:

#### Option A: Automatic (Using Edge Browser)

```bash
python coursera_dl.py --save-edge-cookies coursera_cookies.txt
```

**Note:** Close Microsoft Edge completely before running this command.

#### Option B: Manual (Browser Extension)

1. Install a cookie export extension (e.g., "Get cookies.txt" or "EditThisCookie")
2. Log into Coursera
3. Export cookies for `coursera.org`
4. Save as `coursera_cookies.txt`

## Usage

### Method 1: Command Line (Simple)

Download a course by providing its URL:

```bash
python download_course.py "https://www.coursera.org/learn/data-analytics-foundations"
```

**With custom output directory:**

```bash
python download_course.py "https://www.coursera.org/learn/python-for-data-analytics" "./my_courses"
```

**With custom cookies file:**

```bash
python download_course.py "https://www.coursera.org/learn/applied-statistics" "./Downloads" "./my_cookies.txt"
```

### Method 2: Import as Function (Advanced)

```python
from download_course import download_coursera_course

# Simple download
download_coursera_course("https://www.coursera.org/learn/data-analytics-foundations")

# With custom parameters
download_coursera_course(
    course_url="https://www.coursera.org/learn/python-basics",
    output_path="./my_courses",
    cookies_file="./my_cookies.txt"
)
```

### Method 3: Batch Download Multiple Courses

```python
from download_course import download_coursera_course

courses = [
    "https://www.coursera.org/learn/data-analytics-foundations",
    "https://www.coursera.org/learn/python-for-data-analytics",
    "https://www.coursera.org/learn/applied-statistics-for-data-analytics",
    "https://www.coursera.org/learn/data-io-and-preprocessing-with-python-and-sql"
]

for course_url in courses:
    print(f"\nDownloading: {course_url}")
    success = download_coursera_course(course_url)
    if success:
        print(f"✓ Successfully downloaded!")
    else:
        print(f"✗ Download failed!")
```

## Function Parameters

```python
download_coursera_course(course_url, output_path=None, cookies_file=None)
```

### Parameters:

- **`course_url`** (required): Full Coursera course URL
  - Format: `https://www.coursera.org/learn/course-name`
  - Example: `https://www.coursera.org/learn/data-analytics-foundations`

- **`output_path`** (optional): Directory where files will be saved
  - Default: `./Downloads`
  - Example: `./my_courses` or `D:/coursera/courses`

- **`cookies_file`** (optional): Path to your cookies file
  - Default: `./coursera_cookies.txt`
  - Example: `./my_cookies.txt`

### Returns:
- `True` if download was successful
- `False` if download failed

## Examples

### Example 1: Quick Download

```bash
python download_course.py "https://www.coursera.org/learn/machine-learning"
```

This downloads the course to `./Downloads/machine-learning/`

### Example 2: Custom Location

```bash
python download_course.py "https://www.coursera.org/learn/deep-learning" "D:/my_courses"
```

This downloads to `D:/my_courses/deep-learning/`

### Example 3: Python Script

Create a file `my_download.py`:

```python
from download_course import download_coursera_course

# Download DeepLearning.AI Data Analytics Certificate courses
courses = [
    "https://www.coursera.org/learn/data-analytics-foundations",
    "https://www.coursera.org/learn/python-for-data-analytics",
    "https://www.coursera.org/learn/applied-statistics-for-data-analytics",
    "https://www.coursera.org/learn/data-io-and-preprocessing-with-python-and-sql"
]

for url in courses:
    download_coursera_course(url)
```

Run it:
```bash
python my_download.py
```

## What Gets Downloaded?

For each course, you'll get:
- ✅ All video lectures (`.mp4`)
- ✅ Subtitles (`.srt`)
- ✅ Transcripts (`.txt`)
- ✅ Supplementary materials (`.xlsx`, `.pdf`, `.docx`, etc.)
- ✅ HTML pages with instructions and readings
- ✅ Practice labs and graded assignments (data files)

## File Structure

```
Downloads/
└── course-name/
    ├── 01_module-1/
    │   ├── 01_lesson-1/
    │   │   ├── 01_video-title.mp4
    │   │   ├── 01_video-title.srt
    │   │   ├── 01_video-title.txt
    │   │   └── ...
    │   └── 02_lesson-2/
    │       └── ...
    ├── 02_module-2/
    │   └── ...
    └── ...
```

## Troubleshooting

### Problem: "Cookies file not found"
**Solution:** Make sure `coursera_cookies.txt` exists in the current directory.
```bash
python coursera_dl.py --save-edge-cookies coursera_cookies.txt
```

### Problem: "Invalid Coursera URL"
**Solution:** Use the full course URL format:
```
https://www.coursera.org/learn/course-name
```

### Problem: "403 Forbidden" error
**Solution:** 
1. Make sure you're enrolled in the course
2. Re-export your cookies (they may have expired)
3. Ensure your CAUTH cookie is valid

### Problem: "No files downloaded"
**Solution:**
1. Check that cookies are valid and not empty
2. Verify you're enrolled in the course
3. Close Edge browser before extracting cookies
4. Try manually exporting cookies using a browser extension

## Advanced Usage

### Check if URL is valid before downloading:

```python
from download_course import extract_course_slug

try:
    slug = extract_course_slug("https://www.coursera.org/learn/my-course")
    print(f"Valid course slug: {slug}")
except ValueError as e:
    print(f"Invalid URL: {e}")
```

### Download with error handling:

```python
from download_course import download_coursera_course

courses = [
    "https://www.coursera.org/learn/course-1",
    "https://www.coursera.org/learn/course-2",
    "https://www.coursera.org/learn/course-3"
]

failed = []
for course_url in courses:
    try:
        if not download_coursera_course(course_url):
            failed.append(course_url)
    except Exception as e:
        print(f"Error: {e}")
        failed.append(course_url)

if failed:
    print(f"\nFailed downloads: {len(failed)}")
    for url in failed:
        print(f"  - {url}")
```

## Tips

1. **Enroll first**: Make sure you're enrolled in the course before downloading
2. **Fresh cookies**: Export cookies while logged in to Coursera
3. **Close browser**: Close Edge completely before extracting cookies automatically
4. **Check space**: Ensure you have enough disk space (courses can be 1-5 GB each)
5. **Stable connection**: Use a stable internet connection for large downloads
6. **Batch downloads**: Download during off-peak hours for better speeds

## Support

For issues or questions:
1. Check the main README.md
2. Review EDGE_COOKIES_README.md for cookie issues
3. Check the error messages in the console output

## License

This tool is for personal educational use only. Respect Coursera's Terms of Service.
