"""
LuxLIB by Valentin Thuillier alias LuxFerre
"""

import hashlib
import os
import urllib.request as r
from pypresence import Presence
import pysftp

def get_md5(dir_file):
    """
    Récuperer le MD5 d'un fichier spécifié

    param:
    dir_file: string (directory or just file_name)

    return type: string (md5)
    """

    md5_hash = hashlib.md5()
    try:
        with open(dir_file, 'rb') as file:
            for chunk in iter(lambda: file.read(4096), b""):
                md5_hash.update(chunk)
    except: pass        
    return md5_hash.hexdigest()

def is_a_file(dir_fname):
    actual_dir = os.getcwd()
    try:
        os.chdir(dir_fname)
        os.chdir(actual_dir)
        return False
    except:
        return True

def get_all_file(start_dir: str): # Pb
    original_path = os.getcwd()
    if("/" != start_dir[-1]): start_dir += '/'
    os.chdir(start_dir)
    all_files = os.listdir()
    x = False
    for elt in all_files:
        if not(is_a_file(start_dir + elt)): x = True
    if not(x): return all_files
    files = []
    for elt in all_files:
        if not(is_a_file(start_dir + elt)):
            os.chdir(original_path)
            files.append({elt: get_all_file(start_dir + elt + '/')})
        else: files.append(elt)
    return files

def get_good_formate(all_file: list, started='') -> list:
    final = []
    for elt in all_file:
        if(isinstance(elt, str)): final.append(started + elt)
        else: final.append(get_good_formate(list(elt.values())[0], started=started + list(elt.keys())[0] + '/'))
    return final

def set_on_just_list(all_file_formated: list) -> list:
    liste = all_file_formated.copy()
    if(liste == []): return []
    elif(isinstance(liste[0], list)):
        l = liste.pop(0)
        return set_on_just_list(l) + set_on_just_list(liste)
    x = liste.pop(0)
    return [x] + set_on_just_list(liste)

def generate_downloader(start_dir: str, output_dir: str, name="downloader.lxf"):
    original_path = os.getcwd()
    if("/" != start_dir[-1]): start_dir += '/'
    liste = set_on_just_list(get_good_formate(get_all_file(start_dir)))
    os.chdir(output_dir)
    if(name in os.listdir()): os.remove(name)
    with open(name, 'a', encoding='UTF-8') as file:
        for elt in liste:
            file.write(elt + '|' + get_md5(start_dir + elt) + '\n')
    os.chdir(original_path)



def init_server_sftp(ip_server: str, user: str, password: str, dir_name: str):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    with pysftp.Connection(host=ip_server, username=user, password=password, cnopts=cnopts) as sftp:
        splited = spliter(dir_name)
        dir = ""
        for elt in splited:
            dir = elt
            try:
                sftp.mkdir(elt)
                sftp.cd(dir)
            except: sftp.cd(dir)
    with pysftp.Connection(host=ip_server, username=user, password=password, cnopts=cnopts) as sftp:
        print(dir)
        sftp.cd(dir)
        if("downloader.lxf" in os.listdir()): d = True
        else: d = False
        if("ignore.lxf" in os.listdir()): i = True
        else: i = False
        with open("downloader.lxf", 'a'): pass
        with open("ignore.lxf", 'a'): pass
        sftp.put("downloader.lxf", dir + "downloader.lxf")
        sftp.put("ignore.lxf", dir + "downloader.lxf")
        if(not d): os.remove("downloader.lxf")
        if(not i): os.remove("ignore.lxf")
        sftp.mkdir(dir + "files")

