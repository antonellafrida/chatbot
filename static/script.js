
function enviarConsulta(frase) {
    let chatbox = document.getElementById("chatbox");
    
    chatbox.innerHTML += `<div class="user-msg">${frase}</div>`;
    procesarMensaje(frase);
}


function getBotResponse() {
    let input = document.getElementById("userInput");
    let msg = input.value.trim();
    
    if (msg === "") return;
    
    let chatbox = document.getElementById("chatbox");
    chatbox.innerHTML += `<div class="user-msg">${msg}</div>`;
    procesarMensaje(msg);
    input.value = ""; // Limpiar input
}


function procesarMensaje(msg) {
    
    let formData = new FormData();
    formData.append("msg", msg);

    fetch("/get", {
        method: "POST",
        body: new URLSearchParams(formData)
    })
    .then(response => response.json())
    .then(data => {
        let chatbox = document.getElementById("chatbox");
        
        chatbox.innerHTML += `<div class="bot-msg">${data.response}</div>`;
        
        
        chatbox.scrollTop = chatbox.scrollHeight;
    })
    .catch(error => {
        console.error("Error:", error);
    });
}