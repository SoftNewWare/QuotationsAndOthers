from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Main title
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "RAM KISHAN TIWARI", ln=True, align="C")

        # Subheading
        self.set_font("Arial", "B", 12)
        self.set_fill_color(0, 51, 153)  # Dark blue
        self.set_text_color(255, 255, 255)  # White text
        self.cell(0, 10, "Painting Contractor", ln=True, align="C", fill=True)

        # Contact info
        self.set_font("Arial", "", 11)
        self.set_text_color(0, 0, 0)  # Reset to black
        self.cell(0, 10, "26 Dev Bhoomi Complex, Navrangpura, Ahmedabad - 380009", ln=True, align="C")
        self.cell(0, 8, "M. 7285010069", ln=True, align="C")

        # Line
        self.ln(5)
        self.line(10, self.get_y(), 200, self.get_y())

# Example usage:
if __name__ == "__main__":
    pdf = PDF()
    pdf.add_page()
    pdf.output("examples.pdf")