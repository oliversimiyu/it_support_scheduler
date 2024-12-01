# IT Support Team Scheduler

A comprehensive web application for managing IT support team schedules and shift assignments. Built with Flask and modern web technologies.

## 🚀 Features

### Core Functionality
- **User Authentication**
  - Role-based access control (Admin/Team Member)
  - Secure login and registration
  - Team member profile management

- **Schedule Management**
  - Shift assignment and tracking
  - Personal schedule view
  - Team-wide schedule overview
  - Prevent double booking

- **Analytics Dashboard**
  - Shift distribution visualization (Pie Chart)
  - Team member workload analysis (Bar Chart)
  - Weekly shift patterns (Line Chart)
  - Real-time data updates

- **Admin Features**
  - Team member management
  - Shift assignment
  - Analytics access
  - Schedule optimization

### Technical Features
- Responsive design with Bootstrap 5
- Interactive charts using Chart.js
- SQLite database with SQLAlchemy
- Flask-Login for authentication
- CSRF protection
- Modern UI with Font Awesome icons

## 🛠️ Technology Stack

- **Backend**
  - Python 3.x
  - Flask
  - SQLAlchemy
  - Flask-Login
  - Flask-WTF

- **Frontend**
  - HTML5
  - CSS3
  - Bootstrap 5
  - Chart.js
  - Font Awesome

- **Database**
  - SQLite
  - SQLAlchemy ORM

## 📋 Prerequisites

- Python 3.x
- pip (Python package manager)
- Git

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/oliversimiyu/it_support_scheduler.git
cd it_support_scheduler
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python init_db.py
```

5. Run the application:
```bash
python main.py
```

The application will be available at `http://localhost:5000`

## 👥 User Roles

### Administrator
- Access to analytics dashboard
- Manage team members
- Assign and modify shifts
- View all schedules

### Team Member
- View personal schedule
- See team-wide schedule
- Update profile information
- View assigned shifts

## 📊 Analytics Features

1. **Shift Distribution**
   - Visual breakdown of shift types
   - Interactive pie chart
   - Real-time updates

2. **Team Member Workload**
   - Bar chart showing shifts per member
   - Workload comparison
   - Historical data

3. **Weekly Patterns**
   - Line chart of shifts by day
   - Trend analysis
   - Schedule optimization insights

## 🔒 Security Features

- Password hashing
- CSRF protection
- Session management
- Role-based access control
- Input validation
- Secure form handling

## 🎨 UI/UX Features

- Responsive design
- Modern Bootstrap components
- Intuitive navigation
- Interactive charts
- Clean and professional layout
- Mobile-friendly interface

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For any queries or support, please contact:
[Your Contact Information]
