"""
Module for download-related classes and functions.

We currently support an internal downloader written in Python with just the
essential functionality and four "industrial-strength" external downloaders,
namely, aria2c, axel, curl, and wget.
"""

import logging
import math
import os
import subprocess
import sys
import time

import requests

FILE_DOWNLOAD_TIMEOUT_SECONDS = 30
FILE_DOWNLOAD_TIMEOUT_RETRIES = 1


class DownloadTimeoutError(Exception):
    """Raised when a file download exceeds the configured timeout."""


#
# Below are file downloaders, they are wrappers for external downloaders.
#


class Downloader:
    """
    Base downloader class.

    Every subclass should implement the _start_download method.

    Usage::

      >>> import downloaders
      >>> d = downloaders.SubclassFromDownloader()
      >>> d.download('http://example.com', 'save/to/this/file')
    """

    def _start_download(self, url, filename, resume, timeout_seconds=None):
        """
        Actual method to download the given url to the given file.
        This method should be implemented by the subclass.
        """
        raise NotImplementedError("Subclasses should implement this")

    def download(self, url, filename, resume=False):
        """
        Download the given url to the given file. When the download
        is aborted by the user, the partially downloaded file is also removed.
        """

        timeout_seconds = FILE_DOWNLOAD_TIMEOUT_SECONDS
        max_timeout_attempts = FILE_DOWNLOAD_TIMEOUT_RETRIES + 1
        timeout_attempt = 0
        while timeout_attempt < max_timeout_attempts:
            try:
                return self._start_download(
                    url, filename, resume, timeout_seconds=timeout_seconds
                )
            except DownloadTimeoutError:
                timeout_attempt += 1
                if timeout_attempt >= max_timeout_attempts:
                    logging.warning(
                        "Skipping %s after %d timeout attempts (%ss each).",
                        filename,
                        max_timeout_attempts,
                        timeout_seconds,
                    )
                    return False
                logging.warning(
                    "Download timed out for %s (attempt %d/%d). Retrying...",
                    filename,
                    timeout_attempt,
                    max_timeout_attempts,
                )
                if not resume:
                    try:
                        os.remove(filename)
                    except OSError:
                        pass
            except KeyboardInterrupt as e:
                # keep the file if resume is True
                if not resume:
                    logging.info(
                        "Keyboard Interrupt -- Removing partial file: %s", filename
                    )
                    try:
                        os.remove(filename)
                    except OSError:
                        pass
                raise e
            except requests.exceptions.Timeout:
                timeout_attempt += 1
                if timeout_attempt >= max_timeout_attempts:
                    logging.warning(
                        "Skipping %s after %d timeout attempts (%ss each).",
                        filename,
                        max_timeout_attempts,
                        timeout_seconds,
                    )
                    return False
                logging.warning(
                    "Request timed out for %s (attempt %d/%d). Retrying...",
                    filename,
                    timeout_attempt,
                    max_timeout_attempts,
                )
                if not resume:
                    try:
                        os.remove(filename)
                    except OSError:
                        pass


class ExternalDownloader(Downloader):
    """
    Downloads files with an external downloader.

    We could possibly use python to stream files to disk,
    but this is slow compared to these external downloaders.

    :param session: Requests session.
    :param bin: External downloader binary.
    """

    # External downloader binary
    bin = None

    def __init__(self, session, bin=None, downloader_arguments=None):
        self.session = session
        self.bin = bin or self.__class__.bin
        self.downloader_arguments = downloader_arguments or []

        if not self.bin:
            raise RuntimeError("No bin specified")

        self._check_bin()

    def _prepare_cookies(self, command, url):
        """
        Extract cookies from the requests session and add them to the command
        """

        req = requests.models.Request()
        req.method = "GET"
        req.url = url

        cookie_values = requests.cookies.get_cookie_header(self.session.cookies, req)

        if cookie_values:
            self._add_cookies(command, cookie_values)

    def _enable_resume(self, command):
        """
        Enable resume feature
        """

        raise RuntimeError("Subclass should implement this")

    def _add_cookies(self, command, cookie_values):
        """
        Add the given cookie values to the command
        """

        raise RuntimeError("Subclasses should implement this")

    def _create_command(self, url, filename):
        """
        Create command to execute in a subprocess.
        """
        raise NotImplementedError("Subclasses should implement this")

    def _check_bin(self):
        """
        Make sure the downloader is installed
        """
        try:
            ret = subprocess.run([self.bin, "--version"])
        except FileNotFoundError:
            raise RuntimeError(f"Downloader '{self.bin}' not found")

        if ret.returncode != 0:
            raise RuntimeError(
                f"Downloader '{self.bin}' returned a non-zero exit status"
            )

    def _start_download(self, url, filename, resume, timeout_seconds=None):
        command = self._create_command(url, filename)
        command.extend(self.downloader_arguments)
        self._prepare_cookies(command, url)
        if resume:
            self._enable_resume(command)

        logging.debug("Executing %s: %s", self.bin, command)
        try:
            result = subprocess.run(command, timeout=timeout_seconds)
        except OSError as e:
            msg = f"{e}. Are you sure that '{self.bin}' is the right bin?"
            raise OSError(msg)
        except subprocess.TimeoutExpired:
            raise DownloadTimeoutError("Timed out while running external downloader")

        if result.returncode != 0:
            logging.warning(
                "External downloader '%s' failed for %s with exit code %s",
                self.bin,
                filename,
                result.returncode,
            )
            return False
        return True


