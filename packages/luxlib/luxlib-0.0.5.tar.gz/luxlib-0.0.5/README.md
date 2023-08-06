# LuxLIB

LuxLIB est une librairie Python permettant la mise à jour automatique depuis un serveur. Mais aussi de pouvoir mettre à jour son serveur depuis le client.

## Installation

Pour installer LuxLIB, il faudra utiliser [pip](https://pip.pypa.io/en/stable/).

```bash
pip install luxlib
```

## Utilisation

```python
import luxlib

# Pour le télécharger
#Initialisation de la classe
downloader = luxlib.Downloader("LIEN (ip ou url)", "NAME_FOLDER_CLIENT", custom_java=True or False, logger=True or False, sftp=True or False, user="USERNAME SFTP", password="PASSWORD SFTP", main_dir="DIRECTORY SERVER")

#Affichage du récapitulatif
downloader.get_recap()

# Démarrage de la mise à jour
downloader.update()

# Pour la mise à jour serveur
# Initialisation de la classe
updater = luxlib.Updater("IP", "USERNAME", "PASSWORD", dir='CLIENT', dir_server='SERVER', logger=True or False)
```

## License
[MIT](https://choosealicense.com/licenses/mit/)