@echo off
node ./node_modules/nodemon/bin/nodemon ./app/server/app.js -w ./app/server/action -w ./app/server/app.js -i ./app/server/public -i ./app/server/views
pause