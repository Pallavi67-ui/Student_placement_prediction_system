import os
import random
import json
import joblib
import pandas as pd
import mysql.connector
from mysql.connector import Error
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

app = Flask(__name__)
app.secret_key = "student_placement_prediction_secret_key"

# ================= DATABASE CONFIGURATION & HELPERS =================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "placement_prediction"
}


def get_db_connection():
    """Create and return a new MySQL database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"[DB Error] Could not connect to MySQL database: {e}")
        return None


def normalize_output(text):
    """Normalize student typed output and expected output for fair comparison."""
    if text is None:
        return ""
    cleaned = str(text).strip().replace("\r\n", "\n").replace("\r", "\n")
    # Strip optional surrounding quotes if student included quotes
    if (cleaned.startswith('"') and cleaned.endswith('"')) or (cleaned.startswith("'") and cleaned.endswith("'")):
        cleaned = cleaned[1:-1].strip()
    return cleaned.lower()


def ensure_database_compatibility():
    """
    Ensure all required tables and columns exist without modifying or losing existing data.
    Adds compatibility tables for company-based assessments safely.
    """
    conn = get_db_connection()
    if not conn:
        print("[DB Warning] Skipping schema compatibility check: MySQL not accessible.")
        return

    try:
        cursor = conn.cursor(buffered=True)

        # 1. students table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INT AUTO_INCREMENT PRIMARY KEY,
                fullname VARCHAR(255) NOT NULL,
                register_number VARCHAR(100) NOT NULL,
                department VARCHAR(100) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)

        # 2. admin table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin (
                admin_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)

        # Ensure default admin account exists
        cursor.execute("SELECT COUNT(*) FROM admin")
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO admin (username, password) VALUES (%s, %s)",
                ("admin", "admin123")
            )
            conn.commit()

        # 3. academics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS academics (
                academic_id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                semester INT DEFAULT 1,
                sgpa FLOAT DEFAULT 0.0,
                prev_sem FLOAT DEFAULT 0.0,
                cgpa FLOAT DEFAULT 0.0,
                backlogs INT DEFAULT 0,
                internship VARCHAR(10) DEFAULT 'No',
                projects INT DEFAULT 0,
                extra_curr INT DEFAULT 0,
                certifications INT DEFAULT 0,
                aptitude INT DEFAULT 0,
                company_name VARCHAR(255) DEFAULT '',
                internship_domain VARCHAR(255) DEFAULT '',
                internship_duration VARCHAR(100) DEFAULT '',
                skills TEXT
            )
        """)

        # Helper to check and add missing columns in academics
        cursor.execute("SHOW COLUMNS FROM academics")
        academics_cols = [row[0].lower() for row in cursor.fetchall()]

        academics_column_defs = {
            "semester": "INT DEFAULT 1",
            "sgpa": "FLOAT DEFAULT 0.0",
            "company_name": "VARCHAR(255) DEFAULT ''",
            "internship_domain": "VARCHAR(255) DEFAULT ''",
            "internship_duration": "VARCHAR(100) DEFAULT ''",
            "skills": "TEXT"
        }
        for col_name, col_type in academics_column_defs.items():
            if col_name.lower() not in academics_cols:
                cursor.execute(f"ALTER TABLE academics ADD COLUMN {col_name} {col_type}")
                conn.commit()

        # 4. student_certifications table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student_certifications (
                cert_id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                cert_name VARCHAR(255) NOT NULL,
                cert_org VARCHAR(255) NOT NULL,
                cert_year INT NOT NULL,
                credential_code VARCHAR(255) NOT NULL
            )
        """)

        # 5. communication_questions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS communication_questions (
                question_id INT AUTO_INCREMENT PRIMARY KEY,
                question TEXT NOT NULL,
                category VARCHAR(100) NOT NULL,
                option_a VARCHAR(255) NOT NULL,
                option_b VARCHAR(255) NOT NULL,
                option_c VARCHAR(255) NOT NULL,
                option_d VARCHAR(255) NOT NULL,
                correct_option VARCHAR(10) NOT NULL
            )
        """)

        # 6. communication table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS communication (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                score FLOAT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 7. technical_questions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS technical_questions (
                question_id INT AUTO_INCREMENT PRIMARY KEY,
                category VARCHAR(100) NOT NULL,
                question TEXT NOT NULL,
                option_a VARCHAR(255) NOT NULL,
                option_b VARCHAR(255) NOT NULL,
                option_c VARCHAR(255) NOT NULL,
                option_d VARCHAR(255) NOT NULL,
                correct_option VARCHAR(10) NOT NULL
            )
        """)

        # 8. aptitude_questions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS aptitude_questions (
                question_id INT AUTO_INCREMENT PRIMARY KEY,
                question TEXT NOT NULL,
                option_a VARCHAR(255) NOT NULL,
                option_b VARCHAR(255) NOT NULL,
                option_c VARCHAR(255) NOT NULL,
                option_d VARCHAR(255) NOT NULL,
                correct_option VARCHAR(10) NOT NULL,
                category VARCHAR(100) DEFAULT 'Quantitative Aptitude'
            )
        """)

        # 9. prediction_results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prediction_results (
                prediction_id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                prediction_score FLOAT NOT NULL,
                placement_status VARCHAR(100) NOT NULL,
                technical_score FLOAT DEFAULT 0.0,
                technical_correct INT DEFAULT 0,
                technical_total INT DEFAULT 10,
                prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Check and add missing columns to prediction_results
        cursor.execute("SHOW COLUMNS FROM prediction_results")
        pred_cols = [row[0].lower() for row in cursor.fetchall()]

        pred_column_defs = {
            "technical_score": "FLOAT DEFAULT 0.0",
            "technical_correct": "INT DEFAULT 0",
            "technical_total": "INT DEFAULT 10"
        }
        for col_name, col_type in pred_column_defs.items():
            if col_name.lower() not in pred_cols:
                cursor.execute(f"ALTER TABLE prediction_results ADD COLUMN {col_name} {col_type}")
                conn.commit()

        # 10. companies table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                company_id INT AUTO_INCREMENT PRIMARY KEY,
                company_name VARCHAR(100) NOT NULL UNIQUE,
                description TEXT,
                active TINYINT DEFAULT 1
            )
        """)

        # 11. company_technical_questions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS company_technical_questions (
                question_id INT AUTO_INCREMENT PRIMARY KEY,
                company_id INT DEFAULT 0,
                category VARCHAR(100) NOT NULL,
                question_type VARCHAR(50) NOT NULL DEFAULT 'mcq',
                question TEXT NOT NULL,
                code_snippet TEXT,
                option_a VARCHAR(255) DEFAULT '',
                option_b VARCHAR(255) DEFAULT '',
                option_c VARCHAR(255) DEFAULT '',
                option_d VARCHAR(255) DEFAULT '',
                correct_answer VARCHAR(255) NOT NULL,
                expected_output VARCHAR(255) DEFAULT '',
                explanation TEXT,
                difficulty VARCHAR(50) DEFAULT 'Medium',
                active TINYINT DEFAULT 1
            )
        """)

        # 12. company_assessment_results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS company_assessment_results (
                result_id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                company_id INT NOT NULL,
                company_name VARCHAR(100) NOT NULL,
                score FLOAT NOT NULL,
                correct_answers INT DEFAULT 0,
                total_questions INT DEFAULT 10,
                category_scores TEXT,
                strong_areas TEXT,
                moderate_areas TEXT,
                weak_areas TEXT,
                assessment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Seed initial questions and companies if tables are empty
        seed_questions_if_empty(cursor, conn)
        seed_company_data_if_empty(cursor, conn)

        cursor.close()
        conn.close()
    except Exception as ex:
        print(f"[DB Compatibility Warning] Exception during schema verification: {ex}")
        if conn and conn.is_connected():
            conn.close()


