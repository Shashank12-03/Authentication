from django.shortcuts import render
import mysql.connector as sql
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

def PatientSignup(request):
    first_name = ''
    last_name = ''
    profile_picture = 'default_profile_picture.jpg'
    user_name = ''
    email = ''
    password = ''
    address = ''
    city = ''
    state = ''
    pincode = ''
    error_message = None
    success_message = None

    if request.method == "POST":
        # Extracting form data
        data = request.POST
        first_name = data.get("firstName", "")
        last_name = data.get("lastName", "")
        profile_picture = data.get("profilePicture", "default_profile_picture.jpg")
        user_name = data.get("username", "")
        email = data.get("email", "")
        password = data.get("password", "")
        confirm_password = data.get("confirmPassword", "")
        address = data.get("addressLine1", "")
        city = data.get("city", "")
        state = data.get("state", "")
        pincode = data.get("pincode", "")
        Data={ 'first_name': first_name,
                'last_name': last_name,
                'user_name': user_name,
                'email': email,
                'address': address,
                'city': city,
                'state': state,
                'pincode': pincode,} 
        if password != confirm_password:
            error_message = "Password and Confirm Password do not match. Please try again."
        else:
            # Hashing the password
            hashed_password = make_password(password)

            try:
                # Database connection and insertion
                conn = sql.connect(host="localhost", user="root", passwd="Shashank@12", database='LoginOut')
                cursor_obj = conn.cursor()

                statement = "INSERT INTO patient VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                    first_name, profile_picture, user_name, email, hashed_password, address, city, state, pincode, last_name)

                cursor_obj.execute(statement)
                conn.commit()

                success_message = "Signup successful!" 
                return render(request,'Patient.html',{'Data':Data})

            except Exception as e:
                error_message = f"Error during signup: {e}"
            finally:
                cursor_obj.close()
                conn.close()

    return render(request, 'PatientSignup.html', {'error_message': error_message, 'success_message': success_message})

def PatientLogin(request):
    user_name = ''
    password = ''
    message = ''

    if request.method == "POST":
        conn = sql.connect(host="localhost", user='root', passwd="Shashank@12", database="LoginOut")
        cursor_obj = conn.cursor()
        data = request.POST

        for key, value in data.items():
            if key == "username":
                user_name = value
            if key == "password":
                password = value

        statement = "SELECT * FROM patient WHERE username=%s"
        cursor_obj.execute(statement, (user_name,))

        # Fetch the user from the database
        user_data = cursor_obj.fetchone()

        if user_data is None or not check_password(password, user_data[4]):
            message = "Username or Password is not correct"
            return render(request, 'PatientLogin.html', {'message': message})
        else:
            user_info = {
            'first_name': user_data[0],
            'last_name': user_data[9],
            'user_name': user_data[2],
            'email': user_data[3],
            'address': user_data[5],
            'city': user_data[6],
            'state': user_data[7],
            'pincode': user_data[8],
        }
            return render(request, 'Patient.html',{'Data': user_info})

    return render(request, 'PatientLogin.html')

def home_view(request):
    return render(request, 'home.html')