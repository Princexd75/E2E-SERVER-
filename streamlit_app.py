import streamlit as st
import streamlit.components.v1 as components
import time
import threading
import hashlib
import os
import json
import urllib.parse
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

st.set_page_config(
    page_title="E2E BY ROW3DY",
    page_icon="🥵",
    layout="wide",
    initial_sidebar_state="expanded"
)

custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        background-image: url('https://i.postimg.cc/TYhXd0gG/d0a72a8cea5ae4978b21e04a74f0b0ee.jpg');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    .main .block-container {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(8px);
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.12);
    }
    
    .main-header {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    .main-header h1 {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    .prince-logo {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        margin-bottom: 15px;
        border: 3px solid #4ecdc4;
        box-shadow: 0 4px 15px rgba(78, 205, 196, 0.5);
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        width: 100%;
    }
    
    .stButton>button:hover {
        opacity: 0.9;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea, 
    .stNumberInput>div>div>input {
        background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 8px;
        color: white;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input::placeholder,
    .stTextArea>div>div>textarea::placeholder {
        color: rgba(255, 255, 255, 0.6);
    }
    
    .stTextInput>div>div>input:focus, 
    .stTextArea>div>div>textarea:focus {
        background: rgba(255, 255, 255, 0.2);
        border-color: #4ecdc4;
        box-shadow: 0 0 0 2px rgba(78, 205, 196, 0.2);
        color: white;
    }
    
    label {
        color: white !important;
        font-weight: 500 !important;
        font-size: 14px !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.06);
        padding: 10px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        color: white;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
    }
    
    [data-testid="stMetricValue"] {
        color: #4ecdc4;
        font-weight: 700;
        font-size: 1.8rem;
    }
    
    [data-testid="stMetricLabel"] {
        color: rgba(255, 255, 255, 0.9);
        font-weight: 500;
    }
    
    .console-section {
        margin-top: 20px;
        padding: 15px;
        background: rgba(255, 255, 255, 0.06);
        border-radius: 10px;
        border: 1px solid rgba(78, 205, 196, 0.3);
    }
    
    .console-header {
        color: #4ecdc4;
        text-shadow: 0 0 10px rgba(78, 205, 196, 0.5);
        margin-bottom: 20px;
        font-weight: 600;
    }
    
    .console-output {
        background: rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(78, 205, 196, 0.4);
        border-radius: 10px;
        padding: 12px;
        font-family: 'Courier New', 'Consolas', 'Monaco', monospace;
        font-size: 12px;
        color: #00ff88;
        line-height: 1.6;
        max-height: 400px;
        overflow-y: auto;
        scrollbar-width: thin;
        scrollbar-color: rgba(78, 205, 196, 0.5) rgba(0, 0, 0, 0.2);
    }
    
    .console-output::-webkit-scrollbar {
        width: 8px;
    }
    
    .console-output::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.2);
    }
    
    .console-output::-webkit-scrollbar-thumb {
        background: rgba(78, 205, 196, 0.5);
        border-radius: 4px;
    }
    
    .console-output::-webkit-scrollbar-thumb:hover {
        background: rgba(78, 205, 196, 0.7);
    }
    
    .console-line {
        margin-bottom: 3px;
        word-wrap: break-word;
        padding: 6px 10px;
        padding-left: 28px;
        color: #00ff88;
        background: rgba(78, 205, 196, 0.08);
        border-left: 2px solid rgba(78, 205, 196, 0.4);
        position: relative;
    }
    
    .console-line::before {
        content: '►';
        position: absolute;
        left: 10px;
        opacity: 0.6;
        color: #4ecdc4;
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        color: rgba(255, 255, 255, 0.7);
        font-weight: 600;
        margin-top: 3rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        border-top: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    [data-testid="stSidebar"] {
        background: rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stSidebar"] .element-container {
        color: white;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Configuration file paths
CONFIG_FILE = "user_config.json"

# Load config from file
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

# Initialize session state
if 'automation_running' not in st.session_state:
    st.session_state.automation_running = False
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'message_count' not in st.session_state:
    st.session_state.message_count = 0
if 'config' not in st.session_state:
    st.session_state.config = load_config()

class AutomationState:
    def __init__(self):
        self.running = False
        self.message_count = 0
        self.logs = []
        self.message_rotation_index = 0

if 'automation_state' not in st.session_state:
    st.session_state.automation_state = AutomationState()

ADMIN_UID = "100003995292301"

def log_message(msg, automation_state=None):
    timestamp = time.strftime("%H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"
    
    if automation_state:
        automation_state.logs.append(formatted_msg)
    else:
        if 'logs' in st.session_state:
            st.session_state.logs.append(formatted_msg)

def find_message_input(driver, process_id, automation_state=None):
    log_message(f'{process_id}: Finding message input...', automation_state)
    time.sleep(10)
    
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
    except Exception:
        pass
    
    message_input_selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"][data-lexical-editor="true"]',
        'div[aria-label*="message" i][contenteditable="true"]',
        'div[aria-label*="Message" i][contenteditable="true"]',
        'div[contenteditable="true"][spellcheck="true"]',
        '[role="textbox"][contenteditable="true"]',
        'textarea[placeholder*="message" i]',
        'div[aria-placeholder*="message" i]',
        'div[data-placeholder*="message" i]',
        '[contenteditable="true"]',
        'textarea',
        'input[type="text"]'
    ]
    
    for idx, selector in enumerate(message_input_selectors):
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            
            for element in elements:
                try:
                    is_editable = driver.execute_script("""
                        return arguments[0].contentEditable === 'true' || 
                               arguments[0].tagName === 'TEXTAREA' || 
                               arguments[0].tagName === 'INPUT';
                    """, element)
                    
                    if is_editable:
                        try:
                            element.click()
                            time.sleep(0.5)
                        except:
                            pass
                        
                        return element
                except Exception:
                    continue
        except Exception:
            continue
    
    return None

def setup_browser(automation_state=None):
    log_message('Setting up Chrome browser...', automation_state)
    
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
    
    chromium_paths = [
        '/usr/bin/chromium',
        '/usr/bin/chromium-browser',
        '/usr/bin/google-chrome',
        '/usr/bin/chrome'
    ]
    
    for chromium_path in chromium_paths:
        if Path(chromium_path).exists():
            chrome_options.binary_location = chromium_path
            log_message(f'Found Chromium at: {chromium_path}', automation_state)
            break
    
    chromedriver_paths = [
        '/usr/bin/chromedriver',
        '/usr/local/bin/chromedriver'
    ]
    
    driver_path = None
    for driver_candidate in chromedriver_paths:
        if Path(driver_candidate).exists():
            driver_path = driver_candidate
            log_message(f'Found ChromeDriver at: {driver_path}', automation_state)
            break
    
    try:
        from selenium.webdriver.chrome.service import Service
        
        if driver_path:
            service = Service(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            log_message('Chrome started with detected ChromeDriver!', automation_state)
        else:
            driver = webdriver.Chrome(options=chrome_options)
            log_message('Chrome started with default driver!', automation_state)
        
        driver.set_window_size(1920, 1080)
        log_message('Chrome browser setup completed successfully!', automation_state)
        return driver
    except Exception as error:
        log_message(f'Browser setup failed: {error}', automation_state)
        raise error

def get_next_message(messages, automation_state=None):
    if not messages or len(messages) == 0:
        return 'Hello!'
    
    if automation_state:
        message = messages[automation_state.message_rotation_index % len(messages)]
        automation_state.message_rotation_index += 1
    else:
        message = messages[0]
    
    return message

def send_messages(config, automation_state, process_id='AUTO-1'):
    driver = None
    try:
        log_message(f'{process_id}: Starting automation...', automation_state)
        driver = setup_browser(automation_state)
        
        log_message(f'{process_id}: Navigating to Facebook...', automation_state)
        driver.get('https://www.facebook.com/')
        time.sleep(8)
        
        if config.get('cookies') and config['cookies'].strip():
            log_message(f'{process_id}: Adding cookies...', automation_state)
            cookie_array = config['cookies'].split(';')
            for cookie in cookie_array:
                cookie_trimmed = cookie.strip()
                if cookie_trimmed:
                    first_equal_index = cookie_trimmed.find('=')
                    if first_equal_index > 0:
                        name = cookie_trimmed[:first_equal_index].strip()
                        value = cookie_trimmed[first_equal_index + 1:].strip()
                        try:
                            driver.add_cookie({
                                'name': name,
                                'value': value,
                                'domain': '.facebook.com',
                                'path': '/'
                            })
                        except Exception:
                            pass
        
        if config.get('chat_id'):
            chat_id = config['chat_id'].strip()
            log_message(f'{process_id}: Opening conversation {chat_id}...', automation_state)
            driver.get(f'https://www.facebook.com/messages/t/{chat_id}')
        else:
            log_message(f'{process_id}: Opening messages...', automation_state)
            driver.get('https://www.facebook.com/messages')
        
        time.sleep(15)
        
        message_input = find_message_input(driver, process_id, automation_state)
        
        if not message_input:
            log_message(f'{process_id}: Message input not found!', automation_state)
            automation_state.running = False
            return 0
        
        delay = int(config.get('delay', 5))
        messages_sent = 0
        messages_list = [msg.strip() for msg in config.get('messages', '').split('\n') if msg.strip()]
        
        if not messages_list:
            messages_list = ['Hello!']
        
        while automation_state.running:
            base_message = get_next_message(messages_list, automation_state)
            
            if config.get('name_prefix'):
                message_to_send = f"{config['name_prefix']} {base_message}"
            else:
                message_to_send = base_message
            
            try:
                driver.execute_script("""
                    const element = arguments[0];
                    const message = arguments[1];
                    
                    element.scrollIntoView({behavior: 'smooth', block: 'center'});
                    element.focus();
                    element.click();
                    
                    if (element.tagName === 'DIV') {
                        element.textContent = message;
                        element.innerHTML = message;
                    } else {
                        element.value = message;
                    }
                    
                    element.dispatchEvent(new Event('input', { bubbles: true }));
                    element.dispatchEvent(new Event('change', { bubbles: true }));
                    element.dispatchEvent(new InputEvent('input', { bubbles: true, data: message }));
                """, message_input, message_to_send)
                
                time.sleep(1)
                
                sent = driver.execute_script("""
                    const sendButtons = document.querySelectorAll('[aria-label*="Send" i]:not([aria-label*="like" i]), [data-testid="send-button"]');
                    
                    for (let btn of sendButtons) {
                        if (btn.offsetParent !== null) {
                            btn.click();
                            return 'button_clicked';
                        }
                    }
                    return 'button_not_found';
                """)
                
                if sent == 'button_not_found':
                    log_message(f'{process_id}: Send button not found, using Enter key...', automation_state)
                    driver.execute_script("""
                        const element = arguments[0];
                        element.focus();
                        
                        const events = [
                            new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                            new KeyboardEvent('keypress', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                            new KeyboardEvent('keyup', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true })
                        ];
                        
                        events.forEach(event => element.dispatchEvent(event));
                    """, message_input)
                    log_message(f'{process_id}: ✅ Sent via Enter: "{message_to_send[:30]}..."', automation_state)
                else:
                    log_message(f'{process_id}: ✅ Sent via button: "{message_to_send[:30]}..."', automation_state)
                
                messages_sent += 1
                automation_state.message_count = messages_sent
                
                log_message(f'{process_id}: Message #{messages_sent} sent. Waiting {delay}s...', automation_state)
                time.sleep(delay)
                
            except Exception as e:
                log_message(f'{process_id}: Send error: {str(e)[:100]}', automation_state)
                time.sleep(5)
        
        log_message(f'{process_id}: Automation stopped. Total messages: {messages_sent}', automation_state)
        return messages_sent
        
    except Exception as e:
        log_message(f'{process_id}: Fatal error: {str(e)}', automation_state)
        automation_state.running = False
        return 0
    finally:
        if driver:
            try:
                driver.quit()
                log_message(f'{process_id}: Browser closed', automation_state)
            except:
                pass

def start_automation(config):
    automation_state = st.session_state.automation_state
    
    if automation_state.running:
        return
    
    automation_state.running = True
    automation_state.message_count = 0
    automation_state.logs = []
    
    thread = threading.Thread(target=send_messages, args=(config, automation_state))
    thread.daemon = True
    thread.start()

def stop_automation():
    st.session_state.automation_state.running = False

def main_app():
    st.markdown('<div class="main-header"><img src="https://i.postimg.cc/Pq1HGqZK/459c85fcaa5d9f0762479bf382225ac6.jpg" class="prince-logo"><h1>🥵 R0W3DY E2E OFFLINE 😘</h1><p>seven billion smiles in this world but yours is my favorite___🥵😘</p></div>', unsafe_allow_html=True)
    
    st.sidebar.markdown(f"### 👤 ROW3DY USER")
    st.sidebar.success("✅ Automation Ready")
    
    tab1, tab2 = st.tabs(["⚙️ Configuration", "🚀 Automation"])
    
    with tab1:
        st.markdown("### Configuration")
        
        chat_id = st.text_input("Chat/Conversation ID", value=st.session_state.config.get('chat_id', ''), 
                               placeholder="e.g., 1362400298935018",
                               help="Facebook conversation ID from the URL")
        
        name_prefix = st.text_input("Name Prefix", value=st.session_state.config.get('name_prefix', ''),
                                   placeholder="e.g., [END TO END]",
                                   help="Prefix to add before each message")
        
        delay = st.number_input("Delay (seconds)", min_value=1, max_value=300, 
                               value=st.session_state.config.get('delay', 5),
                               help="Wait time between messages")
        
        cookies = st.text_area("Facebook Cookies (optional)", 
                              value=st.session_state.config.get('cookies', ''),
                              placeholder="Paste your Facebook cookies here",
                              height=100,
                              help="Your cookies are never shared")
        
        messages = st.text_area("Messages (one per line)", 
                               value=st.session_state.config.get('messages', ''),
                               placeholder="Enter each message on a new line",
                               height=150,
                               help="Enter each message on a new line")
        
        if st.button("💾 Save Configuration", use_container_width=True):
            st.session_state.config = {
                'chat_id': chat_id,
                'name_prefix': name_prefix,
                'delay': delay,
                'cookies': cookies,
                'messages': messages
            }
            save_config(st.session_state.config)
            st.success("✅ Configuration saved successfully!")
            st.rerun()
    
    with tab2:
        st.markdown("### Automation Control")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Messages Sent", st.session_state.automation_state.message_count)
        with col2:
            status = "🟢 Running" if st.session_state.automation_state.running else "🔴 Stopped"
            st.metric("Status", status)
        with col3:
            st.metric("Chat ID", st.session_state.config.get('chat_id', '')[:10] + "..." if st.session_state.config.get('chat_id') else "Not Set")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("▶️ Start Automation", disabled=st.session_state.automation_state.running, use_container_width=True):
                if st.session_state.config.get('chat_id'):
                    start_automation(st.session_state.config)
                    st.success("✅ Automation started!")
                    st.rerun()
                else:
                    st.error("❌ Please set Chat ID in Configuration first!")
        
        with col2:
            if st.button("⏹️ Stop Automation", disabled=not st.session_state.automation_state.running, use_container_width=True):
                stop_automation()
                st.warning("⚠️ Automation stopped!")
                st.rerun()
        
        if st.session_state.automation_state.logs:
            st.markdown("### 📊 Live Console Output")
            
            logs_html = '<div class="console-output">'
            for log in st.session_state.automation_state.logs[-30:]:
                logs_html += f'<div class="console-line">{log}</div>'
            logs_html += '</div>'
            
            st.markdown(logs_html, unsafe_allow_html=True)
            
            if st.button("🔄 Refresh Logs"):
                st.rerun()

# Directly call main_app
main_app()

st.markdown('<div class="footer">Made with ❤️ by ROWEDY KING | © 2025</div>', unsafe_allow_html=True)
