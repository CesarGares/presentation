"""
ESTA CLASE UTILIZA PYAUTOGUI PARA PERMITIR CONTROLAR ELEMENTOS DE LA PANTALLA Y SIMULAR EL COMPARTAMIENTO HUMANO, POR EJEMPLO
watch() Se espera hasta que localiza una imagen en pantalla
lookforimage() Busca una imagen entre los diferentes programas del SO, se desplaza entre ventanas utilizando el atajo alt+tab
decide() Busca dos imagenes, cuando encuentre alguna de las dos regresa el valor de la que encontro 1 o 2
seeimageandclick() Busca una imagen en la pantalla y cuando la encuentre le va a dar click, se espera hasta localizarla
exist_in_screen() Si una de las dos imagenes está presente en la pantalla regresa true o false
"""

import pyautogui as pa
import time

class screenFunctions:

    def __init__(self, number_of_windows):
        """
        Starts object to control screen objects

        Args:
            number_of_windows: Number of windows to displace using alt+tab shortcurt, set to 0 if it is a one-window application 

        """
        self.vnt = number_of_windows

    def look_for_image(self,image_path, is_alternate=False, alternate_image_path=""):
        """
        Looks for an image on the screen and returns the center coordinates of the image.

        Args:
            image_path (str): Path of the image to be searched.
            is_alternate (bool): Whether to search for an alternate image if the primary image is not found.
            alternate_image_path (str): Path of the alternate image to be searched.

        Returns:
            tuple: The (x, y) coordinates of the center of the found image.

        Raises:
            ImageNotFoundException: If the specified image is not found.
        """
        CONFIDENCE_THRESHOLD=0.95
        while True:
            print(f"Looking for {image_path}")

            # Presses the Alt key
            pa.keyDown("alt")

            # Switches between windows by pressing the Tab key
            for _ in range(self.vnt-1):
                pa.press("tab")

            # Releases the Alt key
            pa.keyUp("alt")

            # Searches for the primary image
            primary_image_location = pa.locateCenterOnScreen(image_path, grayscale=True, confidence=CONFIDENCE_THRESHOLD)

            if primary_image_location is not None:
                return primary_image_location

            if is_alternate:
                # Searches for the alternate image if the primary image is not found
                alternate_image_location = pa.locateCenterOnScreen(alternate_image_path, grayscale=True, confidence=CONFIDENCE_THRESHOLD)
                if alternate_image_location is not None:
                    pa.press("space")  # Presses the Space key
                    return alternate_image_location



    def watch(self, path):
        """Espera a que se encuentre una imagen en la pantalla.

        Args:
            path (str): La ruta de la imagen a buscar.

        Returns:
            None
        """
        CONFIDENCE_THRESHOLD=0.9
        while True:
            print(f"Buscando {path}...")
            image_location = pa.locateCenterOnScreen(path, grayscale=True, confidence=CONFIDENCE_THRESHOLD)
            if image_location is not None:
                print(f"Imagen encontrada en {image_location}.")
                return
            time.sleep(0.5)

    def decide(self, path1, path2):
        """Se cicla mientras busca dos imagenes, regresa 1 o 2 dependiendo de que imagen encontró primero"""
        while True:
            print("buscando " + path1)
            image1 = pa.locateCenterOnScreen(path1, grayscale=True, confidence=0.95)
            if image1 is not None:
                return 1
            
            print("buscando " + path2)
            image2 = pa.locateCenterOnScreen(path2, grayscale=True, confidence=0.95)
            if image2 is not None:
                return 2

    def seeimageandclick(self, path, altern=""):
        """Se cicla mientras busca una imagen en pantalla. Cuando la encuentra da un click en la posicion donde encontró la imagen"""
        while True:
            image = pa.locateCenterOnScreen(path, grayscale=True, confidence=0.95)
            if image is not None:
                print("seeing for click " + path)
                x, y = image
                pa.click(x, y)
                print(x, y)
                return

            if altern != "":
                altern_image = pa.locateCenterOnScreen(altern, grayscale=True, confidence=0.95)
                if altern_image is not None:
                    print("seeing for click " + altern)
                    x, y = altern_image
                    pa.click(x, y)
                    print(x, y)
                    return

    def exist_in_screen(self, path, path2):
        """
        Busca la imagen path o path2 en pantalla. Retorna True si encuentra alguna, False en caso contrario.
        """
        if pa.locateCenterOnScreen(path, grayscale=False, confidence=0.98) is not None:
            return True
        elif pa.locateCenterOnScreen(path2, grayscale=False, confidence=0.98) is not None:
            return True
        else:
            return False

    def get_found_image_id(self, path="", path2=""):
        """
        Busca la presencia de dos imágenes en la pantalla y devuelve un valor indicando cuál de ellas se encontró primero.
        
        Args:
            path (str): Ruta a la primera imagen a buscar.
            path2 (str): Ruta a la segunda imagen a buscar.
        
        Returns:
            int: 1 si la primera imagen fue encontrada, 2 si la segunda imagen fue encontrada.
        """
        while True:
            print("searching "+path)
            try:
                x, y = pa.locateCenterOnScreen(
                    path, grayscale=False, confidence=0.98)
                return 1
            except Exception as e:
                try:
                    x, y = pa.locateCenterOnScreen(
                        path2, grayscale=False, confidence=0.98)
                    return 2
                except Exception as e:
                    pass
