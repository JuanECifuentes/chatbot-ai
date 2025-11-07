// Chat Interface JavaScript
class ChatInterface {
    constructor() {
        this.currentConversationId = null;
        this.conversations = [];
        this.isLoading = false;
        
        this.elements = {
            messageInput: document.getElementById('message-input'),
            sendBtn: document.getElementById('send-btn'),
            messagesContainer: document.getElementById('messages-container'),
            conversationHistory: document.getElementById('conversation-history'),
            newChatBtn: document.getElementById('new-chat-btn'),
            welcomeMessage: document.getElementById('welcome-message')
        };
        
        this.init();
    }
    
    init() {
        this.attachEventListeners();
        this.loadConversations();
        this.adjustTextareaHeight();
    }
    
    // Get CSRF token from cookies
    getCsrfToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // Get headers with CSRF token
    getHeaders(includeContentType = true) {
        const headers = {
            'X-CSRFToken': this.getCsrfToken(),
        };
        if (includeContentType) {
            headers['Content-Type'] = 'application/json';
        }
        return headers;
    }
    
    attachEventListeners() {
        // Send button click
        this.elements.sendBtn.addEventListener('click', () => this.sendMessage());
        
        // Enter key to send (Shift+Enter for new line)
        this.elements.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Input validation
        this.elements.messageInput.addEventListener('input', () => {
            this.adjustTextareaHeight();
            this.toggleSendButton();
        });
        
        // New chat button
        this.elements.newChatBtn.addEventListener('click', () => this.startNewChat());
    }
    
    adjustTextareaHeight() {
        const textarea = this.elements.messageInput;
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
    }
    
    toggleSendButton() {
        const hasText = this.elements.messageInput.value.trim().length > 0;
        this.elements.sendBtn.disabled = !hasText || this.isLoading;
    }
    
    async loadConversations() {
        try {
            const response = await fetch('/api/chatbot/conversations/');
            if (!response.ok) throw new Error('Failed to load conversations');
            
            this.conversations = await response.json();
            this.renderConversationHistory();
        } catch (error) {
            console.error('Error loading conversations:', error);
            this.showError('Failed to load conversation history');
        }
    }
    
    renderConversationHistory() {
        const container = this.elements.conversationHistory;
        
        if (this.conversations.length === 0) {
            container.innerHTML = '<div class="empty-state">No conversations yet</div>';
            return;
        }
        
        container.innerHTML = this.conversations.map(conv => `
            <div class="conversation-item ${conv.id === this.currentConversationId ? 'active' : ''}" 
                 data-id="${conv.id}">
                <div class="conversation-title">${this.escapeHtml(conv.title)}</div>
                <div class="conversation-time">${this.formatDate(conv.updated_at)}</div>
            </div>
        `).join('');
        
        // Add click handlers
        container.querySelectorAll('.conversation-item').forEach(item => {
            item.addEventListener('click', () => {
                const convId = parseInt(item.dataset.id);
                this.loadConversation(convId);
            });
        });
    }
    
    async loadConversation(conversationId) {
        try {
            const response = await fetch(`/api/chatbot/conversations/${conversationId}/`);
            if (!response.ok) throw new Error('Failed to load conversation');
            
            const conversation = await response.json();
            this.currentConversationId = conversationId;
            
            // Update UI
            this.elements.welcomeMessage.style.display = 'none';
            this.renderMessages(conversation.messages);
            this.updateActiveConversation();
        } catch (error) {
            console.error('Error loading conversation:', error);
            this.showError('Failed to load conversation');
        }
    }
    
    renderMessages(messages) {
        this.elements.messagesContainer.innerHTML = '';
        
        messages.forEach(msg => {
            this.appendMessage(msg.content, msg.sender === 'user' ? 'user' : 'assistant', false);
        });
        
        this.scrollToBottom();
    }
    
    appendMessage(content, sender, animate = true) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        if (!animate) messageDiv.style.animation = 'none';
        
