import random
import webbrowser

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu

KV = r"""
Screen:

    in_class: text

    BoxLayout:

        orientation: "vertical"

        MDToolbar:
            title: "Menu"
            left_action_items: [["menu", lambda x: navigation_drawer.set_state()]]

        Widget:

    MDNavigationLayout:

        ScreenManager:

            id: screen_manager

            Screen:

                name: "screen_1"

                MDLabel:
                    text: "Welcome\n\nto\n\nthe\n\nVocabulary\n\nTrainer!"
                    font_style: "H4"
                    halign: "center"

            Screen:

                name: "screen_2"

                MDLabel:
                    text: "Please translate"
                    font_style: "Body1"
                    halign: "center"
                    pos_hint: {"center_y": 0.85}

                MDLabel:
                    text: ""
                    id: label_word_in
                    font_style: "H6"
                    halign: "center"
                    pos_hint: {"center_y": 0.75}

                MDTextField:
                    hint_text: "Enter translation here"
                    id: text
                    pos_hint: {"center_x": 0.5, "center_y": 0.65}
                    size_hint_x: None
                    mode: "rectangle"
                    width: 600

                MDLabel:
                    text: ""
                    id: label_word_out
                    font_style: "H6"
                    halign: "center"
                    pos_hint: {"center_y": 0.55}
                    markup: True

                MDFillRoundFlatButton:
                    text: "Next"
                    font_style: "Button"
                    pos_hint: {"center_x": 0.3, "center_y": 0.45}
                    on_press: app.next()

                MDFillRoundFlatButton:
                    text: "Check"
                    font_style: "Button"
                    pos_hint: {"center_x": 0.7, "center_y": 0.45}
                    on_press: app.check()

                MDLabel:
                    text: "Category: All"
                    id: label_category
                    font_style: "Body1"
                    pos_hint: {"center_x": 0.55, "center_y": 0.2}

                MDRaisedButton:
                    text: "Category"
                    id: button_category
                    font_style: "Button"
                    pos_hint: {"center_x": 0.1, "center_y": 0.1}
                    md_bg_color: app.theme_cls.primary_light
                    on_release: app.menu.open()

                MDFillRoundFlatButton:
                    text: "Solve"
                    font_style: "Button"
                    pos_hint: {"center_x": 0.5, "center_y": 0.1}
                    md_bg_color: app.theme_cls.primary_light
                    on_press: app.solve()

                MDFloatingActionButtonSpeedDial:
                    callback: app.language_setting_callback
                    data: app.language_setting_dict
                    bg_color_root_button: app.theme_cls.primary_light
                    root_button_anim: True

            Screen:

                name: "screen_3"

                MDLabel:
                    text: "This is a RandomCollection production."
                    font_style: "Body1"
                    halign: "center"
                    pos_hint: {"center_y": 0.7}

                MDLabel:
                    text: "For more information, visit"
                    font_style: "Body1"
                    halign: "center"
                    pos_hint: {"center_y": 0.6}

                MDLabel:
                    text: "[ref=randomcollection_github]RandomCollection GitHub[/ref]"
                    font_style: "Body1"
                    halign: "center"
                    pos_hint: {"center_y": 0.5}
                    markup: True
                    theme_text_color: "Custom"
                    text_color: 5/255, 99/255, 193/255, 1
                    underline: True
                    on_ref_press: app.open_link(link="https://github.com/RandomCollection")

                MDLabel:
                    text: "or"
                    font_style: "Body1"
                    halign: "center"
                    pos_hint: {"center_y": 0.4}

                MDLabel:
                    text: "[ref=randomcollection_github_page]RandomCollection GitHub Page[/ref]"
                    font_style: "Body1"
                    halign: "center"
                    pos_hint: {"center_y": 0.3}
                    markup: True
                    theme_text_color: "Custom"
                    text_color: 5/255, 99/255, 193/255, 1
                    underline: True
                    on_ref_press: app.open_link(link="https://randomcollection.github.io/")

        MDNavigationDrawer:
            id: navigation_drawer
            orientation: "vertical"
            padding: "12dp", "12dp", "12dp", "0dp"
            spacing: "5dp"

            AnchorLayout:
                anchor_x: "left"
                size_hint_y: None
           
            MDLabel:
                text: "Vocabulary Trainer"
                font_style: "Button"
                size_hint_y: None
                height: self.texture_size[1]

            MDLabel:
                text: "RandomCollection"
                font_style: "Caption"
                size_hint_y: None
                height: self.texture_size[1]

            ScrollView:

                MDList:

                    OneLineAvatarListItem:
                        text: "Home"
                        on_press:
                            navigation_drawer.set_state("close")
                            screen_manager.current = "screen_1"
                        IconLeftWidget:
                            icon: "home-circle"

                    OneLineAvatarListItem:
                        text: "Start"
                        on_press:
                            navigation_drawer.set_state("close")
                            screen_manager.current = "screen_2"
                        IconLeftWidget:
                            icon: "play-circle"

                    OneLineAvatarListItem:
                        text: "About"
                        on_press:
                            navigation_drawer.set_state("close")
                            screen_manager.current = "screen_3"
                        IconLeftWidget:
                            icon: "account-circle"
            Widget:
"""

