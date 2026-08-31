/**
 * POTENTIAL AI - Chatbot Interface Logic
 * Connects frontend message interface to POST /api/chat
 */

document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('userInput');
    const clearBtn = document.getElementById('clearChatBtn');

    if (userInput) {
        userInput.focus();
    }

    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            const chatMessages = document.getElementById('chatMessages');
            if (chatMessages) {
                chatMessages.innerHTML = `
                    <div class="message bot">
                        <div class="avatar bot-avatar">Ψ</div>
                        <div class="message-bubble">
                            <p><strong>Conversation cleared.</strong> How else may I assist you with PRPCEM information?</p>
                            <div class="timestamp">Just now</div>
                        </div>
                    </div>
                `;
            }
        });
    }
});

function sendPrompt(text) {
    const input = document.getElementById('userInput');
    if (input) {
        input.value = text;
        const form = document.getElementById('chatForm');
        if (form) {
            form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
        }
    }
}

async function handleChatSubmit(event) {
    event.preventDefault();
    const input = document.getElementById('userInput');
    const message = input.value.trim();
    if (!message) return;

    // 1. Append User Message
    appendMessage('user', message);
    input.value = '';

    // 2. Show Typing Indicator
    showTypingIndicator();

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });

        removeTypingIndicator();

        if (!response.ok) {
            appendMessage('bot', "I'm having trouble connecting to the server. Please try again in a moment.");
            return;
        }

        const data = await response.json();
        appendMessage('bot', data.response, data.sources, data.ai_details, data.academic_year);

    } catch (error) {
        console.error('Chat error:', error);
        removeTypingIndicator();
        appendMessage('bot', "A network error occurred while communicating with the AI service.");
    }
}

function appendMessage(sender, text, sources = [], aiDetails = null, academicYear = null) {
    const container = document.getElementById('chatMessages');
    if (!container) return;

    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}`;

    const now = new Date();
    const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    let formattedText = formatMarkdown(text);

    let sourcesHtml = '';
    if (sources && sources.length > 0) {
        sourcesHtml = `
            <div class="source-box">
                <div class="source-header">🔗 Official Source Attribution:</div>
                ${sources.map(s => `
                    <div>
                        <a href="${s.url}" target="_blank" rel="noopener noreferrer" class="source-link">
                            • ${s.title || s.url} ↗
                        </a>
                    </div>
                `).join('')}
                ${academicYear ? `<div style="font-size: 0.72rem; color: #94a3b8; margin-top: 0.25rem;">Academic Year: ${academicYear}</div>` : ''}
            </div>
        `;
    }

    let aiDetailsHtml = '';
    if (aiDetails && sender === 'bot') {
        const detailId = 'ai-detail-' + Math.random().toString(36).substr(2, 9);
        aiDetailsHtml = `
            <button class="ai-details-toggle" onclick="toggleAIDetails('${detailId}')">
                ⚡ View AI Reasoning Details
            </button>
            <div id="${detailId}" class="ai-details-box">
                <div><strong>Predicted Intent:</strong> ${aiDetails.intent} (Confidence: ${(aiDetails.confidence_score * 100).toFixed(1)}%)</div>
                <div><strong>Experta Rule:</strong> ${aiDetails.experta_rule}</div>
                <div><strong>Symbolic Action:</strong> ${aiDetails.reasoning_action}</div>
                <div><strong>Knowledge Engine:</strong> ${aiDetails.knowledge_engine}</div>
            </div>
        `;
    }

    if (sender === 'user') {
        msgDiv.innerHTML = `
            <div class="avatar user-avatar">You</div>
            <div class="message-bubble">
                <div>${escapeHTML(text)}</div>
                <div class="timestamp">${timeStr}</div>
            </div>
        `;
    } else {
        msgDiv.innerHTML = `
            <div class="avatar bot-avatar">Ψ</div>
            <div class="message-bubble">
                <div>${formattedText}</div>
                ${sourcesHtml}
                ${aiDetailsHtml}
                <div class="timestamp">${timeStr}</div>
            </div>
        `;
    }

    container.appendChild(msgDiv);
    container.scrollTop = container.scrollHeight;
}

function showTypingIndicator() {
    const container = document.getElementById('chatMessages');
    if (!container) return;

    const typingDiv = document.createElement('div');
    typingDiv.id = 'typingIndicator';
    typingDiv.className = 'message bot';
    typingDiv.innerHTML = `
        <div class="avatar bot-avatar">Ψ</div>
        <div class="typing-indicator">
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
        </div>
    `;
    container.appendChild(typingDiv);
    container.scrollTop = container.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

function toggleAIDetails(elementId) {
    const box = document.getElementById(elementId);
    if (box) {
        box.classList.toggle('show');
    }
}

function escapeHTML(str) {
    const p = document.createElement('p');
    p.textContent = str;
    return p.innerHTML;
}

function formatMarkdown(text) {
    if (!text) return '';
    let html = escapeHTML(text);

    // Headings
    html = html.replace(/### (.*?)(?:\n|$)/g, '<h3>$1</h3>');
    html = html.replace(/## (.*?)(?:\n|$)/g, '<h3>$1</h3>');

    // Bold text **text**
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Italic *text*
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');

    // Markdown links [title](url)
    html = html.replace(/\[(.*?)\]\((https?:\/\/.*?)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer" style="color: #38bdf8; text-decoration: underline;">$1</a>');

    // Bullet points
    html = html.replace(/(?:^|\n)[•\-*] (.*?)(?=(?:\n[•\-*] )|\n\n|$)/gs, (match) => {
        const items = match.trim().split(/\n[•\-*] /);
        const listItems = items.map(item => `<li>${item.replace(/^[•\-*] /, '')}</li>`).join('');
        return `<ul>${listItems}</ul>`;
    });

    // Paragraph breaks
    html = html.replace(/\n\n/g, '<br><br>');
    html = html.replace(/\n/g, '<br>');

    return html;
}
