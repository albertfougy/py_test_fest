import csv
import os
import random
import re
import subprocess
from unittest import TestCase


class Player:
    def __init__(self, **kwargs):
        self.name = kwargs.get('Name')
        self.height = kwargs.get('Height (inches)')
        self.experience = kwargs.get('Soccer Experience')
        self.guardian_names = kwargs.get('Guardian Name(s)')

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, str(self))

    def __dict__(self):
        return {
            'Name': self.name,
            'Height (inches)': self.height,
            'Soccer Experience': self.experience,
            'Guardian Name(s)': self.guardian_names
        }

    @property
    def filename(self):
        return re.sub('\s+', '_', self.name).lower() + '.txt'


class LeagueBuilderTests(TestCase):
    def setUp(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.players = []
        with open('soccer_players.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for player in reader:
                self.players.append(Player(**player))

    def _run_code(self):
        '''Execute the student's code directly'''
        subprocess.run([
            "python3",
            os.path.join(self.current_dir, "league_builder.py")
        ])

    def _cleanup(self):
        '''Delete any generated text files'''
        for filename in os.scandir(self.current_dir):
            if filename.is_file() and filename.name.endswith('.txt'):
                os.remove(os.path.join(self.current_dir, filename.name))

    def test_collections_exist(self):
        '''Test that the expected collections exist'''
        import league_builder
        self.assertTrue(league_builder.league)
        self.assertTrue(league_builder.sharks)
        self.assertTrue(league_builder.dragons)
        self.assertTrue(league_builder.raptors)

    def test_letters_exist(self):
        '''Test that executing the code creates all of the letters'''
        filenames = [p.filename for p in self.players]

        self._run_code()

        for filename in filenames:
            path = os.path.join(self.current_dir, filename)
            assert os.path.exists(path)

    def test_letter_content(self):
        '''Test a random letter's content. Not 100% accurate'''
        random_player = random.choice(self.players)

        self._run_code()

        with open(random_player.filename) as f:
            letter = f.read()
            self.assertRegex(letter, r'^Dear {}'.format(
                random_player.guardian_names
            ))
            self.assertRegex(letter, r'[Sharks|Raptors|Dragons]')
            self.assertIn(random_player.name, letter)
            self.assertRegex(letter, r'March 1[7|8], [1|3]pm')

    def test_main_block(self):
        '''Make sure importing the file doesn't create the letters'''
        self._cleanup()
        import league_builder
        self.assertFalse(os.path.exists(os.path.join(
            self.current_dir,
            self.players[0].filename
        )))
