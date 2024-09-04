"""
Library: Cloudflare Identifier
Author: Haluk YAMANER
Email: haluk@halukyamaner.com
Web: https://www.halukyamaner.com
Version: 1.0

Description:
    This script checks for Cloudflare-specific headers and other security-related headers in the response 
    headers of a given domain. It helps identify if a website is using Cloudflare as a CDN or security provider
    and provides additional information on security measures like HSTS, XSS protection, and other common headers.

Usage:
    The script is executed from the command line. The user is prompted to input the domain name 
    (without http/https), and the script will perform an HTTP request to fetch and analyze the headers 
    returned by the server.

Requirements:
    Python 3.x
    Modules: requests

Features:
    - Identifies Cloudflare-specific headers (e.g., cf-ray, cf-cache-status)
    - Detects additional common security headers (e.g., Strict-Transport-Security, X-Frame-Options)
    - Provides feedback if Cloudflare is detected
    - Handles exceptions when the domain cannot be reached
"""
import requests

# Function to check Cloudflare headers and provide additional details
def check_cloudflare_headers(domain):
    try:
        # Send a GET request to the domain
        response = requests.get(f'https://{domain}', timeout=10)
        
        # Fetch the headers from the response
        headers = response.headers
        
        # Cloudflare-specific headers
        cloudflare_headers = ['cf-ray', 'cf-cache-status', 'server', 'cf-request-id']
        # Other headers that may indicate CDN or security services
        additional_headers = ['x-powered-by', 'strict-transport-security', 'x-content-type-options', 
                              'x-xss-protection', 'x-frame-options', 'x-cdn', 'x-cache', 'x-forwarded-for']
        
        cloudflare_detected = False
        
        print("\n--- Cloudflare-Specific Headers ---")
        for header in cloudflare_headers:
            if header in headers:
                if header == 'server' and 'cloudflare' not in headers[header].lower():
                    continue
                print(f"{header}: {headers[header]}")
                cloudflare_detected = True
        
        # Check for common security headers or additional CDN-related headers
        print("\n--- Additional Header Information ---")
        for header in additional_headers:
            if header in headers:
                print(f"{header}: {headers[header]}")
        
        if 'server' in headers:
            print(f"\nServer Header: {headers['server']}")
        else:
            print("\nNo server header found.")

        if cloudflare_detected:
            print("\nThis site appears to be using Cloudflare.")
        else:
            print("\nNo Cloudflare-specific headers detected.")
    
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to {domain}: {e}")

# Main program
if __name__ == "__main__":
    # Prompt user for domain
    domain = input("Enter the domain name (without http/https): ").strip()
    
    # Check if the domain is using Cloudflare and provide detailed information
    check_cloudflare_headers(domain)
