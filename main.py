import csv
import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

# Transaction categories
categories = [
    "Transport", "Food", "Utilities", "Entertainment", "Health",
    "Shopping", "Education", "Business Expenses", "Housing", "Travel",
    "Gifts", "Savings", "Investments", "Charity", "Personal Care", "Other"
]

# List to hold transaction records
transactions = []

class Pennywise:
    def __init__(self, master):
        self.master = master
        self.master.title("Pennywise")
        self.master.geometry("800x600")
        self.master.configure(bg="#f0f0f0")

        # Set the app icon
        self.set_app_icon()

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", padding=10, font=("Arial", 12))
        self.style.configure("TLabel", font=("Arial", 12), background="#f0f0f0")
        self.style.configure("TEntry", font=("Arial", 12))

        self.create_widgets()
        self.chart_window = None

    def set_app_icon(self):
        icon_path = "appicon.png"  
        if os.path.exists(icon_path):
            if os.name == 'nt': 
                self.master.iconbitmap(icon_path)
            else:  
                icon_img = tk.PhotoImage(file=icon_path)
                self.master.iconphoto(True, icon_img)

    def create_widgets(self):
        main_frame = ttk.Frame(self.master, padding="20")
        main_frame.pack(expand=True, fill="both")

        ttk.Button(main_frame, text="Add Transaction", command=self.add_transaction_gui).pack(pady=10, fill="x")
        ttk.Button(main_frame, text="View Transactions", command=self.view_transactions_gui).pack(pady=10, fill="x")
        ttk.Button(main_frame, text="Export Transactions", command=self.export_transactions_gui).pack(pady=10, fill="x")
        ttk.Button(main_frame, text="Show Pie Chart", command=lambda: self.show_chart_gui("pie")).pack(pady=10, fill="x")
        ttk.Button(main_frame, text="Show Bar Chart", command=lambda: self.show_chart_gui("bar")).pack(pady=10, fill="x")

    def add_transaction_gui(self):
        add_window = tk.Toplevel(self.master)
        add_window.title("Add Transaction")
        add_window.geometry("400x500")
        add_window.configure(bg="#f0f0f0")

        frame = ttk.Frame(add_window, padding="20")
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text="Amount:").grid(row=0, column=0, sticky="w", pady=5)
        amount_entry = ttk.Entry(frame)
        amount_entry.grid(row=0, column=1, sticky="ew", pady=5)

        ttk.Label(frame, text="Category:").grid(row=1, column=0, sticky="w", pady=5)
        category_var = tk.StringVar()
        category_combo = ttk.Combobox(frame, textvariable=category_var, values=categories, state="readonly")
        category_combo.grid(row=1, column=1, sticky="ew", pady=5)
        category_combo.set(categories[0])

        ttk.Label(frame, text="Date (DD-MM-YYYY):").grid(row=2, column=0, sticky="w", pady=5)
        date_entry = ttk.Entry(frame)
        date_entry.grid(row=2, column=1, sticky="ew", pady=5)
        date_entry.insert(0, datetime.datetime.now().strftime("%d-%m-%Y"))

        ttk.Button(frame, text="Add Transaction", command=lambda: self.save_transaction(
            amount_entry.get(), category_var.get(), date_entry.get(), add_window
        )).grid(row=3, column=0, columnspan=2, pady=20)

    def save_transaction(self, amount, category, date_str, window):
        if not amount.startswith('£'):
            amount = '£' + amount
        try:
            date = datetime.datetime.strptime(date_str, "%d-%m-%Y")
        except ValueError:
            messagebox.showerror("Error", "Date format should be DD-MM-YYYY")
            return
        transactions.append({
            "amount": amount,
            "category": category,
            "date": date
        })
        messagebox.showinfo("Success", "Transaction added successfully!")
        window.destroy()
        self.update_charts()

    def view_transactions_gui(self):
        view_window = tk.Toplevel(self.master)
        view_window.title("View Transactions")
        view_window.geometry("600x400")
        view_window.configure(bg="#f0f0f0")

        frame = ttk.Frame(view_window, padding="20")
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text="Start Date (DD-MM-YYYY):").grid(row=0, column=0, sticky="w", pady=5)
        start_date_entry = ttk.Entry(frame)
        start_date_entry.grid(row=0, column=1, sticky="ew", pady=5)

        ttk.Label(frame, text="End Date (DD-MM-YYYY):").grid(row=1, column=0, sticky="w", pady=5)
        end_date_entry = ttk.Entry(frame)
        end_date_entry.grid(row=1, column=1, sticky="ew", pady=5)

        tree = ttk.Treeview(frame, columns=("Date", "Amount", "Category"), show="headings")
        tree.heading("Date", text="Date")
        tree.heading("Amount", text="Amount")
        tree.heading("Category", text="Category")
        tree.grid(row=2, column=0, columnspan=2, pady=10, sticky="nsew")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scrollbar.grid(row=2, column=2, sticky="ns")
        tree.configure(yscrollcommand=scrollbar.set)

        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)

        def show_transactions():
            for item in tree.get_children():
                tree.delete(item)

            start_date_str = start_date_entry.get()
            end_date_str = end_date_entry.get()
            try:
                start_date = datetime.datetime.strptime(start_date_str, "%d-%m-%Y")
                end_date = datetime.datetime.strptime(end_date_str, "%d-%m-%Y")
            except ValueError:
                messagebox.showerror("Error", "Date format should be DD-MM-YYYY")
                return

            for transaction in transactions:
                if start_date <= transaction["date"] <= end_date:
                    tree.insert("", "end", values=(
                        transaction['date'].strftime('%d-%m-%Y'),
                        transaction['amount'],
                        transaction['category']
                    ))

        ttk.Button(frame, text="View Transactions", command=show_transactions).grid(row=3, column=0, columnspan=2, pady=10)

    def export_transactions_gui(self):
        folder_path = filedialog.askdirectory(title="Select a folder to save the files")

        if folder_path:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            export_folder = os.path.join(folder_path, f"financial_data_{timestamp}")
            os.makedirs(export_folder, exist_ok=True)

            export_type = simpledialog.askstring("Export Type", "Export (1) specific time range or (2) all transactions? Enter 1 or 2:")

            if export_type == '1':
                start_date_str = simpledialog.askstring("Start Date", "Enter the start date (DD-MM-YYYY):")
                end_date_str = simpledialog.askstring("End Date", "Enter the end date (DD-MM-YYYY):")
                try:
                    start_date = datetime.datetime.strptime(start_date_str, "%d-%m-%Y")
                    end_date = datetime.datetime.strptime(end_date_str, "%d-%m-%Y")
                except ValueError:
                    messagebox.showerror("Error", "Date format should be DD-MM-YYYY")
                    return

                transactions_to_export = [t for t in transactions if start_date <= t["date"] <= end_date]
                csv_file_path = os.path.join(export_folder, "transactions_range.csv")
            elif export_type == '2':
                transactions_to_export = transactions
                csv_file_path = os.path.join(export_folder, "transactions_all.csv")
            else:
                messagebox.showerror("Error", "Invalid choice. Export cancelled.")
                return

            with open(csv_file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Amount", "Category"])
                for transaction in transactions_to_export:
                    writer.writerow([transaction["date"].strftime('%d-%m-%Y'), transaction["amount"], transaction["category"]])
            messagebox.showinfo("Success", f"Transactions exported to {csv_file_path} successfully!")

            self.export_charts(export_folder)

    def export_charts(self, folder):
        pie_chart_path = os.path.join(folder, "transaction_distribution_pie.png")
        bar_chart_path = os.path.join(folder, "transaction_distribution_bar.png")

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
        self.generate_pie_chart(ax1)
        self.generate_bar_chart(ax2)
        plt.tight_layout()
        plt.savefig(os.path.join(folder, "transaction_distribution_combined.png"))
        plt.close()

        messagebox.showinfo("Success", f"Charts exported to {folder} successfully!")

    def show_chart_gui(self, chart_type):
        if self.chart_window:
            self.chart_window.destroy()

        self.chart_window = tk.Toplevel(self.master)
        self.chart_window.title(f"Financial Tracker - {chart_type.capitalize()} Chart")
        self.chart_window.geometry("800x600")

        fig, ax = plt.subplots(figsize=(10, 7))
        canvas = FigureCanvasTkAgg(fig, master=self.chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        if chart_type == "pie":
            self.generate_pie_chart(ax)
        elif chart_type == "bar":
            self.generate_bar_chart(ax)

        self.chart_window.protocol("WM_DELETE_WINDOW", self.close_chart_window)

    def close_chart_window(self):
        if self.chart_window:
            self.chart_window.destroy()
            self.chart_window = None

    def update_charts(self):
        if self.chart_window:
            for widget in self.chart_window.winfo_children():
                widget.destroy()
            
            fig, ax = plt.subplots(figsize=(10, 7))
            canvas = FigureCanvasTkAgg(fig, master=self.chart_window)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            if "Pie" in self.chart_window.title():
                self.generate_pie_chart(ax)
            elif "Bar" in self.chart_window.title():
                self.generate_bar_chart(ax)

    def generate_pie_chart(self, ax, top_n=8):
        category_totals = {category: 0 for category in categories}
        for transaction in transactions:
            category_totals[transaction["category"]] += float(transaction["amount"].replace('£', ''))
        
        sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
        top_categories = sorted_categories[:top_n]
        other_total = sum(total for _, total in sorted_categories[top_n:])
        
        labels = [category for category, _ in top_categories]
        sizes = [total for _, total in top_categories]
        
        if other_total > 0:
            labels.append('Other')
            sizes.append(other_total)

        ax.clear()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        ax.set_title('Transaction Distribution by Category')

    def generate_bar_chart(self, ax):
        category_totals = {category: 0 for category in categories}
        for transaction in transactions:
            category_totals[transaction["category"]] += float(transaction["amount"].replace('£', ''))

        labels = list(category_totals.keys())
        sizes = list(category_totals.values())

        ax.clear()
        ax.bar(labels, sizes, color='skyblue')
        ax.set_title('Transaction Totals by Category')
        ax.set_xlabel('Category')
        ax.set_ylabel('Total Amount (£)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

if __name__ == "__main__":
    root = tk.Tk()
    app = Pennywise(root)
    root.mainloop()