from flask import Flask, render_template, request, session, redirect, url_for
import pandas as pd
import random
from dbmodel import db, Name, Bio, Prompt, Response, Profile, ProfilePromptsResponses, Participant

app = Flask(__name__)
import os

# Set the configuration values in your Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv("SECRET_KEY")
app.config['N_PROFILES'] = int(os.getenv("N_PROFILES"))
app.config['PROMPTS_MAX_OCCURENCE'] = int(os.getenv("PROMPTS_MAX_OCCURENCE"))

db = db
db.init_app(app)
        
def build_profiles_set(participant):
    connection = db.session.connection()
    names = pd.read_sql_table('names',connection, index_col='ID')
    bios = pd.read_sql_table('bios', connection, index_col='ID')
    prompts = pd.read_sql_table('prompts', connection, index_col='ID')
    responses = pd.read_sql_table('responses', connection, index_col='ID')
    random.seed(participant.ID) #setting random seed to randomize pictures based on participant.ID
    pictures = random.sample(range(0, 110), app.config['N_PROFILES']) if participant.Preferred_gender == 'F' else random.sample(range(111, 220), app.config['N_PROFILES']) #selecting pictures sample based on preferred_gender
    bios_randomized = {"H" : bios[bios['source']=='H'].sample(n=app.config['N_PROFILES'] // 2,replace=False,random_state=participant.ID*74),"AI" : bios[bios['source']=='AI'].sample(n=app.config['N_PROFILES']//2,replace=False,random_state=participant.ID*23)} #selecting random subsets of bios for H and AI conditions (size N/2 each)
    h_ai_distribution = ['H','AI'] * (app.config['N_PROFILES'] // 2) 
    random.Random(participant.ID).shuffle(h_ai_distribution) #setting the order for profiles to show depending on condition
    condition_index = {'H':0, 'AI':0} #counter
    prompts_occurence = {} #storage for prompts max_occurence control
    for condition in h_ai_distribution: #for each of the profiles
        bio = int(bios_randomized[condition].iloc[condition_index[condition]].name) #select random bio from the preselected sample
        name = int(names[names['gender']==participant.Preferred_gender].sample(n=1,random_state=participant.ID*1000+sum(condition_index.values())).iloc[0].name) #select random name
        prompts_per_profile = prompts.sample(n=3, replace=False, random_state=participant.ID*1000+sum(condition_index.values())) #select random set of 3 prompts
        picture = str(pictures[sum(condition_index.values())]) + '.jpg' #setting path to the picture file
        if len(picture) == 6: #fix naming
            picture = '0' + picture
        elif len(picture) == 5: #fix naming
            picture = '00' + picture
        profile_entry = Profile( #create profile instance for the db
                ID_Bio=bio,
                ID_Name=name,
                Age=random.randrange(20, 30), #randomly select age between 20 and 30
                Picture=picture,
                Source=condition)
        prompts_count = 0
        for p_id,_ in prompts_per_profile.iterrows(): #selecting prompts and responses. For each of the 3 prompts:
            response_random_state=participant.ID*10000+sum(condition_index.values()) + prompts_count #setting random state for response selection
            response_per_prompt = responses[(responses['source'] == condition) & (responses['ID_Prompt'] == p_id)].sample(n=1, replace=False, random_state=participant.ID+1000+len(condition_index)+response_random_state) #choosing response that corresponds to the current prompt and matches the condition
            response_random_state = response_random_state + 1 #changing random_state to get next random response for the nexxt prompt
            responses.drop(response_per_prompt.iloc[0].name, inplace=True) #remove used response from the pool
            profile_prompt_response_entry = ProfilePromptsResponses(ID_Prompt=p_id,ID_Response=int(response_per_prompt.iloc[0].name)) #binding the prompt and the response
            profile_entry.prompts_and_responses.append(profile_prompt_response_entry) #binding the prompt and the response to the current profile
            try:
                prompts_occurence[p_id] = prompts_occurence[p_id] + 1 #count actual occurence of the prompt
                if prompts_occurence[p_id] <= app.config['PROMPTS_MAX_OCCURENCE']: #if exceeds max_occurence
                    prompts.drop(p_id,inplace=True) #then remove from the pool
            except KeyError: #if it is the first occurence of the prompt
                prompts_occurence[p_id] = 1 #then add it to the occurence control dictionary
            prompts_count = prompts_count + 1 #increasing prompts_count to process the next_prompt
        participant.profiles.append(profile_entry)
        db.session.add(profile_entry) #add profile instance to the db
        condition_index[condition] = condition_index[condition] + 1 #increasing profiles counter (based on control condition)




@app.route('/', methods=['GET', 'POST'])
def index():
        return render_template('index.html')

    # Render the index template (this will be executed for both GET and POST requests)

@app.route('/create_participant', methods=['POST'])
def create_participant():
    try:
        data = request.form
        with app.app_context():
            participant = Participant( #create participant instance for the db
                        Age = int(data['age']),
                        Gender = data['gender'],
                        Preferred_gender = data['preferred_gender'],
                        Education_level = data['education_level'],
                        Education_field = data['education_field'],
                        Relationship_status = data['relationship_status'],
                        Duration_use = data['duration'],
                        Frequency_use = data['frequency'],
                        Goals = data['goals'],
                        Most_successful_experience = data['online_dating_experience']
            )
            db.session.add(participant)
            db.session.commit()
            build_profiles_set(participant)
            db.session.commit()
            session['participant_id'] = participant.ID
            session['current_n'] = 0
    except Exception as e:
        db.session.rollback()
        print(e.args)
    return redirect(url_for('profile'), code=307)
    return 'profiles set built successfully'

@app.route('/set_test_session',methods=['POST'])
def set_test_session():
    session['participant_id'] = int(request.form['participant_id'])
    session['current_n'] = 0
    return redirect(url_for('profile'), code=307)



#@app.route('/get_profile', methods=['POST'])
def get_profile():
    with app.app_context():
        profile = db.session.get(Participant,session['participant_id']).profiles[session['current_n']]
        if profile == None:
            return None
        picture = profile.Picture
        name = db.session.get(Name,profile.ID_Name).name
        bio = db.session.get(Bio,profile.ID_Bio).text
        age = str(int(profile.Age))
        prompts_and_responses = profile.prompts_and_responses
        prs = []
        for pr in prompts_and_responses:
            p = db.session.get(Prompt,pr.ID_Prompt).text
            r = db.session.get(Response,pr.ID_Response).text
            prs.append((p,r))
        attractiveness = 4 if profile.Attractiveness_score is None else int(profile.Attractiveness_score)
        trustworthiness = 4 if profile.Trustworthiness_score is None else int(profile.Trustworthiness_score)
        authenticity = 4 if profile.Authenticity_score is None else int(profile.Authenticity_score)

        return {'picture':picture, 
                'current_n':session['current_n'], 
                'name':name, 'bio':bio, 'age':age, 
                'prompts_and_responses':prs, 
                'num_profiles':app.config['N_PROFILES'],
                'attractiveness':attractiveness,
                'trustworthiness':trustworthiness,
                'authenticity':authenticity}

@app.route('/profile', methods=['POST'])
def profile():
    return render_template('profile.html', data=get_profile())
    # return render_template('profile.html', current_profile=profile, current_n=current_n, profile_name=name.name, bio=bio.text, age=age, prompts_and_responses=prs, num_profiles=N_profiles)
    # return "Profile not found!"

@app.route('/submit_ratings', methods=['POST'])
def submit_ratings():
    with app.app_context():
        profile = db.session.query(Profile).filter_by(ID_Participant=session['participant_id']).limit(1).offset(session['current_n']).first()
        profile.Attractiveness_score = int(request.form['attractiveness'])
        profile.Trustworthiness_score = int(request.form['trustworthiness'])
        profile.Authenticity_score = int(request.form['authenticity'])
        db.session.commit()
    # Do something with the ratings (store in a database, perform analysis, etc.)
    if request.form['to'] == 'Next':
        if session['current_n'] < app.config['N_PROFILES'] - 1:
            session['current_n'] = session['current_n'] + 1
            return redirect(url_for('profile'), code=307) 
        else:
            return render_template('end.html')
    elif request.form['to'] == 'Previous':
        if session['current_n'] > 0:
            session['current_n'] = session['current_n'] - 1
            return redirect(url_for('profile'), code=307)
        else:
            return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)