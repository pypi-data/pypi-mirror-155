__author__ = """Aria Bagheri"""
__email__ = 'ariab9342@gmail.com'
__version__ = '1.1.0'

from enum import Enum

import pyhibp
from pyhibp import pwnedpasswords

from .walk_check import walk_checker

pyhibp.set_user_agent(ua="Python Password Security/1.1.0 (Library to check password security)")


class PasswordSecurityRequirement(Enum):
    USE_UPPERCASE = 1
    USE_LOWERCASE = 2
    USE_NUMBERS = 3
    USE_SPECIAL_CHARACTERS = 4
    MIN_16_CHARACTERS = 5
    NOT_PUBLICLY_KNOWN = 6
    NOT_KEYBOARD_WALK = 7
    NO_BANNED_WORDS = 8


PSR = PasswordSecurityRequirement


class PasswordSecurity:
    verifiers: set[PSR] = {
        PSR.USE_LOWERCASE,
        PSR.USE_UPPERCASE,
        PSR.USE_NUMBERS,
        PSR.USE_SPECIAL_CHARACTERS,
        PSR.MIN_16_CHARACTERS,
        PSR.NOT_PUBLICLY_KNOWN,
        PSR.NOT_KEYBOARD_WALK,
        PSR.NO_BANNED_WORDS,
    }
    banned_words: set[str] = set()

    def __init__(self, verifiers: set[PSR] = None, banned_words: set[str] = None):
        if verifiers:
            self.verifiers = verifiers
        if banned_words:
            self.banned_words = banned_words

    def verify_password(self, password: str, additional_banned_words: set[str] = None):
        banned_words = self.banned_words
        additional_banned_words and banned_words.update(additional_banned_words)

        is_safe = True
        is_safe &= PSR.NO_BANNED_WORDS not in self.verifiers or not self.contains_banned_words(password,
                                                                                               banned_words)
        is_safe &= PSR.MIN_16_CHARACTERS not in self.verifiers or self.is_password_long_enough(password)

        set_problems = self.get_character_set_missing_list(password)
        is_safe &= PSR.USE_NUMBERS not in self.verifiers or PSR.USE_NUMBERS not in set_problems
        is_safe &= PSR.USE_UPPERCASE not in self.verifiers or PSR.USE_UPPERCASE not in set_problems
        is_safe &= PSR.USE_LOWERCASE not in self.verifiers or PSR.USE_LOWERCASE not in set_problems
        is_safe &= PSR.USE_SPECIAL_CHARACTERS not in self.verifiers or PSR.USE_SPECIAL_CHARACTERS not in set_problems

        is_safe &= PSR.NOT_PUBLICLY_KNOWN not in self.verifiers or not self.is_password_public(password)
        is_safe &= PSR.NOT_KEYBOARD_WALK not in self.verifiers or not self.is_keyboard_walk(password)

        return is_safe

    def check_password_safety(self, password: str, additional_banned_words: set[str] = None) -> set[PSR]:
        banned_words = self.banned_words
        additional_banned_words and banned_words.update(additional_banned_words)

        problems = set()
        PSR.NO_BANNED_WORDS in self.verifiers and \
            self.contains_banned_words(password, banned_words) and \
            problems.add(PSR.NO_BANNED_WORDS)

        character_set_problems = self.get_character_set_missing_list(password)
        problems.update(character_set_problems.intersection(self.verifiers))

        PSR.NOT_PUBLICLY_KNOWN in self.verifiers and \
            self.is_password_public(password) and \
            problems.add(PSR.NOT_PUBLICLY_KNOWN)

        PSR.NOT_KEYBOARD_WALK in self.verifiers and \
            self.is_keyboard_walk(password) and \
            problems.add(PSR.NOT_KEYBOARD_WALK)
        return problems

    @staticmethod
    def contains_banned_words(password: str, banned_words: set[str]):
        return any(map(lambda x: x in password or password in x, banned_words))

    @staticmethod
    def is_password_long_enough(password: str):
        return len(password) >= 16

    @staticmethod
    def get_character_set_missing_list(password: str) -> set[PSR]:
        has_uppercase = has_lowercase = has_numbers = has_special_characters = False

        # https://owasp.org/www-community/password-special-characters
        special_characters = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

        problems = set()

        for c in password:
            has_uppercase |= c.isupper()
            has_lowercase |= c.islower()
            has_numbers |= c.isdigit()
            has_special_characters |= c in special_characters

        not has_uppercase and problems.add(PSR.USE_UPPERCASE)
        not has_lowercase and problems.add(PSR.USE_LOWERCASE)
        not has_numbers and problems.add(PSR.USE_NUMBERS)
        not has_special_characters and problems.add(PSR.USE_SPECIAL_CHARACTERS)

        return problems

    @staticmethod
    def is_password_public(password: str):
        return pwnedpasswords.is_password_breached(password) != 0

    @staticmethod
    def is_keyboard_walk(password: str):
        return walk_checker(password, strict=False)