class WgetDownloader(ExternalDownloader):
    """
    Uses wget, which is robust and gives nice visual feedback.
    """

    bin = "wget"

    def _enable_resume(self, command):
        command.append("-c")

    def _add_cookies(self, command, cookie_values):
        command.extend(["--header", "Cookie: " + cookie_values])

    def _create_command(self, url, filename):
        return [self.bin, url, "-O", filename, "--no-cookies", "--no-check-certificate"]


class CurlDownloader(ExternalDownloader):
    """
    Uses curl, which is robust and gives nice visual feedback.
    """

    bin = "curl"

    def _enable_resume(self, command):
        command.extend(["-C", "-"])

    def _add_cookies(self, command, cookie_values):
        command.extend(["--cookie", cookie_values])

    def _create_command(self, url, filename):
        return [self.bin, url, "-k", "-#", "-L", "-o", filename]


class Aria2Downloader(ExternalDownloader):
    """
    Uses aria2. Unfortunately, it does not give a nice visual feedback, but
    gets the job done much faster than the alternatives.
    """

    bin = "aria2c"

    def _enable_resume(self, command):
        command.append("-c")

    def _add_cookies(self, command, cookie_values):
        command.extend(["--header", "Cookie: " + cookie_values])

    def _create_command(self, url, filename):
        return [
            self.bin,
            url,
            "-o",
            filename,
            "--check-certificate=false",
            "--log-level=notice",
            "--max-connection-per-server=4",
            "--min-split-size=1M",
        ]


class AxelDownloader(ExternalDownloader):
    """
    Uses axel, which is robust and it both gives nice
    visual feedback and get the job done fast.
    """

    bin = "axel"

    def _enable_resume(self, command):
        logging.warn("Resume download not implemented for this " "downloader!")

    def _add_cookies(self, command, cookie_values):
        command.extend(["-H", "Cookie: " + cookie_values])

    def _create_command(self, url, filename):
        return [self.bin, "-o", filename, "-n", "4", "-a", url]


def format_bytes(bytes):
    """
    Get human readable version of given bytes.
    Ripped from https://github.com/rg3/youtube-dl
    """
    if bytes is None:
        return "N/A"
    if type(bytes) is str:
        bytes = float(bytes)
    if bytes == 0.0:
        exponent = 0
    else:
        exponent = int(math.log(bytes, 1024.0))
    suffix = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"][exponent]
    converted = float(bytes) / float(1024**exponent)
    return f"{converted:.2f}{suffix}"


