# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect, render_to_response
from django.views.generic import TemplateView
import requests
import json
from django.utils.timezone import datetime
from config import * 
from models import *

def getLandingPage(request, wat):
  # print "HERE IS MY COOKIE" + request.COOKIES.get('cookie_name')
  # if request.COOKIES.get('cookie_name') != None:
    # return HttpResponseRedirect('http://127.0.0.1:8000/dashboard')
  return render_to_response('index.html')

def login(request):
  url = "https://drchrono.com/o/authorize/?redirect_url=http://127.0.0.1:8000/auth/drchrono/callback&response_type=code&client_id=" + CLIENT_ID
  return HttpResponseRedirect(url)

def logout(request):
  redirect = HttpResponseRedirect('/')
  redirect.delete_cookie('cookie_name')
  return redirect

def handleAuthCode(request):
  code = request.GET.get('code', 'ERROR')
  if (code != 'ERROR'):
    return getTokenFromDrchrono(code)
  return HttpResponseRedirect('/')

def getTokenFromDrchrono(code):
  # if 'error' in get_params:
  #     raise ValueError('Error authorizing application: %s' % get_params[error])
  response = requests.post('https://drchrono.com/o/token/', data={
      'code': code,
      'grant_type': 'authorization_code',
      'redirect_uri': 'http://127.0.0.1:8000/auth/drchrono/handleAuthCode',
      'client_id': CLIENT_ID,
      'client_secret': CLIENT_SECRET,
  })
  response.raise_for_status()
  data = response.json()

  # Save these in your database associated with the user
  access_token = data['access_token']
  refresh_token = data['refresh_token']
  # expires_timestamp = datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=data['expires_in'])

  # get user's id to use for doctor Id when posting patient info
  response = requests.get('https://drchrono.com/api/users/current', headers={
      'Authorization': 'Bearer %s' % access_token,
    })

  response.raise_for_status()
  #doctor ID stored below
  userInfoData= response.json()['doctor']

  redirect = HttpResponseRedirect('http://127.0.0.1:8000/dashboard')
  redirect.set_cookie('cookie_name', access_token, httponly=True)
  redirect.set_cookie('doctorid', userInfoData)
  return redirect

def getToken(request):
  if 'cookie_name' in request.COOKIES:
    value = request.COOKIES['cookie_name']
    return value
  return False

def getPatients(request):
  access_token = getToken(request)

  if getToken(request) == False:
    print "You are not authenticated"
    response = 'null'
    return HttpResponse(response)

  headers = {
    'Authorization': 'Bearer ' + access_token,
  }

  patients = []
  patients_url = 'https://drchrono.com/api/patients'
  while patients_url:
    data = requests.get(patients_url, headers=headers).json()
    patients.extend(data['results'])
    patients_url = data['next']

  return HttpResponse(json.dumps(patients))

def getUserInfo(request):
  access_token = getToken(request)

  if getToken(request) == False:
    print "You are not authenticated"
    response = None
    return HttpResponse(json.dumps(response))

  response = requests.get('https://drchrono.com/api/users/current', headers={
      'Authorization': 'Bearer %s' % access_token,
    })

  response.raise_for_status()
  data = response.json()

  return HttpResponse(json.dumps(data))

def validateCheckInUser(request):
  firstName = request.GET["first_name"]
  lastName = request.GET["last_name"]

  access_token = getToken(request)

  headers = {
    'Authorization': 'Bearer ' + access_token,
  }

  patients_url = 'https://drchrono.com/api/patients?first_name=' + firstName + '&last_name=' + lastName

  patientIdData = requests.get(patients_url, headers=headers)
  status_code = patientIdData.status_code

  if status_code == '500':
    return HttpResponseServerError()

  patientIdData = patientIdData.json()
  appointments_url = 'https://drchrono.com/api/appointments?date=' + str(datetime.today()) + '&patient=' + str(patientIdData['results'][0]['id'])
  patientAppointment = requests.get(appointments_url, headers=headers).json()['results']
  if patientAppointment[0]['status'] == 'Arrived':
    return HttpResponseServerError()

  if len(patientAppointment) == 0:
    print 'no appointment today'
    return HttpResponseServerError()

  patientData = {
    'first_name': firstName,
    'last_name': lastName,
    'patient_id': patientIdData['results'][0]['id'],
    'appointment_id': patientAppointment[0]['id']
  }


  return HttpResponse(json.dumps(patientData))

def updatePatientDemo(request):
  access_token = getToken(request)
  data = {
    'doctor': request.COOKIES['doctorid'], # this is the doctor id
    'id': request.GET['patient_id'], # this is the patient id
    'home_phone': request.GET['home_phone'],
    'address': request.GET['address'],
    'city': request.GET['city'],
    'zip_code': request.GET['zip_code'],
  }

  headers = {
    'Authorization': 'Bearer ' + access_token,
  }

  # print str(request.GET['patient_id'])
  patients_url = 'https://drchrono.com/api/patients/' + str(request.GET['patient_id'])
  r = requests.patch(patients_url, data=data, headers=headers)
  assert r.status_code == 204 # HTTP 204 success, no content

  # Set patient status as Arrived
  data1 = {
    'status': 'Arrived',
  }
  appointment_url = 'https://drchrono.com/api/appointments/' + request.GET['appointment_id']

  updateAppointmentStatus = requests.patch(appointment_url, data=data1, headers=headers)
  assert updateAppointmentStatus.status_code == 204
  # print request.GET['appointment_id']
  # mark time of when patient checked in at the data base
  Appointment(appointment_id=str(request.GET['appointment_id']), time_checkedin=str(datetime.today()), time_ready='false').save()
  # for data in Appointment.objects:
  #   # print data.time_checkedin
  #   # print data.appointment_id, request.GET['appointment_id']
  #   if data.appointment_id == request.GET['appointment_id']:
  # #     print 'here'
  #     print data.time_checkedin

  return HttpResponse(updateAppointmentStatus.status_code)

def getAppointments(request):
  access_token = getToken(request)

  headers = {
    'Authorization': 'Bearer ' + access_token,
  }

  today = datetime.today().isoformat()
  appointments = []
  url = 'https://drchrono.com/api/appointments?date=' + str(today)

  while url:
    data = requests.get(url, headers=headers).json()
    # attach when the user checked in into the results
    for value in Appointment.objects:
      if value.appointment_id == data['results'][0]['id']:
        data['results'][0][u'time_checkedin'] = value.time_checkedin
        data['results'][0][u'time_ready'] = value.time_ready

    appointments.extend(data['results'])
    url = data['next']

  # print appointments
  # loop through appointments and attach a first name and lastname to each appointment's patient ID
  for x in range(0, len(appointments)):
    patienturl = 'https://drchrono.com/api/patients/' + str(appointments[x]['patient'])
    patient_response = requests.get(patienturl, headers=headers).json()
    appointments[x]['first_name'] = patient_response['first_name']
    appointments[x]['last_name'] = patient_response['last_name']

  return HttpResponse(json.dumps(appointments));

def stopTimer(request):
  appointmentid = request.GET['appointment_id']
  # Appointment.objects(appointment_id=appointmentid).update()
  for data in Appointment.objects:
    if data.appointment_id == appointmentid:
      data.update(set__time_ready=str(datetime.today()))

  return HttpResponse(True)