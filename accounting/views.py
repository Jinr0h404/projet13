from django.shortcuts import render
from django.views import View
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from schedule.models import Session
from patient.models import Patient, Address
from .forms import BillSessionForm


# Create your views here.
class BillPdfView(View):
    def get(self, request, pk):
        form = BillSessionForm()
        session = Session.objects.get(pk=pk)
        patient = Patient.objects.get(pk=session.patient_unique_id.id)
        context = {'session_id': pk, 'session': session, 'form': form, 'patient': patient}
        # return render(request, "patient/index_patient.html", {'form': form, 'form_address': form_address})
        return render(request, "accounting/session_bill.html", context)

    def post(self, request, pk):
        form = BillSessionForm(request.POST)
        session = Session.objects.get(pk=pk)
        linelist_head = ["Cabiet d'ostéopathie", 'Prénom  Nom', 'adresse du cabinet', 'Numéro de tel']
        linelist_patient = ['Facture destinée {{session.reason}}', session.reason, 'Numéro de tel']
        if form.is_valid():
            patient=Patient.objects.get(pk=session.patient_unique_id.id)
            print(patient)
            # Create a file-like buffer to receive PDF data.
            buffer = io.BytesIO()
            # Create the PDF object, using the buffer as its "file."
            p = canvas.Canvas(buffer)
            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            p.drawString(1, 1, "x1.y1")
            p.drawString(1, 50, "x1.y50")
            p.drawString(1, 830, "x1.y830")
            p.drawString(1, 415, "x1.y415")
            p.drawString(550, 1, "x550.y1")
            p.drawString(550, 50, "x550.y50")
            p.drawString(550, 830, "x550.y830")
            p.drawString(550, 415, "x550.y415")
            p.drawString(280, 830, "x280.y830")
            p.drawString(280, 1, "x280.y1")
            # p.rect(x, y, width, height, stroke=1, fill=0)
            p.rect(50, 415, 480, 60, stroke=1, fill=0)
            p.rect(280, 385, 250, 30, stroke=1, fill=0)
            # p.line(x1,y1,x2,y2) horizontal
            p.line(50, 445, 530, 445)
            # line vertical
            p.line(385, 385, 385, 475)
            p.drawString(550, 1000, "Hello world.")
            p.drawRightString(80, 80, "Hello world.")
            p.drawCentredString(100, 100, "Hello world.")
            text = p.beginText(5, 800)
            for line in linelist_head:
                text.textLine(line)
            p.drawText(text)
            text_patient = p.beginText(5, 600)
            for line in linelist_patient:
                text_patient.textLine(line)
            p.drawText(text_patient)
            # Close the PDF object cleanly, and we're done.
            p.showPage()
            p.save()
            # FileResponse sets the Content-Disposition header so that browsers
            # present the option to save the file.
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
