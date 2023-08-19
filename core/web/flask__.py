from flask import Flask, request, render_template
from custom_modules import customlib
from dataclasses import asdict
from users import Person

app = Flask(__name__)

class UserRegistrationForm:
    def __init__(self):
        self.username = None
        self.phone_number = None
        self.password = None
        self.national_identification_number = None
        self.address = None

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        registration_form = UserRegistrationForm()
        registration_form.username = request.form.get('username')
        registration_form.phone_number = request.form.get('phone_number')
        registration_form.password = request.form.get('password')
        registration_form.national_identification_number = request.form.get('national_id')
        registration_form.address = request.form.get('address')

        user_data = asdict(registration_form)
        # Create a new Person object using the provided data
        new_user = Person(**user_data)

        # Perform user registration logic here, e.g., adding to database
        # ...

        return "User registered successfully!"
    return render_template('registration_form.html')  # You can create an HTML template for the registration form

if __name__ == '__main__':
    app.run(debug=True)
