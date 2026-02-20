from celery import shared_task
import time
import random

def log_task_to_db(task_id, task_name, status, result=None):
    from demo_app.models import TaskMetadata
    obj, created = TaskMetadata.objects.update_or_create(
        task_id=task_id,
        defaults={
            'task_name': task_name,
            'status': status,
            'result': result
        }
    )
    return obj

@shared_task(bind=True)
def heavy_task_simulation(self, email):
    """
    Simulates a heavy task, e.g., generating a report or sending an email.
    """
    task_id = self.request.id
    log_task_to_db(task_id, "Heavy Task Simulation", "STARTED")
    
    print(f"Start processing email for {email}...")
    self.update_state(state='PROGRESS', meta={'message': f"Start processing email for {email}..."})
    
    # Simulate work steps
    time.sleep(2)
    self.update_state(state='PROGRESS', meta={'message': "Generating report data..."})
    log_task_to_db(task_id, "Heavy Task Simulation", "PROGRESS", {"step": "report data"})
    
    time.sleep(2) 
    self.update_state(state='PROGRESS', meta={'message': "Finalizing email..."})
    log_task_to_db(task_id, "Heavy Task Simulation", "PROGRESS", {"step": "finalizing"})
    
    time.sleep(1)
    print(f"Finished processing email for {email}!")
    result = f"Email sent to {email}"
    log_task_to_db(task_id, "Heavy Task Simulation", "SUCCESS", {"final_result": result})
    return result

# ==============================================================================
# 1. PERIODIC TASKS (CELERY BEAT)
# ==============================================================================
@shared_task
def daily_maintenance_task():
    """
    Example of a periodic task.
    """
    log_task_to_db("periodic-" + str(time.time()), "Daily Maintenance", "STARTED")
    print("[Maintenance] Starting daily cleanup...")
    time.sleep(3) # Simulate DB cleanup
    print("[Maintenance] Cleanup complete. Old records archived.")
    log_task_to_db("periodic-" + str(time.time()), "Daily Maintenance", "SUCCESS", "Maintenance OK")
    return "Maintenance OK"

# ==============================================================================
# 2. ROBUST ERROR HANDLING (RETRIES)
# ==============================================================================
@shared_task(bind=True, autoretry_for=(ConnectionError,), retry_backoff=True, retry_kwargs={'max_retries': 3})
def unstable_api_call_task(self, order_id):
    task_id = self.request.id
    log_task_to_db(task_id, f"Payment Order #{order_id}", "STARTED")
    
    print(f"[Payment] Attempting to charge Order #{order_id}...")
    self.update_state(state='PROGRESS', meta={'message': f"Attempting to charge Order #{order_id}..."})
    time.sleep(1)
    
    # Simulate random failure (70% chance of fail)
    if random.choice([True, True, False]):
        print(f"[Payment] Connection failed for Order #{order_id}! Retrying...")
        log_task_to_db(task_id, f"Payment Order #{order_id}", "RETRYING")
        self.update_state(state='PROGRESS', meta={'message': f"Connection failed for Order #{order_id}! Retrying..."})
        raise ConnectionError("Simulated connection timeout to Payment Gateway")
    
    print(f"[Payment] Charge successful for Order #{order_id}!")
    log_task_to_db(task_id, f"Payment Order #{order_id}", "SUCCESS", f"Order {order_id} Charged")
    self.update_state(state='PROGRESS', meta={'message': f"Charge successful for Order #{order_id}!"})
    return f"Order {order_id} Charged"

# ==============================================================================
# 3. WORKFLOWS (CHAINS)
# ==============================================================================
@shared_task(bind=True)
def validate_order(self, order_data):
    """Step 1: Validate order details."""
    log_task_to_db(self.request.id, f"Workflow: Validate {order_data['id']}", "SUCCESS")
    print(f"[Workflow] Validating order: {order_data}...")
    time.sleep(1)
    return order_data 

@shared_task(bind=True)
def process_payment(self, order_data):
    """Step 2: Process payment."""
    log_task_to_db(self.request.id, f"Workflow: Payment {order_data['id']}", "SUCCESS")
    print(f"[Workflow] Processing payment for {order_data['id']}...")
    time.sleep(2)
    order_data['payment_status'] = 'paid'
    return order_data

@shared_task(bind=True)
def ship_order(self, order_data):
    """Step 3: Ship the item."""
    log_task_to_db(self.request.id, f"Workflow: Ship {order_data['id']}", "SUCCESS")
    print(f"[Workflow] Shipping Order #{order_data['id']} to {order_data['address']}...")
    time.sleep(1)
    return f"Order {order_data['id']} Shipped!"
