#----------------------
# Creator: vbookshelf
# GitHub: https://github.com/vbookshelf/myOfflineAi
# License: MIT
# Version: 1.0
#----------------------

from flask import Flask, render_template_string, request, jsonify, Response
import json
import os
import sys
import base64
import fitz  # PyMuPDF
from PIL import Image
import io

import requests
import subprocess

import ollama
from ollama import chat as ollama_chat, ChatResponse
from urllib.parse import urlparse



# The context size of all Ollama models is set to 4096 tokens.
# There is no warning when the context is exceeded, but
# the quality of the responses becomes very poor.
# This happens because Ollama will automatically drop the oldest 
# messages/tokens from the history to make space for the new input. 
# You don’t see an error, but earlier conversation context is silently lost.

# Here we set a custom context size.
# Note: Setting large context sizes will slow down inference.
NUM_CTX = 16000


TEMPERATURE = 0.6
TOP_K = 60
TOP_P = 0.95
FREQUENCY_PENALTY = 1.0
REPEAT_PENALTY = 1.0


# Max number of pdf pages allowed per pdf file
MAX_PAGES = 15

# Each pdf page is converted into an image.
# The image resolution is set here.
# Use moderate DPI for balance of quality/size
# 1.5x scale provides good readability while reducing file size
PDF_IMAGE_RES = 1.5 # 150 dpi

# Max pdf upload size
MAX_UPLOAD_FILE_SIZE = 20 * 1024 * 1024 # (20MB)

# The name of the last model selected
# is stored in this file
LAST_MODEL_FILE = "last_model.txt"

# User created agents are stored in this file
AGENTS_FILE = "agents.json"



# -----------------------------------------
# Remember the last model:
# This code remembers the last model that the user selected so
# the user's favorite model is always selected in the dropdown.
# The model name is saved in a file named last_model.txt
# -----------------------------------------

def save_last_model(model_name):
    """Saves the last selected model name to a file."""
    try:
        with open(LAST_MODEL_FILE, "w") as f:
            f.write(model_name)
    except IOError as e:
        print(f"[ERROR] Could not save the last model selection: {e}", file=sys.stderr)

def load_last_model():
    """Loads the last selected model name from a file if it exists."""
    if not os.path.exists(LAST_MODEL_FILE):
        return None
    try:
        with open(LAST_MODEL_FILE, "r") as f:
            return f.read().strip()
    except IOError as e:
        print(f"[ERROR] Could not read the last model selection: {e}", file=sys.stderr)
        return None



# -----------------------------------------
# Make sure that the app only connects to localhost:
# On Mac/Windows the Ollama desktop application usually launches 
# the Ollama server automatically on startup.
# Enforce that OLLAMA_HOST points to localhost only.
# -----------------------------------------

current_ollama_host = os.environ.get("OLLAMA_HOST", "").strip()

print('++++++++++++')
print(f"Current Ollama host: {current_ollama_host!r}")
print('++++++++++++')

def is_localhost_url(url):
    if not url:
        return True  # treat empty as using default localhost client (be strict if you prefer)
    parsed = urlparse(url if "://" in url else "http://" + url)
    hostname = parsed.hostname
    port = parsed.port or 11434
    if hostname in ("127.0.0.1", "localhost") and port == 11434:
        return True
    return False

if not is_localhost_url(current_ollama_host):
    print(f"[SECURITY] OLLAMA_HOST is not localhost: {current_ollama_host}. Aborting start.", file=sys.stderr)
    sys.exit(1)
	
	
	
# -----------------------------------------
# Get a list of Ollama models that the user has downloaded:
# This code ensures that all the models that the user has downloaded
# appear in the dropdown menu, ready to be used.
# -----------------------------------------


def get_ollama_models():
    # Try Ollama HTTP API first
    try:
        resp = requests.get("http://localhost:11434/api/tags", timeout=3)
        resp.raise_for_status()
        data = resp.json()
        return [m["name"] for m in data.get("models", [])]
    except Exception:
        # Fallback to CLI if API is not available
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
            lines = result.stdout.strip().splitlines()
            if len(lines) > 1:
                # skip header, split on whitespace, take first column
                return [line.split()[0] for line in lines[1:]]
        except Exception:
            pass
    return []


model_list = get_ollama_models()
if not model_list:
    # fallback in case nothing is found
    model_list = ['gemma3:4b', 'gemma3:12b', 'qwen3:4b', 'qwen3:14b']

# Try to load the last used model
last_model = load_last_model()

# Check if the loaded model exists in the current list of available models
if last_model and last_model in model_list:
    MODEL_NAME = last_model
    print(f"[INFO] Loaded last used model: {MODEL_NAME}")
else:
    MODEL_NAME = model_list[0]  # Default to the first available if not found or invalid
    print(f"[INFO] Defaulting to first available model: {MODEL_NAME}")
		
	
	
# -----------------------------------------
# Flask Code
# -----------------------------------------

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_UPLOAD_FILE_SIZE