class Downloader:
    def __init__(self, url_server: str, name_folder: str, custom_java: bool, logger=False, sftp=False, user='', password='', main_dir='') -> None:
        self.__path = os.getcwd()
        self.__url = url_server
        self.__folder = name_folder
        self.__logger = logger
        self.__custom_java = custom_java
        if('.' != self.__folder[0]): self.__folder = '.' + self.__folder
        if('/' != self.__url[-1]): self.__url += '/'
        self.__folder_dir = os.getenv('APPDATA') + "\\" + self.__folder
        self.__sftp = sftp
        try:
            os.chdir(self.__folder_dir)
            os.chdir(self.__path)
        except:
            os.chdir(os.getenv('APPDATA'))
            os.mkdir(self.__folder)
            os.chdir(self.__path)

        if not(self.__sftp):
            try:
                os.chdir(self.__folder_dir)
                if("downloader.lxf" in os.listdir()): os.remove("downloader.lxf")
                if(self.__logger): print("Téléchargement du fichier downloader.lxf")
                r.urlretrieve(self.__url + "downloader.lxf", "downloader.lxf")
                if("ignore.lxf" in os.listdir()): os.remove("ignore.lxf")
                if(self.__logger): print("Téléchargement du fichier ignore.lxf")
                r.urlretrieve(self.__url + "ignore.lxf", "ignore.lxf")
            except: raise Exception("Problème durant la récupération des informations de téléchargement !")
        else:
            self.__user = user
            self.__password = password
            self.__dir_sftp = main_dir
            self.__ip = url_server
            self.__cnopts = pysftp.CnOpts()
            self.__cnopts.hostkeys = None
            os.chdir(self.__folder_dir)
            with pysftp.Connection(host=self.__ip, username=self.__user, password=self.__password, private_key='.ppk', cnopts=self.__cnopts) as sftp:
                if(self.__logger): print("Connexion faite au serveur sftp !")
                sftp.get(self.__dir_sftp + "downloader.lxf", "downloader.lxf")
                sftp.get(self.__dir_sftp + "ignore.lxf", "ignore.lxf")


        if(self.__logger): print("Lecture du fichier downloader.lxf")
        self.__data_serv = self.read_downloader()
        if(self.__logger): print("Génération et lecture des fichiers client")
        self.generate_have_file()
        self.__data_client = self.read_downloader(name="actual_file.lxf")
        os.chdir(os.getenv('APPDATA'))
        if(self.__folder not in os.listdir()): os.mkdir(self.__folder)

        # Fichier problème
        self.__miss = self.check_miss_file()
        self.__changed = self.check_changed_file()
        self.__not_in = self.check_not_in_downloader()

        os.chdir(self.__path)
        if(self.__logger): print("Lecture du fichier ignore")
        self.__ignore = self.read_ignore()
        os.chdir(self.__folder_dir)

        if(self.__logger): print("Comparaison des informations des fichiers compris et les fichiers ignorés")
        for ignore in self.__ignore:
            for not_in in self.__not_in:
                if(ignore in not_in): self.__not_in.remove(not_in)

        self.__updated = False



    def get_url(self): return self.__url
    def get_data_server(self): return self.__data_serv
    def get_data_client(self): return self.__data_client
    def get_folder_dir(self): return self.__folder_dir
    def get_folder(self): return self.__folder
    def get_miss_file(self): return self.__miss
    def get_changed_file(self): return self.__changed
    def get_not_in_downloader(self): return self.__not_in
    def get_ignore(self): return self.__ignore
    def get_updated(self): return self.__updated
    def get_custom_java(self): return self.__custom_java
    def is_sftp(self): return self.__sftp
    def get_user(self):
        if(self.__sftp): return self.__user
    def get_password(self):
        if(self.__sftp): return self.__password
    def get_dir_sftp(self):
        if(self.__sftp): return self.__dir_sftp
    def get_cnopts(self):
        if(self.__sftp): return self.__cnopts

    def get_recap(self):
        print("Récapitulatif des valeurs dans le Downloader:")
        print("URL du serveur:", self.get_url())
        print("Nom du dossier:", self.get_folder())
        print("Mode SFTP ?:", self.is_sftp())
        if(self.is_sftp()):
            print("Nom de compte:", self.get_user())
            print("Mot de passe:", "*" * len(self.get_password()))
        print("Directoire du dossier:", self.get_folder_dir())
        print("Utilisation d'un java custom:", self.get_custom_java())
        print("Données du serveur:", self.get_data_server())
        print("Données du client:", self.get_data_client())
        print("Fichier(s) manquant(s):", self.get_miss_file())
        print("Fichier(s) modifié(s):", self.get_changed_file())
        print("Fichier(s) non reconnu(s):", self.get_not_in_downloader())
        print("Fichier(s) ou dossier(s) ignorés:", self.get_ignore())
        print("Mise à jour faite ?:", self.get_updated())
        print("\nFin du récapitulatif")

    def set_url(self, new_url: str): self.__url = new_url
    def set_folder_dir(self, new_folder: str): self.__folder_dir = new_folder
    def set_folder(self, new_folder: str): self.__folder = new_folder
    def set_updated(self, new_value: bool): self.__updated = new_value
    def set_custom_java(self, new_value: bool): self.__custom_java = new_value

    def read_downloader(self, name="downloader.lxf"):
        with open(name, 'r', encoding='UTF-8') as data:
            all_data = data.readlines()
        dico = {}
        for line in all_data:
            if('\n' in line): line = line[:-1]
            directory = ''
            md5_code = ''
            x = True
            for elt in line:
                if(elt == '|'): x = False
                elif(x): directory += elt
                else: md5_code += elt
            dico[directory] = md5_code
        return dico

    def discord_presence(self, client_id: str, state='', details='', large_image='', large_text='', small_image='', small_text=''):
        self.__discord = Presence(client_id)
        self.__discord.update(state=state, details=details, large_image=large_image, large_text=large_text, small_image=small_image, small_text=small_text)
    
    def start_presence(self): self.__discord.connect()
    def stop_presence(self): self.__discord.close()

    def affiche_data_server(self):
        for keys, values in self.__data_serv.items():
            print(keys + " : " + values)

    def affiche_data_client(self):
        for keys, values in self.__data_client.items():
            print(keys, ':', values)

    def generate_have_file(self):
        try:
            os.chdir(self.__folder_dir)
        except:
            os.mkdir(self.__folder_dir)
        return generate_downloader(self.__folder_dir, self.__folder_dir, name="actual_file.lxf")

    def check_miss_file(self):
        final = []
        if(self.__logger): print("Recherche des fichier(s) manquant sur le client")
        for keys, _ in self.__data_serv.items():
            try:
                self.__data_client[keys]
            except KeyError:
                final.append(keys)
        return final

    def check_changed_file(self):
        final = []
        if(self.__logger): print("Recherches des fichiers changés changé sur le serveur")
        for keys, values in self.__data_serv.items():
            if(keys in list(self.__data_client.keys())):
                if(self.__data_client[keys] != values): final.append(keys)
        return final

    def check_not_in_downloader(self):
        final = []
        if(self.__logger): print("Recherche des fichiers non compris dans le serveur")
        for keys, _ in self.__data_client.items():
            try:
                self.__data_serv[keys]
            except KeyError:
                final.append(keys)
        return final

    def read_ignore(self):
        os.chdir(self.__folder_dir)
        with open("ignore.lxf", 'r', encoding='UTF-8') as ignore:
            all_ignore = ignore.readlines()
        final = []
        for elt in all_ignore:
            if('' == elt[:-1]): pass
            else: final.append(elt[:-1])
        os.chdir(self.__path)
        return final

    def delete_not_in_downloader(self):
        if(self.__logger): print("Suppresion des fichiers non autorisé")
        for elt in self.__not_in:
            try:
                os.remove(elt)
                if(self.__logger): print(elt, "a bien été supprimé")
            except:
                if(self.__logger): print("ERROR: Problème avec le fichier: ", elt)

    def delete_changed_file(self):
        if(self.__logger): print("Suppresion des fichiers changés")
        for elt in self.__changed:
            os.remove(elt)
            if(self.__logger): print(elt, "a bien été supprimés")

    def update(self):
        if(self.__logger): print("Mise à jour lancé")
        self.delete_not_in_downloader()
        if(self.__logger): print('\n\n')
        self.delete_changed_file()
        if(self.__logger): print('\n\n')
        self.download_files()
        if(self.__logger): print("\nMise à jour des fichiers terminés !")
        self.__updated = True

    def folder_to_file(self, file_dir: str):
        final = []
        temps = ''
        for elt in file_dir:
            if(elt == '/' or elt == '\\'):
                final.append(temps)
                temps = ''
            else: temps += elt
        return final

    def download_files(self):
        if not(self.__sftp):
            if(self.__logger): print("Lancement du téléchargement des fichiers...")
            if(self.__logger): print("Fichier(s) manquants en cours de téléchargement,", str(len(self.__miss)), "fichiers a télécharger !")
            download = self.__miss + self.__changed
            for file in download:
                self.make_folder(self.folder_to_file(file))
                r.urlretrieve(self.__url + 'files/' + file, file)
                if(self.__logger): print(file, "téléchargé avec succés")
            if(self.__logger): print("Fichier(s) changés en cours de téléchargement,", str(len(self.__changed)), "fichiers a télécharger !")
            self.__updated = True
        else:
            if(self.__logger): print("Lancement du téléchargement par SFTP...")
            if(self.__logger): print("Fichier(s) manquants en cours de téléchargement,", str(len(self.__miss)), "fichiers a télécharger !")
            download = self.__miss + self.__changed
            for file in download:
                if(file == 'downloader.lxf' or file == "ignore.lxf" or file == "actual_file.lxf"): continue
                self.make_folder(self.folder_to_file(file))
                with pysftp.Connection(host=self.__ip, username=self.__user, password=self.__password, private_key='.ppk', cnopts=self.__cnopts) as sftp:
                    sftp.get(self.__dir_sftp + "files/" + file, file)
                    if(self.__logger): print(file, "télécharger avec succés")
            self.__updated = True


    def make_folder(self, list_folder: list, path=''):
        if(list_folder == []): return
        actual_folder_to = list_folder.pop(0)
        try:
            os.mkdir(self.__folder_dir + path + '/' + actual_folder_to)
        except:
            pass
        self.make_folder(list_folder, path=path + '/' + actual_folder_to)

    def run(self, cmd: str):
        if not(self.__updated):
            print("Démarrage impossible, vous avez pas fait la vérification et la mise à jour des fichiers !")
            return
        if(self.__custom_java): os.system('"' + self.__folder_dir + '/custom_java/bin/java.exe" ' + cmd)
        else: os.system(cmd)

