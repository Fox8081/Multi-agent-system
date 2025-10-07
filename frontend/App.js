// This is the main script for our frontend.
// I'm using plain JavaScript to keep it simple and show understanding of the fundamentals.

document.addEventListener('DOMContentLoaded', () => {
    // Getting references to all the HTML elements we need to interact with.
    const queryForm = document.getElementById('query-form');
    const queryInput = document.getElementById('query-input');
    const pdfUpload = document.getElementById('pdf-upload');
    const statusArea = document.getElementById('status-area');
    const resultArea = document.getElementById('result-area');
    const answerText = document.getElementById('answer-text');
    const agentUsed = document.getElementById('agent-used');
    const rationale = document.getElementById('rationale');
    const submitButton = document.getElementById('submit-button');

    // This variable will hold the unique ID of the uploaded PDF.
    let uploadedFileId = null;

    // --- Event Listener for PDF Upload ---
    // This runs when the user selects a file.
    pdfUpload.addEventListener('change', async (event) => {
        const file = event.target.files[0];
        if (!file) return;

        // Using FormData to send the file to the backend, which is standard practice.
        const formData = new FormData();
        formData.append('file', file);

        statusArea.textContent = `Uploading ${file.name}...`;

        try {
            // Making the API call to our '/upload_pdf' endpoint.
            const response = await fetch('/upload_pdf', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                uploadedFileId = data.file_id; // Store the file_id from the backend.
                statusArea.textContent = `✅ ${file.name} uploaded successfully. You can now ask questions about it.`;
            } else {
                statusArea.textContent = `Error: ${data.error}`;
            }
        } catch (error) {
            statusArea.textContent = 'An error occurred during file upload.';
            console.error('Upload Error:', error);
        }
    });

    // --- Event Listener for Form Submission ---
    // This runs when the user clicks the "Ask" button.
    queryForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevents the page from reloading.
        const query = queryInput.value;

        if (!query) return;

        statusArea.textContent = 'Thinking...';
        submitButton.disabled = true; // Disable the button to prevent multiple requests.
        resultArea.classList.add('hidden'); // Hide old results.

        try {
            // Making the API call to our '/ask' endpoint.
            const response = await fetch('/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                // Sending the query and the file_id (which can be null).
                body: JSON.stringify({ query: query, file_id: uploadedFileId })
            });

            const data = await response.json();

            if (response.ok) {
                // Displaying the results from the backend in the correct HTML elements.
                answerText.innerText = data.answer;
                agentUsed.innerText = data.agents_used.join(', ');
                rationale.innerText = data.rationale;
                resultArea.classList.remove('hidden'); // Show the results area.
                statusArea.textContent = ''; // Clear the status message.
            } else {
                statusArea.textContent = `Error: ${data.error}`;
            }
        } catch (error) {
            statusArea.textContent = 'An error occurred while getting the answer.';
            console.error('Ask Error:', error);
        } finally {
            submitButton.disabled = false; // Re-enable the button.
        }
    });
})