# SkillTrack — Testing Basics

## Why We Test

Automated tests help verify that API endpoints behave as expected and that existing features continue working after code changes.

## Testing Tools

- **pytest:** Runs automated tests and reports failures.
- **FastAPI TestClient:** Sends requests to API endpoints during tests.
- **assert:** Checks whether an actual result matches the expected result.

## What We Test in SkillTrack

- Successful course and lesson creation.
- Authentication and role-based access.
- Instructor ownership of courses and lessons.
- Student enrollment and duplicate enrollment prevention.
- Retrieving, updating, and deleting resources.
- Handling missing courses and lessons.

## Common HTTP Status Codes

- `200 OK` — Request succeeded.
- `201 Created` — A resource was created.
- `204 No Content` — Request succeeded without a response body.
- `403 Forbidden` — The user is not permitted to perform the action.
- `404 Not Found` — The requested resource does not exist.

## Testing Principle

A passing test confirms the specific behavior checked by that test. It does not guarantee that every possible edge case has been tested.
