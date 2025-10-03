# Coursera Full Course Downloader

A comprehensive tool for downloading Coursera course materials including videos, subtitles, transcripts, assignments, and supplementary resources. Available as both a **graphical user interface (GUI)** application and a **command-line interface (CLI)** tool.

## 📋 Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [GUI Application](#gui-application)
  - [Command Line Interface](#command-line-interface)
  - [Python API](#python-api)
- [Authentication Methods](#authentication-methods)
- [What Gets Downloaded](#what-gets-downloaded)
- [Documentation](#documentation)
- [Troubleshooting](#troubleshooting)
- [Disclaimer](#disclaimer)
- [License](#license)

## 🎯 Introduction

**Coursera Full Course Downloader** is a Python-based tool that enables users to download complete Coursera courses for offline viewing and studying. The tool organizes downloaded materials in a structured format, preserving the course hierarchy (weeks/modules, lessons, and individual resources).

This project is designed to help learners access their enrolled courses offline, making education more accessible for those with limited internet connectivity or who prefer offline study materials.

## ✨ Features

- **Multiple Interfaces**: Choose between an intuitive GUI or powerful command-line interface
- **Complete Course Downloads**: Downloads all course materials including:
  - Video lectures (MP4 format)
  - Subtitles and transcripts (SRT, TXT)
  - Supplementary materials (PDFs, Excel files, datasets)
  - HTML readings and instructions
  - Practice labs and assignments
- **Flexible Authentication**: Multiple authentication methods supported:
  - Microsoft Edge browser cookies (automatic extraction)
  - Chrome, Firefox, Safari, and other browsers (via browser-cookie3)
  - Cookie files (Netscape format)
  - Manual CAUTH token
- **Organized File Structure**: Downloads are organized by modules and lessons, maintaining course hierarchy
- **Batch Downloads**: Download multiple courses sequentially
- **Parallel Downloads**: Multi-threaded downloading for improved speed
- **Resume Capability**: Continue interrupted downloads
- **Customizable Options**: Configure video resolution, subtitle languages, output paths, and more

## 🔧 Installation

### Prerequisites

- **Python 3.6 or higher**
- **Windows, macOS, or Linux** operating system
- **Active Coursera account** with enrollment in desired courses

### Install Dependencies

1. Clone or download this repository:
```bash
git clone https://github.com/yourusername/Coursera-Downloader.git
cd Coursera-Downloader
```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

### Method 1: Using the GUI (Easiest)

1. Run the GUI application:
```bash
python maingui.py
```

2. Select your authentication method (Edge cookies recommended)
3. Enter the course name or URL
4. Click "Download" and wait for completion

### Method 2: Command Line (3 Steps)

**Step 1** - Extract cookies from Microsoft Edge:
```bash
python coursera_dl.py --save-edge-cookies coursera_cookies.txt
```
*Note: Close Edge browser completely before running this command*

**Step 2** - Download your course:
```bash
python download_course.py "https://www.coursera.org/learn/YOUR-COURSE-NAME"
```

**Step 3** - Access your files:
```
Files will be saved in: ./Downloads/YOUR-COURSE-NAME/
```

## 📖 Usage

### GUI Application

The GUI provides an easy-to-use interface for downloading courses:

```bash
python maingui.py
```

**Features:**
- Select authentication method from dropdown
- Browse for cookie files or enter credentials
- Configure download options (video quality, subtitles, etc.)
- View download progress in real-time
- Access downloaded courses directly from the interface

### Command Line Interface

#### Basic Usage

Download a course using Edge cookies:
```bash
python coursera_dl.py --edge-cookies machine-learning
```

Download using a cookie file:
```bash
python coursera_dl.py --cookies_file coursera_cookies.txt deep-learning
```

Download multiple courses:
```bash
python coursera_dl.py --cookies_file coursera_cookies.txt course-1 course-2 course-3
```

#### Advanced Options

```bash
# Specify output directory
python coursera_dl.py --cookies_file cookies.txt --path ./my_courses course-name

# Download with specific video resolution
python coursera_dl.py --cookies_file cookies.txt --video-resolution 720p course-name

# Download specific subtitle language
python coursera_dl.py --cookies_file cookies.txt --subtitle-language es course-name

# Download with multiple parallel threads
python coursera_dl.py --cookies_file cookies.txt --jobs 4 course-name

# List all enrolled courses
python coursera_dl.py --cookies_file cookies.txt --list-courses
```

### Python API

Use the downloader programmatically in your Python scripts:

```python
from download_course import download_coursera_course

# Download a single course
download_coursera_course("https://www.coursera.org/learn/machine-learning")

# Download with custom parameters
download_coursera_course(
    course_url="https://www.coursera.org/learn/deep-learning",
    output_path="./my_courses",
    cookies_file="./my_cookies.txt"
)

# Download multiple courses
courses = [
    "https://www.coursera.org/learn/neural-networks-deep-learning",
    "https://www.coursera.org/learn/deep-neural-network",
    "https://www.coursera.org/learn/machine-learning-projects"
]

for course in courses:
    success = download_coursera_course(course)
    if success:
        print(f"✓ Successfully downloaded: {course}")
    else:
        print(f"✗ Failed: {course}")
```

## 🔐 Authentication Methods

### Option 1: Edge Browser Cookies (Recommended)

Automatically extract cookies from Microsoft Edge:

```bash
# Extract and save cookies
python coursera_dl.py --save-edge-cookies coursera_cookies.txt

# Use extracted cookies
python coursera_dl.py --cookies_file coursera_cookies.txt course-name
```

**Requirements:**
- Windows 10/11
- Microsoft Edge browser
- Logged into Coursera in Edge
- Edge browser must be closed during extraction

### Option 2: Other Browsers

Use cookies from Chrome, Firefox, Safari, etc.:

```bash
python coursera_dl.py --browser chrome course-name
python coursera_dl.py --browser firefox course-name
```

### Option 3: Manual Cookie File

Export cookies manually using a browser extension:

1. Install a cookie export extension (e.g., "EditThisCookie", "Get cookies.txt")
([Recommended](https://microsoftedge.microsoft.com/addons/detail/cookieeditor/neaplmfkghagebokkhpjpoebhdledlfi))
2. Log into Coursera
3. Export cookies in Netscape format
4. Save as `coursera_cookies.txt`
5. Use with `--cookies_file` option

### Option 4: Direct CAUTH Token

If you have your CAUTH cookie value:

```bash
python coursera_dl.py --cookies-cauth YOUR_CAUTH_VALUE course-name
```

## 📦 What Gets Downloaded

Each course download includes:

| Content Type | File Format | Description |
|-------------|-------------|-------------|
| **Video Lectures** | `.mp4` | All course videos in selected quality |
| **Subtitles** | `.srt` | Synchronized subtitle files |
| **Transcripts** | `.txt` | Plain text transcripts |
| **Readings** | `.html`, `.pdf` | Course readings and articles |
| **Assignments** | `.pdf`, `.html` | Assignment instructions |
| **Resources** | Various | Excel files, datasets, code files, etc. |
| **Notebooks** | `.ipynb` | Jupyter notebooks (if available) |

### File Structure

```
Downloads/
└── course-name/
    ├── 01_week-1-introduction/
    │   ├── 01_lesson-1-overview/
    │   │   ├── 01_welcome-video.mp4
    │   │   ├── 01_welcome-video.srt
    │   │   ├── 01_welcome-video.txt
    │   │   ├── 02_course-overview.html
    │   │   └── 03_syllabus.pdf
    │   └── 02_lesson-2-fundamentals/
    │       └── ...
    ├── 02_week-2-getting-started/
    │   └── ...
    └── ...
```

## 📚 Documentation

For more detailed information, please refer to:

- **[QUICK_START.md](QUICK_START.md)** - Fastest way to get started (3 steps)
- **[DOWNLOAD_GUIDE.md](DOWNLOAD_GUIDE.md)** - Comprehensive usage guide with examples
- **[EDGE_COOKIES_README.md](EDGE_COOKIES_README.md)** - Detailed Edge cookies setup and troubleshooting
- **[changelog.md](changelog.md)** - Version history and updates

## 🔧 Troubleshooting

### Problem: Cookies not found

**Solution:**
```bash
python coursera_dl.py --save-edge-cookies coursera_cookies.txt
```
Ensure Edge browser is completely closed before extracting cookies.

### Problem: 403 Forbidden error

**Solutions:**
- Verify you are enrolled in the course
- Re-export your cookies (they may have expired)
- Ensure cookies are from an active Coursera session
- Try logging out and back into Coursera, then re-export cookies

### Problem: No files downloaded

**Solutions:**
- Check that cookie file exists and is not empty
- Verify you're enrolled in the course on Coursera
- Ensure you have sufficient disk space
- Check your internet connection stability

### Problem: Download stops/freezes

**Solutions:**
- Use `--jobs 1` to disable parallel downloading
- Check your internet connection
- Try downloading during off-peak hours
- Use `--download-delay` to add delays between downloads

### Problem: Video quality issues

**Solution:**
```bash
# Specify video resolution (360p, 540p, 720p)
python coursera_dl.py --cookies_file cookies.txt --video-resolution 720p course-name
```

For more troubleshooting tips, see the [DOWNLOAD_GUIDE.md](DOWNLOAD_GUIDE.md).

## ⚠️ Disclaimer

**IMPORTANT - PLEASE READ CAREFULLY:**

This tool is provided for **personal educational use only**. By using this tool, you acknowledge and agree to the following:

1. **Terms of Service**: You must comply with [Coursera's Terms of Use](https://www.coursera.org/about/terms). This tool is intended to help enrolled students access their course materials offline for personal study purposes only.

2. **Enrollment Required**: You must be properly enrolled in any course you attempt to download. Do not use this tool to access courses you are not enrolled in.

3. **No Redistribution**: Downloaded content is for your personal use only. Do not redistribute, share, sell, or publish any downloaded materials. Respect intellectual property rights of course instructors and Coursera.

4. **No Commercial Use**: This tool and downloaded materials must not be used for commercial purposes.

5. **Educational Purpose**: This tool is designed to facilitate offline learning for students with limited internet access or who prefer offline study. Use it responsibly and ethically.

6. **Account Responsibility**: You are solely responsible for your Coursera account. Misuse of this tool may result in account suspension or termination by Coursera.

7. **No Warranty**: This software is provided "as is" without any warranties. The authors are not responsible for any misuse or consequences arising from the use of this tool.

8. **Respect Content Creators**: Remember that course content is created by educators who invest significant time and effort. Support them by respecting their work and Coursera's platform.

**By using this tool, you agree to use it responsibly, ethically, and in accordance with all applicable laws and terms of service.**

## 📄 License

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)**.

[![CC BY-NC 4.0](https://licensebuttons.net/l/by-nc/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc/4.0/)

**You are free to:**
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material

**Under the following terms:**
- **Attribution** — You must give appropriate credit
- **NonCommercial** — You may not use the material for commercial purposes

For the full license text, see the [LICENSE](LICENSE) file.

---

## 🤝 Contributing

Contributions are welcome! Please ensure that any contributions:
- Follow the existing code style
- Include appropriate documentation
- Respect Coursera's Terms of Service
- Are for personal educational use only

## 📧 Support

For issues, questions, or feature requests:
1. Check the documentation files (QUICK_START.md, DOWNLOAD_GUIDE.md)
2. Review the troubleshooting section above
3. Check existing issues on the project repository

---

## 🙏 Credits

This project is based on the excellent work by [@touhid314](https://github.com/touhid314) and their [Coursera-Downloader](https://github.com/touhid314/Coursera-Downloader) project. Special thanks for creating and maintaining this valuable educational tool that has helped countless learners access course materials offline.

---

**Made with ❤️ for learners worldwide. Happy learning! 🎓**

*Note: This is an independent project and is not affiliated with, endorsed by, or sponsored by Coursera or any of its partners.*

