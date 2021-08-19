import pdfkit
from PyPDF2 import PdfFileWriter, PdfFileReader

def output_profile_to_pdf(profiles, team_name, year_for_roster, year_for_report, how_many_pa_to_appear):

    html_doc_name = "data/" + team_name + "/" + year_for_roster + "/" + team_name + "_batting_" + year_for_report + "_report.html"
    pdf_doc_name = "data/" + team_name + "/" + year_for_roster + "/" + team_name + "_batting_" + year_for_report + "_report.pdf"

    pdfkit.from_file(html_doc_name, pdf_doc_name)

    pages_to_delete = [0]
    infile = PdfFileReader(pdf_doc_name, 'rb')
    output = PdfFileWriter()

    for i in range(infile.getNumPages()):
        if i not in pages_to_delete:
            p = infile.getPage(i)
            output.addPage(p)

    with open(pdf_doc_name, 'wb') as f:
        output.write(f)

    return True
