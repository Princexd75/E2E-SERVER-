import streamlit as st
import time
import threading
import json
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

st.set_page_config(
    page_title="E2E BY ROW3DY",
    page_icon="🥵",
    layout="wide"
)

# Simplified CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .main-header {
        text-align: center;
        padding: 2rem;
        background: rgba(0,0,0,0.5);
        border-radius: 15px;
        margin-bottom: 2rem;
    }
    .console-output {
        background: black;
        color: #00ff00;
        padding: 15px;
        border-radius: 10px;
        font-family: monospace;
        max-height: 400px;
        overflow-y: auto;
    }
</style>
""", unsafe_allow_html=True)

CONFIG_FILE = "user_config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {'chat_id': '', 'name_prefix': '', 'delay': 5, 'cookies': '', 'messages': 'Hello!'}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

# Session state
if 'automation_state' not in st.session_state:
    st.session_state.automation_state = type('obj', (object,), {
        'running': False, 'message_count': 0, 'logs': [], 'message_rotation_index': 0
    })()

def log_message(msg):
    timestamp = time.strftime("%H:%M:%S")
    st.session_state.automation_state.logs.append(f"[{timestamp}] {msg}")

def send_messages_visible(config):
    """VISIBLE MODE - aap dekh sakte ho kya ho raha hai"""
    driver = None
    try:
        log_message("🚀 Starting automation in VISIBLE mode...")
        
        # Non-headless mode - aap browser dekh sakte ho
        chrome_options = Options()
        # COMMENT OUT headless - browser dikhega
        # chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1280,720')
        
        # Try to find chrome
        from selenium.webdriver.chrome.service import Service
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            log_message("✅ Chrome started successfully!")
        except:
            # Try with specific paths
            chrome_paths = ['/usr/bin/chromium', '/usr/bin/google-chrome']
            for cp in chrome_paths:
                if Path(cp).exists():
                    chrome_options.binary_location = cp
                    try:
                        driver = webdriver.Chrome(options=chrome_options)
                        log_message(f"✅ Chrome started with {cp}")
                        break
                    except:
                        continue
        
        if not driver:
            log_message("❌ Could not start Chrome browser")
            return 0
        
        # Go to Facebook
        log_message("📍 Navigating to Facebook...")
        driver.get('https://www.facebook.com/')
        time.sleep(5)
        
        # Add cookies if provided
        if config.get('cookies') and config['cookies'].strip():
            log_message("🍪 Adding cookies...")
            driver.get('https://www.facebook.com/')
            time.sleep(2)
            
            cookie_pairs = config['cookies'].split(';')
            for cookie in cookie_pairs:
                cookie = cookie.strip()
                if '=' in cookie:
                    name, value = cookie.split('=', 1)
                    try:
                        driver.add_cookie({'name': name, 'value': value, 'domain': '.facebook.com'})
                        log_message(f"   Added cookie: {name}")
                    except Exception as e:
                        log_message(f"   Failed: {name} - {str(e)[:50]}")
            
            driver.refresh()
            time.sleep(5)
        
        # Take screenshot to see current page
        screenshot_path = "facebook_login_check.png"
        driver.save_screenshot(screenshot_path)
        log_message(f"📸 Screenshot saved: {screenshot_path}")
        
        # Get current URL
        current_url = driver.current_url
        log_message(f"📍 Current URL: {current_url}")
        
        # Check if logged in
        page_source = driver.page_source.lower()
        if 'login' in page_source and 'password' in page_source:
            log_message("⚠️ WARNING: You are NOT logged into Facebook!")
            log_message("💡 Please add your Facebook cookies in Configuration tab")
        
        # Navigate to messages
        chat_id = config['chat_id'].strip()
        if chat_id:
            # Detect if it's E2EE chat
            if 'e2ee' in chat_id.lower() or len(chat_id) > 20:
                message_url = f'https://www.facebook.com/messages/e2ee/t/{chat_id}'
            else:
                message_url = f'https://www.facebook.com/messages/t/{chat_id}'
            
            log_message(f"📍 Opening conversation: {message_url}")
            driver.get(message_url)
        else:
            log_message("📍 Opening messages page")
            driver.get('https://www.facebook.com/messages')
        
        time.sleep(8)
        
        # Take screenshot of messages page
        driver.save_screenshot("messages_page.png")
        log_message(f"📸 Messages page screenshot saved")
        
        # Find message input
        log_message("🔍 Looking for message input box...")
        
        message_input = None
        selectors = [
            'div[contenteditable="true"][role="textbox"]',
            'div[contenteditable="true"]',
            'div[aria-label*="Message" i]',
            'div[aria-label*="message" i]',
            '[contenteditable="true"]'
        ]
        
        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for elem in elements:
                    if elem.is_displayed():
                        message_input = elem
                        log_message(f"✅ Found message input with selector: {selector}")
                        break
                if message_input:
                    break
            except:
                continue
        
        if not message_input:
            log_message("❌ Could NOT find message input box!")
            log_message("💡 Make sure you're logged into Facebook correctly")
            driver.save_screenshot("no_input_box.png")
            return 0
        
        # Send messages
        messages_list = [msg.strip() for msg in config.get('messages', '').split('\n') if msg.strip()]
        if not messages_list:
            messages_list = ['Test message from automation']
        
        delay = int(config.get('delay', 5))
        sent_count = 0
        
        while st.session_state.automation_state.running:
            for msg in messages_list:
                if not st.session_state.automation_state.running:
                    break
                
                if config.get('name_prefix'):
                    full_msg = f"{config['name_prefix']} {msg}"
                else:
                    full_msg = msg
                
                log_message(f"✏️ Typing: {full_msg[:50]}...")
                
                # Type message
                try:
                    # Click and focus
                    driver.execute_script("arguments[0].click();", message_input)
                    time.sleep(0.5)
                    
                    # Clear and type
                    driver.execute_script("""
                        arguments[0].focus();
                        arguments[0].innerHTML = '';
                        arguments[0].textContent = '';
                    """, message_input)
                    time.sleep(0.3)
                    
                    # Type using JavaScript
                    driver.execute_script("""
                        const element = arguments[0];
                        const text = arguments[1];
                        element.textContent = text;
                        element.dispatchEvent(new Event('input', {bubbles: true}));
                    """, message_input, full_msg)
                    
                    time.sleep(1)
                    
                    # Try to send
                    send_success = False
                    
                    # Method 1: Find send button
                    send_btn = driver.execute_script("""
                        const btns = document.querySelectorAll('[aria-label*="Send" i], [data-testid="send-button"], div[role="button"]');
                        for (let btn of btns) {
                            if (btn.innerText.toLowerCase().includes('send') || 
                                btn.getAttribute('aria-label')?.toLowerCase().includes('send')) {
                                btn.click();
                                return true;
                            }
                        }
                        return false;
                    """)
                    
                    if send_success:
                        log_message(f"✅ Sent via button: {full_msg[:30]}...")
                    else:
                        # Method 2: Press Enter
                        driver.execute_script("""
                            const element = arguments[0];
                            element.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter', keyCode: 13}));
                            element.dispatchEvent(new KeyboardEvent('keyup', {key: 'Enter', code: 'Enter', keyCode: 13}));
                        """, message_input)
                        log_message(f"✅ Sent via Enter: {full_msg[:30]}...")
                    
                    sent_count += 1
                    st.session_state.automation_state.message_count = sent_count
                    
                    # Take screenshot after sending
                    if sent_count % 3 == 0:
                        driver.save_screenshot(f"message_{sent_count}.png")
                        log_message(f"📸 Screenshot saved: message_{sent_count}.png")
                    
                    log_message(f"⏰ Waiting {delay} seconds...")
                    time.sleep(delay)
                    
                except Exception as e:
                    log_message(f"❌ Error sending: {str(e)[:100]}")
                    time.sleep(3)
        
        log_message(f"🏁 Automation stopped. Total messages: {sent_count}")
        return sent_count
        
    except Exception as e:
        log_message(f"❌ Fatal error: {str(e)}")
        return 0
    finally:
        if driver:
            log_message("🔒 Keeping browser open for 10 seconds...")
            time.sleep(10)
            driver.quit()
            log_message("🔒 Browser closed")

def start_automation(config):
    if st.session_state.automation_state.running:
        return
    
    st.session_state.automation_state.running = True
    st.session_state.automation_state.message_count = 0
    st.session_state.automation_state.logs = []
    
    thread = threading.Thread(target=send_messages_visible, args=(config,))
    thread.daemon = True
    thread.start()

def stop_automation():
    st.session_state.automation_state.running = False

# UI
st.markdown("""
<div class="main-header">
    <h1>🥵 R0W3DY E2E OFFLINE 😘</h1>
    <p>Facebook Message Automation - Visible Mode for Debugging</p>
