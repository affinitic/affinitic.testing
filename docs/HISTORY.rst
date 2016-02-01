Changelog
=========

0.1.11 (2016-02-01)
-------------------

- Add IAnnotation to allow translate() on AdvancedTestRequest refs #7875
  [aurore]


0.1.10 (2015-07-16)
-------------------

- Do not use pkg_resources.get_distribution that is not working with Products.Transience
  [schminitz]


0.1.9 (2015-04-29)
------------------

- Avoid an error if Products.Transience is not available
  [mpeeters]


0.1.8 (2015-03-27)
------------------

- Add AdvancedTestRequest class : #6854


0.1.7 (2014-07-25)
------------------

- Fix a possible error with sql comments


0.1.6 (2014-07-22)
------------------

- Fix an error with some sql statements on multiple lines


0.1.5 (2014-07-22)
------------------

- Fix an error with mysql and multiple sql statements


0.1.4 (2014-07-01)
------------------

- Execute all sql instructions in one transaction

- Close database session after inserts


0.1.3 (2014-06-19)
------------------

- Ignore empty sql statements


0.1.2 (2014-05-27)
------------------

- Add sql_directory parameter for the database test case


0.1.1 (2013-11-27)
------------------

- Fix a problem with the mocking of properties


0.1 (2013-09-02)
----------------

- Initial release
