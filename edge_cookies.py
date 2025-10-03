# -*- coding: utf-8 -*-

"""
Edge browser cookie extraction module.
This module handles extracting cookies from Microsoft Edge browser database.
"""

import os
import sqlite3
import logging
import tempfile
import shutil
from pathlib import Path
import json
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import win32crypt
import requests
from http import cookiejar as cookielib


class EdgeCookieExtractor:
    """
    Extracts cookies from Microsoft Edge browser database.
    """
    
    def __init__(self):
        self.edge_cookies_path = self._get_edge_cookies_path()
        self.edge_key_path = self._get_edge_key_path()
        
    def _get_edge_cookies_path(self):
        """
        Get the path to Edge cookies database. Supports custom profiles.
        
        Respects env EDGE_PROFILE (e.g., "Work"). Also auto-detects by scanning
        profile directories under "User Data".
        """
        user_profile = os.environ.get('USERPROFILE', '')
        edge_user_data = os.path.join(user_profile, 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data')
        preferred_profile = os.environ.get('EDGE_PROFILE')  # e.g., "Work"

        def path_for(profile_dir, network=True):
            if network:
                return os.path.join(edge_user_data, profile_dir, 'Network', 'Cookies')
            return os.path.join(edge_user_data, profile_dir, 'Cookies')

        # Build candidate list (ordered by likelihood)
        candidates = []
        if preferred_profile:
            candidates.append(path_for(preferred_profile, True))
            candidates.append(path_for(preferred_profile, False))
        # Common profiles
        for prof in ['Work', 'Profile 1', 'Default', 'Profile 2']:
            candidates.append(path_for(prof, True))
            candidates.append(path_for(prof, False))

        # Add any other detected profiles dynamically
        try:
            for name in os.listdir(edge_user_data):
                # only folders
                p = os.path.join(edge_user_data, name)
                if not os.path.isdir(p):
                    continue
                # skip non-profile dirs by quick filter
                if name.lower() in ['system profile', 'guest profile', 'crashpad', 'snapshots']:
                    continue
                candidates.append(path_for(name, True))
                candidates.append(path_for(name, False))
        except Exception:
            pass

        for edge_path in candidates:
            if os.path.exists(edge_path):
                return edge_path

        raise FileNotFoundError("Edge cookies database not found. Set EDGE_PROFILE, or ensure Edge profile has cookies.")
    
    def _get_edge_key_path(self):
        """
        Get the path to Edge encryption key.
        """
        user_profile = os.environ.get('USERPROFILE', '')
        key_path = os.path.join(user_profile, 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', 'Local State')
        return key_path
    
    def _get_encryption_key(self):
        """
        Extract the encryption key from Edge's Local State file.
        """
        try:
            with open(self.edge_key_path, 'r', encoding='utf-8') as f:
                local_state = json.load(f)
            
            encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
            encrypted_key = encrypted_key[5:]  # Remove 'DPAPI' prefix
            
            # Use Windows DPAPI to decrypt the key
            key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
            return key
        except Exception as e:
            logging.error(f"Failed to extract encryption key: {e}")
            return None
    
    def _decrypt_cookie_value(self, encrypted_value, key):
        """
        Decrypt cookie value from Chromium/Edge.

        Supports:
        - AES-GCM with 'v10' prefix (nonce 12 bytes after prefix, tag last 16 bytes)
        - Older DPAPI-encrypted blobs (prefix 0x01 0x00 0x00 0x00)
        """
        try:
            if not encrypted_value:
                return None

            # AES-GCM: value starts with ASCII 'v10'
            if encrypted_value[:3] == b'v10' or encrypted_value[:3] == b'v11':
                nonce = encrypted_value[3:15]
                ciphertext_tag = encrypted_value[15:]
                if len(ciphertext_tag) < 16:
                    return None
                ciphertext = ciphertext_tag[:-16]
                tag = ciphertext_tag[-16:]
                cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
                decryptor = cipher.decryptor()
                decrypted = decryptor.update(ciphertext) + decryptor.finalize()
                return decrypted.decode('utf-8')

            # Legacy DPAPI blob
            if encrypted_value[:4] == b"\x01\x00\x00\x00":
                try:
                    return win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[1].decode('utf-8')
                except Exception:
                    return None

            # Unknown format
            return None
        except Exception as e:
            logging.debug(f"Failed to decrypt cookie value: {e}")
            return None
    
    def extract_cookies_for_domain(self, domain='coursera.org'):
        """
        Extract cookies for a specific domain from Edge database.
        
        Args:
            domain (str): Domain to extract cookies for (default: 'coursera.org')
            
        Returns:
            requests.cookies.RequestsCookieJar: Cookie jar with extracted cookies
        """
        if not os.path.exists(self.edge_cookies_path):
            raise FileNotFoundError("Edge cookies database not found")
        
        # Create a temporary copy of the database since Edge might have it locked
        temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_db.close()
        
        try:
            shutil.copy2(self.edge_cookies_path, temp_db.name)
            
            # Connect to the database
            conn = sqlite3.connect(temp_db.name)
            cursor = conn.cursor()
            
            # Query for cookies from the specified domain
            query = """
            SELECT name, value, encrypted_value, host_key, path, expires_utc, is_secure, is_httponly
            FROM cookies 
            WHERE host_key LIKE ? OR host_key LIKE ?
            """
            
            cursor.execute(query, (f'%{domain}%', f'%.{domain}%'))
            rows = cursor.fetchall()
            
            # Get encryption key
            key = self._get_encryption_key()
            
            # Create cookie jar
            cookie_jar = requests.cookies.RequestsCookieJar()
            
            for row in rows:
                name, value, encrypted_value, host_key, path, expires_utc, is_secure, is_httponly = row
                
                # Decrypt the cookie value if it's encrypted
                if encrypted_value and key:
                    decrypted_value = self._decrypt_cookie_value(encrypted_value, key)
                    if decrypted_value:
                        value = decrypted_value
                
                # Create cookie
                cookie = cookielib.Cookie(
                    version=0,
                    name=name,
                    value=value,
                    port=None,
                    port_specified=False,
                    domain=host_key,
                    domain_specified=True,
                    domain_initial_dot=host_key.startswith('.'),
                    path=path,
                    path_specified=True,
                    secure=bool(is_secure),
                    expires=expires_utc if expires_utc else None,
                    discard=False,
                    comment=None,
                    comment_url=None,
                    rest={}
                )
                
                cookie_jar.set_cookie(cookie)
            
            conn.close()
            return cookie_jar
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_db.name)
            except:
                pass
    
    def save_cookies_to_file(self, domain='coursera.org', filename='edge_cookies.txt'):
        """
        Extract cookies and save them to a file in Netscape format.
        
        Args:
            domain (str): Domain to extract cookies for
            filename (str): Output filename
            
        Returns:
            str: Path to the saved cookies file
        """
        cookie_jar = self.extract_cookies_for_domain(domain)
        
        # Save in Netscape format
        with open(filename, 'w') as f:
            f.write('# Netscape HTTP Cookie File\n')
            f.write('# This is a generated file! Do not edit.\n\n')
            
            for cookie in cookie_jar:
                # Convert to Netscape format
                domain_flag = 'TRUE' if cookie.domain_initial_dot else 'FALSE'
                path_flag = 'TRUE' if cookie.path_specified else 'FALSE'
                secure_flag = 'TRUE' if cookie.secure else 'FALSE'
                expires = str(int(cookie.expires)) if cookie.expires else '0'
                
                line = f"{cookie.domain}\t{domain_flag}\t{cookie.path}\t{path_flag}\t{expires}\t{cookie.name}\t{cookie.value}\n"
                f.write(line)
        
        logging.info(f"Saved {len(cookie_jar)} cookies to {filename}")
        return filename


def get_edge_cookies_for_coursera():
    """
    Convenience function to get Coursera cookies from Edge.
    
    Returns:
        requests.cookies.RequestsCookieJar: Cookie jar with Coursera cookies
    """
    extractor = EdgeCookieExtractor()
    return extractor.extract_cookies_for_domain('coursera.org')


def save_edge_cookies_for_coursera(filename='coursera_edge_cookies.txt'):
    """
    Convenience function to save Coursera cookies from Edge to file.
    
    Args:
        filename (str): Output filename
        
    Returns:
        str: Path to the saved cookies file
    """
    extractor = EdgeCookieExtractor()
    return extractor.save_cookies_to_file('coursera.org', filename)


if __name__ == '__main__':
    # Test the cookie extraction
    try:
        extractor = EdgeCookieExtractor()
        cookies = extractor.extract_cookies_for_domain('coursera.org')
        print(f"Extracted {len(cookies)} cookies for coursera.org")
        
        # Save to file
        filename = extractor.save_cookies_to_file('coursera.org', 'coursera_cookies.txt')
        print(f"Cookies saved to {filename}")
        
    except Exception as e:
        print(f"Error: {e}")
