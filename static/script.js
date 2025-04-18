function stopSpeaking() {
    fetch('/stop', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            addMessage("You", "🛑 Stopped Bunny");
            addMessage("Bunny", data.reply);
        });
}

function addMessage(sender, message) {
    const chatbox = document.getElementById("chatbox");
    const newMsg = document.createElement("div");
    newMsg.classList.add("message");
    newMsg.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatbox.appendChild(newMsg);
    chatbox.scrollTop = chatbox.scrollHeight;
}

function clearChat() {
    document.getElementById("chatbox").innerHTML = "";
}

function sendMessage() {
    const userInput = document.getElementById("userInput");
    const message = userInput.value.trim();
    if (!message) return;

    addMessage("You", message);
    fetch('/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
    })
    .then(res => res.json())
    .then(data => {
        addMessage("Bunny", data.reply);
        userInput.value = "";
    });
}

function startMic() {
    addMessage("You (Mic)", "🎙️ Listening...");
    fetch('/mic')
        .then(res => res.json())
        .then(data => {
            addMessage("You", data.user);
            addMessage("Bunny", data.reply);
        });
}
