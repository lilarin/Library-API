import uuid


def generate_session_url():
    base_url = "https://payment-provider.com/session/"
    session_id = uuid.uuid4()
    session_url = f"{base_url}{session_id}"
    return session_url


session_url = generate_session_url()
print(session_url)
