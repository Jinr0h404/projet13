from django.shortcuts import render
from django.views import View
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from schedule.models import Session
from .forms import BillSessionForm


# Create your views here.
class BillPdfView(View):
    def get(self, request, pk):
        form = BillSessionForm()
        session = Session.objects.get(pk=pk)
        context = {'session_id': pk, 'session': session, 'form': form}
        # return render(request, "patient/index_patient.html", {'form': form, 'form_address': form_address})
        return render(request, "accounting/session_bill.html", context)

    def post(self, request, pk):
        form = BillSessionForm(request.POST)
        session = Session.objects.get(pk=pk)
        linelist = ['Prénom  Nom', 'adresse du cabinet', 'Numéro de tel']
        linelist_patient = ['Facture destinée à', session.reason, 'Numéro de tel']
        if form.is_valid():
            # Create a file-like buffer to receive PDF data.
            buffer = io.BytesIO()
            # Create the PDF object, using the buffer as its "file."
            p = canvas.Canvas(buffer)
            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            p.drawString(1, 1, "Hello world.")
            p.drawRightString(80, 80, "Hello world.")
            p.drawCentredString(100, 100, "Hello world.")
            text = p.beginText(5, 800)
            for line in linelist:
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
