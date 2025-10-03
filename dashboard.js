document.addEventListener('DOMContentLoaded', () => {
    const logoutBtn = document.getElementById('logout-btn');
    const uploadForm = document.getElementById('uploadForm');
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file');
    const selectedFileNameDisplay = document.getElementById('selected-file-name');

    // --- Logout Functionality ---
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            console.log('Logging out...');
            window.location.href = 'index.html'; // Ensure this points to your login page
        });
    }

    // --- Drag & Drop File Upload Functionality ---
    if (dropZone) {
        // 1. Click on the drop zone to open the file dialog
        dropZone.addEventListener('click', () => {
            fileInput.click();
        });

        // 2. Add a visual indicator when a file is dragged over
        dropZone.addEventListener('dragover', (event) => {
            event.preventDefault(); // Necessary to allow drop
            dropZone.classList.add('drag-over');
        });

        // 3. Remove the visual indicator when the file is no longer being dragged over
        dropZone.addEventListener('dragleave', () => {
            dropZone.classList.remove('drag-over');
        });

        // 4. Handle the actual file drop
        dropZone.addEventListener('drop', (event) => {
            event.preventDefault();
            dropZone.classList.remove('drag-over');
            
            const files = event.dataTransfer.files;
            fileInput.files = files; // Assign dropped files to the hidden input
            handleFileSelection();
        });

        // 5. Handle file selection when using the file dialog
        fileInput.addEventListener('change', handleFileSelection);

        function handleFileSelection() {
            if (fileInput.files.length > 0) {
                selectedFileNameDisplay.textContent = `Selected file: ${fileInput.files[0].name}`;
            } else {
                selectedFileNameDisplay.textContent = '';
            }
        }
    }

    // --- Form Submission Logic ---
    if (uploadForm) {
        uploadForm.addEventListener('submit', (event) => {
            event.preventDefault();
            if (fileInput.files.length > 0) {
                alert(`Uploading file: ${fileInput.files[0].name}. (Backend not implemented)`);
                // Here you would add the code to actually send the file to a server
            } else {
                alert('Please select a file to upload.');
            }
        });
    }

    // --- Anomaly Table (example data to show the table works) ---
    const anomalyTableBody = document.querySelector('#anomalyTable tbody');
    if (anomalyTableBody) {
        const exampleData = [
            { id: '101', sub: 'CS202', date: '2025-10-02', type: 'Duplicate Entry' },
            { id: '105', sub: 'MA101', date: '2025-10-01', type: 'Suspicious Signature' }
        ];

        exampleData.forEach(item => {
            const row = anomalyTableBody.insertRow();
            row.insertCell().textContent = item.id;
            row.insertCell().textContent = item.sub;
            row.insertCell().textContent = item.date;
            row.insertCell().textContent = item.type;
        });
    }
});