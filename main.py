import requests
import json

def get_ip_and_headers(url, headers=None, proxies=None):
    """
    Makes an HTTP GET request to the given URL and returns the IP and headers
    received by the target server.
    """
    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        response.raise_for_status() # Raise an exception for HTTP errors
        data = response.json()
        
        # httpbin.org/ip returns {'origin': 'IP_ADDRESS'}
        # httpbin.org/headers returns {'headers': {...}}
        
        ip_address = data.get('origin', 'N/A')
        request_headers = data.get('headers', {})
        
        return ip_address, request_headers
    except requests.exceptions.RequestException as e:
        return f"Error: {e}", {}

if __name__ == "__main__":
    target_ip_url = "https://httpbin.org/ip"

    print("--- 1. Default Request (Your actual IP and User-Agent) ---")
    # This request uses your system's default IP and User-Agent.
    # Web servers can track you based on this information.
    ip_default, headers_default = get_ip_and_headers(target_ip_url)
    print(f"  Observed IP: {ip_default}")
    print(f"  Observed User-Agent: {headers_default.get('User-Agent', 'N/A')}")
    print("-" * 50 + "\n")

    print("--- 2. Request with Custom User-Agent ---")
    # Changing the User-Agent can sometimes help bypass simple bot detection,
    # as it makes your request appear to come from a different browser or device.
    custom_headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
    }
    ip_custom_ua, headers_custom_ua = get_ip_and_headers(target_ip_url, headers=custom_headers)
    print(f"  Observed IP: {ip_custom_ua}")
    print(f"  Observed User-Agent: {headers_custom_ua.get('User-Agent', 'N/A')}")
    print("  Note: IP address remains the same, only User-Agent changed.")
    print("-" * 50 + "\n")

    print("--- 3. Illustrating Request via Proxy (to change IP) ---")
    # Mobile proxies are used to change your apparent IP address to a real
    # mobile network IP, making requests appear to come from a mobile device
    # in a specific location, bypassing IP-based restrictions or blocks.
    # This section demonstrates how to configure a proxy in 'requests'.
    # For this to work, you need a *real* proxy server running.
    # Replace 'http://your_proxy_ip:port' with your actual proxy details.
    
    # Example placeholder for a proxy. This will likely fail without a real proxy.
    proxy_address = "http://127.0.0.1:8080" # Replace with your actual proxy IP and port
    proxies = {
        "http": proxy_address,
        "https": proxy_address,
    }

    print(f"  Attempting request via proxy: {proxy_address}")
    ip_via_proxy, headers_via_proxy = get_ip_and_headers(target_ip_url, proxies=proxies)
    print(f"  Observed IP (via proxy attempt): {ip_via_proxy}")
    print(f"  Observed User-Agent (via proxy attempt): {headers_via_proxy.get('User-Agent', 'N/A')}")
    print("  Note: If the IP is 'Error: ...' or your original IP, the proxy either failed or wasn't active.")
    print("  A successful proxy connection would show the proxy's IP address.")
    print("  Mobile proxies provide real mobile IPs to achieve this effect.")
    print("-" * 50 + "\n")
