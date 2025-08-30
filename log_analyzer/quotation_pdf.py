from fpdf import FPDF
from datetime import datetime

class QuotationPDF(FPDF):
    def add_for_field(self):
        if hasattr(self, 'for_field') and self.for_field:
            self.set_font('Arial', 'B', 11)
            self.set_text_color(*self.ACCENT)
            self.cell(0, 7, f'For: {self.for_field}', ln=1)
            self.ln(3)
        self.set_text_color(*self.TEXT_COLOR)
    # Theme colors (RGB)
    HEADER_BG = (10, 90, 160)         # deep blue for header background
    ACCENT = (0, 102, 204)            # accent color for separators
    TABLE_HEADER_BG = (10, 90, 160)   # same as header for table header
    TABLE_ROW_FILL1 = (245, 247, 250) # very light grey
    TABLE_ROW_FILL2 = (255, 255, 255) # white
    DRAW_COLOR = (100, 100, 100)      # border/draw color
    TEXT_COLOR = (0, 0, 0)            # default text color
    HEADER_TEXT_COLOR = (255, 255, 255)

    def header(self):
        # Header background bar (taller to fit both name and address)
        header_height = 28
        self.set_fill_color(*self.HEADER_BG)
        self.set_draw_color(*self.HEADER_BG)
        self.set_line_width(0.0)
        self.rect(0, 0, self.w, header_height, 'F')  # full-width tall bar at top

        # Company name centered near the top of the bar
        if hasattr(self, 'company_name'):
            self.set_xy(self.l_margin, 6)
            self.set_text_color(*self.HEADER_TEXT_COLOR)
            self.set_font('Arial', 'B', 22)
            self.cell(0, 12, self.company_name, ln=1, align='C', border=0)

        # Company address immediately below the name, inside the bar
        if hasattr(self, 'company_address'):
            self.set_xy(self.l_margin, self.get_y())
            self.set_text_color(*self.HEADER_TEXT_COLOR)
            self.set_font('Arial', '', 10)
            self.multi_cell(self.w - self.l_margin - self.r_margin, 5, self.company_address, align='C')

        self.ln(2)
        # draw a thick accent separator
        # small gap after header
        self.ln(3)
        # reset draw/text colors and line width
        self.set_line_width(0.2)
        self.set_draw_color(*self.DRAW_COLOR)
        self.set_text_color(*self.TEXT_COLOR)

    def draw_separator(self, thickness=2, color=None):
        if color is None:
            color = self.ACCENT
        self.set_draw_color(*color)
        self.set_line_width(thickness)
        x1 = self.l_margin
        x2 = self.w - self.r_margin
        y = self.get_y()
        self.line(x1, y, x2, y)
        self.ln(1)
        # restore defaults
        self.set_line_width(0.2)
        self.set_draw_color(*self.DRAW_COLOR)

    def add_issued_to(self, issued_to):
        self.set_font('Arial', 'B', 12)
        self.set_text_color(*self.TEXT_COLOR)
        self.cell(0, 8, f'Issued To: {issued_to}', ln=1)
        self.ln(4)  # Gentle spacing

    def add_date(self, date_str=None):
        """
        Print the date below 'Issued To' as a simple cell, no header redraw.
        """
        self.set_font('Arial', '', 11)
        self.set_text_color(*self.TEXT_COLOR)
        if not date_str:
            date_str = datetime.now().strftime('%d-%m-%Y')
        self.cell(0, 8, f'Date: {date_str}', ln=1)
        self.ln(4)  # Gentle spacing

    def add_items_table(self, items, blank_zero=True):
        """
        Render the items table with colored header, alternating row fills,
        thicker colored borders and a final total row.
        If blank_zero=True, zero values (0.0) are shown as empty strings.
        """
        # Table layout (must fit within page width)
        col_widths = [60, 40, 40, 40]  # sums to 180 (fits A4 with default margins)
        # Header
        self.set_fill_color(*self.TABLE_HEADER_BG)
        self.set_text_color(*self.HEADER_TEXT_COLOR)
        self.set_font('Arial', 'B', 12)
        self.set_draw_color(*self.TABLE_HEADER_BG)
        self.set_line_width(0.8)
        self.cell(col_widths[0], 9, 'Item', border=1, align='L', fill=True)
        self.cell(col_widths[1], 9, 'Rate/Sq.Ft.', border=1, align='C', fill=True)
        self.cell(col_widths[2], 9, 'Total Area', border=1, align='C', fill=True)
        self.cell(col_widths[3], 9, 'Cost', border=1, align='R', fill=True, ln=1)

        # Reset for rows
        self.set_font('Arial', '', 11)
        self.set_draw_color(*self.DRAW_COLOR)
        self.set_line_width(0.4)

        total_price = 0.0
        fill_toggle = False

        for item in items:
            name = str(item.get('name', '') or '')
            rate = item.get('rate', '')
            area = item.get('area', '')
            cost = item.get('cost', '')


            # Parse numeric values for calculation, but display raw rate
            try:
                rate_val = float(rate) if rate not in (None, '') and rate.replace('.','',1).isdigit() else 0.0
            except (ValueError, TypeError):
                rate_val = 0.0

            try:
                area_val = float(area) if area not in (None, '') and area.replace('.','',1).isdigit() else 0.0
            except (ValueError, TypeError):
                area_val = 0.0

            # Calculate cost if both rate and area are numeric
            if (rate_val and area_val):
                cost_val = rate_val * area_val
            else:
                try:
                    cost_val = float(cost) if cost not in (None, '') and cost.replace('.','',1).isdigit() else 0.0
                except (ValueError, TypeError):
                    cost_val = 0.0

            total_price += cost_val

            # Row fill color alternating
            fill_color = self.TABLE_ROW_FILL1 if fill_toggle else self.TABLE_ROW_FILL2
            self.set_fill_color(*fill_color)
            fill_flag = True if fill_color != self.TABLE_ROW_FILL2 else False

            # Prepare display strings, optionally hide zeros
            rate_str = rate if rate else ''  # Show raw rate value
            area_str = f'{area_val:g}' if (area_val != 0 or not blank_zero) else ''
            cost_str = f'{cost_val:.2f}' if (cost_val != 0 or not blank_zero) else ''

            # Cells
            self.set_text_color(*self.TEXT_COLOR)
            self.cell(col_widths[0], 8, name, border=1, fill=fill_flag)
            self.cell(col_widths[1], 8, rate_str, border=1, align='C', fill=fill_flag)
            self.cell(col_widths[2], 8, area_str, border=1, align='C', fill=fill_flag)
            self.cell(col_widths[3], 8, cost_str, border=1, align='R', fill=fill_flag, ln=1)

            fill_toggle = not fill_toggle

        # Total row with accent top border
        self.ln(1)
        # Draw a colored separator before total
        self.set_font('Arial', 'B', 12)
        self.set_text_color(*self.TEXT_COLOR)
        self.set_draw_color(*self.DRAW_COLOR)
        self.set_fill_color(255, 255, 255)
        self.cell(sum(col_widths[:3]), 9, 'Total Price', border=1, align='L', fill=False)
        total_str = f'{total_price:.2f}' if (total_price != 0 or not blank_zero) else ''
        self.cell(col_widths[3], 9, total_str, border=1, align='R', fill=False, ln=1)
        # restore defaults
        self.set_font('Arial', '', 11)
        self.set_line_width(0.2)
        self.set_draw_color(*self.DRAW_COLOR)
        self.set_text_color(*self.TEXT_COLOR)
        self.ln(3)


