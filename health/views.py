from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,logout,login
from .models import Patient, Doctor, Medical, Appointment
from .models import Doctors_Invoice, Adminstration, Prescription, Medical_Record, Billing_Record
import datetime
import uuid
import random
from django.db.models import Avg,Sum,Count,Min,Max
from random import randint
from datetime import timedelta
from datetime import date
from django.db.models import Sum, F, FloatField
from django.db.models.functions import Cast



# Create your views here.
def access(user):
    try:
        user = Doctor.objects.get(user=user)
        if user.status == "pending":
            return False
        else:
            return True
    except:
        try:
            user = Medical.objects.get(user=user)
            if user.status == "pending":
                return False
            else:
                return True
        except:
            try:
                if user.status == "pending":
                    return False
                else:
                    return True
            except:
                pass

def dashboard_for_patient(request):
    appointment = Appointment.objects.filter(patient=Patient.objects.get(user=request.user))
    return render(
        request,
        'patient/dashboard_for_patient.html',
        context={'appointment':appointment}
        )

def dr_appointments_all(request):
    appointment = Appointment.objects.filter(patient=Patient.objects.get(user=request.user))
    return render(
        request,
        'patient/dr_appointments.html',
        context={'data':appointment}
        )

def patient_appointment(request):
    appointment = Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user))
    return render(
        request,
        'dr/patient_appointment.html',
        context={'data':appointment}
        )


def patient_invoices_all(request):
    appointment=Appointment.objects.all()
    print(appointment)
    return render(
        request,
        'medical/patient_invoices_all.html',
        context={'data':appointment}
        )

def all_prescription(request):
    patients = Patient.objects.all()
    data = []
    for patient in patients:
        appointments = patient.appointment_set.all()
        appointments_data = []
        for appointment in appointments:
            prescriptions = appointment.prescription_set.all()
            prescriptions_data = []
            for prescription in prescriptions:
                prescription_data = {
                    'name': prescription.name,
                    'quantity': prescription.quantity,
                    'days': prescription.days,
                    'time': prescription.time,
                }
                prescriptions_data.append(prescription_data)
            appointment_data = {
                'doctor_username': appointment.doctor.user.username,
                'prescriptions': prescriptions_data,
            }
            appointments_data.append(appointment_data)
        patient_data = {
            'first_name': patient.user.first_name,
            'last_name': patient.user.last_name,
            'appointments': appointments_data,
        }
        data.append(patient_data)
    print(data)
    return render(request, 'medical/all_prescription.html', context={'data': data})

def dr_dashboard(request):
    today_date = datetime.date.today()
    data = Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user))
    pend = Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user),status="pending")
    appointment = Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user)).count()
    up = Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user), a_date__gte=today_date).exclude(a_date=today_date)
    today = Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user), a_date=today_date)
    t_today = today.count()
    t_pending = pend.count()
    context = {
        'data': data,
        'total': appointment,
        'up': up,
        'today': today,
        't_today':t_today,
        't_pending':t_pending
        }
    return render(
        request,
        'dr/dr_dashboard.html',
        context
        )

def medical_dashboard(request):
    return render(
        request,
        'medical/medical_dashboard.html'
        )

def home(request):
    data=Doctor.objects.all()
    doc = ""
    if request.method == "POST":
        location = request.POST['loc']
        specialist = request.POST['spe']
        if location and specialist:
            doc  = Doctor.objects.filter(cl_address__icontains = location,specialist__icontains = specialist)
        elif not location and specialist:
            doc  = Doctor.objects.filter(specialist__icontains = specialist)
        elif location and not specialist:
            doc  = Doctor.objects.filter(cl_address__icontains = location)
        else:
            doc = Doctor.objects.all()
    try:
        user = User.objects.get(username=request.user)
        error = Patient.objects.get(user=user)
        return redirect('dashboard_for_patient')
    except:
        try:
            user = User.objects.get(username=request.user)
            error = Doctor.objects.get(user=user)
            return redirect('dr_dashboard')
        except:
            try:
                user = User.objects.get(username=request.user)
                error = Medical.objects.get(user=user)
                return redirect('medical_dashboard')
            except:
                try:
                    user = User.objects.get(username=request.user)
                    if user.is_staff:
                        return redirect('admin_dashboard')
                except:
                    pass
    
    return render(
        request,
        'index.html',
        context={'data':data,'doc':doc}
        )

