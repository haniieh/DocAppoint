from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from health.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home,name="home"),
    path('login', Login,name="login"),
    path('register', Registeration,name="register"),
    path('logout', Logout,name="logout"),
    path('cancel_appointment<int:pid>', cancel_appointment,name="cancel_appointment"),
    path('patient_invoices<int:pid><str:task>', patient_invoices,name="patient_invoices"),

#Admin 
    path('admin_dashboard', admin_dashboard,name="admin_dashboard"),
    path('all_appointments', all_appointments,name="all_appointments"),
    path('display_doctors', display_doctors,name="display_doctors"),
    path('display_patients', display_patients,name="display_patients"),
    path('request_healthcard', request_healthcard,name="request_healthcard"),
    path('grant_card<int:pid>', grant_card,name="grant_card"),
    path('card_cancelation<int:pid>', card_cancelation,name="card_cancelation"),
    path('delete_patient<int:pid>', delete_patient,name="delete_patient"),
    path('user_cards', user_cards,name="user_cards"),
    path('display_medical', display_medical,name="display_medical"),
    path('dr_invoices<int:pid>', dr_invoices,name="dr_invoices"),
    path('admin_patient_search_by_username', admin_patient_search_by_username, name="admin_patient_search_by_username"),
    path('admin_profile', admin_profile, name="admin_profile"),
    path('edit_admin_profile', edit_admin_profile, name="edit_admin_profile"),

#Patient 
    path('dashboard_for_patient', dashboard_for_patient,name="dashboard_for_patient"),
    path('profile_for_patient', profile_for_patient,name="profile_for_patient"), 
    path('patient_update_password', patient_update_password,name="patient_update_password"),
    path('search_dr', search_dr,name="search_dr"), 
    path('booked_paid<int:pid>', booked_paid,name="booked_paid"),
    path('payment<int:pid>', payment,name="payment"),
    path('appointment<int:pid>', appointment,name="appointment"),
    path('patient_appoinment', patient_appoinment,name="patient_appoinment"), 
    path('patient_confirmed_appoinments',patient_confirmed_appoinments,name="patient_confirmed_appoinments"),
    path('history_p_appointment',history_p_appointment,name="history_p_appointment"),
    path('patient_search_appoinment',patient_search_appoinment,name="patient_search_appoinment"),
    path('healthcard',healthcard,name="healthcard"),
    path('success_request',success_request,name="success_request"),
    path('apply_healthcard',apply_healthcard,name="apply_healthcard"),
    path('dr_appointments_all',dr_appointments_all,name="dr_appointments_all"),
    path('display_dr_profile_by_name/<str:username>',display_dr_profile_by_name, name="display_dr_profile_by_name"),
    path('display_dr_calender/<str:username>',display_dr_calender,name='display_dr_calender'),

#dr
    path('dr_dashboard', dr_dashboard,name="dr_dashboard"),
    path('dr_profile', dr_profile,name="dr_profile"),
    path('dr_update_password', dr_update_password,name="dr_update_password"),
    path('dr_appointment', dr_appointment,name="dr_appointment"),
    path('update_status<int:pid>', update_status,name="update_status"),
    path('dr_confirmed_appoinment',dr_confirmed_appoinment,name="dr_confirmed_appoinment"),
    path('dr_history_appoinment',dr_history_appoinment,name="dr_history_appoinment"),
    path('new_medicine<int:pid>', new_medicine, name="new_medicine"),
    path('doctor_invoice<int:pid>', doctor_invoices, name="doctor_invoice"),
    path('doctor_cancel_appointment<int:pid>', doctor_cancel_appointment, name="doctor_cancel_appointment"),
    path('patient_dashboard<int:pid>', patient_dashboard, name="patient_dashboard"),
    path('doctor_status<int:pid>', doctor_status, name="doctor_status"),
    path('d_search_appointment',d_search_appointment,name="d_search_appointment"),
    path('patient_appointment',patient_appointment,name="patient_appointment"),
    path('doctor_patient_search_by_username', doctor_patient_search_by_username, name="doctor_patient_search_by_username"),
    path('my_patient', my_patient, name="my_patient"),
    path('add_prescription<int:pid>', add_prescription, name="add_prescription"),
    path('add_presc<int:pid>', add_presc, name="add_presc"),
    path('add_medical<int:pid>', add_medical, name="add_medical"),
    path('add_bill<int:pid>', add_bill, name="add_bill"),
    path('add_bil<int:pid>', add_bil, name="add_bil"),
    path('delete_presc<int:pid>', delete_presc, name="delete_presc"),
    path('delete_bill<int:pid>', delete_bill, name="delete_bill"),
    path('confirmation_by_admin',confirmation_by_admin,name='confirmation_by_admin'),

#Medical 
    path('medical_dashboard', medical_dashboard,name="medical_dashboard"),
    path('medical_profile', medical_profile,name="medical_profile"),
    path('medical_update_password', medical_update_password,name="medical_update_password"),
    path('patient_search_id', patient_search_id, name="patient_search_id"),
    path('medical_invoices<int:pid>', medical_invoices, name="medical_invoices"),
    path('medical_add_medicine<int:pid>', medical_add_medicine, name="medical_add_medicine"),
    path('patient_invoices_all', patient_invoices_all, name="patient_invoices_all"),
    path('medical_status<int:pid>', medical_status, name="medical_status"),
    path('all_prescription',all_prescription,name="all_prescription")

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)