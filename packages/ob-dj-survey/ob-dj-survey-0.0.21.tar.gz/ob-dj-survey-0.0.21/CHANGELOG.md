# Changelog

## 0.0.13

### What's new

- Allow Update Survey Answers For a User, on Every Submission.

**Full Changelog**: <https://github.com/obytes/ob-dj-survey/compare/0.0.12...0.0.13>


## 0.0.12

### What's new

- Remove `fieldset` from django-admin.py to allow djang-translations to render the language fields
- Specify the `field` in the `UserSerializer`

**Full Changelog**: <https://github.com/obytes/ob-dj-survey/compare/0.0.11...0.0.12>


## 0.0.11

### What's new

- Add `meta` field of type JSON to questions, choices and survey.
- Change `SurveyAnswers` to `SurveyAnswer` model.
- Remove `section` field from Survey Model.

**Full Changelog**: <https://github.com/obytes/ob-dj-survey/compare/0.0.10...0.0.11>

## 0.0.10

### What's new

- Allow Question to be linked to multiple Surveys.
- Allow Choices To be Linked to Multiple Questions.
- Enhance Admin Fields/Data Display.
- Added bash command in Makefile to access container for debugging purposes.

**Full Changelog**: <https://github.com/obytes/ob-dj-survey/compare/0.0.9...0.0.10>

## 0.0.9

### What's new

- Add `description` field `questions` and `choices` as optional value.
- Return The Optional Fields in the serializer and make them available for edit in the admin panel.

**Full Changelog**: <https://github.com/obytes/ob-dj-survey/compare/0.0.8...0.0.9>

## 0.0.8

### What's new

- Added `SubmissionType` For `Survey` Model to set if user will submit all answers or just a few.
- Added Survey Model Validations.
- Set Questions under `Section` Model.
- Deleted `Category` Model.

**Full Changelog**: <https://github.com/obytes/ob-dj-survey/compare/0.0.7...0.0.8>

## 0.0.7

### What's new

- Return survey name in the API Serializer
- Return IDs instead of PK'sin the API Serializer

**Full Changelog**: <https://github.com/obytes/ob-dj-survey/compare/0.0.6...0.0.7>

## 0.0.6

### What's new

- Display Survey-Name on `__str__()`
- Display survey name in Django Admin.

**Full Changelog**: <https://github.com/obytes/ob-dj-survey/compare/0.0.5...0.0.6>

## 0.0.5

### What's new

- Adds unique name field to survey model.
- Add Unit Testing for Admin Panel & Migrations.
- Group all APIs Endpoints in one Tag.

**Full Changelog**: <https://github.com/obytes/ob-dj-survey/compare/0.0.4...0.0.5>

## 0.0.4

### What's new

- Show questions and choices in survey details.
- Serializer for survey details.

**Full Changelog**: <https://github.com/obytes/ob-dj-survey/compare/0.0.3...0.0.4>

## 0.0.3

### What's new

- Listing Surveys APIs & Return Only Active Surveys.
- Create an API to Submit Answers for a Survey.
- Add Slack Notification for new releases.

**Full Changelog**: <https://github.com/obytes/ob-dj-survey/compare/0.0.2...0.0.3>

## 0.0.2

### What's new

- Update Readme File & Fix some typos.

**Full Changelog**: <https://github.com/obytes/ob-dj-survey/compare/0.0.1...0.0.2>

## 0.0.1

- Fix Tests & Add `FactoryBoy` For New Models.
- Refactor code & Create Flexible Tests.
- Updated Makefile, Added PR template.
- Refactored tests & Update Github Workflows.
- Documented the Package to be used in Django APP.
- Create Endpoints for listing Surveys
- Bump Requirements & Upgrade some Dependencies.
- Add docs & auto versionning.

**Full Changelog**: <https://github.com/obytes/ob-dj-survey/commits/0.0.1>
