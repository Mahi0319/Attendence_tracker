import streamlit as st
import pandas as pd
from datetime import date, datetime
from uuid import uuid4


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Mahesh • Attendance Tracker",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# SESSION STATE
# ============================================================

if "students" not in st.session_state:
    st.session_state.students = []

if "attendance" not in st.session_state:
    st.session_state.attendance = []

if "editing_student" not in st.session_state:
    st.session_state.editing_student = None


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #0b0d12;
    --surface: rgba(255,255,255,0.055);
    --surface-strong: rgba(255,255,255,0.075);
    --border: rgba(255,255,255,0.10);
    --text: #f8fafc;
    --muted: #94a3b8;
    --primary: #8b5cf6;
    --primary-light: #a78bfa;
    --green: #34d399;
    --yellow: #fbbf24;
    --red: #fb7185;
}

* {
    font-family: "Inter", sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 0%,
            rgba(124,58,237,0.18),
            transparent 28%
        ),
        radial-gradient(
            circle at 90% 10%,
            rgba(59,130,246,0.12),
            transparent 25%
        ),
        linear-gradient(
            135deg,
            #080a0f 0%,
            #0d1017 45%,
            #090b10 100%
        );
    color: var(--text);
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* ============================================================
   HERO
   ============================================================ */

.hero-box {
    position: relative;
    overflow: hidden;
    padding: 38px;
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 28px;
    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.075),
            rgba(255,255,255,0.025)
        );
    box-shadow:
        0 30px 80px rgba(0,0,0,0.35),
        inset 0 1px 0 rgba(255,255,255,0.05);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    margin-bottom: 25px;
}

.hero-box:after {
    content: "";
    position: absolute;
    width: 280px;
    height: 280px;
    right: -110px;
    top: -150px;
    border-radius: 50%;
    background: rgba(139,92,246,0.16);
    filter: blur(5px);
}

.hero-title {
    position: relative;
    z-index: 2;
    font-size: 36px;
    font-weight: 800;
    letter-spacing: -1.4px;
    color: #ffffff;
}

.hero-subtitle {
    position: relative;
    z-index: 2;
    max-width: 760px;
    margin-top: 8px;
    color: #a8b1c2;
    font-size: 14px;
    line-height: 1.7;
}

.hero-badge {
    position: relative;
    z-index: 2;
    display: inline-block;
    margin-top: 18px;
    padding: 7px 12px;
    border: 1px solid rgba(167,139,250,0.20);
    border-radius: 999px;
    background: rgba(139,92,246,0.10);
    color: #c4b5fd;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.7px;
}


/* ============================================================
   METRIC CARDS
   ============================================================ */

[data-testid="stMetric"] {
    min-height: 135px;
    padding: 22px !important;
    border: 1px solid var(--border);
    border-radius: 20px;
    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.075),
            rgba(255,255,255,0.025)
        );
    box-shadow:
        0 18px 45px rgba(0,0,0,0.20),
        inset 0 1px 0 rgba(255,255,255,0.04);
    backdrop-filter: blur(14px);
    transition:
        transform 0.25s ease,
        border-color 0.25s ease,
        box-shadow 0.25s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    border-color: rgba(167,139,250,0.35);
    box-shadow:
        0 25px 55px rgba(0,0,0,0.30),
        0 0 25px rgba(139,92,246,0.07);
}

[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 0.7px;
    text-transform: uppercase;
}

[data-testid="stMetricValue"] {
    color: #f8fafc !important;
    font-size: 28px !important;
    font-weight: 800 !important;
}


/* ============================================================
   TITLES
   ============================================================ */

.section-title {
    margin-top: 30px;
    margin-bottom: 5px;
    color: #f8fafc;
    font-size: 23px;
    font-weight: 800;
    letter-spacing: -0.5px;
}

.section-description {
    margin-bottom: 18px;
    color: #7f8ba0;
    font-size: 13px;
}


/* ============================================================
   TABS
   ============================================================ */

button[data-baseweb="tab"] {
    color: #8d99aa !important;
    font-weight: 600 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #c4b5fd !important;
}

div[data-baseweb="tab-highlight"] {
    background-color: #8b5cf6 !important;
}


/* ============================================================
   INPUTS
   ============================================================ */

.stTextInput input,
.stNumberInput input,
.stDateInput input,
.stSelectbox div[data-baseweb="select"],
.stTextArea textarea {
    background: rgba(255,255,255,0.045) !important;
    color: #f8fafc !important;
    border-color: rgba(255,255,255,0.10) !important;
    border-radius: 11px !important;
}

