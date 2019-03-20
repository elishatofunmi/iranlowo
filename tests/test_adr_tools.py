# -*- coding: utf-8 -*-

import filecmp
import iranlowo
import os

def test_strip_accents():
    ca_fr = "Montréal, über, 12.89, Mère, Françoise, noël, 889"
    yo_0 = "ọjọ́ìbí 18 Oṣù Keje 1918 jẹ́ Ààrẹ Gúúsù Áfríkà"
    yo_1 = "Kí ó tó di ààrẹ"

    assert iranlowo.adr_tools.strip_accents(ca_fr) == "Montreal, uber, 12.89, Mere, Francoise, noel, 889"
    assert iranlowo.adr_tools.strip_accents(yo_0) == "ojoibi 18 Osu Keje 1918 je Aare Guusu Afrika"
    assert iranlowo.adr_tools.strip_accents(yo_1) == "Ki o to di aare"


def test_strip_accents_from_file():
    cwd = os.getcwd()
    src_file = cwd + "/tests/testdata/file1.txt"
    target_file = cwd + "/tests/testdata/file2.txt"
    test_target_file = cwd + "/tests/testdata/file3.txt"

    assert(iranlowo.adr_tools.strip_accents_from_file(src_file, test_target_file) is True)
    assert(filecmp.cmp(src_file, test_target_file) is False)
    assert(filecmp.cmp(target_file, test_target_file))

#
# def test_convert_to_nfc():
#     nfd_file = "./testdata/nfd.txt"
#     target_file = "./testdata/file3.txt"
#
#     assert(iranlowo.adr_tools.convert_to_NFC(nfd_file, target_file) == True)
#     # assert(target_file meets specs for NFD or matches a previously validated NFC file)