import pygame
from PIL import Image

class Button:
    def __init__(self, texture_dir: str, pos: tuple, interne_value=None) -> None:
        self.__x, self.__y = self.__pos = pos
        self.__dir_tex = texture_dir
        self.__texture = pygame.image.load(texture_dir)
        self.__interne_value = interne_value
        
    def get_x(self): return self.__x
    def get_y(self): return self.__y
    def get_pos(self): return self.__pos
    def get_texture_dir(self): return self.__dir_tex
    def get_texture(self): return self.__texture
    def get_interne_value(self): return self.__interne_value
    
    def set_interne_value(self, value):
        self.__interne_value = value
    
    def change_texture(self, texture_dir: str):
        self.__dir_tex = texture_dir
        self.__texture = pygame.image.load(texture_dir)
    
    def change_pos(self, new_pos: tuple) -> bool:
        assert isinstance(new_pos, tuple) or isinstance(new_pos, list), "Les positions doit être soit un tuple soit une liste"
        assert len(new_pos) == 2, "new_pos doit contenir deux coordonnées (x/y)"
        try:
            self.__x, self.__y = self.__pos = new_pos
            return True
        except:
            return False
        
    def is_cliqued(self, pos_mouse: tuple) -> bool:
        assert isinstance(pos_mouse, tuple) or isinstance(pos_mouse, list), "Les positions doit être soit un tuple soit une liste"
        assert len(pos_mouse) == 2, "pos_mouse doit contenir deux coordonnées (x/y)"
        width, height = Image.open(self.__dir_tex).width, Image.open(self.__dir_tex).height
        larg_mouse, haut_mouse = pos_mouse
        if(larg_mouse >= self.__x and larg_mouse <= self.__x + width and haut_mouse >= self.__y and haut_mouse <= self.__y + height): return True
        else: return False