.stTextInput label,
.stNumberInput label,
.stDateInput label,
.stSelectbox label,
.stTextArea label,
.stRadio label {
    color: #aab4c4 !important;
}


/* ============================================================
   FORM
   ============================================================ */

[data-testid="stForm"] {
    padding: 24px;
    border: 1px solid var(--border);
    border-radius: 22px;
    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.065),
            rgba(255,255,255,0.025)
        );
    box-shadow:
        0 20px 55px rgba(0,0,0,0.22);
    backdrop-filter: blur(15px);
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button,
.stFormSubmitButton > button {
    min-height: 42px;
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 11px;
    background: rgba(255,255,255,0.06);
    color: #f8fafc;
    font-weight: 600;
    transition:
        transform 0.2s ease,
        background 0.2s ease,
        border-color 0.2s ease,
        box-shadow 0.2s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    transform: translateY(-2px);
    background: rgba(139,92,246,0.15);
    border-color: rgba(167,139,250,0.35);
    color: #ffffff;
    box-shadow: 0 10px 25px rgba(0,0,0,0.20);
}


/* ============================================================
   CONTAINERS
   ============================================================ */

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: rgba(255,255,255,0.09) !important;
    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.055),
            rgba(255,255,255,0.025)
        ) !important;
    border-radius: 18px !important;
    box-shadow: 0 15px 40px rgba(0,0,0,0.16);
}


/* ============================================================
   PROGRESS
   ============================================================ */

div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(
        90deg,
        #7c3aed,
        #a78bfa
    ) !important;
}


/* ============================================================
   DATAFRAME
   ============================================================ */

[data-testid="stDataFrame"] {
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 15px;
    overflow: hidden;
}


/* ============================================================
   ALERTS
   ============================================================ */

div[data-testid="stAlert"] {
    border-radius: 13px;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    margin-top: 45px;
    padding-top: 20px;
    border-top: 1px solid rgba(255,255,255,0.07);
    text-align: center;
    color: #64748b;
    font-size: 11px;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def calculate_percentage(present, total):
    if total == 0:
        return 0.0
    return round((present / total) * 100, 2)


def get_status(percentage):
    if percentage >= 75:
        return "Good"
    elif percentage >= 60:
        return "Warning"
    return "Critical"


def get_student(student_id):
    for student in st.session_state.students:
        if student["id"] == student_id:
            return student
    return None


def roll_exists(roll_number, ignore_id=None):
    for student in st.session_state.students:
        if student["id"] == ignore_id:
            continue

        if student["roll_number"].lower() == roll_number.lower():
            return True

    return False


def attendance_exists(student_id, attendance_date):
    return any(
        record["student_id"] == student_id
        and record["date"] == str(attendance_date)
        for record in st.session_state.attendance
    )


def delete_student(student_id):
    st.session_state.students = [
        student
        for student in st.session_state.students
        if student["id"] != student_id
    ]

    st.session_state.attendance = [
        record
        for record in st.session_state.attendance
        if record["student_id"] != student_id
    ]


# ============================================================
# HERO
# ============================================================

st.markdown(
    '<div class="hero-box"><div class="hero-title">🎓 Mahesh Attendance Tracker</div><div class="hero-subtitle">Manage students, record daily attendance and monitor academic attendance performance from one simple dashboard.</div><div class="hero-badge">● LIVE ATTENDANCE DASHBOARD</div></div>',
    unsafe_allow_html=True
)


# ============================================================
# CALCULATE METRICS
# ============================================================

students = st.session_state.students

total_students = len(students)

total_classes = sum(
    student["total_classes"]
    for student in students
)

total_present = sum(
    student["present_classes"]
    for student in students
)

overall_attendance = calculate_percentage(
    total_present,
    total_classes
)

needs_attention = sum(
    1
    for student in students
    if calculate_percentage(
        student["present_classes"],
        student["total_classes"]
    ) < 75
)


# ============================================================
# METRIC ROW
# ============================================================

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        "👨‍🎓 Total Students",
        total_students
    )

with m2:
    st.metric(
        "📚 Total Classes",
        total_classes
    )

with m3:
    st.metric(
        "📊 Overall Attendance",
        f"{overall_attendance}%"
    )

with m4:
    st.metric(
        "⚠️ Needs Attention",
        needs_attention
    )


# ============================================================
# NAVIGATION
# ============================================================

dashboard_tab, add_tab, attendance_tab, students_tab, analytics_tab = st.tabs(
    [
        "🏠 Dashboard",
        "➕ Add Student",
        "📅 Mark Attendance",
        "👥 Students",
        "📊 Analytics"
    ]
)


