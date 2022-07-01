import discord
from discord.ext import commands
import json
from shutil import move
from tempfile import NamedTemporaryFile
import requests
import urllib as urli

class general():
    #====(### JSON ###)====#
    def jload(file):
        with open(file,'r') as file:
            return json.load(file)

    def jsave(file,key,dado):
        with open(file,'r') as file, NamedTemporaryFile('w',delete=False) as out:
            dados = json.load(file)
            dados[key] = dado
            json.dump(dados,out,ensure_ascii=False,indent=4,separators=(',',':'))
        move(out.name,file)

    def jloadn(link,ty:int = 0):
        if ty == 0:
            r = requests.get(link)
            t = json.loads(r.content)
            return t
        else:
            r = requests.get(link)
            j = r.json()
            return j

    #====(### SQL ###)====#
    def table(cursor,name,items):
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {name}(
                {items}
            )
            """
        )
    def get(cur,table,key,value):
        return cur.execute(
            f"""
            SELECT {key} FROM {table} WHERE id = {value}
            """
        ).fetchone()

    def insert(cur,table,value):
        cur.execute(
            f"""
            INSERT INTO {table} ({value[0]}) VALUES({value[1]})
            """
        )

    def update(cur,table,parameters,condition):
        cur.execute(
            f"""
            UPDATE {table} SET {parameters[0]} = {parameters[1]} WHERE {condition[0]} = {condition[1]}
            """
        )

    def delete(cur,table,condition):
        cur.execute(
            f"""
            DELETE FROM {table} WHERE {condition[0]} = {condition[1]}
            """
        )

if __name__ == '__main__':
    tk = ''
    for i in input('> '):
        tk = f'{i} {tk}'

    print(tk)