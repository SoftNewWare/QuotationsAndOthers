from flask import Flask, render_template_string, request, send_file
from fpdf import FPDF
import io
app = Flask(__name__)

class BaseLetterhead(FPDF):
    def __init__(self):
        super().__init__()
        self.fields = {}
        self.primary_color = (0, 0, 0)
        self.secondary_color = (0, 0, 0)

    def set_fields(self, fields):
        self.fields = fields

        def hex_to_rgb(s):
            if not s:
                return (0, 0, 0)
            s = s.lstrip('#')
            return tuple(int(s[i:i+2], 16) for i in (0, 2, 4))

        self.primary_color = hex_to_rgb(fields.get("primary_color", "#003399"))
        self.secondary_color = hex_to_rgb(fields.get("secondary_color", "#003399"))

    def header(self):
        # default no-op header
        pass

class LetterheadTemplate1(BaseLetterhead):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*self.primary_color)
        self.cell(0, 10, self.fields.get("title", ""), ln=True, align="L")
        self.set_text_color(0, 0, 0)
        self.cell(0, 8, self.fields.get("address", ""), ln=True, align="L")
        self.ln(5)

class LetterheadTemplate2(BaseLetterhead):
    def header(self):
        self.set_font("Times", "B", 16)
        self.set_text_color(*self.primary_color)
        self.cell(0, 12, self.fields.get("title", ""), ln=True, align="C")
        self.set_text_color(0, 0, 0)
        self.ln(5)

class LetterheadTemplate3(BaseLetterhead):
    def header(self):
        self.set_fill_color(*self.primary_color)
        self.rect(0, 0, 210, 10, 'F')
        self.set_font("Courier", "B", 12)
        self.set_text_color(255, 255, 255)
        self.set_y(4)
        self.cell(0, 8, self.fields.get("title", ""), ln=True, align="C")
        self.ln(5)

class LetterheadTemplate4(BaseLetterhead):
    def header(self):
        self.set_font("Courier", "B", 12)
        self.set_text_color(*self.primary_color)
        self.cell(0, 10, self.fields.get("title", ""), ln=True, align="L")
        self.ln(5)

class LetterheadTemplate5(BaseLetterhead):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.set_text_color(*self.primary_color)
        self.cell(0, 10, self.fields.get("title", ""), ln=True, align="R")
        self.ln(5)

class LetterheadTemplate6(BaseLetterhead):
    def header(self):
        self.set_fill_color(*self.primary_color)
        self.rect(0, 0, 210, 15, 'F')
        self.set_font("Times", "B", 15)
        self.set_text_color(255, 255, 255)
        self.set_y(6)
        self.cell(0, 8, self.fields.get("title", ""), ln=True, align="C")
        self.set_y(18)
        self.set_font("Times", "", 11)
        self.set_text_color(*self.secondary_color)
        self.cell(0, 8, self.fields.get("subtitle", ""), ln=True, align="C")
        self.set_text_color(0, 0, 0)
        self.cell(0, 8, self.fields.get("address", ""), ln=True, align="C")
        self.cell(0, 8, f"Mobile: {self.fields.get('mobile', '')}", ln=True, align="C")
        self.ln(5)

class LetterheadTemplate7(BaseLetterhead):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(*self.primary_color)
        self.cell(0, 10, self.fields.get("title", ""), ln=True, align="C")
        self.set_font("Helvetica", "I", 12)
        self.set_text_color(*self.secondary_color)
        self.cell(0, 10, self.fields.get("subtitle", ""), ln=True, align="C")
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, self.fields.get("address", ""), ln=True, align="C")
        self.cell(0, 8, f"Phone: {self.fields.get('mobile', '')}", ln=True, align="C")
        self.ln(5)
        self.set_draw_color(*self.primary_color)
        self.line(10, self.get_y(), 200, self.get_y())

class LetterheadTemplate8(BaseLetterhead):
    def header(self):
        self.set_font("Courier", "B", 16)
        self.set_text_color(*self.primary_color)
        self.cell(0, 10, self.fields.get("title", ""), ln=True, align="C")
        self.set_font("Courier", "", 12)
        self.set_text_color(*self.secondary_color)
        self.cell(0, 10, self.fields.get("subtitle", ""), ln=True, align="C")
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, self.fields.get("address", ""), ln=True, align="C")
        self.cell(0, 8, f"Mobile: {self.fields.get('mobile', '')}", ln=True, align="C")
        self.ln(5)
        self.set_draw_color(*self.primary_color)
        self.line(10, self.get_y(), 200, self.get_y())

