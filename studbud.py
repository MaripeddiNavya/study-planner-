import streamlit as st
import google.generativeai as genai

# ✅ Set up API Key for Google Gemini AI
GOOGLE_API_KEY = "AIzaSyBDiJXHgpKJ6YxApdp8dGzBrMkf-BYQeo8"  # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)

# ✅ Choose a valid AI model
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")

# ✅ User database (temporary storage using session state)
if "users" not in st.session_state:
    st.session_state.users = {}  # Format: {"username": "password"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "page" not in st.session_state:
    st.session_state.page = "login"  # Default page is Login

# ✅ Sidebar Navigation (Only Visible After Login)
if st.session_state.logged_in:
    st.sidebar.write(f"👋 Welcome, **{st.session_state.username}**!")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.page = "login"
        st.rerun()

# ✅ Registration Page
if st.session_state.page == "register":
    st.title("📝 Register a New Account")

    new_username = st.text_input("👤 Choose a Username")
    new_password = st.text_input("🔑 Choose a Password", type="password")
    confirm_password = st.text_input("🔑 Confirm Password", type="password")

    if st.button("Register"):
        if new_username in st.session_state.users:
            st.error("❌ Username already exists. Try another one.")
        elif new_password != confirm_password:
            st.error("❌ Passwords do not match!")
        elif len(new_password) < 4:
            st.error("❌ Password should be at least 4 characters long.")
        else:
            st.session_state.users[new_username] = new_password
            st.success("✅ Registration successful! You can now log in.")
            st.session_state.page = "login"
            st.rerun()

    if st.button("Already have an account? Login here"):
        st.session_state.page = "login"
        st.rerun()

# ✅ Login Page
elif st.session_state.page == "login":
    st.title("🔐 Login to StudBud")
    
    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.page = "study_planner"
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

    if st.button("New user? Register here"):
        st.session_state.page = "register"
        st.rerun()

# ✅ If logged in, show the Study Planner
if st.session_state.logged_in and st.session_state.page == "study_planner":
    st.title("📚 StudBud: AI Study Planner")

    # Sidebar Navigation
    menu = st.sidebar.radio("📌 Menu", ["Study Plan", "Extra Resources"])

    if menu == "Study Plan":
        st.subheader("🎯 Create Your Study Plan")
        
        # Dropdown for department selection
        departments = ["Engineering", "Pharmacy", "Medical", "Arts", "Commerce", "Science", "Law", "Management", "Others"]
        selected_department = st.selectbox("Select Your Department", departments)

        # User study query
        user_query = st.text_area("Describe your study needs (e.g., 'I need help with pharmacology and chemistry.')")

        def get_study_plan(department, query):
            try:
                prompt = f"Create a detailed, personalized study plan for a {department} student. Consider the following needs: {query}"
                response = model.generate_content(prompt)
                return response.text
            except Exception as e:
                return f"Error generating study plan: {e}"

        if st.button("📝 Generate Study Plan"):
            if user_query:
                study_plan = get_study_plan(selected_department, user_query)
                st.subheader("📅 Your AI-Generated Study Plan:")
                st.write(study_plan)
            else:
                st.warning("⚠️ Please enter your study preferences.")

    elif menu == "Extra Resources":
        st.subheader("📖 Extra Study Resources")

        # ✅ Google Drive PDFs & Study Links
        resources = {
            "Engineering": {
                "links": ["https://nptel.ac.in", "https://www.khanacademy.org/science"],
                "drive_pdfs": ["https://drive.google.com/file/d/ENGINEERING_PDF"],
                "youtube": ["https://www.youtube.com/watch?v=engineering_tutorial"]
            },
            "Pharmacy": {
                "links": ["https://www.drugbank.ca", "https://pharmawiki.in"],
                "drive_pdfs": ["https://drive.google.com/file/d/PHARMACY_PDF"],
                "youtube": ["https://www.youtube.com/watch?v=pharmacy_lecture"]
            },
            "Medical": {
                "links": ["https://www.medscape.com", "https://www.nejm.org"],
                "drive_pdfs": ["https://drive.google.com/file/d/MEDICAL_PDF"],
                "youtube": ["https://www.youtube.com/watch?v=medical_tutorial"]
            },
            "Commerce": {
                "links": ["https://www.investopedia.com", "https://www.accountingcoach.com"],
                "drive_pdfs": ["https://drive.google.com/file/d/COMMERCE_PDF"],
                "youtube": ["https://www.youtube.com/watch?v=commerce_lecture"]
            },
            "Science": {
                "links": ["https://www.sciencedirect.com", "https://www.nature.com"],
                "drive_pdfs": ["https://drive.google.com/file/d/SCIENCE_PDF"],
                "youtube": ["https://www.youtube.com/watch?v=science_tutorial"]
            },
            "Law": {
                "links": ["https://www.law.cornell.edu", "https://www.scotusblog.com"],
                "drive_pdfs": ["https://drive.google.com/file/d/LAW_PDF"],
                "youtube": ["https://www.youtube.com/watch?v=law_tutorial"]
            },
            "Others": {
                "links": ["https://www.edx.org", "https://www.udemy.com"],
                "drive_pdfs": ["https://drive.google.com/file/d/OTHER_PDF"],
                "youtube": ["https://www.youtube.com/watch?v=general_tutorial"]
            }
        }
        
        if selected_department in resources:
            st.write("🌐 **Recommended Links:**")
            for link in resources[selected_department]["links"]:
                st.markdown(f"- [{link}]({link})")

           