def seed_questions_if_empty(cursor, conn):
    """Seed baseline questions for assessments if tables are empty."""
    # Seed communication questions
    cursor.execute("SELECT COUNT(*) FROM communication_questions")
    if cursor.fetchone()[0] == 0:
        comm_seed = [
            ("Choose the sentence with correct subject-verb agreement.", "Grammar", "Neither the teacher nor the students was present.", "Neither the teacher nor the students were present.", "Neither the teacher nor the students is present.", "Neither the teacher nor the students has been present.", "B"),
            ("Identify the error: 'She has been working here since three years.'", "Grammar", "She has been", "working here", "since three years", "No error", "C"),
            ("Select the synonym for 'Meticulous':", "Vocabulary", "Careless", "Thorough and precise", "Ambiguous", "Hasty", "B"),
            ("Select the antonym for 'Candid':", "Vocabulary", "Frank", "Honest", "Deceitful", "Outspoken", "C"),
            ("Reading comprehension: What is the primary purpose of an executive summary?", "Reading Comprehension", "Provide exhaustive technical details", "Summarize key findings and recommendations concisely", "List author biographies", "Present raw survey data", "B"),
            ("Which tone is most suitable for a formal client status update email?", "Reading Comprehension", "Casual and humorous", "Professional, clear, and objective", "Demanding and urgent", "Passive and vague", "B"),
            ("In professional workplace communication, CC'ing a manager is primarily used to:", "Professional Communication", "Publicly criticize a colleague", "Keep stakeholders informed of project milestones", "Replace formal documentation", "Avoid direct responsibility", "B"),
            ("When presenting a technical proposal to non-technical executives, you should:", "Professional Communication", "Use excessive acronyms and jargon", "Focus on business value, return on investment, and impact", "Read every code line aloud", "Skip the presentation entirely", "B"),
            ("Situational: A client changes requirements two days before deployment. You should:", "Situational Communication", "Ignore the request and deploy existing code", "Assess impact, communicate timelines and trade-offs clearly to stakeholders", "Blame your teammates publicly", "Cancel the entire contract immediately", "B"),
            ("Situational: During a code review, a teammate gives harsh feedback. You should:", "Situational Communication", "Argue back aggressively", "Remain calm, evaluate technical merit objectively, and discuss solutions", "Delete the code repository", "Report them to HR immediately without discussion", "B")
        ]
        cursor.executemany("""
            INSERT INTO communication_questions
            (question, category, option_a, option_b, option_c, option_d, correct_option)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, comm_seed)
        conn.commit()

    # Seed technical questions
    cursor.execute("SELECT COUNT(*) FROM technical_questions")
    if cursor.fetchone()[0] == 0:
        tech_seed = [
            ("Python & Core CS", "What is the average time complexity of searching an element in a Hash Map (dict)?", "O(1)", "O(n)", "O(log n)", "O(n^2)", "A"),
            ("Data Structures", "Which data structure uses LIFO (Last-In-First-Out) principle?", "Queue", "Stack", "Binary Tree", "Linked List", "B"),
            ("Database Systems", "Which SQL clause is used to filter rows after an aggregation with GROUP BY?", "WHERE", "ORDER BY", "HAVING", "DISTINCT", "C"),
            ("Object Oriented Programming", "Which OOP concept describes wrapping data and methods into a single unit?", "Inheritance", "Polymorphism", "Abstraction", "Encapsulation", "D"),
            ("Python Programming", "Which of the following data types is immutable in Python?", "List", "Dictionary", "Tuple", "Set", "C"),
            ("Algorithms", "What is the worst-case time complexity of Quick Sort?", "O(n log n)", "O(n)", "O(n^2)", "O(log n)", "C"),
            ("Web Technologies", "Which HTTP method is typically used to create a new resource on a RESTful server?", "GET", "POST", "PUT", "DELETE", "B"),
            ("Operating Systems", "Which condition is NOT a necessary condition for a deadlock to occur?", "Mutual Exclusion", "Hold and Wait", "Preemption", "Circular Wait", "C"),
            ("Computer Networks", "Which protocol operates at the Transport Layer of the OSI Model to provide reliable delivery?", "IP", "TCP", "UDP", "HTTP", "B"),
            ("Machine Learning", "Which algorithm is an ensemble method based on multiple decision trees?", "Linear Regression", "K-Means", "Random Forest", "Naive Bayes", "C")
        ]
        cursor.executemany("""
            INSERT INTO technical_questions
            (category, question, option_a, option_b, option_c, option_d, correct_option)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, tech_seed)
        conn.commit()

    # Seed aptitude questions
    cursor.execute("SELECT COUNT(*) FROM aptitude_questions")
    if cursor.fetchone()[0] == 0:
        apt_seed = [
            ("A train 120 meters long passes a telegraph post in 6 seconds. What is the speed of the train in km/h?", "60 km/h", "72 km/h", "80 km/h", "90 km/h", "B", "Quantitative Aptitude"),
            ("If a product is sold for Rs. 540 with a 20% loss, what was the original cost price?", "Rs. 600", "Rs. 650", "Rs. 675", "Rs. 700", "C", "Quantitative Aptitude"),
            ("Find the next number in the series: 3, 7, 15, 31, 63, ...", "125", "127", "129", "131", "B", "Number Series"),
            ("A and B together can finish a job in 12 days. A alone can do it in 20 days. In how many days can B alone complete it?", "25 days", "30 days", "35 days", "40 days", "B", "Time and Work"),
            ("Pointing to a photograph, a man said: 'She is the daughter of my grandfather's only son.' How is the woman related to the man?", "Mother", "Sister", "Aunt", "Daughter", "B", "Logical Reasoning"),
            ("A clock shows 3:40. What is the angle between the hour hand and the minute hand?", "120 degrees", "130 degrees", "140 degrees", "150 degrees", "B", "Logical Reasoning"),
            ("In a code, 'TEACHER' is written as 'VGCEJGT'. How is 'STUDENT' written in that code?", "UVWFEPV", "UVWDGOU", "UVWFGOV", "TVWEFPU", "A", "Coding & Decoding"),
            ("A bag contains 5 red, 4 blue, and 3 green marbles. What is the probability of picking a blue marble?", "1/3", "1/4", "1/2", "5/12", "A", "Probability"),
            ("The average age of a class of 30 students is 15 years. If the teacher's age is included, the average increases by 1. What is the teacher's age?", "42 years", "44 years", "46 years", "48 years", "C", "Averages"),
            ("If 15% of a number is 45, what is 80% of that same number?", "240", "260", "280", "300", "A", "Percentages")
        ]
        cursor.executemany("""
            INSERT INTO aptitude_questions
            (question, option_a, option_b, option_c, option_d, correct_option, category)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, apt_seed)
        conn.commit()


def seed_company_data_if_empty(cursor, conn):
    """Seed companies and rich multi-type technical practice questions if empty."""
    # 1. Seed companies
    cursor.execute("SELECT COUNT(*) FROM companies")
    if cursor.fetchone()[0] == 0:
        companies_seed = [
            ("TCS", "Tata Consultancy Services - Practice patterns for NQT, Ninja, and Digital technical evaluations."),
            ("Infosys", "Infosys - Sample technical assessments focusing on algorithmic logic and core computer science."),
            ("Wipro", "Wipro - Elite NLTH technical & programming fundamentals practice questions."),
            ("Accenture", "Accenture - Practice questions on pseudocode, critical reasoning, and technical concepts."),
            ("Cognizant", "Cognizant - GenC and GenC Next practice modules covering data structures and SQL."),
            ("Capgemini", "Capgemini - Core technical assessment practice with pseudocode and coding concepts."),
            ("IBM", "IBM - Practice questions on system architecture, algorithms, and cloud foundations."),
            ("Deloitte", "Deloitte - Technology consulting sample questions covering databases, OOP, and modern tech."),
            ("EY", "Ernst & Young - Technology consulting and digital services technical practice questions."),
            ("Amazon", "Amazon - SDE level practice on data structures, algorithms, recursion, and system concepts."),
            ("Microsoft", "Microsoft - Fundamental practice questions on algorithmic complexity, trees, and logic."),
            ("Google", "Google - Analytical problem solving, time complexity, and data structure reasoning practice."),
            ("Zoho", "Zoho - Advanced C, logic building, pointer mechanics, and algorithmic problem solving."),
            ("UST", "UST Global - Enterprise software development, web APIs, and database practice questions."),
            ("Quest Global", "Quest Global - Product engineering, C/C++, and embedded logic practice questions."),
            ("Other", "General multi-company previous-pattern technical assessment questions.")
        ]
        cursor.executemany("""
            INSERT INTO companies (company_name, description, active)
            VALUES (%s, %s, 1)
        """, companies_seed)
        conn.commit()

    # 2. Seed company technical questions
    cursor.execute("SELECT COUNT(*) FROM company_technical_questions")
    if cursor.fetchone()[0] == 0:
        # Fetch company ID map
        cursor.execute("SELECT company_id, company_name FROM companies")
        company_map = {row[1]: row[0] for row in cursor.fetchall()}

        tcs_id = company_map.get("TCS", 0)
        infy_id = company_map.get("Infosys", 0)
        wip_id = company_map.get("Wipro", 0)
        acc_id = company_map.get("Accenture", 0)
        amz_id = company_map.get("Amazon", 0)
        zoh_id = company_map.get("Zoho", 0)
        gen_id = 0  # 0 indicates universal pool available to any company

        q_seed = [
            # 1. Output Prediction - Python (Loops & Math)
            (
                gen_id, "Python", "output_prediction",
                "What will be the output of this Python program?",
                "x = 5\ny = 3\nprint(x + y * 2)",
                "", "", "", "",
                "11", "11",
                "Due to operator precedence, y * 2 evaluates to 6 first, and 5 + 6 equals 11.",
                "Easy"
            ),
            # 2. Output Prediction - Python (Slicing)
            (
                tcs_id, "Python", "output_prediction",
                "What is the output of the following slice operation?",
                "s = 'PLACEMENT'\nprint(s[1:5])",
                "", "", "", "",
                "LACE", "LACE",
                "String slicing s[1:5] extracts characters from index 1 to 4: L-A-C-E.",
                "Easy"
            ),
            # 3. Output Prediction - Python (List Comprehension & Filtering)
            (
                infy_id, "Python", "output_prediction",
                "What will be printed by this code snippet?",
                "nums = [1, 2, 3, 4, 5]\nres = [x * 2 for x in nums if x % 2 == 0]\nprint(res)",
                "", "", "", "",
                "[4, 8]", "[4, 8]",
                "Only even numbers (2, 4) satisfy the condition, multiplied by 2 gives [4, 8].",
                "Medium"
            ),
            # 4. Output Prediction - Python (Dictionaries)
            (
                wip_id, "Python", "output_prediction",
                "Predict the output of the dictionary operation:",
                "d = {'a': 1, 'b': 2}\nd['a'] = d.get('a', 0) + 10\nprint(d['a'])",
                "", "", "", "",
                "11", "11",
                "d.get('a', 0) returns 1; 1 + 10 = 11, which updates key 'a'.",
                "Easy"
            ),
            # 5. Output Prediction - C (Pointers & Pre-increment)
            (
                zoh_id, "C/C++", "output_prediction",
                "What will be the output of this C code snippet?",
                "#include <stdio.h>\nint main() {\n    int a = 10;\n    int *ptr = &a;\n    *ptr += 5;\n    printf(\"%d\", a);\n    return 0;\n}",
                "", "", "", "",
                "15", "15",
                "*ptr modifies the value of variable 'a' directly in memory to 10 + 5 = 15.",
                "Medium"
            ),
            # 6. Output Prediction - Java (String Immutability)
            (
                acc_id, "Java", "output_prediction",
                "What will be the output of this Java code snippet?",
                "String str = \"Hello\";\nstr.concat(\" World\");\nSystem.out.println(str);",
                "", "", "", "",
                "Hello", "Hello",
                "Strings are immutable in Java. concat() returns a new string, leaving original 'str' unchanged.",
                "Medium"
            ),
            # 7. Output Prediction - Recursion (Logic)
            (
                amz_id, "Algorithms", "output_prediction",
                "What will be printed when func(4) is executed?",
                "def func(n):\n    if n <= 1:\n        return 1\n    return n + func(n - 1)\n\nprint(func(4))",
                "", "", "", "",
                "10", "10",
                "func(4) = 4 + func(3) = 4 + 3 + func(2) = 4 + 3 + 2 + 1 = 10.",
                "Medium"
            ),
            # 8. MCQ - Data Structures (FIFO)
            (
                gen_id, "Data Structures", "mcq",
                "Which data structure operates strictly on the FIFO (First-In-First-Out) principle?",
                None,
                "Stack", "Queue", "Binary Search Tree", "Priority Queue",
                "B", "",
                "A Queue maintains First-In-First-Out (FIFO) ordering where elements are inserted at rear and removed from front.",
                "Easy"
            ),
            # 9. MCQ - Data Structures (Stack Application)
            (
                tcs_id, "Data Structures", "mcq",
                "Which of the following problems is most efficiently solved using a Stack data structure?",
                None,
                "Balanced Parentheses checking", "Breadth-First Search", "Round Robin CPU Scheduling", "Priority Job Dispatch",
                "A", "",
                "Checking balanced parentheses utilizes a LIFO Stack to match closing symbols with the most recent open symbol.",
                "Easy"
            ),
            # 10. MCQ - Data Structures (BST Inorder)
            (
                infy_id, "Data Structures", "mcq",
                "Performing an Inorder traversal on a Binary Search Tree (BST) visits the node keys in:",
                None,
                "Reverse sorted order", "Strictly ascending sorted order", "Level-by-level order", "Random hashing order",
                "B", "",
                "Inorder traversal (Left, Root, Right) on a valid BST always produces keys in non-decreasing sorted order.",
                "Easy"
            ),
            # 11. Code / Logic - Time Complexity
            (
                amz_id, "Algorithms", "mcq",
                "What is the average time complexity of searching for an element in a balanced Binary Search Tree (AVL / Red-Black)?",
                None,
                "O(1)", "O(log n)", "O(n)", "O(n log n)",
                "B", "",
                "Because tree height is bounded by O(log n), search, insert, and delete take O(log n) average time.",
                "Medium"
            ),
            # 12. Code / Logic - Sorting Worst Case
            (
                wip_id, "Algorithms", "mcq",
                "Which comparison-based sorting algorithm has a guaranteed worst-case time complexity of O(n log n)?",
                None,
                "Quick Sort", "Merge Sort", "Bubble Sort", "Insertion Sort",
                "B", "",
                "Merge Sort repeatedly divides and merges arrays in guaranteed O(n log n) time in all cases (best, average, worst).",
                "Medium"
            ),
            # 13. MCQ - SQL (Aggregation filtering)
            (
                gen_id, "SQL", "mcq",
                "Which SQL clause is used to filter aggregated data generated by a GROUP BY clause?",
                None,
                "WHERE", "ORDER BY", "HAVING", "DISTINCT",
                "C", "",
                "The HAVING clause filters grouped summary records, whereas WHERE filters individual rows prior to aggregation.",
                "Easy"
            ),
            # 14. Code / Logic - SQL Join
            (
                acc_id, "SQL", "mcq",
                "Which SQL JOIN returns all rows from the left table, and matching records from the right table?",
                None,
                "INNER JOIN", "RIGHT JOIN", "LEFT JOIN", "FULL OUTER JOIN",
                "C", "",
                "A LEFT JOIN returns all rows from the left-hand table, filling unmatched right-hand columns with NULL.",
                "Easy"
            ),
            # 15. MCQ - DBMS (ACID Properties)
            (
                gen_id, "DBMS", "mcq",
                "In database transaction management, the 'I' in ACID stands for:",
                None,
                "Integrity", "Isolation", "Inheritance", "Indexing",
                "B", "",
                "ACID stands for Atomicity, Consistency, Isolation, and Durability.",
                "Easy"
            ),
            # 16. MCQ - DBMS (Primary Key)
            (
                tcs_id, "DBMS", "mcq",
                "Which constraint combination uniquely defines a Primary Key in relational database design?",
                None,
                "UNIQUE and NULLABLE", "UNIQUE and NOT NULL", "FOREIGN KEY and DEFAULT", "CHECK and AUTO_INCREMENT",
                "B", "",
                "A Primary Key uniquely identifies each row and strictly forbids NULL values (UNIQUE + NOT NULL).",
                "Easy"
            ),
            # 17. MCQ - OOP (Polymorphism)
            (
                gen_id, "OOP", "mcq",
                "Which concept allows a single function name or operator to possess different behaviors depending on parameters?",
                None,
                "Encapsulation", "Polymorphism", "Abstraction", "Inheritance",
                "B", "",
                "Polymorphism allows methods or operators to take many forms (e.g. method overloading and overriding).",
                "Easy"
            ),
            # 18. MCQ - OOP (Inheritance)
            (
                infy_id, "OOP", "mcq",
                "Which type of inheritance is NOT directly supported by classes in Java to avoid ambiguity (diamond problem)?",
                None,
                "Single Inheritance", "Multilevel Inheritance", "Hierarchical Inheritance", "Multiple Inheritance",
                "D", "",
                "Java does not allow a class to extend multiple classes directly to prevent the Diamond Problem; interfaces are used instead.",
                "Medium"
            ),
            # 19. MCQ - Operating Systems (Deadlock)
            (
                gen_id, "Operating Systems", "mcq",
                "Which of the following is NOT one of the Coffman conditions required for a deadlock to occur?",
                None,
                "Mutual Exclusion", "Hold and Wait", "Preemption Allowed", "Circular Wait",
                "C", "",
                "No Preemption is the necessary condition. If resources can be preempted, deadlock is prevented.",
                "Medium"
            ),
            # 20. MCQ - Operating Systems (Virtual Memory)
            (
                wip_id, "Operating Systems", "mcq",
                "Thrashing in an operating system occurs when:",
                None,
                "CPU operates at 100% compute load", "The system spends more time paging than executing processes", "Deadlock occurs between two threads", "A process terminates abnormally",
                "B", "",
                "Thrashing happens when excessive page faults force the OS to spend more time swapping pages than executing user code.",
                "Medium"
            ),
            # 21. MCQ - Computer Networks (OSI Layers)
            (
                gen_id, "Computer Networks", "mcq",
                "At which layer of the OSI model do routers primarily operate to forward packets across networks?",
                None,
                "Data Link Layer (Layer 2)", "Network Layer (Layer 3)", "Transport Layer (Layer 4)", "Application Layer (Layer 7)",
                "B", "",
                "Routers inspect logical IP addresses and operate at the Network Layer (Layer 3) to route packets.",
                "Easy"
            ),
            # 22. MCQ - Computer Networks (TCP vs UDP)
            (
                amz_id, "Computer Networks", "mcq",
                "Which transport protocol provides connection-oriented, reliable, acknowledged byte-stream delivery?",
                None,
                "UDP", "IP", "TCP", "ICMP",
                "C", "",
                "TCP (Transmission Control Protocol) establishes a 3-way handshake and guarantees in-order reliable delivery.",
                "Easy"
            ),
            # 23. MCQ - Web Development (REST Status)
            (
                gen_id, "Web Development", "mcq",
                "What HTTP status code represents '201 Created' in a RESTful Web API?",
                None,
                "200", "201", "204", "301",
                "B", "",
                "HTTP status code 201 indicates that the request succeeded and led to the creation of a new resource.",
                "Easy"
            ),
            # 24. MCQ - Web Development (CSS Box Model)
            (
                gen_id, "Web Development", "mcq",
                "In the standard CSS Box Model, which layer sits immediately between the content and the border?",
                None,
                "Margin", "Padding", "Outline", "Box-shadow",
                "B", "",
                "The CSS Box Model comprises Content -> Padding -> Border -> Margin.",
                "Easy"
            ),
            # 25. Output Prediction - Python (String join)
            (
                gen_id, "Python", "output_prediction",
                "What is the output of this Python code?",
                "words = ['Cloud', 'AI', 'ML']\nprint('-'.join(words))",
                "", "", "", "",
                "Cloud-AI-ML", "Cloud-AI-ML",
                "The join() method concatenates list elements separated by the hyphen '-' delimiter.",
                "Easy"
            ),
            # 26. Code / Logic - Missing Line / Bug
            (
                zoh_id, "Problem Solving", "output_prediction",
                "What is the output of this integer division logic in Python?",
                "a = 17 // 3\nb = 17 % 3\nprint(f'{a},{b}')",
                "", "", "", "",
                "5,2", "5,2",
                "Integer floor division 17 // 3 yields 5; remainder 17 % 3 yields 2. Result is 5,2.",
                "Easy"
            ),
            # 27. Code / Logic - Array Indexing (Python)
            (
                tcs_id, "Programming", "output_prediction",
                "What will be the output of this list mutation in Python?",
                "a = [10, 20, 30]\nb = a\nb.append(40)\nprint(len(a))",
                "", "", "", "",
                "4", "4",
                "Variables 'a' and 'b' reference the exact same list object in memory; modifying 'b' mutates 'a' as well.",
                "Medium"
            ),
            # 28. Output Prediction - Boolean Logic
            (
                infy_id, "Problem Solving", "output_prediction",
                "What boolean value will be printed by this logical condition?",
                "x = (5 > 2) and not (3 == 4 or 1 > 5)\nprint(x)",
                "", "", "", "",
                "True", "True",
                "(5 > 2) is True. (3 == 4 or 1 > 5) is False. not(False) is True. True and True yields True.",
                "Easy"
            ),
            # 29. MCQ - Data Structures (Hashing collision)
            (
                amz_id, "Data Structures", "mcq",
                "Which collision resolution technique uses linked lists to chain elements sharing the same hash index?",
                None,
                "Linear Probing", "Quadratic Probing", "Separate Chaining", "Double Hashing",
                "C", "",
                "Separate Chaining stores colliding entries in a linked list attached to each bucket of the hash table.",
                "Medium"
            ),
            # 30. MCQ - OOP (Encapsulation)
            (
                tcs_id, "OOP", "mcq",
                "Which OOP principle is implemented by declaring class attributes private and providing public getters and setters?",
                None,
                "Inheritance", "Encapsulation", "Polymorphism", "Abstraction",
                "B", "",
                "Encapsulation restricts direct external access to an object's internal state and validates access via methods.",
                "Easy"
            )
        ]

        cursor.executemany("""
            INSERT INTO company_technical_questions
            (company_id, category, question_type, question, code_snippet,
             option_a, option_b, option_c, option_d, correct_answer, expected_output, explanation, difficulty, active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
        """, q_seed)
        conn.commit()


# Run DB compatibility setup on start
ensure_database_compatibility()

# ================= LOAD ML MODEL =================

MODEL_PATH = "placement_model_old.pkl"

model = None
try:
    model = joblib.load(MODEL_PATH)
    print(f"[ML Model] Successfully loaded model from '{MODEL_PATH}'.")
except Exception as e:
    print(f"[ML Model Error] Failed loading '{MODEL_PATH}': {e}")

# ================= GENERAL ROUTES =================

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

# ================= AUTHENTICATION ROUTES =================

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        fullname = request.form.get('fullname', '').strip()
        register_number = request.form.get('register_number', '').strip()
        department = request.form.get('department', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not all([fullname, register_number, department, email, password]):
            return render_template('register.html', error="All fields are required.")

        conn = get_db_connection()
        if not conn:
            return render_template('register.html', error="Database connection error. Please try again.")

        try:
            cursor = conn.cursor(buffered=True)
            cursor.execute("SELECT student_id FROM students WHERE email = %s", (email,))
            if cursor.fetchone():
                cursor.close()
                conn.close()
                return render_template('register.html', error="An account with this email already exists.")

            query = """
                INSERT INTO students (fullname, register_number, department, email, password)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (fullname, register_number, department, email, password))
            conn.commit()
            cursor.close()
            conn.close()

            return redirect(url_for('login'))
        except Error as err:
            if conn and conn.is_connected():
                conn.close()
            return render_template('register.html', error=f"Registration failed: {err}")

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        conn = get_db_connection()
        if not conn:
            return render_template('login.html', error="Database connection failed.")

        try:
            cursor = conn.cursor(buffered=True)
            query = "SELECT * FROM students WHERE email=%s AND password=%s"
            cursor.execute(query, (email, password))
            student = cursor.fetchone()
            cursor.close()
            conn.close()

            if student:
                session.clear()
                session["student_id"] = student[0]
                session["fullname"] = student[1]
                session["register_number"] = student[2]
                session["department"] = student[3]
                session["email"] = student[4]

                # Preload existing academic info and assessment scores into session
                load_student_session_data(student[0])

                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', error="Invalid Email or Password.")
        except Error as err:
            if conn and conn.is_connected():
                conn.close()
            return render_template('login.html', error=f"Database error: {err}")

    return render_template('login.html')


def load_student_session_data(student_id):
    """Helper to populate session with student profile and assessment scores from DB."""
    conn = get_db_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor(buffered=True)
        # Academics
        cursor.execute("""
            SELECT semester, sgpa, prev_sem, cgpa, backlogs, internship,
                   projects, extra_curr, certifications, aptitude,
                   company_name, internship_domain, internship_duration
            FROM academics
            WHERE student_id=%s
        """, (student_id,))
        acad = cursor.fetchone()
        if acad:
            session["semester"] = acad[0]
            session["sgpa"] = acad[1]
            session["prev_sem"] = acad[2]
            session["cgpa"] = acad[3]
            session["backlogs"] = acad[4]
            session["internship"] = acad[5]
            session["projects"] = acad[6]
            session["extra_curr"] = acad[7]
            session["certifications"] = acad[8]
            session["aptitude"] = acad[9]
            session["company_name"] = acad[10]
            session["internship_domain"] = acad[11]
            session["internship_duration"] = acad[12]

        # Communication
        cursor.execute("SELECT score FROM communication WHERE student_id=%s ORDER BY communication_id DESC LIMIT 1", (student_id,))
        comm = cursor.fetchone()
        if comm:
            session["communication_score"] = float(comm[0])

        # Prediction / Technical
        cursor.execute("""
            SELECT prediction_score, placement_status, technical_score, technical_correct, technical_total
            FROM prediction_results
            WHERE student_id=%s
            ORDER BY prediction_date DESC LIMIT 1
        """, (student_id,))
        pred = cursor.fetchone()
        if pred:
            session["prediction_score"] = float(pred[0])
            session["placement_status"] = pred[1]
            session["technical_score"] = float(pred[2]) if pred[2] is not None else 0.0
            session["technical_correct"] = int(pred[3]) if pred[3] is not None else 0
            session["technical_total"] = int(pred[4]) if pred[4] is not None else 10

        # Latest Company Assessment
        cursor.execute("""
            SELECT result_id, company_name, score, strong_areas, weak_areas, assessment_date
            FROM company_assessment_results
            WHERE student_id=%s
            ORDER BY assessment_date DESC LIMIT 1
        """, (student_id,))
        comp_res = cursor.fetchone()
        if comp_res:
            session["latest_company_result_id"] = comp_res[0]
            session["latest_company_name"] = comp_res[1]
            session["latest_company_score"] = float(comp_res[2])
            session["latest_company_strong"] = comp_res[3] or ""
            session["latest_company_weak"] = comp_res[4] or ""

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"[Session Preload Error] {e}")
        if conn and conn.is_connected():
            conn.close()


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ================= DASHBOARD ROUTE =================