# ============================================================
# DASHBOARD
# ============================================================

with dashboard_tab:

    st.markdown(
        '<div class="section-title">Attendance Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">Quickly monitor the current attendance performance of your students.</div>',
        unsafe_allow_html=True
    )

    if not students:

        st.info(
            "🎓 Welcome to your Attendance Tracker. "
            "Add your first student to start monitoring attendance."
        )

    else:

        highest = max(
            students,
            key=lambda student: calculate_percentage(
                student["present_classes"],
                student["total_classes"]
            )
        )

        highest_percentage = calculate_percentage(
            highest["present_classes"],
            highest["total_classes"]
        )

        today_present = sum(
            1
            for record in st.session_state.attendance
            if record["date"] == str(date.today())
            and record["status"] == "Present"
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "🏆 Highest Attendance",
                f"{highest_percentage}%"
            )
            st.caption(highest["name"])

        with c2:
            st.metric(
                "📅 Present Today",
                today_present
            )

        with c3:
            st.metric(
                "🎯 Required Attendance",
                "75%"
            )

        st.markdown(
            '<div class="section-title">Student Performance</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-description">Current attendance percentage of each student.</div>',
            unsafe_allow_html=True
        )

        for student in students:

            percentage = calculate_percentage(
                student["present_classes"],
                student["total_classes"]
            )

            status = get_status(percentage)

            with st.container(border=True):

                left, middle, right = st.columns(
                    [5, 2, 1]
                )

                with left:

                    st.markdown(
                        f"**{student['name']}**"
                    )

                    st.caption(
                        f"{student['roll_number']} • "
                        f"{student['branch']} • "
                        f"{student['year']}"
                    )

                    st.progress(
                        min(percentage / 100, 1.0)
                    )

                with middle:

                    st.metric(
                        "Attendance",
                        f"{percentage}%"
                    )

                with right:

                    if status == "Good":
                        st.success("Good")

                    elif status == "Warning":
                        st.warning("Warning")

                    else:
                        st.error("Critical")


# ============================================================
# ADD STUDENT
# ============================================================

with add_tab:

    st.markdown(
        '<div class="section-title">Add New Student</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">Create a student profile before recording attendance.</div>',
        unsafe_allow_html=True
    )

    with st.form(
        "add_student_form",
        clear_on_submit=True
    ):

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input(
                "Student Name",
                placeholder="e.g. Mahesh Babu"
            )

        with col2:
            roll = st.text_input(
                "Roll Number",
                placeholder="e.g. 23CS101"
            )

        col3, col4 = st.columns(2)

        with col3:
            branch = st.selectbox(
                "Branch",
                [
                    "CSE",
                    "IT",
                    "ECE",
                    "EEE",
                    "ME",
                    "Civil"
                ]
            )

        with col4:
            year = st.selectbox(
                "Year",
                [
                    "1st Year",
                    "2nd Year",
                    "3rd Year",
                    "4th Year"
                ]
            )

        submitted = st.form_submit_button(
            "Create Student Profile",
            use_container_width=True
        )

    if submitted:

        name = name.strip()
        roll = roll.strip()

        if not name:
            st.error("Please enter the student name.")

        elif not roll:
            st.error("Please enter the roll number.")

        elif roll_exists(roll):
            st.error("A student with this roll number already exists.")

        else:

            new_student = {
                "id": str(uuid4()),
                "name": name,
                "roll_number": roll,
                "branch": branch,
                "year": year,
                "total_classes": 0,
                "present_classes": 0,
                "created_at": datetime.now().isoformat()
            }

            st.session_state.students.append(
                new_student
            )

            st.success(
                f"✅ {name} added successfully!"
            )

            st.rerun()


# ============================================================
# MARK ATTENDANCE
# ============================================================

