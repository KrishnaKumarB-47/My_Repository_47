/**
 * Chatbot JavaScript for Artisan Marketplace
 * Handles chat interactions, message display, and API communication
 */

class ChatbotInterface {
    constructor() {
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatMessages = document.getElementById('chatMessages');
        this.charCount = document.getElementById('charCount');
        this.aiStatus = document.getElementById('aiStatus');
        this.loadingOverlay = document.getElementById('loadingOverlay');
        
        this.isLoading = false;
        this.messageHistory = [];
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.updateCharCount();
        this.scrollToBottom();
    }
    
    setupEventListeners() {
        // Send button click
        this.sendButton.addEventListener('click', () => this.sendMessage());
        
        // Enter key press
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Character count update
        this.messageInput.addEventListener('input', () => {
            this.updateCharCount();
            this.toggleSendButton();
        });
        
        // Auto-resize textarea if needed (for future enhancement)
        this.messageInput.addEventListener('input', () => {
            this.autoResize();
        });
    }
    
    updateCharCount() {
        const count = this.messageInput.value.length;
        this.charCount.textContent = `${count}/500`;
        
        if (count > 450) {
            this.charCount.style.color = '#dc3545';
        } else if (count > 400) {
            this.charCount.style.color = '#ffc107';
        } else {
            this.charCount.style.color = '#6c757d';
        }
    }
    
    toggleSendButton() {
        const hasText = this.messageInput.value.trim().length > 0;
        this.sendButton.disabled = !hasText || this.isLoading;
    }
    
    autoResize() {
        // Future enhancement: auto-resize input if using textarea
        // For now, keeping as single line input
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        
        if (!message || this.isLoading) {
            return;
        }
        
        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Clear input and update UI
        this.messageInput.value = '';
        this.updateCharCount();
        this.toggleSendButton();
        
        // Show loading state
        this.setLoadingState(true);
        this.addTypingIndicator();
        
        try {
            const response = await this.callChatAPI(message);
            
            // Remove typing indicator
            this.removeTypingIndicator();
            
            if (response.success) {
                this.addMessage(response.message, 'bot');
            } else {
                this.addMessage(response.message || 'Sorry, I encountered an error. Please try again.', 'bot');
            }
            
        } catch (error) {
            console.error('Chat API error:', error);
            this.removeTypingIndicator();
            this.addMessage('Sorry, I\'m having trouble connecting. Please check your internet connection and try again.', 'bot');
        } finally {
            this.setLoadingState(false);
            this.messageInput.focus();
        }
    }
    
    sendQuickMessage(message) {
        this.messageInput.value = message;
        this.updateCharCount();
        this.toggleSendButton();
        this.sendMessage();
    }
    
    async callChatAPI(message) {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    }
    
    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = sender === 'bot' ? '<i class="fas fa-robot"></i>' : '<i class="fas fa-user"></i>';
        
        const content = document.createElement('div');
        content.className = 'message-content';
        
        const messageText = document.createElement('div');
        messageText.className = 'message-text';
        messageText.innerHTML = this.formatMessage(text);
        
        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = new Date().toLocaleTimeString();
        
        content.appendChild(messageText);
        content.appendChild(messageTime);
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
        
        this.chatMessages.appendChild(messageDiv);
        
        // Store in history
        this.messageHistory.push({
            text: text,
            sender: sender,
            timestamp: new Date().toISOString()
        });
        
        // Scroll to bottom
        this.scrollToBottom();
        
        // Keep only last 50 messages in DOM for performance
        this.cleanupOldMessages();
    }
    
    formatMessage(text) {
        // Convert line breaks to <br>
        text = text.replace(/\n/g, '<br>');
        
        // Convert URLs to links
        text = text.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>');
        
        // Convert **bold** to <strong>
        text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // Convert *italic* to <em>
        text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
        
        return text;
    }
    
    addTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message typing-indicator';
        typingDiv.id = 'typingIndicator';
        
        typingDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                <div class="message-text">
                    <div class="typing-indicator">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </div>
            </div>
        `;
        
        this.chatMessages.appendChild(typingDiv);
        this.scrollToBottom();
    }
    
    removeTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    setLoadingState(loading) {
        this.isLoading = loading;
        this.toggleSendButton();
        
        if (loading) {
            this.aiStatus.innerHTML = '<i class="fas fa-circle"></i> AI is thinking...';
            this.aiStatus.className = 'ai-status thinking';
        } else {
            this.aiStatus.innerHTML = '<i class="fas fa-circle"></i> AI Assistant Ready';
            this.aiStatus.className = 'ai-status';
        }
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    cleanupOldMessages() {
        const messages = this.chatMessages.querySelectorAll('.message');
        if (messages.length > 50) {
            // Remove oldest messages (keep the welcome message)
            for (let i = 1; i < messages.length - 49; i++) {
                if (messages[i] && !messages[i].classList.contains('typing-indicator')) {
                    messages[i].remove();
                }
            }
        }
    }
    
    // Utility methods
    clearChat() {
        const messages = this.chatMessages.querySelectorAll('.message');
        messages.forEach(message => {
            if (!message.classList.contains('typing-indicator')) {
                message.remove();
            }
        });
        
        this.messageHistory = [];
        this.addMessage('Hello! I\'m your AI assistant for the Artisan Marketplace. How can I help you today?', 'bot');
    }
    
    exportChat() {
        const chatData = {
            timestamp: new Date().toISOString(),
            messages: this.messageHistory
        };
        
        const blob = new Blob([JSON.stringify(chatData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `chatbot-conversation-${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}

// Global functions for quick actions
function sendQuickMessage(message) {
    if (window.chatbot) {
        window.chatbot.sendQuickMessage(message);
    }
}

function sendMessage() {
    if (window.chatbot) {
        window.chatbot.sendMessage();
    }
}

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.chatbot = new ChatbotInterface();
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to send message
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            sendMessage();
        }
        
        // Escape to clear input
        if (e.key === 'Escape') {
            document.getElementById('messageInput').value = '';
            window.chatbot.updateCharCount();
            window.chatbot.toggleSendButton();
        }
    });
    
    // Add service worker registration for offline support (future enhancement)
    if ('serviceWorker' in navigator) {
        // Service worker registration can be added here
        console.log('Service Worker support detected');
    }
});

// Error handling for unhandled promises
window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
    
    if (window.chatbot) {
        window.chatbot.removeTypingIndicator();
        window.chatbot.setLoadingState(false);
        window.chatbot.addMessage('Sorry, I encountered an unexpected error. Please try again.', 'bot');
    }
});

// Performance monitoring
if ('performance' in window) {
    window.addEventListener('load', function() {
        const loadTime = performance.now();
        console.log(`Chatbot loaded in ${loadTime.toFixed(2)}ms`);
    });
}
