// ==========================================
// Skeleton Crew: Core Interaction Logic
// ==========================================
// 
// This file is organized into the following sections:
// 1. DOM Element References
// 2. Upload Queue Management
// 3. File Validation
// 4. File Upload Logic
// 5. Chat Interface Logic
// 6. Message Display Functions
// 7. Loading Indicators
// 8. Progress Bar Management
// 9. Error Handling
// 10. UI Utilities
// 11. Initialization
// ==========================================

// ==========================================
// 1. DOM ELEMENT REFERENCES
// ==========================================

/** @type {HTMLInputElement} File input element for document uploads */
const fileInput = document.getElementById('fileInput');

/** @type {HTMLInputElement} Text input element for chat queries */
const queryInput = document.getElementById('queryInput');

/** @type {HTMLElement} Container for upload status messages */
const uploadStatus = document.getElementById('upload-status');

/** @type {HTMLElement} Container for chat message history */
const chatHistory = document.getElementById('chat-history');

// ==========================================
// 2. UPLOAD QUEUE MANAGEMENT
// ==========================================

/**
 * Upload queue manager for sequential file processing
 * Ensures files are uploaded one at a time with proper status tracking
 * @namespace
 */
const uploadQueue = {
    /** @type {Array<{file: File, status: string, id: number, error?: string}>} Queue of files to upload */
    queue: [],
    
    /** @type {boolean} Whether a file is currently being processed */
    isProcessing: false,
    
    /**
     * Adds a file to the upload queue and starts processing
     * @param {File} file - The file to add to the queue
     */
    add(file) {
        this.queue.push({
            file: file,
            status: 'queued',
            id: Date.now() + Math.random()
        });
        this.updateQueueDisplay();
        this.processNext();
    },
    
    /**
     * Processes the next file in the queue
     * Automatically called after each upload completes
     */
    processNext() {
        if (this.isProcessing || this.queue.length === 0) {
            return;
        }
        
        this.isProcessing = true;
        const item = this.queue[0];
        item.status = 'processing';
        this.updateQueueDisplay();
        
        this.uploadFile(item)
            .then(() => {
                item.status = 'complete';
                this.queue.shift(); // Remove completed item
                this.updateQueueDisplay();
                this.isProcessing = false;
                this.processNext(); // Process next item in queue
            })
            .catch((error) => {
                item.status = 'error';
                item.error = error.message || 'Upload failed';
                this.updateQueueDisplay();
                this.isProcessing = false;
                // Don't process next automatically on error - wait for user action
            });
    },
    
    /**
     * Uploads a single file with progress tracking
     * @param {{file: File, status: string, id: number}} item - The queue item to upload
     * @returns {Promise<void>}
     * @throws {Error} If upload fails or file validation fails
     */
    async uploadFile(item) {
        const file = item.file;
        
        // Validate file before upload
        const validation = validateFile(file);
        if (!validation.valid) {
            throw new Error(validation.error);
        }

        const formData = new FormData();
        formData.append('file', file);
        
        uploadStatus.style.opacity = "0";
        updateProgress(0, 'reading');

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Upload failed');
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            while (true) {
                const {done, value} = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                const lines = chunk.split('\n');

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const data = JSON.parse(line.substring(6));
                        
                        if (data.error) {
                            hideProgressBar();
                            throw new Error(data.error);
                        }
                        
                        if (data.progress !== undefined) {
                            updateProgress(data.progress, data.stage);
                        }
                        
                        if (data.stage === 'complete') {
                            await new Promise(resolve => setTimeout(resolve, 500));
                            hideProgressBar();
                            showUploadSuccess(data.filename, data.pages || 1);
                            if (chatHistory.children[0]?.classList.contains('text-center')) {
                                chatHistory.innerHTML = '';
                            }
                            addSystemMessage("Document ingested. Memory updated.");
                        }
                    }
                }
            }
        } catch (e) {
            hideProgressBar();
            showUploadError(e.message || "Network connection failed. Please check your connection and try again.");
            throw e;
        }
    },
    
    /**
     * Updates the queue status display in the UI
     * Shows current processing status and queue length
     */
    updateQueueDisplay() {
        const queueStatus = document.getElementById('queue-status');
        if (!queueStatus) return;
        
        if (this.queue.length === 0) {
            queueStatus.style.display = 'none';
            return;
        }
        
        queueStatus.style.display = 'block';
        
        const isGhost = document.body.classList.contains('theme-dark-gothic');
        const queuedCount = this.queue.filter(item => item.status === 'queued').length;
        const processingCount = this.queue.filter(item => item.status === 'processing').length;
        const errorCount = this.queue.filter(item => item.status === 'error').length;
        
        let statusText = '';
        if (processingCount > 0) {
            statusText = isGhost 
                ? `🕯️ Channeling ${this.queue[0].file.name}...`
                : `⚙️ Processing ${this.queue[0].file.name}...`;
        }
        
        if (queuedCount > 0) {
            const queueText = isGhost
                ? `${queuedCount} soul${queuedCount > 1 ? 's' : ''} waiting in the void`
                : `${queuedCount} file${queuedCount > 1 ? 's' : ''} in queue`;
            statusText += statusText ? ` (${queueText})` : queueText;
        }
        
        if (errorCount > 0) {
            const errorText = isGhost
                ? `${errorCount} ritual${errorCount > 1 ? 's' : ''} failed`
                : `${errorCount} error${errorCount > 1 ? 's' : ''}`;
            statusText += statusText ? ` | ${errorText}` : errorText;
        }
        
        queueStatus.innerHTML = `
            <div class="text-xs opacity-70 mt-2 p-2 rounded" 
                 style="background: var(--bg-card); border: 1px solid var(--border);">
                ${statusText}
            </div>
        `;
    },
    
    /**
     * Retries all failed uploads in the queue
     */
    retryFailed() {
        const failedItems = this.queue.filter(item => item.status === 'error');
        failedItems.forEach(item => {
            item.status = 'queued';
            delete item.error;
        });
        this.updateQueueDisplay();
        this.processNext();
    },
    
    /**
     * Removes all failed items from the queue
     */
    clearErrors() {
        this.queue = this.queue.filter(item => item.status !== 'error');
        this.updateQueueDisplay();
    }
};

