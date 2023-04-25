function showMessage() {
    let message = document.getElementById("fadedMessage");
    let textArea = document.getElementById("textInput");
    let integerInput = document.getElementById("integerInput");
    if (textArea.value && integerInput.value) {
        message.classList.remove("fade");
    }
    
}