with attendance_tab:

    st.markdown(
        '<div class="section-title">Mark Attendance</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">Record daily attendance. The percentage is calculated automatically.</div>',
        unsafe_allow_html=True
    )

    if not students:

        st.warning(
            "Please add students before marking attendance."
        )

    else:

        student_options = {
            f"{student['roll_number']} • {student['name']}":
            student["id"]
            for student in students
        }

        with st.form("attendance_form"):

            selected_label = st.selectbox(
                "Select Student",
                list(student_options.keys())
            )

            attendance_date = st.date_input(
                "Attendance Date",
                value=date.today()
            )

            attendance_status = st.radio(
                "Attendance Status",
                ["Present", "Absent"],
                horizontal=True
            )

            save_attendance = st.form_submit_button(
                "Save Attendance",
                use_container_width=True
            )

        if save_attendance:

            student_id = student_options[
                selected_label
            ]

            student = get_student(student_id)

            if attendance_exists(
                student_id,
                attendance_date
            ):

                st.warning(
                    "⚠️ Attendance has already been recorded "
                    "for this student on this date."
                )

            else:

                student["total_classes"] += 1

                if attendance_status == "Present":
                    student["present_classes"] += 1

                record = {
                    "id": str(uuid4()),
                    "student_id": student_id,
                    "student_name": student["name"],
                    "roll_number": student["roll_number"],
                    "date": str(attendance_date),
                    "status": attendance_status
                }

                st.session_state.attendance.append(
                    record
                )

                percentage = calculate_percentage(
                    student["present_classes"],
                    student["total_classes"]
                )

                st.success(
                    f"✅ {student['name']} marked "
                    f"{attendance_status}."
                )

                st.info(
                    f"Current attendance: **{percentage}%**"
                )

                st.rerun()


# ============================================================
# STUDENTS
# ============================================================

with students_tab:

    st.markdown(
        '<div class="section-title">Student Records</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">Search, edit and delete student records.</div>',
        unsafe_allow_html=True
    )

    if not students:

        st.info(
            "No students available yet."
        )

    else:

        f1, f2, f3 = st.columns(
            [2, 1, 1]
        )

        with f1:
            search = st.text_input(
                "🔎 Search",
                placeholder="Name or roll number"
            )

        with f2:

            branches = sorted(
                {
                    student["branch"]
                    for student in students
                }
            )

            branch_filter = st.selectbox(
                "Branch",
                ["All"] + branches
            )

        with f3:

            status_filter = st.selectbox(
                "Status",
                [
                    "All",
                    "Good",
                    "Warning",
                    "Critical"
                ]
            )

        filtered_students = []

        for student in students:

            percentage = calculate_percentage(
                student["present_classes"],
                student["total_classes"]
            )

            status = get_status(percentage)

            search_match = (
                search.lower() in student["name"].lower()
                or
                search.lower() in student["roll_number"].lower()
            )

            branch_match = (
                branch_filter == "All"
                or student["branch"] == branch_filter
            )

            status_match = (
                status_filter == "All"
                or status_filter == status
            )

            if (
                search_match
                and branch_match
                and status_match
            ):
                filtered_students.append(student)

        st.caption(
            f"{len(filtered_students)} student(s) found"
        )

        for student in filtered_students:

            percentage = calculate_percentage(
                student["present_classes"],
                student["total_classes"]
            )

            status = get_status(percentage)

            with st.container(border=True):

                top1, top2, top3 = st.columns(
                    [5, 2, 1]
                )

                with top1:

                    st.markdown(
                        f"**{student['name']}**"
                    )

                    st.caption(
                        f"{student['roll_number']} • "
                        f"{student['branch']} • "
                        f"{student['year']}"
                    )

                with top2:

                    st.metric(
                        "Attendance",
                        f"{percentage}%"
                    )

                with top3:

                    if status == "Good":
                        st.success("Good")

                    elif status == "Warning":
                        st.warning("Warning")

                    else:
                        st.error("Critical")

                st.progress(
                    min(percentage / 100, 1.0)
                )

                st.caption(
                    f"Present: {student['present_classes']} "
                    f"• Total Classes: {student['total_classes']}"
                )

                edit_col, delete_col = st.columns(2)

                with edit_col:

                    if st.button(
                        "✏️ Edit",
                        key=f"edit_{student['id']}",
                        use_container_width=True
                    ):

                        st.session_state.editing_student = (
                            student["id"]
                        )

                        st.rerun()

                with delete_col:

                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_{student['id']}",
                        use_container_width=True
                    ):

                        delete_student(
                            student["id"]
                        )

                        st.session_state.editing_student = None

                        st.success(
                            "Student deleted successfully."
                        )

                        st.rerun()


# ============================================================
# EDIT STUDENT
# ============================================================