// ==========================================
// 3. FILE VALIDATION
// ==========================================

/**
 * Validates a file before upload
 * Checks file type, size, and ensures file is not empty
 * 
 * @param {File} file - The file to validate
 * @returns {{valid: boolean, error: string|null}} Validation result with error message if invalid
 */
function validateFile(file) {
    const isGhost = document.body.classList.contains('theme-dark-gothic');
    
    // File type validation - only .txt and .pdf allowed
    const allowedTypes = ['.txt', '.pdf'];
    const fileName = file.name.toLowerCase();
    const hasValidExtension = allowedTypes.some(ext => fileName.endsWith(ext));
    
    if (!hasValidExtension) {
        const errorMsg = isGhost 
            ? "The spirits reject this offering. Only .txt or .pdf scrolls are accepted."
            : "File type not supported. Please upload a .txt or .pdf document.";
        return { valid: false, error: errorMsg };
    }
    
    // File size validation - 10MB limit (configurable)
    const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB in bytes
    if (file.size > MAX_FILE_SIZE) {
        const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
        const maxMB = (MAX_FILE_SIZE / (1024 * 1024)).toFixed(0);
        const errorMsg = isGhost
            ? `This tome is too heavy for the spirits (${sizeMB}MB). Maximum: ${maxMB}MB.`
            : `File size exceeds limit (${sizeMB}MB). Maximum allowed: ${maxMB}MB.`;
        return { valid: false, error: errorMsg };
    }
    
    // Empty file check
    if (file.size === 0) {
        const errorMsg = isGhost
            ? "The void rejects emptiness. This scroll contains no essence."
            : "File appears to be empty. Please select a valid document.";
        return { valid: false, error: errorMsg };
    }
    
    // All validations passed
    return { valid: true, error: null };
}

// ==========================================
// 4. FILE UPLOAD LOGIC
// ==========================================

/**
 * Handles file upload button click
 * Validates the selected file and adds it to the upload queue
 * @returns {Promise<void>}
 */
async function uploadFile() {
    if (!fileInput.files[0]) {
        showStatus("Please select a file first.", "error");
        return;
    }
    
    const file = fileInput.files[0];
    
    // Quick validation before adding to queue
    const validation = validateFile(file);
    if (!validation.valid) {
        showUploadError(validation.error);
        return;
    }
    
    // Add to queue for sequential processing
    uploadQueue.add(file);
    
    // Clear file input so user can select same file again if needed
    fileInput.value = '';
}

// ==========================================
// 5. CHAT INTERFACE LOGIC
// ==========================================

/**
 * Sends a chat query to the server and displays the response
 * Handles user message display, loading indicators, and AI response rendering
 * @returns {Promise<void>}
 */
async function sendQuery() {
    const query = queryInput.value.trim();
    if (!query) return;

    // 1. Add User Message immediately
    addMessage(query, 'user');
    queryInput.value = '';

    // 2. Show Loading Indicator during query processing
    const loadingId = showLoading();

    try {
        // Get selected document sources for filtering
        const selectedSources = getSelectedSources();
        
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                query: query,
                sources: selectedSources
            })
        });
        const result = await response.json();
        
        // 3. Hide Loading Indicator
        hideLoading(loadingId);
        
        // 4. Add AI Response with Sources
        const aiResponse = result.echo || result.error || "No response received.";
        addMessage(aiResponse, 'ai');

        // NEW: If sources exist, show them!
        if (result.sources && result.sources.length > 0) {
            addSources(result.sources);
        }

    } catch (e) {
        hideLoading(loadingId);
        
        // Use comprehensive error handling with retry option
        showNetworkError('query', () => {
            // Restore the query and retry
            queryInput.value = query;
            sendQuery();
        }, chatHistory);
        
        console.error(e);
    }
}

/**
 * Sets up Enter key submission for the chat input field
 * - Enter key alone: submits the query
 * - Shift+Enter: allows multi-line input (if textarea is used in future)
 * - Prevents default form submission behavior
 */
function setupEnterKeySubmission() {
    if (!queryInput) return;
    
    queryInput.addEventListener('keypress', function(event) {
        // Check if Enter key was pressed
        if (event.key === 'Enter') {
            // If Shift is held, allow multi-line input (do nothing)
            if (event.shiftKey) {
                // Allow default behavior for multi-line input
                return;
            }
            
            // Enter alone: prevent default and submit query
            event.preventDefault();
            sendQuery();
        }
    });
}

// ==========================================
// 6. MESSAGE DISPLAY FUNCTIONS
// ==========================================

/**
 * Scrolls the chat history to the bottom to show the latest message
 * Implements smooth scrolling with edge case handling for user manual scroll
 * Only scrolls if user is already near the bottom (within 100px)
 */
