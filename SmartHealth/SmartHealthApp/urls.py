from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),	      
			path("PatientLogin.html", views.PatientLogin, name="PatientLogin"),
			path("DoctorLogin.html", views.DoctorLogin, name="DoctorLogin"),
			path("PatientSignup.html", views.PatientSignup, name="PatientSignup"),
			path("PatientSignupAction", views.PatientSignupAction, name="PatientSignupAction"),
			path("PatientLoginAction", views.PatientLoginAction, name="PatientLoginAction"),
			path("DoctorLoginAction", views.DoctorLoginAction, name="DoctorLoginAction"),
			path("AdminLogin.html", views.AdminLogin, name="AdminLogin"),
			path("AdminLoginAction", views.AdminLoginAction, name="AdminLoginAction"),
			path("AddDoctor.html", views.AddDoctor, name="AddDoctor"),
			path("AddDoctorAction", views.AddDoctorAction, name="AddDoctorAction"),
			path("ViewHospitalDetails", views.ViewHospitalDetails, name="ViewHospitalDetails"),
			path("AddHealth.html", views.AddHealth, name="AddHealth"),
			path("AddHealthAction", views.AddHealthAction, name="AddHealthAction"),
			path("ViewPatientHospital", views.ViewPatientHospital, name="ViewPatientHospital"),
			path("ViewHealth", views.ViewHealth, name="ViewHealth"),
			path("ViewPatientReport", views.ViewPatientReport, name="ViewPatientReport"),
			path("Prescription", views.Prescription, name="Prescription"),
			path("PrescriptionAction", views.PrescriptionAction, name="PrescriptionAction"),
			path("AddDisease.html", views.AddDisease, name="AddDisease"),
			path("AddDiseaseAction", views.AddDiseaseAction, name="AddDiseaseAction"),
			path("SearchDoctor.html", views.SearchDoctor, name="SearchDoctor"),
			path("SearchDoctorAction", views.SearchDoctorAction, name="SearchDoctorAction"),
]