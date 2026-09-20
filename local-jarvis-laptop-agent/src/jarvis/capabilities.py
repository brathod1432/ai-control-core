"""Capability gate scaffolding for web, browser, screenshot, and app awareness."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .contracts import PermissionClass


class CapabilityKind(str, Enum):
    WEB_SURFING = "web_surfing"
    LOCAL_BROWSER_INSPECTION = "local_browser_inspection"
    SCREENSHOT_INSPECTION = "screenshot_inspection"
    APP_INSPECTION = "app_inspection"
    DESKTOP_AUTOMATION = "desktop_automation"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class CapabilityGateDecision:
    capability: CapabilityKind
    permission: PermissionClass
    approval_required: bool
    read_only: bool
    proposal_only: bool
    reason: str


def evaluate_capability_request(text: str) -> CapabilityGateDecision:
    """Classify capability requests before any future tool implementation."""

    normalized = " ".join(text.casefold().split())
    if _contains_any(normalized, ("http://", "https://", "www.", "browse to", "open website", "web surfing", "search the web")):
        return CapabilityGateDecision(
            capability=CapabilityKind.WEB_SURFING,
            permission=PermissionClass.NETWORK,
            approval_required=True,
            read_only=True,
            proposal_only=True,
            reason="Web surfing can contact external destinations and needs approval for the exact target.",
        )
    if _contains_any(normalized, ("chrome", "browser", "cdp", "localhost", "127.0.0.1")):
        return CapabilityGateDecision(
            capability=CapabilityKind.LOCAL_BROWSER_INSPECTION,
            permission=PermissionClass.AUTOMATE_APP,
            approval_required=True,
            read_only=True,
            proposal_only=True,
            reason="Local browser inspection should use an approved read-only Chrome/CDP target.",
        )
    if _contains_any(normalized, ("screenshot", "screen shot", "screen capture", "what is on my screen")):
        return CapabilityGateDecision(
            capability=CapabilityKind.SCREENSHOT_INSPECTION,
            permission=PermissionClass.AUTOMATE_APP,
            approval_required=True,
            read_only=True,
            proposal_only=True,
            reason="Screenshots may contain private data and require approval before capture or inspection.",
        )
    if _contains_any(normalized, ("active window", "app inspection", "inspect app", "desktop app", "window state")):
        return CapabilityGateDecision(
            capability=CapabilityKind.APP_INSPECTION,
            permission=PermissionClass.AUTOMATE_APP,
            approval_required=True,
            read_only=True,
            proposal_only=True,
            reason="App inspection is local and read-only first, but still needs approval because it can expose private UI state.",
        )
    if _contains_any(normalized, ("click", "type", "press", "submit", "full desktop automation", "control my desktop")):
        return CapabilityGateDecision(
            capability=CapabilityKind.DESKTOP_AUTOMATION,
            permission=PermissionClass.AUTOMATE_APP,
            approval_required=True,
            read_only=False,
            proposal_only=True,
            reason="Unsafe full desktop automation is not implemented yet; Jarvis can only propose a safe plan.",
        )
    return CapabilityGateDecision(
        capability=CapabilityKind.UNKNOWN,
        permission=PermissionClass.NONE,
        approval_required=False,
        read_only=True,
        proposal_only=True,
        reason="No browser, screenshot, app, or desktop capability request was detected.",
    )


def _contains_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(term in text for term in terms)