function scrollToBottom() {
    const chatHistory = document.getElementById('chat-history');
    if (!chatHistory) return;
    
    // Check if user has manually scrolled up
    // If they're within 100px of the bottom (inclusive), auto-scroll
    // Otherwise, respect their scroll position
    const distanceFromBottom = chatHistory.scrollHeight - chatHistory.scrollTop - chatHistory.clientHeight;
    const isNearBottom = distanceFromBottom <= 100;
    
    if (isNearBottom) {
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
}

/**
 * Adds a message to the chat history
 * Handles both user and AI messages with distinct styling
 * Implements typewriter effect for AI messages
 * 
 * @param {string} text - The message text to display
 * @param {'user'|'ai'} type - The type of message (user or ai)
 */
function addMessage(text, type) {
    const div = document.createElement('div');
    div.className = `flex ${type === 'user' ? 'justify-end' : 'justify-start'} chat-message animate-pop-in`;
    
    // Distinct CSS classes for user vs AI messages
    let contentClass = type === 'user' 
        ? 'chat-message-user text-white px-5 py-3 rounded-2xl rounded-tr-none shadow-lg' 
        : 'chat-message-ai px-5 py-3 rounded-2xl rounded-tl-none shadow-md';
    
    // Create message container with proper structure
    const messageContainer = document.createElement('div');
    const isGhost = document.body.classList.contains('theme-dark-gothic');
    
    messageContainer.className = type === 'user' 
        ? 'flex items-start gap-2 flex-row-reverse max-w-[80%]'
        : 'flex items-start gap-2 max-w-[80%]';
    
    // Add icon/avatar for both user and AI messages
    const icon = document.createElement('span');
    icon.className = 'message-icon text-xl flex-shrink-0';
    
    if (type === 'ai') {
        icon.setAttribute('aria-label', 'AI response');
        icon.textContent = isGhost ? '🔮' : '⚖️';
    } else {
        icon.setAttribute('aria-label', 'User message');
        icon.textContent = isGhost ? '👤' : '👤';
    }
    
    messageContainer.appendChild(icon);
    
    // Create content wrapper
    const contentWrapper = document.createElement('div');
    contentWrapper.className = 'flex flex-col';
    
    // Create content div with proper styling
    const contentDiv = document.createElement('div');
    contentDiv.className = `${contentClass} text-sm leading-relaxed`;
    contentDiv.style.wordBreak = 'break-word';
    contentDiv.style.whiteSpace = 'pre-wrap';
    contentDiv.style.display = 'block';
    
    // Add timestamp (optional, non-intrusive)
    const timestamp = new Date();
    const timeString = timestamp.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
    
    const timestampDiv = document.createElement('div');
    timestampDiv.className = 'message-timestamp text-xs opacity-50 mt-1';
    timestampDiv.textContent = timeString;
    timestampDiv.setAttribute('aria-label', `Message sent at ${timeString}`);
    
    // Assemble the structure
    contentWrapper.appendChild(contentDiv);
    contentWrapper.appendChild(timestampDiv);
    messageContainer.appendChild(contentWrapper);
    div.appendChild(messageContainer);
    
    // Immediate display of user messages
    chatHistory.appendChild(div);
    
    if (type === 'ai') {
        // Play response sound when AI starts answering
        audioManager.playResponseSound();
        
        // Determine speed based on theme (Ghost = Slow, Legal = Fast)
        const isGhost = document.body.classList.contains('theme-dark-gothic');
        const speed = isGhost ? 50 : 10; 
        
        let i = 0;
        function typeWriter() {
            if (i < text.length) {
                // Handle code blocks with monospace formatting
                const char = text.charAt(i);
                
                // Simple code block detection (text between backticks)
                if (char === '`') {
                    const nextBacktick = text.indexOf('`', i + 1);
                    if (nextBacktick !== -1) {
                        // Extract code block
                        const codeText = text.substring(i + 1, nextBacktick);
                        const codeSpan = document.createElement('code');
                        codeSpan.className = 'font-mono bg-opacity-20 px-1 rounded';
                        codeSpan.style.backgroundColor = 'var(--border)';
                        codeSpan.textContent = codeText;
                        contentDiv.appendChild(codeSpan);
                        i = nextBacktick + 1;
                    } else {
                        contentDiv.innerHTML += char;
                        i++;
                    }
                } else {
                    contentDiv.innerHTML += char;
                    i++;
                }
                
                // Randomize ghost timing for "creepy" feel
                const jitter = isGhost ? Math.random() * 50 : 0;
                setTimeout(typeWriter, speed + jitter);
                scrollToBottom();
            } else {
                // Typing complete - stop the response sound
                audioManager.stopResponseSound();
            }
        }
        typeWriter();
    } else {
        // Immediate display with proper text wrapping and escaping
        contentDiv.innerHTML = formatMessageText(text);
    }
    
    // Auto-scroll to show latest message
    scrollToBottom();
}

/**
 * Formats message text with proper HTML escaping and code block support
 * Handles inline code blocks (text between backticks)
 * 
 * @param {string} text - The raw message text
 * @returns {string} HTML-formatted message text
 */
function formatMessageText(text) {
    // Escape HTML but preserve line breaks
    const escaped = escapeHtml(text);
    
    // Handle code blocks (text between backticks)
    return escaped.replace(/`([^`]+)`/g, '<code class="font-mono bg-opacity-20 px-1 rounded" style="background-color: var(--border);">$1</code>');
}

/**
 * Adds a system message to the chat history
 * Used for status updates like "Document ingested"
 * 
 * @param {string} text - The system message text
 */
function addSystemMessage(text) {
    const div = document.createElement('div');
    div.className = "flex justify-center my-2 opacity-50 text-xs tracking-widest uppercase";
    div.innerHTML = `<span>${text}</span>`;
    chatHistory.appendChild(div);
    scrollToBottom();
}

/**
 * Adds source citations to the chat history
 * Displays document sources with page numbers
 * Only shows sources that actually contained relevant information
 * 
 * @param {Array<{source: string, page: number}>} sources - Array of source objects from vector search results
 */
function addSources(sources) {
    // Filter out any empty or invalid sources
    const validSources = sources.filter(s => s && s.source);
    
    // Don't show sources section if no valid sources exist
    if (validSources.length === 0) {
        return;
    }
    
    const isGhost = document.body.classList.contains('theme-dark-gothic');
    const div = document.createElement('div');
    div.className = "flex flex-col justify-start mb-4 ml-2 gap-2";
    
    // Theme-specific styling for the "Evidence" box
    const boxStyle = isGhost 
        ? "border-l-2 border-red-900 text-red-400 italic text-xs pl-3 opacity-80"
        : "bg-blue-50 border border-blue-100 text-blue-800 text-xs p-3 rounded shadow-sm";

    const title = isGhost ? "👁️ ECHOS DETECTED:" : "⚖️ CITATION REFERENCE:";
    
    // Create a clean list of unique sources with page numbers
    // Only includes sources that were actually retrieved by vector search
    const sourceMap = {};
    validSources.forEach(s => {
        const name = s.source;
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
    scrollToBottom();
}

// ==========================================
// 7. LOADING INDICATORS
// ==========================================

/**
 * Shows a loading indicator in the chat area during AI response generation
 * Creates a typing indicator with animated dots
 * @returns {string} The ID of the loading indicator element
 */
function showLoading() {
    const id = 'loading-' + Date.now();
    const div = document.createElement('div');
    div.id = id;
    div.className = "flex justify-start chat-message loading-indicator";
    div.style.opacity = '0';
    div.innerHTML = `
        <div class="chat-message-ai px-4 py-3 rounded-2xl rounded-tl-none max-w-[80%] flex gap-2 items-center">
            <div class="w-2 h-2 bg-[var(--accent)] rounded-full animate-bounce"></div>
            <div class="w-2 h-2 bg-[var(--accent)] rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
            <div class="w-2 h-2 bg-[var(--accent)] rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
        </div>
    `;
    chatHistory.appendChild(div);
    
    // Smooth fade-in transition
    setTimeout(() => {
        div.style.transition = 'opacity 0.3s ease-in';
        div.style.opacity = '1';
    }, 10);
    
    scrollToBottom();
    return id;
}

/**
 * Hides and removes a loading indicator from the chat area
 * Applies smooth fade-out transition before removal
 * @param {string} id - The ID of the loading indicator to remove
 */
function hideLoading(id) {
    const el = document.getElementById(id);
    if (el) {
        // Smooth fade-out transition
        el.style.transition = 'opacity 0.3s ease-out';
        el.style.opacity = '0';
        
        // Remove element after transition completes
        setTimeout(() => {
            if (el.parentNode) {
                el.remove();
            }
        }, 300);
    }
}

// ==========================================
// 8. PROGRESS BAR MANAGEMENT
// ==========================================

/**
 * Displays a status message in the upload status area
 * @param {string} text - The status message text
 * @param {'error'|'success'|'info'} type - The type of status message
 */
function showStatus(text, type) {
    uploadStatus.innerText = text;
    uploadStatus.style.opacity = "1";
    
    if (type === 'error') uploadStatus.className = "mt-3 text-xs font-bold text-red-500";
    else if (type === 'success') uploadStatus.className = "mt-3 text-xs font-bold text-green-500";
    else uploadStatus.className = "mt-3 text-xs italic animate-pulse text-[var(--accent)]";
}

/**
 * Displays upload success feedback with document details
 * Shows theme-appropriate success message with filename and page count
 * Auto-dismisses after 5 seconds
 * 
 * @param {string} filename - The name of the uploaded file
 * @param {number} pageCount - The number of pages in the document
 */
function showUploadSuccess(filename, pageCount) {
    const isGhost = document.body.classList.contains('theme-dark-gothic');
    
    // Theme-appropriate success messages with page count
    const pageText = pageCount === 1 ? 'page' : 'pages';
    const message = isGhost
        ? `✨ The spirits have accepted "${filename}". ${pageCount} ${pageText} absorbed into the void.`
        : `✓ Document "${filename}" successfully processed. ${pageCount} ${pageText} indexed.`;
    
    // Create success message element
    const successDiv = document.createElement('div');
    successDiv.className = 'upload-feedback success-message';
    successDiv.innerHTML = `
        <div class="flex items-start gap-3 p-4 rounded-lg shadow-lg animate-fade-in" 
             style="background: ${isGhost ? 'rgba(139, 0, 0, 0.2)' : 'rgba(34, 197, 94, 0.1)'}; 
                    border: 1px solid ${isGhost ? 'var(--accent)' : '#22c55e'};">
            <span class="text-xl">${isGhost ? '🔮' : '✓'}</span>
            <div class="flex-1">
                <p class="text-sm font-semibold mb-1" style="color: ${isGhost ? 'var(--accent)' : '#22c55e'};">
                    ${isGhost ? 'Ritual Complete' : 'Upload Successful'}
                </p>
                <p class="text-xs opacity-80">${message}</p>
            </div>
        </div>
    `;
    
    // Clear previous feedback and show new message
    uploadStatus.innerHTML = '';
    uploadStatus.appendChild(successDiv);
    uploadStatus.style.opacity = "1";
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        successDiv.style.transition = 'opacity 0.5s ease-out';
        successDiv.style.opacity = '0';
        setTimeout(() => {
            if (uploadStatus.contains(successDiv)) {
                uploadStatus.removeChild(successDiv);
            }
        }, 500);
    }, 5000);
}

/**
 * Displays upload error feedback with specific error reason
 * Shows theme-appropriate error message with dismiss button
 * 
 * @param {string} errorReason - The reason for the upload failure
 */
function showUploadError(errorReason) {
    const isGhost = document.body.classList.contains('theme-dark-gothic');
    
    // Theme-appropriate error messages
    const title = isGhost ? 'The Spirits Reject This' : 'Upload Failed';
    const icon = isGhost ? '💀' : '⚠️';
    
    // Create error message element with dismiss button
    const errorDiv = document.createElement('div');
    errorDiv.className = 'upload-feedback error-message';
    errorDiv.innerHTML = `
        <div class="flex items-start gap-3 p-4 rounded-lg shadow-lg animate-fade-in" 
             style="background: rgba(239, 68, 68, 0.1); border: 1px solid #ef4444;">
            <span class="text-xl">${icon}</span>
            <div class="flex-1">
                <p class="text-sm font-semibold mb-1" style="color: #ef4444;">
                    ${title}
                </p>
                <p class="text-xs opacity-80">${errorReason}</p>
            </div>
            <button onclick="dismissUploadError(this)" 
                    class="text-xs px-2 py-1 rounded hover:bg-red-500 hover:bg-opacity-20 transition-colors"
                    style="color: #ef4444;">
                ✕
            </button>
        </div>
    `;
    
    // Clear previous feedback and show new message
    uploadStatus.innerHTML = '';
    uploadStatus.appendChild(errorDiv);
    uploadStatus.style.opacity = "1";
}

/**
 * Dismisses an upload error message
 * Called when user clicks the dismiss button
 * 
 * @param {HTMLElement} button - The dismiss button element
 */
function dismissUploadError(button) {
    const errorDiv = button.closest('.upload-feedback');
    if (errorDiv) {
        errorDiv.style.transition = 'opacity 0.3s ease-out';
        errorDiv.style.opacity = '0';
        setTimeout(() => {
            if (uploadStatus.contains(errorDiv)) {
                uploadStatus.removeChild(errorDiv);
            }
        }, 300);
    }
}

/**
 * Updates the upload progress bar
 * Validates percent value and delegates to showProgressBar
 * 
 * @param {number} percent - The progress percentage (0-100)
 * @param {string} stage - The current upload stage
 */
function updateProgress(percent, stage) {
    // Core function to update progress bar UI
    // Validates inputs and delegates to showProgressBar
    
    // Ensure percent is within valid range [0, 100]
    const validPercent = Math.max(0, Math.min(100, percent));
    
    // Show the progress bar with updated values
    showProgressBar(validPercent, stage || 'processing');
}

/**
 * Shows and updates the progress bar UI
 * Updates bar width, percentage text, and stage label
 * 
 * @param {number} percent - The progress percentage (0-100)
 * @param {string} stage - The current upload stage
 */
function showProgressBar(percent, stage) {
    const container = document.getElementById('upload-progress-container');
    const bar = document.getElementById('progress-bar');
    const percentText = document.getElementById('progress-percent');
    const label = document.getElementById('progress-label');
    
    const isGhost = document.body.classList.contains('theme-dark-gothic');
    
    container.classList.remove('hidden');
    bar.style.width = percent + '%';
    percentText.innerText = percent + '%';
    
    // Update label based on stage
    const stageLabels = {
        'reading': isGhost ? '📖 Reading grimoire...' : '📖 Reading file...',
        'parsing': isGhost ? '🔮 Deciphering runes...' : '📄 Parsing pages...',
        'vectorizing': isGhost ? '👻 Channeling spirits...' : '⚙️ Vectorizing...',
        'finalizing': isGhost ? '✨ Sealing ritual...' : '✓ Finalizing...',
        'complete': isGhost ? '✨ Ritual Complete' : '✓ Complete'
    };
    
    label.innerText = stageLabels[stage] || (isGhost ? '🕯️ Processing...' : '⚙️ Processing...');
}

/**
 * Hides the progress bar
 */
function hideProgressBar() {
    const container = document.getElementById('upload-progress-container');
    container.classList.add('hidden');
}

// ==========================================
// 9. ERROR HANDLING
// ==========================================

/**
 * Shows a comprehensive error message with title, description, and dismiss button
 * Implements theme-appropriate styling and ARIA live regions for accessibility
 * 
 * @param {string} title - The error title/heading
 * @param {string} description - Detailed error description
 * @param {HTMLElement} container - The container element to display the error in (optional, defaults to body)
 * @param {Object} options - Additional options for error display
 * @param {number} options.timeout - Auto-dismiss timeout in milliseconds (0 = no auto-dismiss)
 * @param {boolean} options.retryable - Whether to show a retry button
 * @param {Function} options.onRetry - Callback function for retry action
 * @param {Function} options.onDismiss - Callback function when error is dismissed
 * @returns {HTMLElement} The error element that was created
 */
function showError(title, description, container = null, options = {}) {
    const isGhost = document.body.classList.contains('theme-dark-gothic');
    
    // Default options
    const {
        timeout = 0,
        retryable = false,
        onRetry = null,
        onDismiss = null
    } = options;
    
    // Theme-appropriate icons and styling
    const icon = isGhost ? '💀' : '⚠️';
    const errorClass = isGhost ? 'error-message-gothic' : 'error-message-professional';
    
    // Create error element with proper ARIA attributes
    const errorDiv = document.createElement('div');
    errorDiv.className = `error-message ${errorClass} animate-fade-in`;
    errorDiv.setAttribute('role', 'alert');
    errorDiv.setAttribute('aria-live', 'assertive');
    errorDiv.setAttribute('aria-atomic', 'true');
    
    // Build error content
    let errorHTML = `
        <div class="flex items-start gap-3 p-4 rounded-lg shadow-lg" 
             style="background: rgba(239, 68, 68, 0.1); border: 1px solid #ef4444;">
            <span class="text-xl flex-shrink-0" aria-hidden="true">${icon}</span>
            <div class="flex-1">
                <p class="text-sm font-semibold mb-1" style="color: #ef4444;">
                    ${escapeHtml(title)}
                </p>
                <p class="text-xs opacity-80" style="color: var(--text-main);">
                    ${escapeHtml(description)}
                </p>
            </div>
            <div class="flex gap-2 flex-shrink-0">
    `;
    
    // Add retry button if retryable
    if (retryable && onRetry) {
        errorHTML += `
            <button class="error-retry-btn text-xs px-3 py-1 rounded transition-colors font-semibold"
                    style="background: #ef4444; color: white;"
                    aria-label="Retry action">
                ${isGhost ? '🔄 Retry Ritual' : '🔄 Retry'}
            </button>
        `;
    }
    
    // Add dismiss button
    errorHTML += `
                <button class="error-dismiss-btn text-xs px-2 py-1 rounded hover:bg-red-500 hover:bg-opacity-20 transition-colors"
                        style="color: #ef4444;"
                        aria-label="Dismiss error">
                    ✕
                </button>
            </div>
        </div>
    `;
    
    errorDiv.innerHTML = errorHTML;
    
    // Add event listeners
    const dismissBtn = errorDiv.querySelector('.error-dismiss-btn');
    dismissBtn.addEventListener('click', () => {
        dismissError(errorDiv, onDismiss);
    });
    
    if (retryable && onRetry) {
        const retryBtn = errorDiv.querySelector('.error-retry-btn');
        retryBtn.addEventListener('click', () => {
            dismissError(errorDiv);
            onRetry();
        });
    }
    
    // Append to container or body
    const targetContainer = container || document.body;
    targetContainer.appendChild(errorDiv);
    
    // Auto-dismiss if timeout is set
    if (timeout > 0) {
        setTimeout(() => {
            if (errorDiv.parentNode) {
                dismissError(errorDiv, onDismiss);
            }
        }, timeout);
    }
    
    return errorDiv;
}

/**
 * Dismisses an error message with smooth fade-out animation
 * 
 * @param {HTMLElement} errorElement - The error element to dismiss
 * @param {Function} onDismiss - Optional callback function when dismissed
 */
function dismissError(errorElement, onDismiss = null) {
    if (!errorElement || !errorElement.parentNode) return;
    
    // Smooth fade-out transition
    errorElement.style.transition = 'opacity 0.3s ease-out, transform 0.3s ease-out';
    errorElement.style.opacity = '0';
    errorElement.style.transform = 'translateY(-10px)';
    
    // Remove element after transition completes
    setTimeout(() => {
        if (errorElement.parentNode) {
            errorElement.remove();
        }
        
        // Call onDismiss callback if provided
        if (onDismiss && typeof onDismiss === 'function') {
            onDismiss();
        }
    }, 300);
}

/**
 * Shows a network error with retry option
 * Specialized error handler for network-related failures
 * 
 * @param {string} operation - The operation that failed (e.g., "upload", "query")
 * @param {Function} retryCallback - Function to call when user clicks retry
 * @param {HTMLElement} container - Optional container for the error
 */
function showNetworkError(operation, retryCallback, container = null) {
    const isGhost = document.body.classList.contains('theme-dark-gothic');
    
    const title = isGhost 
        ? 'The Veil Has Closed' 
        : 'Network Connection Failed';
    
    const description = isGhost
        ? `The spirits cannot reach the mortal realm. The ${operation} ritual has been interrupted. Check your connection and try again.`
        : `Unable to complete ${operation} operation. Please check your network connection and try again.`;
    
    showError(title, description, container, {
        retryable: true,
        onRetry: retryCallback,
        timeout: 0 // Don't auto-dismiss network errors
    });
}

/**
 * Shows a generic error in the chat area
 * Convenience function for displaying errors in the chat interface
 * 
 * @param {string} message - The error message to display
 */
function showChatError(message) {
    const isGhost = document.body.classList.contains('theme-dark-gothic');
    
    const title = isGhost ? 'The Spirits Are Silent' : 'Error';
    
    showError(title, message, chatHistory, {
        timeout: 8000 // Auto-dismiss after 8 seconds
    });
}

// ==========================================
// 10. UI UTILITIES
// ==========================================

/**
 * Escapes HTML special characters and preserves line breaks
 * Prevents XSS attacks by converting HTML to text
 * 
 * @param {string} text - The text to escape
 * @returns {string} HTML-safe text with line breaks
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML.replace(/\n/g, '<br>');
}

/**
 * Checks if the current theme is the Ghost/Ouija Board theme
 * @returns {boolean} True if Ghost theme is active
 */
function isGhostTheme() {
    return document.body.classList.contains('theme-dark-gothic');
}

/**
 * Gets theme-appropriate text for a given context
 * @param {string} ghostText - Text to use for Ghost theme
 * @param {string} legalText - Text to use for Legal Eagle theme
 * @returns {string} The appropriate text for the current theme
 */
function getThemeText(ghostText, legalText) {
    return isGhostTheme() ? ghostText : legalText;
}

// ==========================================
// 11. AUDIO MANAGEMENT
// ==========================================

/**
 * Audio manager for handling background ambience and response sounds
 * Implements browser autoplay policy compliance and mute controls
 * @namespace
 */
const audioManager = {
    /** @type {HTMLAudioElement|null} Background audio element (Ghost mode only) */
    bgAudio: null,
    
    /** @type {HTMLAudioElement|null} Response sound effect element */
    responseAudio: null,
    
    /** @type {HTMLButtonElement|null} Mute toggle button */
    soundToggle: null,
    
    /** @type {boolean} Whether audio is currently muted */
    isMuted: false,
    
    /** @type {boolean} Whether background audio has been started */
    bgStarted: false,
    
    /**
     * Initializes the audio system
     * Sets up audio elements and event listeners
     */
    init() {
        this.bgAudio = document.getElementById('bg-audio');
        this.responseAudio = document.getElementById('response-audio');
        this.soundToggle = document.getElementById('sound-toggle');
        
        if (!this.soundToggle) return;
        
        // Set up mute toggle button
        this.soundToggle.addEventListener('click', () => {
            this.toggleMute();
        });
        
        // Auto-start Ghost ambience on first user interaction
        // (Browsers block autoplay until user interacts with the page)
        if (this.bgAudio) {
            const startAmbience = () => {
                if (!this.bgStarted && !this.isMuted) {
                    this.startBackgroundAudio();
                }
            };
            
            // Listen for first click or keypress
            document.addEventListener('click', startAmbience, { once: true });
            document.addEventListener('keypress', startAmbience, { once: true });
        }
    },
    
    /**
     * Starts background audio (Ghost mode only)
     * Handles browser autoplay restrictions gracefully
     */
    startBackgroundAudio() {
        if (!this.bgAudio || this.bgStarted) return;
        
        this.bgAudio.volume = 0.3; // Keep it subtle
        this.bgAudio.play()
            .then(() => {
                this.bgStarted = true;
                console.log('Background ambience started');
            })
            .catch(e => {
                console.log('Audio waiting for user interaction:', e.message);
            });
    },
    
    /**
     * Plays the response sound effect with looping
     * Called when AI starts responding
     * The sound will loop continuously until stopResponseSound() is called
     */
    playResponseSound() {
        if (!this.responseAudio || this.isMuted) return;
        
        this.responseAudio.currentTime = 0; // Reset to start
        this.responseAudio.volume = 0.5;
        this.responseAudio.loop = true; // Enable looping
        this.responseAudio.play()
            .catch(e => {
                console.log('Response sound failed:', e.message);
            });
    },
    
    /**
     * Stops the response sound effect immediately
     * Called when AI finishes typing
     */
    stopResponseSound() {
        if (!this.responseAudio) return;
        
        this.responseAudio.pause();
        this.responseAudio.currentTime = 0; // Reset to start for next time
        this.responseAudio.loop = false; // Disable looping
    },
    
    /**
     * Toggles mute state for all audio
     * Updates button icon and pauses/resumes audio
     */
    toggleMute() {
        this.isMuted = !this.isMuted;
        
        // Update button icon
        if (this.soundToggle) {
            this.soundToggle.innerText = this.isMuted ? '🔇' : '🔊';
            this.soundToggle.setAttribute('aria-label', 
                this.isMuted ? 'Unmute sound' : 'Mute sound');
        }
        
        // Handle background audio
        if (this.bgAudio) {
            if (this.isMuted) {
                this.bgAudio.pause();
            } else {
                this.startBackgroundAudio();
            }
        }
    },
    
    /**
     * Checks if audio is available and not muted
     * @returns {boolean} True if audio can be played
     */
    isAudioEnabled() {
        return !this.isMuted && (this.bgAudio !== null || this.responseAudio !== null);
    }
};

// ==========================================
// 12. INITIALIZATION
// ==========================================

/**
 * Initializes the application when DOM is ready
 * Sets up event listeners and prepares the UI
 */
function initializeApp() {
    // Set up Enter key submission for chat
    setupEnterKeySubmission();
    
    // Initialize audio system
    audioManager.init();
    
    // Load document library
    refreshDocuments();
    
    // Add any other initialization code here
    console.log('Skeleton Crew initialized');
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApp);
} else {
    // DOM already loaded
    initializeApp();
}

// ==========================================
// 13. DOCUMENT LIBRARY MANAGEMENT
// ==========================================

/**
 * Fetches and displays the list of uploaded documents
 * Shows document name, page count, and chunk count with selection checkboxes
 */
async function refreshDocuments() {
    const documentList = document.getElementById('document-list');
    if (!documentList) return;
    
    const isGhost = document.body.classList.contains('theme-dark-gothic');
    
    try {
        const response = await fetch('/documents');
        const data = await response.json();
        
        if (!data.documents || data.documents.length === 0) {
            documentList.innerHTML = `
                <div class="text-center text-xs opacity-40 py-4">
                    ${isGhost ? 'No spirits bound yet...' : 'No documents uploaded yet'}
                </div>
            `;
            updateSelectionCount();
            return;
        }
        
        // Build document list with checkboxes
        let html = '';
        data.documents.forEach(doc => {
            const pageText = doc.pages === 1 ? 'page' : 'pages';
            const chunkText = doc.chunks === 1 ? 'chunk' : 'chunks';
            
            html += `
                <div class="document-item flex items-center gap-3 p-2 rounded hover:bg-opacity-50 transition-all" 
                     style="background: var(--bg-card);">
                    <input type="checkbox" 
                           class="doc-checkbox cursor-pointer" 
                           data-source="${escapeHtml(doc.source)}"
                           onchange="updateSelectionCount()"
                           checked>
                    <div class="flex-1 min-w-0">
                        <div class="text-sm font-semibold truncate" title="${escapeHtml(doc.source)}">
                            ${isGhost ? '📜' : '📄'} ${escapeHtml(doc.source)}
                        </div>
                        <div class="text-xs opacity-60">
                            ${doc.pages} ${pageText} • ${doc.chunks} ${chunkText}
                        </div>
                    </div>
                    <button onclick="deleteDocument('${escapeHtml(doc.source)}')" 
                            class="text-xs px-2 py-1 rounded opacity-60 hover:opacity-100 transition-opacity"
                            style="color: #ef4444;"
                            title="Delete document">
                        🗑️
                    </button>
                </div>
            `;
        });
        
        documentList.innerHTML = html;
        updateSelectionCount();
        
    } catch (e) {
        console.error('Failed to load documents:', e);
        documentList.innerHTML = `
            <div class="text-center text-xs text-red-500 py-4">
                ${isGhost ? 'The spirits refuse to manifest...' : 'Failed to load documents'}
            </div>
        `;
    }
}

/**
 * Deletes a document from the database
 * @param {string} source - The document source identifier
 */
async function deleteDocument(source) {
    const isGhost = document.body.classList.contains('theme-dark-gothic');
    
    const title = isGhost ? 'Banish Document?' : 'Delete Document?';
    const message = isGhost
        ? `Banish "${source}" from the void? This cannot be undone.`
        : `Delete "${source}"? This action cannot be undone.`;
    const confirmText = isGhost ? 'Banish' : 'Delete';
    
    showConfirmDialog({
        title,
        message,
        confirmText,
        cancelText: 'Cancel',
        dangerous: true,
        onConfirm: async () => {
            try {
                const response = await fetch(`/documents/${encodeURIComponent(source)}`, {
                    method: 'DELETE'
                });
                
                const result = await response.json();
                
                if (result.success) {
                    // Refresh the document list
                    await refreshDocuments();
                    
                    // Show success message
                    const successMsg = isGhost
                        ? `${source} has been banished. ${result.deleted_chunks} fragments erased.`
                        : `${source} deleted successfully. ${result.deleted_chunks} chunks removed.`;
                    
                    addSystemMessage(successMsg);
                } else {
                    throw new Error(result.error || 'Delete failed');
                }
                
            } catch (e) {
                console.error('Delete failed:', e);
                const errorMsg = isGhost
                    ? 'The spirits resist banishment...'
                    : 'Failed to delete document';
                showChatError(errorMsg);
            }
        }
    });
}

/**
 * Toggles all document checkboxes
 */
function toggleAllDocuments() {
    const selectAll = document.getElementById('select-all-docs');
    const checkboxes = document.querySelectorAll('.doc-checkbox');
    
    checkboxes.forEach(cb => {
        cb.checked = selectAll.checked;
    });
    
    updateSelectionCount();
}

/**
 * Updates the selection count display
 */
function updateSelectionCount() {
    const checkboxes = document.querySelectorAll('.doc-checkbox');
    const checked = document.querySelectorAll('.doc-checkbox:checked');
    const countDisplay = document.getElementById('selection-count');
    const selectAll = document.getElementById('select-all-docs');
    
    if (countDisplay) {
        countDisplay.textContent = `${checked.length} selected`;
    }
    
    // Update "select all" checkbox state
    if (selectAll) {
        selectAll.checked = checkboxes.length > 0 && checked.length === checkboxes.length;
        selectAll.indeterminate = checked.length > 0 && checked.length < checkboxes.length;
    }
}

/**
 * Gets the list of selected document sources
 * @returns {string[]|null} Array of selected sources, or null if all are selected
 */
function getSelectedSources() {
    const checkboxes = document.querySelectorAll('.doc-checkbox');
    const checked = document.querySelectorAll('.doc-checkbox:checked');
    
    // If all are selected, return null (no filter)
    if (checked.length === checkboxes.length) {
        return null;
    }
    
    // Return array of selected sources
    return Array.from(checked).map(cb => cb.dataset.source);
}

// ==========================================
// 14. CUSTOM MODAL DIALOG SYSTEM
// ==========================================

/**
 * Shows a custom confirmation dialog with theme-appropriate styling
 * @param {Object} options - Configuration options
 * @param {string} options.title - Dialog title
 * @param {string} options.message - Dialog message
 * @param {string} options.confirmText - Text for confirm button (default: "Confirm")
 * @param {string} options.cancelText - Text for cancel button (default: "Cancel")
 * @param {Function} options.onConfirm - Callback when confirmed
 * @param {Function} options.onCancel - Callback when cancelled (optional)
 * @param {boolean} options.dangerous - Whether this is a dangerous action (red styling)
 */
function showConfirmDialog(options) {
    const {
        title = 'Confirm Action',
        message = 'Are you sure?',
        confirmText = 'Confirm',
        cancelText = 'Cancel',
        onConfirm = () => {},
        onCancel = () => {},
        dangerous = false
    } = options;
    
    const isGhost = document.body.classList.contains('theme-dark-gothic');
    
    // Create modal overlay
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(5px);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        animation: fadeIn 0.2s ease-out;
    `;
    
    // Create modal dialog
    const modal = document.createElement('div');
    modal.className = 'modal-dialog';
    modal.style.cssText = `
        background: var(--bg-card);
        border: 2px solid ${dangerous ? '#ef4444' : 'var(--border)'};
        border-radius: 12px;
        padding: 24px;
        max-width: 450px;
        width: 90%;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        animation: slideUp 0.3s ease-out;
        position: relative;
    `;
    
    // Add glow effect for ghost theme
    if (isGhost) {
        modal.style.boxShadow = `0 0 40px ${dangerous ? 'rgba(139, 0, 0, 0.5)' : 'rgba(139, 0, 0, 0.3)'}, 0 20px 60px rgba(0, 0, 0, 0.5)`;
    }
    
    // Icon based on theme and danger level
    let icon = '❓';
    if (dangerous) {
        icon = isGhost ? '💀' : '⚠️';
    } else {
        icon = isGhost ? '🔮' : '📋';
    }
    
    // Build modal content
    modal.innerHTML = `
        <div class="modal-header" style="margin-bottom: 16px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 32px;">${icon}</span>
                <h3 style="font-size: 20px; font-weight: bold; color: ${dangerous ? '#ef4444' : 'var(--primary)'}; margin: 0;">
                    ${escapeHtml(title)}
                </h3>
            </div>
        </div>
        <div class="modal-body" style="margin-bottom: 24px;">
            <p style="color: var(--text-main); line-height: 1.6; margin: 0;">
                ${escapeHtml(message)}
            </p>
        </div>
        <div class="modal-footer" style="display: flex; gap: 12px; justify-content: flex-end;">
            <button class="modal-btn-cancel" style="
                padding: 10px 24px;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
                background: var(--bg-input);
                color: var(--text-main);
                border: 1px solid var(--border);
            ">
                ${escapeHtml(cancelText)}
            </button>
            <button class="modal-btn-confirm" style="
                padding: 10px 24px;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
                background: ${dangerous ? '#ef4444' : 'var(--accent)'};
                color: white;
                border: none;
                box-shadow: 0 2px 8px ${dangerous ? 'rgba(239, 68, 68, 0.3)' : 'rgba(0, 0, 0, 0.2)'};
            ">
                ${escapeHtml(confirmText)}
            </button>
        </div>
    `;
    
    overlay.appendChild(modal);
    document.body.appendChild(overlay);
    

    // Get buttons
    const confirmBtn = modal.querySelector('.modal-btn-confirm');
    const cancelBtn = modal.querySelector('.modal-btn-cancel');
    
    // Add hover effects
    confirmBtn.addEventListener('mouseenter', () => {
        confirmBtn.style.transform = 'translateY(-2px)';
        confirmBtn.style.boxShadow = `0 4px 12px ${dangerous ? 'rgba(239, 68, 68, 0.4)' : 'rgba(0, 0, 0, 0.3)'}`;
    });
    confirmBtn.addEventListener('mouseleave', () => {
        confirmBtn.style.transform = 'translateY(0)';
        confirmBtn.style.boxShadow = `0 2px 8px ${dangerous ? 'rgba(239, 68, 68, 0.3)' : 'rgba(0, 0, 0, 0.2)'}`;
    });
    
    cancelBtn.addEventListener('mouseenter', () => {
        cancelBtn.style.background = 'var(--bg-card)';
        cancelBtn.style.transform = 'translateY(-2px)';
    });
    cancelBtn.addEventListener('mouseleave', () => {
        cancelBtn.style.background = 'var(--bg-input)';
        cancelBtn.style.transform = 'translateY(0)';
    });
    
    // Handle confirm
    confirmBtn.addEventListener('click', () => {
        closeModal();
        onConfirm();
    });
    
    // Handle cancel
    cancelBtn.addEventListener('click', () => {
        closeModal();
        onCancel();
    });
    
    // Close on overlay click
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
            closeModal();
            onCancel();
        }
    });
    
    // Close on Escape key
    const escapeHandler = (e) => {
        if (e.key === 'Escape') {
            closeModal();
            onCancel();
        }
    };
    document.addEventListener('keydown', escapeHandler);
    
    // Close modal function
    function closeModal() {
        document.removeEventListener('keydown', escapeHandler);
        overlay.style.animation = 'fadeOut 0.2s ease-out';
        modal.style.animation = 'slideDown 0.2s ease-out';
        setTimeout(() => {
            if (overlay.parentNode) {
                overlay.remove();
            }
        }, 200);
    }
    
    // Focus confirm button for keyboard accessibility
    setTimeout(() => confirmBtn.focus(), 100);
}

/**
 * Shows a simple alert dialog (non-blocking, prettier than window.alert)
 * @param {Object} options - Configuration options
 * @param {string} options.title - Dialog title
 * @param {string} options.message - Dialog message
 * @param {string} options.buttonText - Text for OK button (default: "OK")
 * @param {Function} options.onClose - Callback when closed (optional)
 */
function showAlertDialog(options) {
    const {
        title = 'Notice',
        message = '',
        buttonText = 'OK',
        onClose = () => {}
    } = options;
    
    showConfirmDialog({
        title,
        message,
        confirmText: buttonText,
        cancelText: null,
        onConfirm: onClose,
        dangerous: false
    });
    
    // Hide cancel button for alert
    const modal = document.querySelector('.modal-dialog');
    const cancelBtn = modal?.querySelector('.modal-btn-cancel');
    if (cancelBtn) {
        cancelBtn.style.display = 'none';
    }
}
