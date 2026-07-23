# TaskFlow

TaskFlow is a simple and clean web application to manage tasks and team members. It helps companies track their projects, assign tasks to workers, and monitor deadlines.

---

### 🚀 Live Demo
* **Website:** [TaskFlow Live Application](https://taskflow-y9zm.onrender.com)
* **Demo Account:** 
  * **Username:** `user`
  * **Password:** `user12345`

---

## Tech Stack
* **Backend:** Python / Django
* **Frontend:** HTML, CSS (Bootstrap-based template)
* **Database:** PostgreSQL (Production) / SQLite (Local Dev)
* **Deployment:** Render

---

## Features & Pages Description

### 1. Login Page
* **Function:** Secure entry page for users.
* **Features:** Simple form with Username and Password fields to access system safely.

### 2. TaskFlow Dashboard
* **Function:** Main page that shows project's current status.
* **Features:** Colored statistic cards showing **Total Tasks**, **Completed**, **In Progress**, **Failed Deadlines**, and **Total Workers**.

### 3. Tasks List Page
* **Function:** Central list of all project tasks.
* **Features:**
  * Search bar to find tasks by name quickly.
  * Information table showing Task Name (with Tag badges), Deadline, Priority, and action buttons.
  * Pagination to navigate through multiple pages of tasks.

### 4. Task Details Page
* **Function:** Shows full information about specific task.
* **Features:** Displays description, tags, priority, deadline, and assigned workers. Includes quick-action buttons: **Mark as completed**, **Update**, and **Delete**.

### 5. Create / Update Task Page
* **Function:** Clean form to add new tasks or edit existing ones.
* **Features:**
  * Input fields for Name, Description, and Deadline.
  * Dropdowns for Priority and Task Type.
  * Styled selection boxes for Assignees and Tags.
  * "Is completed" switch (only on Update page) and "Save Task" button.

### 6. Delete Task Confirmation
* **Function:** Safety modal window to prevent accidental deletions.
* **Features:** Asks user if they are sure they want to delete task, with red **Yes, Delete** button.

### 7. Workers List Page
* **Function:** Directory of all team members.
* **Features:** Search bar to find workers by username and table showing Username, Full Name, and Job Position.

### 8. Worker Details Page
* **Function:** Individual profile page for team member.
* **Features:** Shows worker's name, position, and two clean columns: **Tasks in progress** and **Tasks completed**.

### 9. Logout / Guest Screen
* **Function:** Confirms that user has securely logged out.
* **Features:** Displays success message and "Click here to login again" button, changing sidebar status to "Guest".

---

## How to Run Project Locally

1. **Clone repository:**
    ```bash
    git clone https://github.com/LassisterV16/py-task-manager/
    cd taskflow
    ```

2. **Create and activate virtual environment:**
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run migrations:**
    ```bash
    python manage.py migrate
    ```

5. **Create superuser (admin):**
    ```bash
    python manage.py createsuperuser
    ```

6. **Start development server:**
    ```bash
    python manage.py runserver
    ```

**Now open http://127.0.0.1:8000/ in your browser.**
