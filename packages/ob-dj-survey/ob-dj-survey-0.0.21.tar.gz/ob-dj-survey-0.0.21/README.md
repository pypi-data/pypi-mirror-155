# OBytes Django Survey App

[![Build & Test](https://github.com/obytes/ob-dj-survey/actions/workflows/test-build.yml/badge.svg)](https://github.com/obytes/ob-dj-survey/actions/workflows/test-build.yml)
[![Publish to PyPI](https://github.com/obytes/ob-dj-survey/actions/workflows/release.yml/badge.svg)](https://github.com/obytes/ob-dj-survey/actions/workflows/release.yml)

Survey Django Application is designed to be a simple and easy to use survey application for Django, which can be used to collect data from users.

## Quick start

1. Install `ob-dj-survey` latest version `pip install ob-dj-survey`

2. Add "ob_dj_survey" to your `INSTALLED_APPS` setting like this:

```python
   # settings.py
   INSTALLED_APPS = [
        ...
        "ob_dj_survey.core.survey",
   ]
```

3. Include the  URLs in your project urls.py like this:

```python
   # urls.py
   path("survey/", include("ob_dj_survey.apis.survey.urls")),
```

4. Run ``python manage.py migrate`` to create the survey models.

## Developer Guide

1. Clone github repo `git clone [url]`

2. `pipenv install --dev`

3. `pre-commit install`

4. Run unit tests `make test`
