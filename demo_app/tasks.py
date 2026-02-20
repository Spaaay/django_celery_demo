from celery import shared_task
import time
import random

@shared_task(bind=True)
def heavy_task_simulation(self, email):
    """
    Simulates a heavy task, e.g., generating a report or sending an email.
    """
    print(f"Start processing email for {email}...")
    self.update_state(state='PROGRESS', meta={'message': f"Start processing email for {email}..."})
    
    # Simulate work steps
    time.sleep(2)
    self.update_state(state='PROGRESS', meta={'message': "Generating report data..."})
    
    time.sleep(2) 
    self.update_state(state='PROGRESS', meta={'message': "Finalizing email..."})
    
    time.sleep(1)
    print(f"Finished processing email for {email}!")
    return f"Email sent to {email}"

# ==============================================================================
# 1. PERIODIC TASKS (CELERY BEAT)
# ==============================================================================
@shared_task
def daily_maintenance_task():
    """
    Example of a periodic task.
    In a real app, this might clear old logs, generate daily stats, or sync data.
    """
    print("[Maintenance] Starting daily cleanup...")
    time.sleep(3) # Simulate DB cleanup
    print("[Maintenance] Cleanup complete. Old records archived.")
    return "Maintenance OK"

# ==============================================================================
# 2. ROBUST ERROR HANDLING (RETRIES)
# ==============================================================================
@shared_task(bind=True, autoretry_for=(ConnectionError,), retry_backoff=True, retry_kwargs={'max_retries': 3})
def unstable_api_call_task(self, order_id):
    """
    Simulates an unstable 3rd party API call (e.g., Stripe, Twilio).
    
    bind=True: Allows access to 'self', needed for logging or manual retries.
    autoretry_for=(ConnectionError,): Automatically retry if this exception is raised.
    retry_backoff=True: Exponential backoff (wait 1s, then 2s, 4s, 8s...).
    """
    print(f"[Payment] Attempting to charge Order #{order_id}...")
    self.update_state(state='PROGRESS', meta={'message': f"Attempting to charge Order #{order_id}..."})
    time.sleep(1)
    
    # Simulate random failure (70% chance of fail)
    if random.choice([True, True, False]):
        print(f"[Payment] Connection failed for Order #{order_id}! Retrying...")
        self.update_state(state='PROGRESS', meta={'message': f"Connection failed for Order #{order_id}! Retrying..."})
        raise ConnectionError("Simulated connection timeout to Payment Gateway")
    
    print(f"[Payment] Charge successful for Order #{order_id}!")
    self.update_state(state='PROGRESS', meta={'message': f"Charge successful for Order #{order_id}!"})
    return f"Order {order_id} Charged"

# ==============================================================================
# 3. WORKFLOWS (CHAINS)
# ==============================================================================
@shared_task
def validate_order(order_data):
    """Step 1: Validate order details."""
    print(f"[Workflow] Validating order: {order_data}...")
    time.sleep(1)
    return order_data # Pass data to next task

@shared_task
def process_payment(order_data):
    """Step 2: Process payment."""
    print(f"[Workflow] Processing payment for {order_data['id']}...")
    time.sleep(2)
    # Simulate adding payment info
    order_data['payment_status'] = 'paid'
    return order_data

@shared_task
def ship_order(order_data):
    """Step 3: Ship the item."""
    print(f"[Workflow] Shipping Order #{order_data['id']} to {order_data['address']}...")
    time.sleep(1)
    return f"Order {order_data['id']} Shipped!"