class LetterheadTemplate9(BaseLetterhead):
    def header(self):
        self.set_font("Arial", "B", 18)
        self.set_text_color(*self.primary_color)
        self.cell(0, 12, self.fields.get("title", ""), ln=True, align="C")
        self.set_font("Arial", "", 12)
        self.set_text_color(*self.secondary_color)
        self.cell(0, 10, self.fields.get("subtitle", ""), ln=True, align="C")
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, self.fields.get("address", ""), ln=True, align="C")
        self.cell(0, 8, f"Contact: {self.fields.get('mobile', '')}", ln=True, align="C")
        self.ln(5)
        self.set_draw_color(*self.primary_color)
        self.line(10, self.get_y(), 200, self.get_y())

class LetterheadTemplate10(BaseLetterhead):
    def header(self):
        self.set_font("Times", "B", 20)
        self.set_text_color(*self.primary_color)
        self.cell(0, 14, self.fields.get("title", ""), ln=True, align="C")
        self.set_font("Times", "", 12)
        self.set_text_color(*self.secondary_color)
        self.cell(0, 10, self.fields.get("subtitle", ""), ln=True, align="C")
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, self.fields.get("address", ""), ln=True, align="C")
        self.cell(0, 8, f"Mobile: {self.fields.get('mobile', '')}", ln=True, align="C")
        self.ln(5)
        self.set_draw_color(*self.primary_color)
        self.line(10, self.get_y(), 200, self.get_y())

class LetterheadTemplate11(BaseLetterhead):
    def header(self):
        self.set_fill_color(*self.primary_color)
        self.rect(0, 0, 210, 10, 'F')
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(255, 255, 255)
        self.set_y(4)
        self.cell(0, 8, self.fields.get("title", ""), ln=True, align="C")
        self.set_y(14)
        self.set_font("Helvetica", "", 11)
        self.set_text_color(*self.secondary_color)
        self.cell(0, 8, self.fields.get("subtitle", ""), ln=True, align="C")
        self.set_text_color(0, 0, 0)
        self.cell(0, 8, self.fields.get("address", ""), ln=True, align="C")
        self.cell(0, 8, f"Contact: {self.fields.get('mobile', '')}", ln=True, align="C")
        self.ln(5)

TEMPLATES = {
    "classic": LetterheadTemplate1,
    "modern": LetterheadTemplate2,
    "bluebar": LetterheadTemplate3,
    "left-courier": LetterheadTemplate4,
    "right-arial": LetterheadTemplate5,
    "topbar": LetterheadTemplate6,
    "helvetica": LetterheadTemplate7,
    "courier": LetterheadTemplate8,
    "arial-bold": LetterheadTemplate9,
    "times-bold": LetterheadTemplate10,
    "minimal": LetterheadTemplate11,
}

# --- HTML Form ---
FORM_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Letterhead PDF Generator</title>
  <style>
    body {
      background: #f7f9fa;
      font-family: 'Segoe UI', Arial, sans-serif;
      margin: 0;
      padding: 0;
    }
    .container {
      max-width: 440px;
      background: #fff;
      margin: 40px auto;
      padding: 32px 28px 24px 28px;
      border-radius: 12px;
      box-shadow: 0 2px 16px rgba(0,0,0,0.07);
    }
    h2 {
      text-align: center;
      color: #003399;
      margin-bottom: 22px;
      font-weight: 600;
    }
    label {
      display: block;
      margin-top: 14px;
      margin-bottom: 5px;
      color: #222;
      font-size: 15px;
    }
    input[type="text"], textarea, select, input[type="color"] {
      width: 100%;
      padding: 8px 10px;
      border: 1px solid #cfd8dc;
      border-radius: 5px;
      font-size: 15px;
      background: #f5f7fa;
      margin-bottom: 2px;
      box-sizing: border-box;
      transition: border-color 0.2s;
    }
    input[type="text"]:focus, textarea:focus, select:focus, input[type="color"]:focus {
      border-color: #003399;
      outline: none;
    }
    textarea {
      resize: vertical;
      min-height: 60px;
      max-height: 180px;
    }
    .btn {
      width: 100%;
      background: #003399;
      color: #fff;
      border: none;
      padding: 11px 0;
      border-radius: 5px;
      font-size: 16px;
      font-weight: 600;
      margin-top: 18px;
      cursor: pointer;
      transition: background 0.2s;
    }
    .btn:hover {
      background: #001f66;
    }
    .footer {
      text-align: center;
      color: #aaa;
      font-size: 13px;
      margin-top: 30px;
    }
    .color-row {
      display: flex;
      gap: 10px;
      align-items: center;
      margin-bottom: 8px;
    }
    .color-row label {
      margin: 0 0 0 0;
      font-size: 14px;
      flex: 1;
    }
    .color-row input[type="color"] {
      width: 40px;
      height: 32px;
      padding: 0;
      border: none;
      background: none;
      flex: 0;
    }
  </style>
