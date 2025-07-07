// Send message to backend and display response
function sendMessage() {
  const msgInput = document.getElementById('msg');
  const msg = msgInput.value.trim();
  if (!msg) return;

  fetch('/send', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: 'message=' + encodeURIComponent(msg)
  })
  .then(res => res.text())
  .then(reply => {
    const box = document.getElementById('chatbox');
    box.innerHTML += `<p><b>You:</b> ${msg}</p>`;
    box.innerHTML += `<p><b>Bot:</b> ${reply}</p>`;
    msgInput.value = '';
    box.scrollTop = box.scrollHeight;
  });
}

// Load previous chat history
function loadHistory() {
  fetch('/history')
    .then(res => res.json())
    .then(data => {
      const box = document.getElementById('chatbox');
      data.chats.forEach(chat => {
        box.innerHTML += `<p><b>You:</b> ${chat.message}</p>`;
        box.innerHTML += `<p><b>Bot:</b> ${chat.reply}</p>`;
      });
      box.scrollTop = box.scrollHeight;
    });
}

function sendMessage() {
const msgInput = document.getElementById('msg');
const msg = msgInput.value.trim();
if (!msg) return;

const chatBox = document.getElementById('chatbox');

// Show user's message
const userBubble = document.createElement('div');
userBubble.className = 'chat-bubble user';
userBubble.textContent = msg;
chatBox.appendChild(userBubble);
chatBox.scrollTop = chatBox.scrollHeight;

// Clear input
msgInput.value = '';

// Send to backend
fetch('/send', {
method: 'POST',
headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
body: 'message=' + encodeURIComponent(msg)
})
.then(res => res.text())
.then(reply => {
const botBubble = document.createElement('div');
botBubble.className = 'chat-bubble bot';
botBubble.textContent = reply;
chatBox.appendChild(botBubble);
chatBox.scrollTop = chatBox.scrollHeight;
});
}

// Load previous chat history
function loadHistory() {
fetch('/history')
.then(res => res.json())
.then(data => {
const chatBox = document.getElementById('chatbox');
chatBox.innerHTML = '';
data.chats.forEach(chat => {
const user = document.createElement('div');
user.className = 'chat-bubble user';
user.textContent = chat.message;
chatBox.appendChild(user);
    const bot = document.createElement('div');
    bot.className = 'chat-bubble bot';
    bot.textContent = chat.reply;
    chatBox.appendChild(bot);
  });
  chatBox.scrollTop = chatBox.scrollHeight;
});}

document.getElementById('clearBtn').addEventListener('click', function () {
      fetch('/clear', { method: 'GET' })
        .then(() => {
          chatBox.innerHTML = '';
        });
    });
