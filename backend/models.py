from app import db

class Homie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.Text, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    img_url = db.Column(db.String(200), nullable=True)

    # __table_args__ = (CheckConstraint(gender.in_(["male", "female"])),)

    def to_json(self):
        return {
            "id":self.id,
            "name":self.name,
            "role":self.role,
            "desc":self.desc,
            "gender":self.gender,
            "imgUrl":self.img_url
        }
