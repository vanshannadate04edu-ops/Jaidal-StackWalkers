document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const errorMessage = document.getElementById('error-message');

    loginForm.addEventListener('submit', (event) => {
        // Prevent the form from reloading the page
        event.preventDefault();

        // Get the values from the input fields
        const username = event.target.username.value;
        const password = event.target.password.value;

        // --- NEW: General format validation rules using Regular Expressions ---
        // Username Rule: Must be 6-15 characters and contain both letters and numbers.
        const usernameRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,15}$/;
        // Password Rule: Must be at least 8 characters, with one uppercase letter, one lowercase letter, and one number.
        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/;

        // --- MODIFIED: The if/else condition now checks the format ---

        // 1. Check if the username format is valid
        if (!usernameRegex.test(username)) {
            errorMessage.textContent = 'Invalid username. Must be 6-15 characters and include letters and numbers.';
            return; // Stop the login attempt
        }
        
        // 2. Check if the password format is valid
        if (!passwordRegex.test(password)) {
            errorMessage.textContent = 'Invalid password. Must be 8+ characters with uppercase, lowercase, and a number.';
            return; // Stop the login attempt
        }

        // 3. If both formats are correct, the login is successful
        console.log('Login successful! Redirecting...');
        errorMessage.textContent = ''; // Clear any previous errors
        window.location.href = 'dashboard.html';
    });
});