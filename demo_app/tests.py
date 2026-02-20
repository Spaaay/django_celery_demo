from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
from demo_app import tasks
import json

class TaskStatusTests(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('demo_app.views.AsyncResult')
    def test_task_status_pending(self, mock_async_result):
        # Mock a PENDING task
        mock_result = MagicMock()
        mock_result.status = 'PENDING'
        mock_result.result = None
        mock_result.info = None
        mock_async_result.return_value = mock_result

        response = self.client.get('/task-status/test-pending-id/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'PENDING')
        self.assertEqual(data['task_id'], 'test-pending-id')

    @patch('demo_app.views.AsyncResult')
    def test_task_status_progress(self, mock_async_result):
        # Mock a PROGRESS task with info
        mock_result = MagicMock()
        mock_result.status = 'PROGRESS'
        mock_result.result = None
        mock_result.info = {'message': 'Processing step 1...'}
        mock_async_result.return_value = mock_result

        response = self.client.get('/task-status/test-progress-id/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'PROGRESS')
        self.assertEqual(data['info'], {'message': 'Processing step 1...'})

    @patch('demo_app.views.AsyncResult')
    def test_task_status_success(self, mock_async_result):
        # Mock a SUCCESS task
        mock_result = MagicMock()
        mock_result.status = 'SUCCESS'
        mock_result.result = 'Task Completed'
        mock_result.info = None
        mock_async_result.return_value = mock_result

        response = self.client.get('/task-status/test-success-id/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'SUCCESS')
        self.assertEqual(data['result'], 'Task Completed')

class TaskExecutionTests(TestCase):
    def test_heavy_task_simulation_execution(self):
        # Allow passing 'self' to task by mocking update_state
        # Since we use bind=True, we can just call it if we mock the bind
        # Or easier: just call the function directly if we weren't using bind=True.
        # With bind=True, we can use 'apply' or construct the task.
        
        # Using apply() to run synchronously and mock update_state
        with patch('demo_app.tasks.heavy_task_simulation.update_state') as mock_update:
            result = tasks.heavy_task_simulation.apply(args=["test@example.com"]).get()
            
            self.assertEqual(result, "Email sent to test@example.com")
            
            # Verify update_state was called with PROGRESS
            self.assertTrue(mock_update.called)
            call_args_list = mock_update.call_args_list
            
            # Check for specific messages
            messages = [call[1]['meta']['message'] for call in call_args_list if 'meta' in call[1]]
            self.assertIn("Start processing email for test@example.com...", messages)
            self.assertIn("Generating report data...", messages)

    def test_unstable_task_success(self):
         with patch('demo_app.tasks.unstable_api_call_task.update_state') as mock_update:
            # Mock random to ensure success
            with patch('random.choice', return_value=False): # False triggers success path in our code logic? 
                # Wait, code says: if random.choice([True, True, False]): raise Error
                # So False means NO error.
                
                result = tasks.unstable_api_call_task.apply(args=["ORD-123"]).get()
                self.assertEqual(result, "Order ORD-123 Charged")
                
                # Check messages
                messages = [call[1]['meta']['message'] for call in mock_update.call_args_list if 'meta' in call[1]]
                self.assertIn("Attempting to charge Order #ORD-123...", messages)
                self.assertIn("Charge successful for Order #ORD-123!", messages)
