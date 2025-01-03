document.addEventListener("DOMContentLoaded", function () {
        const form = document.getElementById("register-form");
        const passwordField = form.querySelector('input[name="password"]');
        const passwordError = document.getElementById("password-error");

        form.addEventListener("submit", function (event) {
            const password = passwordField.value;

            const isLongEnough = password.length >= 8;
            const hasUppercase = /[A-Z]/.test(password);

            if (!isLongEnough || !hasUppercase) {
                event.preventDefault();

                passwordError.style.display = "block";
            } else {
                passwordError.style.display = "none";
            }
        });
    });