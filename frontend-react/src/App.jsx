import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Hello from './components/Hello'
import ProfileCard from './components/ProfileCard'
import CeleryRedisTest from './components/CeleryRedisTest'

function App() {
  const [count, setCount] = useState("s")
  const [counter, setCounter] = useState(0)
  const [users, setUsers] = useState([]);
  const [isLoading, setIsLoading] = useState(false)

  const [taskId, setTaskId] = useState(null)
  const [taskStatus, setTaskStatus] = useState(null)

  useEffect(() => {
    setIsLoading(true)
    fetch('http://localhost:8000/react-users/')
      .then(response => response.json())
      .then(data => {
        setUsers(data)
        setIsLoading(false)
      })
      .catch(error => {
        console.log(error)
        setIsLoading(false)
      })

  }, []);

  useEffect(() => {
    if (!taskId || taskStatus === 'SUCCESS' || taskStatus === 'FAILURE') return;
    const interval = setInterval(() => {
      checkStatus();
    }, 2000);
    return () => clearInterval(interval);
  }, [taskId, taskStatus]);

  const runTask = () => {
    setTaskId(null);
    setTaskStatus(null);
    fetch('http://localhost:8000/trigger-task/')
      .then(responce => responce.json())
      .then(data => {
        setTaskId(data.task_id);
        setTaskStatus("PENDING");
      })
      .catch(error => console.error("Error:", error));
  }

  const checkStatus = () => {
    fetch(`http://localhost:8000/task-status/${taskId}/`)
      .then(response => response.json())
      .then(data => {
        setTaskStatus(data.status);
      })
      .catch(error => console.error("Error:", error));
  }

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <Hello name="John" />
      {isLoading ? (
        <p>Loading users...</p>
      ) : (
        users.map((user) => (
          <ProfileCard
            key={user.id}
            name={user.name}
            job={user.job}
            experience={user.experience}
          />
        ))
      )}
      <CeleryRedisTest />
      <div className="card">
        <button onClick={runTask}>Run Task</button>
        {taskId && <p>Task Started! ID: {taskId}</p>}
        {taskStatus && <p>Task Status: {taskStatus}</p>}
        <button onClick={() => setCount((count) => count + "s")}>
          count is {count}
        </button>
        <button onClick={() => setCounter((counter) => counter + 1)}>+</button>
        <button onClick={() => setCounter((counter) => counter - 1)}>-</button>
        <button onClick={() => setCounter((counter) => 0)}>reset</button>
        <p>{counter}</p>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
