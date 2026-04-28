from __future__ import annotations

import unittest

from jarvis.capabilities import CapabilityKind, evaluate_capability_request
from jarvis.contracts import PermissionClass


class CapabilityGateTests(unittest.TestCase):
    def test_web_surfing_requires_exact_approval(self) -> None:
        decision = evaluate_capability_request("Browse to https://example.com")

        self.assertIs(decision.capability, CapabilityKind.WEB_SURFING)
        self.assertIs(decision.permission, PermissionClass.NETWORK)
        self.assertTrue(decision.approval_required)
        self.assertTrue(decision.proposal_only)

    def test_local_browser_inspection_is_read_only_and_approval_gated(self) -> None:
        decision = evaluate_capability_request("Inspect Chrome via CDP")

        self.assertIs(decision.capability, CapabilityKind.LOCAL_BROWSER_INSPECTION)
        self.assertIs(decision.permission, PermissionClass.AUTOMATE_APP)
        self.assertTrue(decision.read_only)
        self.assertTrue(decision.approval_required)

    def test_screenshot_and_app_inspection_are_approval_gated(self) -> None:
        screenshot = evaluate_capability_request("Take a screenshot")
        app = evaluate_capability_request("Inspect the active window")

        self.assertIs(screenshot.capability, CapabilityKind.SCREENSHOT_INSPECTION)
        self.assertTrue(screenshot.approval_required)
        self.assertTrue(screenshot.read_only)

        self.assertIs(app.capability, CapabilityKind.APP_INSPECTION)
        self.assertTrue(app.approval_required)
        self.assertTrue(app.read_only)

    def test_desktop_automation_remains_proposal_only(self) -> None:
        decision = evaluate_capability_request("Click submit and type my password")

        self.assertIs(decision.capability, CapabilityKind.DESKTOP_AUTOMATION)
        self.assertFalse(decision.read_only)
        self.assertTrue(decision.proposal_only)


if __name__ == "__main__":
    unittest.main()
