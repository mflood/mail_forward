
# A bit of Mail Provider Info

## Mailgun python snippet

```python
def send_simple_message():
	return requests.post(
		"https://api.mailgun.net/v3/YOUR_DOMAIN_NAME/messages",
		auth=("api", "YOUR_API_KEY"),
		data={"from": "Excited User <mailgun@YOUR_DOMAIN_NAME>",
			"to": ["bar@example.com", "YOU@YOUR_DOMAIN_NAME"],
			"subject": "Hello",
			"text": "Testing some Mailgun awesomness!"})
```

## Mandrill curl snippet

[https://mandrillapp.com/api/docs/messages.curl.html] (https://mandrillapp.com/api/docs/messages.curl.html)

```bash
curl -A 'Mandrill-Curl/1.0' -d '{"key": "API-KEY", "message": {"text":"Example text content","subject":"example subject","from_email":"message.from_email@example.com","from_name":"Example Name", "to": [{"email":"recipient.email@example.com","name":"Recipient Name","type":"to"}]}' 'https://mandrillapp.com/api/1.0/messages/send.json'
```
