def test_slider_values():
    min = 10000000000
    for _ in range(500):  # Tester 10 valeurs différentes
        value = slider.read()
        if value < min:
            min = value
        print("Slider value:", value)
        sleep(1)  # Attente d'une seconde entre chaque lecture
    return min