@app.route('/dashboard')
def dashboard():
    if "student_id" not in session:
        return redirect(url_for('login'))

    student_id = session["student_id"]
    load_student_session_data(student_id)

    # Fetch active companies for the "Prepare for a Company" dropdown
    companies = []
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(buffered=True)
            cursor.execute("SELECT company_id, company_name, description FROM companies WHERE active=1 ORDER BY company_name ASC")
            companies = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"[Dashboard Companies Fetch Error] {e}")
            if conn and conn.is_connected():
                conn.close()

    # If DB offline or empty, provide fallback list of top companies
    if not companies:
        companies = [
            (1, "TCS", "Tata Consultancy Services - NQT & Ninja practice pattern."),
            (2, "Infosys", "Infosys - DSE & Specialist practice pattern."),
            (3, "Wipro", "Wipro - Elite NLTH technical practice."),
            (4, "Accenture", "Accenture - Advanced Technical Assessment practice."),
            (5, "Cognizant", "Cognizant - GenC & GenC Next practice."),
            (6, "Capgemini", "Capgemini - Technical & Coding assessment."),
            (7, "Amazon", "Amazon - SDE level problem solving practice."),
            (8, "Zoho", "Zoho - C Programming and logical problem solving.")
        ]

    # Calculate Recommended Next Step dynamically
    cgpa = float(session.get("cgpa", 0.0) or 0.0)
    comm_score = session.get("communication_score")
    tech_score = session.get("technical_score")
    apt_score = session.get("aptitude")
    comp_score = session.get("latest_company_score")
    comp_weak = session.get("latest_company_weak", "")
    pred_score = session.get("prediction_score")

    if cgpa == 0.0:
        next_step = {
            "title": "Enter Your Academic Details",
            "message": "Begin your placement readiness evaluation by entering your SGPA, CGPA, backlogs, and project history.",
            "url": url_for('academics'),
            "btn_text": "Complete Academic Details"
        }
    elif comm_score is None:
        next_step = {
            "title": "Complete Communication Assessment",
            "message": "Take the 10-question communication test to evaluate your grammar, verbal clarity, and workplace interaction skills.",
            "url": url_for('communication'),
            "btn_text": "Start Communication Test"
        }
    elif tech_score is None:
        next_step = {
            "title": "Attempt General Technical Assessment",
            "message": "Test your programming foundations and computer science concepts across 10 random technical questions.",
            "url": url_for('technical_assessment'),
            "btn_text": "Start Technical Test"
        }
    elif apt_score is None or apt_score == 0:
        next_step = {
            "title": "Complete Aptitude Assessment",
            "message": "Quantify your quantitative problem solving and logical agility through the 10-question aptitude assessment.",
            "url": url_for('aptitude_assessment'),
            "btn_text": "Start Aptitude Test"
        }
    elif comp_score is None:
        next_step = {
            "title": "Take Company-Based Technical Assessment",
            "message": "Select your dream campus recruiter (TCS, Infosys, Amazon, etc.) to evaluate specific technical strengths & weaknesses.",
            "url": url_for('company_selection'),
            "btn_text": "Select Target Company"
        }
    elif comp_weak:
        next_step = {
            "title": f"Strengthen Identified Weak Areas ({comp_weak})",
            "message": f"Your recent company evaluation highlighted improvement targets in {comp_weak}. Practice these topics before attempting another mock assessment.",
            "url": url_for('company_selection'),
            "btn_text": "Retake Company Assessment"
        }
    else:
        next_step = {
            "title": "Review Final Placement Prediction",
            "message": "Great progress! Your profile and assessment scores are recorded. Check your hybrid ML readiness classification and detailed suggestions.",
            "url": url_for('view_result'),
            "btn_text": "View Prediction Result"
        }

    return render_template(
        'dashboard.html',
        companies=companies,
        next_step=next_step
    )