def Registeration(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            mode = request.POST['mode']
            if mode == "Patient":
                Patient.objects.create(user=user)
            if mode == "Doctor":
                Doctor.objects.create(user=user,status="pending")
            if mode == "Medical":
                Medical.objects.create(user=user,status="pending")
            messages.success(request,'You have Registered Successfully')
            return redirect('login')
    else:
        form = SignUpForm()
    
    return render(
        request,
        'register.html',
        context = {'form':form}
        )

def Login(request):
    if request.method == "POST":
        user_name = request.POST['username']
        user_password = request.POST['password']
        user = authenticate(username=user_name,password=user_password)
        if user is not None:
            login(request,user)
            messages.success(request,'You logged in successfully!')
            return redirect('home')
        else:
            messages.success(request,'The credientials are not valid!')
            return redirect('login')
        
    return render(
        request,
        'login.html'
        )

def Logout(request):
    logout(request)
    messages.info(request,'You have logged out successfully!')
    return redirect('login')

def profile_for_patient(request):
    user = User.objects.get(id=request.user.id)
    print(user)
    patient = Patient.objects.get(user=user)
    form = PatientForm(request.POST or None,instance=patient)
    if request.method == "POST":
        form = PatientForm(request.POST,request.FILES,instance=patient)
        if form.is_valid():
            try:
                for info in [request.POST['first_name'],request.POST['last_name']]:  
                    for letter in info:
                        if not letter.isalpha():
                            return messages.success(request,'Please enter valid name')
            except:
                pass
            form.save()
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.save()
            messages.success(request,'Profile Updated Successfully!')
            return redirect("profile_for_patient")
    
    return render(
        request,
        'patient/profile.html',
        context= {'form':form}
        )

def patient_update_password(request):
    if request.method=="POST":
        old_pass = request.POST['pwd1']
        new_pass = request.POST['pwd2']
        confirmed_pass = request.POST['pwd3']
        if new_pass == confirmed_pass:
            user = User.objects.get(username__exact=request.user.username)
            user.set_password(confirmed_pass)
            user.save()
            messages.success(request,'Your password updated successfully!')
            return redirect("patient_update_password")
    return render(
        request,
        'patient/update_password.html'
        )

def display_dr_profile_by_name(request,username):
    user = User.objects.get(username=username)
    doctor = Doctor.objects.get(user=user)
    print(doctor.addr)
    return render(
        request,
        'patient/dr_profile.html',
        context={'data':user,'dr':doctor}
        )



def dr_profile(request):
    user = User.objects.get(id=request.user.id)
    doctor = Doctor.objects.get(user=user)
    form = DoctorForm(request.POST or None,instance=doctor)
    if request.method == "POST":
        form = DoctorForm(request.POST or None,request.FILES or None, instance=doctor)
        if form.is_valid():
            form.save()
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.save()
            messages.success(request,'Profile Updated Successfully')
            return redirect("dr_profile")
   
    return render(
        request,
        'dr/profile.html',
        context = {'doc':doctor,'form':form}
        )

def dr_update_password(request):
    if request.method=="POST":
        old_pass= request.POST['pwd1']
        new_pass = request.POST['pwd2']
        confirmed_pass = request.POST['pwd3']
        if new_pass == confirmed_pass:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(confirmed_pass)
            u.save()
            messages.success(request,'Password Changed Successfully')
            return redirect("dr_update_password")
    return render(
        request,
        'dr/update_password.html'
        )

def search_dr(request):
    data = Doctor.objects.all()
    location = "All"
    gender = "All"
    specialist = "All"
    if request.method == "POST":
        location = ""
        specialist = ""
        gender = ""
        try:
            location = request.POST['location']
        except:
            pass
        try:
            gender = request.POST['gender_type']
        except:
            pass
        data = Doctor.objects.filter(gender__icontains=gender,cl_address__icontains=location)
    
    return render(
        request,
        'patient/search_dr.html',
        context={'data':data,'l':location,'g':gender,'s':specialist}
        )

def display_dr_calender(request,username):
    user = User.objects.get(username=username)
    dr = Doctor.objects.get(user=user)
    # appointment = Appointment.objects.get(doctor=dr)
    appointments = Appointment.objects.filter(doctor=dr)
    print(dr.image)
    return render(
        request,
        'patient/display_dr_calender.html',
        context={
        "user":user,
        "dr":dr,
        "appointments":appointments
        })


def appointment(request,pid):
    doctor=Doctor.objects.get(id=pid)
    if request.method == "POST":
        a = request.POST['a_date']
        from_time = request.POST['from_time']
        to_time = request.POST['to_time']
        app=Appointment.objects.create(
            doctor=doctor,
            patient=Patient.objects.get(user=request.user),
            a_date=a,
            from_time=from_time,
            to_time=to_time,
            status="pending",
            p_status="pending"
            )
        messages.success(
            request,
            "Appointment Request Sent Successfully"
            )
        return redirect("payment",app.id)
    return render(
        request,
        'patient/appointment.html',
        context={'doctor':doctor}
        )

def payment(request,pid):
    data=Appointment.objects.get(id=pid)
    if request.method=="POST":
        data.p_status="complete"
        data.save()
        messages.success(
            request,
            "Payment Completed Successfully"
            )
        return redirect("booked_paid",data.id)

    return render(
        request,
        'patient/payments.html',
        context={'data':data}
        )

def booked_paid(request,pid):
    appointment=Appointment.objects.get(id=pid)
    return render(
        request,
        'patient/booked_paid.html',
        context={'data':appointment}
        )

def patient_appoinment(request):
    appointment=Appointment.objects.filter(patient=Patient.objects.get(user=request.user),status="pending")
    return render(
        request,
        'patient/patient_appoinment.html',
        context={'data':appointment}
        )

def dr_appointment(request):
    if not access(request.user):
        messages.success(
            request,
            'Update Your Profile and Wait for Verification'
            )
        return redirect('dr_profile')
    appointment=Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user),status="pending")
    return render(
        request,
        'dr/dr_appoinment.html',
        context={'data':appointment}
        )