</div>
""", unsafe_allow_html=True)

# Load config
config = load_config()

# Sidebar
st.sidebar.markdown("### 👑 ROW3DY KING")
st.sidebar.success("✅ Debug Mode Active")
st.sidebar.info("📸 Screenshots will be saved in current directory")

# Main tabs
tab1, tab2 = st.tabs(["⚙️ Configuration", "🚀 Automation"])

with tab1:
    st.markdown("### ⚙️ Configuration Settings")
    
    chat_id = st.text_input("Chat/Conversation ID", value=config.get('chat_id', ''),
                           placeholder="Facebook chat ID from URL",
                           help="Open chat in browser, copy ID from URL")
    
    name_prefix = st.text_input("Name Prefix (Optional)", value=config.get('name_prefix', ''),
                               placeholder="e.g., [BOSS]")
    
    delay = st.number_input("Delay Between Messages (seconds)", min_value=2, max_value=30,
                           value=config.get('delay', 5))
    
    cookies = st.text_area("Facebook Cookies (IMPORTANT!)", value=config.get('cookies', ''),
                          placeholder="Paste cookies here to stay logged in:\nc_user=123456; xs=123456; etc...",
                          height=100,
                          help="Without cookies, you won't be logged in!")
    
    messages = st.text_area("Messages (one per line)", value=config.get('messages', ''),
                           placeholder="Hello!\nHow are you?\nTest message",
                           height=150)
    
    if st.button("💾 Save Configuration", use_container_width=True):
        config = {
            'chat_id': chat_id,
            'name_prefix': name_prefix,
            'delay': delay,
            'cookies': cookies,
            'messages': messages
        }
        save_config(config)
        st.success("✅ Configuration saved!")
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📖 How to Get Chat ID:")
    st.markdown("""
    1. Open Facebook Messenger in browser
    2. Open the chat you want to automate
    3. Look at URL: `https://www.facebook.com/messages/t/CHAT_ID_HERE`
    4. Copy that CHAT_ID
    
    **For E2EE chats:** URL will be `https://www.facebook.com/messages/e2ee/t/...`
    """)

with tab2:
    st.markdown("### 🚀 Automation Control")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Messages Sent", st.session_state.automation_state.message_count)
    with col2:
        status = "🟢 RUNNING" if st.session_state.automation_state.running else "🔴 STOPPED"
        st.metric("Status", status)
    with col3:
        has_chat = "✅ Set" if config.get('chat_id') else "❌ Not Set"
        st.metric("Chat ID", has_chat)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ START AUTOMATION", disabled=st.session_state.automation_state.running, use_container_width=True):
            if config.get('chat_id'):
                start_automation(config)
                st.success("✅ Automation started! Watch the browser window...")
                st.rerun()
            else:
                st.error("❌ Please set Chat ID first!")
    
    with col2:
        if st.button("⏹️ STOP AUTOMATION", disabled=not st.session_state.automation_state.running, use_container_width=True):
            stop_automation()
            st.warning("⚠️ Automation stopped!")
            st.rerun()
    
    # Live logs
    if st.session_state.automation_state.logs:
        st.markdown("### 📊 Live Console")
        logs_html = '<div class="console-output">'
        for log in st.session_state.automation_state.logs[-50:]:
            logs_html += f'<div>➤ {log}</div>'
        logs_html += '</div>'
        st.markdown(logs_html, unsafe_allow_html=True)
        
        if st.button("🔄 Clear Logs"):
            st.session_state.automation_state.logs = []
            st.rerun()

st.markdown("---")
st.markdown("<center>Made with ❤️ by ROWEDY KING</center>", unsafe_allow_html=True)
