from django.http import JsonResponse
from django.shortcuts import render
from django.core.cache import cache
from celery import chain
from .tasks import (
    heavy_task_simulation, 
    unstable_api_call_task, 
    validate_order, 
    process_payment, 
    ship_order
)
from celery.result import AsyncResult
import uuid

def index(request):
    return render(request, 'index.html')

def trigger_task(request):
    """
    Triggers the Celery task asynchronously.
    """
    task = heavy_task_simulation.delay("user@example.com")
    return JsonResponse({
        "status": "Task accepted",
        "task_id": task.id
    })

def trigger_retry_task(request):
    """
    Triggers a task that might fail and retry automatically.
    """
    # Generate a random order ID
    order_id = str(uuid.uuid4())[:8]
    task = unstable_api_call_task.delay(order_id)
    return JsonResponse({
        "status": "Retry task started",
        "task_id": task.id,
        "note": "Check worker logs. It might fail and retry automatically."
    })

def trigger_workflow(request):
    """
    Triggers a Chain (Workflow) of tasks.
    """
    order_data = {
        "id": "ORD-12345",
        "item": "Laptop",
        "address": "123 Tech Street",
        "amount": 1500
    }
    
    # Chain: Validate -> Process Payment -> Ship
    # The result of each task is passed as the first argument to the next.
    workflow = chain(
        validate_order.s(order_data) | 
        process_payment.s() | 
        ship_order.s()
    )
    
    result = workflow.apply_async()
    
    return JsonResponse({
        "status": "Workflow started",
        "chain_id": result.id,
        "structure": "Validate -> Payment -> Ship"
    })

def cache_test(request):
    """
    Demonstrates using Redis as a cache.
    """
    # Try to get value from cache
    count = cache.get("page_views")
    
    if count is None:
        count = 0
    
    count += 1
    
    # Save back to cache with 1 hour timeout
    cache.set("page_views", count, timeout=3600)
    
    return JsonResponse({
        "page_views": count,
        "source": "Redis"
    })

def get_task_status(request, task_id):
    """
    Returns the current status of a task.
    """
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result if task_result.status == 'SUCCESS' else str(task_result.result),
        "info": task_result.info if isinstance(task_result.info, dict) else str(task_result.info)
    }
    return JsonResponse(result)

def get_react_users(request):
    users = [
        {"id": 1, "name": "Іван", "job": "Barista", "experience": "12 years"},
        {"id": 2, "name": "Марія", "job": "Manager", "experience": "25 years"},
        {"id": 3, "name": "Олег", "job": "Driver", "experience": "120 years"},
    ]
    return JsonResponse(users, safe=False)
