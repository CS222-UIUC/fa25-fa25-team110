import importlib
import sys
import types
import unittest
from unittest import mock


def make_fake_streamlit(**overrides):
	m = types.ModuleType("streamlit")
	# Minimal attributes used by the apps
	m.session_state = {}
	m.query_params = {}
	m.set_page_config = lambda *a, **k: None
	m.link_button = lambda *a, **k: setattr(m, "_last_link", (a, k))
	m.title = lambda *a, **k: None
	m.rerun = lambda *a, **k: setattr(m, "_rerun_called", True)
	m.write = lambda *a, **k: None
	m.success = lambda *a, **k: setattr(m, "_last_success", a)
	m.error = lambda *a, **k: setattr(m, "_last_error", a)
	m.button = lambda *a, **k: False
	m.text_input = lambda *a, **k: ""
	# allow overrides for tests
	for k, v in overrides.items():
		setattr(m, k, v)
	return m


class LoginAndFrontendTests(unittest.TestCase):
	def setUp(self):
		# Ensure a fresh fake streamlit before importing modules that use it at top-level
		self.fake_st = make_fake_streamlit()
		sys.modules["streamlit"] = self.fake_st

	def tearDown(self):
		# Remove our injected fake so other tests/imports aren't affected
		sys.modules.pop("streamlit", None)
		# Also remove imported app modules so they re-import fresh in other tests
		sys.modules.pop("login", None)
		sys.modules.pop("frontend.app", None)

	def test_save_tokens_logged_in_and_auth_headers(self):
		login = importlib.import_module("login")

		# start with empty session
		self.assertFalse(login.logged_in())

		login.save_tokens("access-token", "refresh-token")
		self.assertTrue(login.logged_in())
		self.assertIn("auth", self.fake_st.session_state)
		self.assertEqual(self.fake_st.session_state["auth"]["access"], "access-token")

		headers = login.auth_headers()
		self.assertEqual(headers.get("Authorization"), "Bearer access-token")

	def test_parse_tokens_from_url_sets_tokens_and_clears_qp_and_reruns(self):
		login = importlib.import_module("login")

		# simulate query params present
		self.fake_st.query_params = {"access": "A", "refresh": "R"}
		# ensure no auth before
		self.fake_st.session_state = {}

		# call parse_tokens_from_url and assert it saved tokens, cleared qp and called rerun
		login.parse_tokens_from_url()

		self.assertIn("auth", self.fake_st.session_state)
		self.assertEqual(self.fake_st.session_state["auth"]["access"], "A")
		self.assertEqual(self.fake_st.query_params, {})
		self.assertTrue(getattr(self.fake_st, "_rerun_called", False))

	def test_login_button_uses_api_base(self):
		login = importlib.import_module("login")
		# call login_button
		login.login_button()
		# our fake stored last link args
		last = getattr(self.fake_st, "_last_link", None)
		self.assertIsNotNone(last)
		args, kwargs = last
		# first positional arg is the label, second is the url
		# our fake stores all positional args in a tuple
		# validate URL contains the expected path
		# The module-level API_BASE should be present
		expected = f"{login.API_BASE}/accounts/google/login/"
		# The link_button invocation uses label then url per login.py
		self.assertIn(expected, args[1])

	def test_frontend_app_shows_success_on_valid_credentials(self):
		# prepare fake streamlit that returns username/password and records success/error
		def text_input(prompt, type=None):
			if "Username" in prompt:
				return "tester"
			if "Password" in prompt:
				return "secret"
			return ""

		def button(label):
			# simulate clicking the Login button
			return True

		fake = make_fake_streamlit(text_input=text_input, button=button)
		sys.modules["streamlit"] = fake

		# import the frontend app (executes top-level UI code)
		importlib.import_module("frontend.app")

		# after import, success should have been called with greeting
		self.assertTrue(hasattr(fake, "_last_success"))
		self.assertIn("tester", fake._last_success[0])

	def test_frontend_app_shows_error_when_missing_credentials(self):
		# simulate empty username/password and clicking Login
		def text_input(prompt, type=None):
			return ""

		def button(label):
			return True

		fake = make_fake_streamlit(text_input=text_input, button=button)
		sys.modules["streamlit"] = fake

		# re-import frontend.app
		importlib.import_module("frontend.app")

		# should have recorded an error
		self.assertTrue(hasattr(fake, "_last_error"))

	def test_login_shows_protected_endpoints_when_logged_in_ok(self):
		# Prepare fake streamlit that has an auth token and collects writes
		writes = []

		def write(*a, **k):
			writes.append(a)

		fake = make_fake_streamlit(write=write, button=lambda label: False)
		fake.session_state = {"auth": {"access": "tok", "refresh": "r"}}
		sys.modules["streamlit"] = fake

		# Mock requests.get to return OK responses for /api/me/ and /api/protected-data/
		with mock.patch("requests.get") as mock_get:
			mock_resp1 = mock.Mock()
			mock_resp1.ok = True
			mock_resp1.json.return_value = {"user": "me"}

			mock_resp2 = mock.Mock()
			mock_resp2.ok = True
			mock_resp2.json.return_value = {"data": "secret"}

			mock_get.side_effect = [mock_resp1, mock_resp2]

			importlib.import_module("login")

		# login.py should have called st.write twice with the expected tuples
		self.assertIn(("**/api/me**:", {"user": "me"}), writes)
		self.assertIn(("**/api/protected-data**:", {"data": "secret"}), writes)

	def test_login_shows_error_text_when_requests_fail(self):
		# Prepare fake streamlit that has an auth token and collects writes
		writes = []

		def write(*a, **k):
			writes.append(a)

		fake = make_fake_streamlit(write=write, button=lambda label: False)
		fake.session_state = {"auth": {"access": "tok", "refresh": "r"}}
		sys.modules["streamlit"] = fake

		# Mock requests.get to return non-OK responses
		with mock.patch("requests.get") as mock_get:
			mock_resp1 = mock.Mock()
			mock_resp1.ok = False
			mock_resp1.text = "fail1"

			mock_resp2 = mock.Mock()
			mock_resp2.ok = False
			mock_resp2.text = "fail2"

			mock_get.side_effect = [mock_resp1, mock_resp2]

			importlib.import_module("login")

		# login.py should have called st.write with error text for both endpoints
		self.assertIn(("**/api/me**:", "fail1"), writes)
		self.assertIn(("**/api/protected-data**:", "fail2"), writes)


if __name__ == "__main__":
	unittest.main()
