-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 07, 2026 at 04:38 PM
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
-- Table structure for table `technical_questions`
--

CREATE TABLE `technical_questions` (
  `question_id` int(11) NOT NULL,
  `category` varchar(100) NOT NULL,
  `question` text NOT NULL,
  `option_a` varchar(255) NOT NULL,
  `option_b` varchar(255) NOT NULL,
  `option_c` varchar(255) NOT NULL,
  `option_d` varchar(255) NOT NULL,
  `correct_option` char(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `technical_questions`
--

INSERT INTO `technical_questions` (`question_id`, `category`, `question`, `option_a`, `option_b`, `option_c`, `option_d`, `correct_option`) VALUES
(1, 'Basic Programming', 'Which data structure follows the LIFO principle?', 'Queue', 'Stack', 'Array', 'Linked List', 'B'),
(2, 'Basic Programming', 'Which of the following is a programming language?', 'HTML', 'CSS', 'Python', 'SQL', 'C'),
(3, 'Basic Programming', 'What is the purpose of a loop?', 'To store data', 'To repeat a block of code', 'To create a database', 'To display images', 'B'),
(4, 'Basic Programming', 'Which data structure follows the FIFO principle?', 'Stack', 'Queue', 'Tree', 'Graph', 'B'),
(5, 'Python', 'Which keyword is used to define a function in Python?', 'function', 'define', 'def', 'fun', 'C'),
(6, 'Python', 'Which of the following is a mutable data type in Python?', 'Tuple', 'String', 'List', 'Integer', 'C'),
(7, 'Python', 'What is the output of len([10, 20, 30])?', '2', '3', '4', '0', 'B'),
(8, 'Python', 'Which symbol is used for a single-line comment in Python?', '//', '#', '/* */', '--', 'B'),
(9, 'Java', 'Which keyword is used to create a class in Java?', 'class', 'Class', 'new', 'define', 'A'),
(10, 'Java', 'Which method is the entry point of a Java program?', 'start()', 'run()', 'main()', 'execute()', 'C'),
(11, 'Java', 'Which feature allows the same method name with different parameters?', 'Inheritance', 'Encapsulation', 'Method Overloading', 'Abstraction', 'C'),
(12, 'Java', 'Which keyword is used to create an object in Java?', 'object', 'create', 'new', 'this', 'C'),
(13, 'C++', 'Which symbol is used to end a statement in C++?', ':', ';', '.', ',', 'B'),
(14, 'C++', 'Which keyword is used for dynamic memory allocation?', 'malloc', 'new', 'create', 'alloc', 'B'),
(15, 'C++', 'Which concept allows a class to inherit properties from another class?', 'Polymorphism', 'Inheritance', 'Encapsulation', 'Compilation', 'B'),
(16, 'C++', 'Which header file is commonly used for input and output in C++?', '<stdio.h>', '<iostream>', '<string.h>', '<input.h>', 'B'),
(17, 'JavaScript', 'Which keyword declares a variable that cannot be reassigned?', 'var', 'let', 'const', 'static', 'C'),
(18, 'JavaScript', 'Which operator is used for strict equality?', '=', '==', '===', '!=', 'C'),
(19, 'JavaScript', 'Which function displays a message in the browser console?', 'print()', 'console.log()', 'display()', 'show()', 'B'),
(20, 'JavaScript', 'Which keyword is used to declare a block-scoped variable?', 'var', 'let', 'define', 'variable', 'B'),
(21, 'SQL', 'Which SQL command retrieves data from a table?', 'GET', 'SELECT', 'FETCH', 'READ', 'B'),
(22, 'SQL', 'Which command adds a new record to a table?', 'ADD', 'INSERT', 'UPDATE', 'CREATE', 'B'),
(23, 'SQL', 'Which clause is used to filter records in SQL?', 'ORDER BY', 'GROUP BY', 'WHERE', 'FILTER', 'C'),
(24, 'SQL', 'Which command is used to modify existing records?', 'CHANGE', 'UPDATE', 'MODIFY', 'ALTER', 'B'),
(25, 'HTML', 'What does HTML stand for?', 'Hyper Text Markup Language', 'High Text Machine Language', 'Hyperlink Text Management Language', 'Home Tool Markup Language', 'A'),
(26, 'HTML', 'Which HTML tag is used to create a hyperlink?', '<link>', '<a>', '<href>', '<url>', 'B'),
(27, 'HTML', 'Which tag is used to create a paragraph?', '<p>', '<para>', '<text>', '<paragraph>', 'A'),
(28, 'HTML', 'Which tag is used to display an image?', '<image>', '<img>', '<picture>', '<src>', 'B'),
(29, 'CSS', 'What does CSS stand for?', 'Computer Style Sheets', 'Cascading Style Sheets', 'Creative Style System', 'Colorful Style Sheets', 'B'),
(30, 'CSS', 'Which CSS property is used to change text color?', 'font-color', 'text-color', 'color', 'foreground', 'C'),
(31, 'CSS', 'Which property is used to change the background color?', 'background-color', 'bg-color', 'color-background', 'background', 'A'),
(32, 'CSS', 'Which CSS property is used to change the font size?', 'font-style', 'text-size', 'font-size', 'size', 'C'),
(33, 'Data Structures', 'Which data structure consists of nodes connected by edges?', 'Array', 'Stack', 'Graph', 'Queue', 'C'),
(34, 'Data Structures', 'Which data structure is commonly used for hierarchical data?', 'Array', 'Tree', 'Stack', 'Queue', 'B'),
(35, 'Data Structures', 'Which data structure allows insertion and deletion from both ends?', 'Stack', 'Deque', 'Tree', 'Graph', 'B'),
(36, 'Data Structures', 'Which data structure stores elements in contiguous memory locations?', 'Linked List', 'Array', 'Graph', 'Tree', 'B'),
(37, 'Database', 'Which key uniquely identifies a record in a table?', 'Foreign Key', 'Primary Key', 'Candidate Key', 'Secondary Key', 'B'),
(38, 'Database', 'Which key is used to establish a relationship between two tables?', 'Primary Key', 'Foreign Key', 'Super Key', 'Unique Key', 'B'),
(39, 'Database', 'Which database system are you using for this project?', 'MongoDB', 'MySQL', 'Oracle', 'SQLite', 'B'),
(40, 'Database', 'Which command is used to remove a table from a database?', 'DELETE TABLE', 'REMOVE TABLE', 'DROP TABLE', 'CLEAR TABLE', 'C'),
(41, 'Basic Programming', 'Which symbol is commonly used to assign a value to a variable?', '=', '==', '!=', '>=', 'A'),
(42, 'Basic Programming', 'Which data type is commonly used to store whole numbers?', 'float', 'int', 'char', 'string', 'B'),
(43, 'Basic Programming', 'Which data type is commonly used to store decimal numbers?', 'int', 'char', 'float', 'boolean', 'C'),
(44, 'Basic Programming', 'Which statement is used to make a decision in a program?', 'if', 'print', 'input', 'import', 'A'),
(45, 'Basic Programming', 'Which loop is generally used when the number of iterations is known?', 'while loop', 'for loop', 'do-while loop', 'infinite loop', 'B'),
(46, 'Basic Programming', 'Which loop continues executing while a condition is true?', 'for loop', 'while loop', 'switch', 'if statement', 'B'),
(47, 'Basic Programming', 'What is the first index of an array in most programming languages such as C, C++, Java and Python?', '0', '1', '-1', '2', 'A'),
(48, 'Basic Programming', 'What is a variable?', 'A fixed value', 'A named storage location for data', 'A programming language', 'A type of loop', 'B'),
(49, 'Basic Programming', 'Which operator is commonly used for addition?', '*', '-', '+', '/', 'C'),
(50, 'Basic Programming', 'Which operator is commonly used for multiplication?', '+', '*', '%', '=', 'B'),
(51, 'Basic Programming', 'Which operator returns the remainder after division?', '/', '//', '%', '**', 'C'),
(52, 'Basic Programming', 'Which logical operator represents AND?', '||', '!', '&&', '%', 'C'),
(53, 'Basic Programming', 'Which logical operator represents OR in many programming languages?', '&&', '||', '!', '==', 'B'),
(54, 'Basic Programming', 'Which keyword is commonly used to return a value from a function?', 'break', 'continue', 'return', 'stop', 'C'),
(55, 'Basic Programming', 'What is a function?', 'A reusable block of code that performs a task', 'A type of variable', 'A database', 'An operating system', 'A'),
(56, 'Basic Programming', 'What does a compiler do?', 'Runs only web pages', 'Converts source code into machine or target code', 'Stores data permanently', 'Creates hardware', 'B'),
(57, 'Basic Programming', 'What is debugging?', 'Writing comments', 'Finding and fixing errors in a program', 'Creating variables', 'Installing software', 'B'),
(58, 'Basic Programming', 'Which error occurs when a program violates the rules of a programming language?', 'Logical error', 'Runtime error', 'Syntax error', 'Network error', 'C'),
(59, 'Basic Programming', 'What is an infinite loop?', 'A loop that executes only once', 'A loop that never terminates under its current condition', 'A loop that contains no condition', 'A loop used only for arrays', 'B'),
(60, 'Basic Programming', 'Which statement is commonly used to exit a loop immediately?', 'continue', 'break', 'return_type', 'case', 'B'),
(61, 'Basic Programming', 'Which statement skips the current iteration of a loop and proceeds to the next iteration?', 'break', 'exit', 'continue', 'stop', 'C'),
(62, 'C++', 'Which keyword is used to define a class in C++?', 'struct', 'class', 'object', 'define', 'B'),
(63, 'C++', 'Which function is the entry point of a C++ program?', 'start()', 'begin()', 'main()', 'run()', 'C'),
(64, 'C++', 'Which header file is commonly used for input and output in C++?', '<stdio.h>', '<iostream>', '<string.h>', '<stdlib.h>', 'B'),
(65, 'C++', 'Which operator is used with cout for output?', '>>', '<<', '==', '&&', 'B'),
(66, 'C++', 'Which operator is used with cin for input?', '<<', '>>', '==', '++', 'B'),
(67, 'C++', 'Which keyword is used to create an object dynamically?', 'create', 'new', 'malloc', 'object', 'B'),
(68, 'C++', 'Which keyword is used to release memory allocated using new?', 'delete', 'free', 'remove', 'destroy', 'A'),
(69, 'C++', 'Which feature allows multiple functions with the same name but different parameters?', 'Inheritance', 'Function overloading', 'Encapsulation', 'Abstraction', 'B'),
(70, 'C++', 'Which feature allows a derived class to use members of a base class?', 'Polymorphism', 'Inheritance', 'Overloading', 'Compilation', 'B'),
(71, 'C++', 'Which symbol is used to declare a pointer?', '&', '*', '#', '%', 'B'),
(72, 'C++', 'Which operator is used to obtain the address of a variable?', '*', '&', '->', '::', 'B'),
(73, 'C++', 'Which operator is used to access a member through an object?', '->', '.', '::', '&', 'B'),
(74, 'C++', 'Which operator is commonly used to access a member through a pointer to an object?', '.', '::', '->', '&', 'C'),
(75, 'C++', 'Which keyword is used to prevent a class from being inherited in modern C++?', 'static', 'final', 'sealed', 'private', 'B'),
(76, 'C++', 'Which concept allows the same function or operator to behave differently depending on its operands or context?', 'Polymorphism', 'Compilation', 'Encapsulation', 'Namespace', 'A'),
(77, 'C++', 'Which keyword is used to define a constant variable in C++?', 'constant', 'const', 'fixed', 'readonly', 'B'),
(78, 'C++', 'What is a constructor in C++?', 'A function used to destroy an object', 'A special member function used to initialize objects', 'A function used only for input', 'A global variable', 'B'),
(79, 'C++', 'What is a destructor in C++?', 'A special member function called when an object is destroyed', 'A function used to create an object', 'A function used for inheritance', 'A function used to allocate memory', 'A'),
(80, 'C++', 'Which keyword is used to define a namespace?', 'package', 'namespace', 'module', 'group', 'B'),
(81, 'C++', 'Which standard container stores elements in a dynamic array-like structure?', 'vector', 'stack', 'queue', 'map', 'A'),
(82, 'C++', 'Which C++ container follows the Last In First Out principle?', 'queue', 'vector', 'stack', 'list', 'C'),
(83, 'CSS', 'What does CSS stand for?', 'Cascading Style Sheets', 'Computer Style Sheets', 'Creative Style System', 'Colorful Style Sheets', 'A'),
(84, 'CSS', 'Which HTML tag is used to link an external CSS file?', '<style>', '<css>', '<link>', '<script>', 'C'),
(85, 'CSS', 'Which CSS property is used to change text color?', 'font-color', 'text-color', 'color', 'foreground', 'C'),
(86, 'CSS', 'Which property is used to change the background color of an element?', 'background-color', 'bg-color', 'color-background', 'background-style', 'A'),
(87, 'CSS', 'Which property is used to change the font size?', 'text-size', 'font-size', 'font-style', 'text-font', 'B'),
(88, 'CSS', 'Which CSS property is used to make text bold?', 'font-weight', 'font-bold', 'text-weight', 'bold-text', 'A'),
(89, 'CSS', 'Which property is used to align text horizontally?', 'text-align', 'align-text', 'text-position', 'horizontal-align', 'A'),
(90, 'CSS', 'Which value of position keeps an element fixed relative to the browser window?', 'static', 'relative', 'absolute', 'fixed', 'D'),
(91, 'CSS', 'Which CSS property controls the space inside an element?', 'margin', 'padding', 'border', 'spacing', 'B'),
(92, 'CSS', 'Which CSS property controls the space outside an element?', 'padding', 'margin', 'border-spacing', 'outline', 'B'),
(93, 'CSS', 'Which property is used to create rounded corners?', 'corner-radius', 'border-radius', 'round-border', 'border-round', 'B'),
(94, 'CSS', 'Which property is used to add a shadow around an element?', 'element-shadow', 'box-shadow', 'border-shadow', 'shadow-box', 'B'),
(95, 'CSS', 'Which CSS layout system is designed for one-dimensional layouts?', 'Grid', 'Flexbox', 'Table', 'Float', 'B'),
(96, 'CSS', 'Which CSS layout system is designed for two-dimensional layouts?', 'Flexbox', 'Grid', 'Inline', 'Position', 'B'),
(97, 'CSS', 'Which property is used to set the width of an element?', 'element-width', 'width', 'size', 'box-width', 'B'),
(98, 'CSS', 'Which property is used to set the height of an element?', 'height', 'element-height', 'box-height', 'size-height', 'A'),
(99, 'CSS', 'Which selector is used to select an element with a specific id?', '.', '#', '*', '@', 'B'),
(100, 'CSS', 'Which selector is used to select elements belonging to a specific class?', '#', '.', '@', '&', 'B'),
(101, 'CSS', 'Which selector selects all elements on a page?', '#', '.', '*', 'all', 'C'),
(102, 'CSS', 'Which property controls the stacking order of positioned elements?', 'stack-order', 'z-index', 'layer', 'position-index', 'B'),
(103, 'CSS', 'Which CSS property is used to make an element invisible while still keeping its space?', 'display: none', 'visibility: hidden', 'opacity: 0 and display none', 'hide: true', 'B'),
(104, 'Data Structures', 'Which data structure follows the LIFO principle?', 'Queue', 'Stack', 'Array', 'Linked List', 'B'),
(105, 'Data Structures', 'Which data structure follows the FIFO principle?', 'Stack', 'Tree', 'Queue', 'Graph', 'C'),
(106, 'Data Structures', 'Which data structure consists of nodes connected using links?', 'Array', 'Linked List', 'Stack', 'Queue', 'B'),
(107, 'Data Structures', 'Which data structure is commonly used to implement recursion?', 'Queue', 'Stack', 'Array', 'Graph', 'B'),
(108, 'Data Structures', 'Which data structure is commonly used in Breadth First Search?', 'Stack', 'Queue', 'Tree', 'Heap', 'B'),
(109, 'Data Structures', 'Which data structure is commonly used in Depth First Search?', 'Queue', 'Stack', 'Array', 'Hash Table', 'B'),
(110, 'Data Structures', 'What is the average time complexity of searching for an element in a hash table?', 'O(n)', 'O(log n)', 'O(1)', 'O(n log n)', 'C'),
(111, 'Data Structures', 'Which data structure is used to represent hierarchical relationships?', 'Stack', 'Tree', 'Queue', 'Array', 'C'),
(112, 'Data Structures', 'Which tree has at most two children per node?', 'Binary Tree', 'AVL Tree', 'B-Tree', 'Heap', 'A'),
(113, 'Data Structures', 'In a Binary Search Tree, where are values smaller than the root generally stored?', 'Right subtree', 'Left subtree', 'Parent node', 'Leaf only', 'B'),
(114, 'Data Structures', 'Which traversal visits the root before its subtrees?', 'Inorder', 'Postorder', 'Preorder', 'Level order', 'C'),
(115, 'Data Structures', 'Which traversal visits the root between the left and right subtrees?', 'Preorder', 'Inorder', 'Postorder', 'Level order', 'B'),
(116, 'Data Structures', 'Which traversal visits the root after its subtrees?', 'Preorder', 'Inorder', 'Postorder', 'Level order', 'C'),
(117, 'Data Structures', 'Which data structure is commonly used to implement a priority queue?', 'Heap', 'Stack', 'Linked List only', 'Array only', 'A'),
(118, 'Data Structures', 'Which sorting algorithm repeatedly selects the smallest element from the unsorted portion?', 'Bubble Sort', 'Selection Sort', 'Merge Sort', 'Quick Sort', 'B'),
(119, 'Data Structures', 'Which sorting algorithm repeatedly compares adjacent elements?', 'Selection Sort', 'Bubble Sort', 'Merge Sort', 'Heap Sort', 'B'),
(120, 'Data Structures', 'Which sorting algorithm uses divide and conquer by splitting the array into smaller parts and merging them?', 'Bubble Sort', 'Insertion Sort', 'Merge Sort', 'Selection Sort', 'C'),
(121, 'Data Structures', 'What is the worst-case time complexity of binary search on a sorted array?', 'O(1)', 'O(n)', 'O(log n)', 'O(n²)', 'C'),
(122, 'Data Structures', 'Which data structure stores elements in contiguous memory locations?', 'Linked List', 'Array', 'Graph', 'Tree', 'B'),
(123, 'Data Structures', 'What is a node with no children in a tree called?', 'Root', 'Parent', 'Leaf', 'Edge', 'C'),
(124, 'Data Structures', 'What is an edge in a graph?', 'A vertex', 'A connection between two vertices', 'A root node', 'A tree level', 'B'),
(125, 'Database', 'What is a database?', 'A collection of organized data', 'A programming language', 'A computer network', 'An operating system', 'A'),
(126, 'Database', 'What does DBMS stand for?', 'Database Management System', 'Data Backup Management System', 'Database Machine System', 'Data Business Management Software', 'A'),
(127, 'Database', 'Which of the following is an example of a DBMS?', 'MySQL', 'HTML', 'CSS', 'JavaScript', 'A'),
(128, 'Database', 'What is a table in a relational database?', 'A collection of rows and columns', 'A programming function', 'A network device', 'A file compression method', 'A'),
(129, 'Database', 'What is a row in a database table commonly called?', 'Attribute', 'Record', 'Column', 'Field type', 'B'),
(130, 'Database', 'What is a column in a database table commonly called?', 'Record', 'Tuple', 'Attribute', 'Database', 'C'),
(131, 'Database', 'Which key uniquely identifies each record in a table?', 'Foreign Key', 'Primary Key', 'Candidate Table', 'Composite Table', 'B'),
(132, 'Database', 'What is the purpose of a foreign key?', 'To uniquely identify every database', 'To connect records between related tables', 'To encrypt the database', 'To delete duplicate rows', 'B'),
(133, 'Database', 'Which constraint prevents NULL values in a column?', 'UNIQUE', 'CHECK', 'NOT NULL', 'DEFAULT', 'C'),
(134, 'Database', 'Which constraint ensures that values in a column are unique?', 'UNIQUE', 'DEFAULT', 'CHECK', 'INDEX', 'A'),
(135, 'Database', 'What is normalization used for?', 'Increasing data redundancy', 'Reducing data redundancy and improving data organization', 'Deleting all duplicate databases', 'Encrypting tables', 'B'),
(136, 'Database', 'Which normal form removes repeating groups and ensures atomic values?', 'First Normal Form', 'Second Normal Form', 'Third Normal Form', 'Fourth Normal Form', 'A'),
(137, 'Database', 'What is a relationship between tables?', 'A connection between related data in tables', 'A programming loop', 'A CSS property', 'A network protocol', 'A'),
(138, 'Database', 'Which operation is used to retrieve data from a database?', 'SELECT', 'INSERT', 'DELETE', 'UPDATE', 'A'),
(139, 'Database', 'Which operation is used to add new records to a table?', 'SELECT', 'INSERT', 'UPDATE', 'ALTER', 'B'),
(140, 'Database', 'Which operation is used to modify existing records?', 'INSERT', 'UPDATE', 'SELECT', 'CREATE', 'B'),
(141, 'Database', 'Which operation is used to remove records from a table?', 'DELETE', 'DROP', 'REMOVE', 'CLEAR', 'A'),
(142, 'Database', 'What is a database index mainly used for?', 'To improve data retrieval speed', 'To delete records', 'To create backups', 'To change passwords', 'A'),
(143, 'Database', 'What is a transaction in a database?', 'A group of operations treated as a logical unit', 'A database column', 'A type of primary key', 'A database password', 'A'),
(144, 'Database', 'Which property of transactions means all operations are completed or none are completed?', 'Consistency', 'Atomicity', 'Isolation', 'Durability', 'B'),
(145, 'Database', 'Which property ensures that committed data remains saved even after a system failure?', 'Atomicity', 'Isolation', 'Durability', 'Consistency', 'C'),
(146, 'HTML', 'What does HTML stand for?', 'Hyper Text Markup Language', 'High Text Machine Language', 'Hyperlink Text Management Language', 'Home Tool Markup Language', 'A'),
(147, 'HTML', 'Which tag is used to create the largest heading?', '<h6>', '<heading>', '<h1>', '<head>', 'C'),
(148, 'HTML', 'Which tag is used to create a paragraph?', '<paragraph>', '<p>', '<para>', '<text>', 'B'),
(149, 'HTML', 'Which tag is used to create a hyperlink?', '<link>', '<a>', '<href>', '<url>', 'B'),
(150, 'HTML', 'Which attribute specifies the destination of a hyperlink?', 'src', 'href', 'link', 'destination', 'B'),
(151, 'HTML', 'Which tag is used to display an image?', '<image>', '<img>', '<picture>', '<src>', 'B'),
(152, 'HTML', 'Which attribute specifies the image source?', 'href', 'src', 'alt', 'link', 'B'),
(153, 'HTML', 'Which attribute provides alternative text for an image?', 'title', 'alt', 'text', 'description', 'B'),
(154, 'HTML', 'Which tag is used to create an unordered list?', '<ol>', '<ul>', '<list>', '<li>', 'B'),
(155, 'HTML', 'Which tag is used to create an ordered list?', '<ul>', '<ol>', '<li>', '<order>', 'B'),
(156, 'HTML', 'Which tag represents an individual list item?', '<item>', '<li>', '<list-item>', '<i>', 'B'),
(157, 'HTML', 'Which tag is used to create a table?', '<table>', '<tab>', '<tbl>', '<data>', 'A'),
(158, 'HTML', 'Which tag is used to define a table row?', '<td>', '<tr>', '<row>', '<th>', 'B'),
(159, 'HTML', 'Which tag is used to define a table header cell?', '<td>', '<head>', '<th>', '<header-cell>', 'C'),
(160, 'HTML', 'Which tag is used to define a table data cell?', '<data>', '<td>', '<cell>', '<tr>', 'B'),
(161, 'HTML', 'Which tag is used to create a form?', '<input>', '<form>', '<field>', '<submit>', 'B'),
(162, 'HTML', 'Which input type is used for a password field?', 'text', 'password', 'secure', 'hidden-password', 'B'),
(163, 'HTML', 'Which input type allows the user to select one option from a group?', 'checkbox', 'radio', 'select-one', 'option', 'B'),
(164, 'HTML', 'Which HTML element is used to create a clickable button?', '<button>', '<click>', '<btn>', '<input-button>', 'A'),
(165, 'HTML', 'Which tag is used to define important text semantically?', '<strong>', '<important>', '<bold>', '<bolder>', 'A'),
(166, 'HTML', 'Which HTML element is commonly used as a generic block-level container?', '<span>', '<div>', '<section-text>', '<container>', 'B'),
(167, 'Java', 'Which keyword is used to create a class in Java?', 'define', 'class', 'struct', 'object', 'B'),
(168, 'Java', 'Which method is the starting point of a Java application?', 'start()', 'run()', 'main()', 'execute()', 'C'),
(169, 'Java', 'Which keyword is used to inherit a class in Java?', 'implements', 'inherits', 'extends', 'using', 'C'),
(170, 'Java', 'Which keyword is used when a class implements an interface?', 'extends', 'implements', 'interface', 'instanceof', 'B'),
(171, 'Java', 'Which keyword is used to create an object in Java?', 'create', 'new', 'make', 'object', 'B'),
(172, 'Java', 'Which data type is used to store a single character?', 'String', 'char', 'character', 'text', 'B'),
(173, 'Java', 'Which data type stores true or false values?', 'int', 'boolean', 'bit', 'logical', 'B'),
(174, 'Java', 'Which keyword is used to prevent a class from being inherited?', 'static', 'private', 'final', 'constant', 'C'),
(175, 'Java', 'Which keyword is used to handle exceptions?', 'try', 'check', 'error', 'exception', 'A'),
(176, 'Java', 'Which block is executed when an exception occurs?', 'if', 'catch', 'finally', 'throw', 'B'),
(177, 'Java', 'Which block is generally executed whether an exception occurs or not?', 'catch', 'try', 'finally', 'throw', 'C'),
(178, 'Java', 'Which keyword is used to explicitly throw an exception?', 'throws', 'throw', 'exception', 'raise', 'B'),
(179, 'Java', 'Which collection does not allow duplicate elements?', 'ArrayList', 'HashSet', 'Vector', 'LinkedList', 'B'),
(180, 'Java', 'Which collection stores data as key-value pairs?', 'HashSet', 'ArrayList', 'HashMap', 'Stack', 'C'),
(181, 'Java', 'Which class is commonly used to create a mutable sequence of characters?', 'String', 'StringBuilder', 'Character', 'CharSequence', 'B'),
(182, 'Java', 'Which keyword refers to the current object?', 'super', 'this', 'current', 'self', 'B'),
(183, 'Java', 'Which keyword is used to refer to the parent class?', 'parent', 'base', 'super', 'this', 'C'),
(184, 'Java', 'What is method overloading?', 'Same method name with different parameter lists', 'Same method name in different packages only', 'Deleting a method', 'Calling a method repeatedly', 'A'),
(185, 'Java', 'What is method overriding?', 'Changing the return type only', 'Providing a new implementation of an inherited method', 'Creating multiple constructors', 'Calling a private method', 'B'),
(186, 'Java', 'Which feature allows Java programs to run on different platforms?', 'Pointers', 'Platform-independent bytecode', 'Direct hardware access', 'Assembly code', 'B'),
(187, 'Java', 'Which component executes Java bytecode?', 'JDK', 'JVM', 'JAR', 'Javadoc', 'B'),
(188, 'JavaScript', 'What is JavaScript mainly used for in web development?', 'Styling web pages', 'Adding interactivity and dynamic behavior', 'Creating database tables', 'Designing hardware', 'B'),
(189, 'JavaScript', 'Which keyword can be used to declare a variable in JavaScript?', 'var', 'variable', 'declare', 'letvar', 'A'),
(190, 'JavaScript', 'Which keyword declares a block-scoped variable that can be reassigned?', 'const', 'let', 'fixed', 'static', 'B'),
(191, 'JavaScript', 'Which keyword declares a block-scoped variable that cannot normally be reassigned?', 'let', 'var', 'const', 'static', 'C'),
(192, 'JavaScript', 'Which symbol is used for a single-line comment in JavaScript?', '<!--', '//', '##', '**', 'B'),
(193, 'JavaScript', 'Which function is commonly used to display a message in the browser console?', 'console.log()', 'print()', 'display()', 'writeConsole()', 'A'),
(194, 'JavaScript', 'Which operator checks both value and type equality?', '==', '=', '===', '!=', 'C'),
(195, 'JavaScript', 'Which operator is used for assignment?', '==', '=', '===', '=>', 'B'),
(196, 'JavaScript', 'Which data type represents true or false?', 'Number', 'String', 'Boolean', 'Object', 'C'),
(197, 'JavaScript', 'Which method adds an element to the end of an array?', 'push()', 'add()', 'append()', 'insert()', 'A'),
(198, 'JavaScript', 'Which method removes the last element from an array?', 'remove()', 'delete()', 'pop()', 'last()', 'C'),
(199, 'JavaScript', 'Which method removes the first element from an array?', 'pop()', 'shift()', 'removeFirst()', 'deleteFirst()', 'B'),
(200, 'JavaScript', 'Which method adds an element to the beginning of an array?', 'push()', 'prepend()', 'unshift()', 'addFirst()', 'C'),
(201, 'JavaScript', 'Which keyword is used to define a function?', 'function', 'def', 'method', 'fun', 'A'),
(202, 'JavaScript', 'Which object represents the HTML document loaded in the browser?', 'window', 'document', 'page', 'html', 'B'),
(203, 'JavaScript', 'Which method selects an element by its id?', 'getElementById()', 'selectById()', 'getId()', 'findId()', 'A'),
(204, 'JavaScript', 'Which event occurs when a user clicks an HTML element?', 'onhover', 'onclick', 'onpress', 'onselect', 'B'),
(205, 'JavaScript', 'Which method converts a JSON string into a JavaScript object?', 'JSON.parse()', 'JSON.convert()', 'JSON.object()', 'JSON.read()', 'A'),
(206, 'JavaScript', 'Which method converts a JavaScript object into a JSON string?', 'JSON.parse()', 'JSON.stringify()', 'JSON.convert()', 'JSON.encode()', 'B'),
(207, 'JavaScript', 'Which value represents the absence of an assigned value in JavaScript?', 'empty', 'undefined', 'voided', 'nothing', 'B'),
(208, 'JavaScript', 'Which operator is commonly used for logical AND in JavaScript?', '||', '&&', '!', 'AND', 'B'),
(209, 'Python', 'Which symbol is used to write a comment in Python?', '//', '<!--', '#', '/* */', 'C'),
(210, 'Python', 'Which keyword is used to define a function in Python?', 'function', 'def', 'fun', 'define', 'B'),
(211, 'Python', 'Which data type is used to store an ordered collection that can be changed?', 'tuple', 'list', 'set', 'string', 'B'),
(212, 'Python', 'Which data type is immutable and ordered?', 'List', 'Set', 'Dictionary', 'Tuple', 'D'),
(213, 'Python', 'Which data type stores key-value pairs?', 'List', 'Tuple', 'Dictionary', 'Set', 'C'),
(214, 'Python', 'Which collection does not allow duplicate elements?', 'List', 'Tuple', 'Set', 'Dictionary', 'C'),
(215, 'Python', 'Which function is used to find the length of an object?', 'size()', 'length()', 'len()', 'count()', 'C'),
(216, 'Python', 'Which function is used to display output?', 'display()', 'print()', 'output()', 'show()', 'B'),
(217, 'Python', 'Which function is commonly used to get input from the user?', 'scan()', 'read()', 'input()', 'get()', 'C'),
(218, 'Python', 'Which keyword is used for a conditional statement?', 'when', 'if', 'condition', 'check', 'A'),
(219, 'Python', 'Which keyword is used to handle exceptions?', 'catch', 'except', 'error', 'handle', 'B'),
(220, 'Python', 'Which keyword is used to raise an exception manually?', 'throw', 'raise', 'error', 'except', 'B'),
(221, 'Python', 'Which operator is used for exponentiation?', '^', '**', '//', '%%', 'B'),
(222, 'Python', 'Which operator performs floor division?', '/', '%', '//', '**', 'C'),
(223, 'Python', 'Which method adds an item to the end of a list?', 'add()', 'insert()', 'append()', 'push()', 'C'),
(224, 'Python', 'Which method removes and returns the last item of a list by default?', 'delete()', 'remove()', 'pop()', 'drop()', 'C'),
(225, 'Python', 'Which keyword is used to create a class?', 'class', 'object', 'struct', 'define', 'A'),
(226, 'Python', 'Which keyword is used to import a module?', 'include', 'import', 'using', 'require', 'B'),
(227, 'Python', 'What is the output of len(\"Python\")?', '5', '6', '7', '8', 'B'),
(228, 'Python', 'Which value represents a missing or empty value in Python?', 'null', 'undefined', 'None', 'empty', 'C'),
(229, 'Python', 'Which built-in function returns the largest value from an iterable?', 'maximum()', 'large()', 'max()', 'top()', 'C'),
(230, 'SQL', 'What does SQL stand for?', 'Structured Query Language', 'Simple Query Language', 'System Query Logic', 'Structured Question Language', 'A'),
(231, 'SQL', 'Which SQL statement is used to retrieve data?', 'GET', 'SELECT', 'FETCH DATA', 'OPEN', 'B'),
(232, 'SQL', 'Which SQL statement is used to insert new records?', 'ADD', 'INSERT', 'CREATE', 'PUT', 'B'),
(233, 'SQL', 'Which SQL statement is used to modify existing records?', 'CHANGE', 'MODIFY', 'UPDATE', 'ALTER', 'C'),
(234, 'SQL', 'Which SQL statement is used to remove records from a table?', 'REMOVE', 'DELETE', 'CLEAR', 'DROP ROW', 'B'),
(235, 'SQL', 'Which clause is used to filter rows?', 'ORDER BY', 'GROUP BY', 'WHERE', 'SORT BY', 'C'),
(236, 'SQL', 'Which clause is used to sort query results?', 'SORT', 'ORDER BY', 'GROUP BY', 'ARRANGE', 'B'),
(237, 'SQL', 'Which keyword is used to remove duplicate results?', 'UNIQUE', 'DISTINCT', 'DIFFERENT', 'ONLY', 'B'),
(238, 'SQL', 'Which function returns the number of rows?', 'COUNT()', 'NUMBER()', 'ROWS()', 'TOTAL()', 'A'),
(239, 'SQL', 'Which function returns the largest value?', 'MAX()', 'HIGHEST()', 'LARGE()', 'TOP()', 'A'),
(240, 'SQL', 'Which function returns the smallest value?', 'MIN()', 'LOWEST()', 'SMALL()', 'BOTTOM()', 'A'),
(241, 'SQL', 'Which function calculates the average value?', 'MEAN()', 'AVG()', 'AVERAGE()', 'MIDDLE()', 'B'),
(242, 'SQL', 'Which function calculates the total of numeric values?', 'TOTAL()', 'SUM()', 'ADD()', 'COUNT()', 'B'),
(243, 'SQL', 'Which clause groups rows having the same values?', 'GROUP BY', 'ORDER BY', 'WHERE', 'COLLECT BY', 'A'),
(244, 'SQL', 'Which clause is used to filter grouped results?', 'WHERE', 'HAVING', 'FILTER', 'GROUP FILTER', 'B'),
(245, 'SQL', 'Which command is used to create a new table?', 'MAKE TABLE', 'NEW TABLE', 'CREATE TABLE', 'BUILD TABLE', 'C'),
(246, 'SQL', 'Which command is used to change the structure of an existing table?', 'UPDATE', 'ALTER TABLE', 'CHANGE TABLE', 'MODIFY ROW', 'B'),
(247, 'SQL', 'Which command permanently removes a table and its structure?', 'DELETE TABLE', 'REMOVE TABLE', 'DROP TABLE', 'CLEAR TABLE', 'C'),
(248, 'SQL', 'Which keyword is used to combine rows from two or more tables based on a related column?', 'JOIN', 'MERGE ONLY', 'CONNECT', 'COMBINE', 'A'),
(249, 'SQL', 'Which JOIN returns only matching records from both tables?', 'LEFT JOIN', 'RIGHT JOIN', 'INNER JOIN', 'FULL JOIN', 'C'),
(250, 'SQL', 'Which constraint uniquely identifies each record in a table?', 'FOREIGN KEY', 'PRIMARY KEY', 'UNIQUE ROW', 'IDENTIFIER', 'B');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `technical_questions`
--
ALTER TABLE `technical_questions`
  ADD PRIMARY KEY (`question_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `technical_questions`
--
ALTER TABLE `technical_questions`
  MODIFY `question_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=251;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
