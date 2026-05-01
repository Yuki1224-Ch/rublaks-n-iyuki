# local_solver.py - CUSTOM SOLVER - No External APIs, Works on All Terminals
import time
import threading
from util import get_config

try:
    from custom_solver import CustomCaptchaSolver
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("[!] Warning: Playwright not available. Custom solver will not work.")

config = get_config()

# Cache solver instance to avoid restarting browser every time
_solver_instance = None
_solver_lock = threading.Lock()

def get_solver():
    global _solver_instance
    with _solver_lock:
        if _solver_instance is None:
            _solver_instance = CustomCaptchaSolver(debug=False)
    return _solver_instance

def solve_captcha_wrapper(session):
    """
    Runs the synchronous captcha solver in a separate thread to prevent freezing.
    Returns True if solved, False otherwise.
    """
    if not PLAYWRIGHT_AVAILABLE:
        print("[-] Playwright not available, cannot solve captcha")
        return False
    
    result_container = {"success": False, "token": None}
    event = threading.Event()

    def run_solver():
        nonlocal result_container
        try:
            solver = get_solver()
            
            # Get URL from session - adjust based on your actual session implementation
            url = getattr(session, 'url', 'https://www.roblox.com/login')
            
            # Get proxy from session - handle both dict and string formats
            proxy_dict = None
            if hasattr(session, 'proxy'):
                proxy_data = session.proxy
                if isinstance(proxy_data, dict):
                    proxy_dict = proxy_data
                elif isinstance(proxy_data, str) and proxy_data:
                    # Convert string proxy to dict format
                    proxy_dict = {"server": proxy_data}
            
            print(f"[*] Solving captcha for URL: {url}")
            
            # Call the synchronous solver directly
            result = solver.solve_with_token(
                site_key="476068BF-9607-4799-B53D-966BE98E2B81",
                service_url=url,
                proxy=proxy_dict
            )
            
            if result.get('success'):
                result_container['success'] = True
                result_container['token'] = result.get('token')
                
                # Inject token back into session if needed
                if hasattr(session, 'set_captcha_token'):
                    session.set_captcha_token(result['token'])
            
        except Exception as e:
            print(f"Solver Thread Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            event.set()

    # Start thread
    t = threading.Thread(target=run_solver)
    t.daemon = True
    t.start()
    
    # Wait max 45 seconds for solver
    completed = event.wait(timeout=45)
    
    if not completed:
        print("⚠️ Captcha solver timed out (45s)")
        return False
        
    return result_container['success']
