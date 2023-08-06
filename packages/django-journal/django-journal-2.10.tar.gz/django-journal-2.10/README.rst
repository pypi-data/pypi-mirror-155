Journal application
===================

Log event to a journal. Keep details of the event linked to the event message,
keep also the template for displaying the event in case we want to improve
display.

To use just do::

      import django_journal
      django_journal.record('my-tag', '{user} did this to {that}',
                 user=request.user, that=model_instance)

Code Style
==========

black is used to format the code, using these parameters::

    black --target-version py37 --skip-string-normalization --line-length 110

There is .pre-commit-config.yaml to use pre-commit to automatically run black
before commits. (execute `pre-commit install` to install the git hook.)

isort is used to format the imports, using these parameter::

    isort --profile black --line-length 110

pyupgrade is used to automatically upgrade syntax, using these parameters::

    pyupgrade --keep-percent-format --py37-plus

There is .pre-commit-config.yaml to use pre-commit to automatically run black,
isort and pyupgrade before commits. (execute `pre-commit install` to install
the git hook.)

Admin display
-------------

``admin.JournalModelAdmin`` recompute messages from the journal message as HTML
adding links for filtering by object and to the ``change`` admin page for the
object if it has one.

Recording error events
----------------------

If you use transactions you must use ``error_record()`` instead of
``record()`` and set ``JOURNAL_DB_FOR_ERROR_ALIAS`` in your settings to
define another db alias to use so that journal record does not happen
inside the current transaction.
