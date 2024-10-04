pip install pandas matplotlib
date,category,amount
2024-10-01,Salary,5000
2024-10-02,Groceries,-150
2024-10-03,Entertainment,-50
import pandas as pd
import matplotlib.pyplot as plt

# Function to add a new transaction
def add_transaction(date, category, amount):
    data = {'date': [date], 'category': [category], 'amount': [amount]}
    df = pd.DataFrame(data)
    df.to_csv('finance_data.csv', mode='a', header=False, index=False)

# Function to read and analyze data
def analyze_data():
    df = pd.read_csv('finance_data.csv')
    print("Total Income: ", df[df['amount'] > 0]['amount'].sum())
    print("Total Expenses: ", df[df['amount'] < 0]['amount'].sum())
    print("Net Savings: ", df['amount'].sum())

# Function to visualize data
def visualize_data():
    df = pd.read_csv('finance_data.csv')
    df.groupby('category')['amount'].sum().plot(kind='pie', autopct='%1.1f%%')
    plt.title('Expense Categories')
    plt.show()

# Example usage
add_transaction('2024-10-04', 'Transport', -20)
analyze_data()
visualize_data()
