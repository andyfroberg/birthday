# Birthday Reminder Web App
## **Quick Start Guide**
 ```bash
 # Clone this repository
 $  git clone https://github.com/andyfroberg/birthday.git

# Navigate to the main app directory 'birthday'
$  cd birthday

# Create and start the containers
$  docker-compose --profile production up -d --build
 ```
## **Project File Structure**
```
birthday
│   README.md
│   docker-compose.yml  
│
└───flask-project
│   │   Dockerfile
│   │   app.py
│   │   email_notifications.py
│   │   forms.py
│   │   models.py
│   │   requirements.txt
│   │
│   └───templates
│       │   add_event.html
│       │   base.html
│       │   change_password.html
│       │   edit_event.html
│       │   home.html
│       │   login.html
│       │   register.html
│       │   reminders.html
│       │   update_event.html
│   
└───nginx
    │   Dockerfile
    │   nginx.conf
```


## **TCSS 506**
This project was created as the capstone for TCSS 506 at UW Tacoma as part of the Graduate Certificate in Software Development Engineering in 2022-23.
## **Team STAX**
#### Sheehan Smith
#### Tom Swanson
#### Andrew Froberg
#### Xiying Long




## **Team Responsibilities**
#### The entire team worked together on many of the features of the web app. This allowed us all to gain experience with various full-stack concepts. The entire team helped one another quite a bit on all the features listed below.
### **Sheehan Smith**
- Project management/team lead
- Docker orchestration/devops
- Change password feature
- Date conversion functionality
### **Tom Swanson**
- Database design and implementation
- Initial celebrity API feature creation
- Sorting events
- Email notifications (not implemented in final version)
### **Andrew Froberg**
- Filtering events feature
- Implemented celebrity API feature to add events route
- Docker orchestration/devops
- Final web design and styling
### **Xiying Long**
- Initial website design and styling
- User registration
- Log in/log out functionality
- Add user-created event functionality
- Update and delete user-created events