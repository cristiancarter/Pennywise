# Pennywise 💰

Pennywise is a personal finance management application that helps you track your transactions, visualize your spending through charts, and export your financial data. This README provides an overview of its features, installation steps, and usage instructions.

## Features

### 1. Add Transactions 📝
- **Description:** Easily log your financial transactions with details like amount, category, and date.
- **Usage:** Click the "Add Transaction" button to open a form where you can enter transaction details. The amount is automatically prefixed with '£', and the date defaults to the current date.

### 2. View Transactions 📅
- **Description:** View all your transactions or filter them by date range.
- **Usage:** Click the "View Transactions" button to open a window where you can enter a start and end date to filter transactions. The results are displayed in a table.

### 3. Export Transactions 🗂️
- **Description:** Export your transaction data to a CSV file for specific date ranges or all transactions.
- **Usage:** Click the "Export Transactions" button, select a folder, and choose whether to export all transactions or those within a specified date range.

### 4. Visualize Spending with Charts 📊
- **Description:** Visualize your spending patterns with pie and bar charts.
- **Usage:** 
  - **Pie Chart:** Click the "Show Pie Chart" button to view a pie chart showing the distribution of expenses by category.
  - **Bar Chart:** Click the "Show Bar Chart" button to view a bar chart representing the total amount spent in each category.


## Installation

To run the Pennywise application, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/Pennywise.git
   cd Pennywise
   ```

2. **Install the Required Dependencies**:
   The application uses the `matplotlib` library for charting, which needs to be installed. Other modules such as `csv`, `datetime`, `tkinter`, and `os` are part of the Python standard library and do not require separate installation.
   
   To install `matplotlib`, run:
   ```bash
   pip install matplotlib
   ```

3. **Run the Application**:
   Start the application by running:
   ```bash
   python app.py
   ```
   Ensure that the `appicon.png` file is present in the project directory to set the application icon.

## Usage

1. **Start the App:** After running the application, the main window of Pennywise will appear.
2. **Add Transactions:** Click on "Add Transaction" to log your expenses.
3. **View Transactions:** Use the "View Transactions" feature to see your expenses over a selected date range.
4. **Export Data:** Export your financial data as needed.
5. **Visualize Spending:** Use the chart options to get insights into your spending habits.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any feature requests, bug fixes, or enhancements.
