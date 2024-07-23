#python

import os
from unittest import TestCase, mock
from ebscopy import edsapi

class ParseHighlight(TestCase):
    def test_working(self):
        output = edsapi._parse_highlight("first &lt;highlight&gt;term&lt;/highlight&gt; last")
        self.assertEqual(output["orig"], "first &lt;highlight&gt;term&lt;/highlight&gt; last")
        self.assertEqual(output["clean"], "first term last")
        self.assertEqual(output["start_pos"], 6)
        self.assertEqual(output["end_pos"], 10)

    def test_html_highlight(self):
        output = edsapi._parse_highlight("first <highlight>term</highlight> last")
        self.assertEqual(output["orig"], "first <highlight>term</highlight> last")
        self.assertEqual(output["clean"], "first <highlight>term</highlight> last")
        self.assertEqual(output["start_pos"], 0)
        self.assertEqual(output["end_pos"], 0)

    def test_no_highlight(self):
        output = edsapi._parse_highlight("first term last")
        self.assertEqual(output["orig"], "first term last")
        self.assertEqual(output["clean"], "first term last")
        self.assertEqual(output["start_pos"], 0)
        self.assertEqual(output["end_pos"], 0)


class GetItemData(TestCase):
    data = [
            {"Name": "Title", "Data": "The Title"},
            {"Name": "Author", "Data": "The Author"},
            {"Group": "A", "Data": "1"},
            {"Group": "B", "Data": "1"},
    ]
    def test_core_valid(self):
        output = edsapi._get_item_data(self.data, "Name", "Title")
        self.assertEqual(output, "The Title")

    def test_core_missing(self):
        output = edsapi._get_item_data(self.data, "Name", "Subject")
        self.assertIsNone(output)

    def test_name_valid(self):
        output = edsapi._get_item_data_by_name(self.data, "Title")
        self.assertEqual(output, "The Title")

    def test_group_valid(self):
        output = edsapi._get_item_data_by_group(self.data, "A")
        self.assertEqual(output, "1")

@mock.patch.dict(os.environ, {"EDS_USER": "fake_user", "EDS_PASS": "fake_password", "EDS_ORG": "", "EDS_PROFILE": ""})
class UseOrGet(TestCase):
    def test_in_env(self):
        output = edsapi._use_or_get("user_id", "")
        self.assertEqual(output, "fake_user")

    def test_not_in_env(self):
        output = edsapi._use_or_get("profile", "fake_profile")
        self.assertEqual(output, "fake_profile")

    def test_missing_value(self):
        with self.assertRaises(ValueError):
            edsapi._use_or_get("org", "")

    def test_bad_kind(self):
        with self.assertRaises(KeyError):
            edsapi._use_or_get("bad_kind", "")

class GetOrUse(TestCase):
    @mock.patch.dict(os.environ, {"EDS_BASE_HOST": "env_host"})
    def test_no_value_passed(self):
        output = edsapi._get_or_use("base_host", "")
        self.assertEqual(output, "env_host")

    @mock.patch.dict(os.environ, {"EDS_BASE_HOST": "env_host"})
    def test_value_passed(self):
        output = edsapi._get_or_use("base_host", "passed_host")
        self.assertEqual(output, "env_host")

    @mock.patch.dict(os.environ, {"EDS_BASE_HOST": ""})
    def test_empty_variable_in_env(self):
        output = edsapi._get_or_use("base_host", "passed_host")
        self.assertEqual(output, "passed_host")

    def test_no_variable_in_env(self):
        # May want to capture the actual value and put it back later
        os.environ.pop('EDS_BASE_HOST', None)
        output = edsapi._get_or_use("base_host", "passed_host_2")
        self.assertEqual(output, "passed_host_2")

    def test_no_variable_in_env_and_no_param(self):
        with self.assertRaises(ValueError):
            edsapi._get_or_use("base_host")

class Uniq(TestCase):
    def test_has_dupes(self):
        output = edsapi._uniq(["one", "two", "one", "two", "three"])
        self.assertEqual(output,["one", "two", "three"])

    def test_no_dupes(self):
        output = edsapi._uniq(["one", "two", "three"])
        self.assertEqual(output,["one", "two", "three"])


# EOF