# ================= STAGE 1: ACADEMICS ROUTE =================

@app.route('/academics', methods=['GET', 'POST'])
def academics():
    if "student_id" not in session:
        return redirect(url_for('login'))

    student_id = session["student_id"]
    conn = get_db_connection()

    if request.method == "POST":
        semester = int(request.form.get('semester', 1) or 1)
        sgpa = float(request.form.get('sgpa', 0.0) or 0.0)
        prev_sem = float(request.form.get('prev_sem', 0.0) or 0.0)
        cgpa = float(request.form.get('cgpa', 0.0) or 0.0)
        backlogs = int(request.form.get('backlogs', 0) or 0)
        internship = request.form.get('internship', 'No')
        projects = int(request.form.get('projects', 1) or 1)
        extra_curr = int(request.form.get('extra_curr', 5) or 5)
        certifications = int(request.form.get('certifications', 0) or 0)
        aptitude = int(request.form.get('aptitude', 60) or 60)
        company_name = request.form.get('company_name', '').strip()
        internship_domain = request.form.get('internship_domain', '').strip()
        internship_duration = request.form.get('internship_duration', '').strip()

        if semester == 1 and prev_sem == 0:
            prev_sem = round(sgpa * 9.5, 2) if sgpa > 0 else 0.0

        if conn:
            try:
                cursor = conn.cursor(buffered=True)
                cursor.execute("SELECT academic_id FROM academics WHERE student_id=%s", (student_id,))
                existing = cursor.fetchone()

                if existing:
                    cursor.execute("""
                        UPDATE academics
                        SET semester=%s, sgpa=%s, prev_sem=%s, cgpa=%s, backlogs=%s,
                            internship=%s, projects=%s, extra_curr=%s, certifications=%s,
                            aptitude=%s, company_name=%s, internship_domain=%s, internship_duration=%s
                        WHERE student_id=%s
                    """, (
                        semester, sgpa, prev_sem, cgpa, backlogs,
                        internship, projects, extra_curr, certifications,
                        aptitude, company_name, internship_domain, internship_duration,
                        student_id
                    ))
                else:
                    cursor.execute("""
                        INSERT INTO academics
                        (student_id, semester, sgpa, prev_sem, cgpa, backlogs,
                         internship, projects, extra_curr, certifications, aptitude,
                         company_name, internship_domain, internship_duration)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """, (
                        student_id, semester, sgpa, prev_sem, cgpa, backlogs,
                        internship, projects, extra_curr, certifications, aptitude,
                        company_name, internship_domain, internship_duration
                    ))
                conn.commit()
                cursor.close()
                conn.close()
            except Error as err:
                print(f"[Academics DB Error] {err}")
                if conn and conn.is_connected():
                    conn.close()

        # Update session
        session["semester"] = semester
        session["sgpa"] = sgpa
        session["prev_sem"] = prev_sem
        session["cgpa"] = cgpa
        session["backlogs"] = backlogs
        session["internship"] = internship
        session["projects"] = projects
        session["extra_curr"] = extra_curr
        session["certifications"] = certifications
        session["aptitude"] = aptitude
        session["company_name"] = company_name
        session["internship_domain"] = internship_domain
        session["internship_duration"] = internship_duration

        return redirect(url_for('certifications'))

    # GET Request: Load existing details
    academic = None
    if conn:
        try:
            cursor = conn.cursor(buffered=True)
            cursor.execute("""
                SELECT semester, sgpa, prev_sem, cgpa, backlogs, internship,
                       projects, extra_curr, certifications, aptitude,
                       company_name, internship_domain, internship_duration
                FROM academics
                WHERE student_id=%s
            """, (student_id,))
            academic = cursor.fetchone()
            cursor.close()
            conn.close()
        except Error as err:
            print(f"[Academics Fetch Error] {err}")
            if conn and conn.is_connected():
                conn.close()

    return render_template('academics.html', academic=academic)

