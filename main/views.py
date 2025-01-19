from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, InternshipForm, ApplicationForm
from .models import Internship, Application
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserRegistrationForm()
    return render(request, 'main/register.html', {'form': form})

@login_required
def company_dashboard(request):
    internships = Internship.objects.filter(company=request.user)
    return render(request, 'main/company_dashboard.html', {'internships': internships})

@login_required
def create_internship(request):
    if request.method == 'POST':
        form = InternshipForm(request.POST)
        if form.is_valid():
            internship = form.save(commit=False)
            internship.company = request.user
            internship.save()
            return redirect('company_dashboard')
    else:
        form = InternshipForm()
    return render(request, 'main/create_internship.html', {'form': form})

@login_required
def student_dashboard(request):
    internships = Internship.objects.all()
    return render(request, 'main/student_dashboard.html', {'internships': internships})

@login_required
def internship_details(request, pk):
    internship = get_object_or_404(Internship, pk=pk)
    return render(request, 'main/internship_details.html', {'internship': internship})

@login_required
def apply_for_internship(request, pk):
    internship = get_object_or_404(Internship, pk=pk)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.student = request.user
            application.internship = internship
            application.save()
            return redirect('student_dashboard')
    else:
        form = ApplicationForm()
    return render(request, 'main/apply.html', {'form': form, 'internship': internship})

@login_required
def company_profile(request):
    internships = Internship.objects.filter(company=request.user)
    return render(request, 'main/company_profile.html', {'internships': internships})

@login_required
def edit_internship(request, pk):
    internship = get_object_or_404(Internship, pk=pk, company=request.user)
    if request.method == 'POST':
        form = InternshipForm(request.POST, instance=internship)
        if form.is_valid():
            form.save()
            return redirect('company_profile')
    else:
        form = InternshipForm(instance=internship)
    return render(request, 'main/edit_internship.html', {'form': form})

@login_required
def delete_internship(request, pk):
    internship = get_object_or_404(Internship, pk=pk, company=request.user)
    internship.delete()
    return redirect('company_profile')

@login_required
def student_profile(request):
    applications = Application.objects.filter(student=request.user)
    return render(request, 'main/student_profile.html', {'applications': applications})

@login_required
@login_required
def manage_applications(request):
    if request.user.user_type != 'company':
        return redirect('login')

    # Fetch internships created by this company
    internships = Internship.objects.filter(company=request.user)
    # Fetch applications for these internships
    applications = Application.objects.filter(internship__in=internships).select_related('internship', 'student')

    # Render the existing template
    return render(request, 'main/manage_applications.html', {
        'applications': applications
    })


@login_required
def update_application_status(request, pk, status):
    application = get_object_or_404(Application, pk=pk)
    application.status = status
    application.save()

    # Add a success message
    messages.success(request, f'Application marked as {status.capitalize()}.')

    return redirect('manage_applications')

class CustomLoginView(LoginView):
    def get_success_url(self):
        # Redirect based on user type
        if self.request.user.user_type == 'student':
            return '/student-dashboard/'  # Replace with your student dashboard URL
        elif self.request.user.user_type == 'company':
            return '/company-dashboard/'  # Replace with your company dashboard URL
        else:
            return '/'  # Fallback to homepage or another default page
        
def available_internships(request):
    if request.user.user_type != 'student':
        return redirect('login')

    # Fetch internships that are open for applications
    internships = Internship.objects.filter(Q(status='open'))

    return render(request, 'main/available_internships.html', {'internships': internships})

