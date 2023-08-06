__author__ = """Aria Bagheri"""
__email__ = 'ariab9342@gmail.com'
__version__ = '1.0.2'

from enum import Enum
from typing import List

import pyhibp
from pyhibp import pwnedpasswords

from .walk_check import walk_checker

pyhibp.set_user_agent(ua="Python Password Security/1.0.2 (Library to check password security)")


class PasswordSecurityRequirement(Enum):
    USE_UPPERCASE = 1
    USE_LOWERCASE = 2
    USE_NUMBERS = 3
    USE_SPECIAL_CHARACTERS = 4
    AT_LEAST_16_CHARACTERS = 5
    NOT_PUBLICLY_KNOWN = 6
    NOT_KEYBOARD_WALK = 7
    SHOULD_NOT_CONTAIN_BANNED_WORDS = 8


PSR = PasswordSecurityRequirement


class PasswordSecurity:
    verifiers: List[PasswordSecurityRequirement] = [
        PSR.USE_LOWERCASE,
        PSR.USE_UPPERCASE,
        PSR.USE_NUMBERS,
        PSR.USE_SPECIAL_CHARACTERS,
        PSR.AT_LEAST_16_CHARACTERS,
        PSR.NOT_PUBLICLY_KNOWN,
        PSR.NOT_KEYBOARD_WALK,
        PSR.SHOULD_NOT_CONTAIN_BANNED_WORDS,
    ]
    banned_words: list = []

    def __init__(self, verifiers: List[PSR] = None, banned_words: list[str] = None):
        if verifiers:
            self.verifiers = verifiers
        if banned_words:
            self.banned_words = banned_words

    def verify_password(self, password: str, additional_banned_words: list[str] = None):
        banned_words = self.banned_words
        if additional_banned_words:
            banned_words.extend(additional_banned_words)

        is_safe = True
        if PSR.SHOULD_NOT_CONTAIN_BANNED_WORDS in self.verifiers and banned_words:
            is_safe &= not any(map(lambda x: x in password, banned_words))
        if PSR.AT_LEAST_16_CHARACTERS in self.verifiers:
            is_safe &= PasswordSecurity.is_password_long_enough(password)

        is_safe &= len(PasswordSecurity.get_character_set_missing_list(password)) == 0

        if is_safe and PSR.NOT_PUBLICLY_KNOWN in self.verifiers:
            is_safe &= not PasswordSecurity.is_password_publicly_known(password)

        if is_safe and PSR.NOT_KEYBOARD_WALK in self.verifiers:
            is_safe &= not PasswordSecurity.is_keyboard_walk(password)
        return is_safe

    def check_password_safety(self, password: str, additional_banned_words: list[str] = None):
        banned_words = self.banned_words
        if additional_banned_words:
            banned_words.extend(additional_banned_words)
        missed_list = []
        if PSR.SHOULD_NOT_CONTAIN_BANNED_WORDS in self.verifiers and any(map(lambda x: x in password, banned_words)):
            missed_list.append(PSR.SHOULD_NOT_CONTAIN_BANNED_WORDS)

        character_set_problems = PasswordSecurity.get_character_set_missing_list(password)
        missed_list.extend(character_set_problems)

        if PSR.NOT_PUBLICLY_KNOWN in self.verifiers and PasswordSecurity.is_password_publicly_known(password):
            missed_list.append(PSR.NOT_PUBLICLY_KNOWN)

        if PSR.NOT_KEYBOARD_WALK in self.verifiers and PasswordSecurity.is_keyboard_walk(password):
            missed_list.append(PSR.NOT_KEYBOARD_WALK)
        return missed_list

    @staticmethod
    def is_password_long_enough(password: str):
        return len(password) >= 16

    @staticmethod
    def get_character_set_missing_list(password: str):
        has_uppercase = has_lowercase = has_numbers = has_special_characters = False

        # https://owasp.org/www-community/password-special-characters
        special_characters = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

        problems = []

        for c in password:
            if not has_uppercase and c.isupper():
                has_uppercase = True
                problems.append(PSR.USE_UPPERCASE)
            if not has_lowercase and c.islower():
                has_lowercase = True
                problems.append(PSR.USE_LOWERCASE)
            if not has_numbers and c.isdigit():
                has_numbers = True
                problems.append(PSR.USE_NUMBERS)
            if not has_special_characters and c in special_characters:
                has_special_characters = True
                problems.append(PSR.USE_SPECIAL_CHARACTERS)
            if has_special_characters and has_numbers and has_uppercase and has_lowercase:
                break
        return problems

    @staticmethod
    def is_password_publicly_known(password: str):
        return pwnedpasswords.is_password_breached(password) != 0

    @staticmethod
    def is_keyboard_walk(password: str):
        return walk_checker(password, strict=False)
