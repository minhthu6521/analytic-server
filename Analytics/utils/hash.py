from hashids import Hashids


class Hasher(object):
    hash_salt_setting = 'HASH_SALT'
    hash_min_length_setting = 'HASH_MIN_LENGTH'

    def init_app(self, app):
        self.min_length = app.config[self.hash_min_length_setting]
        self.salt = app.config[self.hash_salt_setting]

    def decode_hash(self, hash):
        decoded = Hashids(self.salt, self.min_length).decode(hash)
        self.check(decoded)
        return decoded[0]

    def decode_hashes(self, hashes):
        return [self.decode_hash(hash) for hash in hashes]

    def encode_hashes(self, numbers):
        return [self.encode_hash(num) for num in numbers]

    def encode_hash(self, num):
        # type: (object|int) -> object
        if isinstance(num, tuple):
            return Hashids(self.salt, self.min_length).encode(*num)
        elif int(num):
            return Hashids(self.salt, self.min_length).encode(num)
        return None

    def check(self, decoded):
        if len(decoded) != 1:
            raise ValueError("Invalid hash input")


hasher = Hasher()

encode_hash = hasher.encode_hash
decode_hash = hasher.decode_hash
decode_hashes = hasher.decode_hashes
encode_hashes = hasher.encode_hashes
