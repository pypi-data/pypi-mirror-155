import unittest

if __name__ == '__main__':

    # TODO update test suite to use Nose which automatically discovers tests cases
    testmodules = [
        'arthurai.tests.test_regression_model',
        'arthurai.tests.test_cv_model',
        'arthurai.tests.test_multistage_regression_model',
        'arthurai.tests.test_multistage_multiclass_model',
        'arthurai.tests.test_nlp_model',
    ]

    suite = unittest.TestSuite()

    for t in testmodules:
        try:
            # If the module defines a suite() function, call it to get the suite.
            mod = __import__(t, globals(), locals(), ['suite'])
            suitefn = getattr(mod, 'suite')
            suite.addTest(suitefn())
        except (ImportError, AttributeError):
            # else, just load all the test cases from the module.
            suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

    unittest.TextTestRunner().run(suite)