def update_status(request,pid):
    if not access(request.user):
        messages.success(
            request,
            'Your profile has been updated. Please wait for verification.'
            )
        return redirect('dr_profile')
    appointment=Appointment.objects.get(id=pid)
    form=AppointmentForm(request.POST or None,instance=appointment)
    to_time = request.GET.get('to_time')
    if request.method=="POST":
        print(request)
        a_date=request.POST['a_date']
        from_time = request.POST['from_time']
        to_time = request.POST['to_time']
        appointment.a_date=a_date
        appointment.from_time = from_time
        appointment.to_time = to_time
        appointment.status="confirmed"
        appointment.save()
        messages.success(request,"Payment Completed Successfully, and the appoitment booked Successfully")
        return redirect("dr_appointment")
    else:
        print("probelm")
    return render(
        request,
        'dr/update_status.html',
        context={'form':form,'data':appointment}
        )

def patient_confirmed_appoinments(request):
    today_date=datetime.date.today()
    appointment=Appointment.objects.filter(patient=Patient.objects.get(user=request.user),status="confirmed",a_date__gte=today_date)
    return render(
        request,
        'patient/patient_confirmed_appoinments.html',
        context={'data':appointment}
        )

def confirmation_by_admin(request):
    return render(request,'dr/confirmation_by_admin.html')

