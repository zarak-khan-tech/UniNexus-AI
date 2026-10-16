# English: Integration package — base contract for external system adapters.
# Roman Urdu: Integration package — external system adapters ke liye base contract.

# English: Importing adapters here triggers their self-registration with the
# global registry. Without this, the API would report zero integrations.
# Roman Urdu: Yahan adapters import karne se woh khud global registry mein
# register ho jate hain. Warna API zero integrations dikhati.
from backend.app.integrations.adapters import generic_rest  # noqa: F401
