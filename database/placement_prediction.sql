-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 20, 2026 at 12:26 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `placement_prediction`
--

-- --------------------------------------------------------

--
-- Table structure for table `academics`
--

CREATE TABLE `academics` (
  `academic_id` int(11) NOT NULL,
  `student_id` int(11) DEFAULT NULL,
  `cgpa` float DEFAULT NULL,
  `backlogs` int(11) DEFAULT NULL,
  `internship` varchar(10) DEFAULT NULL,
  `projects` int(11) DEFAULT NULL,
  `certifications` int(11) DEFAULT NULL,
  `aptitude` int(11) DEFAULT NULL,
  `skills` text DEFAULT NULL,
  `prev_sem` int(11) DEFAULT NULL,
  `extra_curr` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `academics`
--

INSERT INTO `academics` (`academic_id`, `student_id`, `cgpa`, `backlogs`, `internship`, `projects`, `certifications`, `aptitude`, `skills`, `prev_sem`, `extra_curr`) VALUES
(1, 1, 8.41, 0, 'Yes', 3, 4, 60, 'python,java,mysql,html', NULL, NULL),
(2, 1, 8.4, 0, 'Yes', 3, 5, 45, 'python,java,html,css\r\n', NULL, NULL),
(3, 1, 9.5, 0, 'Yes', 4, 4, 56, 'python,java,\r\n', NULL, NULL),
(4, 1, 6.7, 1, 'Yes', 5, 2, 73, 'python\r\n', 7, 3);

-- --------------------------------------------------------

--
-- Table structure for table `communication`
--

CREATE TABLE `communication` (
  `communication_id` int(11) NOT NULL,
  `student_id` int(11) DEFAULT NULL,
  `score` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `communication`
--

INSERT INTO `communication` (`communication_id`, `student_id`, `score`) VALUES
(1, 1, 85.71),
(2, 1, 50),
(3, 1, 65),
(4, 1, 75),
(5, 1, 65);

-- --------------------------------------------------------

--
-- Table structure for table `communication_questions`
--

CREATE TABLE `communication_questions` (
  `question_id` int(11) NOT NULL,
  `question` text DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `option_a` varchar(255) DEFAULT NULL,
  `option_b` varchar(255) DEFAULT NULL,
  `option_c` varchar(255) DEFAULT NULL,
  `option_d` varchar(255) DEFAULT NULL,
  `correct_option` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `communication_questions`
--

INSERT INTO `communication_questions` (`question_id`, `question`, `category`, `option_a`, `option_b`, `option_c`, `option_d`, `correct_option`) VALUES
(1, 'Choose the correct sentence', 'Grammar', 'She go to college daily', 'She goes to college daily', 'She going college daily', 'She gone college daily', 'B'),
(2, 'Choose the correct past tense of go', 'Grammar', 'goed', 'going', 'went', 'gone', 'C'),
(3, 'Select the correct article: He is ___ engineer', 'Grammar', 'a', 'an', 'the', 'no article', 'B'),
(4, 'Choose the plural form of mouse', 'Grammar', 'mouses', 'mice', 'mouseses', 'mices', 'B'),
(5, 'Choose the correct sentence', 'Grammar', 'They was happy', 'They were happy', 'They is happy', 'They be happy', 'B'),
(6, 'Fill the blank: She is interested ___ music', 'Grammar', 'on', 'at', 'in', 'for', 'C'),
(7, 'Choose the correct form: He ___ football every evening', 'Grammar', 'play', 'plays', 'playing', 'played', 'B'),
(8, 'Choose the correct sentence', 'Grammar', 'I have finished my work', 'I has finished my work', 'I finishing my work', 'I finish have work', 'A'),
(9, 'Choose the correct pronoun', 'Grammar', 'Me and John went there', 'John and I went there', 'John and me went there', 'I and John goes there', 'B'),
(10, 'Comparative form of bad is', 'Grammar', 'badder', 'worse', 'worstest', 'more bad', 'B'),
(11, 'Choose correct sentence', 'Grammar', 'He can sings well', 'He can sing well', 'He can singing well', 'He can sang well', 'B'),
(12, 'Passive voice of \"They completed the project\"', 'Grammar', 'The project was completed by them', 'The project completed them', 'The project is completing', 'They was completed project', 'A'),
(13, 'Choose correct conjunction: I stayed home ___ I was sick', 'Grammar', 'or', 'because', 'but', 'so', 'B'),
(14, 'Choose the correct spelling', 'Grammar', 'Accomodation', 'Accommodation', 'Acommodation', 'Accomadation', 'B'),
(15, 'Choose the correct sentence', 'Grammar', 'Neither Ram nor Ravi are coming', 'Neither Ram nor Ravi is coming', 'Neither Ram nor Ravi coming', 'Neither Ram nor Ravi be coming', 'B'),
(16, 'Present continuous form of run', 'Grammar', 'run', 'runs', 'is running', 'ran', 'C'),
(17, 'Choose correct sentence', 'Grammar', 'I am good at programming', 'I am good in programming', 'I good at programming', 'I am goodness programming', 'A'),
(18, 'Choose correct form', 'Grammar', 'They has completed', 'They have completed', 'They completed have', 'They having completed', 'B'),
(19, 'Choose correct sentence', 'Grammar', 'Your welcome', 'You are welcome', 'You welcome', 'Welcome you are', 'B'),
(20, 'Choose correct sentence', 'Grammar', 'The news are interesting', 'The news is interesting', 'The news were interesting', 'News are is interesting', 'B'),
(21, 'Choose the synonym of happy', 'Vocabulary', 'Sad', 'Joyful', 'Angry', 'Weak', 'B'),
(22, 'Choose the antonym of strong', 'Vocabulary', 'Powerful', 'Weak', 'Active', 'Brave', 'B'),
(23, 'What is the meaning of confident?', 'Vocabulary', 'Feeling sure about yourself', 'Feeling afraid', 'Feeling tired', 'Feeling confused', 'A'),
(24, 'Choose the synonym of intelligent', 'Vocabulary', 'Smart', 'Lazy', 'Slow', 'Careless', 'A'),
(25, 'Choose the antonym of success', 'Vocabulary', 'Achievement', 'Failure', 'Victory', 'Growth', 'B'),
(26, 'Choose the correct meaning of opportunity', 'Vocabulary', 'A difficult problem', 'A chance to do something', 'A punishment', 'A mistake', 'B'),
(27, 'Choose the synonym of important', 'Vocabulary', 'Necessary', 'Small', 'Weak', 'Simple', 'A'),
(28, 'Choose the antonym of ancient', 'Vocabulary', 'Old', 'Modern', 'Historic', 'Traditional', 'B'),
(29, 'Choose the synonym of quick', 'Vocabulary', 'Fast', 'Late', 'Slow', 'Weak', 'A'),
(30, 'Choose the antonym of honest', 'Vocabulary', 'Truthful', 'Kind', 'Dishonest', 'Helpful', 'C'),
(31, 'What does \"innovative\" mean?', 'Vocabulary', 'Creative and new', 'Old fashioned', 'Unclear', 'Impossible', 'A'),
(32, 'Choose the synonym of improve', 'Vocabulary', 'Develop', 'Reduce', 'Destroy', 'Stop', 'A'),
(33, 'Choose the antonym of increase', 'Vocabulary', 'Grow', 'Expand', 'Decrease', 'Improve', 'C'),
(34, 'Choose the meaning of reliable', 'Vocabulary', 'Can be trusted', 'Cannot be used', 'Very expensive', 'Very small', 'A'),
(35, 'Choose the synonym of difficult', 'Vocabulary', 'Easy', 'Hard', 'Simple', 'Clear', 'B'),
(36, 'Choose the antonym of accept', 'Vocabulary', 'Receive', 'Reject', 'Allow', 'Approve', 'B'),
(37, 'Choose the synonym of communicate', 'Vocabulary', 'Share information', 'Hide information', 'Forget information', 'Remove information', 'A'),
(38, 'Choose the meaning of professional', 'Vocabulary', 'Showing skill and proper behavior', 'Being careless', 'Being lazy', 'Being rude', 'A'),
(39, 'Choose the antonym of positive', 'Vocabulary', 'Good', 'Negative', 'Strong', 'Active', 'B'),
(40, 'Choose the synonym of prepare', 'Vocabulary', 'Plan', 'Ignore', 'Destroy', 'Forget', 'A'),
(41, 'Read: \"Riya studies every evening because she wants to score high marks.\" Why does Riya study every evening?', 'Reading Comprehension', 'She wants to score high marks', 'She dislikes studying', 'She has no classes', 'She wants to waste time', 'A'),
(42, 'Read: \"Technology has changed the way people communicate. Emails and video calls help people connect quickly.\" What helps people connect quickly?', 'Reading Comprehension', 'Books', 'Technology', 'Games', 'Travel', 'B'),
(43, 'Read: \"The company introduced a training program to improve employee skills.\" Why was the training program introduced?', 'Reading Comprehension', 'To reduce work', 'To improve skills', 'To close the company', 'To hire students', 'B'),
(44, 'Read: \"A healthy lifestyle includes regular exercise and balanced food.\" What is included in a healthy lifestyle?', 'Reading Comprehension', 'Only sleeping', 'Exercise and balanced food', 'Eating junk food', 'Avoiding activities', 'B'),
(45, 'Read: \"Rahul completed his project before the deadline. His manager appreciated his dedication.\" Why did the manager appreciate Rahul?', 'Reading Comprehension', 'He completed work early', 'He missed the deadline', 'He left the project', 'He avoided work', 'A'),
(46, 'Read: \"Online learning allows students to attend classes from anywhere.\" What is the advantage of online learning?', 'Reading Comprehension', 'Students cannot study', 'Students can learn from anywhere', 'Students need no teachers', 'Students stop learning', 'B'),
(47, 'Read: \"The library provides students with many books and digital resources.\" What does the library provide?', 'Reading Comprehension', 'Only games', 'Books and digital resources', 'Food items', 'Transportation', 'B'),
(48, 'Read: \"Good communication skills help employees work effectively in teams.\" What helps employees work effectively?', 'Reading Comprehension', 'Poor attitude', 'Good communication skills', 'Less teamwork', 'Avoiding people', 'B'),
(49, 'Read: \"An internship gives students practical experience related to their field.\" What does an internship provide?', 'Reading Comprehension', 'Entertainment', 'Practical experience', 'Holiday time', 'Only certificates', 'B'),
(50, 'Read: \"The student prepared well for the interview and answered confidently.\" Why did the student answer confidently?', 'Reading Comprehension', 'Because of preparation', 'Because of luck', 'Because of avoiding questions', 'Because of no practice', 'A'),
(51, 'Read: \"Artificial Intelligence helps computers perform tasks that normally require human intelligence.\" What does AI help computers do?', 'Reading Comprehension', 'Perform intelligent tasks', 'Stop working', 'Avoid information', 'Delete data', 'A'),
(52, 'Read: \"Teamwork is important because people can combine their skills to achieve goals.\" Why is teamwork important?', 'Reading Comprehension', 'People combine skills', 'People work alone', 'Goals are removed', 'Skills decrease', 'A'),
(53, 'Read: \"Time management helps students complete tasks within a specific period.\" What does time management help with?', 'Reading Comprehension', 'Completing tasks on time', 'Ignoring tasks', 'Delaying work', 'Avoiding schedules', 'A'),
(54, 'Read: \"A resume contains information about education, skills, and experience.\" What does a resume contain?', 'Reading Comprehension', 'Personal hobbies only', 'Education and skills', 'Bank details', 'Travel history', 'B'),
(55, 'Read: \"The internet provides access to information from around the world.\" What does the internet provide?', 'Reading Comprehension', 'Access to information', 'Only entertainment', 'No resources', 'Limited communication', 'A'),
(56, 'Read: \"The manager encouraged employees to share their ideas during meetings.\" What did the manager encourage?', 'Reading Comprehension', 'Sharing ideas', 'Skipping meetings', 'Avoiding discussions', 'Ignoring employees', 'A'),
(57, 'Read: \"Continuous learning helps professionals adapt to new technologies.\" Why is continuous learning important?', 'Reading Comprehension', 'To adapt to changes', 'To stop improvement', 'To avoid skills', 'To reduce knowledge', 'A'),
(58, 'Read: \"The placement training program focuses on aptitude, technical skills, and interviews.\" What does the program focus on?', 'Reading Comprehension', 'Only sports', 'Aptitude and skills', 'Only attendance', 'Only exams', 'B'),
(59, 'Read: \"Communication barriers can create misunderstandings between people.\" What can communication barriers create?', 'Reading Comprehension', 'Better understanding', 'Misunderstandings', 'Strong relationships', 'More confidence', 'B'),
(60, 'Read: \"Successful students maintain discipline and consistency in their studies.\" What do successful students maintain?', 'Reading Comprehension', 'Discipline and consistency', 'Carelessness', 'Irregular habits', 'Lack of planning', 'A'),
(61, 'What is important during a professional interview?', 'Professional Communication', 'Being prepared', 'Ignoring questions', 'Speaking without thinking', 'Arriving late', 'A'),
(62, 'Which is the best way to start a formal email?', 'Professional Communication', 'Hey friend', 'Dear Sir/Madam', 'Hi buddy', 'Hello dude', 'B'),
(63, 'Good communication in a workplace helps to:', 'Professional Communication', 'Create misunderstandings', 'Improve teamwork', 'Avoid all people', 'Reduce productivity', 'B'),
(64, 'During an interview, you should maintain:', 'Professional Communication', 'Eye contact', 'Silence', 'Negative attitude', 'Disinterest', 'A'),
(65, 'What should you do before attending an interview?', 'Professional Communication', 'Research about the company', 'Ignore company details', 'Avoid preparation', 'Arrive without knowledge', 'A'),
(66, 'Active listening means:', 'Professional Communication', 'Paying attention while someone speaks', 'Interrupting frequently', 'Ignoring the speaker', 'Changing topics', 'A'),
(67, 'A professional email should be:', 'Professional Communication', 'Clear and polite', 'Very informal', 'Full of mistakes', 'Without a subject', 'A'),
(68, 'What is the purpose of a resume?', 'Professional Communication', 'To present qualifications', 'To write stories', 'To share jokes', 'To list hobbies only', 'A'),
(69, 'During a presentation, you should:', 'Professional Communication', 'Speak clearly', 'Read without understanding', 'Avoid the audience', 'Speak very quietly', 'A'),
(70, 'Teamwork requires:', 'Professional Communication', 'Cooperation', 'Competition only', 'Ignoring others', 'Lack of communication', 'A'),
(71, 'What should you do when you disagree with a teammate?', 'Professional Communication', 'Discuss respectfully', 'Argue loudly', 'Ignore the person', 'Leave the team', 'A'),
(72, 'Body language includes:', 'Professional Communication', 'Facial expressions and gestures', 'Only writing', 'Only typing', 'Only reading', 'A'),
(73, 'Professional behavior includes:', 'Professional Communication', 'Respect and responsibility', 'Being careless', 'Ignoring rules', 'Arriving late', 'A'),
(74, 'What should you avoid during an interview?', 'Professional Communication', 'Negative comments about previous organizations', 'Confidence', 'Proper dressing', 'Eye contact', 'A'),
(75, 'Communication skills are important because they:', 'Professional Communication', 'Help express ideas clearly', 'Prevent teamwork', 'Reduce understanding', 'Create confusion', 'A'),
(76, 'When speaking in a meeting, you should:', 'Professional Communication', 'Share relevant ideas', 'Interrupt everyone', 'Ignore the topic', 'Speak randomly', 'A'),
(77, 'A good leader should:', 'Professional Communication', 'Listen to team members', 'Ignore suggestions', 'Avoid responsibility', 'Discourage teamwork', 'A'),
(78, 'What is the correct interview dress style?', 'Professional Communication', 'Formal and neat', 'Very casual', 'Untidy clothes', 'Unprofessional style', 'A'),
(79, 'Feedback should be:', 'Professional Communication', 'Constructive', 'Insulting', 'Negative always', 'Ignored', 'A'),
(80, 'Professional communication should be:', 'Professional Communication', 'Respectful and effective', 'Confusing', 'Careless', 'Unclear', 'A'),
(81, 'You are unable to complete a task before the deadline. What should you do?', 'Situational Communication', 'Inform your manager early and explain the situation', 'Ignore the deadline', 'Blame someone else', 'Stop working', 'A'),
(82, 'A team member makes a mistake. What is the best response?', 'Situational Communication', 'Help them correct it politely', 'Criticize them publicly', 'Ignore the problem', 'Report immediately without discussion', 'A'),
(83, 'During an interview, you do not know an answer. What should you do?', 'Situational Communication', 'Admit it politely and explain your approach', 'Give a random wrong answer', 'Remain silent', 'Leave the interview', 'A'),
(84, 'A colleague disagrees with your idea. You should:', 'Situational Communication', 'Listen and discuss the idea', 'Argue immediately', 'Ignore the colleague', 'End the conversation', 'A'),
(85, 'You receive negative feedback from your supervisor. What should you do?', 'Situational Communication', 'Accept it and improve', 'Become angry', 'Ignore the feedback', 'Blame others', 'A'),
(86, 'You need information from another department. What is the best approach?', 'Situational Communication', 'Communicate politely and request information', 'Send rude messages', 'Wait without asking', 'Ignore the requirement', 'A'),
(87, 'You are late for an important meeting. What should you do?', 'Situational Communication', 'Inform the team and apologize', 'Enter without explanation', 'Ignore everyone', 'Cancel your work', 'A'),
(88, 'A customer is unhappy with a service. What should you do?', 'Situational Communication', 'Listen and try to solve the issue', 'Argue with the customer', 'Ignore the complaint', 'End communication', 'A'),
(89, 'You have multiple tasks with the same deadline. What should you do?', 'Situational Communication', 'Prioritize and manage tasks', 'Ignore all tasks', 'Complete randomly', 'Delay everything', 'A'),
(90, 'Your teammate is not participating in a project. What should you do?', 'Situational Communication', 'Discuss the issue with them', 'Remove them immediately', 'Ignore the situation', 'Complain publicly', 'A'),
(91, 'You are asked to lead a team project. What should you do first?', 'Situational Communication', 'Understand goals and assign responsibilities', 'Start without planning', 'Avoid communication', 'Work alone', 'A'),
(92, 'You made an error in your work. What should you do?', 'Situational Communication', 'Accept and correct the mistake', 'Hide the mistake', 'Blame others', 'Ignore it', 'A'),
(93, 'During a presentation, someone asks a difficult question. You should:', 'Situational Communication', 'Answer calmly or explain honestly', 'Become nervous and stop', 'Ignore the person', 'Argue with them', 'A'),
(94, 'Your teammate has a different opinion. You should:', 'Situational Communication', 'Respectfully discuss both opinions', 'Reject immediately', 'Stop communication', 'Create conflict', 'A'),
(95, 'You are given a new technology task you do not know. What should you do?', 'Situational Communication', 'Learn and ask for guidance', 'Refuse immediately', 'Ignore the task', 'Complain', 'A'),
(96, 'You notice a problem in a project. What is the best action?', 'Situational Communication', 'Report and suggest solutions', 'Hide the problem', 'Wait until failure', 'Ignore it', 'A'),
(97, 'You have to work with a difficult teammate. You should:', 'Situational Communication', 'Maintain professionalism', 'Fight with them', 'Avoid all communication', 'Create more problems', 'A'),
(98, 'You receive an important email. What should you do?', 'Situational Communication', 'Read carefully and respond appropriately', 'Delete it', 'Ignore it', 'Forward without reading', 'A'),
(99, 'You are asked to complete an unfamiliar task. What should you do?', 'Situational Communication', 'Understand the requirement and learn', 'Refuse without reason', 'Avoid responsibility', 'Leave the task', 'A'),
(100, 'During teamwork, the best approach is:', 'Situational Communication', 'Cooperate and communicate', 'Work separately without discussion', 'Compete with teammates', 'Ignore team members', 'A');

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `student_id` int(11) NOT NULL,
  `fullname` varchar(100) DEFAULT NULL,
  `register_number` varchar(50) DEFAULT NULL,
  `department` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`student_id`, `fullname`, `register_number`, `department`, `email`, `password`) VALUES
(1, 'Pallavikrishna.B', 'kte25mca-2042', 'MCA', 'pallavi@gmail.com', '25mp2470');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `academics`
--
ALTER TABLE `academics`
  ADD PRIMARY KEY (`academic_id`),
  ADD KEY `student_id` (`student_id`);

--
-- Indexes for table `communication`
--
ALTER TABLE `communication`
  ADD PRIMARY KEY (`communication_id`),
  ADD KEY `student_id` (`student_id`);

--
-- Indexes for table `communication_questions`
--
ALTER TABLE `communication_questions`
  ADD PRIMARY KEY (`question_id`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`student_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `academics`
--
ALTER TABLE `academics`
  MODIFY `academic_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `communication`
--
ALTER TABLE `communication`
  MODIFY `communication_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `communication_questions`
--
ALTER TABLE `communication_questions`
  MODIFY `question_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=101;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `student_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `academics`
--
ALTER TABLE `academics`
  ADD CONSTRAINT `academics_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`);

--
-- Constraints for table `communication`
--
ALTER TABLE `communication`
  ADD CONSTRAINT `communication_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
