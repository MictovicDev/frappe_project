import frappe
from frappe import _
from frappe.utils import now_datetime


@frappe.whitelist()
def create_project(title, description, status="Open"):
    """Create a new project with validation and logging."""
    
    # Validate dates if provided

    project = frappe.get_doc({
        "doctype": "Project",
        "title": title,
        "description": description,
        "status": status,
    })
    
    project.insert()
    frappe.db.commit()

    # Log creation
    frappe.logger().info(f"Project '{project.name}' created successfully.")

    # Clear project cache after insertion
    frappe.cache().delete_value("all_projects")

    return project



@frappe.whitelist()
def get_projects():
    """Fetch all projects with their linked tasks and caching."""
    cache_key = "all_projects"

    if cached_projects := frappe.cache().get_value(cache_key):
        return cached_projects

    projects = frappe.get_all("Project", fields=["name", "title", "description", "status"])

    # Fetch all tasks in one query for efficiency
    task_data = frappe.get_all("Task", fields=["name", "title", "status", "project"])

    # Map tasks to their respective projects
    task_map = {}
    for task in task_data:
        task_map.setdefault(task["project"], []).append(task)

    # Attach tasks to each project
    for project in projects:
        project["tasks"] = task_map.get(project["name"], [])

    # Store in cache for 10 minutes
    frappe.cache().set_value(cache_key, projects, expires_in_sec=600)

    return projects



@frappe.whitelist()
def update_project(name, status):
    """Update project status with validation."""
    if not frappe.db.exists("Project", name):
        frappe.throw(_("Project not found"))

    project = frappe.get_doc("Project", name)
    project.status = status
    project.modified_on = now_datetime()
    project.save()

    # Clear project cache after update
    frappe.cache().delete_value("all_projects")
    frappe.cache().delete_value(f"project_{name}")

    # Log update
    frappe.logger().info(f"Project '{name}' updated to '{status}'.")

    return project



@frappe.whitelist()
def delete_project(name):
    """Delete a project with validation and logging."""
    if not frappe.db.exists("Project", name):
        frappe.throw(_("Project not found"))

    frappe.delete_doc("Project", name)

    # Clear caches after deletion
    frappe.cache().delete_value("all_projects")
    frappe.cache().delete_value(f"project_{name}")

    # Log deletion
    frappe.logger().warning(f"Project '{name}' deleted.")

    return {"message": f"Project '{name}' deleted successfully."}