if st.session_state.editing_student:

    student = get_student(
        st.session_state.editing_student
    )

    if student:

        st.markdown(
            '<div class="section-title">Edit Student</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-description">Update the student profile information.</div>',
            unsafe_allow_html=True
        )

        with st.form("edit_student_form"):

            col1, col2 = st.columns(2)

            with col1:

                edit_name = st.text_input(
                    "Student Name",
                    value=student["name"]
                )

            with col2:

                edit_roll = st.text_input(
                    "Roll Number",
                    value=student["roll_number"]
                )

            col3, col4 = st.columns(2)

            branch_options = [
                "CSE",
                "IT",
                "ECE",
                "EEE",
                "ME",
                "Civil"
            ]

            year_options = [
                "1st Year",
                "2nd Year",
                "3rd Year",
                "4th Year"
            ]

            with col3:

                edit_branch = st.selectbox(
                    "Branch",
                    branch_options,
                    index=branch_options.index(
                        student["branch"]
                    )
                )

            with col4:

                edit_year = st.selectbox(
                    "Year",
                    year_options,
                    index=year_options.index(
                        student["year"]
                    )
                )

            save_changes = st.form_submit_button(
                "💾 Save Changes",
                use_container_width=True
            )

        if save_changes:

            edit_name = edit_name.strip()
            edit_roll = edit_roll.strip()

            if not edit_name:

                st.error(
                    "Student name cannot be empty."
                )

            elif not edit_roll:

                st.error(
                    "Roll number cannot be empty."
                )

            elif roll_exists(
                edit_roll,
                student["id"]
            ):

                st.error(
                    "That roll number already exists."
                )

            else:

                student["name"] = edit_name
                student["roll_number"] = edit_roll
                student["branch"] = edit_branch
                student["year"] = edit_year

                for record in st.session_state.attendance:

                    if record["student_id"] == student["id"]:

                        record["student_name"] = edit_name
                        record["roll_number"] = edit_roll

                st.session_state.editing_student = None

                st.success(
                    "Student updated successfully!"
                )

                st.rerun()

        if st.button(
            "Cancel Editing",
            use_container_width=True
        ):

            st.session_state.editing_student = None

            st.rerun()


# ============================================================
# ANALYTICS
# ============================================================

with analytics_tab:

    st.markdown(
        '<div class="section-title">Attendance Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">Analyze attendance performance with interactive visualizations.</div>',
        unsafe_allow_html=True
    )

    if not students:

        st.info(
            "Add students and attendance records to generate analytics."
        )

    else:

        chart_rows = []

        for student in students:

            percentage = calculate_percentage(
                student["present_classes"],
                student["total_classes"]
            )

            chart_rows.append(
                {
                    "Student": student["name"],
                    "Attendance": percentage
                }
            )

        chart_df = pd.DataFrame(
            chart_rows
        )

        left, right = st.columns(2)

        with left:

            st.subheader("📊 Attendance by Student")

            st.bar_chart(
                chart_df.set_index("Student"),
                y="Attendance",
                height=350
            )

        with right:

            status_count = {
                "Good": 0,
                "Warning": 0,
                "Critical": 0
            }

            for student in students:

                percentage = calculate_percentage(
                    student["present_classes"],
                    student["total_classes"]
                )

                status = get_status(percentage)

                status_count[status] += 1

            status_df = pd.DataFrame(
                {
                    "Status": list(status_count.keys()),
                    "Students": list(status_count.values())
                }
            )

            st.subheader("🎯 Attendance Distribution")

            st.bar_chart(
                status_df.set_index("Status"),
                y="Students",
                height=350
            )

        st.divider()

        st.subheader("📋 Attendance Report")

        report = []

        for student in students:

            percentage = calculate_percentage(
                student["present_classes"],
                student["total_classes"]
            )

            report.append(
                {
                    "Student": student["name"],
                    "Roll Number": student["roll_number"],
                    "Branch": student["branch"],
                    "Year": student["year"],
                    "Present": student["present_classes"],
                    "Total Classes": student["total_classes"],
                    "Attendance": f"{percentage}%",
                    "Status": get_status(percentage)
                }
            )

        report_df = pd.DataFrame(report)

        st.dataframe(
            report_df,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# ATTENDANCE HISTORY
# ============================================================

if st.session_state.attendance:

    st.markdown(
        '<div class="section-title">Attendance History</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">Complete record of attendance entries.</div>',
        unsafe_allow_html=True
    )

    history = []

    for record in st.session_state.attendance:

        history.append(
            {
                "Date": record["date"],
                "Student": record["student_name"],
                "Roll Number": record["roll_number"],
                "Status": record["status"]
            }
        )

    history_df = pd.DataFrame(history)

    history_df = history_df.sort_values(
        "Date",
        ascending=False
    )

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer">🎓 Mahesh Attendance Tracker • Built with Python + Streamlit • Session-based attendance management</div>',
    unsafe_allow_html=True
)