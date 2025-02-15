# 📱🎯 Mobile & Backend Project with Django & React Native Expo

## 🌟 1. Introduction
The project includes:

Backend: Django (CRUD) combined with the research topic Enhanced Face Classification Using Centroid-Based Representation.

Mobile: React Native Expo fetch API from backend

Virtual Device: Android Studio (Pixel_3a_API_30).

## 🌟 2. Technologies Used

Backend: Django, Django Rest Framework, OpenCV, TensorFlow, CV2.

Mobile: React Native, Router Expo, Image Picker.

Database: PostgreSQL/SQLite.

Virtual Device: Android Studio (Pixel_3a_API_30).

# ⚙️ 3. Backend Installation (Django)
### Clone project
git clone https://github.com/your-repo.git](https://github.com/dominhquan2003/Enhanced-Face-Classification-Using-Centroid-Based-Representation
cd backendapi

### Install libraries
pip install -r requirements.txt

### Run migrations
python manage.py makemigrations
python manage.py migrate

### Run server
python manage.py runserver 

# ⚙️ 4. Android Virtual Device Installation Guide
## 4.1 Install Java 
1. Visit the official Oracle Java Downloads page. [Download](https://www.oracle.com/java/technologies/downloads/)
2. Choose the appropriate version for your machine.
3. Set up the environment:
- Open Windows search and type "Edit environment variables".
- Press Enter to open the Environment Variables window.
- Now, in the System variables section, click Path > Edit > New.
- Copy the path of the folder containing the installed JDK binaries. For example, in this case, the path is C:\Program Files\Java\jdk-18.0.1.1\bin.
- Switch to the Environment variables window, paste the copied path, and save the changes.
- Next, in the User Variables section, click New.
- Add PATH_HOME to the variable name box and C:\Program Files\Java\jdk-18.0.1.1 to the variable value box.
- Finally, save the changes by clicking OK.
*Remember to replace the JDK version with the one you are using. In the example case, the version jdk-18.0.1.1 is used.
## 4.2 Install Android Studio [Download](https://developer.android.com/studio?hl=vi) 
After installation, open the application -> More action -> Virtual Device -> Click the "+" sign in the top left corner.

# ⚙️ 5. React Native 
1. npm install 


# ⚙️ 6. Run application
* After installation, go to the main directory where there are two files start_backend.sh and start_frontend.sh. 
  Use gitbash to open them with ./start_backend.sh and ./start_frontend.sh