# ================= STAGE 2: CERTIFICATIONS ROUTE =================

@app.route('/certifications', methods=['GET', 'POST'])
def certifications():
    if "student_id" not in session:
        return redirect(url_for('login'))

    student_id = session["student_id"]
    conn = get_db_connection()

    if request.method == "POST":
        cert_names = request.form.getlist('cert_name[]')
        cert_orgs = request.form.getlist('cert_org[]')
        cert_years = request.form.getlist('cert_year[]')
        cert_ids = request.form.getlist('cert_id[]')

        valid_certs = []
        for i in range(len(cert_names)):
            name = cert_names[i].strip() if i < len(cert_names) else ""
            org = cert_orgs[i].strip() if i < len(cert_orgs) else ""
            year = int(cert_years[i]) if i < len(cert_years) and cert_years[i].isdigit() else 2024
            code = cert_ids[i].strip() if i < len(cert_ids) else ""
            if name:
                valid_certs.append((name, org, year, code))

        valid_certs = valid_certs[:5]
        cert_count = len(valid_certs)

        if conn:
            try:
                cursor = conn.cursor(buffered=True)
                cursor.execute("DELETE FROM student_certifications WHERE student_id=%s", (student_id,))
                for c in valid_certs:
                    cursor.execute("""
                        INSERT INTO student_certifications
                        (student_id, cert_name, cert_org, cert_year, credential_code)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (student_id, c[0], c[1], c[2], c[3]))

                cursor.execute("""
                    UPDATE academics
                    SET certifications=%s
                    WHERE student_id=%s
                """, (cert_count, student_id))

                conn.commit()
                cursor.close()
                conn.close()
            except Error as err:
                print(f"[Certifications DB Error] {err}")
                if conn and conn.is_connected():
                    conn.close()

        session["certifications"] = cert_count
        return redirect(url_for('communication'))

    existing_certs = []
    if conn:
        try:
            cursor = conn.cursor(buffered=True)
            cursor.execute("""
                SELECT cert_id, student_id, cert_name, cert_org, cert_year, credential_code
                FROM student_certifications
                WHERE student_id=%s
            """, (student_id,))
            existing_certs = cursor.fetchall()
            cursor.close()
            conn.close()
        except Error as err:
            print(f"[Certifications Fetch Error] {err}")
            if conn and conn.is_connected():
                conn.close()

    return render_template('certifications.html', existing_certs=existing_certs)


@app.route('/skip_certifications')
def skip_certifications():
    if "student_id" not in session:
        return redirect(url_for('login'))

    student_id = session["student_id"]
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(buffered=True)
            cursor.execute("UPDATE academics SET certifications=0 WHERE student_id=%s", (student_id,))
            conn.commit()
            cursor.close()
            conn.close()
        except Error as err:
            print(f"[Skip Certifications Error] {err}")
            if conn and conn.is_connected():
                conn.close()

    session["certifications"] = 0
    return redirect(url_for('communication'))

# ================= STAGE 3: COMMUNICATION ASSESSMENT ROUTE =================

@app.route('/communication', methods=['GET', 'POST'])
def communication():
    if "student_id" not in session:
        return redirect(url_for('login'))

    student_id = session["student_id"]
    conn = get_db_connection()

    if request.method == "POST":
        comm_qids = session.get("comm_qids", [])
        correct_count = 0
        total_questions = len(comm_qids) if comm_qids else 10

        if conn and comm_qids:
            try:
                cursor = conn.cursor(buffered=True)
                format_strings = ','.join(['%s'] * len(comm_qids))
                cursor.execute(
                    f"SELECT question_id, correct_option FROM communication_questions WHERE question_id IN ({format_strings})",
                    tuple(comm_qids)
                )
                answer_map = {row[0]: row[1].strip().upper() for row in cursor.fetchall()}

                for qid in comm_qids:
                    user_ans = request.form.get(f"q{qid}", "").strip().upper()
                    if user_ans and user_ans == answer_map.get(qid):
                        correct_count += 1

                score = round((correct_count / total_questions) * 100, 2)

                cursor.execute(
                    "INSERT INTO communication (student_id, score) VALUES (%s, %s)",
                    (student_id, score)
                )
                conn.commit()
                cursor.close()
                conn.close()
            except Error as err:
                print(f"[Communication Post Error] {err}")
                score = round((correct_count / max(total_questions, 1)) * 100, 2)
                if conn and conn.is_connected():
                    conn.close()
        else:
            score = 0.0

        session["communication_score"] = score
        session.pop("comm_qids", None)

        return redirect(url_for('technical_assessment'))

    selected_questions = []
    if conn:
        try:
            cursor = conn.cursor(buffered=True)
            categories = [
                "Grammar",
                "Vocabulary",
                "Reading Comprehension",
                "Professional Communication",
                "Situational Communication"
            ]

            for cat in categories:
                cursor.execute(
                    "SELECT * FROM communication_questions WHERE category=%s",
                    (cat,)
                )
                q_list = cursor.fetchall()
                if q_list:
                    k = min(2, len(q_list))
                    selected_questions.extend(random.sample(q_list, k))

            if len(selected_questions) < 10:
                selected_ids = [q[0] for q in selected_questions]
                if selected_ids:
                    format_strings = ','.join(['%s'] * len(selected_ids))
                    cursor.execute(
                        f"SELECT * FROM communication_questions WHERE question_id NOT IN ({format_strings})",
                        tuple(selected_ids)
                    )
                else:
                    cursor.execute("SELECT * FROM communication_questions")
                remaining = cursor.fetchall()
                needed = 10 - len(selected_questions)
                if remaining:
                    selected_questions.extend(random.sample(remaining, min(needed, len(remaining))))

            random.shuffle(selected_questions)
            cursor.close()
            conn.close()
        except Error as err:
            print(f"[Communication Get Error] {err}")
            if conn and conn.is_connected():
                conn.close()

    session["comm_qids"] = [q[0] for q in selected_questions]
    return render_template('communication-assessment.html', questions=selected_questions)


@app.route('/skip_communication')
def skip_communication():
    if "student_id" not in session:
        return redirect(url_for('login'))

    student_id = session["student_id"]
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(buffered=True)
            cursor.execute("INSERT INTO communication (student_id, score) VALUES (%s, 0.0)", (student_id,))
            conn.commit()
            cursor.close()
            conn.close()
        except Error as err:
            print(f"[Skip Communication DB Error] {err}")
            if conn and conn.is_connected():
                conn.close()

    session["communication_score"] = 0.0
    session.pop("comm_qids", None)
    return redirect(url_for('technical_assessment'))

# ================= STAGE 4: GENERAL TECHNICAL ASSESSMENT ROUTE =================

@app.route('/technical_assessment', methods=['GET', 'POST'])
def technical_assessment():
    if "student_id" not in session:
        return redirect(url_for('login'))

    student_id = session["student_id"]
    conn = get_db_connection()

    if request.method == "POST":
        tech_qids = session.get("tech_qids", [])
        correct_count = 0
        total_questions = len(tech_qids) if tech_qids else 10

        if conn and tech_qids:
            try:
                cursor = conn.cursor(buffered=True)
                format_strings = ','.join(['%s'] * len(tech_qids))
                cursor.execute(
                    f"SELECT question_id, correct_option FROM technical_questions WHERE question_id IN ({format_strings})",
                    tuple(tech_qids)
                )
                answer_map = {row[0]: row[1].strip().upper() for row in cursor.fetchall()}

                for qid in tech_qids:
                    user_ans = request.form.get(f"q{qid}", "").strip().upper()
                    if user_ans and user_ans == answer_map.get(qid):
                        correct_count += 1

                tech_score = round((correct_count / total_questions) * 100, 2)
                cursor.close()
                conn.close()
            except Error as err:
                print(f"[Technical Post Error] {err}")
                tech_score = round((correct_count / max(total_questions, 1)) * 100, 2)
                if conn and conn.is_connected():
                    conn.close()
        else:
            tech_score = 0.0

        session["technical_score"] = tech_score
        session["technical_correct"] = correct_count
        session["technical_total"] = total_questions
        session.pop("tech_qids", None)

        return redirect(url_for('aptitude_assessment'))

    selected_questions = []
    if conn:
        try:
            cursor = conn.cursor(buffered=True)
            cursor.execute("SELECT * FROM technical_questions")
            all_questions = cursor.fetchall()
            if all_questions:
                k = min(10, len(all_questions))
                selected_questions = random.sample(all_questions, k)
            cursor.close()
            conn.close()
        except Error as err:
            print(f"[Technical Assessment Fetch Error] {err}")
            if conn and conn.is_connected():
                conn.close()

    session["tech_qids"] = [q[0] for q in selected_questions]
    return render_template('technical-assessment.html', questions=selected_questions)


@app.route('/skip_technical_assessment')
def skip_technical_assessment():
    if "student_id" not in session:
        return redirect(url_for('login'))

    session["technical_score"] = 0.0
    session["technical_correct"] = 0
    session["technical_total"] = 10
    session.pop("tech_qids", None)

    return redirect(url_for('aptitude_assessment'))

# ================= STAGE 5: APTITUDE ASSESSMENT ROUTE =================

@app.route('/aptitude_assessment', methods=['GET', 'POST'])
def aptitude_assessment():
    if "student_id" not in session:
        return redirect(url_for('login'))

    student_id = session["student_id"]
    conn = get_db_connection()

    if request.method == "POST":
        apt_qids = session.get("apt_qids", [])
        correct_count = 0
        total_questions = len(apt_qids) if apt_qids else 10

        if conn and apt_qids:
            try:
                cursor = conn.cursor(buffered=True)
                format_strings = ','.join(['%s'] * len(apt_qids))
                cursor.execute(
                    f"SELECT question_id, correct_option FROM aptitude_questions WHERE question_id IN ({format_strings})",
                    tuple(apt_qids)
                )
                answer_map = {row[0]: row[1].strip().upper() for row in cursor.fetchall()}

                for qid in apt_qids:
                    user_ans = request.form.get(f"q{qid}", "").strip().upper()
                    if user_ans and user_ans == answer_map.get(qid):
                        correct_count += 1

                apt_score = round((correct_count / total_questions) * 100, 2)

                cursor.execute("UPDATE academics SET aptitude=%s WHERE student_id=%s", (int(apt_score), student_id))
                conn.commit()
                cursor.close()
                conn.close()
            except Error as err:
                print(f"[Aptitude Post Error] {err}")
                apt_score = round((correct_count / max(total_questions, 1)) * 100, 2)
                if conn and conn.is_connected():
                    conn.close()
        else:
            apt_score = session.get("aptitude", 60)

        session["aptitude"] = int(apt_score)
        session.pop("apt_qids", None)

        return redirect(url_for('prediction'))

    selected_questions = []
    if conn:
        try:
            cursor = conn.cursor(buffered=True)
            cursor.execute("SELECT * FROM aptitude_questions")
            all_questions = cursor.fetchall()
            if all_questions:
                k = min(10, len(all_questions))
                selected_questions = random.sample(all_questions, k)
            cursor.close()
            conn.close()
        except Error as err:
            print(f"[Aptitude Get Error] {err}")
            if conn and conn.is_connected():
                conn.close()

    session["apt_qids"] = [q[0] for q in selected_questions]
    return render_template('aptitude-assessment.html', questions=selected_questions)


@app.route('/skip_aptitude_assessment')
def skip_aptitude_assessment():
    if "student_id" not in session:
        return redirect(url_for('login'))

    session.pop("apt_qids", None)
    return redirect(url_for('prediction'))

# ================= COMPANY-BASED TECHNICAL ASSESSMENT =================

@app.route('/company_selection')
def company_selection():
    """Display company selection portal for students to choose target companies."""
    if "student_id" not in session:
        return redirect(url_for('login'))

    companies = []
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(buffered=True)
            cursor.execute("SELECT company_id, company_name, description FROM companies WHERE active=1 ORDER BY company_name ASC")
            companies = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as err:
            print(f"[Company Selection Fetch Error] {err}")
            if conn and conn.is_connected():
                conn.close()

    # Fallback if empty
    if not companies:
        companies = [
            (1, "TCS", "Tata Consultancy Services - NQT, Ninja & Digital practice questions."),
            (2, "Infosys", "Infosys - Specialist & DSE coding and algorithmic practice."),
            (3, "Wipro", "Wipro - Elite NLTH technical & programming fundamentals."),
            (4, "Accenture", "Accenture - Critical reasoning, pseudocode & technical practice."),
            (5, "Cognizant", "Cognizant - GenC & GenC Next data structures and SQL practice."),
            (6, "Capgemini", "Capgemini - Core technical assessment and pseudocode."),
            (7, "IBM", "IBM - Systems, architecture & cloud fundamentals practice."),
            (8, "Deloitte", "Deloitte - Technology consulting and database concepts."),
            (9, "EY", "Ernst & Young - Technology consulting practice questions."),
            (10, "Amazon", "Amazon - SDE level data structures, algorithms & logic."),
            (11, "Microsoft", "Microsoft - Algorithmic complexity and core CS practice."),
            (12, "Google", "Google - Analytical problem solving and algorithm analysis."),
            (13, "Zoho", "Zoho - C programming, pointer mechanics and logic building."),
            (14, "UST", "UST Global - Enterprise software & API development practice."),
            (15, "Quest Global", "Quest Global - Product engineering and embedded logic practice."),
            (16, "Other", "Universal sample previous-pattern technical assessment.")
        ]

    return render_template('company-selection.html', companies=companies)


@app.route('/company_assessment/<int:company_id>')
def company_assessment(company_id):
    """Start a 10-question company-based technical assessment with diverse question types."""
    if "student_id" not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    company_name = "Target Company"
    selected_questions = []

    if conn:
        try:
            cursor = conn.cursor(buffered=True)
            # Get company name
            cursor.execute("SELECT company_name FROM companies WHERE company_id=%s", (company_id,))
            row = cursor.fetchone()
            if row:
                company_name = row[0]

            # Fetch questions matching company or general pool (company_id = 0)
            cursor.execute("""
                SELECT question_id, category, question_type, question, code_snippet,
                       option_a, option_b, option_c, option_d, correct_answer, expected_output, explanation, difficulty
                FROM company_technical_questions
                WHERE active=1 AND (company_id=%s OR company_id=0)
            """, (company_id,))
            pool = cursor.fetchall()

            if pool:
                # Select up to 10 non-duplicate questions
                k = min(10, len(pool))
                selected_questions = random.sample(pool, k)

            cursor.close()
            conn.close()
        except Exception as err:
            print(f"[Company Assessment Fetch Error] {err}")
            if conn and conn.is_connected():
                conn.close()

    if not selected_questions:
        flash("No active practice questions currently found for this company. Please try another selection.")
        return redirect(url_for('company_selection'))

    # Store in session
    session["target_company_id"] = company_id
    session["target_company_name"] = company_name
    session["company_qids"] = [q[0] for q in selected_questions]

    return render_template(
        'company-assessment.html',
        questions=selected_questions,
        company_id=company_id,
        company_name=company_name
    )


def generate_company_feedback(strong_areas, moderate_areas, weak_areas):
    """Generate personalized actionable technical feedback and recommended study topics."""
    feedback = {}

    if strong_areas:
        feedback["strong"] = f"You demonstrated strong proficiency in {', '.join(strong_areas)}. Your fundamentals in these topics meet high campus recruitment standards."
    else:
        feedback["strong"] = "Dedicate consistent practice to build at least 2-3 core technical areas into standout strengths before campus drives."

    if moderate_areas:
        feedback["moderate"] = f"You possess a fair conceptual understanding of {', '.join(moderate_areas)}, but regular coding drills will elevate your accuracy to top-tier cutoffs."
    else:
        feedback["moderate"] = "No topics in the moderate band; your technical performance clearly divides between masteries and revision priorities."

    if weak_areas:
        feedback["weak"] = f"Focused revision needed in {', '.join(weak_areas)}. Prioritize revisiting fundamental concepts, step-by-step logic tracing, and sample interview questions."
    else:
        feedback["weak"] = "Excellent performance! None of your evaluated technical categories fell below the 50% threshold."

    study_recommendations = {
        "Data Structures": "Practice Arrays, Linked Lists, Stacks, Queues, Binary Search Trees, and Breadth-First/Depth-First Traversals.",
        "Algorithms": "Review Time & Space Complexity (Big-O), Binary Search, Two Pointers, and Merge/Quick Sort algorithms.",
        "DBMS": "Study ACID properties, Normalization (1NF through BCNF), Primary vs Foreign Keys, and Indexing principles.",
        "SQL": "Practice multi-table JOINs, GROUP BY with HAVING, nested subqueries, and aggregate analytical queries.",
        "OOP": "Review Polymorphism, Encapsulation, Abstract classes vs Interfaces, and Method Overloading vs Overriding.",
        "Python": "Practice list comprehensions, slicing mechanics, dictionary operations, string methods, and lambda functions.",
        "Java": "Study String immutability, Garbage Collection, Collections Framework (ArrayList, HashMap), and OOP hierarchies.",
        "C/C++": "Practice pointer dereferencing, memory allocation (malloc/free), pre/post increments, and recursion stack tracing.",
        "Operating Systems": "Review CPU Scheduling, Paging, Virtual Memory Thrashing, and Coffman deadlock conditions.",
        "Computer Networks": "Study OSI Model layers, TCP vs UDP 3-way handshakes, HTTP status codes, and IP subnetting.",
        "Web Development": "Review RESTful API design, HTTP methods (GET, POST, PUT), and CSS Box Model fundamentals.",
        "Programming": "Focus on step-by-step code tracing, variable mutability, edge cases, and integer division logic.",
        "Problem Solving": "Practice tracing loop conditions, boolean logic combinations, and algebraic equation solving."
    }

    topics = []
    for area in weak_areas + moderate_areas:
        if area in study_recommendations:
            rec = study_recommendations[area]
            if not any(t["topic"] == rec for t in topics):
                topics.append({"category": area, "topic": rec})

    if not topics:
        topics.append({
            "category": "Advanced Preparation",
            "topic": "Explore System Design basics, LeetCode medium questions, and company-specific previous interview rounds."
        })

    return feedback, topics


@app.route('/submit_company_assessment', methods=['POST'])
def submit_company_assessment():
    """Process student company assessment submission and evaluate category-wise strengths."""
    if "student_id" not in session:
        return redirect(url_for('login'))

    student_id = session["student_id"]
    company_id = session.get("target_company_id", 0)
    company_name = session.get("target_company_name", "Target Company")
    company_qids = session.get("company_qids", [])

    if not company_qids:
        flash("Assessment session expired or no questions answered. Please reselect your target company.")
        return redirect(url_for('company_selection'))

    conn = get_db_connection()
    if not conn:
        flash("Database connection error while saving assessment. Please try again.")
        return redirect(url_for('dashboard'))

    correct_answers = 0
    total_questions = len(company_qids)
    category_stats = {}  # {category: {"correct": int, "total": int}}

    try:
        cursor = conn.cursor(buffered=True)
        format_strings = ','.join(['%s'] * len(company_qids))
        cursor.execute(
            f"""
            SELECT question_id, category, question_type, correct_answer, expected_output
            FROM company_technical_questions
            WHERE question_id IN ({format_strings})
            """,
            tuple(company_qids)
        )
        questions_data = cursor.fetchall()

        for row in questions_data:
            qid = row[0]
            cat = row[1]
            qtype = row[2]
            correct_ans = row[3]
            expected_out = row[4]

            if cat not in category_stats:
                category_stats[cat] = {"correct": 0, "total": 0}
            category_stats[cat]["total"] += 1

            student_val = request.form.get(f"q{qid}", "").strip()

            is_correct = False
            if qtype == "output_prediction":
                # Compare normalized string output
                normalized_student = normalize_output(student_val)
                normalized_expected = normalize_output(expected_out or correct_ans)
                if normalized_student and normalized_student == normalized_expected:
                    is_correct = True
            else:
                # MCQ or single-choice code logic
                if student_val.upper() == correct_ans.strip().upper():
                    is_correct = True

            if is_correct:
                correct_answers += 1
                category_stats[cat]["correct"] += 1

        overall_score = round((correct_answers / max(total_questions, 1)) * 100, 1)

        # Calculate category scores and classify into Strong, Moderate, Weak
        category_scores = {}
        strong_areas = []
        moderate_areas = []
        weak_areas = []

        for cat, stats in category_stats.items():
            cat_pct = round((stats["correct"] / max(stats["total"], 1)) * 100, 1)
            category_scores[cat] = {
                "score": cat_pct,
                "correct": stats["correct"],
                "total": stats["total"]
            }
            if cat_pct >= 75.0:
                strong_areas.append(cat)
            elif cat_pct >= 50.0:
                moderate_areas.append(cat)
            else:
                weak_areas.append(cat)

        # Generate personalized feedback and recommended topics
        feedback, recommended_topics = generate_company_feedback(strong_areas, moderate_areas, weak_areas)

        # Save to database
        category_scores_json = json.dumps(category_scores)
        strong_str = ", ".join(strong_areas)
        moderate_str = ", ".join(moderate_areas)
        weak_str = ", ".join(weak_areas)

        cursor.execute("""
            INSERT INTO company_assessment_results
            (student_id, company_id, company_name, score, correct_answers, total_questions,
             category_scores, strong_areas, moderate_areas, weak_areas)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            student_id, company_id, company_name, overall_score, correct_answers, total_questions,
            category_scores_json, strong_str, moderate_str, weak_str
        ))
        result_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()

        # Update session cache
        session["latest_company_result_id"] = result_id
        session["latest_company_name"] = company_name
        session["latest_company_score"] = overall_score
        session["latest_company_strong"] = strong_str
        session["latest_company_weak"] = weak_str
        session.pop("company_qids", None)

        return redirect(url_for('company_result', result_id=result_id))
    except Exception as e:
        print(f"[Submit Company Assessment Error] {e}")
        if conn and conn.is_connected():
            conn.close()
        flash(f"Error evaluating submission: {e}")
        return redirect(url_for('dashboard'))