SPANISH = ['el animal', 'el caballo', 'el perro', 'el pez', 'la vaca', 'adiós', 'el alemán', 'bienvenido', 'el bolígrafo', 'la botella', 'buenas noches', 'buenas tardes', 'buenos días', 'la casa', 'el cepillo', 'el cigarrillo', 'la ciudad', 'el coche', 'cómo estás', 'el cuaderno', 'de nada', 'la gente', 'la gitana', 'el gitano', 'gracias', 'la guerra', 'hasta luego', 'hasta mañana', 'hasta pronto', 'hola', 'el hombre', 'el imbécil', 'el libro', 'mucha suerte', 'muchas gracias', 'mucho gusto', 'la niña', 'el niño', 'la pared', 'pásalo bien', 'por favor', 'qué tal', 'la razón', 'la torre', 'el diente', 'la mano', 'ayer', 'el día', 'domingo', 'hoy', 'jueves', 'lunes', 'mañana', 'martes', 'miércoles', 'sábado', 'la semana', 'viernes', 'la abuela', 'el abuelo', 'amar', 'la amiga', 'el amigo', 'besar', 'la boda', 'casarse', 'el cumpleaños', 'el divorcio', 'la familia', 'la hermana', 'el hermano', 'la hija', 'el hijo', 'la madre', 'el marido', 'el matrimonio', 'la mujer', 'la nieta', 'el nieto', 'la novia', 'el novio', 'el padre', 'querer', 'te quiero', 'la tía', 'el tío', 'la cebolla', 'el chocolate', 'el chorizo', 'la harina', 'el vino', 'la zanahoria', 'el baño', 'la cocina', 'la cuchara', 'el cuchillo', 'la mesa', 'la silla', 'el tenedor', 'el vaso', 'la luna', 'catorce', 'cero', 'cien', 'cinco', 'cincuenta', 'cuarenta', 'cuatro', 'diecinueve', 'dieciocho', 'dieciseis', 'diecisiete', 'diez', 'doce', 'dos', 'mil', 'noventa', 'nueve', 'ochenta', 'ocho', 'once', 'quince', 'seis', 'sesenta', 'setenta', 'siete', 'trece', 'treinta', 'tres', 'uno', 'veinte', 'cómo', 'cuándo', 'cuánto', 'dónde', 'él', 'gordo', 'pero', 'por qué', 'qué', 'quién', 'todo', 'yo', 'beber', 'querer', 'trabajar', 'volar', 'la oferta', 'agotado', 'la panadería', 'el banco', 'el importe', 'el pago', 'barato', 'el céntimo', 'la droguería', 'comprar', 'el mercadillo', 'la garantía', 'usado', 'el sueldo', 'el dinero', 'la caja', 'el dinero suelto', 'gratuito', 'el cliente', 'la clienta', 'el despegue', 'la salida', 'salir', 'llegar', 'la llegada', 'la estancia', 'el mirador', 'el bañador', 'bañarse', 'la estación', 'el andén', 'visitar', 'al autobús', 'la habitación doble', 'la habitación individual', 'la recepción', 'el pasajero', 'el billete', 'el horario', 'el vuelvo', 'el aeropuerte', 'el avión', 'el equipaje', 'el hotel', 'la maleta', 'el mapa', 'el pasaporte', 'el viaje', 'viajar', 'la vuelta', 'la sombra', 'nadar', 'la playa', 'bucear', 'el traje', 'el biquini', 'la blusa', 'el monedero', 'el guante', 'el bolso', 'la camisa', 'el sombrero', 'la chaqueta', 'el vestido', 'la corbata', 'el maquillaje', 'el abrigo', 'el perfume', 'el jersey', 'el paraguas', 'la falda', 'la bufanda', 'el zapato', 'la bota', 'el calectín', 'la camiseta', 'el bolso', 'la ropa interior', 'el cepillo de dientes', 'la manzana', 'la berenjena', 'el aguacate', 'el plátano', 'la pera', 'el panecillo', 'la fresa', 'el café solo', 'la comida', 'el pescado', 'la carne', 'la trucha', 'la gamba', 'la carne de ave', 'la bebida', 'el pepino', 'la carne picada', 'la pechuga de pollo', 'el yogur', 'el café', 'la patata', 'el ajo', 'el salmón', 'la fruta', 'el aceite', 'la naranja', 'el pimiento', 'la pimienta', 'maduro', 'crudo', 'el vino tinto', 'el zumo', 'la sal', 'picante', 'el jamón', 'el bistec', 'el té', 'el atún', 'el tomate', 'la vista', 'el árbol', 'la montaña', 'el rayo', 'la flor', 'el trueno', 'el campo', 'la roca', 'el río', 'la primavera', 'la tormenta', 'el otoño', 'el calor', 'el frío', 'la costa', 'el mar', 'la naturaleza', 'el norte', 'el este', 'la planta', 'la lluvia', 'el verano', 'el sol', 'el sur', 'el valle', 'la temperatura', 'el bosque', 'el agua', 'el oeste', 'el viento', 'el invierno', 'la nube', 'el desierto', 'el comienzo', 'la duración', 'el momento', 'el tiempo', 'por la tarde', 'por la noche', 'la tarde', 'el mediodía', 'la noche', 'el pasado', 'el futuro', 'el reloij', 'la fecha', 'anual', 'el calendario', 'el segundo', 'la hora', 'el fin de semana', 'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre', 'el cubo de basura', 'lavar', 'la bañera', 'el balcón', 'la escoba', 'los cubiertos', 'la cama', 'el sofá', 'la ducha', 'la entrada', 'el comedor', 'la ventana', 'el telvisor', 'el garaje', 'la casa', 'la puerta de casa', 'la cocina', 'el sótano', 'la almohada', 'la nevera', 'la lámpara', 'limpiar', 'el dormitorio', 'la llave', 'el armario', 'el espejo', 'el enchufe', 'el piso', 'la silla', 'la taza', 'el plato', 'la alfombra', 'el servicio', 'la escalera', 'la puerta', 'la ropa', 'la colada', 'el piso', 'el salón', 'la habitación', 'los animales', 'los caballos', 'los perros', 'los peces', 'las vacas', 'los alemanes', 'los bolígrafos', 'las botellas', 'las casas', 'las ciudades', 'las coches', 'los cuadernos', 'los hombres', 'los imbéciles', 'los libros', 'las paredes', 'los razones', 'las torres', 'los dientes', 'los manos', 'los padres', 'los hermanos', 'las cebollas', 'las zanahorias', 'los baños', 'las cocinas', 'las cucharas', 'los cuchillos', 'las mesas', 'las sillas', 'los tenedores', 'los vasos', 'las lunas', 'las vacaciones', 'las gafas', 'los pantalones', 'los vaqueros', 'las joyas', 'las gafas del sol', 'los fiambres']
GERMAN = ['das Tier', 'das Pferd', 'der Hund', 'der Fisch', 'die Kuh', 'auf Wiedersehen', 'der Deutsche', 'willkommen', 'der Kugelschreiber', 'die Flasche', 'gute Nacht', 'guten Tag', 'guten Morgen', 'das Haus', 'die Bürste', 'die Zigarette', 'die Stadt', 'das Auto', 'wie geht es dir', 'das Heft', 'gern geschehen', 'die Leute', 'die Zigeunerin', 'der Zigeuner', 'danke', 'der Krieg', 'bis später', 'bis morgen', 'bis dann', 'hallo', 'der Mann', 'der Idiot', 'das Buch', 'viel Glück', 'vielen Dank', 'sehr erfreut', 'das Mädchen', 'der Junge', 'die Wand', 'viel Spaß', 'bitte', "wie geht's", 'der Grund', 'der Turm', 'der Zahn', 'die Hand', 'gestern', 'der Tag', 'Sonntag', 'heute', 'Donnerstag', 'Montag', 'morgen', 'Dienstag', 'Mittwoch', 'Samstag', 'die Woche', 'Freitag', 'die Oma', 'der Opa', 'lieben', 'die Freundin', 'der Freund', 'küssen', 'die Hochzeit', 'heiraten', 'der Geburtstag', 'die Scheidung', 'die Famillie', 'die Schwester', 'der Bruder', 'die Tochter', 'der Sohn', 'die Mutter', 'der Ehemann', 'die Ehe', 'die Frau', 'die Enkelin', 'der Enkel', 'die Freundin', 'der Freund', 'der Vater', 'mögen', 'ich liebe Dich', 'die Tante', 'der Onkel', 'die Zwiebel', 'die Schokolade', 'die Wurst', 'das Mehl', 'der Wein', 'die Karotte', 'das Bad', 'die Küche', 'der Löffel', 'das Messer', 'der Tisch', 'der Stuhl', 'die Gabel', 'das Glas', 'der Mond', 'vierzehn', 'null', 'hundert', 'fünf', 'fünfzig', 'vierzig', 'vier', 'neunzehn', 'achtzehn', 'sechzehn', 'siebzehn', 'zehn', 'zwölf', 'zwei', 'tausend', 'neunzig', 'neun', 'achtzig', 'acht', 'elf', 'fünfzehn', 'sechs', 'sechzig', 'siebzig', 'sieben', 'dreizehn', 'dreißig', 'drei', 'eins', 'zwanzig', 'wie', 'wann', 'wie viel', 'wo', 'er', 'dick', 'aber', 'warum', 'was', 'wer', 'alles', 'ich', 'trinken', 'wollen', 'arbeiten', 'fliegen', 'das Angebot', 'ausverkauft', 'die Bäckerei', 'die Bank', 'der Betrag', 'die Bezahlung', 'billig', 'der Cent', 'die Drogerie', 'einkaufen', 'der Flohmarkt', 'die Garantie', 'gebraucht', 'das Gehalt', 'das Geld', 'die Kasse', 'das Kleingeld', 'kostenlos', 'der Kunde', 'die Kundin', 'der Abflug', 'die Abreise', 'abreisen', 'ankommen', 'die Ankunft', 'der Aufenthalt', 'der Aussichtspunkt', 'die Badehose', 'baden', 'der Bahnhof', 'der Bahnsteig', 'besuchen', 'der Bus', 'das Doppelzimmer', 'das Einzelzimmer', 'die Rezeption', 'der Fahrgast', 'die Fahrkarte', 'der Fahrplan', 'der Flug', 'der Flughafen', 'das Flugzeug', 'das Gepäck', 'das Hotel', 'der Koffer', 'die Landkarte', 'der Pass', 'die Reise', 'reisen', 'die Rückfahrt', 'der Schatten', 'schwimmen', 'der Strand', 'tauchen', 'der Anzug', 'der Bikini', 'die Bluse', 'der Geldbeutel', 'der Handschuh', 'die Handtasche', 'das Hemd', 'der Hut', 'die Jacke', 'das Kleid', 'die Krawatte', 'das Make-Up', 'der Mantel', 'das Parfüm', 'der Pullover', 'der Regenschirm', 'der Rock', 'der Schal', 'der Schuh', 'der Stiefel', 'der Strumpf', 'das T-Shirt', 'die Tasche', 'die Unterwäsche', 'die Zahnbürste', 'der Apfel', 'die Aubergine', 'die Avocado', 'die Banane', 'die Birne', 'das Brötchen', 'die Erdbeere', 'der Espresso', 'das Essen', 'der Fisch', 'das Fleisch', 'die Forelle', 'die Garnele', 'das Geflügel', 'das Getränk', 'die Gurke', 'das Hackfleisch', 'die Hähnchenbrust', 'der Joghurt', 'der Kaffee', 'die Kartoffel', 'der Knoblauch', 'der Lachs', 'das Obst', 'das Öl', 'die Orange', 'die Paprika', 'der Pfeffer', 'reif', 'roh', 'der Rotwein', 'der Saft', 'das Salz', 'scharf', 'der Schinken', 'das Steak', 'der Tee', 'der Thunfisch', 'die Tomate', 'die Aussicht', 'der Baum', 'der Berg', 'der Blitz', 'die Blume', 'der Donner', 'das Feld', 'der Fels', 'der Fluss', 'der Frühling', 'das Gewitter', 'der Herbst', 'die Hitze', 'die Kälte', 'die Küste', 'das Meer', 'die Natur', 'der Norden', 'der Osten', 'die Pflanze', 'der Regen', 'der Sommer', 'die Sonne', 'der Süden', 'das Tal', 'die Temperatur', 'der Wald', 'das Wasser', 'der Westen', 'der Wind', 'der Winter', 'die Wolke', 'die Wüste', 'der Anfang', 'die Dauer', 'der Moment', 'die Zeit', 'abends', 'nachts', 'der Nachmittag', 'der Mittag', 'die Nacht', 'die Vergangenheit', 'die Zukunft', 'die Uhr', 'das Datum', 'jährlich', 'der Kalender', 'die Sekunde', 'die Stunde', 'das Wochenende', 'Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember', 'der Abfalleimer', 'abspülen', 'die Badewanne', 'der Balkon', 'der Besen', 'das Besteck', 'das Bett', 'das Sofa', 'die Dusche', 'der Eingang', 'das Esszimmer', 'das Fenster', 'der Fenseher', 'die Garage', 'das Haus', 'die Haustür', 'der Küche', 'der Keller', 'das Kissen', 'der Kühlschrank', 'die Lampe', 'putzen', 'das Schlafzimmer', 'der Schlüssel', 'der Schrank', 'der Spiegel', 'die Steckdose', 'das Stockwerk', 'der Stuhl', 'die Tasse', 'der Teller', 'der Teppich', 'die Toilette', 'die Treppe', 'die Tür', 'die Kleidung', 'die Wäsche', 'die Wohnung', 'das Wohnzimmer', 'das Zimmer', 'die Tiere', 'die Pferde', 'die Hunde', 'die Fische', 'die Kühe', 'die Deutschen', 'die Kugelschreiber', 'die Flaschen', 'die Häuser', 'die Städte', 'die Autos', 'die Hefte', 'die Männer', 'die Idioten', 'die Bücher', 'die Wände', 'die Gründe', 'die Türme', 'die Zähne', 'die Hände', 'die Eltern', 'die Geschwister', 'die Zwiebeln', 'die Karotten', 'die Bäder', 'die Küchen', 'die Löffel', 'die Messer', 'die Tische', 'die Stühle', 'die Gabeln', 'die Gläser', 'die Monde', 'der Urlaub', 'die Brille', 'die Hose', 'die Jeans', 'der Schmuck', 'die Sonnenbrille', 'der Aufschnitt']
CATEGORY = ['ANIMAL', 'ANIMAL', 'ANIMAL', 'ANIMAL', 'ANIMAL', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BODY', 'BODY', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FAMILY', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'LIVING', 'LIVING', 'LIVING', 'LIVING', 'LIVING', 'LIVING', 'LIVING', 'LIVING', 'NATURE', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'TBD', 'TBD', 'TBD', 'TBD', 'TBD', 'TBD', 'TBD', 'TBD', 'TBD', 'TBD', 'TBD', 'TBD', 'VERB', 'VERB', 'VERB', 'VERB', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'CLOTHS', 'CLOTHS', 'CLOTHS', 'CLOTHS', 'CLOTHS', 'CLOTHS', 'CLOTHS', 'CLOTHS', 'CLOTHS', 'CLOTHS', 'CLOTHS', 'CLOTHS', 'CLOTHS', 'CLOTHS', 'CLOTHS', 'CLOTHS', 'CLOTHS', 'CLOTHS', 'CLOTHS', 'CLOTHS', 'CLOTHS', 'CLOTHS', 'CLOTHS', 'CLOTHS', 'CLOTHS', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'FOOD', 'NATURE', 'NATURE', 'NATURE', 'NATURE', 'NATURE', 'NATURE', 'NATURE', 'NATURE', 'NATURE', 'NATURE', 'NATURE', 'NATURE', 'NATURE', 'NATURE', 'NATURE', 'NATURE', 'NATURE', 'NATURE', 'NATURE', 'NATURE', 'NATURE', 'NATURE', 'NATURE', 'NATURE', 'NATURE', 'NATURE', 'NATURE', 'FOOD', 'NATURE', 'NATURE', 'NATURE', 'NATURE', 'NATURE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'BASIS', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', 'DATE', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'ANIMAL', 'ANIMAL', 'ANIMAL', 'ANIMAL', 'ANIMAL', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BASIS', 'BODY', 'BODY', 'FAMILY', 'FAMILY', 'FOOD', 'FOOD', 'LIVING', 'LIVING', 'LIVING', 'LIVING', 'LIVING', 'LIVING', 'LIVING', 'LIVING', 'NATURE', '', 'CLOTHS', 'CLOTHS', 'CLOTHS', 'CLOTHS', 'CLOTHS', 'FOOD']

# CONSTANTS ############################################################################################################

CATEGORY_UNIQUE = [i.capitalize() for i in set(CATEGORY)]
DICT_LANGUAGE_SETTING = {
	"Random": "arrow-left-right",
	"ES -> DE": "arrow-right",
	"ES <- DE": "arrow-left",
}

# GLOBAL VARIABLES #####################################################################################################

language_setting_mode = list(DICT_LANGUAGE_SETTING.keys())[1]
category_var = ""


# FUNCTIONS ############################################################################################################

def language_setting(mode: str) -> (list, list):
	if mode == list(DICT_LANGUAGE_SETTING.keys())[0]:
		if random.randint(0, 1) == 0:
			return SPANISH.copy(), GERMAN.copy()
		else:
			return GERMAN.copy(), SPANISH.copy()
	if mode == list(DICT_LANGUAGE_SETTING.keys())[1]:
		return SPANISH.copy(), GERMAN.copy()
	if mode == list(DICT_LANGUAGE_SETTING.keys())[2]:
		return GERMAN.copy(), SPANISH.copy()


# CLASS ################################################################################################################

class VocabularyTrainer(MDApp):
	# TODO: show a streak

	in_class = ObjectProperty(None)
	language_setting_dict = DICT_LANGUAGE_SETTING.copy()

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.theme_cls.primary_palette = "Teal"
		self.theme_cls.primary_hue = "700"
		self.theme_cls.theme_style = "Light"
		self.screen = Builder.load_file("main.kv")
		menu_items = [
			{
				"text": f"{category}",
				"viewclass": "OneLineListItem",
				"height": dp(56),
				"on_release": lambda x=f"{category}": self.callback(x),
			} for category in ["All"] + CATEGORY_UNIQUE
		]
		self.menu = MDDropdownMenu(
			caller=self.screen.ids.button_category,
			items=menu_items,
			width_mult=3,
			max_height=dp(224),
			background_color=self.theme_cls.primary_light,
		)

	# SCREEN 2 - START -------------------------------------------------------------------------------------------------

	def next(self):
		global n
		global words_out_used
		words_in, words_out = language_setting(mode=language_setting_mode)
		if category_var != "":
			idxs = [i for i, e in enumerate(CATEGORY) if e == category_var]
			words_in_used = [words_in[i] for i in idxs]
			words_out_used = [words_out[i] for i in idxs]
		else:
			idxs = [e for i, e in enumerate(CATEGORY)]
			words_in_used = words_in.copy()
			words_out_used = words_out.copy()
		n = random.randint(0, len(idxs)-1)
		label = self.root.ids.label_word_in
		label.text = words_in_used[n]
		self.root.in_class.text = ""
		label = self.root.ids.label_word_out
		label.text = ""

	def check(self):
		if self.root.in_class.text == words_out_used[n]:
			label = self.root.ids.label_word_out
			label.text = "[color=238823]Correct =)[/color]"
		else:
			label = self.root.ids.label_word_out
			label.text = "[color=D2222D]Wrong =([/color]"

	def solve(self):
		label = self.root.ids.label_word_out
		label.text = words_out_used[n]

	def callback(self, instance):
		global category_var
		if instance == "All":
			category_var = ""
		else:
			category_var = instance.upper()
		label = self.root.ids.label_category
		label.text = f"Category: {category_var.capitalize()}"
		self.menu.dismiss()

	def language_setting_callback(self, instance):
		global language_setting_mode
		language_setting_mode = [key for key, value in DICT_LANGUAGE_SETTING.items() if value == instance.icon][0]

	# SCREEN 3 - ABOUT -------------------------------------------------------------------------------------------------

	def open_link(self, link: str):
		webbrowser.open(url=link)

	# BUILD ------------------------------------------------------------------------------------------------------------

	def build(self):
		return self.screen


VocabularyTrainer().run()
