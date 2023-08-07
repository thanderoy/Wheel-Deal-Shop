import random
import string


def generate_order_no():
    """
    Generate a random 5 character alphanumeric string.
    Constraints considered:
        -  Human-readable.
        - Allow case-insensitivity by picking only uppercase.
        - Reduce ambiguity by eliminating 1/I/O/0.
    """
    pool = string.ascii_uppercase + string.digits
    pool = list(set(pool) - {'1', 'I', '0', 'O'})
    return "".join(random.choice(pool) for x in range(5))
