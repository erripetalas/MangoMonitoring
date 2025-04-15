// Text-to-Speech Functionality
document.addEventListener("DOMContentLoaded", () => {
    const ttsButton = document.getElementById("tts-button");
    const languageSelector = document.getElementById("language-selector");

    // Create the Stop Reading button
    const stopButton = document.createElement("button");
    stopButton.id = "stop-button";
    stopButton.textContent = "⏹ Stop Reading";
    stopButton.style.display = "none"; // Initially hidden
    document.getElementById("tts-container").appendChild(stopButton); // Append to the TTS container

    let utterance = null;

    ttsButton.addEventListener("click", () => {
        const selectedText = window.getSelection().toString().trim();
        const content = selectedText || document.body.innerText; // Use selected text or fallback to full page text

        if (utterance) {
            window.speechSynthesis.cancel(); // Cancel any ongoing speech
        }

        utterance = new SpeechSynthesisUtterance(content);

        // Set voice and speech properties
        utterance.lang = languageSelector.value; // Use selected language
        utterance.rate = 1; // Set speed (1 is normal)
        utterance.pitch = 1; // Set pitch (1 is normal)

        // Show stop button while speaking
        stopButton.style.display = "inline-block";

        // Speak the text
        window.speechSynthesis.speak(utterance);

        // Hide stop button when speech ends
        utterance.onend = () => {
            stopButton.style.display = "none";
        };

        utterance.onerror = (e) => {
            console.error("Speech synthesis error:", e);
            stopButton.style.display = "none"; // Hide stop button on error
        };
    });

    stopButton.addEventListener("click", () => {
        if (utterance) {
            window.speechSynthesis.cancel(); // Stop the speech
            stopButton.style.display = "none"; // Hide stop button
        }
    });
});