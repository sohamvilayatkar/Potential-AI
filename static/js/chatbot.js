/**
 * POTENTIAL AI - Intelligent College Assistant Chatbot
 * Interactive Chat Interface with Native Web Speech API:
 *  - Speech-to-Text (STT / Voice Input via SpeechRecognition)
 *  - Text-to-Speech (TTS / Read Aloud via SpeechSynthesis)
 *  - Grounded College Source Attribution & Explainable AI Details
 */

// Global State
let recognition = null;
let isListening = false;
let autoSpeakEnabled = false;
let currentUtterance = null;
let activeSpeakBtn = null;
let availableVoices = [];
let speechResumeInterval = null;

// Browser Feature Detection
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const isSTTSupported = !!SpeechRecognition;
const isTTSSupported = 'speechSynthesis' in window && 'SpeechSynthesisUtterance' in window;

document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('userInput');
    const clearBtn = document.getElementById('clearChatBtn');
    const voiceToggleBtn = document.getElementById('voiceAutoSpeakBtn');
    const micBtn = document.getElementById('micBtn');

    if (userInput) {
        userInput.focus();
    }

    // 1. Initialize Auto-Speak Preference
    initAutoSpeakState();

    if (voiceToggleBtn) {
        voiceToggleBtn.addEventListener('click', toggleAutoSpeak);
    }

    // 2. Initialize Voices for TTS
    if (isTTSSupported) {
        loadSpeechVoices();
        if (window.speechSynthesis.onvoiceschanged !== undefined) {
            window.speechSynthesis.onvoiceschanged = loadSpeechVoices;
        }
    }

    // 3. Initialize STT Recognition Engine
    if (isSTTSupported) {
        initSpeechRecognition();
    } else if (micBtn) {
        micBtn.title = "Speech-to-Text is not supported in this browser (Use Chrome or Edge)";
        micBtn.classList.add('disabled');
    }

    // 4. Clear Chat Handler
    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            stopAllSpeech();
            const chatMessages = document.getElementById('chatMessages');
            if (chatMessages) {
                chatMessages.innerHTML = `
                    <div class="message bot">
                        <div class="avatar bot-avatar">Ψ</div>
                        <div class="message-bubble">
                            <p><strong>Conversation cleared.</strong> How else may I assist you with PRPCEM information?</p>
                            <div class="message-footer">
                                <button type="button" class="btn-speak" title="Read message aloud" onclick="toggleSpeakMessage(this)">
                                    <span class="speak-icon">🔊</span>
                                    <span class="speak-text">Listen</span>
                                </button>
                                <div class="timestamp">Just now</div>
                            </div>
                        </div>
                    </div>
                `;
            }
        });
    }
});

/* ==========================================================================
   SPEECH-TO-TEXT (STT) - VOICE RECOGNITION
   ========================================================================== */

