from flask import Flask, render_template,redirect,request,flash
from flask_debugtoolbar import DebugToolbarExtension
from models import  db, connect_db,Pet
from forms import PetForm
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

toolbar = DebugToolbarExtension(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home_page():
    """get list of all pets"""
    pets = Pet.query.all()
    return render_template('home.html',pets=pets)

@app.route('/add',methods=["GET","POST"])
def add_pet():
    """create a pet"""
    form = PetForm()
   
    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        available = form.available.data
        pet = Pet(name=name,species=species,photo_url=photo_url,age=age,notes=notes,available=available)
        db.session.add(pet)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('add_pet_form.html',form = form)
    

@app.route('/<int:id>',methods=["GET","POST"])
def edit_pet(id):
    """edits pets data, specifically photo_url,notes,available"""
    pet = Pet.query.get_or_404(id)
    form = PetForm(obj=pet)

    if form.validate_on_submit():
        pet.name = form.name.data
        pet.species = form.species.data
        pet.photo_url = form.photo_url.data
        pet.age = form.age.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        
        db.session.commit()
        return redirect('/')
    else:
       return render_template('edit_pet_form.html',form = form,pet=pet)