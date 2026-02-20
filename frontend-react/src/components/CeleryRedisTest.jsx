import { useState, useEffect } from 'react';

const API_URL = 'http://localhost:8000';

function CeleryRedisTest() {
    const [taskId, setTaskId] = useState(null);
    const [taskStatus, setTaskStatus] = useState(null);

    const runTask = () => {
        setTaskId(null);
        setTaskStatus("STARTING...");

        // Викликаємо API, яке запускає задачу
        // Воно повертає ТІЛЬКИ ID задачі. Статус там ще не відомий (Pending).
        fetch(`${API_URL}/trigger-retry/`)
            .then(response => response.json())
            .then(data => {
                setTaskId(data.task_id);
                setTaskStatus(data.status); // Це лише початкове повідомлення "Retry task started"
            })
            .catch(error => console.error("Error:", error));
    };

    // Щоб отримати РЕАЛЬНИЙ статус, треба питати сервер окремо по ID
    useEffect(() => {
        if (!taskId) return;

        const interval = setInterval(() => {
            fetch(`${API_URL}/task-status/${taskId}/`)
                .then(res => res.json())
                .then(data => {
                    setTaskStatus(data.status); // Ось тут прийде справжній статус (RETRY, FAILURE, SUCCESS)
                    console.log("Current Status:", data.status, data);

                    if (data.status === 'SUCCESS' || data.status === 'FAILURE') {
                        clearInterval(interval);
                    }
                });
        }, 1000);

        return () => clearInterval(interval);
    }, [taskId]);

    return (
        <div className="card" style={{ border: '2px solid orange', padding: '20px', marginTop: '20px' }}>
            <h2>Celery Retry Test</h2>
            <p>Ця задача може впасти і спробувати ще раз!</p>

            <button onClick={runTask}>Run Unstable Task</button>

            {taskId && <p><strong>Task ID:</strong> {taskId}</p>}
            {taskStatus && <p><strong>Status:</strong> {taskStatus}</p>}
        </div>
    );
}

export default CeleryRedisTest;