# --- HTML Template ---
HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>myOfflineAi</title>
	
	<script src="{{ url_for('static', filename='tailwind.js') }}"></script>
	<script src="{{ url_for('static', filename='marked.min.js') }}"></script>
	<link rel="stylesheet" href="{{ url_for('static', filename='atom-one-dark.min.css') }}">
	<script src="{{ url_for('static', filename='highlight.min.js') }}"></script>
	<link rel="shortcut icon" type="image/png" href="static/icon.png">

    <style>
        /* Main page styling */
        body {
            font-family: 'Arial', sans-serif;
            background-color: white;
        }
        
        /* Custom scrollbar styles for better UX */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: #e2e8f0; /* slate-200 */
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb {
            background: #94a3b8; /* slate-400 */
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #64748b; /* slate-500 */
        }
        
        /* Sidebar animation for mobile toggle */
        #agent-sidebar {
            transition: transform 0.3s ease-in-out;
        }
        
        /* Loading/typing animation for when AI is responding */
        .typing-dot {
            animation: typing-bounce 1.2s infinite ease-in-out;
        }
        .typing-dot:nth-child(2) {
            animation-delay: 0.2s;
        }
        .typing-dot:nth-child(3) {
            animation-delay: 0.4s;
        }
        @keyframes typing-bounce {
            0%, 80%, 100% {
                transform: scale(0);
            }
            40% {
                transform: scale(1.0);
            }
        }
        
        /* Styling for agent icons in the sidebar */
        .agent-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 2rem;
            font-weight: bold;
            border-radius: 0.75rem; /* rounded-xl */
            border-width: 4px;
            border-color: #1e293b; /* slate-800 */
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05); /* shadow-sm */
            width: 4rem; /* w-16 */
            height: 4rem; /* h-16 */
        }
        
        /* Model selector dropdown styling */
        .model-selector {
            border: 1px solid #6b7280; /* Gray-500 */
        }
        
        /* Scrollbar styling for message content areas */
        .message-content::-webkit-scrollbar {
            width: 6px;
        }
        .message-content::-webkit-scrollbar-track {
            background: #e2e8f0;
            border-radius: 10px;
        }
        .message-content::-webkit-scrollbar-thumb {
            background: #94a3b8;
            border-radius: 10px;
        }
        .message-content::-webkit-scrollbar-thumb:hover {
            background: #64748b;
        }
        
        /* --- Styles for Markdown Content in AI responses --- */
        .markdown-content h1, .markdown-content h2, .markdown-content h3 {
            font-weight: bold;
            margin-top: 1.25rem;
            margin-bottom: 0.75rem;
        }
        .markdown-content h1 { font-size: 1.5rem; }
        .markdown-content h2 { font-size: 1.25rem; }
        .markdown-content h3 { font-size: 1.125rem; }
        .markdown-content p {
			/*font-size: 17px;*/
            margin-bottom: 0.75rem;
            line-height: 1.6;
        }
        .markdown-content ul, .markdown-content ol {
            list-style-position: outside;
            margin-left: 1.5rem;
            margin-bottom: 0.75rem;
            line-height: 2.0;
        }
        .markdown-content a {
            color: #4f46e5;
            text-decoration: underline;
            font-weight: 500;
        }
        .markdown-content blockquote {
            border-left: 4px solid #cbd5e1; /* slate-300 */
            padding-left: 1rem;
            margin: 1rem 0.5rem;
            font-style: italic;
            color: #64748b; /* slate-500 */
        }
        .markdown-content code {
            font-family: monospace;
            font-size: 0.875rem;
            background-color: #e2e8f0;
            padding: 0.2rem 0.4rem;
            border-radius: 0.25rem;
        }
        
        /* Code block wrapper styling with copy button */
        .code-block-wrapper {
            position: relative;
            margin-top: 0.5rem;
            margin-bottom: 1rem;
            background-color: #1a202c; /* Darker code block bg */
            border-radius: 0.5rem;
            overflow: hidden;
        }
        .code-block-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #2d3748; /* Header bg */
            padding: 0.5rem 0.75rem;
            color: #e2e8f0;
            font-size: 0.8rem;
        }
        .copy-btn {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            background-color: #4a5568;
            border: none;
            padding: 0.25rem 0.5rem;
            border-radius: 0.25rem;
            cursor: pointer;
            transition: background-color 0.2s;
            font-size: 0.8rem;
        }
        .copy-btn:hover {
            background-color: #718096;
        }
        
        /* Override default code block styles within our wrapper */
        .markdown-content .code-block-wrapper pre {
            background-color: transparent !important;
            margin: 0;
            padding: 0.75rem;
            border-radius: 0;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        .markdown-content .code-block-wrapper pre code,
        .markdown-content .code-block-wrapper pre code.hljs {
            background: transparent !important;
            padding: 0;
            color: #e2e8f0;
        }
		
        /* Styling for AI "thinking" bubble (reasoning display) */
		.thinking-bubble {
		    font-size: 0.85rem;
		    opacity: 0.9;
		    max-height: 200px;
		    overflow-y: auto;
		    white-space: pre-wrap;
		    transition: background-color 0.2s;
		}
		.thinking-bubble:hover {
		    background-color: #e2e8f0; /* slate-200 hover */
		}
		.hidden-reasoning {
		    font-family: monospace;
		    line-height: 1.4;
		    white-space: pre-wrap;
		}
        .edit-agent-btn {
            opacity: 0;
            transition: opacity 0.2s ease-in-out;
        }
        .agent-item:hover .edit-agent-btn {
            opacity: 1;
        }
    </style>
	
</head>
<body class="flex h-screen overflow-hidden text-slate-800">

    <div class="flex flex-1 overflow-hidden relative max-w-7xl mx-auto">
	
        <aside id="agent-sidebar" class="w-full md:w-80 lg:w-96 p-4 bg-slate-800 border-r border-slate-700 text-slate-100 overflow-y-auto flex-shrink-0 absolute md:relative h-full z-20 md:z-10 transform -translate-x-full md:translate-x-0">
            <div class="flex justify-between items-center mb-4">
				<button id="close-sidebar-btn" class="md:hidden text-slate-400 hover:text-white">
				    <span class="text-xl">&times;</span>
				</button>
            </div>
            
            <div class="mb-4">
                <label for="model-selector" class="block text-sm font-medium text-slate-300 mb-2">Select Model:</label>
                <select id="model-selector" class="bg-slate-800 model-selector w-full p-3 rounded-lg text-white focus:outline-none transition-all duration-200">
                    {% for model in model_list %}
                    <option value="{{ model }}" {% if model == current_model %}selected{% endif %} class="bg-slate-800 text-white">{{ model }}</option>
                    {% endfor %}
                </select>
				
                <div id="model-status" class="invisible mt-2 text-xs text-slate-400">
                    Current: <span id="current-model-display">{{ current_model }}</span>
                </div>
            </div>
            
            <div class="mb-4">
                <button id="open-create-agent-modal-btn" class="w-full py-2.5 px-4 bg-indigo-600 text-white rounded-lg font-semibold hover:bg-indigo-700 transition-colors duration-200 flex items-center justify-center space-x-2">
                    <span>+</span>
                    <span>Create Ai Tool</span>
                </button>
            </div>
            
            <div id="agent-list" class="w-full space-y-3">
            </div>
        </aside>
        
        <main class="flex-1 flex flex-col bg-slate-100">
				
			<header class="md:hidden flex items-center justify-between p-3 bg-white border-b border-slate-200 shadow-sm">
			    <button id="open-sidebar-btn" class="text-slate-600 hover:text-indigo-600">
			        <span class="text-xl">&#9776;</span>
			    </button>
			    <h2 id="mobile-header-title" class="font-bold text-lg">myOfflineAi</h2>
			    <div class="w-8"></div>
			</header>
            
            <div id="tab-header" class="hidden flex w-full flex-shrink-0 p-2 bg-white/80 backdrop-blur-sm border-b border-slate-200 shadow-sm overflow-x-auto whitespace-nowrap">
            </div>
            
            <div id="tab-content" class="flex-1 flex flex-col p-2 sm:p-4 overflow-hidden">
                <div id="initial-message" class="flex-1 flex items-center justify-center text-center text-slate-500">
                    <div>
                        <span class="text-7xl text-slate-300 mb-2">myOfflineAi</span>
                        <p class="text-xl font-semibold mb-2 mt-3">Private. Transparent. Free.</p>
                        <p>For maximum security please switch off your internet connection<br>
						and put the Ollama desktop app into Airplane mode.<br>
						The system messages of the Ai tools you create are stored in a file.<br>
						Therefore, you are advised not to include<br>
						sensitive information in the tool system messages.</p>
                    </div>
                </div>
            </div>
        </main>
		
		
    </div>
    
    <div id="error-modal" class="hidden fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4">
        <div class="bg-white rounded-lg p-6 w-full max-w-sm shadow-xl">
            <h2 class="text-2xl font-bold text-red-600 mb-4 flex items-center">
                <span class="mr-3">⚠️</span>Error
            </h2>
            <p id="error-message" class="text-slate-700 mb-6"></p>
            <div class="flex justify-end">
                <button id="close-error-modal-btn" class="py-2 px-5 bg-slate-200 text-slate-800 rounded-lg hover:bg-slate-300 transition-colors duration-200 font-semibold">Close</button>
            </div>
        </div>
    </div>
    
    <div id="agent-editor-modal" class="hidden fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4">
        <div class="bg-white rounded-lg p-6 w-full max-w-md shadow-xl transform transition-all duration-300 scale-95 opacity-0">
            <h2 id="agent-modal-title" class="text-2xl font-bold text-slate-800 mb-6">Create an Ai Tool</h2>
			
            <form id="agent-editor-form">
                <input type="hidden" id="agent-id">
                <div class="space-y-4">
                    <div>
                        <label for="agent-name" class="block text-sm font-medium text-slate-700 mb-1">Agent Name</label>
                        <input autocomplete="off" type="text" id="agent-name" required class="w-full p-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="e.g. Text Summarizer">
                    </div>
                    
                    <div>
                        <label for="agent-title" class="block text-sm font-medium text-slate-700 mb-1">Agent Title</label>
                        <input autocomplete="off" type="text" id="agent-title" required class="w-full p-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="e.g. Creates a summary">
                    </div>

                    <div>
                        <label for="agent-type" class="block text-sm font-medium text-slate-700 mb-1">Conversation Type</label>
                        <select id="agent-type" required class="w-full p-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white">
                            <option value="multi-turn">Conversational</option>
                            <option value="single-turn">Non-conversational</option>
                        </select>
                    </div>
                    
                    <div>
                        <label for="agent-persona" class="block text-sm font-medium text-slate-700 mb-1">Persona / System Instruction</label>
                        <textarea autocomplete="off" id="agent-persona" rows="4" required class="w-full p-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="e.g. You are an expert at summarizing text..."></textarea>
                    </div>
                </div>
                
                <div class="flex justify-between mt-6">
                    <div>
                        <button type="button" id="delete-agent-btn" class="hidden py-2 px-5 bg-red-600 text-white rounded-lg hover:bg-red-700 font-semibold">Delete Agent</button>
                    </div>
                    <div class="flex space-x-3">
                        <button type="button" id="cancel-agent-editor-btn" class="py-2 px-5 bg-slate-200 text-slate-800 rounded-lg hover:bg-slate-300 font-semibold">Cancel</button>
                        <button type="submit" id="save-agent-btn" class="py-2 px-5 bg-indigo-500 text-white rounded-lg hover:bg-indigo-700 font-semibold">Create</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
	
	
    <script type="module">
	
	
	/////////////////////////////////////////////////////////////////////////////////////////////////////////////
	//////// MANUALLY ADD PERMANENT AGENTS HERE ////////
	//////// Notes: 
	//////// 1. Each agent needs to have a unique id.
	//////// 2. Two agents have been commented out.
	/////////////////////////////////////////////////////////////////////////////////////////////////////////////
	
	let agents = [
			
            { id: 'assistant', name: 'Ai Assistant', title: 'A friendly Ai Assistant', persona: 'You are a friendly and helpful assistant. Do not use emojis.', color: '#4f46e5', type: 'multi-turn', isDefault: true},
			
			/*
            { id: 'translator', name: 'Spanish Translator', title: 'Translates Spanish to English', persona: 'You are an expert at translating from English to Chinese. You will be given some text. The format will either be plain text or a parsed pdf document. Your task is to translate that text into Chinese. Only output the translation without any explanations.', color: '#4f46e5', type: 'single-turn', isDefault: true},
			
			{ id: 'doc-chatter', name: 'Doc Chatter', title: 'Chat with your pdf document', persona: 'You are an expert at analyzing documents and answering questions about their content. You will be given a document. Respond in a friendly yet professional tone. The user is a busy professional therefore, keep you answers concise. Always support your answers with references from the document - include page numbers, section titles, text excerpts etc.', color: '#4f46e5', type: 'multi-turn', isDefault: true},
			*/
			
			/* ========= User created Agents are loaded into this list ========= */
        ];
		
	/////////////////////////////////////////////////////////////////////////////////////////////////////////////
	/////////////////////////////////////////////////////////////////////////////////////////////////////////////
	
		
		
        let currentModel = '{{ current_model }}';
        const agentListEl = document.getElementById('agent-list');
        const tabHeaderEl = document.getElementById('tab-header');
        const tabContentEl = document.getElementById('tab-content');
        const initialMessageEl = document.getElementById('initial-message');
        const errorModalEl = document.getElementById('error-modal');
        const errorMessageEl = document.getElementById('error-message');
        const agentSidebar = document.getElementById('agent-sidebar');
        const openSidebarBtn = document.getElementById('open-sidebar-btn');
        const closeSidebarBtn = document.getElementById('close-sidebar-btn');
        const closeErrorModalBtn = document.getElementById('close-error-modal-btn');
        const modelSelector = document.getElementById('model-selector');
        const currentModelDisplay = document.getElementById('current-model-display');
        
        const agentEditorModalEl = document.getElementById('agent-editor-modal');
        const agentEditorModalContent = agentEditorModalEl.querySelector('div');
        const openCreateAgentModalBtn = document.getElementById('open-create-agent-modal-btn');
        const cancelAgentEditorBtn = document.getElementById('cancel-agent-editor-btn');
        const agentEditorForm = document.getElementById('agent-editor-form');
        const deleteAgentBtn = document.getElementById('delete-agent-btn');

        let activeChats = {};
        let currentAgentId = null;
        let isTyping = false;
        let abortControllers = {};
		

        function showError(message) {
            errorMessageEl.textContent = message;
            errorModalEl.classList.remove('hidden');
        }
		
        
        async function changeModel(newModel) {
            try {
                const response = await fetch('/change_model', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ model: newModel })
                });
                const result = await response.json();
                if (response.ok) {
                    currentModel = newModel;
                    currentModelDisplay.textContent = newModel;
                } else {
                    showError(result.error || 'Failed to change model');
                    modelSelector.value = currentModel;
                }
            } catch (error) {
                showError('Network error while changing model');
                modelSelector.value = currentModel;
            }
        }
		
        
        function renderAgents() {
            agentListEl.innerHTML = '';
            agents.forEach(agent => {
                const agentItem = document.createElement('div');
                agentItem.className = `agent-item group flex items-center justify-between p-3 rounded-xl cursor-pointer transition-all duration-200 bg-slate-900/40 hover:bg-slate-700/80`;
                agentItem.innerHTML = `
                    <div class="flex items-center space-x-4 overflow-hidden">
                        <div class="flex-shrink-0 agent-icon" style="background-color: ${agent.color};">
                            <span>${agent.name.charAt(0)}</span>
                        </div>
                        <div class="overflow-hidden">
                            <h3 class="font-bold text-slate-50 text-lg truncate">${agent.name}</h3>
                            <p class="text-indigo-400 text-sm font-semibold truncate">${agent.title}</p>
                        </div>
                    </div>
                    ${!agent.isDefault ? `
                    <button class="edit-agent-btn flex-shrink-0 text-slate-400 hover:text-white p-2 rounded-full">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                          <path d="M17.414 2.586a2 2 0 00-2.828 0L7 10.172V13h2.828l7.586-7.586a2 2 0 000-2.828z" />
                          <path fill-rule="evenodd" d="M2 6a2 2 0 012-2h4a1 1 0 010 2H4v10h10v-4a1 1 0 112 0v4a2 2 0 01-2 2H4a2 2 0 01-2-2V6z" clip-rule="evenodd" />
                        </svg>
                    </button>` : ''}
                `;
                agentItem.onclick = () => {
                    openChatTab(agent);
					
					if (window.innerWidth < 768) agentSidebar.classList.add('-translate-x-full');
					
                };

                if (!agent.isDefault) {
                    agentItem.querySelector('.edit-agent-btn').onclick = (e) => {
                        e.stopPropagation();
                        openEditAgentModal(agent);
                    };
                }

                agentListEl.appendChild(agentItem);
            });
        }
		

        function openChatTab(agent) {
            initialMessageEl.classList.add('hidden');
            tabHeaderEl.classList.remove('hidden');
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('text-indigo-700', 'bg-indigo-100'));
            document.querySelectorAll('.chat-view').forEach(view => view.classList.add('hidden'));
            let chatView = document.getElementById(`chat-view-${agent.id}`);
            let tabBtn = document.getElementById(`tab-btn-${agent.id}`);
            if (!chatView) {
                chatView = createChatView(agent);
                tabContentEl.appendChild(chatView);
                tabBtn = createTabButton(agent);
                tabHeaderEl.appendChild(tabBtn);
                activeChats[agent.id] = { history: [], agent: agent, showFullHistory: false };
            }
            tabBtn.classList.add('text-indigo-700', 'bg-indigo-100');
            chatView.classList.remove('hidden');
            currentAgentId = agent.id;
            renderChatHistory(agent.id);
        }
		

        function closeChatTab(agentId) {
            document.getElementById(`tab-btn-${agentId}`)?.remove();
            document.getElementById(`chat-view-${agentId}`)?.remove();
            delete activeChats[agentId];
            const remainingTabKeys = Object.keys(activeChats);
            if (remainingTabKeys.length > 0) {
                const lastAgentId = remainingTabKeys[remainingTabKeys.length - 1];
                openChatTab(activeChats[lastAgentId].agent);
            } else {
                tabHeaderEl.classList.add('hidden');
                initialMessageEl.classList.remove('hidden');
                currentAgentId = null;
            }
        }
		
        
        function createTabButton(agent) {
            const btn = document.createElement('button');
            btn.id = `tab-btn-${agent.id}`;
            btn.className = `tab-btn flex-shrink-0 flex items-center px-4 py-2 rounded-lg text-sm font-medium mr-2 transition-colors duration-200 hover:bg-indigo-100`;
            btn.innerHTML = `<span>${agent.name}</span><span class="close-tab-btn ml-2 text-xs text-slate-400 hover:text-slate-800 p-1" data-agent-id="${agent.id}">&times;</span>`;
            btn.onclick = (e) => {
                if (!e.target.classList.contains('close-tab-btn')) {
                    openChatTab(agent);
                }
            };
            return btn;
        }

		
		
		function createChatView(agent) {
		    const chatView = document.createElement('div');
		    chatView.id = `chat-view-${agent.id}`;
		    chatView.className = `chat-view flex flex-col flex-1 hidden overflow-hidden`;
		    chatView.innerHTML = `
		        <div id="history-toggle-container-${agent.id}" class="mb-2 hidden flex-shrink-0 bg-white border-b border-slate-200 text-center">
		            <button id="history-toggle-btn-${agent.id}" class="mx-auto bg-white text-slate-700 rounded-lg transition-colors text-sm font-medium">
		                Show Conversation
		            </button>
		        </div>
		        <div class="flex-1 overflow-y-auto p-4" id="chat-messages-container-${agent.id}">
		            <div id="chat-messages-${agent.id}" class="space-y-6"></div>
		        </div>
		        <div class="p-4 pt-0">
		            <div id="loading-indicator-${agent.id}" class="hidden flex items-center space-x-2 text-sm text-slate-500 mb-2">
		                 <div class="typing-dot w-2 h-2 bg-slate-400 rounded-full"></div>
		                 <div class="typing-dot w-2 h-2 bg-slate-400 rounded-full"></div>
		                 <div class="typing-dot w-2 h-2 bg-slate-400 rounded-full"></div>
		                 <span>${agent.name} is processing...</span>
		            </div>
		            <form class="chat-form flex flex-col" data-agent-id="${agent.id}">
		                <div id="image-preview-container-${agent.id}" class="mb-2 hidden flex flex-wrap gap-2"></div>
		                <div class="flex space-x-3">
		                    <input type="file" id="file-input-${agent.id}" class="hidden file-input" accept="image/*,.pdf" multiple>
                            <div class="relative group">
                                <button type="button" class="attach-file-btn flex-shrink-0 w-12 h-12 flex items-center justify-center bg-slate-200 text-slate-600 rounded-xl hover:bg-slate-300 transition-colors">
                                    <span style="font-size: 1.5rem;">+</span>
                                </button>
                                <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1 bg-slate-800 text-white text-xs rounded-md whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
                                    jpg, png, pdf
                                </div>
                            </div>
		                    <textarea autocomplete="off" placeholder="Type your message... (Shift+Enter for new line)" rows="1" class="chat-input flex-1 p-3 border border-slate-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"></textarea>
		                    <div class="flex space-x-2">
		                        <button type="submit" class="submit-btn flex-shrink-0 w-12 h-12 flex items-center justify-center bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 transition-colors disabled:bg-indigo-300">
		                            <span>➤</span>
		                        </button>
		                        <button type="button" class="stop-btn hidden flex-shrink-0 w-12 h-12 flex items-center justify-center bg-indigo-700 text-white rounded-xl hover:bg-indigo-600 transition-colors">
		                            <span>⬜</span>
		                        </button>
		                    </div>
		                </div>
		            </form>
		        </div>`;
		    
		    const attachBtn = chatView.querySelector('.attach-file-btn');
		    const fileInput = chatView.querySelector('.file-input');
		    const textInput = chatView.querySelector('.chat-input');
		    const form = chatView.querySelector('.chat-form');
		    const historyToggleBtn = chatView.querySelector(`#history-toggle-btn-${agent.id}`);
		    
		    // Add toggle button click handler
		    historyToggleBtn.onclick = () => {
		        activeChats[agent.id].showFullHistory = !activeChats[agent.id].showFullHistory;
		        renderChatHistory(agent.id);
		    };
		    
		    textInput.addEventListener('keydown', (e) => {
		        if (e.key === 'Enter' && !e.shiftKey) {
		            e.preventDefault();
		            form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
		        }
		    });
		    textInput.addEventListener('input', () => {
		        textInput.style.height = 'auto';
		        textInput.style.height = `${Math.min(textInput.scrollHeight, 200)}px`;
		    });
		    attachBtn.onclick = () => fileInput.click();
		    
		    fileInput.addEventListener('change', async (event) => {
		        const previewContainer = chatView.querySelector(`#image-preview-container-${agent.id}`);
		        const files = event.target.files;
		        if (!files) return;
		        
		        const filePromises = Array.from(files).map(file => {
		            return new Promise(async (resolve, reject) => {
		                if (file.type === 'application/pdf') {
		                    const formData = new FormData();
		                    formData.append('pdf_file', file);
		                    try {
		                        const response = await fetch('/upload_pdf', {
		                            method: 'POST',
		                            body: formData
		                        });
		                        const result = await response.json();
		                        if (response.ok) {
		                            resolve(result.images);
		                        } else {
		                            reject(new Error(result.error || 'Failed to convert PDF to images.'));
		                        }
		                    } catch (error) {
		                        reject(error);
		                    }
		                } else {
		                    const reader = new FileReader();
		                    reader.onload = () => resolve(reader.result);
		                    reader.onerror = reject;
		                    reader.readAsDataURL(file);
		                }
		            });
		        });
		
		        Promise.all(filePromises)
		        .then(results => {
		            const newStrings = results.flat();
		            const existingStrings = JSON.parse(chatView.dataset.imageBase64Array || '[]');
		            chatView.dataset.imageBase64Array = JSON.stringify(existingStrings.concat(newStrings));
		            updatePreviews();
		            fileInput.value = '';
		        })
		        .catch(error => {
		            showError(error.message);
		        });
		        
		        function updatePreviews() {
		            previewContainer.innerHTML = '';
		            const currentStrings = JSON.parse(chatView.dataset.imageBase64Array || '[]');
		            previewContainer.classList.toggle('hidden', currentStrings.length === 0);
		            currentStrings.forEach((base64String, index) => {
		                const wrapper = document.createElement('div');
		                wrapper.className = 'relative';
		                wrapper.innerHTML = `
		                    <img src="${base64String}" class="h-24 w-24 rounded-lg object-cover border-2 border-slate-300">
		                    <button type="button" class="absolute -top-2 -right-2 bg-red-500 text-white rounded-full h-6 w-6 flex items-center justify-center text-xs font-bold shadow-md hover:bg-red-600">&times;</button>`;
		                wrapper.querySelector('button').onclick = () => {
		                    const current = JSON.parse(chatView.dataset.imageBase64Array || '[]');
		                    current.splice(index, 1);
		                    chatView.dataset.imageBase64Array = JSON.stringify(current);
		                    updatePreviews();
		                };
		                previewContainer.appendChild(wrapper);
		            });
		        }
		    });
		    form.addEventListener('submit', handleFormSubmit);
		    return chatView;
		}
        
		
		
		function renderChatHistory(agentId) {
		    const messagesEl = document.getElementById(`chat-messages-${agentId}`);
		    const historyToggleContainer = document.getElementById(`history-toggle-container-${agentId}`);
		    const historyToggleBtn = document.getElementById(`history-toggle-btn-${agentId}`);
		    
		    if (!messagesEl) return;
		    messagesEl.innerHTML = '';
		    const chat = activeChats[agentId];
            if (!chat) return; // Agent might have been deleted
            const { history, agent, showFullHistory } = chat;
		    
		    if (history.length === 0) {
		         messagesEl.innerHTML = `<div class="text-center py-8">
		            <div class="agent-icon mx-auto mb-4 border-4 border-white shadow-lg" style="background-color: ${agent.color};">
		                <span>${agent.name.charAt(0)}</span>
		            </div>
		            <h2 class="text-2xl font-bold">${agent.name}</h2>
		            <p class="text-slate-500 mt-1">${agent.persona}</p>
		        </div>`;
		        // Hide toggle button when no messages
		        historyToggleContainer.classList.add('hidden');
		    } else {
		        // Show/hide toggle button based on message count
		        if (history.length > 2) {
		            historyToggleContainer.classList.remove('hidden');
		            historyToggleBtn.textContent = showFullHistory ? 'Show Recent Only' : `Show Conversation (${history.length} messages)`;
		        } else {
		            historyToggleContainer.classList.add('hidden');
		        }
		
		        // Determine which messages to show
		        let messagesToShow;
		        if (showFullHistory) {
		            messagesToShow = history;
		        } else {
		            // Show only the last user message and last assistant response
		            // Find the last user message and the assistant response that follows it
		            const lastUserIndex = history.map(msg => msg.role).lastIndexOf('user');
		            if (lastUserIndex !== -1) {
		                // If there's an assistant response after the last user message, show both
		                // Otherwise, just show the user message
		                const nextIndex = lastUserIndex + 1;
		                if (nextIndex < history.length && history[nextIndex].role === 'assistant') {
		                    messagesToShow = history.slice(lastUserIndex, nextIndex + 1);
		                } else {
		                    messagesToShow = history.slice(lastUserIndex);
		                }
		            } else {
		                // Fallback: show last 2 messages
		                messagesToShow = history.slice(-2);
		            }
		        }
		        
		        messagesToShow.forEach(msg => renderMessage(agentId, msg));
		        
		        // Handle scrolling based on the view mode
		        if (showFullHistory) {
		            scrollToBottom(agentId);
		        } else {
		            // When showing recent only, scroll to the user's message (first message in the recent view)
		            setTimeout(() => {
		                const chatContainer = document.getElementById(`chat-messages-container-${agentId}`);
		                const firstMessage = messagesEl.querySelector('.flex');
		                if (chatContainer && firstMessage) {
		                    firstMessage.scrollIntoView({ behavior: 'smooth', block: 'start' });
		                }
		            }, 50); // Small delay to ensure DOM is updated
		        }
		    }
		}
		
		        
		function renderMessage(agentId, msg) {
		    const messagesListEl = document.getElementById(`chat-messages-${agentId}`);
		    if (!messagesListEl) return;
		    
		    const isUser = msg.role === 'user';
		    const part = msg.parts?.[0] || {};
		    const rawText = part.text || '';
		    const imageSources = part.images || [];
		    const thinkingContent = part.thinking || ''; // Get stored thinking content
		    
		    const msgEl = document.createElement('div');
		    msgEl.className = `flex items-start gap-3 ${isUser ? 'justify-end' : ''}`;
		    
		    const contentContainer = document.createElement('div');
		    contentContainer.className = isUser ? 'flex flex-col items-end' : '';
		
		    if (isUser && imageSources.length > 0) {
		        const imageContainer = document.createElement('div');
		        imageContainer.className = 'flex flex-wrap gap-2 mb-2 justify-end';
		        imageSources.forEach(src => {
		            const img = document.createElement('img');
		            img.src = src;
		            img.className = 'h-24 w-24 rounded-lg object-cover border-2 border-slate-200 shadow-sm';
		            imageContainer.appendChild(img);
		        });
		        contentContainer.appendChild(imageContainer);
		    }
		
		    /////////////////////////////////////////////
		    ////// User and Response chat bubbles //////
		    ////////////////////////////////////////////
		    
		    if (rawText.trim().length > 0 || !isUser) {
		        // Add thinking bubble if this is an assistant message with thinking content
		        if (!isUser && thinkingContent) {
		            const thinkingEl = document.createElement("div");
		            thinkingEl.className = "thinking-bubble bg-slate-200 text-slate-600 italic rounded-xl p-2 mb-2 cursor-pointer";
		            thinkingEl.textContent = "View reasoning";
		            
		            const hiddenPanel = document.createElement("div");
		            hiddenPanel.className = "hidden hidden-reasoning mt-2 text-xs bg-slate-100 p-2 rounded";
		            hiddenPanel.textContent = thinkingContent;
		            thinkingEl.appendChild(hiddenPanel);
		            
		            thinkingEl.onclick = () => hiddenPanel.classList.toggle("hidden");
		            contentContainer.appendChild(thinkingEl);
		        }
		
		        const bubbleEl = document.createElement('div');
		        const bubbleClasses = isUser 
		            ? 'text-[17px] bg-slate-200 text-slate-700 rounded-br-none shadow-sm mb-2' 
		            : 'text-[17px] text-slate-700 rounded-bl-none border-slate-200';
		        bubbleEl.className = `message-bubble max-w-lg md:max-w-xl lg:max-w-3xl rounded-2xl p-4 ${bubbleClasses}`;
		        
		        if (isUser) {
		            const contentWrapper = document.createElement('div');
		            const textDiv = document.createElement('div');
		            textDiv.className = 'message-content';
		            textDiv.style.whiteSpace = 'pre-wrap';
		            textDiv.style.wordWrap = 'break-word';
		            textDiv.textContent = rawText;
		            
		            // === THIS IS THE RESTORED LOGIC ===
		            textDiv.style.maxHeight = '200px';
		            textDiv.style.overflowY = 'auto';
		            textDiv.style.scrollbarWidth = 'thin';
		            textDiv.style.paddingRight = '8px';
		            contentWrapper.appendChild(textDiv);
		
		            const MAX_LENGTH = 400; // Character limit to show the hint
		            if (rawText.length > MAX_LENGTH) {
		                const scrollHint = document.createElement('div');
		                scrollHint.className = 'text-xs italic text-slate-500 mt-1 text-center';
		                scrollHint.textContent = '↑ scroll ↓';
		                contentWrapper.appendChild(scrollHint);
		            }
		            bubbleEl.appendChild(contentWrapper);
		
		        } else {
		            const markdownDiv = document.createElement('div');
		            markdownDiv.className = 'markdown-content';
		            markdownDiv.innerHTML = marked.parse(rawText);
		            enhanceCodeBlocks(markdownDiv);
		            bubbleEl.appendChild(markdownDiv);
		        }
		        contentContainer.appendChild(bubbleEl);
		    }
		    
		    msgEl.appendChild(contentContainer);
		    messagesListEl.appendChild(msgEl);
		    return msgEl;
		}
				
		

        function enhanceCodeBlocks(element) {
            element.querySelectorAll('pre > code').forEach(codeBlock => {
                const preElement = codeBlock.parentElement;
                if (preElement.parentElement.classList.contains('code-block-wrapper')) return;
                const wrapper = document.createElement('div');
                wrapper.className = 'code-block-wrapper';
                const language = Array.from(codeBlock.classList).find(c => c.startsWith('language-'))?.replace('language-', '') || 'code';
                
                wrapper.innerHTML = `
                    <div class="code-block-header">
                        <span class="font-sans">${language}</span>
                        <button class="copy-btn">Copy</button>
                    </div>`;
                
                preElement.parentNode.insertBefore(wrapper, preElement);
                wrapper.appendChild(preElement);
                
                wrapper.querySelector('.copy-btn').addEventListener('click', () => {
                   navigator.clipboard.writeText(codeBlock.textContent).then(() => {
                       const button = wrapper.querySelector('.copy-btn');
                       button.textContent = 'Copied!';
                       setTimeout(() => { button.textContent = 'Copy'; }, 2000);
                   });
                });
                hljs.highlightElement(codeBlock);
            });
        }
		
		
        function scrollToBottom(agentId) {
            const container = document.getElementById(`chat-messages-container-${agentId}`);
            if (container) container.scrollTop = container.scrollHeight;
        }
		
		
        
        async function streamLlmResponse(chatHistory, systemInstruction, agentId, signal) {
    const messages = [];
    if (systemInstruction) messages.push({ role: "system", content: systemInstruction });
    
    chatHistory.forEach(msg => {
        const contentParts = [];
        const part = msg.parts[0];
        if (part.text) contentParts.push({ type: "text", text: part.text });
        if (part.images) part.images.forEach(imgBase64 => contentParts.push({ type: "image_url", image_url: { url: imgBase64 } }));
        messages.push({ role: msg.role, content: contentParts });
    });

    const agentMessage = { role: "assistant", parts: [{ text: "", thinking: "" }] }; // Add thinking field
    activeChats[agentId].history.push(agentMessage);
    const messageEl = renderMessage(agentId, agentMessage);
    const contentDiv = messageEl.querySelector('.markdown-content');
    const chatContainer = document.getElementById(`chat-messages-container-${agentId}`);

    if (!contentDiv) return;

    try {
        const res = await fetch("/stream_chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ messages, model: currentModel }),
            signal: signal
        });
        if (!res.ok) throw new Error((await res.json()).reply || `Server error: ${res.status}`);
        
        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        let inThinking = false;
        let thinkingBuffer = "";
        let finalBuffer = "";
        let thinkingEl = null;

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n\n');
            buffer = lines.pop();

            for (const line of lines) {
                const isScrolledToBottom = chatContainer 
                    ? chatContainer.scrollHeight - chatContainer.clientHeight <= chatContainer.scrollTop + 50
                    : true;

                if (!line.startsWith('data: ')) continue;
                const jsonData = JSON.parse(line.substring(6));

                // --- THIS IS THE NEW PART ---
                // If the server sends a warning payload, show the modal.
                if (jsonData.warning) {
                    showError(jsonData.warning);
                }
                // --- END OF NEW PART ---

                if (jsonData.error) {
                    finalBuffer += `\n\n**Error:** ${jsonData.error}`;
                } else if (jsonData.chunk) {
                    const chunk = jsonData.chunk;

                    if (chunk.includes("<think>")) {
                        inThinking = true;
                        thinkingBuffer = "";
                        if (!thinkingEl) {
                            thinkingEl = document.createElement("div");
                            thinkingEl.className = "thinking-bubble bg-slate-200 text-slate-600 italic rounded-xl p-2 mb-2 cursor-pointer";
                            thinkingEl.textContent = "Thinking...";
                            thinkingEl.onclick = () => {
                                const hidden = thinkingEl.querySelector(".hidden-reasoning");
                                if (hidden) hidden.classList.toggle("hidden");
                            };
                            const hiddenPanel = document.createElement("div");
                            hiddenPanel.className = "hidden-reasoning mt-2 text-xs bg-slate-100 p-2 rounded";
                            hiddenPanel.textContent = "";
                            thinkingEl.appendChild(hiddenPanel);
                            contentDiv.parentNode.insertBefore(thinkingEl, contentDiv);
                        }
                    }

                    if (inThinking) {
                        scrollToBottom(agentId);
                        thinkingBuffer += chunk;
                        const hiddenPanel = thinkingEl.querySelector(".hidden-reasoning");
                        if (hiddenPanel) {
                            hiddenPanel.textContent = thinkingBuffer.replace("<think>", "").replace("</think>", "").trim();
                        }
                    }

                    if (chunk.includes("</think>")) {
                        inThinking = false;
                        if (thinkingEl) {
                            thinkingEl.textContent = "View reasoning";
                            const hiddenPanel = document.createElement("div");
                            hiddenPanel.className = "hidden hidden-reasoning mt-2 text-xs bg-slate-100 p-2 rounded";
                            hiddenPanel.textContent = thinkingBuffer.replace("<think>", "").replace("</think>", "").trim();
                            thinkingEl.appendChild(hiddenPanel);
                            thinkingEl.onclick = () => hiddenPanel.classList.toggle("hidden");
                        }
                        agentMessage.parts[0].thinking = thinkingBuffer.replace("<think>", "").replace("</think>", "").trim();
                    }

                    if (!inThinking) {
                        finalBuffer += chunk.replace(/<think>[\s\S]*?<\/think>/g, "");
                    }
                }

                agentMessage.parts[0].text = finalBuffer.trim();
                contentDiv.innerHTML = marked.parse(agentMessage.parts[0].text);
                enhanceCodeBlocks(contentDiv);

                if (isScrolledToBottom) {
                    scrollToBottom(agentId);
                }
            }
        }
    } catch (err) {
        if (err.name !== 'AbortError') {
            agentMessage.parts[0].text += `\n\n**Error:** ${err.message}`;
        } else {
            agentMessage.parts[0].text += `\n\n*Stream stopped by user.*`;
        }
        contentDiv.innerHTML = marked.parse(agentMessage.parts[0].text);
    }
}

        
        async function handleFormSubmit(e) {
		    e.preventDefault();
		    const form = e.target;
		    const agentId = form.dataset.agentId;
		    const textInput = form.querySelector(".chat-input");
		    const submitBtn = form.querySelector(".submit-btn");
		    const stopBtn = form.querySelector(".stop-btn");
		    const chatView = document.getElementById(`chat-view-${agentId}`);
		    
		    const messageText = textInput.value.trim();
		    const imageBase64Array = JSON.parse(chatView.dataset.imageBase64Array || '[]');
		
		    if ((messageText === "" && imageBase64Array.length === 0) || !agentId || isTyping) return;
		    
		    const chat = activeChats[agentId];
		    textInput.value = "";
		    textInput.style.height = 'auto';
		    chatView.dataset.imageBase64Array = '[]';
		    document.getElementById(`image-preview-container-${agentId}`).innerHTML = '';
		    document.getElementById(`image-preview-container-${agentId}`).classList.add('hidden');
		    
		    if (chat.history.length === 0) document.getElementById(`chat-messages-${agentId}`).innerHTML = "";
		    
		    const userMessage = { role: "user", parts: [{ text: messageText }] };
		    if (imageBase64Array.length > 0) userMessage.parts[0].images = imageBase64Array;
		    chat.history.push(userMessage);
		
		    // If agent is 'single-turn', clear history except for the current message
		    if (chat.agent.type === 'single-turn') {
		        chat.history = chat.history.slice(-1);
		    }
		
		    // ✅ Always reset to "Show Recent Only" before rendering
		    chat.showFullHistory = false;
		
		    // After adding the user message, re-render to show only recent messages
		    renderChatHistory(agentId);
		
		    isTyping = true;
		    submitBtn.disabled = true;
		    submitBtn.classList.add('hidden');
		    stopBtn.classList.remove('hidden');
		    document.getElementById(`loading-indicator-${agentId}`).classList.remove("hidden");
		    
		    // Disable history toggle button during streaming
		    const historyToggleBtn = document.getElementById(`history-toggle-btn-${agentId}`);
		    if (historyToggleBtn) {
		        historyToggleBtn.disabled = true;
		        historyToggleBtn.classList.add('opacity-50', 'cursor-not-allowed');
		    }
		    
		    const controller = new AbortController();
		    abortControllers[agentId] = controller;
		    stopBtn.onclick = () => controller.abort();
		    
		    try {
		        await streamLlmResponse(chat.history, chat.agent.persona, agentId, controller.signal);
		    } catch (error) {
		        if (error.name !== 'AbortError') showError("The agent had a problem streaming the response.");
		    } finally {
		        isTyping = false;
		        submitBtn.disabled = false;
		        submitBtn.classList.remove('hidden');
		        stopBtn.classList.add('hidden');
		        document.getElementById(`loading-indicator-${agentId}`).classList.add("hidden");
		        
		        // Re-enable history toggle button
		        const historyToggleBtn = document.getElementById(`history-toggle-btn-${agentId}`);
		        if (historyToggleBtn) {
		            historyToggleBtn.disabled = false;
		            historyToggleBtn.classList.remove('opacity-50', 'cursor-not-allowed');
		        }
		        
		        delete abortControllers[agentId];
		        // Prevent automatic scroll to bottom by removing this line.
		        // This respects the user's current scroll position.
		        //scrollToBottom(agentId);
		    }
		}

				
		
		function openAgentEditorModal() {
            agentEditorModalEl.classList.remove('hidden');
            setTimeout(() => agentEditorModalContent.classList.remove('scale-95', 'opacity-0'), 10);
        }
		
        function closeAgentEditorModal() {
             agentEditorModalContent.classList.add('scale-95', 'opacity-0');
             setTimeout(() => agentEditorModalEl.classList.add('hidden'), 300);
        }
		
		function openCreateAgentModal() {
            agentEditorForm.reset();
            document.getElementById('agent-id').value = '';
            document.getElementById('agent-modal-title').innerHTML = `Create an Ai Tool`;
            document.getElementById('save-agent-btn').textContent = 'Create';
            deleteAgentBtn.classList.add('hidden');
            openAgentEditorModal();
        }

        function openEditAgentModal(agent) {
            agentEditorForm.reset();
            document.getElementById('agent-id').value = agent.id;
            document.getElementById('agent-name').value = agent.name;
            document.getElementById('agent-title').value = agent.title;
            document.getElementById('agent-persona').value = agent.persona;
            document.getElementById('agent-type').value = agent.type;
            document.getElementById('agent-modal-title').innerHTML = `Edit Ai Tool`;
            document.getElementById('save-agent-btn').textContent = 'Save Changes';
            deleteAgentBtn.classList.remove('hidden');
            openAgentEditorModal();
        }

        async function handleSaveAgent(e) {
            e.preventDefault();
            const agentId = document.getElementById('agent-id').value;
            const name = document.getElementById('agent-name').value.trim();
            const title = document.getElementById('agent-title').value.trim();
            const persona = document.getElementById('agent-persona').value.trim();
            const type = document.getElementById('agent-type').value;

            if (!name || !title || !persona) return showError("Please fill out all fields.");

            const agentData = {
                name,
                title,
                persona,
                type,
                color: '#4f46e5' // Default color for user agents
            };

            let url = "/agents";
            let method = "POST";

            if (agentId) {
                url = `/agents/${agentId}`;
                method = "PUT";
                agentData.id = agentId;
            } else {
                agentData.id = name.toLowerCase().replace(/\s+/g, '-') + '-' + Date.now();
            }

            try {
                const res = await fetch(url, {
                    method: method,
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(agentData)
                });
                if (!res.ok) {
                    const errorData = await res.json();
                    throw new Error(errorData.error || `Failed to ${agentId ? 'update' : 'create'} agent`);
                }

                if (agentId) {
                    // Find and update in local agents array
                    const index = agents.findIndex(a => a.id === agentId);
                    if (index !== -1) agents[index] = { ...agents[index], ...agentData };
                } else {
                    // Add new agent to the top
                    agents.splice(agents.findIndex(a => !a.isDefault), 0, agentData);
                }
                
                renderAgents();
                closeAgentEditorModal();

            } catch (err) {
                showError(err.message);
            }
        }
        
        async function handleDeleteAgent() {
            const agentId = document.getElementById('agent-id').value;
            if (!agentId) return;

            try {
                const res = await fetch(`/agents/${agentId}`, { method: "DELETE" });
                if (!res.ok) throw new Error("Failed to delete agent");
                
                agents = agents.filter(a => a.id !== agentId);
                closeChatTab(agentId); // Close the tab if it's open
                renderAgents();
                closeAgentEditorModal();
            } catch (err) {
                showError(err.message);
            }
        }

		
        function setupEventListeners() {
            closeErrorModalBtn.onclick = () => errorModalEl.classList.add('hidden');
            openSidebarBtn.onclick = () => agentSidebar.classList.remove('-translate-x-full');
            closeSidebarBtn.onclick = () => agentSidebar.classList.add('-translate-x-full');
            openCreateAgentModalBtn.addEventListener('click', openCreateAgentModal);
            cancelAgentEditorBtn.addEventListener('click', closeAgentEditorModal);
            agentEditorForm.addEventListener('submit', handleSaveAgent);
            deleteAgentBtn.addEventListener('click', handleDeleteAgent);
            modelSelector.addEventListener('change', (e) => changeModel(e.target.value));
            tabHeaderEl.addEventListener('click', e => {
                if (e.target.classList.contains('close-tab-btn')) {
                    e.stopPropagation();
                    closeChatTab(e.target.dataset.agentId);
                }
            });
        }
		
		
		async function loadUserAgents() {
			try {
				const res = await fetch("/agents");
				if (!res.ok) throw new Error("Failed to load saved agents");
				const savedAgents = await res.json();
				
				// Separate default and user agents to preserve order
				const defaultAgents = agents.filter(a => a.isDefault);
				agents = [...defaultAgents, ...savedAgents];
				renderAgents();
			} catch (err) {
				console.error("Error loading agents:", err);
				renderAgents(); // fallback to just defaults
			}
		}

		document.addEventListener('DOMContentLoaded', () => {
			loadUserAgents();
			setupEventListeners();
		});

		
    </script>
	
