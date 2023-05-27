import os.path

from wx import FileConfig


class Config:
    inventree_server = ""
    inventree_username = ""
    inventree_password = ""
    inventree_apikey = ""

    inventree_pca_category = "Assemblies"
    inventree_pcb_category = "Printed-Circuit Boards"

    def __init__(self, local_dir):
        # This is how ibom determines config locations
        self.local_config_file = os.path.join(local_dir, "inventree-bom.config.ini")
        self.global_config_file = os.path.join(
            os.path.dirname(__file__), "..", "config.ini"
        )

    def load_from_ini(self):
        """Init from config file if it exists."""
        if os.path.isfile(self.local_config_file):
            file = self.local_config_file
        elif os.path.isfile(self.global_config_file):
            file = self.global_config_file
        else:
            return

        f = FileConfig(localFilename=file)

        f.SetPath("/inventree")
        self.inventree_server = f.Read("server", self.inventree_server)
        self.inventree_username = f.Read("username", self.inventree_username)
        self.inventree_password = f.Read("password", self.inventree_password)
        self.inventree_apikey = f.Read("apikey", self.inventree_apikey)

        self.inventree_pca_category = f.Read(
            "pca_category", self.inventree_pca_category
        )
        self.inventree_pcb_category = f.Read(
            "pcb_category", self.inventree_pcb_category
        )
