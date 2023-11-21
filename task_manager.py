import tkinter as tk
from tkinter import messagebox

class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("400x400")

        self.users = {}
        self.logged_in_user = None

        self.create_login_screen()

    def create_login_screen(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack()

        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=5)
        self.username_entry = tk.Entry(self.login_frame, width=30)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(self.login_frame, show="*", width=30)
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        register_button = tk.Button(self.login_frame, text="Register", command=self.register)
        register_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            if username in self.users:
                messagebox.showerror("Registration Failed", "Username already exists!")
            else:
                self.users[username] = {"password": password, "tasks": []}
                messagebox.showinfo("Registration Successful", "Registration successful! You can now log in.")
        else:
            messagebox.showerror("Registration Failed", "Please enter a username and password!")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.users:
            if self.users[username]["password"] == password:
                self.logged_in_user = username
                self.login_frame.destroy()  # Close the login window
                self.create_task_manager()
            else:
                messagebox.showerror("Login Failed", "Invalid password!")
        else:
            messagebox.showerror("Login Failed", "User does not exist!")

    def create_task_manager(self):
        self.task_frame = tk.Frame(self.root)
        self.task_frame.pack()

        self.task_label = tk.Label(self.task_frame, text="Your Tasks", font=("Helvetica", 16))
        self.task_label.pack(pady=10)

        self.task_listbox = tk.Listbox(self.task_frame, width=50, height=10)
        self.task_listbox.pack(padx=10, pady=5)

        self.priority_var = tk.StringVar(self.task_frame)
        self.priority_var.set("Low")

        priority_options = ["Low", "Medium", "High"]
        self.priority_dropdown = tk.OptionMenu(self.task_frame, self.priority_var, *priority_options)
        self.priority_dropdown.pack(pady=5)

        self.task_entry = tk.Entry(self.task_frame, width=40)
        self.task_entry.pack(padx=10, pady=5)

        add_task_button = tk.Button(self.task_frame, text="Add Task", command=self.add_task)
        add_task_button.pack(pady=5)

        modify_task_button = tk.Button(self.task_frame, text="Modify Task", command=self.modify_task)
        modify_task_button.pack(pady=5)

        delete_task_button = tk.Button(self.task_frame, text="Delete Task", command=self.delete_task)
        delete_task_button.pack(pady=5)

        logout_button = tk.Button(self.task_frame, text="Logout", command=self.logout)
        logout_button.pack(pady=10)

        self.display_tasks()

    def add_task(self):
        task = self.task_entry.get()
        priority = self.priority_var.get()
        if task:
            self.users[self.logged_in_user]["tasks"].append({"task": task, "priority": priority})
            self.display_tasks()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Add Task Failed", "Please enter a task!")

    def modify_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            selected_task = self.users[self.logged_in_user]["tasks"][selected_task_index[0]]
            new_task = self.task_entry.get()
            new_priority = self.priority_var.get()
            if new_task:
                selected_task["task"] = new_task
                selected_task["priority"] = new_priority
                self.display_tasks()
                self.task_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Modify Task Failed", "Please enter a task!")
        else:
            messagebox.showerror("Modify Task Failed", "Select a task to modify!")

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            self.users[self.logged_in_user]["tasks"].pop(selected_task_index[0])
            self.display_tasks()
        else:
            messagebox.showerror("Delete Task Failed", "Select a task to delete!")

    def display_tasks(self):
        self.task_listbox.delete(0, tk.END)
        tasks = self.users[self.logged_in_user]["tasks"]
        for task in tasks:
            self.task_listbox.insert(tk.END, f"Priority: {task['priority']} - {task['task']}")

    def logout(self):
        self.task_frame.destroy()
        self.create_login_screen()

def main():
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
