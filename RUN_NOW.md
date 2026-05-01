# 🚀 HOW TO RUN YOUR CUSTOM CAPTCHA SOLVER

## ✅ FILES UPDATED:
1. `custom_solver.py` - Your OWN custom captcha solver (synchronous, headless, CV-based)
2. `local_solver.py` - Non-blocking wrapper that runs solver in separate thread

## 📦 STEP 1: INSTALL DEPENDENCIES
```bash
pip install playwright opencv-python-headless numpy pillow requests fake-useragent rich
playwright install chromium
```

## 🔧 STEP 2: VERIFY INSTALLATION
```bash
python -c "from custom_solver import CustomCaptchaSolver; print('✅ Custom Solver Ready!')"
```

## ▶️ STEP 3: RUN YOUR CHECKER
```bash
python main.py
```

## 🎯 WHAT YOU'LL SEE:
- **Live Progress Bar** - Shows exactly how many accounts checked
- **Real-time Stats** - Valid, Invalid, Captcha Solved, Errors
- **No Freezing** - Solver runs in background thread
- **Detailed Logs** - See every action as it happens

## ⚠️ TROUBLESHOOTING:

### "Playwright not installed"
→ Run: `pip install playwright && playwright install chromium`

### "OpenCV not available"
→ Run: `pip install opencv-python-headless numpy pillow`

### "Browser executable not found"
→ Run: `playwright install chromium`

### Still stuck/freezing?
→ Check that `config.json` has `"threads": 5` (not too high)
→ Make sure your proxies are working format: `user:pass:ip:port`

## 🔥 KEY FEATURES:
- ✅ **Your Own Solver** - No 2captcha, no APIs, 100% free
- ✅ **All Terminals** - Linux, Windows, macOS, servers
- ✅ **Headless Mode** - Works without GUI
- ✅ **Non-Blocking** - Uses threading, won't freeze UI
- ✅ **Smart Retry** - Max 3 attempts per captcha
- ✅ **45s Timeout** - Never waits forever
- ✅ **All Proxy Formats** - user:pass:ip:port, http://, etc.

## 📝 PROXY FORMAT EXAMPLES (proxies.txt):
```
user:pass:192.168.1.1:8080
http://user:pass@192.168.1.1:8080
192.168.1.1:8080
user:pass@192.168.1.1:8080
```

## 🎉 READY TO GO!
Just run: `python main.py`