        const avatarIcon = sender === 'user' 
            ? '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>'
            : '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>';
        
        messageDiv.innerHTML = `
            <div class="message-avatar">${avatarIcon}</div>
            <div class="message-content">${this.formatMessageContent(content)}</div>
        `;
        
        this.elements.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    showLoadingMessage() {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'loading-message';
        loadingDiv.id = 'loading-indicator';
        loadingDiv.innerHTML = `
            <div class="message-avatar">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                </svg>
            </div>
            <div class="message-content">
                <div class="loading-dots">
                    <div class="loading-dot"></div>
                    <div class="loading-dot"></div>
                    <div class="loading-dot"></div>
                </div>
            </div>
        `;
        
        this.elements.messagesContainer.appendChild(loadingDiv);
        this.scrollToBottom();
    }
    
    hideLoadingMessage() {
        const loadingDiv = document.getElementById('loading-indicator');
        if (loadingDiv) {
            loadingDiv.remove();
        }
    }
    
    async sendMessage() {
        const message = this.elements.messageInput.value.trim();
        if (!message || this.isLoading) return;
        
        this.isLoading = true;
        this.elements.sendBtn.disabled = true;
        
        // Hide welcome message
        this.elements.welcomeMessage.style.display = 'none';
        
        // Display user message
        this.appendMessage(message, 'user');
        
        // Clear input
        this.elements.messageInput.value = '';
        this.adjustTextareaHeight();
        
        // Show loading indicator
        this.showLoadingMessage();
        
        try {
            const response = await fetch('/api/chatbot/chat/send_message/', {
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify({
                    message: message,
                    conversation_id: this.currentConversationId,
                    top_k: 5
                })
            });
            
            if (!response.ok) {
                throw new Error('Failed to send message');
            }
            
            const data = await response.json();
            
            // Hide loading
            this.hideLoadingMessage();
            
            // Update current conversation ID if new
            if (!this.currentConversationId) {
                this.currentConversationId = data.conversation_id;
                await this.loadConversations();
            }
            
            // Display assistant response
            this.appendMessage(data.response.content, 'assistant');
            
            // Update conversation list
            this.updateActiveConversation();
            
        } catch (error) {
            console.error('Error sending message:', error);
            this.hideLoadingMessage();
            this.showError('Failed to send message. Please try again.');
        } finally {
            this.isLoading = false;
            this.toggleSendButton();
        }
    }
    
    startNewChat() {
        this.currentConversationId = null;
        this.elements.messagesContainer.innerHTML = '';
        this.elements.welcomeMessage.style.display = 'flex';
        this.updateActiveConversation();
        this.elements.messageInput.focus();
    }
    
    updateActiveConversation() {
        document.querySelectorAll('.conversation-item').forEach(item => {
            const convId = parseInt(item.dataset.id);
            if (convId === this.currentConversationId) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
    }
    
    formatMessageContent(content) {
        // Escape HTML and convert newlines to <br>
        content = this.escapeHtml(content);
        
        // Convert markdown-style formatting
        content = content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>');
        
        // Convert newlines to paragraphs
        const paragraphs = content.split('\n\n');
        return paragraphs.map(p => `<p>${p.replace(/\n/g, '<br>')}</p>`).join('');
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    formatDate(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMs / 3600000);
        const diffDays = Math.floor(diffMs / 86400000);
        
        if (diffMins < 1) return 'Just now';
        if (diffMins < 60) return `${diffMins}m ago`;
        if (diffHours < 24) return `${diffHours}h ago`;
        if (diffDays < 7) return `${diffDays}d ago`;
        
        return date.toLocaleDateString();
    }
    
    scrollToBottom() {
        setTimeout(() => {
            this.elements.messagesContainer.scrollTop = this.elements.messagesContainer.scrollHeight;
        }, 100);
    }
    
    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        
        this.elements.messagesContainer.appendChild(errorDiv);
        this.scrollToBottom();
        
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }
}

// Initialize chat interface when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatInterface();
});