@app.route('/skip_company_assessment')
def skip_company_assessment():
    """Allow skipping company assessment gracefully."""
    if "student_id" not in session:
        return redirect(url_for('login'))

    session.pop("company_qids", None)
    return redirect(url_for('dashboard'))


@app.route('/company_result/<int:result_id>')
def company_result(result_id):
    """Render comprehensive Company Technical Assessment Result."""
    if "student_id" not in session:
        return redirect(url_for('login'))

    student_id = session["student_id"]
    conn = get_db_connection()
    result = None

    if conn:
        try:
            cursor = conn.cursor(buffered=True)
            cursor.execute("""
                SELECT result_id, student_id, company_id, company_name, score, correct_answers,
                       total_questions, category_scores, strong_areas, moderate_areas, weak_areas, assessment_date
                FROM company_assessment_results
                WHERE result_id=%s AND student_id=%s
            """, (result_id, student_id))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"[Company Result Fetch Error] {e}")
            if conn and conn.is_connected():
                conn.close()

    if not result:
        flash("Result not found.")
        return redirect(url_for('company_selection'))

    company_name = result[3]
    overall_score = float(result[4])
    correct_answers = int(result[5])
    total_questions = int(result[6])
    category_scores = json.loads(result[7]) if result[7] else {}
    strong_areas = [s.strip() for s in result[8].split(",") if s.strip()] if result[8] else []
    moderate_areas = [s.strip() for s in result[9].split(",") if s.strip()] if result[9] else []
    weak_areas = [s.strip() for s in result[10].split(",") if s.strip()] if result[10] else []
    assessment_date = result[11]

    feedback, recommended_topics = generate_company_feedback(strong_areas, moderate_areas, weak_areas)

    return render_template(
        'company-result.html',
        company_name=company_name,
        overall_score=overall_score,
        correct_answers=correct_answers,
        total_questions=total_questions,
        category_scores=category_scores,
        strong_areas=strong_areas,
        moderate_areas=moderate_areas,
        weak_areas=weak_areas,
        feedback=feedback,
        recommended_topics=recommended_topics,
        assessment_date=assessment_date
    )


