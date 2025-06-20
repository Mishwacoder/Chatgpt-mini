document.addEventListener("DOMContentLoaded", () => {
    const typingForm = document.querySelector(".typing-form");
    const chatContainer = document.querySelector(".chat-list");
    const suggestions = document.querySelectorAll(".suggestion");
    const toggleThemeButton = document.querySelector("#theme-toggle-button");
    const deleteChatButton = document.querySelector("#delete-chat-button");
    const voiceButton = document.getElementById("voice-button");

    // Speech Recognition (Converting Speech to Text)
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    let isListening = false;

    recognition.onstart = () => {
        isListening = true;
        console.log("Speech recognition started...");
    };

    recognition.onend = () => {
        isListening = false;
        console.log("Speech recognition ended.");
    };

    voiceButton.addEventListener("click", () => {
        if (!isListening) {
            recognition.start();
        } else {
            console.warn("Speech recognition is already running.");
        }
    });

    // Chatbot API Request
    const generateAPIResponse = async (incomingMessageDiv) => {
        const textElement = incomingMessageDiv.querySelector(".text");

        try {
            const response = await fetch("/chatbot-response/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: userMessage }),
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.error || "Error fetching chatbot response");

            showTypingEffect(data.response, textElement, incomingMessageDiv);
        } catch (error) {
            textElement.innerText = "Error: " + error.message;
            textElement.parentElement.closest(".message").classList.add("error");
        } finally {
            incomingMessageDiv.classList.remove("loading");
        }
    };

});
