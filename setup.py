from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    # TODO: add any additional package requirements here
    'charlesbot',
]

test_requirements = [
    # TODO: add any additional package test requirements here
    'asynctest',
    'coverage',
    'flake8',
]

setup(
    name='charlesbot-pagerduty-escalations',
    version='0.1.0',
    description="Plugin to create an incident in Pagerduty and assign it to a specific team",
    long_description=readme,
    author="FreshBooks",
    author_email='morpheus@freshbooks.com',
    url='https://github.com/freshbooks/charlesbot-pagerduty-escalations',
    packages=[
        'charlesbot_pagerduty_escalations',
    ],
    package_dir={'charlesbot_pagerduty_escalations':
                 'charlesbot_pagerduty_escalations'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='slack robot chatops charlesbot charlesbot-pagerduty-escalations',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='nose.collector',
    tests_require=test_requirements
)
