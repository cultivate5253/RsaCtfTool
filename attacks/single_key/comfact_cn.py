#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from attacks.abstract_attack import AbstractAttack
from lib.rsalibnum import s2n, gcd
from lib.keys_wrapper import PrivateKey
from lib.utils import timeout, TimeoutError


class Attack(AbstractAttack):
    def __init__(self, attack_rsa_obj, timeout=60):
        super().__init__(attack_rsa_obj, timeout)
        self.speed = AbstractAttack.speed_enum["medium"]

    def comfact(self, cipher, publickey):
        for c in cipher:
            commonfactor = gcd(publickey.n, s2n(c))

            if commonfactor > 1:
                publickey.q = commonfactor
                publickey.p = publickey.n // publickey.q
                priv_key = PrivateKey(
                    int(publickey.p),
                    int(publickey.q),
                    int(publickey.e),
                    int(publickey.n),
                )
                return (priv_key, None)
        return (None, None)

    def attack(self, publickey, cipher=[]):
        """Try an attack where the public key has a common factor with the ciphertext - sourcekris"""
        timeout_delay = self.timeout
        if cipher is not None:
            try:
                with timeout(self.timeout):
                    return self.comfact(cipher, publickey)
            except TimeoutError:
                return (None, None)
        return (None, None)


if __name__ == "__main__":
    attack = Attack()
    attack.test()