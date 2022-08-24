# retirement-calculator

### How to run the application

Easiest Way:
- I deployed the application to heroku and can be accessed by this link: https://whispering-badlands-42217.herokuapp.com/
- That link displays the react frontend which you can enter any user number and see the results displayed
- You can also do https://whispering-badlands-42217.herokuapp.com/{ENTER_USER_ID} to see the json response from my flask backend

Harder Way:
- You can clone this git repo
- Use pipenv to install the python dependencies 
- Use npm install within client for the node modules
- Change proxy within package.json to https://localhost5000.com/
- Run app.py locally 
- npm start within /client 

### Things I would have done differently given more time
- Assume the user dies on their birthday to calculate the amount needed to the day
- Have the user be able to change values such as expected rate of return, savings_rate, and retirement_age so the user could figure out how they can reach their retirement goals 
- Increase accuracy by factoring in taxes, social secutiry, etc...
- Have a table/plot with the users savings over the years until they retire and how the savings grows/decays once they retire
- Would have a nicer looking frontend and the react code could be broken up into components with better functionality