def dr_confirmed_appoinment(request):
    if not access(request.user):
        messages.success(
            request,
            'Your profile have been updated. Please wait for verification'
            )
        return redirect('confirmation_by_admin')
        # return redirect('dr_profile')
    today_date=datetime.date.today()
    appointment=Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user),status="confirmed",a_date__gte=today_date)
    return render(
        request,
        'dr/dr_confirmed_appoinment.html',
        context={'data':appointment}
        )

def history_p_appointment(request):
    today_date=datetime.date.today()
    appointment=Appointment.objects.filter(patient=Patient.objects.get(user=request.user))
    return render(
        request,
        'patient/history_appoinment.html',
        context={'data':appointment}
        )

def new_medicine(request,pid):
    if not access(request.user):
        messages.success(
            request,
            'Your profile have been updated. Please wait for verification!'
            )
        return redirect('dr_profile')
    appointment = Appointment.objects.get(id=pid)
    med = Doctors_Invoice.objects.filter(appointment=appointment)
    if request.method == "POST":
        my_medicine = request.POST['name']
        my_presription = request.POST['presc']
        Doctors_Invoice.objects.create(appointment=appointment,medicine=my_medicine,prescription=my_presription)
        messages.success(request,'The Medicine added!')
        return redirect('new_medicine_add',appointment.id)
    return render(
        request,
        'dr/new_medicine.html',
        context={'med':med}
        )

def dr_history_appoinment(request):
    if not access(request.user):
        messages.success(
            request,
            'Update Your Profile and Wait for Verification'
            )
        return redirect('dr_profile')
    today_date=datetime.date.today()
    appointment=Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user))
    return render(
        request,
        'dr/dr_history_appoinment.html',
        context={'data':appointment}
        )

def patient_search_appoinment(request):
    appointment=""
    form_date = ""
    to_date = ""
    if request.method=="POST":
        form_date=request.POST['from_date']
        to_date=request.POST['to_date']
        i1 = datetime.datetime.fromisoformat(form_date)
        i2 = datetime.datetime.fromisoformat(to_date)
        appointment = Appointment.objects.filter(patient=Patient.objects.get(user=request.user),a_date__gte=datetime.date(i1.year,i1.month,i1.day),a_date__lte=datetime.date(i2.year,i2.month,i2.day))
    return render(
        request,
        'patient/patient_search_appoinment.html',
        context={'data':appointment,'u':form_date,'v':to_date}
        )

def Login_Admin(request):
    error = False
    if request.method == 'POST':
        user_name = request.POST['username']
        my_pass = request.POST['password']
        user = authenticate(username=user_name, password=my_pass)
        if user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            error = True
    return render(
        request,
        'login.html',
        context={'error': error}
        )

def admin_dashboard(request):
    total_doctors = Doctor.objects.all().count()
    total_patients = Patient.objects.all().count()
    total_appointments = Appointment.objects.all().count()
    return render(
        request,
        'admin/admin_dashboard.html',
        context = {'t_doc':total_doctors,'t_pat':total_patients,'t_app2':total_appointments}
        )

def all_appointments(request):
    appointment=Appointment.objects.all()
    return render(
        request,
        'admin/all_appointments.html',
        context={'data':appointment}
        )


def display_doctors(request):
    doctor=Doctor.objects.all()
    return render(
        request,
        'admin/display_doctors.html',
        context={'data':doctor}
        )

def display_patients(request):
    patient=Patient.objects.all()
    return render(
        request,
        'admin/display_patients.html',
        context={'data':patient}
        )

def generate_uid():
    uid_no = ""
    digits = [0] * 10
    for i in range(10000):
        x = str(uuid.uuid4().int)[:4]
        for d in x:
            digits[int(d)] += 1
    for i in digits[:4]:
        uid_no+=str(i)
    return uid_no