def spliter(dir: str) -> str:
    final = []
    temps = ''
    for elt in dir:
        if(elt != "/" and elt != "\\"): temps += elt
        else:
            final.append(temps)
            temps = ''
    string = ''
    returned = []
    for line in final:
        string += line + "/"
        returned.append(string)
    return returned

class Updater:
    def __init__(self, sftp_server: str, user: str, password: str, dir='', dir_server='', logger=False):
        self.__ip = sftp_server
        self.__username = user
        self.__password = password
        self.__dir = dir
        self.__logger = logger
        if(self.__dir[:-1] != "/" and self.__dir[:-1] != "\\"): self.__dir += "/"
        self.__cnopts = pysftp.CnOpts()
        self.__cnopts.hostkeys = None
        self.__dir_server = dir_server
        if(self.__dir_server[:-1] != "/" and self.__dir_server[:-1] != "\\"): self.__dir_server += "/"

        self.__path = os.getcwd()

        try:
            os.chdir(self.__dir)
        except:
            pass
        if(self.__logger): print("Génération du downloader")
        generate_downloader(self.__dir, self.__path)
        os.chdir(self.__path)
        if(self.__logger): print("Lecture du downloader client")
        self.__downloader = self.read_downloader()

        try:
            with pysftp.Connection(host=self.__ip, username=self.__username, password=self.__password, cnopts=self.__cnopts) as sftp:
                sftp.get(self.__dir_server + "downloader.lxf", "actual_downloader.lxf")
            if(self.__logger): print("Lecture du downloader serveur")
            self.__downloader_server = self.read_downloader(name="actual_downloader.lxf")
        except: self.__downloader_server = []
        if(self.__logger): print("Comparaison des fichiers")
        self.__update = self.compare()

    def compare(self):
        final = {}
        for key, md5 in self.__downloader.items():
            if(key not in list(self.__downloader_server.keys())): final[key] = md5
            elif(self.__downloader[key] != self.__downloader_server[key]): final[key] = md5
        return final
        

    def read_downloader(self, name="downloader.lxf"):
        with open(name, 'r', encoding='UTF-8') as data:
            all_data = data.readlines()
        dico = {}
        for line in all_data:
            if('\n' in line): line = line[:-1]
            if("actual_file.lxf" not in line and "downloader.lxf" not in line):
                directory = ''
                md5_code = ''
                x = True
                for elt in line:
                    if(elt == '|'): x = False
                    elif(x): directory += elt
                    else: md5_code += elt
                dico[directory] = md5_code
        return dico

    def update(self):
        for keys in self.__update:
            with pysftp.Connection(host=self.__ip, username=self.__username, password=self.__password, private_key='.ppk', cnopts=self.__cnopts) as sftp:
                try:
                    sftp.remove(self.__dir_server + "files/" + keys)
                except:
                    pass
                try:
                    for elt in spliter(keys):
                        try:
                            sftp.mkdir(self.__dir_server + "files/" + elt)
                        except:
                            pass
                except:
                    pass
                try:
                    sftp.put(self.__dir + keys, self.__dir_server + "files/" + keys)
                    print(f"{keys} upload !")
                except: print("Problème avec le fichier: " + keys)
        with pysftp.Connection(host=self.__ip, username=self.__username, password=self.__password, private_key='.ppk', cnopts=self.__cnopts) as sftp:
            try:
                sftp.remove(self.__dir_server + "downloader.lxf")
            except:
                pass
            try:
                sftp.put(self.__path + "\\downloader.lxf", self.__dir_server + "downloader.lxf")
            except: 
                print("Problème avec le downloader.lxf")


# Chargement du module ...
print("==" * 20)
print('|' + ' ' * 38 + '|')
print('|' + ' ' * 12 + 'LuxLIB started' + ' ' * 12 + '|')
print('|' + ' ' * 6 + 'Code by Valentin Thuillier' + ' ' * 6 + '|')
print('|' + ' ' * 38 + '|')
print("==" * 20)