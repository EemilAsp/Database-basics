
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure
from bokeh.palettes import Spectral5
from asyncio.windows_events import NULL
from pickle import NONE
import sqlite3
db = sqlite3.connect(r"C:\Users\eemil\Project.db")
cur = db.cursor()
def initializeDB():
    try:
        f = open("sqlcommands.sql", "r")
        commandstring = ""
        for line in f.readlines():
            commandstring+=line
        cur.executescript(commandstring)
    except sqlite3.OperationalError:
        print("Database exists, skip initialization")

def main():
    userInput = -1
    while(userInput != "0"):
        print("\nMenu options:")
        print("1: Print sales made by employee")
        print("2: Print sales by product")
        print("3: Insert new table")
        print("4: Activate discounts!")
        print("5: Visualize sales")
        print("0: Quit")
        userInput = input("What do you want to do? ")
        print(userInput)
        if userInput == "1":
            salesbyEmployee()
        if userInput == "2":
            salesbyProduct()
        if userInput == "3":
            newTables()
        if userInput == "4":
            activateDiscount()
        if userInput == "5":
            visualizeSales()
        if userInput == "0":
            print("Thank you for using!")
    db.close()        
    return


def salesbyEmployee():
    print("Printing the sales made by each employee")
    print("Department|Salesman|OrderID|Product|Worth $")
    cur.execute('''Select department_name AS 'Department',
	                (Employees.first_name ||' '|| Employees.last_name) AS 'Salesman',
	                Orders.order_id AS 'OrderID',
	                Products.product_name AS 'Product',
	                ProductsOrders.cost AS 'Sales_Worth'
                    From Departments
                    Inner JOIN Employees ON Employees.department_id = Departments.department_id
                    Inner JOIN Orders ON Orders.employee_id = Employees.employee_id
                    INNER JOIN Products ON Products.product_id = ProductsOrders.product_id
                    INNER JOIN ProductsOrders ON ProductsOrders.order_id = Orders.order_id
                    ORDER BY Department''')
    result = cur.fetchall()
    for i in result:
        print(*i, sep='|')
    return

def salesbyProduct():
    print("Sales by customer")
    print("OrderID|Customer|worth $|Product")
    cur.execute('''Select  Orders.order_id AS OrderID,
		Customers.customer_name AS Customer,
		ProductsOrders.cost AS Sales_worth,
		Products.product_name AS Product
		From Orders
		Inner JOIN Customers ON customers.customer_id = Orders.customer_id
		Inner JOIN ProductsOrders ON ProductsOrders.order_id = Orders.order_id
		JOIN Products ON Products.product_id = ProductsOrders.product_id AND ProductsOrders.order_id = Orders.order_id
		Order by orderID''')
    result = cur.fetchall()
    for i in result:
        print(*i, sep='|')
    return

def newTables():
    name = ''
    while(True):
        name = input("Give customers name: ")
        if name:
            break
    email = input("Give customers email: ")
    number = input("Give customers phone number: ")
    cur.execute(''''Insert INTO CUSTOMERS (customer_name, customer_email, customer_number)
                VALUES ('=?', '=?', =?) ''',[name, email, number])
    cur.execute('Select * from Customers')
    result = cur.fetchall()
    print("Customer name|Customer email|Customer number")
    for i in result:
        print(*i, sep='|')
    return

def activateDiscount():
    x = int(input("Give discount discount pertentage '%' as whole number"))
    cur.execute('''Update Products SET price_per_unit = round((price_per_unit / ?),2) Where product_id IS NOT NULL''',[x,])
    cur.execute('''Update ProductsOrders SET cost = round((cost / ?),2) Where ProductsOrders.order_id IS NOT NULL''',[x,])
    if(x>25):
        print("Wow! Were going broke with %d sales percentage, hopefully the sales will increase!", x)
    return

def visualizeSales():
    output_file("colormapped_bars.html")
    xAxis = []
    sales = []
    cur.execute('''Select department_name AS 'Department',
	                COUNT(Orders.order_id) AS 'Orders_received',
	                SUM(ProductsOrders.cost) AS 'Total_worth'
                    From Departments
                    Inner JOIN Orders ON Orders.department_id = Departments.department_id
                    INNER JOIN ProductsOrders ON ProductsOrders.order_id = Orders.order_id
                    Group BY department_name
                    ORDER BY Department''')
    results = cur.fetchall()
    for i in range(0,5):
        xAxis.append(results[i][0])
        sales.append(results[i][2])
    source = ColumnDataSource(data=dict(xAxis=xAxis, sales=sales, color=Spectral5))
    barchart = figure(x_range=xAxis, y_range=(0,5000), height=250, title="Sales by department", toolbar_location=None, tools="")
    barchart.vbar(x='xAxis', top='sales', width=0.9, color='color', legend_field='xAxis', source=source)
    barchart.legend.orientation = "horizontal"
    barchart.legend.location = "top_center"
    show(barchart)
    return

main()