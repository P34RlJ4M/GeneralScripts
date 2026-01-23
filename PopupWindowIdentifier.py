import uuid
import base64

def generate_popup_id(length=8):
    raw = uuid.uuid4().bytes
    b64 = base64.urlsafe_b64encode(raw).rstrip(b'=')
    popup_id = b64[:length].decode('ascii')

    print("Generated Popup ID:", popup_id)

    return popup_id


if __name__ == "__main__":
    generate_popup_id()