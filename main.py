import asyncio
import os
import sys
from pystyle import *
from telethon.sync import TelegramClient

def banner():
    cls()
    Write.Print("Choose an option...", Colors.dark_green, interval=0)

def cls():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    os.system("pause>null" if os.name == "nt" else "read -n1 -r -p 'Press any key to continue...'")

async def send_messages_to_groups(client, source_group_name, excluded_group_names):
    # Identificar grupos de destino excluyendo los grupos en excluded_group_names
    group_ids = []
    async for dialog in client.iter_dialogs():
        if dialog.is_group and dialog.name != source_group_name and dialog.name not in excluded_group_names:
            group_ids.append(dialog.id)

    # Obtenemos hasta 10 mensajes del grupo fuente
    source_group = None
    async for dialog in client.iter_dialogs():
        if dialog.is_group and dialog.name == source_group_name:
            source_group = dialog.id
            break

    if source_group is None:
        Write.Print(f"\nGrupo '{source_group_name}' no encontrado. Verifique el nombre.", Colors.red, interval=0)
        return

    # Recuperar los mensajes de spam del grupo fuente
    messages = []
    async for message in client.iter_messages(source_group, limit=10):
        if message.text:
            messages.append(message)

    if not messages:
        Write.Print("\nNo se encontraron mensajes en el grupo fuente.", Colors.red, interval=0)
        return

    # Enviar mensajes de forma intercalada a cada grupo con las pausas indicadas
    while True:
        for message in messages:
            for group_id in group_ids:
                try:
                    await client.forward_messages(group_id, messages=[message])
                    Write.Print(f"\nMensaje reenviado a {group_id}", Colors.green, interval=0)
                    await asyncio.sleep(4)  # Espera de 4 segundos entre envíos a cada grupo
                except Exception as e:
                    Write.Print(f"\nError al reenviar al grupo {group_id}: {str(e)}", Colors.red, interval=0)
            # Pausa de 3000 segundos antes de pasar al siguiente mensaje
            Write.Print(f"\nEsperando 3000 segundos antes de enviar el siguiente mensaje desde {source_group_name}", Colors.orange, interval=0)
            await asyncio.sleep(3000)

async def main():
    cls()
    banner()
    option = Write.Input("\n[~] r00t > ", Colors.dark_green, interval=0)
    if option == '1':
        cls()
        Write.Print("Escribe tu API ID", Colors.dark_green, interval=0)
        api_id = Write.Input("[~] r00t > ", Colors.dark_green, interval=0)
        cls()
        Write.Print("Escribe tu API hash", Colors.dark_green, interval=0)
        api_hash = Write.Input("[~] r00t > ", Colors.dark_green, interval=0)
        cls()
        Write.Print("Escribe los nombres de los grupos a excluir (separados por comas)", Colors.dark_green, interval=0)
        excluded_group_names_input = Write.Input("[~] r00t > ", Colors.dark_green, interval=0)

        # Crear lista de nombres de grupos a excluir
        excluded_group_names = [group.strip() for group in excluded_group_names_input.split(",")]

        client = TelegramClient('anon', api_id, api_hash)
        await client.start()

        # Llamar a la función de envío con el nombre de grupo fuente 'spambotasteriscom'
        await send_messages_to_groups(client, "spambotasteriscom", excluded_group_names)

        await client.disconnect()

    elif option == '2':
        cls()
        sys.exit()
    else:
        Write.Print("Elige una opción válida", Colors.orange, interval=0)
        pause()
        banner()

asyncio.run(main())
