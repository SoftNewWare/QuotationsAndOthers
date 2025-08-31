from flask import Flask, render_template_string, request, send_file, redirect, url_for
from datetime import datetime
import io
from log_analyzer.quotation_pdf import QuotationPDF


app = Flask(__name__)

# Define the root route after app is created
@app.route("/")
def home():
  # Redirect root to the quotation form
  return redirect(url_for("quotation"))

QUOTATION_TEMPLATES = {
    "modern": {
        "label": "Modern Blue",
        "header_bg": (10, 90, 160),
        "accent": (0, 102, 204),
    },
    "classic": {
        "label": "Classic Gray",
        "header_bg": (60, 60, 60),
        "accent": (120, 120, 120),
    },
    "minimal": {
        "label": "Minimal White",
        "header_bg": (255, 255, 255),
        "accent": (0, 0, 0),
    },
}

QUOTATION_FORM_HTML = """
<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <title>Quotation PDF Generator</title>
  <style>
    body {{ background: #f7f9fa; font-family: 'Segoe UI', Arial, sans-serif; }}
    .container {{ max-width: 520px; background: #fff; margin: 40px auto; padding: 32px 28px 24px 28px; border-radius: 12px; box-shadow: 0 2px 16px rgba(0,0,0,0.07); }}
    h2 {{ text-align: center; color: #003399; margin-bottom: 22px; font-weight: 600; }}
    label {{ display: block; margin-top: 14px; margin-bottom: 5px; color: #222; font-size: 15px; }}
    input[type=\"text\"], textarea, select, input[type=\"color\"] {{ width: 100%; padding: 8px 10px; border: 1px solid #cfd8dc; border-radius: 5px; font-size: 15px; background: #f5f7fa; margin-bottom: 2px; box-sizing: border-box; transition: border-color 0.2s; }}
    input[type=\"text\"]:focus, textarea:focus, select:focus, input[type=\"color\"]:focus {{ border-color: #003399; outline: none; }}
    textarea {{ resize: vertical; min-height: 60px; max-height: 180px; }}
    .btn {{ width: 100%; background: #003399; color: #fff; border: none; padding: 11px 0; border-radius: 5px; font-size: 16px; font-weight: 600; margin-top: 18px; cursor: pointer; transition: background 0.2s; }}
    .btn:hover {{ background: #001f66; }}
    .footer {{ text-align: center; color: #aaa; font-size: 13px; margin-top: 30px; }}
    .items-table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
    .items-table th, .items-table td {{ border: 1px solid #cfd8dc; padding: 6px 8px; text-align: left; }}
    .add-row-btn {{ margin-top: 8px; background: #e3eafc; color: #003399; border: 1px solid #003399; border-radius: 4px; padding: 6px 12px; font-size: 14px; cursor: pointer; }}
    .add-row-btn:hover {{ background: #d0dbf7; }}
  </style>
  <script>
    function addItemRow() {{
      const table = document.getElementById('items-table-body');
      const row = document.createElement('tr');
      row.innerHTML = `
        <td><input type=\"text\" name=\"item_name[]\" required></td>
        <td><input type=\"text\" name=\"item_rate[]\" required></td>
        <td><input type=\"text\" name=\"item_area[]\" required></td>
        <td><input type=\"text\" name=\"item_cost[]\" required></td>
        <td><button type=\"button\" onclick=\"this.parentNode.parentNode.remove();\">🗑️</button></td>
      `;
      table.appendChild(row);
    }}
  </script>
</head>
<body>
  <div class=\"container\">
    <h2>Quotation PDF Generator</h2>
    <form method=\"post\">
      <label for=\"company_name\">Company Name</label>
      <input type=\"text\" name=\"company_name\" id=\"company_name\" required>
      <label for=\"company_address\">Company Address</label>
      <input type=\"text\" name=\"company_address\" id=\"company_address\" required>
      <label for=\"issued_to\">Issued To</label>
      <input type=\"text\" name=\"issued_to\" id=\"issued_to\" required>
  <label for=\"date\">Date</label>
  <input type=\"text\" name=\"date\" id=\"date\" value=\"{date}\" required>
  <label for=\"for_field\">For (Purpose of Quotation)</label>
  <input type=\"text\" name=\"for_field\" id=\"for_field\" placeholder=\"e.g. Ceiling Color And AC Body Spray Color Works\">
      <label for=\"template\">Template</label>
      <select name=\"template\" id=\"template\">
        <option value=\"modern\">Modern Blue</option>
        <option value=\"classic\">Classic Gray</option>
        <option value=\"minimal\">Minimal White</option>
      </select>
      <label>Items</label>
      <table class=\"items-table\">
        <thead>
          <tr><th>Item Name</th><th>Rate/Sq.Ft.</th><th>Total Area</th><th>Cost</th><th></th></tr>
        </thead>
        <tbody id=\"items-table-body\">
          <tr>
            <td><input type=\"text\" name=\"item_name[]\" required></td>
            <td><input type=\"text\" name=\"item_rate[]\" required></td>
            <td><input type=\"text\" name=\"item_area[]\" required></td>
            <td><input type=\"text\" name=\"item_cost[]\" required></td>
            <td><button type=\"button\" onclick=\"this.parentNode.parentNode.remove();\">🗑️</button></td>
          </tr>
        </tbody>
      </table>
      <button type=\"button\" class=\"add-row-btn\" onclick=\"addItemRow();\">+ Add Item</button>
      <button class=\"btn\" type=\"submit\">Generate PDF</button>
    </form>
  </div>
  <div class=\"footer\">&copy; 2025 Quotation Generator</div>
</body>
</html>
"""

