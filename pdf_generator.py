from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from datetime import datetime
import random
import qrcode
def generate_report(
    patient_name,
    age,
    gender,
    blood_group,
    height,
    weight,
    bmi,
    risk_level,
    disease,
    confidence,
    severity,
    precautions,
    doctor
):

    filename = "medical_report.pdf"
    report_id = f"MED-{random.randint(1000,9999)}"
    verification_text = (
        f"Report ID: {report_id}\n"
        f"Patient: {patient_name}\n"
        f"Disease: {disease}"
    )
    qr = qrcode.make(
        verification_text
    )
    qr.save(
        "verification_qr.png"
    )
    today = datetime.now().strftime(
        "%d-%m-%Y"
    )
    c = canvas.Canvas(filename)
    logo = ImageReader(
        "assets/logo.png"
    )
    c.drawImage(
        logo,
        50,
        760,
        width=50,
        height=50,
        mask='auto'
    )

    qr_image = ImageReader(
        "verification_qr.png"
    )
    c.drawImage(
        qr_image,
        500,
        690,
        width=45,
        height=45
    )
    c.setFillColor(colors.darkblue)

    c.setFont("Helvetica-Bold", 22)
    title = "MediScan AI"
    c.setFont("Helvetica-Bold", 22)
    
    text_width = c.stringWidth(
        title,
        "Helvetica-Bold",
        22
    )
    c.drawString(
        120,
        790,
        title
    )
    c.setFont("Helvetica", 14)

    subtitle = "Medical Prediction Report"
    c.setFont(
        "Helvetica",
        14
    )
    
    subtitle_width = c.stringWidth(
        subtitle,
        "Helvetica",
        14
    )
    
    c.drawString(
        120,
        765,
        subtitle
    )

    c.line(40, 750, 550, 750)
    c.setFont(
        "Helvetica",
        11
    )
    
    c.drawString(
        50,
        730,
        f"Report ID: {report_id}"
    )
    
    c.drawString(
        360,
        730,
        f"Date: {today}"
    )
   
    c.setFillColor(colors.black)
    c.setFont(
        "Helvetica-Bold",
        15
    )
    
    c.drawString(
        50,
        700,
        "Patient Information"
    )
    
    c.setFont(
        "Helvetica",
        12
    )
    
    c.drawString(
        50,
        675,
    f"Name: {patient_name}"
    )
    
    c.drawString(
        250,
        675,
        f"Age: {age}"
    )
    
    c.drawString(
        400,
        675,
        f"Gender: {gender}"
    )
    c.drawString(
        50,
        650,
        f"Blood Group: {blood_group}"
    )
    c.setFont("Helvetica-Bold", 14)

    c.setFont(
        "Helvetica-Bold",
        15
    )
    c.drawString(
        50,
        610,
        "Prediction Results"
    )
    
    c.setFont(
        "Helvetica-Bold",
        14
    )
    
    c.drawString(
        50,
        580,
        "Predicted Disease:"
    )
    
    c.drawString(
        50,
        550,
        "Confidence:"
    )
    
    c.drawString(
        50,
        520,
        "Severity:"
    )
    
    c.drawString(
        50,
        490,
        "Recommended Doctor:"
    )
    
    c.setFont(
        "Helvetica",
        14
    )
    
    c.drawString(
        250,
        580,
        disease
    )
    
    c.drawString(
        250,
        550,
        confidence
    )
    
    if severity == "High":
        c.setFillColor(colors.red)
    elif severity == "Medium":
        c.setFillColor(colors.orange)
    else:
        c.setFillColor(colors.green)
    c.drawString(
        250,
        520,
        severity
    )
    c.setFillColor(colors.black)
    c.setStrokeColor(colors.darkblue)
    c.setFillColor(colors.darkblue)
    c.setFont(
        "Helvetica-Bold",
        14
    )
    c.drawString(
         300,
         490,
         doctor
    )
    c.setFillColor(colors.black)

    c.setFont(
        "Helvetica-Bold",
        15
    )

    c.setFont(
        "Helvetica-Bold",
        15
    )
    c.drawString(
        50,
        450,
        "Health Metrics"
    )
    
    c.setFont(
        "Helvetica",
        12
    )
    
    c.drawString(
        70,
        430,
        f"Height: {height} cm"
    )
    c.drawString(
        70,
        405,
        f"Weight: {weight} kg"
    )
    if bmi < 18.5:
        bmi_status = "Underweight"
    elif bmi < 25:
        bmi_status = "Normal"
    elif bmi < 30:
        bmi_status = "Overweight"
    else:
        bmi_status = "Obese"
    c.drawString(
        70,
        380,
        f"BMI: {bmi} ({bmi_status})"
    )
    
    c.drawString(
        70,
        355,
        f"Risk Level: {risk_level}"
    )
    c.setFont(
        "Helvetica-Bold",
        15
    )
    c.drawString(
        50,
        205,
        "Precautions"
    )
    c.setFont(
        "Helvetica-Bold",
        15
    )
    c.drawString(
        50,
        310,
        "AI Health Assessment"
    )
    c.setFont(
        "Helvetica",
        12
    )
    c.drawString(
        70,
        285,
        f"Based on the symptoms provided, the patient shows indicators associated with {disease}."
    )
    
    c.drawString(
        70,
        265,
        f"The overall health risk assessment is classified as {risk_level}."
    )
    c.drawString(
        70,
        245,
        f"Follow the recommended precautions and consult a {doctor} if symptoms continue."
    )
    y = 180

    c.setFont("Helvetica", 12)

    for p in precautions:

        c.drawString(
            70,
            y,
            f"• {p}"
        )

        y -= 18

    c.line(
        40,
        40,
        550,
        40
    )
    c.setFont(
        "Helvetica",
        9
    )
    
    c.drawString(
        50,
        25,
        "MediScan AI © 2026"
    )
    c.drawRightString(
        540,
        25,
        "AI-Powered Medical Assessment Report"
    )
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(
        50,
        10,
        "This report is AI-generated and does not replace professional medical advice."
    )
    if severity == "High":
        c.setFillColor(colors.red)
        c.setFont(
            "Helvetica-Bold",
            12
        )
        c.drawString(
            50,
            95,
            "⚠ WARNING: Immediate medical consultation recommended."
        )
        c.setFillColor(colors.black)
    c.save()

    return filename