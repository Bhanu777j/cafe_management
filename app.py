from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Bhanu@4544",
    database="cafe_db"
)

cursor = db.cursor()

# Home Page
@app.route('/')
def home():
    return render_template("index.html")


# Order Route
@app.route('/order', methods=['POST'])
def order():

    selected_items = request.form.getlist('items')

    total_bill = 0
    items_list = []

    # Create new bill first
    cursor.execute("INSERT INTO bills (total) VALUES (0)")
    db.commit()

    bill_id = cursor.lastrowid

    for item_id in selected_items:

        cursor.execute(
            "SELECT item_name, price FROM orders WHERE id=%s",
            (item_id,)
        )

        result = cursor.fetchone()

        if result:
            item_name, price = result

            qty = int(request.form.get(f"qty_{item_id}", 1))

            item_total = price * qty
            total_bill += item_total

            items_list.append((item_name, qty, item_total))

            # Insert into bill_items
            cursor.execute(
                "INSERT INTO bill_items (bill_id, item_name, quantity, price, total) VALUES (%s,%s,%s,%s,%s)",
                (bill_id, item_name, qty, price, item_total)
            )

    # Update total bill
    cursor.execute(
        "UPDATE bills SET total=%s WHERE bill_id=%s",
        (total_bill, bill_id)
    )

    db.commit()

    return render_template(
        "bill.html",
        items=items_list,
        total=total_bill
    )


if __name__ == "__main__":
    app.run(debug=True)