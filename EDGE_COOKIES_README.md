# Coursera Downloader with Edge Cookies Support

This modified version of the Coursera downloader adds support for automatically extracting cookies from Microsoft Edge browser, eliminating the need for manual username/password authentication.

## New Features

### 1. Automatic Edge Cookie Extraction
- Automatically extracts cookies from Microsoft Edge browser
- No need to manually export cookies or use browser extensions
- Supports encrypted cookie values using Windows DPAPI

### 2. New Command Line Options

#### `--edge-cookies`
Extract cookies from Edge browser automatically and use them for authentication.

```bash
python coursera_dl.py --edge-cookies machine-learning
```

#### `--save-edge-cookies <filename>`
Extract cookies from Edge browser and save them to a file for later use.

```bash
python coursera_dl.py --save-edge-cookies my_cookies.txt
```

Then use the saved cookies:
```bash
python coursera_dl.py --cookies_file my_cookies.txt machine-learning
```

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure you have Microsoft Edge installed and have logged into Coursera in Edge.

## Usage Examples

### Basic Usage with Edge Cookies
```bash
# Download a course using Edge cookies
python coursera_dl.py --edge-cookies course-name

# Download multiple courses
python coursera_dl.py --edge-cookies course1 course2 course3
```

### Save and Reuse Cookies
```bash
# Save Edge cookies to a file
python coursera_dl.py --save-edge-cookies coursera_cookies.txt

# Use the saved cookies later
python coursera_dl.py --cookies_file coursera_cookies.txt course-name
```

### Traditional Methods Still Work
```bash
# Traditional username/password login (fallback)
python coursera_dl.py -u your-email@example.com -p your-password course-name

# Use browser_cookie3 for other browsers
python coursera_dl.py --browser chrome course-name
```

## How It Works

1. **Cookie Extraction**: The tool accesses Edge's cookie database (SQLite) and extracts Coursera-related cookies
2. **Decryption**: Encrypted cookie values are decrypted using Windows DPAPI
3. **Authentication**: The extracted cookies are used to authenticate with Coursera's API
4. **Fallback**: If Edge cookie extraction fails, it falls back to traditional username/password authentication

## Requirements

- Windows operating system (for Edge cookie database access)
- Microsoft Edge browser with active Coursera login
- Python 3.6+
- Required Python packages (see requirements.txt)

## Troubleshooting

### Edge Cookies Not Found
If you get an error about Edge cookies not being found:
1. Make sure you're logged into Coursera in Microsoft Edge
2. Try logging out and back into Coursera in Edge
3. Check that Edge is installed in the default location

### Permission Errors
If you get permission errors accessing Edge's cookie database:
1. Make sure Edge is closed completely
2. Run the script as administrator if needed
3. Check that no other applications are using Edge's database

### Fallback to Manual Authentication
If Edge cookie extraction fails, the tool will automatically fall back to traditional username/password authentication.

## Security Notes

- Cookies are extracted from your local Edge browser only
- No cookies are transmitted to external servers
- The tool only accesses cookies for coursera.org domain
- Edge must be closed when extracting cookies to avoid database locks

## File Structure

- `edge_cookies.py` - Edge cookie extraction module
- `cookies.py` - Modified to support Edge cookies
- `commandline.py` - Updated with new command line options
- `coursera_dl.py` - Updated session creation logic

## Dependencies Added

- `cryptography>=3.4.8` - For cookie decryption
- `pywin32>=306` - For Windows DPAPI access

## Compatibility

- Windows 10/11
- Microsoft Edge (any recent version)
- Python 3.6+
- All existing Coursera downloader functionality preserved
