// Variables globales avec les URLs Django
window.DJANGO_URLS = {
    updatePreferences: "{% url 'accounts:update_preferences' %}",
    deactivateAccount: "{% url 'accounts:deactivate_account' %}",
    deleteAccount: "{% url 'accounts:delete_account' %}"
};

window.CSRF_TOKEN = "{{ csrf_token }}";

// Utilitaires
const Utils = {
    getCSRFToken() {
        return window.CSRF_TOKEN || document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;
    },

    showAlert(message, type = 'error') {
        alert(message);
    }
};

// Gestion du profil utilisateur
const ProfileManager = {
    init() {
        this.initFileUpload();
        this.initFormValidation();
        this.initTabNavigation();
        this.initFloatingLabels();
        this.initDateInput();
        this.initAutoAlerts();
    },

    initFileUpload() {
        const fileInput = document.getElementById('id_profile_picture');
        const fileNameDisplay = document.getElementById('file-selected-name');
        const avatarPreview = document.getElementById('avatar-preview');
        
        if (!fileInput) return;

        fileInput.addEventListener('change', (e) => {
            const file = e.target.files?.[0];
            if (!file) return;

            // Afficher le nom du fichier
            if (fileNameDisplay) {
                fileNameDisplay.textContent = file.name;
            }
            
            // Prévisualisation de l'image
            const reader = new FileReader();
            reader.onload = (event) => {
                const imageSrc = event.target.result;
                
                // Mettre à jour l'avatar preview
                if (avatarPreview) {
                    avatarPreview.src = imageSrc;
                }
                
                // Créer ou mettre à jour l'image de prévisualisation
                let imagePreview = document.querySelector('.current-image');
                if (!imagePreview) {
                    imagePreview = document.createElement('img');
                    imagePreview.classList.add('current-image');
                    fileInput.parentElement.prepend(imagePreview);
                }
                imagePreview.src = imageSrc;
            };
            reader.readAsDataURL(file);
        });
    },

    initFormValidation() {
        const errorMessages = document.querySelectorAll('.error-message');
        
        errorMessages.forEach(msg => {
            const formField = msg.parentElement.querySelector('input, textarea, select');
            if (!formField) return;

            const input = document.getElementById(formField.id);
            if (!input) return;

            input.classList.add('error-input');
            input.addEventListener('input', function() {
                if (this.value.trim() !== '') {
                    this.classList.remove('error-input');
                    msg.style.display = 'none';
                }
            });
        });
    },

    initTabNavigation() {
        const tabs = document.querySelectorAll('.profile-tab');
        
        tabs.forEach(tab => {
            tab.addEventListener('click', function() {
                tabs.forEach(t => t.classList.remove('active'));
                this.classList.add('active');
            });
        });
    },

    initFloatingLabels() {
        const formInputs = document.querySelectorAll('.form-group input, .form-group textarea');
        
        formInputs.forEach(input => {
            const label = input.nextElementSibling;
            if (label?.tagName !== 'LABEL') return;

            // État initial
            if (input.value.trim() !== '') {
                label.classList.add('active');
            }
            
            // Événements
            input.addEventListener('input', function() {
                label.classList.toggle('active', this.value.trim() !== '');
            });
            
            input.addEventListener('focus', function() {
                label.classList.add('active');
            });
            
            input.addEventListener('blur', function() {
                if (this.value.trim() === '') {
                    label.classList.remove('active');
                }
            });
        });
    },

    initDateInput() {
        const dateInput = document.getElementById('id_birth_date');
        if (!dateInput) return;

        const dateLabel = dateInput.nextElementSibling;
        if (dateLabel?.tagName === 'LABEL' && dateInput.value) {
            dateLabel.classList.add('active');
        }
    },

    initAutoAlerts() {
        const alerts = document.querySelectorAll('.alert');
        
        alerts.forEach(alert => {
            setTimeout(() => {
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 300);
            }, 5000);
        });
    }
};

// Gestion des préférences
const PreferencesManager = {
    init() {
        this.initPreferenceToggles();
    },

    initPreferenceToggles() {
        const emailNotifications = document.getElementById('email-notifications');
        
        if (emailNotifications) {
            emailNotifications.addEventListener('change', function() {
                PreferencesManager.updatePreference('email_notifications', this.checked);
            });
        }
    },

    updatePreference(preferenceName, value) {
        const csrfToken = Utils.getCSRFToken();
        
        if (!csrfToken) {
            console.error('CSRF token not found');
            Utils.showAlert('Error: Security token not found');
            return;
        }
        
        const formData = new FormData();
        formData.append('preference', preferenceName);
        formData.append('value', value);
        formData.append('csrfmiddlewaretoken', csrfToken);
        
        fetch(window.DJANGO_URLS.updatePreferences, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (!data.success) {
                throw new Error('Server returned error');
            }
            // Optionnel: afficher un message de confirmation
            console.log('Preference updated successfully');
        })
        .catch(error => {
            console.error('Error updating preference:', error);
            Utils.showAlert('Error updating preference');
            
            // Remettre l'ancien état du toggle
            const toggle = document.getElementById(preferenceName.replace('_', '-'));
            if (toggle) {
                toggle.checked = !value;
            }
        });
    }
};

// Gestion des actions de compte
const AccountManager = {
    init() {
        this.initAccountActions();
    },

    initAccountActions() {
        const deactivateBtn = document.querySelector('.deactivate-btn');
        const deleteBtn = document.querySelector('.delete-btn');
        
        if (deactivateBtn) {
            deactivateBtn.addEventListener('click', (e) => {
                e.preventDefault();
                if (confirm('Are you sure you want to deactivate your account?')) {
                    this.handleAccountAction(window.DJANGO_URLS.deactivateAccount);
                }
            });
        }
        
        if (deleteBtn) {
            deleteBtn.addEventListener('click', (e) => {
                e.preventDefault();
                if (confirm('Are you sure you want to permanently delete your account? This action cannot be undone.')) {
                    this.handleAccountAction(window.DJANGO_URLS.deleteAccount);
                }
            });
        }
    },

    handleAccountAction(actionUrl) {
        const csrfToken = Utils.getCSRFToken();
        
        if (!csrfToken) {
            console.error('CSRF token not found');
            Utils.showAlert('Error: Security token not found');
            return;
        }
        
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = actionUrl;
        
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = csrfToken;
        
        form.appendChild(csrfInput);
        document.body.appendChild(form);
        form.submit();
    }
};

// Initialisation au chargement du DOM
document.addEventListener('DOMContentLoaded', function() {
    ProfileManager.init();
    PreferencesManager.init();
    AccountManager.init();
});