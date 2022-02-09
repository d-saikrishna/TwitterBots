# After any changes do the following
heroku login
heroku git:remote -a samvidhanbot
git commit -am "deploy message"
git push heroku