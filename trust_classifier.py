# Import the SafeBrowsing class from the pysafebrowsing library
from pysafebrowsing import SafeBrowsing
from shopping_classifier import get_credentials

# Define a function to check if a URL is safe
def check_url(url):
    
    # Set the API key for Google Safe Browsing API
    KEY = get_credentials("google_safe") # Replace with your Google Safe Browsing API key
    
    # Create a SafeBrowsing object with the API key
    s = SafeBrowsing(KEY)
    
    # Use the lookup_urls method to check if the given URL is malicious
    r = s.lookup_urls([url])
    
    # Check the 'malicious' key in the response for the URL
    if r[url].get('malicious', False):
        # Return 'Non-trusted' if the URL is malicious
        return 'Non-trusted'
    else:
        # Return 'Trusted' if the URL is safe
        return 'Trusted'

# Example usage:
#url = 'http://google.com'
#url = 'http://malware.testing.google.test/testing/malware/' 
#print(check_url(url)) # Output: Non-trusted