def healthcard(request):
    patients=Patient.objects.get(user = request.user)
    if patients.health_uid == None:
        while 1:
            uid_no = generate_uid()
            pat = Patient.objects.filter(health_uid=uid_no)
            if pat:
                continue
            else:
                patients.health_uid = uid_no
                num = random.randrange(1, 10**3)
                cv_no = str(random.randrange(1, 10**3))
                if len(cv_no) == 2:
                    patients.cvv = "1"+cv_no
                elif len(cv_no) == 1:
                    patients.cvv = "1"+cv_no+"2"
                elif len(cv_no) == 0:
                    patients.cvv = "123"
                else:
                    patients.cvv = cv_no
                patients.ex_month = int(datetime.date.today().month)
                patients.ex_year = int(datetime.date.today().year) + 5
                patients.save()
                break
    first = patients.health_uid[:4]
    second = patients.health_uid[4:8]
    third = patients.health_uid[8:12]
    fourth = patients.health_uid[12:16]
    return render(
        request,
        'patient/healthcard.html',
        context={'data':patients,'first':first,'second':second,'third':third,'fourth':fourth}
        )

def apply_healthcard(request):
    return render(
        request,
        'patient/apply_healthcard.html'
        )

def success_request(request):
    patients = Patient.objects.get(user=request.user)
    patients.card_status ="pending"
    patients.save()
    return render(
        request,
        'patient/success_request.html'
        )

def request_healthcard(request):
    patients = Patient.objects.filter(card_status="pending")
    return render(
        request,
        'admin/request_healthcard.html',
        context={'data':patients}
        )

def make_random():
    random_16_digits = ''
    for i in range(16):
        random_16_digits = random_16_digits + str(randint(0,9))
    return random_16_digits

def make_random3():
    random_3_digits = ''
    for i in range(3):
        random_3_digits = random_3_digits + str(randint(0,9))
    return random_3_digits

def get_year():
    expiry_year=(date.today().year)+5
    current_month=date.today().month
    return expiry_year, current_month

def grant_card(request,pid):
    expiry_year, current_month = get_year()
    patients = Patient.objects.get(id=pid)
    patients.health_uid = make_random()
    patients.ex_year = expiry_year
    patients.ex_month = current_month
    patients.cvv = make_random3()
    patients.card_status = "accepted"
    patients.save()
    messages.success(
        request,
        "You have given access for health card to "+patients.user.username+ " successfully!"
        )
    return redirect('user_cards')

def card_cancelation(request,pid):
    patients = Patient.objects.get(id=pid)
    patients.card_status = None
    patients.health_uid = None
    patients.ex_month = None
    patients.ex_year = None
    patients.cvv = None
    patients.save()
    messages.success(
        request,
        "You have canceled the health card of "+patients.user.username+ " successfully!"
        )
    return redirect('user_cards')

def user_cards(request):
    patients = Patient.objects.filter(card_status="accepted")
    return render(
        request,
        'admin/user_cards.html',
        context={'data':patients}
        )

def cancel_appointment(request,pid):
    appoitment = Appointment.objects.get(id=pid)
    appoitment.delete()
    messages.success(
        request,
        'The appointment cancelled successfully!'
        )
    return redirect('patient_appoinment')


def doctor_cancel_appointment(request,pid):
    appoitment = Appointment.objects.get(id=pid)
    appoitment.delete()
    messages.success(
        request,
        'The appointment cancelled successfully!'
        )
    return redirect('dr_appointment')

def patient_invoices(request,pid,task):
    appointment = Appointment.objects.get(id=pid)
    billing_record=""
    total = 0
    try:
        billing_record = Billing_Record.objects.filter(appoint=appointment)
        total = str(billing_record.aggregate(Sum('amount')))[14:][:-1]
    except:
        pass
    dr_invoice = Doctors_Invoice.objects.filter(appointment=appointment)
    return render(
        request,
        'invoices.html',
        context = {'pat':appointment,'med':dr_invoice,'total':total,'task':task}
        )