</body>
</html>
"""

"""
What app settings are stored locally
-------------------------------------

1- The names, titles and system messages/personas of custom Ai tools that the user creates are stored in a file called agents.json. This ensures that each time the app is loaded the user created tools are available. Without this feature any user defined tool would disappear each time the browser tab is closed. The user has the ability to manually delete any tool they have created.

    *** Note: It is recommended that the user not store sensitive information in the agent/tool system messages.

2- The name of the last model that was used is stored in a file called last_model.txt. This ensures that every time the app is loaded the user's favourite model is selected in the dropdown menu. This ensures a smoother user experience.

These files are stored locally in the same folder as as this app.py file.

"""


# Helper functions and routes to create new agents
# -------------------------------------------------

def load_user_agents():
    if not os.path.exists(AGENTS_FILE):
        return []
    try:
        with open(AGENTS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_user_agents(user_agents):
    with open(AGENTS_FILE, "w") as f:
        json.dump(user_agents, f, indent=2)
		
		
@app.route("/agents", methods=["GET"])
def get_agents():
    return jsonify(load_user_agents())
	

@app.route("/agents", methods=["POST"])
def create_agent():
    user_agents = load_user_agents()
    new_agent = request.json
    # Basic validation
    if not all(k in new_agent for k in ['id', 'name', 'title', 'persona', 'type']):
        return jsonify({"error": "Missing agent data"}), 400
    user_agents.append(new_agent)
    save_user_agents(user_agents)
    return jsonify(new_agent), 201

@app.route("/agents/<agent_id>", methods=["PUT"])
def update_agent(agent_id):
    user_agents = load_user_agents()
    agent_found = False
    for i, agent in enumerate(user_agents):
        if agent["id"] == agent_id:
            # Prevent changing id and isDefault status
            updated_data = request.json
            updated_data.pop('id', None)
            updated_data.pop('isDefault', None)
            user_agents[i].update(updated_data)
            agent_found = True
            break
    if agent_found:
        save_user_agents(user_agents)
        return jsonify(user_agents[i])
    return jsonify({"error": "Agent not found"}), 404


@app.route("/agents/<agent_id>", methods=["DELETE"])
def delete_agent(agent_id):
    user_agents = load_user_agents()
    initial_len = len(user_agents)
    user_agents = [a for a in user_agents if a["id"] != agent_id]
    if len(user_agents) < initial_len:
        save_user_agents(user_agents)
        return jsonify({"status": "deleted"})
    return jsonify({"error": "Agent not found"}), 404




	
@app.route("/")
def index():
    """Serves the main HTML page with headers to prevent browser storage/caching."""
    
    # 1. Render the HTML template
    html_content = render_template_string(HTML_TEMPLATE, model_list=model_list, current_model=MODEL_NAME)
    
    # 2. Create an explicit Response object
    response = Response(html_content)
    
    # 3. Add headers to prevent caching and history storage
    # 'no-store': The most critical directive; prevents storage in any cache (private or shared).
    # 'no-cache': Forces the browser to re-validate with the server before using a cached copy (even though no-store is set, this is for redundancy).
    # 'must-revalidate, max-age=0, private': Additional redundant directives for maximum compatibility.
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0, private"
    response.headers["Pragma"] = "no-cache" # Legacy HTTP/1.0 directive
    response.headers["Expires"] = "0"       # Legacy directive
	
    # 4. Add minimal security headers for localhost application
    # X-Content-Type-Options: Prevents browsers from MIME-sniffing responses away from declared content-type
    # This stops browsers from interpreting files as a different type than declared (e.g. treating text as executable)
    response.headers["X-Content-Type-Options"] = "nosniff"
    
    # X-Frame-Options: Prevents this page from being embedded in frames/iframes
    # This protects against clickjacking attacks where malicious sites embed your app invisibly
    # While less critical for localhost-only apps, it's a zero-cost security improvement
    response.headers["X-Frame-Options"] = "DENY"

    return response # Return the Response object
	


		
@app.route("/change_model", methods=["POST"])
def change_model():
    """Changes the active LLM model."""
    global MODEL_NAME
    data = request.json
    new_model = data.get("model")
    if new_model in model_list:
        MODEL_NAME = new_model
        save_last_model(new_model)  # <-- ADD THIS LINE to save the choice
        print(f"[INFO] Model changed to: {MODEL_NAME}")
        return jsonify({"status": "success", "current_model": MODEL_NAME})
    else:
        return jsonify({"error": f"Model '{new_model}' not found in the available list."}), 400
		
		

@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    """
    Receives a PDF file, converts each page to a JPEG image with optimizations,
    and returns the images as a list of base64-encoded strings.
    Can set the page limit.
    """
    if 'pdf_file' not in request.files:
        return jsonify({"error": "No PDF file part in the request"}), 400
    
    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if pdf_file and pdf_file.filename.endswith('.pdf'):
        try:
            pdf_bytes = pdf_file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            
            # Check page limit for medical documents
            #MAX_PAGES = 15
            page_count = len(doc)
            print(f"[DEBUG] PDF '{pdf_file.filename}' has {page_count} pages. Max allowed: {MAX_PAGES}")
            
            if page_count > MAX_PAGES:
                doc.close()
                error_msg = f"PDF has {page_count} pages. Maximum allowed is {MAX_PAGES} pages for optimal processing."
                print(f"[INFO] Rejecting PDF: {error_msg}")
                return jsonify({"error": error_msg}), 400
            
            images = []
            for i, page in enumerate(doc):
                print(f"[DEBUG] Processing page {i+1}/{page_count}")
                # Image Quality Control: Use moderate DPI for balance of quality/size
                # 1.5x scale provides good readability while reducing file size
                matrix = fitz.Matrix(PDF_IMAGE_RES, PDF_IMAGE_RES)  # ~150 DPI instead of default 200+ DPI
                pix = page.get_pixmap(matrix=matrix)
                
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                
                # Compression Settings: Optimize for medical documents
                byte_io = io.BytesIO()
                img.save(byte_io, 'JPEG', quality=90, optimize=True)  # High quality but compressed
                
                base64_encoded = base64.b64encode(byte_io.getvalue()).decode('utf-8')
                images.append(f"data:image/jpeg;base64,{base64_encoded}")
                
                # Memory cleanup after each page
                pix = None
                img.close()
                byte_io.close()
            
            doc.close()
            
            # Log processing info
            print(f"[INFO] Successfully processed {len(images)} pages from PDF: {pdf_file.filename}")
            
            return jsonify({"images": images}), 200
            
        except Exception as e:
            print(f"[ERROR] PDF conversion error: {e}", file=sys.stderr)
            return jsonify({"error": f"Failed to process PDF: {str(e)}"}), 500

    return jsonify({"error": "Invalid file type. Please upload a PDF file."}), 400
	

	
@app.route("/stream_chat", methods=["POST"])
def stream_chat():
    """
    Handles the chat request and streams the response back to the client.
    Handles multimodal requests with images, ensuring images are
    processed before text.
    """
    data = request.json
    client_messages = data.get("messages", [])
    model_to_use = data.get("model", MODEL_NAME)
    print(f"\n[INFO] Received request for /stream_chat with model '{model_to_use}'.")

    ollama_messages = []
    for msg in client_messages:
        role = msg.get('role')
        content = msg.get('content')
        
        if isinstance(content, list):
            # To explicitly ensure images are processed before text, we use two separate loops.
            image_parts = []
            text_parts = []
            
            # Pass 1: Gather all image parts
            for part in content:
                if part.get('type') == 'image_url':
                    base64_data = part.get('image_url', {}).get('url', '')
                    if ',' in base64_data:
                        image_parts.append(base64_data.split(',', 1)[1])

            # Pass 2: Gather all text parts
            for part in content:
                if part.get('type') == 'text':
                    text_parts.append(part.get('text', ''))

            # Construct the message payload. The 'images' field is conceptually
            # presented before the 'content' field in the final structure.
            ollama_msg = {'role': role, 'content': " ".join(text_parts)}
            if image_parts: 
                ollama_msg['images'] = image_parts
            
            ollama_messages.append(ollama_msg)
        
        elif isinstance(content, str):
            ollama_messages.append({'role': role, 'content': content})

    def generate_chunks():
        try:
			
            stream = ollama_chat(
				model=model_to_use, 
				messages=ollama_messages, 
				stream=True, 
				options={
					"num_ctx": NUM_CTX,				
					"temperature": TEMPERATURE, 
					"top_k": TOP_K, 
					"top_p": TOP_P, 
					"frequency_penalty": FREQUENCY_PENALTY, 
					"repeat_penalty": REPEAT_PENALTY,
					}
				)
			
            print("[INFO] Started streaming response from Ollama.")
            for chunk in stream:
                # If the chunk contains message content, yield it to the client
                if 'content' in chunk.get('message', {}):
                    sse_data = json.dumps({'chunk': chunk['message']['content']})
                    yield f"data: {sse_data}\n\n"
                
                # When the stream is finished, the 'done' flag is True.
                # The final chunk contains performance and token stats.
                if chunk.get('done'):
                    prompt_tokens = chunk.get('prompt_eval_count', 0)
                    completion_tokens = chunk.get('eval_count', 0)
                    total_tokens = prompt_tokens + completion_tokens
                    
                    print("[INFO] Finished streaming response.")
                    print(f"   [STATS] Prompt Tokens:     {prompt_tokens}")
                    print(f"   [STATS] Completion Tokens: {completion_tokens}")
                    print(f"   [STATS] Total Tokens:      {total_tokens}")

                    # --- UPDATED: CONTEXT WINDOW WARNING (POST-STREAM) ---
                    # Check if total tokens are within 10% of the NUM_CTX limit.
                    if total_tokens >= (NUM_CTX * 0.9):
                        warning_msg = f"Chat history is now {total_tokens} tokens. The maximum is {NUM_CTX}. The AI will lose track of the conversation. Please start a new chat."
                        
                        # 1. Print warning to the Zsh console
                        print(f"[WARNING] {warning_msg}")
                        
                        # 2. Send a warning payload to the client to trigger the modal
                        warning_payload = json.dumps({'warning': warning_msg})
                        yield f"data: {warning_payload}\n\n"

        except Exception as e:
            print(f"[ERROR] An error occurred during streaming: {e}", file=sys.stderr)
            error_message = json.dumps({'error': f"Ollama API Error: {str(e)}"})
            yield f"data: {error_message}\n\n"

    return Response(generate_chunks(), mimetype='text/event-stream')




if __name__ == "__main__":
	
	# Auto launch in the browser
    import webbrowser, threading
    import os

    def open_browser():
        webbrowser.open("http://127.0.0.1:5000")

	# This check ensures the browser is opened only by the main process.
	# Prevents two browser tabs from being opened when in debug mode.
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        # Launch browser 1 second after server starts
        threading.Timer(1.0, open_browser).start()

    # Start Flask app
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)
	

