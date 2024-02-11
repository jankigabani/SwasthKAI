import cv2
import streamlit as st


def welcome_message():
    st.title("Welcome to SwasthKAI")
    st.write("Before moving on, let's have some quick check on your health.")


def health_preference_form():
    st.sidebar.subheader("Health Preferences")
    diabatic = st.sidebar.selectbox("Are you diabetic?", ("Yes", "No"))
    if diabatic == "Yes":
        diabetic_type = st.sidebar.selectbox("Type of diabetes", ("Type 1", "Type 2"))
    else:
        diabetic_type = None
    allergic = st.sidebar.radio("Do you have any allergies?", ("Yes", "No"))
    if allergic == "Yes":
        allergies = st.sidebar.text_input("List your allergies")
    else:
        allergies = None
    other_habits = st.sidebar.radio("Do you have any other health-related habits?", ("Yes", "No"))
    cruelty_free = st.sidebar.radio("Do you follow a cruelty-free lifestyle?", ("Yes", "No"))

    return {
        "Diabetic": diabatic,
        "Diabetic Type": diabetic_type,
        "Allergic": allergic,
        "Allergies": allergies,
        "Other Habits": other_habits,
        "Cruelty-Free": cruelty_free
    }

from PIL import Image
def food_scanner():
    st.subheader("Let's Scan")
    option = st.selectbox("Select scanning method:", ("Webcam", "Browse"))

    if option == "Webcam":
        st.write("Click the button below to capture an image from your webcam.")

        # Function to capture image from webcam
        def capture_image():
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                st.error("Error: Unable to open webcam.")
                return

            ret, frame = cap.read()
            if not ret:
                st.error("Error: Unable to capture image.")
                return

            cap.release()
            return frame

        if st.button("Capture Image"):
            frame = capture_image()
            if frame is not None:
                st.image(frame, channels="BGR", caption="Captured Image")
                st.write("Image captured successfully!")

    else:
        st.write("Upload an image of the food package to scan.")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg"])

        if uploaded_file is not None:
            # Process the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image")
            st.write("Image uploaded successfully!")


def diet_plan():
    st.title("Diet Plan")

    gender = st.selectbox("What is your gender?", ["Male", "Female", "Other"])
    age = st.number_input("What is your age?", value=0, step=1, format="%d")
    height = st.number_input("What is your height?", value=0, step=1, format="%d")
    weight = st.number_input("What is your current weight?", value=0.0, step=0.1, format="%f")
    activity_level = st.selectbox("How active are you on an average day?", ["Light", "Moderate", "Heavy"])
    eating_preference = st.selectbox("What's your eating preference?",
                                     ["Vegetarian", "Non-Vegetarian", "Vegan", "Ovo-Vegetarian"])
    medical_history = st.multiselect("What's your medical history?",
                                     ["Bloating", "Constipation", "Diabetes", "High Cholesterol", "Hypothyroidism",
                                      "PCOS", "PCOD", "None"])

    # Calculating the BMR and Calorie Requirement based on User Inputs
    if gender == "Male":
        bmr = 88.4 + (13.4 * weight) + (4.8 * height) - (5.68 * age)
    else:
        bmr = 447.6 + (9.25 * weight) + (3.1 * height) - (4.68 * age)

    if activity_level == "Light":
        calorie_requirement = bmr * 1.375
    elif activity_level == "Moderate":
        calorie_requirement = bmr * 1.55
    else:
        calorie_requirement = bmr * 1.725

    # Calculate the number of steps required based on user input
    steps_per_day = 10000 if activity_level == "Moderate" else 15000

    # Food Recommendations
    breakfast = "Oats with milk, nuts, and fruits"
    lunch = "Brown rice, dal, vegetables, and a salad"
    snack = "Boiled eggs, fruit, and nuts"
    dinner = "Grilled chicken/fish/tofu, quinoa, vegetables, and a salad"

    if eating_preference == "Vegetarian":
        lunch = "Brown rice, dal, vegetables, and a salad with paneer/tofu"
        dinner = "Paneer/tofu, quinoa, vegetables, and a salad"

    if eating_preference == "Vegan":
        breakfast = "Oats with soy milk, nuts, and fruits"
        lunch = "Brown rice, lentils, vegetables, and a salad"
        snack = "Roasted chickpeas, fruit, and nuts"
        dinner = "Tofu, quinoa, vegetables, and a salad"

    # Displaying Recommendations
    st.write(f"You need to consume {calorie_requirement:.2f} calories each day to achieve your goals.")
    st.write(f"You should aim to take {steps_per_day} steps per day.")
    st.write("Here are some recommended meals for you:")
    st.write("Breakfast: " + breakfast)
    st.write("Lunch: " + lunch)
    st.write("Snack: " + snack)
    st.write("Dinner: " + dinner)


def main():
    page = st.sidebar.selectbox("Select Page", ["Welcome", "Health Preferences", "Food Scanner", "Diet Plan"])

    if page == "Welcome":
        welcome_message()
    elif page == "Health Preferences":
        health_preference_form()
    elif page == "Food Scanner":
        food_scanner()
    elif page == "Diet Plan":
        diet_plan()


if __name__ == "__main__":
    main()
