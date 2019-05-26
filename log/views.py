from django.core.files.storage import FileSystemStorage
from collections import OrderedDict
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
import os
import re
import json
# Create your views here.

regex_inicio_game = re.compile(r".*InitGame:.*")
regex_mortes = re.compile(r".*Kill:.*:(.*).*killed(.*)by(.*)")


def IndexView(request):
    if request.method == 'POST' and request.FILES['arquivo']:
        arquivo = request.FILES['arquivo']
        fs = FileSystemStorage()
        filename = fs.save(arquivo.name, arquivo)
        return JsonResponse(parser_jogo(os.path.join(settings.MEDIA_ROOT, filename)))
    return render(request, 'log/index.html')

def parser_jogo(arquivo_log):
    jogo_contador = 1
    numero_jogo = "game_{}"
    dicionario_jogo = OrderedDict()
    with open(arquivo_log, "r", encoding="utf-8") as fp:
        for linha in fp.readlines():
            if(regex_inicio_game.match(linha)):
                key=numero_jogo.format(jogo_contador)
                dicionario_jogo[key]={
                    "total_kills":0,
                    "players":[],
                     "kills": {},
                }
                jogo_contador+=1
            if regex_mortes.match(linha):
                parser_mortes(linha, dicionario_jogo[key])
    return dicionario_jogo


def parser_mortes(linha, jogo):
    aux = regex_mortes.match(linha)
    vivo = aux.group(1).strip()
    morto = aux.group(2).strip()
    jogo["total_kills"] += 1
    if (vivo != "<world>" and vivo
            not in jogo["players"]):
        jogo["players"].append(vivo)
    if morto not in jogo["players"]:
        jogo["players"].append(morto)
    if vivo != "<world>":
        if vivo in jogo["kills"].keys():
            jogo["kills"][vivo] += 1
        else:
            jogo["kills"][vivo] = 1
    else:
        if morto in jogo["kills"].keys():
            jogo["kills"][morto] -= 1
        else:
            jogo["kills"][morto] = -1
