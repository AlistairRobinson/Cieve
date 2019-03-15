# Cieve

[![Build Status](https://travis-ci.com/AlistairRobinson/Cieve.svg?token=yo6eYpNXTG4DQuQTZxZz&branch=master)](https://travis-ci.com/AlistairRobinson/Cieve) [![Build Status](https://travis-ci.com/AlistairRobinson/Cieve.svg?token=yo6eYpNXTG4DQuQTZxZz&branch=develop)](https://travis-ci.com/AlistairRobinson/Cieve)

Cieve, a machine learning recruitment system

## Overview

The 2019 DBCampus Project was to develop a prototype smart application system for use by Deutsche Bank. This task was given to all second year Computer Science students at the University of Warwick with the intention of pushing students software development boundaries, in a business environment. We, Team Cieve, believe that we have developed a recruitment system more than capable of not only meeting, but surpassing the requirements given by our client.

Notable features:

 - Applicants are scored on submitted data using machine learning, which can be used to route applicants to better suited roles automatically
 - Recruiters can track and advance applicant progress and have the final say on whether application is accepted
 - Vacancy staging progress can be customised during job creation to allow for flexibility across client departments
 - Recruiters can modify machine learning weights via a custom dashboard
 - Extensive security considerations, from web application vulnerabilities to online phishing scams
 - Mobile first user interface
 - Comprehensive unit testing framework
 - Compliance with GDPR and DPA 2018

## System Requirements

Cieve has been developed with portability and platform independence in mind. As such, the only system requirements for the application are:

 - Python 2.7 or above
 - An internet connection

## Usage

### Application

Cieve has been designed with portability in mind. We recommend installing Cieve locally in a [Python virtual environment](https://docs.python.org/3/library/venv.html). 

Once the environment has been configured and activated, installation of third party Python dependencies will be required. Please see the dependency list in `requirements.txt`. Run the following script in the project's root directory `/` to activate the Cieve web server on `localhost:5000`:

    pip install -r requirements.txt
    export FLASK_APP=flaskr
    python -m flask run

### Unit Testing Framework

To activate the unit testing framework, run the following script in the project's root directory `/`. The testing framework will automatically generate an instance of the Cieve web server if it is not currently running.

    python -m pytest -v

## Future Development Roadmap

The following features are planned for later releases of Cieve:

 - Better lie detection in applications
 - Demographic data for recruiters
 - Improved feedback for applicants
 - Online coding platform for tests
 - Better applicant report for recruiters

 ## Authors

 Cieve was developed by the following team:

 - [Felix Gaul](https://github.com/XilefG), Database Engineer
 - [Nathan Hall](https://github.com/hallnath1), Project Manager
 - [Josh Hankins](https://github.com/joshhankins), Lead Designer
 - [Abdul Kamal](https://github.com/ayydeji), Business Analyst
 - [Alistair Robinson](https://github.com/AlistairRobinson), Data Protection Officer
 - [Justas Tamulis](https://github.com/JustasTamulis), Machine Learning Developer

## Acknowledgements

We would like to thank our module tutor, Marcus King, for his assistance during the development of this project.