@app.route('/latest_company_result')
def latest_company_result():
    """Directly view the student's most recent company assessment result."""
    if "student_id" not in session:
        return redirect(url_for('login'))

    student_id = session["student_id"]
    conn = get_db_connection()
    latest_id = None

    if conn:
        try:
            cursor = conn.cursor(buffered=True)
            cursor.execute(
                "SELECT result_id FROM company_assessment_results WHERE student_id=%s ORDER BY assessment_date DESC LIMIT 1",
                (student_id,)
            )
            row = cursor.fetchone()
            if row:
                latest_id = row[0]
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"[Latest Company Result Error] {e}")
            if conn and conn.is_connected():
                conn.close()

    if latest_id:
        return redirect(url_for('company_result', result_id=latest_id))
    else:
        flash("You have not taken a company assessment yet. Select a company to begin.")
        return redirect(url_for('company_selection'))

# ================= STAGE 6: HYBRID PREDICTION ENGINE =================

def generate_recommendations(backlogs, certifications, technical_score, projects, communication_score, aptitude, cgpa):
    """Generate personalized recommendations based on student's performance factors."""
    suggestions = []
    if backlogs > 0:
        suggestions.append("Prioritize clearing active backlogs to enhance academic eligibility for campus recruitment.")
    if certifications < 2:
        suggestions.append("Earn recognized industry certifications (e.g. AWS, NPTEL, Coursera) to strengthen your technical profile.")
    if technical_score < 60:
        suggestions.append("Strengthen core computer science foundations, algorithms, and practical programming languages (Python, Java, SQL).")
    if projects < 2:
        suggestions.append("Build more practical full-stack or domain projects to showcase demonstrable skills during interviews.")
    if communication_score < 70:
        suggestions.append("Practice verbal articulation, technical explanations, and workplace communication to excel in HR & technical rounds.")
    if aptitude < 60:
        suggestions.append("Dedicate regular practice to quantitative problem solving, logical reasoning, and data interpretation speed.")
    if cgpa < 7.0:
        suggestions.append("Focus on lifting semester SGPA to achieve a cumulative CGPA of 7.0+ for top-tier company cutoffs.")

    if not suggestions:
        suggestions.append("Excellent overall preparation! Continue honing your programming, interview readiness, and soft skills.")

    return suggestions


