document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('csv-file');
    const uploadForm = document.getElementById('upload-form');
    const uploadBtn = document.getElementById('upload-btn');
    const loadingScreen = document.getElementById('loading-screen');
    const landingPage = document.getElementById('landing-page');
    const analyticsPage = document.getElementById('analytics-page');
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');

    // Trigger file selector when upload button is clicked
    uploadBtn.addEventListener('click', () => {
        fileInput.click();
    });

    // Handle file selection and upload
    fileInput.addEventListener('change', () => {
        const file = fileInput.files[0];
        if (!file) return;

        const formData = new FormData(uploadForm);

        // Show loading, hide landing
        loadingScreen.classList.remove('hidden');
        landingPage.classList.add('hidden');

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(res => {
            if (!res.ok) {
                throw new Error('Network response was not ok');
            }
            return res.json();
        })
        .then(data => {
            loadingScreen.classList.add('hidden');

            if (data.error) {
                alert(data.error);
                landingPage.classList.remove('hidden');
                return;
            }

            // Show analytics page
            analyticsPage.classList.remove('hidden');

            // Display basic CSV info and preview
            addBotMessage(`
                <strong>📄 File:</strong> ${data.filename}<br>
                <strong>📊 Rows:</strong> ${data.rowCount}<br>
                <strong>📈 Columns:</strong> ${data.columnCount}<br><br>
                <strong>🔍 Preview:</strong>
                ${renderTable(data.preview.columns, data.preview.rows)}
            `);
        })
        .catch(error => {
            console.error('Error:', error);
            loadingScreen.classList.add('hidden');
            landingPage.classList.remove('hidden');
            alert('Error uploading file: ' + error.message);
        });
    });

    // Handle chat messages
    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    function sendMessage() {
        const message = chatInput.value.trim();
        if (!message) return;

        addUserMessage(message);
        chatInput.value = '';

        // Send to server
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message })
        })
        .then(res => res.json())
        .then(data => {
            addBotMessage(data.message);
        })
        .catch(error => {
            console.error('Error:', error);
            addBotMessage("Sorry, there was an error processing your request.");
        });
    }

    function addUserMessage(content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user-message';
        messageDiv.innerHTML = content;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function addBotMessage(content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';
        messageDiv.innerHTML = content;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function renderTable(columns, rows) {
        let table = '<table class="preview-table"><thead><tr>';
        columns.forEach(col => table += `<th>${col}</th>`);
        table += '</tr></thead><tbody>';
        rows.forEach(row => {
            table += '<tr>';
            row.forEach(cell => table += `<td>${cell}</td>`);
            table += '</tr>';
        });
        table += '</tbody></table>';
        return table;
    }
});