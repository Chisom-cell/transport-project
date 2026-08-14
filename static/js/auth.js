function setupPasswordToggle(inputId, buttonId) {
    const passwordInput = document.getElementById(inputId);
    const toggleButton = document.getElementById(buttonId);
    
    if (!passwordInput || !toggleButton) return;

    const icon = toggleButton.querySelector("i");

    toggleButton.addEventListener("click", function () {
        const isHidden = passwordInput.type === "password";
        passwordInput.type = isHidden ? "text" : "password";
        
        if (icon) {
            icon.classList.toggle("fa-eye", !isHidden);
            icon.classList.toggle("fa-eye-slash", isHidden);
        }
        
        toggleButton.setAttribute("aria-label", isHidden ? "Hide password" : "Show password");
    });
}

document.addEventListener("DOMContentLoaded", function () {
    setupPasswordToggle("password", "togglePassword");
});