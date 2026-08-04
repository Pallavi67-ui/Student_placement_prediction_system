from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import random
import joblib
import pandas as pd


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



# ================= LOAD ML MODEL =================

model = joblib.load("placement_model_old.pkl")





# ================= HOME =================


@app.route('/')

def home():

    return render_template('index.html')





# ================= ABOUT =================


@app.route('/about')

def about():

    return render_template('about.html')







# ================= REGISTER =================


@app.route('/register', methods=['GET','POST'])

def register():


    if request.method == "POST":


        fullname = request.form['fullname']

        register_number = request.form['register_number']

        department = request.form['department']

        email = request.form['email']

        password = request.form['password']



        query = """

        INSERT INTO students

        (
        fullname,
        register_number,
        department,
        email,
        password
        )

        VALUES(%s,%s,%s,%s,%s)

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



        return redirect(
            url_for('login')
        )



    return render_template('register.html')







# ================= LOGIN =================


@app.route('/login', methods=['GET','POST'])

def login():


    if request.method == "POST":


        email = request.form['email']

        password = request.form['password']



        query = """

        SELECT *

        FROM students

        WHERE email=%s AND password=%s

        """



        cursor.execute(

            query,

            (email,password)

        )


        student = cursor.fetchone()



        if student:


            session["student_id"] = student[0]

            session["email"] = email
            session["department"] = student[3]

            return redirect(

                url_for('dashboard')

            )


        else:


            return "Invalid Email or Password"



    return render_template('login.html')
# ================= ADMIN LOGIN =================

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():

    if request.method == "POST":

        username = request.form['username']
        password = request.form['password']

        query = """
        SELECT *
        FROM admin
        WHERE username=%s AND password=%s
        """

        cursor.execute(query, (username, password))

        admin = cursor.fetchone()

        if admin:

            session["admin_id"] = admin[0]
            session["admin_username"] = admin[1]

            return redirect(url_for('admin_dashboard'))

        else:

            return "Invalid Admin Username or Password"

    return render_template("admin_login.html")   
# ================= ADMIN DASHBOARD =================
@app.route('/admin_dashboard')
def admin_dashboard():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    # Total Students
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    # Total Predictions
    cursor.execute("SELECT COUNT(*) FROM prediction_results")
    total_predictions = cursor.fetchone()[0]

    # High Placement Readiness
    cursor.execute("""
        SELECT COUNT(*)
        FROM prediction_results
        WHERE placement_status='High Placement Readiness'
    """)
    high_count = cursor.fetchone()[0]

    # Medium Placement Readiness
    cursor.execute("""
        SELECT COUNT(*)
        FROM prediction_results
        WHERE placement_status='Medium Placement Readiness'
    """)
    medium_count = cursor.fetchone()[0]

    # Low Placement Readiness
    cursor.execute("""
        SELECT COUNT(*)
        FROM prediction_results
        WHERE placement_status='Low Placement Readiness'
    """)
    low_count = cursor.fetchone()[0]

    return render_template(
        "admin_dashboard.html",
        total_students=total_students,
        total_predictions=total_predictions,
        high_count=high_count,
        medium_count=medium_count,
        low_count=low_count
    )
# ================= ADMIN - VIEW STUDENTS =================

@app.route('/admin_students')
def admin_students():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    cursor.execute("""
        SELECT student_id,
               fullname,
               register_number,
               department,
               email
        FROM students
        ORDER BY student_id DESC
    """)

    students = cursor.fetchall()

    return render_template(
        "admin_students.html",
        students=students
    )     
# ================= ADMIN - VIEW PREDICTION RESULTS =================

@app.route('/admin_predictions')
def admin_predictions():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))


    cursor.execute("""
        SELECT 
            prediction_results.prediction_id,
            students.fullname,
            students.register_number,
            students.department,
            prediction_results.prediction_score,
            prediction_results.placement_status,
            prediction_results.prediction_date

        FROM prediction_results

        JOIN students

        ON prediction_results.student_id = students.student_id

        ORDER BY prediction_results.prediction_date DESC

    """)


    predictions = cursor.fetchall()


    return render_template(
        "admin_predictions.html",
        predictions=predictions
    )    
# ================= DASHBOARD =================


@app.route('/dashboard')

def dashboard():

    return render_template('dashboard.html')







# ================= ACADEMICS =================


@app.route('/academics', methods=['GET','POST'])

def academics():


    if request.method == "POST":


        student_id = session.get(
            "student_id"
        )


        cgpa = request.form['cgpa']

        prev_sem = request.form['prev_sem']

        backlogs = request.form['backlogs']

        internship = request.form['internship']

        projects = request.form['projects']

        extra_curr = request.form['extra_curr']

        certifications = request.form['certifications']

        aptitude = request.form['aptitude']

        skills = request.form['skills']

         # Check if academic details already exist

        cursor.execute(
            """
            SELECT academic_id
            FROM academics
            WHERE student_id=%s
            """,
            (student_id,)
        )

        existing_record = cursor.fetchone()


        if existing_record:

            cursor.execute(
                """
                UPDATE academics
                SET
                    cgpa=%s,
                    prev_sem=%s,
                    backlogs=%s,
                    internship=%s,
                    projects=%s,
                    extra_curr=%s,
                    certifications=%s,
                    aptitude=%s,
                    skills=%s
                WHERE student_id=%s
                """,
                (
                    cgpa,
                    prev_sem,
                    backlogs,
                    internship,
                    projects,
                    extra_curr,
                    certifications,
                    aptitude,
                    skills,
                    student_id
                )
            )

        else:

            cursor.execute(
                """
                INSERT INTO academics
                (
                    student_id,
                    cgpa,
                    prev_sem,
                    backlogs,
                    internship,
                    projects,
                    extra_curr,
                    certifications,
                    aptitude,
                    skills
                )

                VALUES
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    student_id,
                    cgpa,
                    prev_sem,
                    backlogs,
                    internship,
                    projects,
                    extra_curr,
                    certifications,
                    aptitude,
                    skills
                )
            )

        db.commit() 



        # Store data in session

        session["cgpa"] = cgpa

        session["prev_sem"] = prev_sem

        session["backlogs"] = backlogs

        session["internship"] = internship

        session["projects"] = projects

        session["extra_curr"] = extra_curr

        session["certifications"] = certifications

        session["aptitude"] = aptitude

        session["skills"] = skills





        return redirect(

            url_for('communication')

        )

    student_id = session.get("student_id")

    cursor.execute(
    """
     SELECT
        cgpa,
        prev_sem,
        backlogs,
        internship,
        projects,
        extra_curr,
        certifications,
        aptitude,
        skills
     FROM academics
     WHERE student_id=%s
     """,
    (student_id,)
)

    academic = cursor.fetchone()

    return render_template(
      "academics.html",
      academic=academic
)




