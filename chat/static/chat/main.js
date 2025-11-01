(() => {
  const form = document.getElementById('chat-form');
  const input = document.getElementById('message-input');
  const messages = document.getElementById('messages');

  function appendMessage(text, cls='bot'){
    const el = document.createElement('div');
    el.className = 'msg ' + (cls === 'user' ? 'user' : 'bot');
    const bubble = document.createElement('div');
    bubble.className = 'bubble ' + (cls === 'user' ? 'user' : 'bot');
    bubble.textContent = text;
    el.appendChild(bubble);
    messages.appendChild(el);
    messages.scrollTop = messages.scrollHeight;
  }

  async function sendMessage(text){
    appendMessage(text, 'user');
    appendMessage('...', 'bot');

    try{
      const res = await fetch('/api/chat/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: text})
      });
      const data = await res.json();
      // remove the temporary '...' bot message
      const last = messages.querySelectorAll('.msg');
      if(last.length) last[last.length-1].remove();
      appendMessage(data.reply || data.error || 'No response', 'bot');
    }catch(e){
      const last = messages.querySelectorAll('.msg');
      if(last.length) last[last.length-1].remove();
      appendMessage('Network error: ' + String(e), 'bot');
    }
  }

  form.addEventListener('submit', (ev) => {
    ev.preventDefault();
    const v = input.value.trim();
    if(!v) return;
    input.value = '';
    sendMessage(v);
  });

  // small quick demo welcome
  appendMessage('Hello! This is a local demo frontend. Type a message and it will be echoed by a mock backend.', 'bot');
})();
