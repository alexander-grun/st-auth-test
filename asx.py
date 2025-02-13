import streamlit as st
import duckdb
from datetime import datetime

@st.cache_resource
def get_duckdb_connection():
    motherduck_token = st.secrets["motherduck_token"]
    return duckdb.connect(f'md:?motherduck_token={motherduck_token}')

conn = get_duckdb_connection()

def get_user(email):
    """Retrieve user from the database by email."""
    result = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    return result

def store_user(email, name):
    """Store a new user or update login count and last login timestamp."""
    user = get_user(email)
    if user:
        conn.execute("UPDATE users SET login_count = login_count + 1, last_login = ? WHERE email = ?",
                     (datetime.now(), email))
    else:
        conn.execute("INSERT INTO users (email, name, last_login) VALUES (?, ?, ?)",
                     (email, name, datetime.now()))

if not st.experimental_user.is_logged_in:
    st.button("Log in with Google", on_click=st.login, args=["google"])
    st.button("Log in with Microsoft", on_click=st.login, args=["microsoft"])
    st.stop()

# Capture user info
user_email = st.experimental_user.email
user_name = st.experimental_user.name

# Store user in DuckDB
store_user(user_email, user_name)

# Display user info
st.markdown(f"Welcome! {user_name} ({user_email})")

st.button("Log out", on_click=st.logout)
st.markdown(f"Welcome! {st.experimental_user.name}")



st.experimental_user


# Basic User Information
# •	user_id (UUID or Auto-incrementing ID) – A unique identifier for each user (recommended over using email as a primary key).
# •	email (TEXT, Unique) – User’s email (often used for login but not as a primary key).
# •	name (TEXT) – Full name of the user.
# •	.
# Authentication & Access
# •	login_count (INTEGER) – Number of times the user has logged in.
# •	last_login (TIMESTAMP) – Last login date and time.
# •	created_at (TIMESTAMP) – Account creation date.
# •	role (TEXT) – User role (e.g., admin, user, moderator).
# •	auth_provider (TEXT) – OAuth provider used (e.g., Google, Microsoft, Auth0).
# Personalization & Preferences
# •	preferences (JSON) – Stores user preferences (e.g., dark mode, language).
# •	location (TEXT) – User's city/country.
# •	timezone (TEXT) – Preferred timezone.
