from flask import Flask, render_template, request, redirect
import json
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect("postgresql://Killer4537:v2_3xMsp_nsVGixdA4TAgmuUSZEchG4i@db.bit.io/Killer4537/CS50-Properties")



@app.route("/")
def index():
    cur = conn.cursor()
    cur.execute("SELECT * FROM property_data ORDER BY RANDOM() LIMIT 3;")
    data = cur.fetchall()
    cur.close()
    return render_template("home.html", data=data)


@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "GET":
        return redirect("/")
    else:
        maxprice = request.form.get("maxamount")
        minprice = request.form.get("minamount")
        postcode = request.form.get('postcode')
        sort = request.form.get('sortby')
        if not maxprice:
            maxprice = 70000000
        else:
            maxprice = int(maxprice)
        if not minprice:
            minprice = 0
        else:
            minprice = int(minprice)
        if not postcode:
            postcode=""
        else:
            postcode = postcode.capitalize()
        if maxprice < minprice:
            return render_template("error.html", msg="Max price is smaller than Minimum price. Please try a different range.")
        cur = conn.cursor()
        cur.execute("SELECT listing_id FROM property_data WHERE postalcode like '%{postcode}%';")
        if cur.fetchall() == None:
            return render_template("error.html", msg="Invalid Postcode, ensure there is a space between outcode and incode")
        cur.close()
        cur = conn.cursor()
        if sort == 'Asc':
            cur.execute("""
                SELECT * FROM property_data WHERE postalcode LIKE %s AND price BETWEEN %s AND %s
                ORDER BY price ASC
                """,
                ('%' + postcode + '%', minprice, maxprice)
                )
        elif sort == 'Desc':
            cur.execute("""
                SELECT * FROM property_data WHERE postalcode LIKE %s AND price BETWEEN %s AND %s
                ORDER BY price DESC
                """,
                ('%' + postcode + '%', minprice, maxprice)
                )
        else:
            cur.execute("""
                SELECT * FROM property_data WHERE postalcode LIKE %s AND price BETWEEN %s AND %s
                """,
                ('%' + postcode + '%', minprice, maxprice)
                )
        data = cur.fetchall()
        cur.close()
        return render_template("search.html", data=data)