def dr_invoices(request,pid):
    appointment = Appointment.objects.get(id=pid)
    prescription = Prescription.objects.filter(appoint=appointment)
    total = str(prescription.aggregate(Sum('price')))[14:][:-1]
    return render(
        request,
        'admin/dr_invoices.html',
        context = {'pat':appointment,'med':prescription,'total':total}
        )

def medical_profile(request):
    user = User.objects.get(id=request.user.id)
    medical = Medical.objects.get(user=user)
    medical_form = MedicalForm(request.POST or None,instance=medical)
    if request.method == "POST":
        medical_form = MedicalForm(request.POST or None,request.FILES or None, instance=medical)
        if medical_form.is_valid():
            medical_form.save()
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.save()
            messages.success(request,'Profile Updated Successfully')
            return redirect("medical_profile")
    return render(
        request,
        'medical/profile.html',
        context={'doc':medical,'form':medical_form}
        )

def medical_update_password(request):
    if request.method=="POST":
        old_password = request.POST['pwd1']
        new_password = request.POST['pwd2']
        confirmed_password = request.POST['pwd3']
        if new_password == confirmed_password:
            user = User.objects.get(username__exact=request.user.username)
            user.set_password(confirmed_password)
            user.save()
            messages.success(
                request,
                'The password updated successfully!'
                )
            return redirect("medical_update_password")
    return render(
        request,
        'medical/update_password.html'
        )

def patient_search_id(request):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('medical_profile')
    patient=""
    uid=""
    appointment=""
    if request.method=="POST":
        uid=request.POST['uid']
        try:
            patient=Patient.objects.get(health_uid=uid)
            appointment = Appointment.objects.filter(patient=patient)
        except:
            messages.success(request,'Invalid Card Number')
    return render(
        request,
        'medical/patient_search_id.html',
        context={'data':patient,'i':uid,'appointment':appointment}
        )

def display_medical(request):
    medical=Medical.objects.all()
    return render(
        request,
        'admin/display_medical.html',
        context={'data':medical}
        )

def medical_invoices(request,pid):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('medical_profile')
    appointment = Appointment.objects.get(id=pid)
    prescription = Prescription.objects.filter(appoint=appointment)
    total = str(prescription.aggregate(Sum('price')))[14:][:-1]
    return render(
        request,
        'medical/invoices.html',
        context = {'pat':appointment,'med':prescription,'total':total}
        )


def doctor_invoices(request,pid):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('dr_profile')
    appointment = Appointment.objects.get(id=pid)
    med = Doctors_Invoice.objects.filter(appointment=appointment)
    # total = str(med.aggregate(Sum('price')).values)
    total = med.aggregate(total_price=Sum(Cast('price', FloatField()))).get('total_price')


    return render(
        request,
        'dr/invoices.html',
        context={'pat':appointment,'med':med,'total':total}
        )

def medical_add_medicine(request,pid):
    if not access(request.user):
        messages.success(
            request,
            'Update Your Profile and Wait for Verification'
            )
        return redirect('medical_profile')
    appointment  = Appointment.objects.get(id=pid)
    prescription = Prescription.objects.filter(appoint=appointment)
    count = prescription.count()
    if request.method == "POST":
        for i in prescription:
            p = request.POST["price"+str(i.id)]
            i = request.POST["id"+str(i.id)]
            doc = Prescription.objects.get(id=i)
            doc.price = p
            doc.save()
        appointment.medical = Medical.objects.get(user=request.user)
        appointment.save()
        messages.success(request,'Price Updated Successfully')
        return redirect('medical_invoices',appointment.id)
    return render(
        request,
        'medical/add_new_medicine.html',
        context={'med':prescription,'data':appointment}
        )

