from flask import request, jsonify
from app import app, db
from models import Homie

@app.route("/api/homies", methods=["GET"])
def get_homies():
    homies = Homie.query.all()
    result = [homie.to_json() for homie in homies]
    return jsonify(result), 200

@app.route("/api/homies", methods=["POST"])
def create_homie():
    try:
        data = request.json

        req_fields = ["name", "role", "desc", "gender"]
        for field in req_fields:
            if field not in data:
                return jsonify({"error":f"missing required field {field}"}), 400

        name = data.get("name")
        role = data.get("role")
        desc = data.get("desc")
        gender = data.get("gender")
        
        if gender == "Male":
            img_url = f"https://avatar.iran.liara.run/public/boy?username={name}"
        elif gender == "Female":
            img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"
        else:
            img_url = None

        new_homie = Homie(name=name, role=role, desc=desc, gender=gender, img_url=img_url)

        db.session.add(new_homie)
        db.session.commit()

        return jsonify({"msg":"new homie created successfully!"}, new_homie.to_json()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":f"{e}"}), 500
    
@app.route("/api/homies/<int:id>", methods=["DELETE"])
def delete_homie(id):
    try:
        homie = Homie.query.get(id)

        if homie is None:
            return jsonify({"error":f"no homie with id {id} found"}), 404
        
        db.session.delete(homie)
        db.session.commit()
        return jsonify({"msg":"homie deleted successfully!"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error":f"{e}"}), 500
    
    
    
@app.route("/api/homies/<int:id>", methods=["PATCH"])
def update_homie(id):
    try:
        homie = Homie.query.get(id)
        if homie is None:
            return jsonify({"error":f"no homie with id {id} found"}), 404

        data = request.json
        # return jsonify({"data":data})
        # return jsonify(data.get("name", homie.name), data.get("role", homie.role), data.get("desc", homie.desc), data.get("gender", homie.gender))
        homie.name = data.get("name", homie.name)
        homie.role = data.get("role", homie.role)
        homie.desc = data.get("desc", homie.desc)
        homie.gender = data.get("gender", homie.gender)

        db.session.commit()
        return jsonify(homie.to_json()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error":f"{e}"}), 500