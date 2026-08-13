
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import data_base  
import re
import vt

load_dotenv(override=True)
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
VIRUSTOTAL_API_KEY = os.getenv("virustotal_key")
intents = discord.Intents.default()
intents.message_content = True
print(bool(VIRUSTOTAL_API_KEY))
bot = commands.Bot(command_prefix="$", intents=intents)

#*  CSS........................................................................./
from funciones import cargar_css
cargar_css()

#*  EVENTOS........................................................................./
@bot.event
async def on_ready():
    data_base.make_base()
    data_base.id_table()
    print(f'--- Bot conectado con exito ---')
    print(f'Nombre: {bot.user.name}')
    print(f'ID: {bot.user.id}')
    print(f'-------------------------------')

#*  COMANDOS........................................................................./

#! comando $hello
@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

#! comando $scan 
@bot.command()
async def scan(ctx): #funcion recibe lo que mando el usuario en el chat de discord
    if not ctx.message.attachments:
        await ctx.send("Por favor, sube un archivo junto con el comando `$scan`.")
        return

    temporal_file = ctx.message.attachments[0]
    file_name = temporal_file.filename  #se obtiene el nombre del archivo subido
    await temporal_file.save(file_name)
    file_whit_hash = data_base.machine_hash(file_name) #se transforma el archivo en hash para poder guardarlo en la base de datos y compararlo con otros hashes
    results = data_base.lock_hash(file_whit_hash)

    client =  vt.Client(VIRUSTOTAL_API_KEY)

    if results:
         await ctx.send(f"este archivo ya estaba guardado en la base de datos. Estado: **{results}** ")

    else:
        try:
                file_info = await client.get_object_async(f"/files/{file_whit_hash}")
                stats =  file_info.last_analysis_stats
                malicious = stats["malicious"]
                
                if malicious > 0:
                    resultado = f"este archivo tiene {malicious} detecciones"
                else:
                    resultado = "archivo limpio"
        except vt.APIError as e:
                if e.code == "NotFoundError":
                    resultado = "archivo no encontrado en virustotal"
                else:
                    resultado = "error de consulta"
        finally:
                await client.close_async()

        data_base.save_result(file_whit_hash, resultado, file_name)
        await ctx.send(f"Resultado del análisis: **{resultado}** (Hash: `{file_whit_hash}`)")

    if os.path.exists(file_name): 
        os.remove(file_name)


#! comando $quiensoy
@bot.command()
async def quiensoy(ctx):
    usuario = ctx.author.name
    canal = ctx.channel.name
    servidor = ctx.guild.name
    await ctx.send(f"jelouda, su nombre es **{usuario}**, usted esta escribiendo desde el canal **#{canal}** en el servidor **'{servidor}'**")

#! comando $calcula = ['calcular', 'restar', 'multiplicar', 'dividir', 'sumar', 'resta', 'suma', 'divide', 'multiplica', 'multiplicacion', 'division']
@bot.command(aliases=['calcular', 'restar', 'multiplicar', 'dividir', 'sumar', 'resta', 'suma', 'divide', 'multiplica', 'multiplicacion', 'division'])
async def calcula(ctx, *, operacion: str):
    patron = r"(\d+)\s*([\+\-\*/])\s*(\d+)" 
    busqueda = re.search(patron, operacion)

    if not busqueda:
        await ctx.send("El formato que usaste para para ejecutar tu operacion es incorrecto usa mejor el siguiente Ejemplo: $calcular 20+20 o tambien $calcular 40  +  40")
        return

    numero1 = int(busqueda.group(1))
    simbolo = busqueda.group(2)
    numero2 = int(busqueda.group(3))

    calculo_final = 0 
    if simbolo == "+": 
        calculo_final = numero1+numero2

    elif simbolo == "-":
        calculo_final = numero1-numero2

    elif simbolo == "/":
        if numero2 == 0:
            await ctx.send("Error: No se puede dividir entre cero. Es literalmente imposible las reglas de nuestro universo no lo permiten.")
            return
        calculo_final = numero1/numero2

    elif simbolo == "*":
        calculo_final = numero1*numero2

    await ctx.send(f"resultado = **{calculo_final}**")

#Aqui estou colocando [from] ya que indica que viene del archivo (data_base) y al colocar import (get_history) estoy llamando al codigo creado por daniel
#@bot.command(aliases=['historial_cmd', 'historia',])
#async def historial(ctx):
 #   registros = get_history()
  #  if not registros:
   #     await ctx.send ('**No hay ningun registro por el momento**')
    #    return
#Aqui use la funcion Embed que me permite darle color a la interfaz del mensaje
#Tambien coloque un titulo y una descripcion para el mensaje para cuando el usuario ejecute el comando para ver su Historial de calculos le aparezca un mensaje indicandole que esos son los datos que tenemos almacenado en la base de datos
    #embed = discord.Embed (
     #   title = "**Historial de  registros guardados en nuestra base de datos**", 
      #  description = "Aqui tienes los 10 ultimos calculos realizados por ti, registrados en nuestra base de datos",
       # Color=discord.Color.Blue() 
        #)
        
    #texto_hitorial=""
 #   for i (nombre_archivo, comando) in enumerate(registros, start=1): 
#    texto_hitorial += "f**{i}.** Archivo "

bot.run(DISCORD_TOKEN)