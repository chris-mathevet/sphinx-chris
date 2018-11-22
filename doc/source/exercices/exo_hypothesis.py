from hypothesis import given
from hypothesis.strategies import text
from fail_test import fail_test

attendu_etudiant = ["encode", "decode"]

@given(text())
def test_decode_encode_inverse(code_etu, s):
   round_trip = code_etu.decode(code_etu.encode(s))
   if s != round_trip:
      fail_test("encoder \"{}\" puis la décoder ne redonne pas la même valeur".format(s))