def d_search_appointment(request):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('dr_profile')
    appointment=""
    from_date = ""
    to_date = ""
    if request.method=="POST":
        from_date=request.POST['from_date']
        to_date=request.POST['to_date']
        i1 = datetime.datetime.fromisoformat(from_date)
        i2 = datetime.datetime.fromisoformat(to_date)
        appointment = Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user),a_date__gte=datetime.date(i1.year,i1.month,i1.day),a_date__lte=datetime.date(i2.year,i2.month,i2.day))
    return render(
        request,
        'dr/search_appoinment.html',
        context={'data':appointment,'u':from_date,'v':to_date}
        )

def doctor_status(request,pid):
    dr = Doctor.objects.get(id=pid)
    if dr.status=="pending":
        dr.status = "accept"
        dr.save()
        messages.success(
            request,
            'Selected Doctor granted to Permission'
            )
    else:
        dr.status = "pending"
        dr.save()
        messages.success(
            request,
              'Selected Doctor Withdraw to Permission'
              )
    return redirect('display_doctors')

def medical_status(request,pid):
    medical = Medical.objects.get(id=pid)
    medical.status = "accept"
    medical.save()
    messages.success(
        request,
        'Selected Medical granted to Permission'
        )
    return redirect('display_medical')

def doctor_patient_search_by_username(request):
    if not access(request.user):
        messages.success(
            request,
            'Update Your Profile and Wait for Verification'
            )
        return redirect('dr_profile')
    my_patient=""
    uid=""
    appointment=""
    if request.method=="POST":
        uid=request.POST['uid']
        try:
            my_patient=Patient.objects.get(health_uid=uid)
            appointment = Appointment.objects.filter(patient=my_patient)
        except:
            messages.success(request,'Invalid Card Number')
    return render(
        request,
        'dr/patient_search_by_username.html',
        context={'data':my_patient,'i':uid,'appointment':appointment}
        )

def admin_patient_search_by_username(request):
    username = ""
    user= None
    patient=""
    appointment =""
    if request.method=="POST":
        username = request.POST['username']
        try:
            user = User.objects.get(username=username)
            patient=Patient.objects.get(user=user)            
            appointment = Appointment.objects.filter(patient=patient)
        except:
            messages.success(request,'Invalid username')
    context = {'data':user,'patient':patient,'appointment':appointment}
    return render(
        request,
        'admin/patient_search_by_username.html',
        context
        )

def admin_profile(request):
    return render(
        request,
        'admin/profile.html'
        )

def edit_admin_profile(request):
    adminstr = Adminstration.objects.get(id=request.user.id)
    if request.method == "POST":
        try:
            f_name = request.POST['fname']
            l_name = request.POST['lname']
            mob = request.POST['mobile']
            addr = request.POST['address']
            email = request.POST['email']
            try:
                img = request.FILES['images']
                adminstr.image = img
                adminstr.save()
            except:
                pass
            adminstr.user.first_name = f_name
            adminstr.user.last_name = l_name
            adminstr.user.email = email
            adminstr.address = addr
            adminstr.mobile = mob
            adminstr.image = img
            adminstr.user.save()
            adminstr.save()
            messages.success(
                request,
                'Profile Updated Successfully'
                )
        except:
            pass
        try:
            old_password = request.POST['pwd1']
            new_password = request.POST['pwd2']
            confirmed_pass = request.POST['pwd3']
            if new_password == confirmed_pass:
                user = User.objects.get(username__exact=request.user.username)
                user.set_password(d)
                user.save()
                messages.success(
                    request,
                      'The password changed successfully'
                      )
        except:
            pass
    return redirect('admin_profile')

def my_patient(request):
    if not access(request.user):
        messages.success(request,'Your profile have been updated. Please wait for verification.')
        return redirect('confirmation_by_admin')
    data = Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user),status="confirmed")
    return render(
        request,
        'dr/my_patient.html',
        context= {'data':data}
        )

