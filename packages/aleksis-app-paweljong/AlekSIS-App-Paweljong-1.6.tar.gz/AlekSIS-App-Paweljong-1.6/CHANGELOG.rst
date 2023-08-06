Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog`_,
and this project adheres to `Semantic Versioning`_.

`1.5.1`_
--------

Fixed
~~~~~

* Fix total amount calculation for event registrations with donations.

`1.5`_
------

Added
~~~~~

* Sync members of group with event registrations
* Add data check for sync of event members

`1.4.6`_
--------

Fixed
~~~~~

* Payment variant selection contained unavailable payment providers.

`1.4.5`_
--------

Fixed
~~~~~

* Implement get_billing_email_recipients() to get invoices send to guardians

`1.4.4`_
--------

Fixed
~~~~~

* Fixed URL to editPersonView

`1.4.3`_
--------

Fixed
-----

* Show link to person edit view on registration detail page
* Add get_person() method on EventRegistration model

`1.4.2`_
--------

Changed
~~~~~~~

* Align with Tezor 1.1
  * Add imaginary SKU to items
  * Return net prices in items
* Fix decimal type for donatiosn and discounts

`1.4.1`_
--------

* Fix a predicate granting privileges to participants

`1.4`_
------

Added
~~~~~

* Registration states
* Integration with Tezor
* Allow to configure email notification recipient for events

`1.3.2`_
--------

Changed
~~~~~~~

* Allow re-using mailings for multiple events by moving sent_to to the per-event table

`1.3.1`_
--------

Fixed
~~~~~

* Fix migration dependency

`1.3`_
------

Added
~~~~~

* Info mailings

Fixed
~~~~~

* Fix html syntax of date_registered email template
* Show date of birth in event_registered mail

`1.2`_
------

Added
~~~~~

* Implement account registration

Fixed
~~~~~

* Fix creation on email addresses
* Fix duplication of form fields in layout

`1.1`_
----------

Added
~~~~~

* Add link to public page to events list
* Add RSS feed of upcoming events
* Add slug field to Event model

Changed
~~~~~~~

* Beautify event information card
* Use consistent page and browser title

Fixed
~~~~~

* Typo in success_url of CreateEventView
* COnfirmation of retraction deadline was missing

`1.0`_
------

Added
~~~~~

* Initial release.


.. _Keep a Changelog: https://keepachangelog.com/en/1.0.0/
.. _Semantic Versioning: https://semver.org/spec/v2.0.0.html


.. _1.0: https://edugit.org/Teckids/hacknfun//AlekSIS-App-Paweljong/-/tags/1.0
.. _1.1: https://edugit.org/Teckids/hacknfun//AlekSIS-App-Paweljong/-/tags/1.1
.. _1.2: https://edugit.org/Teckids/hacknfun//AlekSIS-App-Paweljong/-/tags/1.2
.. _1.3: https://edugit.org/Teckids/hacknfun//AlekSIS-App-Paweljong/-/tags/1.3
.. _1.3.1: https://edugit.org/Teckids/hacknfun//AlekSIS-App-Paweljong/-/tags/1.3.1
.. _1.3.2: https://edugit.org/Teckids/hacknfun//AlekSIS-App-Paweljong/-/tags/1.3.2
.. _1.4: https://edugit.org/Teckids/hacknfun//AlekSIS-App-Paweljong/-/tags/1.4
.. _1.4.1: https://edugit.org/Teckids/hacknfun//AlekSIS-App-Paweljong/-/tags/1.4.1
.. _1.4.2: https://edugit.org/Teckids/hacknfun//AlekSIS-App-Paweljong/-/tags/1.4.2
.. _1.4.3: https://edugit.org/Teckids/hacknfun//AlekSIS-App-Paweljong/-/tags/1.4.3
.. _1.4.4: https://edugit.org/Teckids/hacknfun//AlekSIS-App-Paweljong/-/tags/1.4.4
.. _1.4.5: https://edugit.org/Teckids/hacknfun//AlekSIS-App-Paweljong/-/tags/1.4.5
.. _1.4.6: https://edugit.org/Teckids/hacknfun//AlekSIS-App-Paweljong/-/tags/1.4.6
.. _1.5: https://edugit.org/Teckids/hacknfun//AlekSIS-App-Paweljong/-/tags/1.5
.. _1.5.1: https://edugit.org/Teckids/hacknfun//AlekSIS-App-Paweljong/-/tags/1.5.1
