# coding=utf-8

#  i-Parapheur Utils
#  Copyright (C) 2017-2022 Libriciel-SCOP
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

# module Parapheur

import base64
import mimetypes
import subprocess

import os
import requests
from io import StringIO
from requests.exceptions import SSLError
from suds.cache import NoCache
from suds.client import Client as Sudsclient
from suds.plugin import MessagePlugin, DocumentPlugin
from suds.transport import Reply
from suds.transport.https import HttpAuthenticated

from . import pprint

__author__ = 'lhameury'


class RequestsTransport(HttpAuthenticated):
    def __init__(self, **kwargs):
        self.cert = kwargs.pop('cert', None)
        self.username = kwargs.pop('username', None)
        self.password = kwargs.pop('password', None)
        # super won't work because not using new style class
        HttpAuthenticated.__init__(self, **kwargs)

    def open(self, request):
        """
        Fetches the WSDL using cert.
        :param request: The request object
        """
        self.addcredentials(request)
        if "https" in request.url:
            resp = requests.get(request.url, data=request.message,
                                headers=request.headers, cert=self.cert, verify=False,
                                auth=(self.username, self.password))
        else:
            resp = requests.get(request.url, data=request.message,
                                headers=request.headers)
        result = StringIO(resp.content.decode("utf-8"))
        return result

    def send(self, request):
        # Dirty hack... can not be handled in filter ! BEGIN
        request.message = request.message.replace("contentType".encode(), "xm:contentType".encode())
        # END
        self.addcredentials(request)
        resp = requests.post(request.url, data=request.message,
                             headers=request.headers, cert=self.cert, verify=False,
                             auth=(self.username, self.password))
        result = Reply(resp.status_code, resp.headers.__dict__, resp.content.decode("utf-8"))
        return result


class Filter(MessagePlugin):
    def __init__(self):
        pass

    def marshalled(self, context):
        context.envelope.set('xmlns:xm', 'http://www.w3.org/2005/05/xmlmime')

    def received(self, context):
        reply = context.reply
        context.reply = reply[reply.find("<?xml version"):reply.rfind(">") + 1]


class Handlewsdl(DocumentPlugin):
    def __init__(self):
        pass

    def loaded(self, context):
        # Dirty hack ! Le type DossierID bloque !
        context.document = context.document.replace('type="iph:DossierID"', 'type="xsd:string"')


class Webservice:
    def __init__(self, config, user=None, password=None):
        pprint.log("\n[Parapheur-SOAP]", True)
        # Nom d'utilistaeur
        self.username = user if user is not None else config.get("Parapheur", "username")
        # Mot de passe utilisateur
        self.__password = password if password is not None else config.get("Parapheur", "password")
        # URL webservice
        self.__url = "https://" + config.get("Parapheur", "server") + "/ws-iparapheur"
        # Hostname
        self.__hostname = config.get("Parapheur", "server")
        pprint.info("Serveur     : " + self.__url)
        # Certificat webservice
        self.__cert = (
            os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', "files/public.pem"),
            os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', "files/private.pem"))

        # On vérifie que l'AC est fournie
        autoritypath = os.path.join('/tmp', 'autority.pem')
        # Si non, on récupère la chaîne via une commande openssl
        if not os.path.isfile(autoritypath):
            command = "echo \"\" | " \
                      "openssl s_client -showcerts -connect " + self.__hostname + ":443 2>/dev/null | " \
                                                                                  "sed -n -e '/BEGIN\\ CERTIFICATE/,/END\\ CERTIFICATE/ p'"
            p = subprocess.Popen(command,
                                 shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            aut = p.stdout.read()
            with open(autoritypath, "w") as text_file:
                text_file.write(aut.decode("utf-8"))

        os.environ['REQUESTS_CA_BUNDLE'] = autoritypath

        pprint.info("Utilisateur : " + self.username)

        if os.path.isfile(self.__cert[0]):
            credentials = dict(username=self.username,
                               password=self.__password,
                               cert=self.__cert)
            t = RequestsTransport(**credentials)
            try:
                self.api = Sudsclient(self.__url + '?wsdl', plugins=[Handlewsdl(), Filter()],
                                      location=self.__url, transport=t, cache=NoCache())
                self.api.service.echo("Coucou, ici Python !")
                pprint.success("OK", True)
            except SSLError as e:
                print(e)
        else:
            pprint.error("Fichier {0} introuvable".format(self.__cert), True)

    def call(self):
        return self.api.service

    def listmethods(self):
        return self.api

    def create(self, objectname):
        return self.api.factory.create(objectname)

    @staticmethod
    def loaddocument(chunk_size, location):
        base64file = ""
        with open(location, 'rb') as f:
            while True:
                data = f.read(chunk_size)
                if data:
                    base64file += base64.b64encode(data)
                else:
                    break
        return base64file

    def loadsig(self, location):
        loadedfile = self.create("TypeDoc")
        loadedfile["value"] = self.loaddocument(8192, location)
        loadedfile["_contentType"] = "application/pkcs7-signature"
        return loadedfile

    def loadfile(self, location):
        loadedfile = self.create("TypeDoc")
        loadedfile["value"] = self.loaddocument(8192, location)
        loadedfile["_contentType"] = mimetypes.guess_type(location)[0]
        return loadedfile

    def loadannexefile(self, location, name, mimetype="UTF-8"):
        annexes = self.create("TypeDocAnnexes")
        annexe = self.create("DocAnnexe")
        annexe["nom"] = name
        annexe["fichier"] = self.loadfile(location)
        annexe["mimetype"] = mimetypes.guess_type(location)[0]
        annexe["encoding"] = mimetype
        annexe["signature"] = None
        annexes["DocAnnexe"] = [annexe]
        return annexes
