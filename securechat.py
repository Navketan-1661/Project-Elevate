<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Chat App</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f3f4f6;
        }
        .modal {
            display: none;
            position: fixed;
            z-index: 100;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.4);
            justify-content: center;
            align-items: center;
        }
        .modal-content {
            background-color: #fff;
            margin: auto;
            padding: 20px;
            border-radius: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            max-width: 500px;
            width: 90%;
            animation-name: animatetop;
            animation-duration: 0.4s
        }
        @keyframes animatetop {
            from {top:-300px; opacity:0}
            to {top:0; opacity:1}
        }
        .close-button {
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
        }
        .close-button:hover,
        .close-button:focus {
            color: black;
            text-decoration: none;
            cursor: pointer;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-radius: 50%;
            border-top: 4px solid #3498db;
            width: 20px;
            height: 20px;
            -webkit-animation: spin 2s linear infinite;
            animation: spin 2s linear infinite;
        }
        @-webkit-keyframes spin {
            0% { -webkit-transform: rotate(0deg); }
            100% { -webkit-transform: rotate(360deg); }
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body class="flex items-center justify-center min-h-screen">

    <div id="app" class="bg-white p-8 rounded-2xl shadow-xl w-full max-w-4xl flex flex-col md:flex-row space-y-8 md:space-y-0 md:space-x-8">

        <!-- User and Online Status Section -->
        <div class="w-full md:w-1/3 p-4 bg-gray-50 rounded-xl">
            <h2 class="text-2xl font-bold text-gray-800 mb-4">Secure Chat</h2>
            
            <div id="login-container" class="space-y-4">
                <input type="text" id="username-input" placeholder="Choose a username" class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                <button id="join-button" class="w-full p-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors">Join Chat</button>
            </div>

            <div id="user-info" class="hidden mt-6">
                <h3 class="text-xl font-semibold text-gray-700">My Public Key</h3>
                <textarea id="my-public-key" rows="5" readonly class="w-full mt-2 p-2 text-xs bg-gray-100 border border-gray-200 rounded-lg font-mono overflow-auto resize-none"></textarea>
                <div class="mt-4">
                    <h3 class="text-xl font-semibold text-gray-700">Online Users</h3>
                    <ul id="online-users-list" class="mt-2 space-y-1">
                        <!-- Online users will be dynamically added here -->
                    </ul>
                </div>
            </div>
        </div>
        
        <!-- Chat Interface Section -->
        <div id="chat-container" class="hidden w-full md:w-2/3 flex flex-col h-[500px] bg-gray-50 rounded-xl p-4">
            <div id="messages" class="flex-1 overflow-y-auto p-2 bg-white rounded-lg border border-gray-200">
                <div class="text-center text-gray-400 p-4">Choose a user from the left to start a private chat.</div>
            </div>
            <div class="mt-4 flex flex-col space-y-2">
                <textarea id="message-input" placeholder="Type your message..." rows="3" class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" disabled></textarea>
                <div class="flex flex-wrap items-center space-y-2 sm:space-y-0 sm:space-x-2">
                    <button id="rephrase-button" class="flex-1 p-3 bg-indigo-600 text-white rounded-lg font-semibold hover:bg-indigo-700 transition-colors" disabled>Rephrase Politely ✨</button>
                    <button id="continue-chat-button" class="flex-1 p-3 bg-green-600 text-white rounded-lg font-semibold hover:bg-green-700 transition-colors" disabled>Continue Chat ✨</button>
                    <button id="summarize-button" class="flex-1 p-3 bg-purple-600 text-white rounded-lg font-semibold hover:bg-purple-700 transition-colors" disabled>Summarize Chat ✨</button>
                    <div class="flex-1 flex space-x-2">
                        <select id="language-select" class="flex-1 p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" disabled>
                            <option value="es-US">Spanish</option>
                            <option value="fr-FR">French</option>
                            <option value="de-DE">German</option>
                            <option value="ja-JP">Japanese</option>
                            <option value="hi-IN">Hindi</option>
                            <option value="en-US">English</option>
                        </select>
                        <button id="translate-button" class="flex-1 p-3 bg-blue-400 text-white rounded-lg font-semibold hover:bg-blue-500 transition-colors" disabled>Translate ✨</button>
                    </div>
                    <button id="send-button" class="flex-1 p-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors" disabled>Send</button>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Custom Modal for LLM Suggestions -->
    <div id="llm-modal" class="modal">
      <div class="modal-content">
        <span class="close-button">&times;</span>
        <h3 id="modal-title" class="text-xl font-bold mb-4">Gemini's Suggestion</h3>
        <div id="modal-body" class="p-4 bg-gray-100 rounded-lg min-h-[50px] flex items-center justify-center text-center">
            <div id="spinner" class="spinner hidden"></div>
            <p id="suggestion-text" class="text-gray-700"></p>
        </div>
        <div class="mt-4 text-right">
            <button id="insert-suggestion" class="p-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors">Use This</button>
        </div>
      </div>
    </div>

    <script>
        const socket = io();
        const app = document.getElementById('app');
        const loginContainer = document.getElementById('login-container');
        const usernameInput = document.getElementById('username-input');
        const joinButton = document.getElementById('join-button');
        const chatContainer = document.getElementById('chat-container');
        const messageInput = document.getElementById('message-input');
        const sendButton = document.getElementById('send-button');
        const rephraseButton = document.getElementById('rephrase-button');
        const continueChatButton = document.getElementById('continue-chat-button');
        const summarizeButton = document.getElementById('summarize-button');
        const translateButton = document.getElementById('translate-button');
        const languageSelect = document.getElementById('language-select');
        const onlineUsersList = document.getElementById('online-users-list');
        const messagesContainer = document.getElementById('messages');
        const myPublicKeyTextarea = document.getElementById('my-public-key');
        const userInfoContainer = document.getElementById('user-info');
        const llmModal = document.getElementById('llm-modal');
        const modalBody = document.getElementById('modal-body');
        const closeButton = document.querySelector('.close-button');
        const insertSuggestionButton = document.getElementById('insert-suggestion');
        const suggestionText = document.getElementById('suggestion-text');
        const spinner = document.getElementById('spinner');
        const modalTitle = document.getElementById('modal-title');

        let myUsername = '';
        let myKey = null;
        let recipientUsername = null;
        let peerKeys = {};
        
        let sessionKeys = {};

        // Utility functions for base64 encoding/decoding
        const arrayBufferToBase64 = (buffer) => {
            let binary = '';
            const bytes = new Uint8Array(buffer);
            const len = bytes.byteLength;
            for (let i = 0; i < len; i++) {
                binary += String.fromCharCode(bytes[i]);
            }
            return window.btoa(binary);
        };
        const base64ToArrayBuffer = (base64) => {
            const binary_string = window.atob(base64);
            const len = binary_string.length;
            const bytes = new Uint8Array(len);
            for (let i = 0; i < len; i++) {
                bytes[i] = binary_string.charCodeAt(i);
            }
            return bytes.buffer;
        };
        const importKey = (pem) => {
            const pemHeader = "-----BEGIN PUBLIC KEY-----";
            const pemFooter = "-----END PUBLIC KEY-----";
            const pemContents = pem.substring(pemHeader.length, pem.length - pemFooter.length).trim();
            const binaryDerString = window.atob(pemContents);
            const binaryDer = base64ToArrayBuffer(pemContents);
            return window.crypto.subtle.importKey(
                "spki",
                binaryDer,
                {
                    name: "RSA-OAEP",
                    hash: { name: "SHA-256" }
                },
                true,
                ["encrypt"]
            );
        };

        const generateKeyPair = async () => {
            const keyPair = await window.crypto.subtle.generateKey(
                {
                    name: "RSA-OAEP",
                    modulusLength: 2048,
                    publicExponent: new Uint8Array([0x01, 0x00, 0x01]),
                    hash: { name: "SHA-256" },
                },
                true,
                ["encrypt", "decrypt"]
            );
            return keyPair;
        };

        const exportPublicKey = async (publicKey) => {
            const exported = await window.crypto.subtle.exportKey("spki", publicKey);
            const exportedAsString = arrayBufferToBase64(exported);
            const pem = `-----BEGIN PUBLIC KEY-----\n${exportedAsString}\n-----END PUBLIC KEY-----`;
            return pem;
        };

        const encryptWithPublicKey = async (publicKey, data) => {
            const encryptedData = await window.crypto.subtle.encrypt(
                { name: "RSA-OAEP" },
                publicKey,
                data
            );
            return arrayBufferToBase64(encryptedData);
        };

        const decryptWithPrivateKey = async (privateKey, data) => {
            const decryptedData = await window.crypto.subtle.decrypt(
                { name: "RSA-OAEP" },
                privateKey,
                data
            );
            return decryptedData;
        };
        
        const generateAESKey = async () => {
            return await window.crypto.subtle.generateKey(
                { name: "AES-GCM", length: 256 },
                true,
                ["encrypt", "decrypt"]
            );
        };

        const encryptMessage = async (key, message) => {
            const encodedMessage = new TextEncoder().encode(message);
            const iv = window.crypto.getRandomValues(new Uint8Array(12));
            const encryptedContent = await window.crypto.subtle.encrypt(
                { name: "AES-GCM", iv: iv },
                key,
                encodedMessage
            );
            const fullEncrypted = new Uint8Array(iv.length + encryptedContent.byteLength);
            fullEncrypted.set(iv);
            fullEncrypted.set(new Uint8Array(encryptedContent), iv.length);
            return arrayBufferToBase64(fullEncrypted);
        };

        const decryptMessage = async (key, encryptedData) => {
            const fullEncrypted = base64ToArrayBuffer(encryptedData);
            const iv = fullEncrypted.slice(0, 12);
            const ciphertext = fullEncrypted.slice(12);
            try {
                const decryptedData = await window.crypto.subtle.decrypt(
                    { name: "AES-GCM", iv: iv },
                    key,
                    ciphertext
                );
                return new TextDecoder().decode(decryptedData);
            } catch (e) {
                console.error("Decryption failed:", e);
                return null;
            }
        };

        // UI and Event Handlers
        joinButton.addEventListener('click', async () => {
            myUsername = usernameInput.value.trim();
            if (myUsername) {
                myKey = await generateKeyPair();
                const myPublicKeyPem = await exportPublicKey(myKey.publicKey);
                myPublicKeyTextarea.value = myPublicKeyPem;

                socket.emit('register_user', {
                    username: myUsername,
                    publicKey: myPublicKeyPem
                });

                loginContainer.classList.add('hidden');
                userInfoContainer.classList.remove('hidden');
                chatContainer.classList.remove('hidden');
                messageInput.disabled = false;
                sendButton.disabled = false;
                rephraseButton.disabled = false;
                continueChatButton.disabled = false;
                summarizeButton.disabled = false;
                languageSelect.disabled = false;
                translateButton.disabled = false;
                
                // Request public keys of other users
                socket.emit('get_public_keys');
            } else {
                // Using custom modal instead of alert()
                showCustomModal('Please enter a username.', 'Alert');
            }
        });

        onlineUsersList.addEventListener('click', (event) => {
            if (event.target.tagName === 'LI' && event.target.dataset.username) {
                recipientUsername = event.target.dataset.username;
                const userElements = onlineUsersList.querySelectorAll('li');
                userElements.forEach(el => el.classList.remove('bg-blue-200'));
                event.target.classList.add('bg-blue-200');
                messagesContainer.innerHTML = `<div class="text-center text-gray-400 p-4">You are now chatting with <span class="font-bold text-gray-700">${recipientUsername}</span>.</div>`;
            }
        });
        
        sendButton.addEventListener('click', async () => {
            const message = messageInput.value;
            if (message && recipientUsername) {
                // Ensure recipient's public key is available
                if (!peerKeys[recipientUsername]) {
                    showCustomModal('Recipient public key not found. Please wait or refresh.', 'Error');
                    return;
                }
                
                let aesKey;
                let encryptedAesKey;

                // Check if a session key already exists for this recipient
                if (sessionKeys[recipientUsername]) {
                    aesKey = sessionKeys[recipientUsername];
                    // No need to re-encrypt the key, just send the message
                    encryptedAesKey = null; 
                } else {
                    // Generate a new AES key for the session
                    aesKey = await generateAESKey();
                    sessionKeys[recipientUsername] = aesKey;
                    
                    // Export AES key and encrypt it with recipient's public key
                    const exportedAesKey = await window.crypto.subtle.exportKey("raw", aesKey);
                    const peerPublicKey = await importKey(peerKeys[recipientUsername]);
                    encryptedAesKey = await encryptWithPublicKey(peerPublicKey, exportedAesKey);
                }

                // Encrypt the message with the AES key
                const encryptedMessage = await encryptMessage(aesKey, message);
                
                socket.emit('send_message', {
                    sender: myUsername,
                    recipient: recipientUsername,
                    encryptedMessage: encryptedMessage,
                    encryptedAESKey: encryptedAesKey, // Only sent the first time
                    timestamp: new Date().toISOString()
                });
                
                appendMessage(myUsername, message, 'self');
                messageInput.value = '';
            }
        });

        // Gemini API calls
        rephraseButton.addEventListener('click', async () => {
            const message = messageInput.value.trim();
            if (message) {
                await callGeminiApi('Rephrase the following text to be more polite, concise, and professional.', message, 'insert');
            } else {
                showCustomModal('Please type a message to rephrase.', 'Alert');
            }
        });

        continueChatButton.addEventListener('click', async () => {
            const allMessages = messagesContainer.querySelectorAll('div');
            const lastMessageElement = allMessages[allMessages.length - 1];
            if (lastMessageElement) {
                const lastMessage = lastMessageElement.textContent.trim();
                await callGeminiApi('Based on the previous chat message, provide a polite and engaging suggestion for how to continue the conversation.', lastMessage, 'insert');
            } else {
                showCustomModal('No messages to continue from. Start a conversation first!', 'Alert');
            }
        });

        summarizeButton.addEventListener('click', async () => {
            const allMessages = messagesContainer.querySelectorAll('div');
            if (allMessages.length > 1) {
                let conversation = '';
                allMessages.forEach(msgDiv => {
                    const sender = msgDiv.querySelector('.font-semibold')?.textContent;
                    const text = msgDiv.textContent;
                    conversation += `${sender || myUsername}: ${text}\n`;
                });
                await callGeminiApi('Summarize the following conversation in a single concise paragraph.', conversation, 'display');
            } else {
                showCustomModal('No conversation to summarize. Send or receive some messages first!', 'Alert');
            }
        });

        translateButton.addEventListener('click', async () => {
            const message = messageInput.value.trim();
            const language = languageSelect.options[languageSelect.selectedIndex].text;
            if (message) {
                await callGeminiApi(`Translate the following text into ${language}.`, message, 'insert');
            } else {
                showCustomModal('Please type a message to translate.', 'Alert');
            }
        });

        async function callGeminiApi(systemPrompt, userQuery, actionType) {
            suggestionText.textContent = '';
            spinner.classList.remove('hidden');
            llmModal.style.display = 'flex';
            modalTitle.textContent = actionType === 'display' ? 'Gemini Summary' : 'Gemini\'s Suggestion';
            insertSuggestionButton.style.display = actionType === 'insert' ? 'inline-block' : 'none';

            const apiKey = "";
            const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key=${apiKey}`;

            const payload = {
                contents: [{ parts: [{ text: userQuery }] }],
                systemInstruction: { parts: [{ text: systemPrompt }] },
            };

            let response;
            try {
                response = await fetch(apiUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                if (!response.ok) throw new Error(`API response was not ok: ${response.status}`);
                const result = await response.json();
                const text = result?.candidates?.[0]?.content?.parts?.[0]?.text;
                if (text) {
                    suggestionText.textContent = text;
                    if (actionType === 'insert') {
                        insertSuggestionButton.style.display = 'inline-block';
                    } else {
                        insertSuggestionButton.style.display = 'none';
                    }
                } else {
                    suggestionText.textContent = 'Could not generate a suggestion. Please try again.';
                    insertSuggestionButton.style.display = 'none';
                }
            } catch (error) {
                console.error("Gemini API call failed:", error);
                suggestionText.textContent = 'Failed to get a suggestion. Check the console for details.';
                insertSuggestionButton.style.display = 'none';
            } finally {
                spinner.classList.add('hidden');
            }
        }

        insertSuggestionButton.addEventListener('click', () => {
            messageInput.value = suggestionText.textContent;
            llmModal.style.display = 'none';
        });

        closeButton.addEventListener('click', () => {
            llmModal.style.display = 'none';
        });

        window.onclick = function(event) {
            if (event.target == llmModal) {
                llmModal.style.display = 'none';
            }
        }
        
        function showCustomModal(message, title) {
            suggestionText.textContent = message;
            modalTitle.textContent = title;
            spinner.classList.add('hidden');
            insertSuggestionButton.style.display = 'none';
            llmModal.style.display = 'flex';
        }


        function appendMessage(sender, text, type) {
            const messageElement = document.createElement('div');
            messageElement.classList.add('p-3', 'rounded-lg', 'mb-2');
            
            if (type === 'self') {
                messageElement.classList.add('bg-blue-500', 'text-white', 'self-end', 'text-right', 'ml-auto');
                messageElement.innerHTML = `<div class="text-xs text-blue-200">From: You, To: ${recipientUsername}</div><div>${text}</div>`;
            } else {
                messageElement.classList.add('bg-gray-200', 'text-gray-800', 'self-start');
                messageElement.innerHTML = `<div class="text-xs text-gray-500">From: ${sender}, To: You</div><div>${text}</div>`;
            }
            
            messagesContainer.appendChild(messageElement);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        // Socket.IO event listeners
        socket.on('online_users', (users) => {
            onlineUsersList.innerHTML = '';
            users.forEach(user => {
                if (user !== myUsername) {
                    const li = document.createElement('li');
                    li.textContent = user;
                    li.dataset.username = user;
                    li.classList.add('p-2', 'rounded-lg', 'cursor-pointer', 'hover:bg-gray-200', 'transition-colors');
                    onlineUsersList.appendChild(li);
                }
            });
        });

        socket.on('public_keys_list', (keys) => {
            peerKeys = keys;
            console.log('Received public keys:', peerKeys);
        });

        socket.on('receive_message', async (data) => {
            const sender = data.sender;
            
            // Only process messages for this user
            if (data.recipient !== myUsername) return;

            // If encryptedAESKey is present, it's the first message from this sender
            if (data.encryptedAESKey) {
                const encryptedKeyBuffer = base64ToArrayBuffer(data.encryptedAESKey);
                const decryptedKeyBuffer = await decryptWithPrivateKey(myKey.privateKey, encryptedKeyBuffer);
                
                // Import the decrypted AES key
                const aesKey = await window.crypto.subtle.importKey(
                    "raw",
                    decryptedKeyBuffer,
                    { name: "AES-GCM" },
                    true,
                    ["encrypt", "decrypt"]
                );
                sessionKeys[sender] = aesKey;
            }
            
            // Decrypt the message
            if (sessionKeys[sender]) {
                const decryptedMessage = await decryptMessage(sessionKeys[sender], data.encryptedMessage);
                if (decryptedMessage !== null) {
                    // Only display if the chat is with the current sender
                    if (recipientUsername === sender) {
                        appendMessage(sender, decryptedMessage, 'other');
                    }
                }
            } else {
                 console.error("No session key found for sender:", sender);
            }
        });
        
    </script>
</body>
</html>