def patient_dashboard(request,pid):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('dr_profile')
    my_patients = Patient.objects.get(id=pid)
    dr = Doctor.objects.get(user=request.user)
    appointment = Appointment.objects.filter(patient = my_patients)
    appoint = Appointment.objects.filter(patient = my_patients,doctor=dr).first()
    if not appoint:
        appoint = 0
    else:
        appoint = appoint.id
    return render(
        request,
        'dr/patient_dashboard.html',
        context = {'data': appointment,'pat':my_patients,'pat2':appoint}
        )

def add_presc(request,pid):
    if not access(request.user):
        messages.success(
            request,
            'Update your profile and wait for verification.'
            )
        return redirect('dr_profile')
    appoint  = Appointment.objects.get(id=pid)
    if request.method == "POST":
        name = request.POST['name']
        presc = request.POST['presc']
        day = request.POST['days']
        cal_time = request.POST.getlist('time[]')
        Prescription.objects.create(appoint=appoint,name=name,quantity=presc,days=day,time=cal_time)
        messages.success(
            request,
            'the prescription added!'
            )
        return redirect('add_prescription',appoint.id)

def add_prescription(request,pid):
    if not access(request.user):
        messages.success(
            request,
            'Update Your Profile and Wait for Verification'
            )
        return redirect('dr_profile')
    appoint=""
    try:
        appoint  = Appointment.objects.get(id=pid)
    except:
        pass
    if request.method == "POST":
        messages.success(request,'One Medicine added')
        return redirect('patient_dashboard',appoint.patient.id)
    return render(
        request,
        'dr/add_new_prescription.html',
        context={'data':appoint}
        )

def add_medical(request,pid):
    if not access(request.user):
        messages.success(
            request,
            'Update Your Profile and Wait for Verification'
            )
        return redirect('dr_profile')
    appoint = ""
    try:
        appoint = Appointment.objects.get(id=pid)
    except:
        pass
    if request.method == "POST":
        desc = request.POST['desc']
        my_date = request.POST['date']
        my_files = request.FILES['file']
        Medical_Record.objects.create(appoint=appoint,disc=desc,file=my_files,date=my_date)
        messages.success(
            request,
            'Medical Record Added Successfully'
            )
        return redirect('patient_dashboard',appoint.patient.id)

#deklete one of the add billlllllss????????????????
def add_bil(request,pid):
    if not access(request.user):
        messages.success(
            request,
            'Update Your Profile and Wait for Verification'
            )
        return redirect('dr_profile')
    data = Appointment.objects.get(id=pid)
    if request.method == "POST":
        m = request.POST['title']
        p = request.POST['amount']
        Billing_Record.objects.create(appoint=data,title=m,amount=p)
        messages.success(
            request,
            'One Medicine added')
        return redirect('add_bill',data.id)

def add_bill(request,pid):
    if not access(request.user):
        messages.success(
            request,
            'Update Your Profile and Wait for Verification'
            )
        return redirect('dr_profile')
    appointment = Appointment.objects.get(id=pid)
    if request.method == "POST":
        messages.success(request,'One Billing Record added Successfully')
        return redirect('patient_dashboard',appointment.patient.id)
    return render(
        request,
        'dr/new_billing.html',
        context={'data':appointment}
        )

def delete_bill(request,pid):
    billing_rec = Billing_Record.objects.get(id=pid)
    billing_rec.delete()
    messages.success(
        request,
        'Biling Record deleted successfully'
        )
    return redirect('add_bill',billing_rec.appoint.id)

def delete_presc(request,pid):
    prescr = Prescription.objects.get(id=pid)
    prescr.delete()
    messages.success(request,'Prescription deleted successfully')
    return redirect('add_prescription',prescr.appoint.id)

def delete_patient(request,pid):
    patinets = Patient.objects.get(id=pid)
    patinets.delete()
    messages.success(request,'Patient deleted successfully')
    return redirect('display_patients')