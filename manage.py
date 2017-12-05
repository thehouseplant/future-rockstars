import unittest
import coverage
from flask_script import Manager
from app import app


COV = coverage.coverage(
    branch=True,
    include=[
        'app/*',
        'assign_bands.py',
        'assign_bands2.py',
        'assign_dorms.py'
    ],
    omit=[
        'app/__init__.py'
    ]
)
COV.start()


manager = Manager(app)


@manager.command
def tests():
    tests = unittest.TestLoader().discover('./', pattern='test*.py')
    result = unittest.TextTestResult(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def coverage():
    tests = unittest.TestLoader().discover('./', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage results: ')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
