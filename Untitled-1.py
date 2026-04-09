Python 3.13.5 (tags/v3.13.5:6cb20a2, Jun 11 2025, 16:15:46) [MSC v.1943 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
    import tkinter as tk
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from collections import defaultdict
import os

class ExpenseTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Expense Tracker")
        self.root.geometry("1200x700")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize database
        self.db_name = "expenses.db"
        self.conn = sqlite3.connect(self.db_name)
        self.create_tables()
        
        # Create GUI
        self.create_widgets()
        self.refresh_expense_list()
        
    def create_tables(self):
        """Create necessary tables if they don't exist"""
        cursor = self.conn.cursor()
        
        # Create expenses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                date TEXT NOT NULL,
                payment_method TEXT DEFAULT 'Cash'
            )
        ''')
        
        # Create categories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                budget_limit REAL DEFAULT 0
            )
        ''')
        
        # Insert default categories if table is empty
        cursor.execute("SELECT COUNT(*) FROM categories")
        if cursor.fetchone()[0] == 0:
            default_categories = [
                ('Food', 500), ('Transportation', 200), ('Entertainment', 150),
                ('Shopping', 300), ('Bills', 400), ('Healthcare', 200),
                ('Education', 100), ('Others', 100)
            ]
            cursor.executemany(
                "INSERT INTO categories (name, budget_limit) VALUES (?, ?)",
                default_categories
            )
        
        self.conn.commit()
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="💰 Personal Expense Tracker", 
                               font=('Arial', 20, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Left panel for input
        self.create_input_panel(main_frame)
        
        # Right panel for expense list and stats
        self.create_display_panel(main_frame)
        
        # Bottom panel for buttons
        self.create_button_panel(main_frame)
    
    def create_input_panel(self, parent):
        """Create input panel"""
        input_frame = ttk.LabelFrame(parent, text="Add New Expense", padding="10")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Amount
        ttk.Label(input_frame, text="Amount ($):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.amount_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.amount_var, width=15).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Category
        ttk.Label(input_frame, text="Category:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(input_frame, textvariable=self.category_var, width=15)
        self.category_combo.grid(row=1, column=1, sticky=tk.W, pady=5)
        self.update_category_list()
        
        # Description
        ttk.Label(input_frame, text="Description:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.description_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.description_var, width=15).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Date
        ttk.Label(input_frame, text="Date:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.date_var = tk.StringVar(value=datetime.datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(input_frame, textvariable=self.date_var, width=15).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Payment Method
        ttk.Label(input_frame, text="Payment:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.payment_var = tk.StringVar(value="Cash")
        payment_combo = ttk.Combobox(input_frame, textvariable=self.payment_var, 
                                   values=["Cash", "Card", "Online", "Check"], width=15)
        payment_combo.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Add button
        ttk.Button(input_frame, text="Add Expense", command=self.add_expense, 
                  style='Accent.TButton').grid(row=5, column=0, columnspan=2, pady=20)
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(input_frame, text="Quick Stats", padding="10")
        stats_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(20, 0))
        
        self.stats_label = ttk.Label(stats_frame, text="", font=('Arial', 9))
        self.stats_label.grid(row=0, column=0, sticky=tk.W)
        
        self.update_stats()
    
    def create_display_panel(self, parent):
        """Create display panel"""
        display_frame = ttk.LabelFrame(parent, text="Recent Expenses", padding="10")
        display_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(0, weight=1)
        
        # Create Treeview
        columns = ('ID', 'Amount', 'Category', 'Description', 'Date', 'Payment')
        self.expense_tree = ttk.Treeview(display_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        self.expense_tree.heading('ID', text='ID')
        self.expense_tree.heading('Amount', text='Amount ($)')
        self.expense_tree.heading('Category', text='Category')
        self.expense_tree.heading('Description', text='Description')
        self.expense_tree.heading('Date', text='Date')
        self.expense_tree.heading('Payment', text='Payment')
        
        # Configure column widths
        self.expense_tree.column('ID', width=50)
        self.expense_tree.column('Amount', width=80)
        self.expense_tree.column('Category', width=100)
        self.expense_tree.column('Description', width=150)
        self.expense_tree.column('Date', width=100)
        self.expense_tree.column('Payment', width=80)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.expense_tree.yview)
        self.expense_tree.configure(yscroll=scrollbar.set)
        
        # Grid treeview and scrollbar
        self.expense_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bind double-click to edit
        self.expense_tree.bind('<Double-1>', self.edit_expense)
    
    def create_button_panel(self, parent):
        """Create button panel"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Buttons
        ttk.Button(button_frame, text="📊 View Statistics", 
                  command=self.show_statistics).grid(row=0, column=0, padx=5)
        
        ttk.Button(button_frame, text="📈 Show Graphs", 
                  command=self.show_graphs).grid(row=0, column=1, padx=5)
        
        ttk.Button(button_frame, text="🏷️ Manage Categories", 
                  command=self.manage_categories).grid(row=0, column=2, padx=5)
        
        ttk.Button(button_frame, text="🔍 Search", 
                  command=self.search_expenses).grid(row=0, column=3, padx=5)
        
        ttk.Button(button_frame, text="📤 Export Data", 
                  command=self.export_data).grid(row=0, column=4, padx=5)
        
        ttk.Button(button_frame, text="🗑️ Delete Selected", 
                  command=self.delete_expense).grid(row=0, column=5, padx=5)
        
        ttk.Button(button_frame, text="🔄 Refresh", 
                  command=self.refresh_expense_list).grid(row=0, column=6, padx=5)
    
    def update_category_list(self):
        """Update category combobox"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM categories ORDER BY name")
        categories = [row[0] for row in cursor.fetchall()]
        self.category_combo['values'] = categories
        if categories:
            self.category_combo.set(categories[0])
    
    def add_expense(self):
        """Add new expense"""
        try:
            amount = float(self.amount_var.get())
            category = self.category_var.get()
            description = self.description_var.get()
            date = self.date_var.get()
            payment_method = self.payment_var.get()
            
            if not category:
                messagebox.showerror("Error", "Please select a category!")
                return
            
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO expenses (amount, category, description, date, payment_method)
                VALUES (?, ?, ?, ?, ?)
            ''', (amount, category, description, date, payment_method))
            
            self.conn.commit()
            
            # Clear inputs
            self.amount_var.set("")
            self.description_var.set("")
            self.date_var.set(datetime.datetime.now().strftime("%Y-%m-%d"))
            
            # Refresh display
            self.refresh_expense_list()
            self.update_stats()
            self.check_budget_warning(category)
            
            messagebox.showinfo("Success", f"Expense of ${amount:.2f} added successfully!")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def refresh_expense_list(self):
        """Refresh expense list"""
        # Clear existing items
        for item in self.expense_tree.get_children():
            self.expense_tree.delete(item)
        
        # Fetch recent expenses
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM expenses 
            ORDER BY date DESC, id DESC 
            LIMIT 50
        ''')
        expenses = cursor.fetchall()
        
        # Insert into treeview
        for expense in expenses:
            self.expense_tree.insert('', 'end', values=expense)
    
    def edit_expense(self, event):
        """Edit selected expense"""
        selection = self.expense_tree.selection()
        if not selection:
            return
        
        item = self.expense_tree.item(selection[0])
        expense_data = item['values']
        
        # Create edit window
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Expense")
        edit_window.geometry("300x400")
        edit_window.grab_set()
        
        # Variables
        edit_amount = tk.StringVar(value=str(expense_data[1]))
        edit_category = tk.StringVar(value=expense_data[2])
        edit_description = tk.StringVar(value=expense_data[3])
        edit_date = tk.StringVar(value=expense_data[4])
        edit_payment = tk.StringVar(value=expense_data[5])
        
        # Create form
        ttk.Label(edit_window, text="Amount ($):").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        ttk.Entry(edit_window, textvariable=edit_amount).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(edit_window, text="Category:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        category_edit_combo = ttk.Combobox(edit_window, textvariable=edit_category)
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM categories ORDER BY name")
        category_edit_combo['values'] = [row[0] for row in cursor.fetchall()]
        category_edit_combo.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(edit_window, text="Description:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        ttk.Entry(edit_window, textvariable=edit_description).grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(edit_window, text="Date:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        ttk.Entry(edit_window, textvariable=edit_date).grid(row=3, column=1, padx=10, pady=5)
        
        ttk.Label(edit_window, text="Payment:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        payment_edit_combo = ttk.Combobox(edit_window, textvariable=edit_payment,
                                        values=["Cash", "Card", "Online", "Check"])
        payment_edit_combo.grid(row=4, column=1, padx=10, pady=5)
        
        def save_changes():
            try:
                cursor = self.conn.cursor()
                cursor.execute('''
                    UPDATE expenses 
                    SET amount=?, category=?, description=?, date=?, payment_method=?
                    WHERE id=?
                ''', (float(edit_amount.get()), edit_category.get(), edit_description.get(),
                     edit_date.get(), edit_payment.get(), expense_data[0]))
                
                self.conn.commit()
                self.refresh_expense_list()
                self.update_stats()
                edit_window.destroy()
                messagebox.showinfo("Success", "Expense updated successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        ttk.Button(edit_window, text="Save Changes", command=save_changes).grid(row=5, column=0, columnspan=2, pady=20)
    
    def delete_expense(self):
        """Delete selected expense"""
        selection = self.expense_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an expense to delete!")
            return
        
        item = self.expense_tree.item(selection[0])
        expense_data = item['values']
        
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete the expense of ${expense_data[1]} for {expense_data[2]}?"):
            
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_data[0],))
            self.conn.commit()
            
            self.refresh_expense_list()
            self.update_stats()
            messagebox.showinfo("Success", "Expense deleted successfully!")
    
    def update_stats(self):
        """Update quick statistics"""
        cursor = self.conn.cursor()
        
        # Total expenses this month
        current_month = datetime.datetime.now().strftime("%Y-%m")
        cursor.execute('''
            SELECT SUM(amount), COUNT(*) FROM expenses 
            WHERE strftime('%Y-%m', date) = ?
        ''', (current_month,))
        
        result = cursor.fetchone()
        total_month = result[0] or 0
        count_month = result[1] or 0
        
        # Total all time
        cursor.execute("SELECT SUM(amount), COUNT(*) FROM expenses")
        result = cursor.fetchone()
        total_all = result[0] or 0
        count_all = result[1] or 0
        
        stats_text = f"This Month: ${total_month:.2f} ({count_month} transactions)\n"
        stats_text += f"All Time: ${total_all:.2f} ({count_all} transactions)"
        
        self.stats_label.config(text=stats_text)
    
    def show_statistics(self):
        """Show detailed statistics window"""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Expense Statistics")
        stats_window.geometry("600x500")
        stats_window.grab_set()
        
        # Create notebook for different periods
        notebook = ttk.Notebook(stats_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        periods = [("This Month", "month"), ("This Year", "year"), ("All Time", "all")]
        
        for period_name, period_code in periods:
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=period_name)
            
            # Calculate date range
            today = datetime.datetime.now()
            if period_code == "month":
                start_date = today.replace(day=1).strftime("%Y-%m-%d")
            elif period_code == "year":
                start_date = today.replace(month=1, day=1).strftime("%Y-%m-%d")
            else:
                start_date = "1900-01-01"
            
            # Get statistics
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT category, SUM(amount), COUNT(*), AVG(amount)
                FROM expenses 
                WHERE date >= ?
                GROUP BY category 
                ORDER BY SUM(amount) DESC
            ''', (start_date,))
            
            category_stats = cursor.fetchall()
            
            # Create treeview for category stats
            columns = ('Category', 'Total', 'Count', 'Average')
            stats_tree = ttk.Treeview(frame, columns=columns, show='headings')
            
            for col in columns:
                stats_tree.heading(col, text=col)
                stats_tree.column(col, width=120)
            
            total_amount = 0
            for stat in category_stats:
                stats_tree.insert('', 'end', values=(
                    stat[0], f"${stat[1]:.2f}", stat[2], f"${stat[3]:.2f}"
                ))
                total_amount += stat[1]
            
            stats_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Total label
            total_label = ttk.Label(frame, text=f"Total Spent: ${total_amount:.2f}", 
                                  font=('Arial', 12, 'bold'))
            total_label.pack(pady=10)
    
    def show_graphs(self):
        """Show graphs window"""
        graph_window = tk.Toplevel(self.root)
        graph_window.title("Expense Graphs")
        graph_window.geometry("1000x700")
        graph_window.grab_set()
        
        # Create notebook for different graphs
        notebook = ttk.Notebook(graph_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Category pie chart
        self.create_category_pie_chart(notebook)
        
        # Monthly trend
        self.create_monthly_trend_chart(notebook)
        
        # Payment method chart
        self.create_payment_method_chart(notebook)
    
    def create_category_pie_chart(self, notebook):
        """Create category pie chart"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Category Distribution")
        
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT category, SUM(amount) 
            FROM expenses 
            GROUP BY category 
            ORDER BY SUM(amount) DESC
        ''')
        data = cursor.fetchall()
        
        if not data:
            ttk.Label(frame, text="No data available").pack()
            return
        
        fig, ax = plt.subplots(figsize=(8, 6))
        categories = [row[0] for row in data]
        amounts = [row[1] for row in data]
        
        ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
        ax.set_title('Expenses by Category')
        
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def create_monthly_trend_chart(self, notebook):
        """Create monthly trend chart"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Monthly Trend")
        
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT strftime('%Y-%m', date) as month, SUM(amount)
            FROM expenses
            GROUP BY strftime('%Y-%m', date)
            ORDER BY month
        ''')
        data = cursor.fetchall()
        
        if not data:
            ttk.Label(frame, text="No data available").pack()
            return
        
        fig, ax = plt.subplots(figsize=(8, 6))
        months = [row[0] for row in data]
        amounts = [row[1] for row in data]
        
        ax.plot(months, amounts, marker='o', linewidth=2, markersize=6)
        ax.set_title('Monthly Spending Trend')
        ax.set_xlabel('Month')
        ax.set_ylabel('Amount ($)')
        plt.xticks(rotation=45)
        
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def create_payment_method_chart(self, notebook):
        """Create payment method chart"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Payment Methods")
        
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT payment_method, SUM(amount)
            FROM expenses
            GROUP BY payment_method
            ORDER BY SUM(amount) DESC
        ''')
        data = cursor.fetchall()
        
        if not data:
            ttk.Label(frame, text="No data available").pack()
            return
        
        fig, ax = plt.subplots(figsize=(8, 6))
        methods = [row[0] for row in data]
        amounts = [row[1] for row in data]
        
        ax.bar(methods, amounts, color=['skyblue', 'lightcoral', 'lightgreen', 'gold'])
        ax.set_title('Expenses by Payment Method')
        ax.set_xlabel('Payment Method')
        ax.set_ylabel('Amount ($)')
        
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def manage_categories(self):
        """Manage categories window"""
        cat_window = tk.Toplevel(self.root)
        cat_window.title("Manage Categories")
        cat_window.geometry("500x400")
        cat_window.grab_set()
        
        # Category list
        list_frame = ttk.LabelFrame(cat_window, text="Categories", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ('ID', 'Name', 'Budget Limit')
        cat_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            cat_tree.heading(col, text=col)
            cat_tree.column(col, width=120)
        
        cat_tree.pack(fill=tk.BOTH, expand=True)
        
        # Input frame
        input_frame = ttk.LabelFrame(cat_window, text="Add Category", padding="10")
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(input_frame, text="Name:").grid(row=0, column=0, sticky=tk.W)
        cat_name_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=cat_name_var).grid(row=0, column=1, padx=5)
        
        ttk.Label(input_frame, text="Budget:").grid(row=0, column=2, sticky=tk.W, padx=(20,0))
        cat_budget_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=cat_budget_var).grid(row=0, column=3, padx=5)
        
        def add_category():
            try:
                name = cat_name_var.get().strip()
                budget = float(cat_budget_var.get() or 0)
                
                if not name:
                    messagebox.showerror("Error", "Please enter category name!")
                    return
                
                cursor = self.conn.cursor()
                cursor.execute("INSERT INTO categories (name, budget_limit) VALUES (?, ?)", 
                             (name, budget))
                self.conn.commit()
                
                cat_name_var.set("")
                cat_budget_var.set("")
                refresh_categories()
                self.update_category_list()
                messagebox.showinfo("Success", "Category added successfully!")
                
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Category already exists!")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid budget amount!")
        
        def refresh_categories():
            for item in cat_tree.get_children():
                cat_tree.delete(item)
            
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM categories ORDER BY name")
            categories = cursor.fetchall()
            
            for cat in categories:
                cat_tree.insert('', 'end', values=cat)
        
        ttk.Button(input_frame, text="Add Category", command=add_category).grid(row=0, column=4, padx=10)
        
        refresh_categories()
    
    def search_expenses(self):
        """Search expenses"""
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Expenses")
        search_window.geometry("700x500")
        search_window.grab_set()
        
        # Search frame
        search_frame = ttk.Frame(search_window, padding="10")
        search_frame.pack(fill=tk.X)
        
        ttk.Label(search_frame, text="Search:").grid(row=0, column=0, sticky=tk.W)
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var, width=30)
        search_entry.grid(row=0, column=1, padx=5)
        
        # Results frame
        results_frame = ttk.LabelFrame(search_window, text="Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ('ID', 'Amount', 'Category', 'Description', 'Date')
        results_tree = ttk.Treeview(results_frame, columns=columns, show='headings')
        
        for col in columns:
            results_tree.heading(col, text=col)
            results_tree.column(col, width=120)
        
        results_tree.pack(fill=tk.BOTH, expand=True)
        
        def perform_search():
            keyword = search_var.get().strip()
            if not keyword:
                return
            
            for item in results_tree.get_children():
                results_tree.delete(item)
            
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT * FROM expenses 
                WHERE description LIKE ? OR category LIKE ?
                ORDER BY date DESC
            ''', (f'%{keyword}%', f'%{keyword}%'))
            
            results = cursor.fetchall()
            
            for result in results:
                results_tree.insert('', 'end', values=result[:-1])  # Exclude payment method for space
        
        ttk.Button(search_frame, text="Search", command=perform_search).grid(row=0, column=2, padx=5)
        search_entry.bind('<Return>', lambda e: perform_search())
    
    def export_data(self):
        """Export data to CSV"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
            expenses = cursor.fetchall()
            
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                file.write("ID,Amount,Category,Description,Date,Payment_Method\n")
                for expense in expenses:
                    file.write(f"{expense[0]},{expense[1]},{expense[2]},{expense[3]},{expense[4]},{expense[5]}\n")
            
            messagebox.showinfo("Success", f"Data exported to {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def check_budget_warning(self, category):
        """Check if spending exceeds budget limit"""
        cursor = self.conn.cursor()
        
        # Get budget limit for category
        cursor.execute("SELECT budget_limit FROM categories WHERE name = ?", (category,))
        result = cursor.fetchone()
        
        if not result or result[0] == 0:
            return  # No budget limit set
        
        budget_limit = result[0]
        
        # Get current month spending for this category
        current_month = datetime.datetime.now().strftime("%Y-%m")
        cursor.execute('''
            SELECT SUM(amount) FROM expenses 
            WHERE category = ? AND strftime('%Y-%m', date) = ?
        ''', (category, current_month))
        
        current_spending = cursor.fetchone()[0] or 0
        
        if current_spending > budget_limit:
            messagebox.showwarning("Budget Alert", 
                f"⚠️ You've exceeded your {category} budget!\n"
                f"Budget: ${budget_limit:.2f}\n"
                f"Spent: ${current_spending:.2f}")
        elif current_spending > budget_limit * 0.8:
            messagebox.showinfo("Budget Notice", 
                f"💡 You're at {(current_spending/budget_limit)*100:.1f}% of your {category} budget\n"
                f"Budget: ${budget_limit:.2f}\n"
                f"Spent: ${current_spending:.2f}")
    
    def __del__(self):
        """Close database connection"""
        if hasattr(self, 'conn'):
            self.conn.close()

def main():
    root = tk.Tk()
    
    # Set style
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure custom styles
    style.configure('Accent.TButton', foreground='white', background='#007acc')
    style.map('Accent.TButton', background=[('active', '#005999')])
    
    app = ExpenseTrackerGUI(root)
    
    # Handle window close
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            app.conn.close()
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
[DEBUG ON]
[DEBUG OFF]
