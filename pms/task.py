import frappe
from frappe import _
from frappe.utils import now_datetime

@frappe.whitelist()
def create_task(title, description, assigned_to, due_date, status, project=None):
    """Create a new task with proper validation and logging."""
    
    try:
        due_date = frappe.utils.getdate(due_date)
    except Exception:
        frappe.throw(_("Invalid date format. Use YYYY-MM-DD."))

    if not frappe.db.exists("User", assigned_to):
        frappe.throw(_("Assigned user does not exist."))

    task = frappe.get_doc({
        "doctype": "Task",
        "title": title,
        "description": description,
        "assigned_to": assigned_to,
        "status": status,
        "project": project,
        "due_date": due_date,
    })
    
    task.insert(ignore_permissions=True)
    frappe.db.commit()

    # Log creation
    frappe.logger().info(f"Task '{task.name}' created successfully.")
    
    return task


@frappe.whitelist()
def get_tasks():
    """Fetch all tasks with caching for better performance."""
    cache_key = "all_tasks"
    
    if cached_tasks := frappe.cache().get_value(cache_key):
        return cached_tasks
    
    tasks = frappe.get_all("Task", fields=["name", "title", "description", "due_date", "assigned_to", "status", "project"])
    
    frappe.cache().set_value(cache_key, tasks, expires_in_sec=600)
    
    return tasks


@frappe.whitelist()
def get_task(task_id):
    """Fetch a single task with caching and validation."""
    if not frappe.db.exists("Task", task_id):
        frappe.throw(_("Task not found"))

    cache_key = f"task_{task_id}"
    
    if cached_task := frappe.cache().get_value(cache_key):
        return cached_task

    task = frappe.get_doc("Task", task_id)
    
    # Cache for 5 minutes
    frappe.cache().set_value(cache_key, task, expires_in_sec=300)
    
    return task


@frappe.whitelist()
def update_task(name, status):
    """Update task status with validation."""
    if not frappe.db.exists("Task", name):
        frappe.throw(_("Task not found"))

    task = frappe.get_doc("Task", name)
    task.status = status
    task.modified_on = now_datetime()
    task.save()

    # Clear task cache after update
    frappe.cache().delete_value(f"task_{name}")

    # Log update
    frappe.logger().info(f"Task '{name}' updated to '{status}'.")

    return task


@frappe.whitelist()
def delete_task(name):
    """Delete a task with validation and logging."""
    if not frappe.db.exists("Task", name):
        frappe.throw(_("Task not found"))

    frappe.delete_doc("Task", name)
    
    # Clear caches after deletion
    frappe.cache().delete_value(f"task_{name}")
    frappe.cache().delete_value("all_tasks")

    # Log deletion
    frappe.logger().warning(f"Task '{name}' deleted.")

    return {"message": f"Task '{name}' deleted successfully."}