function initSpeechRecognition() {
    try {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.maxAlternatives = 1;

        // Prefer Indian English or user browser locale
        recognition.lang = navigator.language || 'en-IN';

        recognition.onstart = () => {
            isListening = true;
            stopAllSpeech(); // Mute bot if it was speaking

            const micBtn = document.getElementById('micBtn');
            const banner = document.getElementById('voiceStatusBanner');
            const msg = document.getElementById('voiceStatusMessage');

            if (micBtn) micBtn.classList.add('listening');
            if (banner) banner.classList.remove('hidden');
            if (msg) msg.textContent = "Listening... Speak now into your microphone";
        };

        recognition.onresult = (event) => {
            const input = document.getElementById('userInput');
            let interimTranscript = '';
            let finalTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; ++i) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript;
                } else {
                    interimTranscript += transcript;
                }
            }

            if (input) {
                const liveText = finalTranscript || interimTranscript;
                if (liveText) {
                    input.value = liveText;
                }
            }

            const msg = document.getElementById('voiceStatusMessage');
            if (msg && interimTranscript) {
                msg.textContent = `"${interimTranscript}..."`;
            }

            // Auto-submit when speech is finalized
            if (finalTranscript && finalTranscript.trim()) {
                const form = document.getElementById('chatForm');
                if (form) {
                    setTimeout(() => {
                        stopVoiceRecognition();
                        form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
                    }, 400);
                }
            }
        };

        recognition.onerror = (event) => {
            console.warn('[STT Error]', event.error);
            const msg = document.getElementById('voiceStatusMessage');

            if (msg) {
                if (event.error === 'not-allowed') {
                    msg.textContent = "Microphone access was denied. Please allow microphone permissions.";
                } else if (event.error === 'no-speech') {
                    msg.textContent = "No voice detected. Tap mic and speak again.";
                } else if (event.error === 'network') {
                    msg.textContent = "Voice network service unavailable. Check your connection.";
                } else {
                    msg.textContent = `Voice recognition error: ${event.error}`;
                }
            }

            setTimeout(() => {
                cancelVoiceRecognition();
            }, 2500);
        };

        recognition.onend = () => {
            isListening = false;
            const micBtn = document.getElementById('micBtn');
            const banner = document.getElementById('voiceStatusBanner');

            if (micBtn) micBtn.classList.remove('listening');
            if (banner) banner.classList.add('hidden');
        };

    } catch (e) {
        console.error('Failed to initialize SpeechRecognition:', e);
    }
}

function toggleVoiceInput() {
    if (!isSTTSupported) {
        alert("Speech Recognition is not supported in this browser. Please use Google Chrome, Microsoft Edge, or Safari.");
        return;
    }

    if (isListening) {
        stopVoiceRecognition();
    } else {
        startVoiceRecognition();
    }
}

function startVoiceRecognition() {
    if (!recognition) return;
    try {
        recognition.start();
    } catch (err) {
        console.warn('Recognition start exception:', err);
    }
}

function stopVoiceRecognition() {
    if (!recognition) return;
    try {
        recognition.stop();
    } catch (err) {
        console.warn('Recognition stop exception:', err);
    }
}

function cancelVoiceRecognition() {
    if (!recognition) return;
    try {
        recognition.abort();
    } catch (err) {
        console.warn('Recognition abort exception:', err);
    }
    isListening = false;
    const micBtn = document.getElementById('micBtn');
    const banner = document.getElementById('voiceStatusBanner');
    if (micBtn) micBtn.classList.remove('listening');
    if (banner) banner.classList.add('hidden');
}

/* ==========================================================================
   TEXT-TO-SPEECH (TTS) - READ ALOUD ENGINE
   ========================================================================== */

function loadSpeechVoices() {
    if (!isTTSSupported) return;
    availableVoices = window.speechSynthesis.getVoices();
}

function getBestVoice() {
    if (!availableVoices || availableVoices.length === 0) {
        availableVoices = window.speechSynthesis.getVoices();
    }

    // Priority 1: Indian English natural voice
    let voice = availableVoices.find(v => v.lang === 'en-IN' && !v.name.includes('Fallback'));
    if (voice) return voice;

    // Priority 2: Natural / Online English voices
    voice = availableVoices.find(v => (v.lang.startsWith('en') && (v.name.includes('Natural') || v.name.includes('Google') || v.name.includes('Samantha') || v.name.includes('Daniel'))));
    if (voice) return voice;

    // Priority 3: Any English voice
    voice = availableVoices.find(v => v.lang.startsWith('en'));
    if (voice) return voice;

    return availableVoices[0] || null;
}

function initAutoSpeakState() {
    const saved = localStorage.getItem('potential_ai_auto_speak');
    autoSpeakEnabled = (saved === 'true');
    updateAutoSpeakButtonUI();
}

function toggleAutoSpeak() {
    autoSpeakEnabled = !autoSpeakEnabled;
    localStorage.setItem('potential_ai_auto_speak', autoSpeakEnabled ? 'true' : 'false');
    updateAutoSpeakButtonUI();

    if (!autoSpeakEnabled) {
        stopAllSpeech();
    }
}

