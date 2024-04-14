import asyncio
from EventManager import EventManager

# Initialisation de l'EventManager
event_manager = EventManager()

# Fonction de callback pour l'événement de clic sur le bouton
async def on_button_click(id):
    await asyncio.sleep(1)  # Simuler un traitement long
    print(f"Thread {id} : Button clicked!")

# Ajouter la fonction de callback à l'événement "onclick"
button_event = event_manager.add_event_listener("onclick", on_button_click)

# Fonction pour simuler un appui sur le bouton en boucle
async def simulate_button_press():
    while True:
        # Déclencher l'événement "onclick" pour simuler un appui sur le bouton
        await button_event.trigger(1)
        # Attendre un court instant avant de simuler un nouvel appui
        await asyncio.sleep(0.5)

# Créer une boucle d'événement asyncio
async def main():
    # Lancer la fonction de simulation dans un asyncio Task
    asyncio.create_task(simulate_button_press())

    # Boucle principale pour gérer les événements réels du bouton
    while True:
        await asyncio.sleep(1)
        await button_event.trigger(2)

# Lancer la boucle d'événement asyncio
asyncio.run(main())
