document.addEventListener('DOMContentLoaded', function() {
    /************************
     * Nouvelle fonctionnalité: Drag & Drop et Preview
     ************************/
    const fileUploadArea = document.querySelector('.file-upload-area');
    const fileInput = document.getElementById('image-upload');
    const previewContainer = document.getElementById('preview-container');

    // Drag and drop functionality
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        fileUploadArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        fileUploadArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        fileUploadArea.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
        fileUploadArea.classList.add('drag-over');
    }

    function unhighlight() {
        fileUploadArea.classList.remove('drag-over');
    }

    // Handle dropped files
    fileUploadArea.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }

    // Handle file selection
    fileInput.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            handleFiles(this.files);
        }
    });

    function handleFiles(files) {
        previewContainer.innerHTML = '';
        const file = files[0];
        
        if (!file.type.match('image.*')) {
            showError('Please select an image file (JPG, PNG)');
            return;
        }

        if (file.size > 5 * 1024 * 1024) { // 5MB
            showError('File size should be less than 5MB');
            return;
        }

        const reader = new FileReader();
        
        reader.onload = function(e) {
            createPreview(e.target.result, file.name);
        }
        
        reader.readAsDataURL(file);
    }

    function createPreview(imageSrc, filename) {
        const preview = document.createElement('div');
        preview.className = 'image-preview';
        
        const img = document.createElement('img');
        img.src = imageSrc;
        img.alt = 'Preview';
        
        const details = document.createElement('div');
        details.className = 'preview-details';
        details.innerHTML = `
            <span class="filename">${filename}</span>
            <span class="filesize">${(fileInput.files[0].size / 1024 / 1024).toFixed(2)} MB</span>
        `;
        
        const removeBtn = document.createElement('button');
        removeBtn.className = 'remove-preview';
        removeBtn.innerHTML = '&times;';
        removeBtn.onclick = function() {
            previewContainer.innerHTML = '';
            fileInput.value = '';
        };
        
        preview.appendChild(img);
        preview.appendChild(details);
        preview.appendChild(removeBtn);
        previewContainer.appendChild(preview);
    }

    function showError(message) {
        previewContainer.innerHTML = `<div class="upload-error">${message}</div>`;
        fileInput.value = '';
    }

    /************************
     * Votre code existant (scroll animations)
     ************************/
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.scroll-animate');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.3;
            
            if (elementPosition < screenPosition) {
                element.classList.add('animated');
            }
        });
    };
    
    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll(); // Initial check

    /************************
     * Nouvelle fonctionnalité: Feedback visuel pendant l'upload
     ************************/
    const form = document.querySelector('.upload-form');
    if (form) {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = `
                    <span class="spinner"></span>
                    Analyzing...
                `;
                submitBtn.disabled = true;
            }
        });
    }
});