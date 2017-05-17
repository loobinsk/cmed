import hashlib

from django.contrib.auth.hashers import BasePasswordHasher, mask_hash
from django.utils.datastructures import SortedDict


class MySQLHasher(BasePasswordHasher):
    algorithm = "mysqlsha1_sha1"

    def encode(self, str, *args):
        """
        Hash string twice with SHA1 and return uppercase hex digest,
        prepended with an asterix.
    
        This function is identical to the MySQL PASSWORD() function.
        """
        pass1 = hashlib.sha1(str).digest()
        pass2 = hashlib.sha1(pass1).hexdigest()
        return "*" + pass2.upper()

    def verify(self, password, encoded):
        algorithm, pwd_hash = encoded.split('$', 2)
        return pwd_hash == self.encode(password)

    def safe_summary(self, encoded):
        return SortedDict([
            ('algorithm', self.algorithm),
            ('hash', mask_hash(encoded, show=3)),
        ])
