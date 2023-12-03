import tkinter as tk
import mysql.connector
from tkinter import messagebox
from tkinter import simpledialog


class PasswordManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Password Manager")
        self.master.geometry("1920x1080")
        self.master.config(bg="#dacef3")

        # Initialize the database
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ramsam",
        )

        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS mypasswordmanager")
        self.cursor.execute("USE mypasswordmanager")
        # Create a table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwordmanager (
                id INT AUTO_INCREMENT PRIMARY KEY,
                website VARCHAR(255) NOT NULL,
                username VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        ''')

        self.conn.commit()

        self.show_password = True  # Initialize show_password variable

        # Entry Widgets
        label = tk.Label(master, text="MYPASSWORD  MANAGER", font=("arialblack", 33), bg="#dacef3", fg="#c50000")
        label.place(x=485, y=30)
        label.config(font='arialblack 33 underline')

        tk.Label(master, text="Website/Service:", font=("Arial", 20), bg="#dacef3", fg="#000000").place(x=510, y=110)
        tk.Label(master, text="Username/email :", font=("Arial", 20), bg="#dacef3", fg="#000000").place(x=510, y=180)
        tk.Label(master, text="Password :", font=("Arial", 20), bg="#dacef3", fg="#000000").place(x=510, y=250)

        self.website_entry = tk.Entry(master, font=("Arial", 15), width=25)
        self.username_entry = tk.Entry(master, font=("Arial", 15), width=25)
        self.password_entry = tk.Entry(master, show="*", font=("Arial", 15), width=25)

        self.website_entry.place(x=760, y=120)
        self.username_entry.place(x=760, y=190)
        self.password_entry.place(x=760, y=260)

        # Buttons
        tk.Button(master, text="Add", command=self.add_password, font=("Arial", 18), width=8, bg="#a7e09a").place(x=730, y=350)
        tk.Button(master, text="Clear", command=self.clear_entries, font=("Arial", 18), width=8, bg="yellow").place(x=910, y=350)
        tk.Button(master, text="Exit", command=self.exit_app, font=("Arial", 18), bg="#fa7b7b", width=8).place(x=730, y=550)
        self.show_hide_button = tk.Button(master, text="Show", command=self.showhide, font=("Arial", 13), bg="lightgreen")
        self.show_hide_button.place(x=1050, y=258)

        tk.Button(master, text="ChangePassword", command=self.open_change_password_window, font=("Arial", 18), bg="#007BFF", fg="white").place(x=560, y=448)
        tk.Button(master, text="Delete", command=self.open_delete_website_window, font=("Arial", 18), bg="red").place(x=580, y=353)


        # Button to open the new window for data retrieval
        tk.Button(master, text="MyPasswords", command=self.open_password_window, font=("Arial", 18), bg="#ffc107").place(x=860, y=448)

        # Set the default special password
        self.default_special_password = "panda"

    def open_delete_website_window(self):
        website_to_delete = simpledialog.askstring("Delete Website", "Enter website to delete:")
        
        if website_to_delete:
            # Delete the website entry from the database
            delete_query = "DELETE FROM passwordmanager WHERE website = %s"
            data = (website_to_delete,)
            self.cursor.execute(delete_query, data)
            self.conn.commit()

            # Display success message
            message = f"Website: {website_to_delete}\nSuccessfully deleted from the database."
            tk.messagebox.showinfo("Website Deleted", message)
            self.clear_entries()
        else:
            tk.messagebox.showwarning("Error", "Please enter a website to delete.")


    def open_change_password_special_window(self):
        change_password_special_window = tk.Toplevel(self.master)
        change_password_special_window.title("Change Special Password")
        change_password_special_window.geometry("400x200")
        self.center_window(change_password_special_window, 400, 280)

        tk.Label(change_password_special_window, text="Enter current special password:", font=("Arial", 16)).pack(pady=10)

        current_password_entry = tk.Entry(change_password_special_window, show="*", font=("Arial", 14), width=20)
        current_password_entry.pack(pady=10)

        tk.Label(change_password_special_window, text="Enter new special password:", font=("Arial", 16)).pack(pady=10)

        new_password_entry = tk.Entry(change_password_special_window, show="*", font=("Arial", 14), width=20)
        new_password_entry.pack(pady=10)

        change_button = tk.Button(change_password_special_window, text="Change Special Password", command=lambda: self.change_special_password(current_password_entry.get(), new_password_entry.get()), font=("Arial", 16), bg="#007BFF", fg="white")
        change_button.pack(pady=15)

    def open_password_window(self):
        password_window = tk.Toplevel(self.master)
        password_window.title("Enter Password")
        password_window.geometry("400x200")
        self.center_window(password_window, 400, 300)

        tk.Label(password_window, text="Enter your special password to\naccess yourPasswords:", font=("Arial", 16)).pack(pady=20)

        password_entry = tk.Entry(password_window, show="*", font=("Arial", 14), width=20)
        password_entry.pack(pady=10)

        self.showhide_button = tk.Button(password_window, text="Show", command=lambda: self.showhide_password(password_entry), font=("Arial", 13), bg="lightgreen")
        self.showhide_button.pack(pady=5)

        show_button = tk.Button(password_window, text="ShowPasswords", command=lambda: self.retrieve_data(password_entry.get()), font=("Arial", 16), bg="#ff1493")
        show_button.pack(pady=5)

        # Button to open the window for changing special password
        tk.Button(password_window, text="ChangeSpecialPassword", command=self.open_change_password_special_window, font=("Arial", 16), bg="#007BFF", fg="white").pack(pady=10)

    def change_special_password(self, current_password, new_password):
        # Check the current password against the stored password
        if current_password == self.default_special_password:
            # Update the special password
            self.default_special_password = new_password

            # Show a success message
            messagebox.showinfo("Special Password Changed", "Special password successfully changed.")
        else:
            # Show a warning if the current password is incorrect
            messagebox.showwarning("Invalid Password", "Please enter the correct current special password.")

    

    def open_change_password_window(self):
        change_password_window = tk.Toplevel(self.master)
        change_password_window.title("Change Password")
        change_password_window.geometry("400x200")
        self.center_window(change_password_window, 400, 280)

        tk.Label(change_password_window, text="Enter website name to change password:", font=("Arial", 16)).pack(pady=10)

        website_entry = tk.Entry(change_password_window, font=("Arial", 14), width=20)
        website_entry.pack(pady=10)

        tk.Label(change_password_window, text="Enter your new password:", font=("Arial", 16)).pack(pady=10)

        new_password_entry = tk.Entry(change_password_window, show="*", font=("Arial", 14), width=20)
        new_password_entry.pack(pady=10)

        change_button = tk.Button(change_password_window, text="Change Password", command=lambda: self.change_password(website_entry.get(), new_password_entry.get()), font=("Arial", 16), bg="#007BFF", fg="white")
        change_button.pack(pady=15)

    def change_password(self, website, new_password):
        # Update the password for the specified website in the database
        update_query = "UPDATE passwordmanager SET password = %s WHERE website = %s"
        data = (new_password, website)
        self.cursor.execute(update_query, data)
        self.conn.commit()

        # Show a success message
        if  website and new_password:
            messagebox.showinfo("Password Changed", f"Password for {website} successfully changed.")
        else:
            messagebox.showerror("Error", "You must fill out all fields.")

    

    def center_window(self, window, width, height):
        x = (window.winfo_screenwidth() - width) // 2
        y = (window.winfo_screenheight() - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def showhide_password(self, password_entry):
        if self.show_password:
            self.show_password = False
            password_entry.config(show="")
            self.showhide_button.config(text="Hide", bg="yellow") 

        else:
            self.show_password = True
            password_entry.config(show="*")
            self.showhide_button.config(text="Show", bg="lightgreen")

    
    def retrieve_data(self, entered_password):
        if entered_password == self.default_special_password:
            retrieve_query = "SELECT * FROM passwordmanager"
            self.cursor.execute(retrieve_query)
            data = self.cursor.fetchall()

            result_window = tk.Toplevel(self.master)
            result_window.title("Retrieved Data")
            result_window.geometry("600x400")
            self.center_window(result_window, 600, 400)

            tk.Label(result_window, text="MyPasswords", font=("Arial", 20), fg="red").pack(pady=10)

            # Create a Text widget for displaying data with scrollbar
            text_widget = tk.Text(result_window, font=("Arial", 16), wrap="word", height=10, width=50)
            text_widget.pack(pady=10, padx=10, expand=True, fill="both")

            # Create a Scrollbar
            scrollbar = tk.Scrollbar(result_window, command=text_widget.yview)
            scrollbar.pack(side="left", fill="y")

            # Configure the Text widget to use the scrollbar
            text_widget.config(yscrollcommand=scrollbar.set)

            for entry in data:
                text_widget.insert(tk.END, f"Website: {entry[1]}\nUsername: {entry[2]}\nPassword: {entry[3]}\n\n")

        else:
            messagebox.showwarning("Invalid Password", "Please enter the correct special password.")

    def showhide(self):
        if self.show_password:
            self.show_password = False
            self.password_entry.config(show="*")
            self.show_hide_button.config(text="Show", bg="lightgreen")  # Update button text to "Show"
        else:
            self.show_password = True
            self.password_entry.config(show="")
            self.show_hide_button.config(text="Hide", bg="yellow")  # Update button text to "Hide"

    def add_password(self):
        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if website and username and password:
            # Insert data into the database
            insert_query = "INSERT INTO passwordmanager (website, username, password) VALUES (%s, %s, %s)"
            data = (website, username, password)
            self.cursor.execute(insert_query, data)
            self.conn.commit()

            # Display success message
            message = f"Website: {website}\nUsername: {username}\nPassword: {password}\n\nSuccessfully added to the database."
            tk.messagebox.showinfo("Password Added", message)
            self.clear_entries()
        else:
            tk.messagebox.showwarning("Error", "Please fill in all fields.")

    def clear_entries(self):
        self.website_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def exit_app(self):
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManager(root)
    root.mainloop()
