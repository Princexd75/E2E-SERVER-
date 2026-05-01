import streamlit as st
import streamlit.components.v1 as components
import time
import threading
import uuid
import hashlib
import os
import subprocess
import json
import urllib.parse
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import database as db
import requests

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="E2E BY ROW3DY",
    page_icon="😋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS STYLING ---
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
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea, 
    .stNumberInput>div>div>input {
        background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.25);
        color: white;
    }

    .console-output {
        background: rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(78, 205, 196, 0.4);
        border-radius: 10px;
        padding: 12px;
        font-family: 'Courier New', monospace;
        font-size: 12px;
        color: #00ff88;
        max-height: 400px;
        overflow-y: auto;
    }
    
    .console-line {
        margin-bottom: 3px;
        padding-left: 28px;
        position: relative;
        border-left: 2px solid rgba(78, 205, 196, 0.4);
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        color: rgba(255, 255, 255, 0.7);
        margin-top: 3rem;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- CLASS & STATE ---
class AutomationState:
    def __init__(self):
        self.running = False
        self.message_count = 0
        self.logs = []
        self.message_rotation_index = 0

if 'automation_state' not in st.session_state:
    st.session_state.automation_state = AutomationState()

# --- HELPER FUNCTIONS ---
def log_message(msg, automation_state=None):
    timestamp = time.strftime("%H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"
    if automation_state:
        automation_state.logs.append(formatted_msg)
    else:
        if 'logs' not in st.session_state: st.session_state.logs = []
        st.session_state.logs.append(formatted_msg)

def setup_browser(automation_state=None):
    log_message('Setting up Chrome browser...', automation_state)
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    chromium_paths = ['/usr/bin/chromium', '/usr/bin/google-chrome', '/usr/bin/chrome']
    for path in chromium_paths:
        if Path(path).exists():
            chrome_options.binary_location = path
            break
            
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        log_message(f'Browser setup failed: {e}', automation_state)
        raise e

def find_message_input(driver, process_id, automation_state=None):
    selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"]',
        'textarea',
        'input[type="text"]'
    ]
    for selector in selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements: return elements[0]
        except: continue
    return None

def send_messages(config, automation_state):
    driver = None
    try:
        driver = setup_browser(automation_state)
        driver.get('https://www.facebook.com/')
        time.sleep(5)
        
        if config['cookies']:
            for cookie in config['cookies'].split(';'):
                if '=' in cookie:
                    name, value = cookie.strip().split('=', 1)
                    driver.add_cookie({'name': name, 'value': value, 'domain': '.facebook.com'})
        
        driver.get(f"https://www.facebook.com/messages/t/{config['chat_id']}")
        time.sleep(12)
        
        msg_input = find_message_input(driver, "AUTO-1", automation_state)
        if not msg_input:
            log_message("Error: Message box not found", automation_state)
            automation_state.running = False
            return
            
        messages_list = [m.strip() for m in config['messages'].split('\n') if m.strip()]
        delay = int(config['delay'])

        while automation_state.running:
            base_msg = messages_list[automation_state.message_rotation_index % len(messages_list)]
            final_msg = f"{config['name_prefix']} {base_msg}" if config['name_prefix'] else base_msg
            
            try:
                driver.execute_script("""
                    arguments[0].focus();
                    arguments[0].innerText = arguments[1];
                    arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                """, msg_input, final_msg)
                time.sleep(1)
                msg_input.send_keys(Keys.ENTER)
                
                automation_state.message_count += 1
                automation_state.message_rotation_index += 1
                log_message(f"✅ Message #{automation_state.message_count} Sent", automation_state)
                time.sleep(delay)
            except Exception as e:
                log_message(f"Send Error: {str(e)[:50]}", automation_state)
                time.sleep(5)

    except Exception as e:
        log_message(f"Fatal Error: {e}", automation_state)
        automation_state.running = False
    finally:
        if driver: driver.quit()

# --- MAIN APP INTERFACE ---
def main_app():
    st.markdown("""
    <div class="main-header">
        <img src="https://i.postimg.cc/Pq1HGqZK/459c85fcaa5d9f0762479bf382225ac6.jpg" class="prince-logo">
        <h1>💖 R0W3DY E2E OFFLINE 💖</h1>
        <p>Seven billion smiles in this world but yours is my favorites___💖😋</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["⚙️ Configuration", "🚀 Automation"])

    with tab1:
        st.markdown("### Bot Setup")
        chat_id = st.text_input("Target Chat ID", placeholder="Paste conversation ID here")
        name_prefix = st.text_input("Haters Name / Prefix", placeholder="e.g. [ROWEDY]")
        delay = st.number_input("Delay (Seconds)", min_value=1, value=5)
        cookies = st.text_area("Facebook Cookies", height=100, placeholder="Paste your cookies here")
        messages = st.text_area("Message List (One per line)", height=150, placeholder="Type messages here...")
        
        if st.button("Save Config", use_container_width=True):
            st.session_state.config = {
                'chat_id': chat_id,
                'name_prefix': name_prefix,
                'delay': delay,
                'cookies': cookies,
                'messages': messages
            }
            st.success("Configuration saved!")

    with tab2:
        state = st.session_state.automation_state
        col1, col2 = st.columns(2)
        col1.metric("Messages Sent", state.message_count)
        col2.metric("Status", "🟢 Running" if state.running else "🔴 Stopped")

        if st.button("▶️ Start Automation", disabled=state.running, use_container_width=True):
            if 'config' in st.session_state and st.session_state.config['chat_id']:
                state.running = True
                t = threading.Thread(target=send_messages, args=(st.session_state.config, state))
                t.daemon = True
                t.start()
                st.rerun()
            else:
                st.error("Please save configuration first!")

        if st.button("⏹️ Stop Automation", disabled=not state.running, use_container_width=True):
            state.running = False
            st.rerun()

        st.markdown("### 🖥️ Live Console")
        logs_html = '<div class="console-output">'
        for log in state.logs[-20:]:
            logs_html += f'<div class="console-line">{log}</div>'
        logs_html += '</div>'
        st.markdown(logs_html, unsafe_allow_html=True)
        
        if st.button("🔄 Clear Logs"):
            state.logs = []
            st.rerun()

    st.markdown('<div class="footer">Made with ❤️ by ROWEDY KING | © 2025</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main_app()
