from app import app, dao
from flask import redirect, render_template, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField, validators


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index_view():
    return render_template('index.html', title='Home')


@app.route('/bands', methods=['GET'])
def bands_view():
    raw_bands = dao.query_by_type('band')
    bands = []
    
    for b in raw_bands:
        band = dict(b)
        band['name'] = band['name'].split()
        band['name'] = 'Band ' + str(int(band['name'][1]) + 1)
        band['cohort'] = band['cohort']
        band['Singer'] = band['Singer'].split(' || ')
        band['Singer'] = band['Singer'][2]
        band['Guitarist'] = band['Guitarist'].split(' || ')
        band['Guitarist'] = band['Guitarist'][2]
        band['Drummer'] = band['Drummer'].split(' || ')
        band['Drummer'] = band['Drummer'][2]
        band['Bassist'] = band['Bassist'].split(' || ')
        band['Bassist'] = band['Bassist'][2]
        band['Keyboardist'] = band['Keyboardist'].split(' || ')
        band['Keyboardist'] = band['Keyboardist'][2]
        band['Instrumentalist'] = band['Instrumentalist'].split(' || ')
        band['Instrumentalist'] = band['Instrumentalist'][2]
        bands.append(band)

    return render_template('bands.html', title='Bands', bands=bands)


@app.route('/dorms', methods=['GET'])
def dorms_view():
    raw_dorms = dao.query_by_type('dorm')
    dorms = []

    for d in raw_dorms:
        dorm = dict(d)
        dorm['name'] = dorm['name'].split()
        dorm['name'] = 'Dorm ' + str(int(dorm['name'][1]) + 1)
        if dorm['gender'] == 'male':
            dorm['gender'] == 'Male'
        else:
            dorm['gender'] == 'Female'
        for i, m in enumerate(dorm['members']):
            member = dorm['members'][i].split()
            member = member[1] + ' ' + member[2]
            dorm['members'][i] = member
        dorms.append(dorm)
    
    return render_template('dorms.html', title='Dorms', dorms=dorms)


class NewMemberForm(FlaskForm):
    first_name = StringField('First name', [validators.InputRequired()])
    last_name = StringField('Last name', [validators.InputRequired()])
    gender = SelectField('Gender', [validators.InputRequired],
                         choices=[
                             ('male', 'Male'),
                             ('female', 'Female')
                         ])
    age = IntegerField('Age', [validators.Length(min=13, max=18), validators.InputRequired()])
    street = StringField('Street', [validators.InputRequired()])
    city = StringField('City', [validators.InputRequired()])
    state = StringField('State', [validators.InputRequired()])
    zip_code = IntegerField('ZIP Code', [validators.Length(min=00000, max=99999), validators.InputRequired()])
    talent = SelectField('Talent', [validators.InputRequired()],
                         choices=[
                             ('singer', 'Singer'),
                             ('guitarist', 'Guitarist'),
                             ('drummer', 'Drummer'),
                             ('bassist', 'Bassist'),
                             ('keyboardist', 'Keyboardist'),
                             ('instrumentalist', 'Instrumentalist')
                         ])
    submit = SubmitField('Submit')


@app.route('/members', methods=['GET', 'POST'])
def members():
    members_list = dao.query_by_type('member')

    form = NewMemberForm()
    if form.validate_on_submit():
        # Parse incoming form data
        first_name = form.first_name.data
        last_name = form.last_name.data
        gender = form.gender.data
        age = form.age.data
        street = form.street.data
        city = form.city.data
        state = form.state.data
        zip_code = form.zip_code.data
        talent = form.talent.data

        # Clear form for new submission
        form.first_name.data = ''
        form.last_name.data = ''
        form.gender.data = ''
        form.age.data = ''
        form.street.data = ''
        form.city.data = ''
        form.state.data = ''
        form.zip_code.data = ''
        form.talent.data = ''

    return render_template('members.html', title='Members', members=members_list, form=form)


@app.route('/members/add', methods=['GET'])
def add_member():
    states = [
        "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", 
        "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
        "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
        "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
        "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY" 
    ]
    
    return render_template('add-member.html', title='Add Member', states=states)


@app.route('/members/submit', methods=['POST'])
def submit_member():
    dao.insert_member(request.form)
    
    return redirect('/members')


@app.route('/members/delete', methods=['POST'])
def delete_member():
    member_id = request.form.getlist('memberId')[0]
    dao.remove_member_by_id(member_id)

    return redirect('/members')


@app.route('/members/checkout', methods=['POST'])
def checkout_member():
    member_id = request.form.getlist('memberId')[0]
    query = dict({"checkin": False})
    dao.update_member_by_id(query, member_id)

    return redirect('/members')


@app.route('/members/checkin', methods=['POST'])
def checkin_member():
    member_id = request.form.getlist('memberId')[0]
    query = dict({"checkin": True})
    dao.update_member_by_id(query, member_id)

    return redirect('/members')


@app.route('/members/edit', methods=['POST'])
def edit_member():
    member_id = request.form.getlist('memberId')[0]
    member = dao.query_member_by_id(member_id)
    states = [
        "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", 
        "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
        "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
        "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
        "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY" 
    ]

    return render_template('edit-member.html', title='Edit Member', member=member[0], states=states)


@app.route('/members/update', methods=['POST'])
def update_member():
    member_id = request.form.getlist('memberId')[0]
    member_gender = request.form.getlist('gender')[0]
    member_age = request.form.getlist('age')[0]
    member_street = request.form.getlist('street')[0]
    member_city = request.form.getlist('city')[0]
    member_state = request.form.getlist('state')[0]
    member_zipCode = request.form.getlist('zipCode')[0]
    member_talent = request.form.getlist('talent')[0]
    member_status = request.form.getlist('status')[0]
    #member_checkin = request.form.getlist('checkin')[0]
    #member_forms = request.form.getlist('forms')[0]
    #member_payment = request.form.getlist('payment')[0]
    member_comments = request.form.getlist('comments')[0]
    form_body = ({
        'gender': member_gender, 
        'age': member_age, 
        'street': member_street, 
        'city': member_city, 
        'state': member_state, 
        'zipCode': member_zipCode, 
        'talent': member_talent, 
        'status': member_status,
        #'checkin': member_checkin,
        #'forms': member_forms,
        #'payment': member_payment,
        'comments': member_comments
    })
    dao.update_member_by_id(form_body, member_id)

    return redirect('/members')


@app.route('/email/send', methods=['POST'])
def send_email():
    member_id = request.form.getlist('memberId')[0]
    email_type = request.form.getlist('type')[0]
    member = dao.query_member_by_id(member_id)

    return render_template('email.html', title="Email Template", type=email_type, member=member[0])


# Custom error handling
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
