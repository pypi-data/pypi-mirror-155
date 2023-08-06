"""
.. module:: config.py

setup.py
******

:Description: setup.py

    Configuration file for apafib python package

:Authors:
    bejar

:Version: 

:Date:  06/05/2022
"""


DATALINK = "http://www.cs.upc.edu/~bejar/datasets/"

datasets = {
    "Concrete Slump Test": (10, "slump_test"),
    "auto mpg": (10, "auto-mpg"),
    "HCV data": (10, "hcvdat"),
    "ILPD": (10, "ILPD"),
    "apendicitis": (10, "apendicitis"),
    "glass2": (10, "glass"),
    "rmftsa_ladata": (10, "rmftsa_ladata"),
    "telco-customer-churn": (10, "telco-customer-churn"),
}