def generate_quotation_pdf(
    filename,
    company_name,
    company_address,
    issued_to,
    items,
    date_str=None
):
    pdf = QuotationPDF()
    pdf.company_name = company_name
    pdf.company_address = company_address
    pdf.add_page()

    pdf.add_issued_to(issued_to)
    # "For" line styled
    pdf.set_font('Arial', 'B', 11)
    pdf.set_text_color(*QuotationPDF.ACCENT)
    pdf.cell(0, 7, 'For: Restaurant Ceiling Color And AC Body Spray Color Works', ln=1)
    pdf.ln(3)
    pdf.set_text_color(*QuotationPDF.TEXT_COLOR)

    # Use the single table renderer, keep blanks for zero-cost rows
    pdf.add_items_table(items, blank_zero=True)

    # Optional date after the table
    if date_str:
        pdf.add_date(date_str)
    else:
        pdf.add_date()

    pdf.output(filename)


# Example usage:
if __name__ == "__main__":
    items = [
        {'name': 'Royal Plastic Paint', 'rate': '32', 'area': '', 'cost': ''},
        {'name': 'Oil Paint', 'rate': '25', 'area': '', 'cost': ''},
        {'name': 'Corner A/C Body  Spray', 'rate': '', 'area': '', 'cost': '1200'},
    ]

    # Monkey-patch QuotationPDF.cell to force no borders on all cells
    _original_cell = QuotationPDF.cell
    def _cell_no_border(self, w, h=0, txt='', border=0, ln=0, align='', fill=False, link=''):
        return _original_cell(self, w, h, txt, border=0, ln=ln, align=align, fill=fill, link=link)
    QuotationPDF.cell = _cell_no_border

    generate_quotation_pdf(
        'quotation_example-final-shares.pdf',
        company_name='Ravi Paints',
        company_address='26, Dev Bhoomi Complex, Navrangpura, Ahmedabad, 380009 | Mobile: 9998897890',
        issued_to='Zodiac Restaurant',
        items=items,
        date_str='30-08-2025'
    )
