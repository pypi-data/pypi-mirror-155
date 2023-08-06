"""Generate fake name, title, email."""
import random

from haikunator import Haikunator


class HaikunatorHelper(object):
    """Haikunator Helper."""

    adjectives = [
        "autumn", "hidden", "bitter", "misty", "silent", "empty", "dry",
        "dark", "summer", "icy", "delicate", "quiet", "white", "cool",
        "spring", "winter", "patient", "twilight", "dawn", "crimson",
        "wispy", "weathered", "blue", "billowing", "broken", "cold", "damp",
        "falling", "frosty", "green", "long", "late", "lingering", "bold",
        "little", "morning", "muddy", "old", "read", "rough", "still", "small",
        "sparkling", "throbbing", "shy", "wandering", "withered", "wild",
        "black", "young", "holy", "solitary", "fragrant", "aged", "snowy",
        "proud", "floral", "restless", "divine", "polished", "ancient",
        "purple", "lively", "nameless"
    ]
    nouns = [
        "waterfall", "river", "breeze", "moon", "rain", "wind", "sea",
        "morning", "snow", "lake", "sunset", "pine", "shadow", "leaf", "dawn",
        "glitter", "forest", "hill", "cloud", "meadow", "sun", "glade", "bird",
        "brook", "butterfly", "bush", "dew", "dust", "field", "fire", "flower",
        "firefly", "feather", "grass", "haze", "mountain", "night", "pond",
        "darkness", "snowflake", "silence", "sound", "sky", "shape", "surf",
        "thunder", "violet", "water", "wildflower", "wave", "water",
        "resonance", "sun", "wood", "dream", "cherry", "tree", "fog", "frost",
        "voice", "paper", "frog", "smoke", "star"
    ]
    emails = [
        "qq.com", "163.com", "126.com", "189.com", "google.com", "hotmail.com",
        "outlook.com",
    ]
    first_names = [
        "Adams", "Allen", "Anderson", "Baker", "Brown", "Campbell", "Carter",
        "Clark", "Davis", "Evans", "Garcia", "Gonzales", "Green", "Hall",
        "Harris", "Hernandez", "Hill", "Jackson", "Johnson", "Jones", "King",
        "Lee", "Lewis", "Lopez", "Martin", "Martines", "Miller", "Mitchell",
        "Moore", "Nelson", "Perez", "Phillips", "Ramirez", "Roberts",
        "Robinson", "Rodriguez", "Sanches", "Scott", "Smith", "Taylor",
        "Thomas", "Thompson", "Torres", "Turner", "Walker", "White",
        "Williams", "Wilson", "Wright", "Young"
    ]
    last_names = [
        "Abigail", "Adelaide", "Aggie", "Alex", "Alice", "Amy", "Ava",
        "Belle", "Beatrice", "Bernadette", "Bid", "Brittany", "Camilla",
        "Carol", "Catherine", "Cecily", "Charlotte", "Della", "Doris",
        "Elva", "Eileen", "Eleanora", "Ella", "Ethel", "Eve", "Eulalia",
        "Faustina", "Fidelia", "Flora", "Flavia", "Georgie", "Gill",
        "Gladys", "Grace", "Hilda", "Helga", "Ivy", "Irene", "Jemima",
        "Jane", "Janice", "Jessie", "Joan", "Juliet", "Kathleen", "Lesley",
        "Lily", "Marlene", "Mercedes", "Martha", "Millicent", "Miriam",
        "Monica", "Nadine", "Nicole", "Nita", "Olive", "Pru", "Rebecca",
        "Roberta", "Rosalind", "Rosemary", "Rosa", "Sylvia", "Sonia",
        "Sophie", "Susan", "Toni", "Trudie", "Undine", "Vivian", "Zoe"
    ]

    def _haikunator_t(self):
        """Return haikunator instance."""
        seed = random.uniform(1, 4096)
        haikunator = Haikunator(
            adjectives=HaikunatorHelper.adjectives,
            nouns=HaikunatorHelper.nouns,
            seed=seed
        )
        return haikunator

    def _haikunator_n(self):
        """Return haikunator instance."""
        seed = random.uniform(1, 4096)
        haikunator = Haikunator(
            nouns=HaikunatorHelper.last_names,
            adjectives=HaikunatorHelper.first_names,
            seed=seed
        )
        return haikunator

    def _haikunator_e(self):
        """Return haikunator instance."""
        seed = random.uniform(1, 4096)
        haikunator = Haikunator(
            adjectives=HaikunatorHelper.nouns,
            nouns=HaikunatorHelper.emails,
            seed=seed
        )
        return haikunator

    def generate_title(self):
        """Generate product title."""
        title = self._haikunator_t().haikunate(
            delimiter=' ',
            token_length=0,
        )
        return title

    def generate_name(self):
        """Generate custom name."""
        name = self._haikunator_n().haikunate(
            delimiter=' ',
            token_length=0,
        )
        return name.split(" ")

    def generate_email(self):
        """Generate custom email."""
        email = self._haikunator_e().haikunate(
            delimiter='@',
            token_length=0,
        )
        return email
