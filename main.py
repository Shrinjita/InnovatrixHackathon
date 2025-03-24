import streamlit as st
import pymongo
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb

# ================================
# 🌟 DATABASE CONNECTION
# ================================
# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://user:password@cluster0.mongodb.net/?retryWrites=true&w=majority")
db = client["smartcity"]
users_collection = db["users"]

# ================================
# 🌟 IMAGE & LINK FUNCTIONS
# ================================
def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))

def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)

# ================================
# 🌟 FOOTER LAYOUT
# ================================
def layout(*args):

    style = """
    <style>
      #MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
      .stApp { bottom: 105px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="black",
        text_align="center",
        height="auto",
        opacity=1
    )

    style_hr = styles(
        display="block",
        margin=px(8, 8, "auto", "auto"),
        border_style="inset",
        border_width=px(2)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)

# ================================
# 🌟 FOOTER FUNCTION
# ================================
def footer():
    myargs = [
        "Made with ❤️ by ",
        link("https://github.com/Shrinjita", "@Shrinjita"),
        br(),
        "Contribute on ",
        link("https://github.com/Shrinjita/InnovatrixHackathon", "GitHub"),
        br(),
        "Powered by ",
        image('https://i.imgur.com/thJhzOO.png', width=px(25), height=px(25))
    ]
    layout(*myargs)

# ================================
# 🌟 APP FUNCTIONALITY
# ================================
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Login / Sign Up", "Public Transport", "Waste Segregation", "Admin Dashboard"])

    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>SmartCity+</h1>", unsafe_allow_html=True)

    if page == "Login / Sign Up":
        st.header("🔒 Login / Sign Up")

        # Choose Action
        action = st.radio("Choose Action", ["Login", "Sign Up"])

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if action == "Sign Up":
            if st.button("Sign Up"):
                if username and password:
                    # Add user to MongoDB
                    users_collection.insert_one({"username": username, "password": password})
                    st.success("Signed up successfully! Please login.")
                else:
                    st.warning("Please enter both username and password.")

        if action == "Login":
            if st.button("Login"):
                user = users_collection.find_one({"username": username, "password": password})
                if user:
                    st.success("Logged in successfully!")
                else:
                    st.error("Invalid credentials. Please try again.")

    elif page == "Public Transport":
        st.header("🚍 Public Transport")
        st.write("Transport data and analytics coming soon!")

    elif page == "Waste Segregation":
        st.header("♻️ Waste Segregation")
        st.write("Waste management functionality will be added here.")

    elif page == "Admin Dashboard":
        st.header("📊 Admin Dashboard")
        st.write("Admin management and insights will be displayed here.")

    footer()

if __name__ == "__main__":
    main()
