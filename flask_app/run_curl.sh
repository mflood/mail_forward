# for flask / gunicorn
PORT=5000

# for Docker:
#PORT=8000

# normal message
curl -d '{ "to": "hermannwest@gmail.com", "to_name": "Mr. Fake", "from": "hermannwest@gmail.com", "from_name": "Brightwheel", "subject": "A Message from Brightwheel", "body": "<h1>Your Bill</h1><p>$10</p>"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:$PORT/email

# bad email message
curl -d '{ "to": "bademail", "to_name": "Mr. Fake", "from": "noreply@mybrightwheel.com", "from_name": "Brightwheel", "subject": "A Message from Brightwheel", "body": "<h1>Your Bill</h1><p>$10</p>"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:$PORT/email

# unauth recip
curl -d '{ "to": "someone@example.com", "to_name": "Mr. Fake", "from": "noreply@mybrightwheel.com", "from_name": "Brightwheel", "subject": "A Message from Brightwheel", "body": "<h1>Your Bill</h1><p>$10</p>"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:$PORT/email