@app.route('/prediction')
def prediction():
    if "student_id" not in session:
        return redirect(url_for('login'))

    student_id = session["student_id"]

    if "cgpa" not in session:
        load_student_session_data(student_id)

    semester = session.get("semester", 1)
    sgpa = float(session.get("sgpa", 0.0) or 0.0)
    prev_sem = float(session.get("prev_sem", 0.0) or 0.0)
    cgpa = float(session.get("cgpa", 0.0) or 0.0)
    backlogs = int(session.get("backlogs", 0) or 0)
    internship = session.get("internship", "No")
    projects = int(session.get("projects", 0) or 0)
    extra_curr = int(session.get("extra_curr", 5) or 5)
    certifications = int(session.get("certifications", 0) or 0)
    aptitude = int(session.get("aptitude", 60) or 60)
    communication_score = float(session.get("communication_score", 0.0) or 0.0)
    technical_score = float(session.get("technical_score", 0.0) or 0.0)
    technical_correct = int(session.get("technical_correct", 0) or 0)
    technical_total = int(session.get("technical_total", 10) or 10)

    # Convert features for ML classification
    internship_val = 1 if internship == "Yes" else 0
    communication_ml = round((communication_score / 100.0) * 10)

    # 1. Evaluate Machine Learning Probability using placement_model_old.pkl (80% weight)
    ml_prob = 50.0
    if model:
        try:
            input_df = pd.DataFrame([[
                prev_sem,
                cgpa,
                internship_val,
                extra_curr,
                communication_ml,
                projects
            ]], columns=[
                "Prev_Sem_Result",
                "CGPA",
                "Internship_Experience",
                "Extra_Curricular_Score",
                "Communication_Skills",
                "Projects_Completed"
            ])
            probability = model.predict_proba(input_df)
            ml_prob = round(probability[0][1] * 100, 2)
        except Exception as e:
            print(f"[Model Predict Error] {e}")
            base = min(100.0, (cgpa / 10.0) * 60 + (internship_val * 15) + min(projects * 5, 15) + (communication_ml * 1))
            ml_prob = round(base, 2)
    else:
        base = min(100.0, (cgpa / 10.0) * 55 + (internship_val * 20) + min(projects * 5, 15) + (communication_ml * 1))
        ml_prob = round(base, 2)

    # 2. Evaluate Rule-Based Profile Score (20% weight, 100 pts total)
    tech_pts = (technical_score / 100.0) * 45.0
    apt_pts = (aptitude / 100.0) * 30.0
    cert_pts = min(certifications * 3.0, 15.0)
    comm_pts = (communication_score / 100.0) * 10.0
    rule_score = round(tech_pts + apt_pts + cert_pts + comm_pts, 2)

    # 3. Hybrid Final Placement Readiness Score (80% ML + 20% Rules)
    final_score = round((0.80 * ml_prob) + (0.20 * rule_score), 2)
    final_score = max(0.0, min(100.0, final_score))

    # 4. Placement Readiness Category
    if final_score >= 75.0:
        placement_status = "High Placement Readiness"
    elif final_score >= 50.0:
        placement_status = "Medium Placement Readiness"
    elif final_score >= 35.0:
        placement_status = "Developing Placement Readiness"
    else:
        placement_status = "Low Placement Readiness"

    # 5. Personalized Recommendations
    suggestions = generate_recommendations(
        backlogs, certifications, technical_score, projects,
        communication_score, aptitude, cgpa
    )

    # 6. Save or Update Result in Database
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(buffered=True)
            cursor.execute("SELECT prediction_id FROM prediction_results WHERE student_id=%s", (student_id,))
            existing = cursor.fetchone()

            if existing:
                cursor.execute("""
                    UPDATE prediction_results
                    SET prediction_score=%s,
                        placement_status=%s,
                        technical_score=%s,
                        technical_correct=%s,
                        technical_total=%s,
                        prediction_date=CURRENT_TIMESTAMP
                    WHERE student_id=%s
                """, (
                    final_score,
                    placement_status,
                    technical_score,
                    technical_correct,
                    technical_total,
                    student_id
                ))
            else:
                cursor.execute("""
                    INSERT INTO prediction_results
                    (student_id, prediction_score, placement_status, technical_score, technical_correct, technical_total)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    student_id,
                    final_score,
                    placement_status,
                    technical_score,
                    technical_correct,
                    technical_total
                ))
            conn.commit()
            cursor.close()
            conn.close()
        except Error as err:
            print(f"[Prediction DB Error] {err}")
            if conn and conn.is_connected():
                conn.close()

    session["prediction_score"] = final_score
    session["placement_status"] = placement_status

    return render_template(
        'prediction-result.html',
        prediction=final_score,
        placement_status=placement_status,
        semester=semester,
        sgpa=sgpa,
        prev_sem=prev_sem,
        cgpa=cgpa,
        backlogs=backlogs,
        internship=internship,
        projects=projects,
        extra_curr=extra_curr,
        certifications=certifications,
        aptitude=aptitude,
        communication_score=communication_score,
        technical_score=technical_score,
        technical_correct=technical_correct,
        technical_total=technical_total,
        suggestions=suggestions
    )


@app.route('/view_result')
def view_result():
    if "student_id" not in session:
        return redirect(url_for('login'))

    student_id = session["student_id"]
    conn = get_db_connection()

    prediction_data = None
    academic_data = None

    if conn:
        try:
            cursor = conn.cursor(buffered=True)
            cursor.execute("""
                SELECT prediction_score, placement_status, technical_score, technical_correct, technical_total, prediction_date
                FROM prediction_results
                WHERE student_id=%s
                ORDER BY prediction_date DESC LIMIT 1
            """, (student_id,))
            prediction_data = cursor.fetchone()

            cursor.execute("""
                SELECT semester, sgpa, prev_sem, cgpa, backlogs, internship,
                       projects, extra_curr, certifications, aptitude
                FROM academics
                WHERE student_id=%s
            """, (student_id,))
            academic_data = cursor.fetchone()

            cursor.execute("SELECT score FROM communication WHERE student_id=%s ORDER BY communication_id DESC LIMIT 1", (student_id,))
            comm_data = cursor.fetchone()
            comm_score = float(comm_data[0]) if comm_data else 0.0

            cursor.close()
            conn.close()
        except Error as err:
            print(f"[View Result Fetch Error] {err}")
            if conn and conn.is_connected():
                conn.close()

    if not prediction_data or not academic_data:
        return redirect(url_for('academics'))

    final_score = float(prediction_data[0])
    placement_status = prediction_data[1]
    technical_score = float(prediction_data[2]) if prediction_data[2] is not None else 0.0
    technical_correct = int(prediction_data[3]) if prediction_data[3] is not None else 0
    technical_total = int(prediction_data[4]) if prediction_data[4] is not None else 10

    semester = academic_data[0]
    sgpa = academic_data[1]
    prev_sem = academic_data[2]
    cgpa = academic_data[3]
    backlogs = academic_data[4]
    internship = academic_data[5]
    projects = academic_data[6]
    extra_curr = academic_data[7]
    certifications = academic_data[8]
    aptitude = academic_data[9]

    suggestions = generate_recommendations(
        backlogs, certifications, technical_score, projects,
        comm_score, aptitude, cgpa
    )

    return render_template(
        'prediction-result.html',
        prediction=final_score,
        placement_status=placement_status,
        semester=semester,
        sgpa=sgpa,
        prev_sem=prev_sem,
        cgpa=cgpa,
        backlogs=backlogs,
        internship=internship,
        projects=projects,
        extra_curr=extra_curr,
        certifications=certifications,
        aptitude=aptitude,
        communication_score=comm_score,
        technical_score=technical_score,
        technical_correct=technical_correct,
        technical_total=technical_total,
        suggestions=suggestions
    )

# ================= ADMIN ROUTES =================

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == "POST":
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        conn = get_db_connection()
        if not conn:
            flash("Database connection failed. Please check MySQL service.")
            return render_template('admin_login.html')

        try:
            cursor = conn.cursor(buffered=True)
            cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
            admin = cursor.fetchone()
            cursor.close()
            conn.close()

            if admin:
                session.pop("student_id", None)
                session["admin_id"] = admin[0]
                session["admin_username"] = admin[1]
                return redirect(url_for('admin_dashboard'))
            else:
                flash("Invalid Admin Username or Password.")
                return render_template('admin_login.html')
        except Error as err:
            if conn and conn.is_connected():
                conn.close()
            flash(f"Database error: {err}")
            return render_template('admin_login.html')

    return render_template('admin_login.html')


@app.route('/admin_dashboard')
def admin_dashboard():
    if "admin_id" not in session:
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    total_students = 0
    total_predictions = 0
    total_companies = 0
    total_questions = 0
    high_count = 0
    medium_count = 0
    low_count = 0

    if conn:
        try:
            cursor = conn.cursor(buffered=True)
            cursor.execute("SELECT COUNT(*) FROM students")
            total_students = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM prediction_results")
            total_predictions = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM companies")
            total_companies = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM company_technical_questions")
            total_questions = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM prediction_results WHERE placement_status='High Placement Readiness'")
            high_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM prediction_results WHERE placement_status='Medium Placement Readiness'")
            medium_count = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(*) FROM prediction_results
                WHERE placement_status='Low Placement Readiness' OR placement_status='Developing Placement Readiness'
            """)
            low_count = cursor.fetchone()[0]

            cursor.close()
            conn.close()
        except Error as err:
            print(f"[Admin Dashboard Error] {err}")
            if conn and conn.is_connected():
                conn.close()

    return render_template(
        'admin_dashboard.html',
        total_students=total_students,
        total_predictions=total_predictions,
        total_companies=total_companies,
        total_questions=total_questions,
        high_count=high_count,
        medium_count=medium_count,
        low_count=low_count
    )


@app.route('/admin_students')
def admin_students():
    if "admin_id" not in session:
        return redirect(url_for('admin_login'))

    students = []
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(buffered=True)
            cursor.execute("""
                SELECT student_id, fullname, register_number, department, email
                FROM students
                ORDER BY student_id DESC
            """)
            students = cursor.fetchall()
            cursor.close()
            conn.close()
        except Error as err:
            print(f"[Admin Students Error] {err}")
            if conn and conn.is_connected():
                conn.close()

    return render_template('admin_students.html', students=students)


@app.route('/admin_predictions')
def admin_predictions():
    if "admin_id" not in session:
        return redirect(url_for('admin_login'))

    predictions = []
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(buffered=True)
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
            cursor.close()
            conn.close()
        except Error as err:
            print(f"[Admin Predictions Error] {err}")
            if conn and conn.is_connected():
                conn.close()

    return render_template('admin_predictions.html', predictions=predictions)


@app.route('/admin_companies')
def admin_companies():
    """Admin company and practice questions management."""
    if "admin_id" not in session:
        return redirect(url_for('admin_login'))

    companies = []
    questions = []
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(buffered=True)
            cursor.execute("SELECT company_id, company_name, description, active FROM companies ORDER BY company_name ASC")
            companies = cursor.fetchall()

            cursor.execute("""
                SELECT q.question_id, q.category, q.question_type, q.question, q.difficulty, q.active, c.company_name
                FROM company_technical_questions q
                LEFT JOIN companies c ON q.company_id = c.company_id
                ORDER BY q.question_id DESC
            """)
            questions = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"[Admin Companies Error] {e}")
            if conn and conn.is_connected():
                conn.close()

    return render_template(
        'admin_companies.html',
        companies=companies,
        questions=questions
    )


@app.route('/admin_add_company', methods=['POST'])
def admin_add_company():
    """Add new target company to database."""
    if "admin_id" not in session:
        return redirect(url_for('admin_login'))

    company_name = request.form.get('company_name', '').strip()
    description = request.form.get('description', '').strip()

    if company_name:
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor(buffered=True)
                cursor.execute(
                    "INSERT INTO companies (company_name, description, active) VALUES (%s, %s, 1)",
                    (company_name, description)
                )
                conn.commit()
                cursor.close()
                conn.close()
                flash(f"Company '{company_name}' successfully added!")
            except Exception as e:
                print(f"[Add Company Error] {e}")
                if conn and conn.is_connected():
                    conn.close()
                flash(f"Could not add company: {e}")

    return redirect(url_for('admin_companies'))


@app.route('/admin_add_question', methods=['POST'])
def admin_add_question():
    """Add new technical practice question to database."""
    if "admin_id" not in session:
        return redirect(url_for('admin_login'))

    company_id = int(request.form.get('company_id', 0) or 0)
    category = request.form.get('category', 'Programming').strip()
    question_type = request.form.get('question_type', 'mcq').strip()
    question = request.form.get('question', '').strip()
    code_snippet = request.form.get('code_snippet', '').strip()
    option_a = request.form.get('option_a', '').strip()
    option_b = request.form.get('option_b', '').strip()
    option_c = request.form.get('option_c', '').strip()
    option_d = request.form.get('option_d', '').strip()
    correct_answer = request.form.get('correct_answer', '').strip()
    expected_output = request.form.get('expected_output', '').strip()
    explanation = request.form.get('explanation', '').strip()
    difficulty = request.form.get('difficulty', 'Medium').strip()

    if question:
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor(buffered=True)
                cursor.execute("""
                    INSERT INTO company_technical_questions
                    (company_id, category, question_type, question, code_snippet,
                     option_a, option_b, option_c, option_d, correct_answer, expected_output,
                     explanation, difficulty, active)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
                """, (
                    company_id, category, question_type, question, code_snippet,
                    option_a, option_b, option_c, option_d, correct_answer, expected_output,
                    explanation, difficulty
                ))
                conn.commit()
                cursor.close()
                conn.close()
                flash("Question successfully added to question pool!")
            except Exception as e:
                print(f"[Add Question Error] {e}")
                if conn and conn.is_connected():
                    conn.close()
                flash(f"Could not add question: {e}")

    return redirect(url_for('admin_companies'))


@app.route('/admin_toggle_question/<int:question_id>')
def admin_toggle_question(question_id):
    """Toggle active status of a practice question."""
    if "admin_id" not in session:
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(buffered=True)
            cursor.execute("UPDATE company_technical_questions SET active = 1 - active WHERE question_id=%s", (question_id,))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"[Toggle Question Error] {e}")
            if conn and conn.is_connected():
                conn.close()

    return redirect(url_for('admin_companies'))


@app.route('/admin_logout')
def admin_logout():
    session.pop("admin_id", None)
    session.pop("admin_username", None)
    return redirect(url_for('admin_login'))

# ================= APPLICATION ENTRY POINT =================

if __name__ == '__main__':
    app.run(debug=True)
