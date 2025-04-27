from flask import Flask, render_template, request, jsonify, send_file
import sqlite3
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

app = Flask(__name__)


# Initialize database (if needed)
def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY,
                    description TEXT NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    date TEXT NOT NULL
                 )''')
    conn.commit()
    conn.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_expense', methods=['POST'])
def add_expense():
    description = request.form['description']
    amount = float(request.form['amount'])
    category = request.form['category']
    date = request.form['date']

    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('INSERT INTO expenses (description, amount, category, date) VALUES (?, ?, ?, ?)',
              (description, amount, category, date))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})


@app.route('/get_expenses')
def get_expenses():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('SELECT * FROM expenses')
    expenses = c.fetchall()
    conn.close()
    return jsonify(expenses)


@app.route('/download_pdf')
def download_pdf():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('SELECT * FROM expenses')
    expenses = c.fetchall()
    conn.close()

    # Create a buffer to save the PDF in memory
    buffer = BytesIO()

    # Create the PDF object using SimpleDocTemplate
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Create a table with column headers and data
    data = [['Index', 'Description', 'Amount', 'Category', 'Date']]  # Header row

    for index, expense in enumerate(expenses, start=1):
        data.append([index, expense[1], f"${expense[2]:.2f}", expense[3], expense[4]])

    # Create a Table object
    table = Table(data)

    # Apply table styles
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#3498db")),  # Header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Align text to center
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Data font
        ('FONTSIZE', (0, 0), (-1, -1), 10),  # Font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding for header row
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),  # Data background
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Grid lines for table
        ('TOPPADDING', (0, 0), (-1, 0), 12),  # Padding for header row
        ('BOTTOMPADDING', (0, 1), (-1, -1), 10),  # Padding for data rows
    ])

    table.setStyle(style)

    # Add table to document elements
    elements.append(table)

    # Build the PDF
    doc.build(elements)

    # Send PDF file as a response
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="expenses_report.pdf", mimetype="application/pdf")


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