# ================= COMMUNICATION ASSESSMENT =================


@app.route('/communication', methods=['GET','POST'])

def communication():



    if request.method == "GET":


        categories = [

            "Grammar",

            "Vocabulary",

            "Reading Comprehension",

            "Professional Communication",

            "Situational Communication"

        ]



        selected_questions = []



        for category in categories:



            query = """

            SELECT *

            FROM communication_questions

            WHERE category=%s

            """



            cursor.execute(

                query,

                (category,)

            )


            questions = cursor.fetchall()



            random_questions = random.sample(

                questions,

                4

            )


            selected_questions.extend(

                random_questions

            )



        random.shuffle(

            selected_questions

        )



        session["questions"] = selected_questions




        return render_template(

            "communication-assessment.html",

            questions=selected_questions

        )







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





        communication_score = round(

            (correct_answers / 20) * 100,

            2

        )
        communication_ml = round((communication_score / 100) * 10)




        student_id = session.get(
            "student_id"
        )




        query = """

        INSERT INTO communication

        (
        student_id,
        score
        )

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
        # ================= TECHNICAL SKILL SCORE =================


def calculate_skill_score(skills):


    skills = skills.lower()


    score = 0



    skill_weights = {


        "python":2,

        "java":2,

        "c++":2,

        "javascript":2,

        "sql":1,

        "mysql":1,

        "html":1,

        "css":1,

        "flask":2,

        "machine learning":3


    }



    for skill, weight in skill_weights.items():


        if skill in skills:

            score += weight



    return score
# ================= PREDICTION =================

@app.route('/prediction')
def prediction():

    cgpa = float(session.get("cgpa", 0))
    prev_sem = float(session.get("prev_sem", 0))
    backlogs = int(session.get("backlogs", 0))
    internship = session.get("internship", "No")
    projects = int(session.get("projects", 0))
    extra_curr = int(session.get("extra_curr", 0))
    certifications = int(session.get("certifications", 0))
    aptitude = int(session.get("aptitude", 0))
    skills = session.get("skills", "")

    communication_score = float(session.get("communication_score", 0))
    communication_ml = round((communication_score / 100) * 10)

    # Convert internship to ML value
    internship_value = 1 if internship == "Yes" else 0

    # ================= ML INPUT =================

    input_data = pd.DataFrame(
        [[
            prev_sem,
            cgpa,
            internship_value,
            extra_curr,
            communication_ml,
            projects
        ]],
        columns=[
            "Prev_Sem_Result",
            "CGPA",
            "Internship_Experience",
            "Extra_Curricular_Score",
            "Communication_Skills",
            "Projects_Completed"
        ]
    )

    # ================= ML PREDICTION =================

    probability = model.predict_proba(input_data)

    placement_probability = round(
        probability[0][1] * 100,
        2
    )

    # ================= PROFILE SCORE (20%) =================

    skill_score = calculate_skill_score(skills)

    profile_score = 0

    # Aptitude (40 marks)
    profile_score += min(aptitude, 40)

    # Certifications (20 marks)
    profile_score += min(certifications * 7, 20)

    # Technical Skills (30 marks)
    profile_score += min(skill_score * 5, 30)

    # Backlogs (10 marks)
    if backlogs == 0:
        profile_score += 10
    elif backlogs <= 2:
        profile_score += 5

    # ================= HYBRID SCORE =================

    final_score = round(
        (placement_probability * 0.80) +
        (profile_score * 0.20),
        2
    )

    # ================= SUGGESTIONS =================

    suggestions = []

    if backlogs >= 5:
        suggestions.append(
            "Reduce backlogs and improve academic consistency."
        )

    if certifications < 2:
        suggestions.append(
            "Complete more industry certifications."
        )

    if skill_score < 5:
        suggestions.append(
            "Improve technical skills like Python, Java, SQL and Web Technologies."
        )

    if projects < 2:
        suggestions.append(
            "Develop more practical projects."
        )

    if communication_score < 70:
        suggestions.append(
            "Practice communication and interview skills."
        )

    if aptitude < 60:
        suggestions.append(
            "Improve aptitude and logical reasoning skills."
        )

    if len(suggestions) == 0:
        suggestions.append(
            "Good preparation. Continue improving for better opportunities."
        )

   # =========== FINAL STATUS =================
    if final_score >= 75:
      placement_status = "High Placement Readiness"

    elif final_score >= 50:
        placement_status = "Medium Placement Readiness"

    elif final_score >= 35:
        placement_status = "Developing Placement Readiness"

    else:
     placement_status = "Low Placement Readiness"


    # ================= SAVE RESULT =================

    student_id = session.get("student_id")

    cursor.execute(
        """
        SELECT prediction_id
        FROM prediction_results
        WHERE student_id=%s
        """,
        (student_id,)
    )

    existing_prediction = cursor.fetchone()

    if existing_prediction:

        cursor.execute(
            """
            UPDATE prediction_results
            SET prediction_score=%s,
                placement_status=%s,
                prediction_date=CURRENT_TIMESTAMP
            WHERE student_id=%s
            """,
            (
                final_score,
                placement_status,
                student_id
            )
        )

    else:

        cursor.execute(
            """
            INSERT INTO prediction_results
            (
                student_id,
                prediction_score,
                placement_status
            )
            VALUES(%s,%s,%s)
            """,
            (
                student_id,
                final_score,
                placement_status
            )
        )

    db.commit()

    return render_template(
        "prediction-result.html",
        prediction=final_score,
        placement_status=placement_status,
        communication_score=communication_score,
        cgpa=cgpa,
        prev_sem=prev_sem,
        backlogs=backlogs,
        internship=internship,
        projects=projects,
        extra_curr=extra_curr,
        certifications=certifications,
        aptitude=aptitude,
        skills=skills,
        skill_score=skill_score,
        suggestions=suggestions
    )
# ================= ADMIN LOGOUT =================

@app.route('/admin_logout')
def admin_logout():

    session.pop("admin_id", None)
    session.pop("admin_username", None)

    return redirect(url_for("admin_login"))


# ================= LOGOUT =================


@app.route('/logout')

def logout():


    session.clear()


    return redirect(

        url_for('login')

    )








# ================= RUN =================


if __name__ == "__main__":


    app.run(debug=True)