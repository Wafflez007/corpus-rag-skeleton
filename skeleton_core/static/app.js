// ==========================================
// Skeleton Crew: Core Interaction Logic
// ==========================================

const fileInput = document.getElementById('fileInput');
const queryInput = document.getElementById('queryInput');
const uploadStatus = document.getElementById('upload-status');
const chatHistory = document.getElementById('chat-history');

// --- File Upload Logic ---
async function uploadFile() {
    if (!fileInput.files[0]) {
        showStatus("Please select a file first.", "error");
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    
    showStatus("Transmitting data to core...", "loading");

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        
        if (response.ok) {
            showStatus(`SUCCESS: ${result.message}`, "success");
            // Clear the "System Ready" message if it exists
            if (chatHistory.children[0]?.classList.contains('text-center')) {
                chatHistory.innerHTML = '';
            }
            addSystemMessage("Document ingested. Memory updated.");
        } else {
            showStatus(`ERROR: ${result.error}`, "error");
        }
    } catch (e) {
        showStatus("CRITICAL CONNECTION FAILURE", "error");
        console.error(e);
    }
}

// --- Chat Logic ---
async function sendQuery() {
    const query = queryInput.value.trim();
    if (!query) return;

    // 1. Add User Message immediately
    addMessage(query, 'user');
    queryInput.value = '';

    // 2. Add Loading Indicator
    const loadingId = addLoadingIndicator();

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({query: query})
        });
        const result = await response.json();
        
        // 3. Remove Loading Indicator
        removeMessage(loadingId);
        
        // 4. Add AI Response with Sources
        const aiResponse = result.echo || result.error || "No response received.";
        addMessage(aiResponse, 'ai');

        // NEW: If sources exist, show them!
        if (result.sources && result.sources.length > 0) {
            addSources(result.sources);
        }

    } catch (e) {
        removeMessage(loadingId);
        addMessage("❌ Connection severed. The core is unreachable.", 'error');
        console.error(e);
    }
}

// --- UI Helper Functions ---

function addMessage(text, type) {
    const div = document.createElement('div');
    div.className = `flex ${type === 'user' ? 'justify-end' : 'justify-start'} chat-message`;
    
    let contentClass = type === 'user' 
        ? 'chat-message-user text-white px-5 py-3 rounded-2xl rounded-tr-none shadow-lg max-w-[80%]' 
        : 'chat-message-ai px-5 py-3 rounded-2xl rounded-tl-none shadow-md max-w-[80%]';
        
    const contentDiv = document.createElement('div');
    contentDiv.className = `${contentClass} text-sm leading-relaxed`;
    
    div.appendChild(contentDiv);
    chatHistory.appendChild(div);

    if (type === 'ai') {
        // Determine speed based on theme (Ghost = Slow, Legal = Fast)
        const isGhost = document.body.classList.contains('theme-dark-gothic');
        const speed = isGhost ? 50 : 10; 
        
        let i = 0;
        function typeWriter() {
            if (i < text.length) {
                contentDiv.innerHTML += text.charAt(i);
                i++;
                // Randomize ghost timing for "creepy" feel
                const jitter = isGhost ? Math.random() * 50 : 0;
                setTimeout(typeWriter, speed + jitter);
                chatHistory.scrollTop = chatHistory.scrollHeight;
            }
        }
        typeWriter();
    } else {
        contentDiv.innerHTML = escapeHtml(text);
    }
    
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function addSystemMessage(text) {
    const div = document.createElement('div');
    div.className = "flex justify-center my-2 opacity-50 text-xs tracking-widest uppercase";
    div.innerHTML = `<span>${text}</span>`;
    chatHistory.appendChild(div);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function addLoadingIndicator() {
    const id = 'loading-' + Date.now();
    const div = document.createElement('div');
    div.id = id;
    div.className = "flex justify-start chat-message";
    div.innerHTML = `
        <div class="chat-message-ai px-4 py-3 rounded-2xl rounded-tl-none max-w-[80%] flex gap-2 items-center">
            <div class="w-2 h-2 bg-[var(--accent)] rounded-full animate-bounce"></div>
            <div class="w-2 h-2 bg-[var(--accent)] rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
            <div class="w-2 h-2 bg-[var(--accent)] rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
        </div>
    `;
    chatHistory.appendChild(div);
    chatHistory.scrollTop = chatHistory.scrollHeight;
    return id;
}

function removeMessage(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function showStatus(text, type) {
    uploadStatus.innerText = text;
    uploadStatus.style.opacity = "1";
    
    if (type === 'error') uploadStatus.className = "mt-3 text-xs font-bold text-red-500";
    else if (type === 'success') uploadStatus.className = "mt-3 text-xs font-bold text-green-500";
    else uploadStatus.className = "mt-3 text-xs italic animate-pulse text-[var(--accent)]";
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML.replace(/\n/g, '<br>');
}

function addSources(sources) {
    const isGhost = document.body.classList.contains('theme-dark-gothic');
    const div = document.createElement('div');
    div.className = "flex flex-col justify-start mb-4 ml-2 gap-2";
    
    // Theme-specific styling for the "Evidence" box
    const boxStyle = isGhost 
        ? "border-l-2 border-red-900 text-red-400 italic text-xs pl-3 opacity-80"
        : "bg-blue-50 border border-blue-100 text-blue-800 text-xs p-3 rounded shadow-sm";

    const title = isGhost ? "👁️ ECHOS DETECTED:" : "⚖️ CITATION REFERENCE:";
    
    // Create a clean list of unique sources with page numbers
    // Example: "chang-yun-tai.pdf (Page 5, 12)"
    const sourceMap = {};
    sources.forEach(s => {
        const name = s.source || "Unknown";
        if (!sourceMap[name]) sourceMap[name] = new Set();
        if (s.page) sourceMap[name].add(s.page);
    });

    let sourceHTML = '';
    for (const [name, pages] of Object.entries(sourceMap)) {
        const pageList = Array.from(pages).sort((a,b) => a-b).join(', ');
        const pageText = pageList ? ` (Page ${pageList})` : '';
        sourceHTML += `<div>• ${name}${pageText}</div>`;
    }

    div.innerHTML = `
        <div class="${boxStyle} max-w-[80%]">
            <div class="font-bold mb-1 opacity-70">${title}</div>
            <div class="space-y-1">${sourceHTML}</div>
        </div>
    `;
    chatHistory.appendChild(div);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}