function updateAutoSpeakButtonUI() {
    const icon = document.getElementById('voiceIcon');
    const label = document.getElementById('voiceStatusText');
    const btn = document.getElementById('voiceAutoSpeakBtn');

    if (btn && label && icon) {
        if (autoSpeakEnabled) {
            icon.textContent = '🔊';
            label.innerHTML = 'Auto-Speak: <strong>ON</strong>';
            btn.classList.add('active');
        } else {
            icon.textContent = '🔇';
            label.innerHTML = 'Auto-Speak: <strong>OFF</strong>';
            btn.classList.remove('active');
        }
    }
}

function cleanTextForSpeech(rawText) {
    if (!rawText) return '';
    let text = rawText;

    // Remove markdown links [Title](url) -> Title
    text = text.replace(/\[(.*?)\]\(https?:\/\/.*?\)/g, '$1');

    // Remove raw URLs
    text = text.replace(/https?:\/\/\S+/g, '');

    // Expand known acronyms for natural speech
    text = text.replace(/\bPRPCEM\b/g, 'P. R. Pote Patil College of Engineering and Management');
    text = text.replace(/\bSGBAU\b/g, 'Sant Gadge Baba Amravati University');
    text = text.replace(/\bHOD\b/g, 'Head of the Department');
    text = text.replace(/\bHODs\b/g, 'Heads of Departments');
    text = text.replace(/\bCSE\b/g, 'C S E');
    text = text.replace(/\bAIML\b/g, 'A I and M L');
    text = text.replace(/\bAI&DS\b/g, 'A I and Data Science');
    text = text.replace(/\bEXTC\b/g, 'Electronics and Telecommunication');
    text = text.replace(/\bME\b/g, 'Mechanical Engineering');
    text = text.replace(/\bCE\b/g, 'Civil Engineering');
    text = text.replace(/\bEE\b/g, 'Electrical Engineering');
    text = text.replace(/\bNAAC\b/g, 'NAAC');
    text = text.replace(/\bDTE\b/g, 'D T E');
    text = text.replace(/\bCAP\b/g, 'Centralized Admission Process');
    text = text.replace(/\bFRA\b/g, 'Fee Regulating Authority');
    text = text.replace(/\bEBC\b/g, 'Economically Backward Class');
    text = text.replace(/\bTFWS\b/g, 'Tuition Fee Waiver Scheme');

    // Strip markdown formatting symbols
    text = text.replace(/[#*_~`>]/g, ' ');
    text = text.replace(/•/g, '. ');
    text = text.replace(/[-]{2,}/g, ' ');

    // Strip HTML tags if present
    text = text.replace(/<[^>]*>/g, ' ');

    // Collapse multiple whitespaces and linebreaks
    text = text.replace(/\s+/g, ' ').trim();

    return text;
}

function toggleSpeakMessage(btnElement) {
    if (!isTTSSupported) {
        alert("Text-to-Speech is not supported in this browser.");
        return;
    }

    // If currently speaking this message, stop it
    if (activeSpeakBtn === btnElement && window.speechSynthesis.speaking) {
        stopAllSpeech();
        return;
    }

    // Stop any existing speech first
    stopAllSpeech();

    // Find the message bubble containing this button
    const bubble = btnElement.closest('.message-bubble');
    if (!bubble) return;

    // Get plain text of the message (excluding source box and AI details)
    let textToSpeak = '';
    const clonedBubble = bubble.cloneNode(true);
    
    // Remove source box, AI details, footer from clone
    const unwanted = clonedBubble.querySelectorAll('.source-box, .ai-details-box, .ai-details-toggle, .message-footer, .timestamp');
    unwanted.forEach(el => el.remove());

    textToSpeak = cleanTextForSpeech(clonedBubble.textContent || clonedBubble.innerText);
    if (!textToSpeak) return;

    speakUtterance(textToSpeak, btnElement);
}

function speakUtterance(text, btnElement = null) {
    if (!isTTSSupported || !text) return;

    stopAllSpeech();

    const utterance = new SpeechSynthesisUtterance(text);
    currentUtterance = utterance;

    const voice = getBestVoice();
    if (voice) {
        utterance.voice = voice;
    }

    utterance.rate = 1.0;
    utterance.pitch = 1.0;

    // UI Updates
    if (btnElement) {
        activeSpeakBtn = btnElement;
        btnElement.classList.add('speaking');
        btnElement.innerHTML = `
            <span class="speak-icon">⏹️</span>
            <span class="speak-text">Stop</span>
            <span class="sound-wave">
                <span></span><span></span><span></span>
            </span>
        `;
    }

    const stopHeaderBtn = document.getElementById('stopAllSpeechBtn');
    if (stopHeaderBtn) {
        stopHeaderBtn.classList.remove('hidden');
    }

    // Mitigation for Chrome 15s pause bug
    clearInterval(speechResumeInterval);
    speechResumeInterval = setInterval(() => {
        if (window.speechSynthesis.speaking && !window.speechSynthesis.paused) {
            window.speechSynthesis.pause();
            window.speechSynthesis.resume();
        } else {
            clearInterval(speechResumeInterval);
        }
    }, 10000);

    utterance.onend = () => {
        resetSpeakingUI();
    };

    utterance.onerror = (e) => {
        console.warn('[TTS Error]', e);
        resetSpeakingUI();
    };

    window.speechSynthesis.speak(utterance);
}

function stopAllSpeech() {
    clearInterval(speechResumeInterval);
    if (isTTSSupported && (window.speechSynthesis.speaking || window.speechSynthesis.pending)) {
        window.speechSynthesis.cancel();
    }
    resetSpeakingUI();
}

function resetSpeakingUI() {
    clearInterval(speechResumeInterval);

    if (activeSpeakBtn) {
        activeSpeakBtn.classList.remove('speaking');
        activeSpeakBtn.innerHTML = `
            <span class="speak-icon">🔊</span>
            <span class="speak-text">Listen</span>
        `;
        activeSpeakBtn = null;
    }

    const stopHeaderBtn = document.getElementById('stopAllSpeechBtn');
    if (stopHeaderBtn) {
        stopHeaderBtn.classList.add('hidden');
    }
}

/* ==========================================================================
   CHAT MESSAGING & NETWORKING
   ========================================================================== */

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

    // Stop listening if user hits send
    if (isListening) {
        stopVoiceRecognition();
    }

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
        const botMsgDiv = appendMessage('bot', data.response, data.sources, data.ai_details, data.academic_year);

        // 3. Auto-Speak if enabled
        if (autoSpeakEnabled && isTTSSupported && botMsgDiv) {
            const speakBtn = botMsgDiv.querySelector('.btn-speak');
            const cleanText = cleanTextForSpeech(data.response);
            speakUtterance(cleanText, speakBtn);
        }

    } catch (error) {
        console.error('Chat error:', error);
        removeTypingIndicator();
        appendMessage('bot', "A network error occurred while communicating with the AI service.");
    }
}

function appendMessage(sender, text, sources = [], aiDetails = null, academicYear = null) {
    const container = document.getElementById('chatMessages');
    if (!container) return null;

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
            <button type="button" class="ai-details-toggle" onclick="toggleAIDetails('${detailId}')">
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
                <div class="message-footer">
                    <button type="button" class="btn-speak" title="Read message aloud" onclick="toggleSpeakMessage(this)">
                        <span class="speak-icon">🔊</span>
                        <span class="speak-text">Listen</span>
                    </button>
                    <div class="timestamp">${timeStr}</div>
                </div>
            </div>
        `;
    }

    container.appendChild(msgDiv);
    container.scrollTop = container.scrollHeight;
    return msgDiv;
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
