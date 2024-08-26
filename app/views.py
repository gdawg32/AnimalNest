from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import Group
from .models import Pet, Adopter, VeterinaryRecord, Adoption, Appointment
from django.contrib.auth.models import User
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER

def index(request):
    return render(request, 'index.html' )

def about(request):
    return render(request, 'about.html')

def pets(request):
    available_pets = Pet.objects.filter(adoption_status='Available')
    return render(request, 'pets.html', {'pets': available_pets})

def employee_login(request):
    if request.user.is_authenticated:
        if Group.objects.get(name='employee_user_set') in request.user.groups.all():
            return redirect('employee_portal')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if Group.objects.get(name='employee_user_set') in user.groups.all():
                login(request, user)
                return redirect('employee_portal')  
            else:
                messages.error(request, 'You are not authorized to log in here.')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'employee_login.html')


@login_required
def employee_portal(request):
    if Group.objects.get(name='employee_user_set') not in request.user.groups.all():
        return HttpResponse("You do not have permission to access this page.")
    
    name = request.user.username
    all_pets = Pet.objects.all()
    all_appointments = Appointment.objects.all()  # Query all appointments
    all_adoptions = Adoption.objects.all()

    context = {
        'name': name,
        'pets': all_pets,
        'appointments': all_appointments,  
        'adoptions': all_adoptions,
    }
    # Render the employee portal template
    return render(request, 'employee.html', context)


@login_required
def employee_logout(request):
    logout(request)

    return redirect('employee_login')

@login_required
def add_pet(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        species = request.POST.get('species')
        breed = request.POST.get('breed')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        adoption_status = request.POST.get('adoption_status')
        picture = request.FILES.get('picture')

        # Create and save the new Pet instance
        pet = Pet(
            name=name,
            species=species,
            breed=breed,
            age=age,
            gender=gender,
            adoption_status=adoption_status,
            picture=picture,
            date_of_arrival=timezone.now()
        )
        pet.save()
        return redirect('employee_portal') 

    return render(request, 'pets.html')


def adopter_signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'adopter_signup.html')

        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        adopter = Adopter(user=user, address=address, phone_number=phone_number)
        adopter.save()

        return redirect('adopter_login')

    return render(request, 'adopter_signup.html')

def adopter_login(request):
    if request.user.is_authenticated:
        try:
            Adopter.objects.get(user=request.user)
            return redirect('adopter_portal')
        except Adopter.DoesNotExist:
            pass
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('adopter_portal') # Redirect to adopter portal after login
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'adopter_login.html')

@login_required
def adopter_portal(request):
    adopter = request.user.adopter  # Assuming a logged-in user has a related Adopter object
    appointments = Appointment.objects.filter(adopter=adopter)
    adoptions = Adoption.objects.filter(adopter=adopter)
    context = {
        'adopter_name': f"{adopter.user.first_name} {adopter.user.last_name}",
        'address': adopter.address,
        'phone_number': adopter.phone_number,
        'appointments': appointments,
        'adoptions' : adoptions,
    }
    return render(request, 'adopter_portal.html', context)

@login_required
def adopter_logout(request):
    logout(request)
    return redirect('adopter_login')

@login_required
def edit_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    if request.method == 'POST':
        # Update pet details
        pet.name = request.POST.get('name', pet.name)
        pet.species = request.POST.get('species', pet.species)
        pet.breed = request.POST.get('breed', pet.breed)
        pet.age = request.POST.get('age', pet.age)
        pet.gender = request.POST.get('gender', pet.gender)
        pet.adoption_status = request.POST.get('adoption_status', pet.adoption_status)

        # Handle picture upload
        if 'picture' in request.FILES:
            pet.picture = request.FILES['picture']

        pet.save()

        # Handle veterinary records
        record_id = request.POST.get('record_id')
        if record_id:
            record = get_object_or_404(VeterinaryRecord, record_id=record_id)
            record.checkup_date = request.POST.get('checkup_date', record.checkup_date)
            record.health_issues = request.POST.get('health_issues', record.health_issues)
            record.treatment_given = request.POST.get('treatment_given', record.treatment_given)
            record.notes = request.POST.get('notes', record.notes)
            record.save()
        else:
            if(request.POST.get('checkup_date')):
                # Add new veterinary record
                VeterinaryRecord.objects.create(
                    pet=pet,
                    checkup_date=request.POST.get('checkup_date'),
                    health_issues=request.POST.get('health_issues'),
                    treatment_given=request.POST.get('treatment_given'),
                    notes=request.POST.get('notes')
                )

        return redirect('pets')  # Redirect to the pet list or detail view

    else:
        records = VeterinaryRecord.objects.filter(pet=pet)

    return render(request, 'edit_pet.html', {'pet': pet, 'records': records})

@login_required
def delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, pk=pet_id)
    pet.delete()
    return redirect('employee_portal')

