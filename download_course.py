#!/usr/bin/env python3
"""
Coursera Course Downloader
A simple script to download Coursera courses using cookies authentication.

Usage:
    python download_course.py "https://www.coursera.org/learn/course-name"
    
    Or import and use the function:
    from download_course import download_coursera_course
    download_coursera_course("https://www.coursera.org/learn/course-name")
"""

import sys
import os
import logging
import re
from pathlib import Path


def extract_course_slug(course_url):
    """
    Extract the course slug from a Coursera course URL.
    
    Args:
        course_url (str): Full Coursera course URL
        
    Returns:
        str: Course slug (e.g., 'data-analytics-foundations')
        
    Examples:
        >>> extract_course_slug("https://www.coursera.org/learn/data-analytics-foundations")
        'data-analytics-foundations'
        >>> extract_course_slug("https://www.coursera.org/learn/python-for-data-analytics/")
        'python-for-data-analytics'
    """
    # Pattern to match Coursera learn URLs
    pattern = r'coursera\.org/learn/([a-zA-Z0-9\-]+)'
    match = re.search(pattern, course_url)
    
    if match:
        return match.group(1)
    else:
        raise ValueError(f"Invalid Coursera URL: {course_url}. Expected format: https://www.coursera.org/learn/course-name")


def download_coursera_course(course_url, output_path=None, cookies_file=None):
    """
    Download a Coursera course using the coursera-dl tool.
    
    Args:
        course_url (str): Full Coursera course URL (e.g., "https://www.coursera.org/learn/course-name")
        output_path (str, optional): Directory to save downloaded files. Defaults to "./Downloads"
        cookies_file (str, optional): Path to cookies file. Defaults to "./coursera_cookies.txt"
        
    Returns:
        bool: True if download was successful, False otherwise
        
    Examples:
        >>> download_coursera_course("https://www.coursera.org/learn/data-analytics-foundations")
        >>> download_coursera_course("https://www.coursera.org/learn/python-basics", output_path="./my_courses")
    """
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        stream=sys.stdout,
        force=True
    )
    
    try:
        # Extract course slug from URL
        course_slug = extract_course_slug(course_url)
        logging.info(f"Extracted course slug: {course_slug}")
        
        # Set default paths
        if output_path is None:
            output_path = os.path.join(os.getcwd(), "Downloads")
        
        if cookies_file is None:
            cookies_file = os.path.join(os.getcwd(), "coursera_cookies.txt")
        
        # Verify cookies file exists
        if not os.path.exists(cookies_file):
            logging.error(f"Cookies file not found: {cookies_file}")
            logging.error("Please ensure 'coursera_cookies.txt' exists in the current directory.")
            logging.error("You can create it by running: python coursera_dl.py --save-edge-cookies coursera_cookies.txt")
            return False
        
        # Create output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)
        logging.info(f"Output directory: {output_path}")
        
        # Import coursera_dl modules
        try:
            from commandline import parse_args
            from coursera_dl import main_f
        except ImportError as e:
            logging.error(f"Failed to import coursera_dl modules: {e}")
            logging.error("Please ensure coursera_dl.py and commandline.py are in the same directory.")
            return False
        
        # Set up arguments for coursera_dl
        sys.argv = [
            'coursera_dl.py',
            '--cookies_file', cookies_file,
            '--path', output_path,
            course_slug
        ]
        
        logging.info(f"Starting download for course: {course_slug}")
        logging.info(f"URL: {course_url}")
        logging.info("=" * 80)
        
        # Execute the download
        main_f(None)
        
        logging.info("=" * 80)
        logging.info(f"Download completed for course: {course_slug}")
        
        # Display summary
        course_dir = os.path.join(output_path, course_slug)
        if os.path.exists(course_dir):
            file_count = sum(1 for _ in Path(course_dir).rglob('*') if _.is_file())
            logging.info(f"Total files downloaded: {file_count}")
            logging.info(f"Files saved to: {course_dir}")
        
        return True
        
    except ValueError as e:
        logging.error(str(e))
        return False
    except Exception as e:
        logging.error(f"An error occurred during download: {e}")
        import traceback
        logging.error(traceback.format_exc())
        return False


def main():
    """
    Main function to handle command-line execution.
    """
    if len(sys.argv) < 2:
        print("=" * 80)
        print("Coursera Course Downloader")
        print("=" * 80)
        print("\nUsage:")
        print("  python download_course.py <course_url> [output_path] [cookies_file]")
        print("\nExamples:")
        print('  python download_course.py "https://www.coursera.org/learn/data-analytics-foundations"')
        print('  python download_course.py "https://www.coursera.org/learn/python-basics" "./my_courses"')
        print('  python download_course.py "https://www.coursera.org/learn/ml-intro" "./Downloads" "./my_cookies.txt"')
        print("\nArguments:")
        print("  course_url    : Full Coursera course URL (required)")
        print("  output_path   : Directory to save files (optional, default: ./Downloads)")
        print("  cookies_file  : Path to cookies file (optional, default: ./coursera_cookies.txt)")
        print("\nNote:")
        print("  Make sure you have a valid cookies file before running this script.")
        print("  You can create one using: python coursera_dl.py --save-edge-cookies coursera_cookies.txt")
        print("=" * 80)
        sys.exit(1)
    
    # Get arguments
    course_url = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    cookies_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Download the course
    success = download_coursera_course(course_url, output_path, cookies_file)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()