@app.route("/quotation", methods=["GET", "POST"])
def quotation():
  if request.method == "POST":
    company_name = request.form.get("company_name", "")
    company_address = request.form.get("company_address", "")
    issued_to = request.form.get("issued_to", "")
    date_str = request.form.get("date", datetime.now().strftime('%d-%m-%Y'))
    template_key = request.form.get("template", "modern")
    for_field = request.form.get("for_field", "")
    items = []
    names = request.form.getlist("item_name[]")
    rates = request.form.getlist("item_rate[]")
    areas = request.form.getlist("item_area[]")
    costs = request.form.getlist("item_cost[]")
    for n, r, a, c in zip(names, rates, areas, costs):
      items.append({"name": n, "rate": r, "area": a, "cost": c})
    # Set template colors
    template = QUOTATION_TEMPLATES.get(template_key, QUOTATION_TEMPLATES["modern"])
    try:
      # Sanitize keys in case of accidental whitespace
      header_bg = template.get("header_bg") or template.get("header_bg".strip()) or template.get(" background".strip())
      accent = template.get("accent") or template.get("accent".strip()) or template.get(" accent".strip())
      if header_bg is None or accent is None:
        print(f"TEMPLATE DEBUG: {template}")
        print(f"TEMPLATE KEYS: {list(template.keys())}")
        raise KeyError("header_bg or accent not found in template")
      QuotationPDF.HEADER_BG = header_bg
      QuotationPDF.ACCENT = accent
      QuotationPDF.TABLE_HEADER_BG = header_bg
    except KeyError as e:
      print(f"TEMPLATE DEBUG: {template}")
      print(f"TEMPLATE KEYS: {list(template.keys())}")
      print(f"KEY ACCESSED: {e}")
      raise
    pdf = QuotationPDF()
    pdf.company_name = company_name
    pdf.company_address = company_address
    pdf.for_field = for_field
    pdf.add_page()
    pdf.add_issued_to(issued_to)
    pdf.add_date(date_str)
    pdf.add_for_field()  # Add this method to print the 'For' field
    pdf.add_items_table(items)
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    pdf_buffer = io.BytesIO(pdf_bytes)
    pdf_buffer.seek(0)
    return send_file(
      pdf_buffer,
      as_attachment=True,
      download_name="quotation.pdf",
      mimetype="application/pdf"
    )
  html = QUOTATION_FORM_HTML.format(date=datetime.now().strftime('%d-%m-%Y'))
  return render_template_string(html)

if __name__ == "__main__":
    app.run(debug=True)
