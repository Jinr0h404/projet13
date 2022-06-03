from datetime import date
from django.shortcuts import render
from django.views import View
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from schedule.models import Session
from patient.models import Patient, Address
from .models import Price
from .forms import BillSessionForm


class BillPdfView(View):
    """the BillPdfView class allows the display of an invoice edition page and to generate an invoice in pdf format"""
    def get(self, request, pk):
        """the GET method allows the display of the page for editing an invoice and the form with the choice of
        the type of session"""
        form = BillSessionForm()
        session = Session.objects.get(pk=pk)
        patient = Patient.objects.get(pk=session.patient_unique_id.id)
        context = {'session_id': pk, 'session': session, 'form': form, 'patient': patient}
        return render(request, "accounting/session_bill.html", context)

    def post(self, request, pk):
        """the POST method retrieves the information from the form and will generate a pdf using the reportlab
        library with the desired information depending on the patient and the type of session. We indicate to
        reportlab the coordinates of the lines in abscissa and ordinate"""
        form = BillSessionForm(request.POST)
        session = Session.objects.get(pk=pk)
        linelist_head = ["Cabiet d'ostéopathie", 'Prénom  Nom', 'N° ADELI: xxxxxxxxxx', 'adresse du cabinet',
                         'Ville du cabinet', 'Numéro de tel']
        line_title = "Note d'honoraire"
        line_date = "le " + str(date.today())
        if form.is_valid():
            price = Price.objects.get(pk=request.POST["type_session"])
            session_price = str(price.price)
            session_type = price.session_type
            patient = Patient.objects.get(pk=session.patient_unique_id.id)
            address = Address.objects.get(patient_unique_id=patient.id)
            linelist_patient = ['Facture destinée à ' + patient.first_name + " " + patient.last_name,
                                str(address.street_number) + " " + address.street,
                                str(address.zip_code) + ", " + address.city,
                                patient.phone]
            line_designation_type = "Ostéopathie, séance: " + session_type
            line_designation = "Consultation de " + \
                               patient.first_name + " " + patient.last_name + " le " + str(session.appointment_date)
            # Create a file-like buffer to receive PDF data.
            buffer = io.BytesIO()
            # Create the PDF object, using the buffer as its "file."
            p = canvas.Canvas(buffer)
            # Draw things on the PDF. Here's where the PDF generation happens.
            # p.rect(x, y, width, height, stroke=1, fill=0)
            p.rect(50, 385, 480, 75, stroke=1, fill=0)
            p.rect(280, 355, 250, 30, stroke=1, fill=0)
            # p.line(x1,y1,x2,y2) horizontal
            p.line(50, 430, 530, 430)
            # line vertical
            p.line(385, 355, 385, 460)
            text = p.beginText(40, 800)
            for line in linelist_head:
                text.textLine(line)
            p.drawText(text)
            p.drawCentredString(280, 650, line_title)
            p.drawCentredString(280, 630, line_date)
            text_patient = p.beginText(40, 540)
            for line in linelist_patient:
                text_patient.textLine(line)
            p.drawText(text_patient)
            p.drawRightString(250, 440, "Désignation")
            p.drawRightString(480, 440, "Montant")
            p.drawRightString(350, 365, "TOTAL")
            p.drawString(60, 410, line_designation_type)
            p.drawString(60, 395, line_designation)
            p.drawCentredString(460, 405, session_price)
            p.drawCentredString(460, 365, session_price)
            # Close the PDF object cleanly, and we're done.
            p.showPage()
            p.save()
            # FileResponse sets the Content-Disposition header so that browsers
            # present the option to save the file.
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
