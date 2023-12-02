from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Bio(db.Model):
    __tablename__ = 'bios'
    ID = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(2), nullable=False)

class ProfilePromptsResponses(db.Model):
    __tablename__ = 'experiment_profile_prompts_responses'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    ID_Prompt = db.Column(db.Integer, db.ForeignKey('prompts.ID'), nullable=False)
    ID_Response = db.Column(db.Integer, db.ForeignKey('responses.ID'), nullable=False)
    ID_Profile = db.Column(db.Integer, db.ForeignKey('experiment_profiles.ID'), nullable=False)
    profile = db.relationship("Profile", backref=db.backref('prompts_and_responses'))
    # prompt = db.relationship("Prompts", backref=db.backref('prompt'))
    # response = db.relationship("Responses", backref=db.backref('response'))

# profile_prompts_responses = db.Table('experiment_profile_prompts_responses', db.Model.metadata,
#     db.Column('ID_Profile', db.Integer, db.ForeignKey('experiment_profiles.ID')),
#     db.Column('ID_Prompt', db.Integer, db.ForeignKey('prompts.ID')),
#     db.Column('ID_Response', db.Integer, db.ForeignKey('responses.ID'))
# )


class Profile(db.Model):
    __tablename__ = 'experiment_profiles'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    ID_Participant = db.Column(db.Integer, db.ForeignKey('participants.ID'), nullable=False)
    ID_Bio = db.Column(db.Integer, db.ForeignKey('bios.ID'), nullable=False)
    ID_Name = db.Column(db.Integer, db.ForeignKey('names.ID'), nullable=False)
    Age = db.Column(db.Numeric, nullable=False)
    Picture = db.Column(db.Text, nullable=False)
    Source = db.Column(db.Text, nullable=False)
    Authenticity_score = db.Column(db.Numeric)
    Attractiveness_score = db.Column(db.Numeric)
    Trustworthiness_score = db.Column(db.Numeric)
    participant = db.relationship("Participant", backref=db.backref('profiles'))

    #prompts =  db.relationship("Prompt", back_populates='profile')
    #response = db.relationship("Response", back_populates='profile')

class Participant(db.Model):
    __tablename__ = 'participants'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Age = db.Column(db.Integer)
    Gender = db.Column(db.String(1))
    Preferred_gender = db.Column(db.String(1))
    Education_level = db.Column(db.String(100))
    Education_field = db.Column(db.String(100))
    Relationship_status = db.Column(db.String(1))
    Duration_use = db.Column(db.Text)
    Frequency_use = db.Column(db.Text)
    Goals = db.Column(db.Text)
    Most_successful_experience = db.Column(db.Text)
    Finished_at = db.Column(db.DateTime)



class Name(db.Model):
    __tablename__ = 'names'
    ID = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    gender = db.Column(db.Text, nullable=False)

class Prompt(db.Model):
    __tablename__ = 'prompts'
    ID = db.Column(db.Integer, primary_key=True, nullable=False)
    text = db.Column(db.Text, nullable=False)

class Response(db.Model):
    __tablename__ = 'responses'
    ID = db.Column(db.Integer, primary_key=True, nullable=False)
    ID_Prompt = db.Column(db.Integer, db.ForeignKey('prompts.ID'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(2), nullable=False)