def pet_profile(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    return render(request, 'pet_profile.html', {'pet': pet})

@login_required
def adopt_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    # Check if the pet is available for adoption
    if pet.adoption_status != 'Available':
        messages.error(request, "This pet is not available for adoption.")
        return redirect('pet_profile', pet_id=pet_id)

    # Check if the user is authenticated
    if not request.user.is_authenticated:
        messages.warning(request, "You need to log in to adopt a pet.")
        return redirect('adopter_login')  # Redirect to your login page

    try:
        adopter = Adopter.objects.get(user=request.user)
    except Adopter.DoesNotExist:
        # Handle case where user is logged in but not an adopter
        messages.warning(request, "You need to be an adopter to adopt a pet.")
        return redirect('register_as_adopter')  # Redirect to the registration or info page

    if request.method == 'POST':
        # Get the appointment date from the form
        appointment_date = request.POST.get('appointment_date')

        # Create an appointment record
        appointment = Appointment(
            pet=pet,
            appointment_date=appointment_date,  # Use the selected date
            purpose='Adoption',
            adopter=adopter  # Link the appointment to the adopter
        )
        appointment.save()

        # Update pet status
        pet.adoption_status = 'Pending Adoption'
        pet.save()

        messages.success(request, "Your appointment for adopting this pet has been scheduled.")
        return redirect('pet_profile', pet_id=pet_id)

    # Redirect or show a page for GET requests (optional)
    return redirect('pet_profile', pet_id=pet_id)

@login_required
def approve_adoption(request, appointment_id):
    
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id)

    if request.method == 'POST':
        pet = appointment.pet
        
        # Update the pet's adoption status
        pet.adoption_status = 'Adopted'
        pet.save()

        # Create a new Adoption record
        adoption = Adoption(
            adopter=appointment.adopter,
            pet=pet,
            adoption_date=timezone.now(),
            adoption_fee=0.0
        )
        adoption.save()

        # Delete the appointment record
        appointment.delete()

        # Display a success message
        messages.success(request, f"Adoption approved for {pet.name}.")
        return redirect('employee_portal')

    return redirect('employee_portal')

@login_required
def reject_adoption(request, appointment_id):

    appointment = get_object_or_404(Appointment, appointment_id=appointment_id)

    if request.method == 'POST':
        pet = appointment.pet
        pet.adoption_status = 'Available'
        pet.save()

        # Delete the appointment
        appointment.delete()

        messages.success(request, f"Adoption request for {pet.name} has been rejected.")
        return redirect('employee_portal')  
    
    return redirect('employee_portal')

def download_invoice(request, adoption_id):
    """Generate an invoice PDF for the given adoption ID."""
    adoption = get_object_or_404(Adoption, adoption_id=adoption_id)

    # Create the HttpResponse object
    response = HttpResponse(content_type='application/pdf')
    response[
        'Content-Disposition'
    ] = f'attachment; filename="invoice_{adoption.pet.name}.pdf"'

    # Create the PDF document
    doc = SimpleDocTemplate(
        response,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )

    # Define styles
    styles = getSampleStyleSheet()
    centered_style = ParagraphStyle(name='Center', alignment=TA_CENTER)

    # Add elements to the PDF
    elements = []

    # Title
    title = Paragraph('Pet Adoption Invoice', styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Invoice header
    invoice_number = f'INV-{adoption_id.zfill(5)}'
    header_data = [
        ['Invoice Number', 'Date', 'Due Date'],
        [invoice_number, adoption.adoption_date.strftime('%B %d, %Y'), 'Upon Receipt'],
    ]

    header_table = Table(header_data, colWidths=[2 * inch, 2 * inch, 2 * inch])
    header_table.setStyle(
        TableStyle(
            [
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )
    elements.append(header_table)
    elements.append(Spacer(1, 24))

    # Pet and adoption info
    adoption_info = [
        ['Pet Name', adoption.pet.name],
        ['Species', adoption.pet.species],
        ['Breed', adoption.pet.breed],
        ['Adoption Date', adoption.adoption_date.strftime('%B %d, %Y')],
        ['Adoption Fee', f'${adoption.adoption_fee:.2f}'],
        ['Adopter Name', adoption.adopter],
        ['Adopter Contact', adoption.adopter.phone_number],
    ]

    adoption_table = Table(adoption_info, colWidths=[2.5 * inch, 4 * inch])
    adoption_table.setStyle(
        TableStyle(
            [
                ('BACKGROUND', (0, 0), (0, -1), colors.grey),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (0, -1), 12),
                ('BACKGROUND', (1, 0), (-1, -1), colors.whitesmoke),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )
    elements.append(adoption_table)
    elements.append(Spacer(1, 24))

    # Footer note
    footer_note = Paragraph(
        'Thank you for adopting a pet! Your contribution helps us care for more animals in need.',
        styles['Normal'],
    )
    elements.append(footer_note)

    # Build the PDF
    doc.build(elements)

    return response
