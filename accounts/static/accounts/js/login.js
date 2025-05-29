document.addEventListener('DOMContentLoaded', function() {
    // Animation du formulaire de login
    const authContainer = document.querySelector('.auth-container');
    if (authContainer) {
        authContainer.classList.add('loaded');
    }

    //Gestion des messages flash
    const messages = document.querySelector('.messages');
    if (messages) {
        setTimeout(() => {
            messages.style.opacity = '0';
            setTimeout(() => messages.remove(), 500);
        }, 3000);
    }

    // Effets d'interaction pour les champs de formulaire
    const formGroups = document.querySelectorAll('.form-group');
    formGroups.forEach(group => {
        const input = group.querySelector('input');
        const label = group.querySelector('label');
        
        input.addEventListener('focus', () => {
            label.classList.add('active');
        });
        
        input.addEventListener('blur', () => {
            if (!input.value) {
                label.classList.remove('active');
            }
        });

        // Initialisation pour les champs pré-remplis
        if (input.value) {
            label.classList.add('active');
        }
    });

    //Validation basique avant soumission
    const loginForm = document.getElementById('loginForm') || document.querySelector('.auth-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const username = this.querySelector('[name="username"]');
            const password = this.querySelector('[name="password"]');
            let isValid = true;

            if (!username.value.trim()) {
                username.parentElement.classList.add('error');
                isValid = false;
            }

            if (!password.value.trim()) {
                password.parentElement.classList.add('error');
                isValid = false;
            }

            if (!isValid) {
                e.preventDefault();
                // Ajouter un message d'erreur visuel
                const errorDisplay = this.querySelector('.form-error') || document.createElement('div');
                errorDisplay.className = 'form-error';
                errorDisplay.textContent = 'Please fill in all fields';
                if (!this.querySelector('.form-error')) {
                    this.prepend(errorDisplay);
                }
            }
        });

        // Supprimer les erreurs lors de la saisie
        const inputs = loginForm.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('input', () => {
                input.parentElement.classList.remove('error');
                const errorDisplay = loginForm.querySelector('.form-error');
                if (errorDisplay) {
                    errorDisplay.remove();
                }
            });
        });
    }

    //Effet de chargement pendant la soumission
    const submitButton = document.querySelector('.auth-btn');
    if (submitButton) {
        const originalText = submitButton.innerHTML;
        
        loginForm?.addEventListener('submit', function() {
            submitButton.innerHTML = `
                <span class="spinner"></span>
                Signing in...
            `;
            submitButton.disabled = true;
        });
    }
});