</head>
<body>
  <div class="container">
    <h2>Letterhead PDF Generator</h2>
    <form method="post">
      <label for="template">Template</label>
      <select name="template" id="template">
        <option value="classic">Classic</option>
        <option value="modern">Modern</option>
        <option value="bluebar">Blue Bar</option>
        <option value="left-courier">Left Courier</option>
        <option value="right-arial">Right Arial</option>
        <option value="topbar">Top Bar</option>
        <option value="helvetica">Helvetica</option>
        <option value="courier">Courier</option>
        <option value="arial-bold">Arial Bold</option>
        <option value="times-bold">Times Bold</option>
        <option value="minimal">Minimal</option>
      </select>

      <div class="color-row">
        <label for="primary_color">Primary Color</label>
    <input type="color" name="primary_color" id="primary_color" value="#003399" style="width:48px; height:36px; border:2px solid #888; border-radius:6px; cursor:pointer;">
    <label for="primary_color" style="margin-left:8px; font-size:13px; color:#333; cursor:pointer;">🎨 Pick</label>
      </div>
      <div class="color-row">
        <label for="secondary_color">Secondary Color</label>
    <input type="color" name="secondary_color" id="secondary_color" value="#003399" style="width:48px; height:36px; border:2px solid #888; border-radius:6px; cursor:pointer;">
    <label for="secondary_color" style="margin-left:8px; font-size:13px; color:#333; cursor:pointer;">🎨 Pick</label>
      </div>

      <label for="title">Title</label>
      <input type="text" name="title" id="title" value="RAM KISHAN TIWARI">

      <label for="name">Name</label>
      <input type="text" name="name" id="name" value="Painting Contractor">

      <label for="subtitle">Subtitle</label>
      <input type="text" name="subtitle" id="subtitle" value="Professional Services">

      <label for="address">Address</label>
      <input type="text" name="address" id="address" value="26 Dev Bhoomi Complex, Navrangpura, Ahmedabad - 380009">

      <label for="mobile">Mobile</label>
      <input type="text" name="mobile" id="mobile" value="7285010069">

      <label for="body">Body</label>
      <textarea name="body" id="body" rows="4">Welcome to our services!</textarea>

      <button class="btn" type="submit">Generate PDF</button>
    </form>
  </div>
  <div class="footer">
    &copy; 2025 Letterhead Generator
  </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        template_key = request.form.get("template", "classic")
        fields = {k: v for k, v in request.form.items()}
        pdf_class = TEMPLATES.get(template_key, LetterheadTemplate1)
        pdf = pdf_class()
        pdf.set_fields(fields)
        pdf.add_page()
        # Add body content if present
        body = fields.get("body", "")
        if body:
            pdf.set_font("Arial", "", 12)
            pdf.ln(10)
            pdf.multi_cell(0, 10, body)
        pdf_bytes = pdf.output(dest='S').encode('latin1')
        pdf_buffer = io.BytesIO(pdf_bytes)
        pdf_buffer.seek(0)
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name="letterhead.pdf",
            mimetype="application/pdf"
        )
    return render_template_string(FORM_HTML)

if __name__ == "__main__":
    app.run(debug=True)