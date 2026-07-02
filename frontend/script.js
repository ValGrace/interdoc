document.addEventListener('DOMContentLoaded', () => {
    const apiBase = 'http://127.0.0.1:8000';
    const fileInput = document.getElementById('file-upload');
    const progressContainer = document.getElementById('upload-progress-container');
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');
    const fileNameDisplay = document.getElementById('file-name');
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    if (menuToggle) {
        menuToggle.addEventListener('click', () => {
            sidebar.classList.toggle('active');
        });
    }
    const promptInput = document.querySelector('.main-input');
    const sendButton = document.querySelector('.send-btn');

    function setPromptActive() {
        promptInput.disabled = false;
        promptInput.focus();
        promptInput.placeholder = 'Ask a question about the uploaded document...';
    }

    const responsePanel = document.getElementById('response-panel');
    const responseText = document.getElementById('response-text');

    async function sendQuery() {
        const question = promptInput.value.trim();
        if (!question) return;

        promptInput.disabled = true;
        sendButton.disabled = true;
        sendButton.style.opacity = '0.7';
        responsePanel.classList.remove('hidden');
        responseText.textContent = 'Loading answer...';

        try {
            const response = await fetch(`${apiBase}/query`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question })
            });

            if (!response.ok) {
                throw new Error(`Server responded with status ${response.status}`);
            }

            const data = await response.json();
            responseText.textContent = data.answer || 'No answer returned.';
        } catch (error) {
            responseText.textContent = 'Unable to reach the query service. Check that the backend is running on port 8000.';
            console.error(error);
        } finally {
            promptInput.disabled = false;
            sendButton.disabled = false;
            sendButton.style.opacity = '1';
            promptInput.focus();
            promptInput.value = '';
        }
    }

    sendButton.addEventListener('click', sendQuery);
    promptInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            sendQuery();
        }
    });

    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;
        progressContainer.classList.remove('hidden');
        fileNameDisplay.textContent = file.name;
        progressBar.style.width = '0%';
        progressText.textContent = '0%';

        const xhr = new XMLHttpRequest();
        const formData = new FormData();
        formData.append('file', file);

        xhr.open('POST', `${apiBase}/upload`);

        xhr.upload.onprogress = (event) => {
            if (event.lengthComputable) {
                const percent = Math.round((event.loaded / event.total) * 100);
                progressBar.style.width = `${percent}%`;
                progressText.textContent = `${percent}%`;
            }
        };

        xhr.onload = () => {
            if (xhr.status >= 200 && xhr.status < 300) {
                progressBar.style.width = '100%';
                progressText.textContent = 'Upload Complete!';
                setPromptActive();
                setTimeout(() => {
                    progressContainer.classList.add('hidden');
                    fileInput.value = '';
                }, 1200);
            } else {
                progressText.textContent = 'Upload failed';
                console.error('Upload error', xhr.status, xhr.responseText);
            }
        };

        xhr.onerror = () => {
            progressText.textContent = 'Upload failed';
            console.error('Upload failed');
        };

        xhr.send(formData);
    });
});