# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect, render_to_response
from django.views.generic import TemplateView
import requests
import json
from django.utils.timezone import datetime
from config import * 
from models import Patient, Appointment

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

  patients = []
  patients_url = 'https://drchrono.com/api/patients?first_name=' + firstName + '&last_name=' + lastName
  print patients_url

  data = requests.get(patients_url, headers=headers)
  status_code = data.status_code

  if status_code == '500':
    HttpResponse(500)

  data = data.json()
  patients.extend(data['results'])

  if patients[0]['first_name'] == firstName and patients[0]['last_name'] == lastName:
    return HttpResponse(json.dumps(patients[0]['id']))

def updatePatientDemo(request):
  print 'first'
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
  today = datetime.today().isoformat()
  print today
  appointment_url = 'https://drchrono.com/api/appointments?date=' + '2016-12-01' + '&patient=' + str(request.GET['patient_id'])
  appointmentRequests = requests.get(appointment_url, headers=headers).json()
  appointmentId = appointmentRequests['results'][0]['id']
  appointmentStatus_url = 'https://drchrono.com/api/appointments/' + str(appointmentId)
  updateAppointmentStatus = requests.patch(appointmentStatus_url, data=data1, headers=headers)
  assert updateAppointmentStatus.status_code == 204

  # mark time of when patient checked in at the data base


  return HttpResponse(r.status_code)

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
    appointments.extend(data['results'])
    url = data['next']

  print appointments
  # loop through appointments and attach a first name and lastname to each appointment's patient ID
  for x in range(0, len(appointments)):
    patienturl = 'https://drchrono.com/api/patients/' + str(appointments[x]['patient'])
    patient_response = requests.get(patienturl, headers=headers).json()
    appointments[x]['first_name'] = patient_response['first_name']
    appointments[x]['last_name'] = patient_response['last_name']


  return HttpResponse(json.dumps(appointments));