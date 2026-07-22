# Test Report

## Environment

Simulator: Webots R2025

Robot: e-puck

Language: Python

---

## Test Cases

| Test | Result |
|-------|--------|
| Straight Corridor | ✅ Pass |
| Left Turn | ✅ Pass |
| Right Turn | ✅ Pass |
| Dead End Recovery | ✅ Pass |
| T Junction | ✅ Pass |
| Long Corridor | ✅ Pass |

---

## Controller Parameters

| Parameter | Value |
|-----------|-------|
| Forward Speed | 3.0 |
| Turn Speed | 2.0 |
| Side Threshold | 100 |
| Front Threshold | 180 |
| 90° Turn Steps | 17 |
| 180° Turn Steps | 35 |
| Junction Clear Steps | 10 |

---

## Summary

The robot successfully completed navigation tasks using the Left-Hand Rule.

Observed capabilities:

- Stable wall detection
- Reliable turning
- Dead-end recovery
- State-based navigation

Known limitations:

- No mapping
- No localization
- No shortest-path optimization
- Static environments only