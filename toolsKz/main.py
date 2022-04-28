import os
import configparser

from src.dbPostalCodes.UpdatePostalCodes import UpdatePostalCodes
from src.dbOrgsContacts.UpdateOrgsContacts import UpdateOrgsContacts
from src.licenseMinCulture.ParsingMinCultLicenses import ParsingMinCultLicenses


if __name__ == "__main__":

    # a = ParsingMinCultLicenses()
    # a.runDataParsing()

    # a = UpdatePostalCodes()
    # a.processRun()

    a = UpdateOrgsContacts()
    a.processRun()
