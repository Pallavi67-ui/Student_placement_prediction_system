from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import random

app = Flask(__name__)
app.secret_key = "placement_prediction"


# ================= MYSQL CONNECTION =================

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="placement_prediction"
)

cursor = db.cursor()



# ================= HOME =================

@app.route('/')
def home():
    return render_template('index.html')



# ================= ABOUT =================

@app.route('/about')
def about():
    return render_template('about.html')



# ================= REGISTER =================

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == "POST":

        fullname = request.form['fullname']
        register_number = request.form['register_number']
        department = request.form['department']
        email = request.form['email']
        password = request.form['password']


        query = """
        INSERT INTO students
        (fullname, register_number, department, email, password)
        VALUES (%s,%s,%s,%s,%s)
        """


        values = (
            fullname,
            register_number,
            department,
            email,
            password
        )


        cursor.execute(query, values)
        db.commit()


        return redirect(url_for('login'))


    return render_template('register.html')




# ================= LOGIN =================

@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == "POST":

        email = request.form['email']
        password = request.form['password']


        query = """
        SELECT * FROM students
        WHERE email=%s AND password=%s
        """


        cursor.execute(query,(email,password))

        student = cursor.fetchone()



        if student:

            session["student_id"] = student[0]
            session["email"] = email

            return redirect(url_for('dashboard'))


        else:

            return "Invalid Email or Password"



    return render_template('login.html')




# ================= DASHBOARD =================

@app.route('/dashboard')
def dashboard():

    return render_template('dashboard.html')




# ================= ACADEMICS =================

@app.route('/academics', methods=['GET','POST'])
def academics():


    if request.method == "POST":


        student_id = session.get("student_id")


        cgpa = request.form['cgpa']
        backlogs = request.form['backlogs']
        internship = request.form['internship']
        projects = request.form['projects']
        certifications = request.form['certifications']
        aptitude = request.form['aptitude']
        skills = request.form['skills']



        query = """

        INSERT INTO academics

        (
        student_id,
        cgpa,
        backlogs,
        internship,
        projects,
        certifications,
        aptitude,
        skills
        )

        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)

        """



        values = (

            student_id,
            cgpa,
            backlogs,
            internship,
            projects,
            certifications,
            aptitude,
            skills

        )


        cursor.execute(query,values)

        db.commit()



        session["cgpa"] = cgpa
        session["backlogs"] = backlogs
        session["internship"] = internship
        session["projects"] = projects
        session["certifications"] = certifications
        session["aptitude"] = aptitude
        session["skills"] = skills



        return redirect(url_for('communication'))



    return render_template('academics.html')
    # ================= COMMUNICATION ASSESSMENT =================

@app.route('/communication', methods=['GET','POST'])
def communication():


    # ---------- LOAD RANDOM QUESTIONS ----------
    if request.method == "GET":


        categories = [

            "Grammar",
            "Vocabulary",
            "Reading Comprehension",
            "Professional Communication",
            "Situational Communication"

        ]


        selected_questions = []


        # Select 4 questions from each category

        for category in categories:


            query = """

            SELECT *
            FROM communication_questions
            WHERE category=%s

            """


            cursor.execute(query,(category,))


            questions = cursor.fetchall()


            random_questions = random.sample(
                questions,
                4
            )


            selected_questions.extend(
                random_questions
            )



        # Shuffle final 20 questions

        random.shuffle(selected_questions)



        # Store questions in session

        session["questions"] = selected_questions



        return render_template(
            "communication-assessment.html",
            questions=selected_questions
        )




    # ---------- CHECK ANSWERS ----------

    if request.method == "POST":


        questions = session.get(
            "questions"
        )


        correct_answers = 0



        for question in questions:


            question_id = question[0]


            selected_answer = request.form.get(
                f"q{question_id}"
            )



            correct_option = question[7]



            if selected_answer == correct_option:

                correct_answers += 1




        # Calculate percentage

        communication_score = round(
            (correct_answers / 20) * 100,
            2
        )



        student_id = session.get(
            "student_id"
        )



        query = """

        INSERT INTO communication
        (student_id,score)

        VALUES(%s,%s)

        """



        cursor.execute(

            query,

            (
                student_id,
                communication_score
            )

        )


        db.commit()



        session["communication_score"] = communication_score



        return redirect(
            url_for('prediction')
        )




# ================= PREDICTION =================

@app.route('/prediction')
def prediction():


    cgpa = session.get("cgpa",0)
    backlogs = session.get("backlogs",0)
    internship = session.get("internship","No")
    projects = session.get("projects",0)
    certifications = session.get("certifications",0)
    aptitude = session.get("aptitude",0)
    skills = session.get("skills","")



    communication_score = session.get(
        "communication_score",
        0
    )



    # Temporary prediction
    # Replace with ML model later

    prediction = 85


    placement_status = "High Placement Readiness"



    suggestions = [

        "Continue improving communication skills.",
        "Develop more real-world projects.",
        "Participate in coding competitions.",
        "Maintain consistent academic performance."

    ]



    return render_template(

        "prediction-result.html",

        communication_score=communication_score,

        cgpa=cgpa,

        backlogs=backlogs,

        internship=internship,

        projects=projects,

        certifications=certifications,

        aptitude=aptitude,

        skills=skills,

        prediction=prediction,

        placement_status=placement_status,

        suggestions=suggestions

    )





# ================= LOGOUT =================

@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('login'))




# ================= RUN =================

if __name__ == "__main__":

    app.run(debug=True)