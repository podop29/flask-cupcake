"""Flask app for Cupcakes"""
from crypt import methods
from email import message
from flask import Flask, jsonify, request, render_template, flash, redirect
from models import connect_db, Cupcake,db
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "OOooOOOoOOOoo000"

connect_db(app)



"Serialize Funcs"

def serialize_cupcake(cupcake):

    return{
        "id": cupcake.id,
        "flavor":cupcake.flavor,
        "size":cupcake.size,
        "rating":cupcake.rating,
        "image":cupcake.image
    }

"API EndPoints"

@app.route('/api/cupcakes', methods=["GET"])
def get_cupcakes():
    cupcake = Cupcake.query.all()
    serialized = [serialize_cupcake(c) for c in cupcake]

    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes/<int:id>', methods=["GET"])
def get_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcakes=serialized)


@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Add cupcake, and return data about new cupcake.

    Returns JSON like:
        {cupcake: [{id, flavor, rating, size, image}]}
    """

    data = request.json

    cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None)

    db.session.add(cupcake)
    db.session.commit()

    # POST requests should return HTTP status of 201 CREATED
    return (jsonify(cupcake=cupcake.to_dict()), 201)


@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cake(id):
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size=request.json.get("size", cupcake.size  ) 
    cupcake.rating=request.json.get("rating", cupcake.rating)
    db.session.commit()
    return jsonify(cake=serialize_cupcake(cupcake))


@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_todo(id):
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="DELETE")




'Render Template'
@app.route("/", methods=["GET"])
def show_home():
    return render_template("home.html")




    