"""
This is only for internal use
"""

import pandas as pd

try:
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
except ImportError as e:
    print("Please install the following packages: \n"
          "pip3 install gspread \n"
          "pip3 install --upgrade google-api-python-client oauth2client")
    raise e


class AllInOneTable:
    def __init__(self, sheet='All-in-one Table'):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

        # add credentials to the account
        CREDENTIAL_PATH = '/gale/netapp/cemba3c/BICCN/wmb/google_sheet_service.json'
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIAL_PATH, scope)

        # authorize the client sheet
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open(sheet)

    def get_sheet(self, sheet_name):
        sheet = self.sheet.worksheet(sheet_name)
        head, *data = sheet.get_values()
        return pd.DataFrame(data, columns=head)

    def get_gene_sheet(self):
        return self.get_sheet('Gene')

    def get_brain_region_sheet(self):
        return self.get_sheet('BICCN.BrainRegionMetadata').set_index('NumericValue')
