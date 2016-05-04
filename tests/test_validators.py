from unittest import TestCase
from isatools import isajson
import os
from jsonschema import ValidationError


class ValidateIsaJsonTest(TestCase):

    def setUp(self):
        self._dir = os.path.dirname(__file__)

    def tearDown(self):
        pass

    def test_json_load(self):
        """Tests against 0001"""
        with self.assertRaises(ValueError):
            isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'invalid.json')))

        try:
            isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'minimal_syntax.json')))
        except ValueError:
            self.fail("isajson.validate() raised a ValueError where it shouldn't have!")

    def test_isajson_schemas(self):
        """Tests against 0002"""
        with self.assertRaises(ValidationError):
            isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'invalid_isajson.json')))

        try:
            isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'minimal_syntax.json')))
        except ValidationError:
            self.fail("isajson.validate() raised a ValidationError where it shouldn't have!")

    def test_encoding_check(self):
        """Tests against 0010"""
        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'minimal_syntax.json')))
        if "File should be UTF-8 encoding" in log_msg_stream.getvalue():
            self.fail("Validation warning present when testing against UTF-8 encoded file")

        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'non_utf8.json')))
        if "File should be UTF-8 encoding" not in log_msg_stream.getvalue():
            self.fail("Validation warning missing when testing against UTF-16 encoded file (UTF-8 required)")

    def test_source_link(self):
        """Tests against 1002"""
        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'source_link.json')))
        if "['#source/1'] not found" in log_msg_stream.getvalue():
            self.fail("Validation error present when should pass without error - source link reports broken when present in data")

        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'source_link_fail.json')))
        if "['#source/1'] not found" not in log_msg_stream.getvalue():
            self.fail("Validation error missing when should report error - data has broken source link but not reported in validation report")

    def test_sample_link(self):
        """Tests against 1003"""
        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'sample_link.json')))
        if "['#sample/1'] not found" in log_msg_stream.getvalue():
            self.fail(
                "Validation error present when should pass without error - sample link reports broken when present in data")

        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'sample_link_fail.json')))
        if "['#sample/1'] not found" not in log_msg_stream.getvalue():
            self.fail(
                "Validation error missing when should report error - data has broken sample link but not reported in validation report")

    def test_data_file_link(self):
        """Tests against 1004"""
        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'datafile_link.json')))
        if "['#data/a_file.dat'] not found" in log_msg_stream.getvalue():
            self.fail(
                "Validation error present when should pass without error - data file link reports broken when present in data")

        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'datafile_link_fail.json')))
        if "['#data/a_file.dat'] not found" not in log_msg_stream.getvalue():
            self.fail(
                "Validation error missing when should report error - data has broken data file link but not reported in validation report")

    def test_material_link(self):
        """Tests against 1005"""
        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'material_link.json')))
        if "['#material/1'] not found" in log_msg_stream.getvalue():
            self.fail(
                "Validation error present when should pass without error -materiallink link reports broken when present in data")

        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'material_link_fail.json')))
        if "['#material/1'] not found" not in log_msg_stream.getvalue():
            self.fail(
        "Validation error missing when should report error - data has broken material link but not reported in validation report")

    def test_process_link(self):
        """Tests against 1006"""
        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'process_link.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['errors'] if
                            "Object reference #process/1 not declared" in m['message']]
        if len(object_ref_error) > 0:
            self.fail(
                "Validation error present when should pass without error - process link reports broken when present in data")

        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'process_link_fail.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['errors'] if
                            "Object reference #process/1 not declared" in m['message']]
        if len(object_ref_error) == 0:
            self.fail(
                "Validation error missing when should report error - data has broken process link but not reported in validation report")

    def test_protocol_ref_link(self):
        """Tests against 1007"""
        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'protocol_ref_link.json')))
        if "['#protocol/1'] used in a study or assay process sequence not declared" in log_msg_stream.getvalue():
            self.fail(
                "Validation error present when should pass without error - executesProtocol link reports broken when present in data")
        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'protocol_ref_link_fail.json')))
        if "['#protocol/1'] used in a study or assay process sequence not declared" not in log_msg_stream.getvalue():
            self.fail(
                "Validation error missing when should report error - data has broken executesProtocol link but not reported in validation report")

    # TODO: Got to here in refactoring tests to use new validator reporting method

    def test_factor_link(self):
        """Tests against 1008"""
        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'factor_link.json')))
        if len(object_ref_error) > 0:
            self.fail(
                "Validation error present when should pass without error - factor link in factorValue reports broken when present in data")

        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'factor_link_fail.json')))
        if len(object_ref_error) == 0:
            self.fail(
                "Validation error missing when should report error - data has broken factor link in factorValue but not reported in validation report")

    def test_protocol_parameter_link(self):
        """Tests against 1009"""
        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'protocol_parameter_link.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['errors'] if
                            "Object reference #parameter/1 not declared" in m['message']]
        if len(object_ref_error) > 0:
            self.fail(
                "Validation error present when should pass without error - parameter link in parameterValue reports broken when present in data")

        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'protocol_parameter_link_fail.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['errors'] if
                            "Object reference #parameter/1 not declared" in m['message']]
        if len(object_ref_error) == 0:
            self.fail(
                "Validation error missing when should report error - data has broken parameter link in parameterValue but not reported in validation report")

    def test_iso8601(self):
        """Tests against 3001"""
        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'iso8601.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['warnings'] if
                            "Date 2008-08-15 does not conform to ISO8601 format" in m['message']]
        if len(object_ref_error) > 0:
            self.fail(
                "Validation error present when should pass without error - incorrectly formatted ISO8601 date in publicReleaseDate reports invalid when valid data")

        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'iso8601_fail.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['warnings'] if
                            "Date 15/08/2008 does not conform to ISO8601 format" in m['message']]
        if len(object_ref_error) == 0:
            self.fail(
                "Validation error missing when should report error - data has incorrectly formatted ISO8601 date in publicReleaseDate but not reported in validation report")

    def test_doi(self):
        """Tests against 3002"""
        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'doi.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['warnings'] if
                            "DOI 10.1371/journal.pone.0003042 does not conform to DOI format" in m['message']]
        if len(object_ref_error) > 0:
            self.fail(
                "Validation error present when should pass without error - incorrectly formatted DOI in publication reports invalid when valid data")

        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'doi_fail.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['warnings'] if
                            "DOI 1371/journal.pone.0003042 does not conform to DOI format" in m['message']]
        if len(object_ref_error) == 0:
            self.fail(
                "Validation error missing when should report error - data has incorrectly formatted DOI in publication but not reported in validation report")

    def test_pubmed(self):
        """Tests against 3003"""
        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'pubmed.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['warnings'] if
                            "PubMed ID 18725995 is not valid format" in m['message']]
        if len(object_ref_error) > 0:
            self.fail(
                "Validation error present when should pass without error - incorrectly formatted Pubmed ID in publication reports invalid when valid data")

        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'pubmed_fail.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['warnings'] if
                            "PubMed ID 1872599 is not valid format" in m['message']]
        if len(object_ref_error) == 0:
            self.fail(
                "Validation error missing when should report error - data has incorrectly formatted Pubmed ID in publication but not reported in validation report")

    def test_datafiles(self):
        """Tests against 3004"""
        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'datafiles.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['warnings'] if
                            "Cannot open file a_file.dat" in m['message']]
        if len(object_ref_error) > 0:
            self.fail(
                "Validation error present when should pass without error - incorrectly reports a_file.dat is missing when a_file.dat is present")

        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'datafiles_fail.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['warnings'] if
                            "Cannot open file b_file.dat" in m['message']]
        if len(object_ref_error) == 0:
            self.fail(
                "Validation error missing when should report error - data has incorrectly reported everything is OK but not reported b_file.dat is missing")

    def test_protocol_used(self):
        """Tests against 3005"""
        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'protocol_used.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['warnings'] if
                            "Object reference #protocol/1 not used anywhere in study loc 1 (study location autocalculated by validator - Study ID in JSON not present)" in m['message']]
        if len(object_ref_error) > 0:
            self.fail(
                "Validation error present when should pass without error - incorrectly reports #protocol/1 not used when it has been used in #process/1")

        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'protocol_used_fail.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['warnings'] if
                            "Object reference #protocol/1 not used anywhere in study loc 1 (study location autocalculated by validator - Study ID in JSON not present)" in m['message']]
        if len(object_ref_error) == 0:
            self.fail(
                "Validation error missing when should report error - data has incorrectly reported everything is OK but not reported #protocol/1 as being unused")

    def test_factor_used(self):
        """Tests against 3006"""
        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'factor_used.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['warnings'] if
                            "Object reference #factor/1 not used anywhere in study loc 1 (study location autocalculated by validator - Study ID in JSON not present)" in
                            m['message']]
        if len(object_ref_error) > 0:
            self.fail(
                "Validation error present when should pass without error - incorrectly reports #factor/1 not used when it has been used in #sample/1")

        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'factor_used_fail.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['warnings'] if
                            "Object reference #factor/1 not used anywhere in study loc 1 (study location autocalculated by validator - Study ID in JSON not present)" in
                            m['message']]
        if len(object_ref_error) == 0:
            self.fail(
                "Validation error missing when should report error - data has incorrectly reported everything is OK but not reported #factor/1 as being unused")

    def test_term_source_used(self):
        """Tests against 3007"""
        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'term_source_used.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['warnings'] if
                            "Object reference PATO not used anywhere in investigation (term source check)" in
                            m['message']]
        if len(object_ref_error) > 0:
            self.fail(
                "Validation error present when should pass without error - incorrectly reports PATO not used when it has been used in #factor/1")

        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'term_source_used_fail.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['warnings'] if
                            "Object reference PATO not used anywhere in investigation (term source check)" in
                            m['message']]
        if len(object_ref_error) == 0:
            self.fail(
                "Validation error missing when should report error - data has incorrectly reported everything is OK but not reported PATO as being unused")

# class ValidateIsaTabTest(TestCase):
#
#     def setUp(self):
#         self._dir = os.path.dirname(__file__)
#         self.reporting_level = INFO
#
#     def tearDown(self):
#         pass
#
#     def test_i_no_content(self):
#         with self.assertRaises(ValidationError):
#             isatab.validate_i_file(i_fp=open(os.path.join(self._dir, 'data', 'tab', 'invalid_i', 'i_01.txt')))
#
#     def test_i_no_required_labels(self):
#         with self.assertRaises(ValidationError):
#             isatab.validate_i_file(i_fp=open(os.path.join(self._dir, 'data', 'tab', 'invalid_i', 'i_02.txt')))
#
#     def test_i_valid_labels(self):
#         isatab.validate_i_file(i_fp=open(os.path.join(self._dir, 'data', 'tab', 'valid_i', 'i_01.txt')))
#
#     def test_i_content(self):
#         isatab.validate_i_file(i_fp=open(os.path.join(self._dir, 'data', 'tab', 'invalid_i', 'i_03.txt')))
