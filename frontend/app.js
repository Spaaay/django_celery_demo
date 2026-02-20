const API_BASE_URL = '';

document.addEventListener('DOMContentLoaded', () => {
    // Buttons
    const btnHeavyTask = document.getElementById('btn-heavy-task');
    const btnWorkflow = document.getElementById('btn-workflow');
    const btnRetry = document.getElementById('btn-retry');
    const btnClearLogs = document.getElementById('clear-logs');

    // Status Messages
    const statusHeavy = document.getElementById('status-heavy-task');
    const statusWorkflow = document.getElementById('status-workflow');
    const statusRetry = document.getElementById('status-retry');

    // Connection Check
    checkBackendHealth();

    // Event Listeners
    btnHeavyTask.addEventListener('click', () => triggerTask('/trigger-task/', statusHeavy, 'Heavy Task'));
    btnWorkflow.addEventListener('click', () => triggerTask('/trigger-workflow/', statusWorkflow, 'Workflow'));
    btnRetry.addEventListener('click', () => triggerTask('/trigger-retry/', statusRetry, 'Retry Task'));
    btnClearLogs.addEventListener('click', clearLogs);

    // Functions
    async function triggerTask(endpoint, statusElement, taskName) {
        setLoading(true, statusElement);
        log(`Triggering ${taskName}...`);

        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

            const data = await response.json();

            setLoading(false, statusElement);
            statusElement.textContent = `Task ID: ${data.task_id || data.chain_id}`;
            statusElement.style.color = 'var(--accent-emerald)';

            log(`Success: ${taskName} started. ID: ${data.task_id || data.chain_id}`, 'success');
            console.log(data);

            // Start polling
            pollTaskStatus(data.task_id || data.chain_id, statusElement);

        } catch (error) {
            setLoading(false, statusElement);
            statusElement.textContent = 'Failed to start';
            statusElement.style.color = 'var(--accent-rose)';
            log(`Error: Failed to start ${taskName}. ${error.message}`, 'error');
            console.error(error);
        }
    }

    async function pollTaskStatus(taskId, statusElement) {
        if (!taskId) return;

        // Keep track of the last message to avoid duplicates in the log
        let lastMessage = '';

        const pollInterval = setInterval(async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/task-status/${taskId}/`);
                if (!response.ok) throw new Error('Status check failed');

                const data = await response.json();
                const status = data.status;
                const result = data.result;
                const info = data.info; // This contains our 'meta' dict from update_state

                statusElement.textContent = `ID: ${taskId} | Status: ${status}`;

                // Handle PROGRESS state
                if (status === 'PROGRESS' && info && info.message) {
                    if (info.message !== lastMessage) {
                        log(info.message, 'info');
                        lastMessage = info.message;
                    }
                }

                if (status === 'SUCCESS') {
                    clearInterval(pollInterval);
                    statusElement.style.color = 'var(--accent-emerald)';
                    log(`Task ${taskId} completed successfully.`, 'success');
                    if (result) console.log('Result:', result);
                } else if (status === 'FAILURE' || status === 'REVOKED') {
                    clearInterval(pollInterval);
                    statusElement.style.color = 'var(--accent-rose)';
                    // If it's a failure, 'result' might be the exception string
                    log(`Task ${taskId} failed: ${result}`, 'error');
                } else {
                    statusElement.style.color = 'var(--accent-amber)';
                }

            } catch (error) {
                console.error('Polling error:', error);
                clearInterval(pollInterval);
                statusElement.textContent += ' (Polling Error)';
            }
        }, 1000); // Poll every 1 second
    }

    async function checkBackendHealth() {
        const statusEl = document.getElementById('connection-status');
        try {
            // Using a simple fetch to root or a known endpoint to check connection
            const response = await fetch(`${API_BASE_URL}/`);
            if (response.ok) {
                statusEl.textContent = 'Connected';
                statusEl.style.color = 'var(--accent-emerald)';
                document.querySelector('.dot').style.backgroundColor = 'var(--accent-emerald)';
                document.querySelector('.dot').style.boxShadow = '0 0 8px var(--accent-emerald)';
            } else {
                throw new Error('Backend returned error');
            }
        } catch (e) {
            statusEl.textContent = 'Backend Offline';
            statusEl.style.color = 'var(--accent-rose)';
            document.querySelector('.dot').style.backgroundColor = 'var(--accent-rose)';
            document.querySelector('.dot').style.boxShadow = '0 0 8px var(--accent-rose)';
            log('Could not connect to backend at ' + API_BASE_URL, 'error');
            console.error(e);
        }
    }

    function setLoading(isLoading, element) {
        if (element) {
            if (isLoading) {
                element.textContent = 'Processing...';
                element.style.color = 'var(--text-secondary)';
                element.classList.add('loading');
            } else {
                element.classList.remove('loading');
            }
        }
    }

    function log(message, type = 'system') {
        const container = document.getElementById('activity-log');
        const entry = document.createElement('div');
        entry.className = `log-entry ${type}`;

        const time = new Date().toLocaleTimeString();

        entry.innerHTML = `
            <span class="timestamp">${time}</span>
            <span class="message">${message}</span>
        `;

        container.prepend(entry);
    }

    function clearLogs() {
        const container = document.getElementById('activity-log');
        container.innerHTML = '';
        log('Logs cleared.');
    }
});