class DownloadProgress:
    """
    Report download progress.
    Inspired by https://github.com/rg3/youtube-dl
    """

    def __init__(self, total):
        if total in [0, "0", None]:
            self._total = None
        else:
            self._total = int(total)

        self._current = 0
        self._start = 0
        self._now = 0

        self._finished = False

    def start(self):
        self._now = time.time()
        self._start = self._now

    def stop(self):
        self._now = time.time()
        self._finished = True
        self._total = self._current
        self.report_progress()

    def read(self, bytes):
        self._now = time.time()
        self._current += bytes
        self.report_progress()

    def report(self, bytes):
        self._now = time.time()
        self._current = bytes
        self.report_progress()

    def calc_percent(self):
        if self._total is None:
            return "--%"
        if self._total == 0:
            return "100% done"
        percentage = int(float(self._current) / float(self._total) * 100.0)
        done = int(percentage / 2)
        return "[{0: <50}] {1}%".format(done * "#", percentage)

    def calc_speed(self):
        dif = self._now - self._start
        if self._current == 0 or dif < 0.001:  # One millisecond
            return "---b/s"
        return f"{format_bytes(float(self._current) / dif)}/s"

    def report_progress(self):
        """Report download progress."""
        percent = self.calc_percent()
        total = format_bytes(self._total)

        speed = self.calc_speed()
        total_speed_report = f"{total} at {speed}"

        report = f"\r{percent: <56} {total_speed_report: >30}"

        if self._finished:
            print(report)
        else:
            print(report, end="")
        sys.stdout.flush()


class NativeDownloader(Downloader):
    """
    'Native' python downloader -- slower than the external downloaders.

    :param session: Requests session.
    """

    def __init__(self, session):
        self.session = session

    def _start_download(self, url, filename, resume=False, timeout_seconds=None):
        # resume has no meaning if the file doesn't exists!
        resume = resume and os.path.exists(filename)

        headers = {}
        filesize = None
        if resume:
            filesize = os.path.getsize(filename)
            headers["Range"] = f"bytes={filesize}-"
            logging.info("Resume downloading %s -> %s", url, filename)
        else:
            logging.info("Downloading %s -> %s", url, filename)

        max_attempts = 3
        attempts_count = 0
        error_msg = ""
        while attempts_count < max_attempts:
            started_at = time.time()
            request_timeout = (10, timeout_seconds) if timeout_seconds else None
            r = self.session.get(
                url, stream=True, headers=headers, timeout=request_timeout
            )

            if r.status_code != 200:
                # because in resume state we are downloading only a
                # portion of requested file, server may return
                # following HTTP codes:
                # 206: Partial Content
                # 416: Requested Range Not Satisfiable
                # which are OK for us.
                if resume and r.status_code == 206:
                    pass
                elif resume and r.status_code == 416:
                    logging.info("%s already downloaded", filename)
                    r.close()
                    return True
                else:
                    print("%s %s %s" % (r.status_code, url, filesize))
                    logging.warn(
                        "Probably the file is missing from the AWS "
                        "repository...  waiting."
                    )

                    if r.reason:
                        error_msg = r.reason + " " + str(r.status_code)
                    else:
                        error_msg = "HTTP Error " + str(r.status_code)

                    wait_interval = 2 ** (attempts_count + 1)
                    msg = "Error downloading, will retry in {0} seconds ..."
                    print(msg.format(wait_interval))
                    time.sleep(wait_interval)
                    attempts_count += 1
                    continue

            if resume and r.status_code == 200:
                # if the server returns HTTP code 200 while we are in
                # resume mode, it means that the server does not support
                # partial downloads.
                resume = False

            content_length = r.headers.get("content-length")
            chunk_sz = 1048576
            progress = DownloadProgress(content_length)
            progress.start()
            f = open(filename, "ab") if resume else open(filename, "wb")
            try:
                while True:
                    if timeout_seconds and (time.time() - started_at) > timeout_seconds:
                        raise DownloadTimeoutError(
                            f"Timed out while downloading {filename}"
                        )
                    data = r.raw.read(chunk_sz, decode_content=True)
                    if not data:
                        progress.stop()
                        break
                    progress.report(r.raw.tell())
                    f.write(data)
            finally:
                f.close()
                r.close()
            return True

        if attempts_count == max_attempts:
            logging.warn("Skipping, can't download file ...")
            logging.error(error_msg)
            return False


def get_downloader(session, class_name, args):
    """
    Decides which downloader to use.
    """

    external = {
        "wget": WgetDownloader,
        "curl": CurlDownloader,
        "aria2": Aria2Downloader,
        "axel": AxelDownloader,
    }

    for bin, class_ in external.items():
        if getattr(args, bin):
            return class_(
                session,
                bin=getattr(args, bin),
                downloader_arguments=args.downloader_arguments,
            )

    return NativeDownloader(session)
