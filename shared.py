# SPDX-License-Identifier: GPL-3.0-or-later
"""Shared constants, translations, shortcut helpers and unit helpers."""

import bpy

_PROJECT_URL = "https://github.com/Matsm-Studio/Unreal-Viewport-Navigation-WASD"
_ISSUES_URL = f"{_PROJECT_URL}/issues"

_SHIFT_KEYS = {"LEFT_SHIFT", "RIGHT_SHIFT"}
_CTRL_KEYS = {"LEFT_CTRL", "RIGHT_CTRL"}
_ALT_KEYS = {"LEFT_ALT", "RIGHT_ALT"}

_NAVIGATION_PRESET_ITEMS = (
    ("UNREAL", "Unreal Engine", "RMB + WASD, responsive free-flight navigation"),
    ("BLENDER", "Blender", "Middle-mouse navigation with Blender-oriented motion"),
    ("MAYA", "Maya", "Alt-based navigation and orbit controls"),
    ("UNITY", "Unity", "RMB + WASD with fast free-flight movement"),
    ("GODOT", "Godot", "RMB + WASD with level movement"),
    ("CUSTOM", "Custom", "Use the shortcuts and motion settings below"),
)
_NAVIGATION_KEYS_ITEMS = (
    ("WASD", "WASD", "Use W, A, S and D for horizontal movement"),
    ("ARROWS", "Arrow keys", "Use the arrow keys for horizontal movement"),
    ("BOTH", "WASD + Arrow keys", "Use both WASD and arrow keys"),
    ("CUSTOM", "Custom", "Assign every movement action separately"),
)
_MOVEMENT_MODE_ITEMS = (
    ("FREE", "Free flight", "Forward and backward follow the viewing direction"),
    ("LEVEL", "Level", "Forward and backward stay parallel to the world XY plane"),
)
_CROSSHAIR_STYLE_ITEMS = (
    ("CROSS", "Cross", "Four crosshair lines with a center gap"),
    ("CROSS_DOT", "Cross + dot", "Crosshair lines with a center dot"),
    ("DOT", "Dot", "Center dot only"),
    ("CIRCLE", "Circle", "Center circle"),
    ("FILLED_CIRCLE", "Filled circle", "Solid filled circle in the center"),
)
_MODIFIER_ITEMS = (
    ("NONE", "None", "No modifier"),
    ("SHIFT", "Shift", "Either Shift key"),
    ("CTRL", "Ctrl", "Either Ctrl key"),
    ("ALT", "Alt", "Either Alt key"),
)
_MOUSE_BUTTON_ITEMS = (
    ("RIGHTMOUSE", "Right Mouse Button", "Right mouse button"),
    ("MIDDLEMOUSE", "Middle Mouse Button", "Middle mouse button"),
    ("LEFTMOUSE", "Left Mouse Button", "Left mouse button"),
)
_HUD_POSITION_ITEMS = (
    ("HEADER", "Top - viewport header", "Classic v1.1.1-style information in the viewport header"),
    ("TOP_LEFT", "Top left", "Overlay in the top-left corner"),
    ("TOP_RIGHT", "Top right", "Overlay in the top-right corner"),
    ("BOTTOM_LEFT", "Bottom left", "Overlay in the bottom-left corner"),
    ("BOTTOM_CENTER", "Bottom center", "Overlay centered along the bottom edge"),
    ("BOTTOM_RIGHT", "Bottom right", "Overlay in the bottom-right corner"),
    ("SPLIT", "Split top / bottom", "Speed in the viewport header and controls centered at the bottom"),
)
_SPEED_UNIT_ITEMS = (
    ("BU_S", "Blender units / s", "Blender units per second"),
    ("M_S", "Meters / s", "Meters per second"),
    ("CM_S", "Centimeters / s", "Centimeters per second"),
    ("MM_S", "Millimeters / s", "Millimeters per second"),
    ("KM_H", "Kilometers / h", "Kilometers per hour"),
    ("FT_S", "Feet / s", "Feet per second"),
    ("MPH", "Miles / h", "Miles per hour"),
)

_LANGUAGE_ITEMS = (
    ("EN", "English", "Use English"),
    ("PL", "Polski", "Używaj języka polskiego"),
    ("DE", "Deutsch", "Deutsch verwenden"),
    ("ES", "Español", "Usar español"),
    ("FR", "Français", "Utiliser le français"),
    ("IT", "Italiano", "Usa italiano"),
    ("PT_BR", "Português (Brasil)", "Usar português do Brasil"),
    ("RU", "Русский", "Использовать русский язык"),
    ("JA", "日本語", "日本語を使用"),
    ("ZH_CN", "简体中文", "使用简体中文"),
    ("UK", "Українська", "Використовувати українську"),
    ("CS", "Čeština", "Použít češtinu"),
    ("NL", "Nederlands", "Nederlands gebruiken"),
    ("TR", "Türkçe", "Türkçe kullan"),
    ("KO", "한국어", "한국어 사용"),
)

# The original compact table stores the first 10 languages. Five additional
# languages are layered on top without changing the stable base tuples.
_BASE_LANG_CODES = ('EN', 'PL', 'DE', 'ES', 'FR', 'IT', 'PT_BR', 'RU', 'JA', 'ZH_CN')
_TR_ROWS = {
    'acceleration_time': ('Time to full speed', 'Czas do pełnej prędkości', 'Zeit bis Höchstgeschwindigkeit', 'Tiempo hasta velocidad máxima', 'Temps jusqu’à pleine vitesse', 'Tempo alla velocità massima', 'Tempo até velocidade máxima', 'Время разгона', '最高速度までの時間', '达到全速时间'),
    'advanced_and_tools': ('Advanced and tools', 'Zaawansowane i narzędzia', 'Erweitert und Werkzeuge', 'Avanzado y herramientas', 'Avancé et outils', 'Avanzate e strumenti', 'Avançado e ferramentas', 'Дополнительно и инструменты', '詳細設定とツール', '高级与工具'),
    'advanced_controls': ('Controls and custom keys', 'Sterowanie i własne klawisze', 'Steuerung und eigene Tasten', 'Controles y teclas personalizadas', 'Commandes et touches personnalisées', 'Controlli e tasti personalizzati', 'Controles e teclas personalizadas', 'Управление и свои клавиши', '操作とカスタムキー', '控制和自定义按键'),
    'advanced_help': ('Less-common behavior, speed limits, conflict checking, reset and project links.', 'Rzadziej używane zachowanie, limity prędkości, konflikty skrótów, reset i linki projektu.', 'Seltener benötigtes Verhalten, Geschwindigkeitsgrenzen, Konfliktprüfung, Zurücksetzen und Links.', 'Opciones menos usadas, límites de velocidad, conflictos, restablecimiento y enlaces.', 'Options moins courantes, limites de vitesse, conflits, réinitialisation et liens.', 'Opzioni meno comuni, limiti di velocità, conflitti, ripristino e link.', 'Opções menos usadas, limites de velocidade, conflitos, restauração e links.', 'Редкие параметры, пределы скорости, проверка конфликтов, сброс и ссылки.', '使用頻度の低い動作、速度制限、競合チェック、リセット、プロジェクトリンクです。', '较少使用的行为、速度限制、冲突检查、重置和项目链接。'),
    'backward_key': ('Backward', 'Do tyłu', 'Rückwärts', 'Atrás', 'Arrière', 'Indietro', 'Trás', 'Назад', '後退', '后退'),
    'base_speed': ('Movement speed', 'Prędkość ruchu', 'Bewegungsgeschwindigkeit', 'Velocidad de movimiento', 'Vitesse de déplacement', 'Velocità movimento', 'Velocidade de movimento', 'Скорость движения', '移動速度', '移动速度'),
    'camera_help': ('Camera View uses the same navigation. Orbit rotates around the selected object.', 'Camera View używa tego samego sterowania. Orbita obraca widok wokół zaznaczonego obiektu.', 'Camera View nutzt dieselbe Navigation. Orbit dreht um das ausgewählte Objekt.', 'Camera View usa la misma navegación. La órbita gira alrededor del objeto seleccionado.', 'Camera View utilise la même navigation. L’orbite tourne autour de l’objet sélectionné.', 'Camera View usa la stessa navigazione. L’orbita ruota attorno all’oggetto selezionato.', 'Camera View usa a mesma navegação. A órbita gira ao redor do objeto selecionado.', 'Camera View использует то же управление. Орбита вращается вокруг выбранного объекта.', 'Camera View でも同じ操作を使います。オービットは選択物を中心に回転します。', '相机视图使用相同导航。环绕会围绕选中的对象旋转。'),
    'camera_orbit': ('Camera and orbit', 'Kamera i orbita', 'Kamera und Orbit', 'Cámara y órbita', 'Caméra et orbite', 'Camera e orbita', 'Câmera e órbita', 'Камера и орбита', 'カメラとオービット', '相机和环绕'),
    'camera_orbit_protection_note': ('In Camera View, protection requires a selected target. Esc restores the original camera frame.', 'W widoku kamery ochrona wymaga zaznaczonego celu. Esc przywraca pierwotny kadr kamery.', 'In der Kameraansicht benötigt der Schutz ein ausgewähltes Ziel. Esc stellt den ursprünglichen Bildausschnitt wieder her.', 'En Camera View, la protección requiere un objetivo seleccionado. Esc restaura el encuadre original.', 'En Camera View, la protection exige une cible sélectionnée. Échap restaure le cadrage initial.', 'In Camera View, la protezione richiede un bersaglio selezionato. Esc ripristina l’inquadratura iniziale.', 'Na Camera View, a proteção exige um alvo selecionado. Esc restaura o enquadramento original.', 'В Camera View защита требует выбранную цель. Esc восстанавливает исходный кадр камеры.', 'Camera View では保護時に選択ターゲットが必要です。Esc で元のカメラ構図に戻せます。', '在相机视图中，保护模式需要选定目标。按 Esc 可恢复原始相机构图。'),
    'camera_view_navigation': ('Control the active camera in Camera View', 'Steruj aktywną kamerą w Camera View', 'Aktive Kamera in der Kameraansicht steuern', 'Controlar cámara activa en vista de cámara', 'Contrôler la caméra active en vue caméra', 'Controlla camera attiva in Camera View', 'Controlar câmera ativa na visão da câmera', 'Управлять активной камерой в Camera View', 'カメラビューでアクティブカメラを操作', '在相机视图中控制活动相机'),
    'check_conflicts': ('Check conflicts', 'Sprawdź konflikty', 'Konflikte prüfen', 'Comprobar conflictos', 'Vérifier les conflits', 'Controlla conflitti', 'Verificar conflitos', 'Проверить', '競合を確認', '检查冲突'),
    'conflict_duplicate': ('Duplicate add-on assignment: {shortcut} is used by {actions}', 'Powielone przypisanie dodatku: {shortcut} obsługuje {actions}', 'Duplicate add-on assignment: {shortcut} is used by {actions}', 'Duplicate add-on assignment: {shortcut} is used by {actions}', 'Duplicate add-on assignment: {shortcut} is used by {actions}', 'Duplicate add-on assignment: {shortcut} is used by {actions}', 'Duplicate add-on assignment: {shortcut} is used by {actions}', 'Duplicate add-on assignment: {shortcut} is used by {actions}', 'Duplicate add-on assignment: {shortcut} is used by {actions}', 'Duplicate add-on assignment: {shortcut} is used by {actions}'),
    'conflict_external': ('{shortcut} also runs {operator} in {keymap}', '{shortcut} uruchamia też {operator} w {keymap}', '{shortcut} also runs {operator} in {keymap}', '{shortcut} also runs {operator} in {keymap}', '{shortcut} also runs {operator} in {keymap}', '{shortcut} also runs {operator} in {keymap}', '{shortcut} also runs {operator} in {keymap}', '{shortcut} also runs {operator} in {keymap}', '{shortcut} also runs {operator} in {keymap}', '{shortcut} also runs {operator} in {keymap}'),
    'conflicts_found': ('Potential conflicts found: {count}', 'Możliwe konflikty: {count}', 'Mögliche Konflikte: {count}', 'Posibles conflictos: {count}', 'Conflits possibles : {count}', 'Possibili conflitti: {count}', 'Possíveis conflitos: {count}', 'Возможные конфликты: {count}', '競合の可能性: {count}', '可能的冲突：{count}'),
    'conflicts_none': ('No direct conflicts found in active Blender and add-on keymaps.', 'Nie znaleziono bezpośrednich konfliktów w aktywnych keymapach.', 'Keine direkten Konflikte in aktiven Keymaps gefunden.', 'No se encontraron conflictos directos.', 'Aucun conflit direct trouvé.', 'Nessun conflitto diretto trovato.', 'Nenhum conflito direto encontrado.', 'Прямых конфликтов не найдено.', '直接の競合は見つかりませんでした。', '未发现直接冲突。'),
    'conflicts_not_checked': ('Not checked after the latest shortcut change.', 'Nie sprawdzono po ostatniej zmianie skrótów.', 'Nach der letzten Tastenänderung nicht geprüft.', 'No comprobado tras el último cambio.', 'Non vérifié après la dernière modification.', 'Non controllato dopo l’ultima modifica.', 'Não verificado após a última alteração.', 'Не проверено после последнего изменения.', '最後の変更後は未確認です。', '最后一次修改后尚未检查。'),
    'controls_help': ('Change shortcuts here. Choose Custom to assign every movement direction.', 'Tutaj zmieniasz skróty. Wybierz Własne, aby przypisać każdy kierunek ruchu.', 'Hier änderst du die Tasten. Mit Benutzerdefiniert kannst du jede Bewegungsrichtung zuweisen.', 'Cambia aquí los atajos. Elige Personalizado para asignar cada dirección.', 'Modifiez les raccourcis ici. Choisissez Personnalisé pour attribuer chaque direction.', 'Modifica qui le scorciatoie. Scegli Personalizzato per assegnare ogni direzione.', 'Altere os atalhos aqui. Escolha Personalizado para definir cada direção.', 'Здесь меняются клавиши. Выберите Свои, чтобы назначить каждое направление.', 'ここでショートカットを変更します。カスタムなら各移動方向を個別に設定できます。', '在这里更改快捷键。选择“自定义”可分别设置每个移动方向。'),
    'control_presets': ('Control style', 'Styl sterowania', 'Steuerungsstil', 'Estilo de control', 'Style de contrôle', 'Stile di controllo', 'Estilo de controle', 'Стиль управления', '操作スタイル', '控制风格'),
    'preset_help': ('Choose a familiar editor or engine. The preset changes shortcuts and motion together.', 'Wybierz znany edytor lub silnik. Preset ustawi jednocześnie skróty i charakter ruchu.', 'Wähle einen vertrauten Editor oder eine Engine. Das Preset ändert Tasten und Bewegungsgefühl gemeinsam.', 'Elige un editor o motor conocido. El preajuste cambia a la vez los atajos y el movimiento.', 'Choisissez un éditeur ou moteur familier. Le préréglage modifie ensemble les raccourcis et le mouvement.', 'Scegli un editor o motore familiare. Il preset cambia insieme scorciatoie e movimento.', 'Escolha um editor ou motor conhecido. O preset altera atalhos e movimento em conjunto.', 'Выберите знакомый редактор или движок. Профиль одновременно меняет клавиши и характер движения.', '使い慣れたエディターやエンジンを選びます。プリセットはショートカットと移動感をまとめて変更します。', '选择熟悉的编辑器或引擎。预设会同时更改快捷键和移动手感。'),
    'current_controls': ('Current controls', 'Aktualne sterowanie', 'Aktuelle Steuerung', 'Controles actuales', 'Commandes actuelles', 'Controlli attuali', 'Controles atuais', 'Текущее управление', '現在の操作', '当前控制'),
    'navigation_behavior_help': ('Mouse feel and movement behavior. All button assignments are in Key bindings below.', 'Tutaj ustawiasz odczucie myszy i zachowanie ruchu. Wszystkie przyciski są w sekcji Przypisanie klawiszy poniżej.', 'Hier stellst du Mausgefühl und Bewegungsverhalten ein. Alle Tasten liegen unten unter Tastenbelegung.', 'Aquí ajustas la sensación del ratón y el movimiento. Todas las teclas están abajo en Asignación de teclas.', 'Réglez ici la sensation de souris et le comportement du mouvement. Toutes les touches sont dans Raccourcis ci-dessous.', 'Qui regoli la risposta del mouse e il movimento. Tutti i tasti sono nella sezione Assegnazione tasti qui sotto.', 'Aqui você ajusta a sensação do mouse e o movimento. Todas as teclas ficam em Atalhos abaixo.', 'Здесь настраиваются ощущения мыши и движение. Все кнопки находятся ниже в разделе назначения клавиш.', 'ここではマウス感度と移動挙動を設定します。ボタン割り当ては下のキーバインドにまとめています。', '这里调整鼠标手感和移动行为。所有按键分配都集中在下方“按键绑定”中。'),
    'key_bindings': ('Key bindings', 'Przypisanie klawiszy', 'Tastenbelegung', 'Asignación de teclas', 'Raccourcis', 'Assegnazione tasti', 'Atalhos', 'Назначение клавиш', 'キーバインド', '按键绑定'),
    'key_bindings_help': ('All shortcuts are edited here. Changing any shortcut automatically switches the preset to Custom.', 'Wszystkie skróty zmieniasz w jednym miejscu. Zmiana dowolnego skrótu automatycznie przełączy preset na Własne.', 'Alle Tastenkürzel werden hier geändert. Jede Änderung schaltet das Preset automatisch auf Benutzerdefiniert.', 'Todos los atajos se editan aquí. Cambiar cualquiera cambia automáticamente el preajuste a Personalizado.', 'Tous les raccourcis se modifient ici. Toute modification passe automatiquement le préréglage sur Personnalisé.', 'Tutte le scorciatoie si modificano qui. Qualsiasi modifica passa automaticamente il preset a Personalizzato.', 'Todos os atalhos são editados aqui. Alterar qualquer um muda automaticamente o preset para Personalizado.', 'Все сочетания меняются здесь. Любое изменение автоматически переключает профиль на Пользовательский.', 'すべてのショートカットをここで変更できます。変更するとプリセットは自動でカスタムになります。', '所有快捷键都在这里修改。更改任意快捷键会自动切换为“自定义”预设。'),
    'navigation_trigger': ('Start navigation', 'Uruchamianie nawigacji', 'Navigation starten', 'Iniciar navegación', 'Démarrer la navigation', 'Avvio navigazione', 'Iniciar navegação', 'Запуск навигации', 'ナビゲーション開始', '启动导航'),
    'movement_bindings': ('Movement keys', 'Klawisze ruchu', 'Bewegungstasten', 'Teclas de movimiento', 'Touches de déplacement', 'Tasti movimento', 'Teclas de movimento', 'Клавиши движения', '移動キー', '移动按键'),
    'modifier_bindings': ('Sprint and precision', 'Sprint i precyzja', 'Sprint und Präzision', 'Sprint y precisión', 'Sprint et précision', 'Sprint e precisione', 'Sprint e precisão', 'Ускорение и точность', 'スプリントと精密移動', '加速与精细移动'),
    'speed_bindings': ('Speed adjustment', 'Zmiana prędkości', 'Geschwindigkeit ändern', 'Ajuste de velocidad', 'Réglage de vitesse', 'Regolazione velocità', 'Ajuste de velocidade', 'Изменение скорости', '速度調整', '速度调整'),
    'orbit_bindings': ('Orbit shortcut', 'Skrót orbity', 'Orbit-Tastenkürzel', 'Atajo de órbita', 'Raccourci d’orbite', 'Scorciatoia orbita', 'Atalho de órbita', 'Клавиши орбиты', 'オービットショートカット', '环绕快捷键'),
    'current_layout': ('Active layout', 'Aktualny układ', 'Aktuelles Layout', 'Diseño actual', 'Disposition actuelle', 'Schema attuale', 'Layout atual', 'Текущая схема', '現在のレイアウト', '当前布局'),
    'uses_key': ('Uses: {button}', 'Używa: {button}', 'Taste: {button}', 'Usa: {button}', 'Utilise : {button}', 'Usa: {button}', 'Usa: {button}', 'Клавиша: {button}', '使用キー: {button}', '使用：{button}'),
    'edit_orbit_in_keys': ('Change this shortcut in Key bindings.', 'Ten skrót zmienisz w sekcji Przypisanie klawiszy.', 'Dieses Tastenkürzel änderst du unter Tastenbelegung.', 'Cambia este atajo en Asignación de teclas.', 'Modifiez ce raccourci dans Raccourcis.', 'Modifica questa scorciatoia in Assegnazione tasti.', 'Altere este atalho em Atalhos.', 'Измените это сочетание в разделе назначения клавиш.', 'このショートカットはキーバインドで変更できます。', '请在“按键绑定”中修改此快捷键。'),
    'crosshair_color': ('Crosshair color', 'Kolor celownika', 'Fadenkreuzfarbe', 'Color de mira', 'Couleur du réticule', 'Colore mirino', 'Cor da mira', 'Цвет прицела', '照準色', '准星颜色'),
    'crosshair_gap': ('Center gap', 'Przerwa w środku', 'Mittlere Lücke', 'Hueco central', 'Espace central', 'Spazio centrale', 'Espaço central', 'Центральный зазор', '中央の隙間', '中心间隙'),
    'crosshair_size': ('Crosshair size', 'Rozmiar celownika', 'Fadenkreuzgröße', 'Tamaño de mira', 'Taille du réticule', 'Dimensione mirino', 'Tamanho da mira', 'Размер прицела', '照準サイズ', '准星大小'),
    'crosshair_style': ('Crosshair style', 'Styl celownika', 'Fadenkreuzstil', 'Estilo de mira', 'Style du réticule', 'Stile mirino', 'Estilo da mira', 'Стиль прицела', '照準スタイル', '准星样式'),
    'crosshair_thickness': ('Line thickness', 'Grubość linii', 'Linienstärke', 'Grosor de línea', 'Épaisseur des lignes', 'Spessore linea', 'Espessura da linha', 'Толщина линии', '線の太さ', '线条粗细'),
    'custom_movement': ('Custom movement actions', 'Własne akcje ruchu', 'Eigene Bewegungsaktionen', 'Acciones de movimiento personalizadas', 'Actions de déplacement personnalisées', 'Azioni di movimento personalizzate', 'Ações de movimento personalizadas', 'Свои клавиши движения', 'カスタム移動アクション', '自定义移动操作'),
    'deceleration_time': ('Braking time', 'Czas hamowania', 'Bremszeit', 'Tiempo de frenado', 'Temps de freinage', 'Tempo di frenata', 'Tempo de frenagem', 'Время торможения', '減速時間', '刹车时间'),
    'display': ('Display', 'Wyświetlanie', 'Anzeige', 'Visualización', 'Affichage', 'Visualizzazione', 'Exibição', 'Отображение', '表示', '显示'),
    'display_help': ('Visual helpers only. They do not change navigation behavior.', 'Tylko elementy wizualne. Nie zmieniają działania nawigacji.', 'Nur visuelle Hilfen. Sie ändern das Navigationsverhalten nicht.', 'Solo ayudas visuales. No cambian el comportamiento de navegación.', 'Aides visuelles uniquement. Elles ne changent pas la navigation.', 'Solo aiuti visivi. Non cambiano il comportamento della navigazione.', 'Apenas recursos visuais. Eles não alteram a navegação.', 'Только визуальные элементы. Они не меняют поведение навигации.', '表示補助のみで、ナビゲーション動作は変わりません。', '仅为视觉辅助，不会改变导航行为。'),
    'down_key': ('Down', 'W dół', 'Runter', 'Abajo', 'Bas', 'Giù', 'Baixo', 'Вниз', '下', '下移'),
    'enable_rmb_click_hold': ('Separate click from hold', 'Rozróżniaj kliknięcie i przytrzymanie', 'Klick und Halten trennen', 'Separar clic y pulsación', 'Séparer clic et maintien', 'Separa clic e pressione', 'Separar clique e segurar', 'Разделять щелчок и удержание', 'クリックと長押しを分離', '区分单击和按住'),
    'error_prefs': ('Could not read add-on preferences', 'Nie można odczytać ustawień dodatku', 'Could not read add-on preferences', 'Could not read add-on preferences', 'Could not read add-on preferences', 'Could not read add-on preferences', 'Could not read add-on preferences', 'Could not read add-on preferences', 'Could not read add-on preferences', 'Could not read add-on preferences'),
    'error_region': ('Start navigation over the main 3D viewport region', 'Uruchom nawigację nad głównym obszarem viewportu 3D', 'Start navigation over the main 3D viewport region', 'Start navigation over the main 3D viewport region', 'Start navigation over the main 3D viewport region', 'Start navigation over the main 3D viewport region', 'Start navigation over the main 3D viewport region', 'Start navigation over the main 3D viewport region', 'Start navigation over the main 3D viewport region', 'Start navigation over the main 3D viewport region'),
    'force_perspective': ('Switch to perspective view', 'Przełącz na perspektywę', 'Zur Perspektivansicht wechseln', 'Cambiar a perspectiva', 'Passer en perspective', 'Passa alla prospettiva', 'Mudar para perspectiva', 'Переключать на перспективу', '透視投影へ切り替え', '切换到透视视图'),
    'forward_key': ('Forward', 'Do przodu', 'Vorwärts', 'Adelante', 'Avant', 'Avanti', 'Frente', 'Вперёд', '前進', '前进'),
    'hide_cursor': ('Hide system cursor while navigating', 'Ukryj kursor podczas nawigacji', 'Systemcursor beim Navigieren ausblenden', 'Ocultar cursor al navegar', 'Masquer le curseur pendant la navigation', 'Nascondi cursore durante la navigazione', 'Ocultar cursor durante navegação', 'Скрывать курсор при навигации', 'ナビゲーション中にカーソルを隠す', '导航时隐藏系统光标'),
    'how_to_use': ('How to use', 'Jak używać', 'Bedienung', 'Cómo usar', 'Utilisation', 'Come usare', 'Como usar', 'Как использовать', '使い方', '使用方法'),
    'navigation_section': ('Navigation', 'Nawigacja', 'Navigation', 'Navegación', 'Navigation', 'Navigazione', 'Navegação', 'Навигация', 'ナビゲーション', '导航'),
    'speed_section': ('Speed', 'Prędkość', 'Geschwindigkeit', 'Velocidad', 'Vitesse', 'Velocità', 'Velocidade', 'Скорость', '速度', '速度'),
    'sprint_short': ('Sprint', 'Sprint', 'Sprint', 'Sprint', 'Sprint', 'Sprint', 'Sprint', 'Ускорение', '高速移動', '冲刺'),
    'precision_short': ('Precision', 'Precyzja', 'Präzision', 'Precisión', 'Précision', 'Precisione', 'Precisão', 'Точность', '精密', '精确'),
    'cursor_crosshair': ('Cursor and crosshair', 'Kursor i celownik', 'Cursor und Fadenkreuz', 'Cursor y retícula', 'Curseur et réticule', 'Cursore e mirino', 'Cursor e mira', 'Курсор и прицел', 'カーソルとクロスヘア', '光标和准星'),
    'custom_keys_help': ('Choose Custom in Movement Layout to assign every movement key yourself.', 'Wybierz Własne w Układzie ruchu, aby samodzielnie przypisać każdy klawisz poruszania.', 'Wähle Benutzerdefiniert im Bewegungslayout, um jede Bewegungstaste selbst zuzuweisen.', 'Elige Personalizado en Diseño de movimiento para asignar cada tecla.', 'Choisissez Personnalisé dans la disposition des déplacements pour attribuer chaque touche.', 'Scegli Personalizzato nello schema movimento per assegnare ogni tasto.', 'Escolha Personalizado no layout de movimento para definir cada tecla.', 'Выберите Свои в схеме движения, чтобы назначить каждую клавишу.', '移動レイアウトでカスタムを選ぶと各移動キーを設定できます。', '在移动布局中选择自定义即可分别设置每个移动键。'),
    'viewport_info': ('Viewport information', 'Informacje w viewporcie', 'Viewport-Informationen', 'Información del viewport', 'Informations du viewport', 'Informazioni viewport', 'Informações do viewport', 'Информация во вьюпорте', 'ビューポート情報', '视口信息'),
    'viewport_info_help': ('Choose where speed and controls appear while navigating. The classic header matches the simpler v1.1.1 style.', 'Wybierz, gdzie podczas nawigacji mają być prędkość i skróty. Klasyczny nagłówek odpowiada prostszemu stylowi z 1.1.1.', 'Wähle, wo Geschwindigkeit und Steuerung während der Navigation erscheinen. Der klassische Kopf entspricht dem einfacheren Stil aus 1.1.1.', 'Elige dónde aparecen la velocidad y los controles al navegar. La cabecera clásica usa el estilo sencillo de la 1.1.1.', 'Choisissez où afficher la vitesse et les commandes pendant la navigation. L’en-tête classique reprend le style simple de la 1.1.1.', 'Scegli dove mostrare velocità e comandi durante la navigazione. L’intestazione classica riprende lo stile semplice della 1.1.1.', 'Escolha onde velocidade e controles aparecem durante a navegação. O cabeçalho clássico segue o estilo simples da 1.1.1.', 'Выберите, где во время навигации показывать скорость и управление. Классический заголовок повторяет простой стиль 1.1.1.', 'ナビゲーション中の速度と操作表示の位置を選びます。クラシックヘッダーは 1.1.1 のシンプルな表示に近いです。', '选择导航时速度和控制提示的显示位置。经典标题栏接近 1.1.1 的简洁风格。'),
    'info_position': ('Information position', 'Pozycja informacji', 'Position der Informationen', 'Posición de la información', 'Position des informations', 'Posizione informazioni', 'Posição das informações', 'Положение информации', '情報の位置', '信息位置'),
    'show_navigation_info': ('Show navigation information', 'Pokazuj informacje nawigacji', 'Navigationsinformationen anzeigen', 'Mostrar información de navegación', 'Afficher les informations de navigation', 'Mostra informazioni di navigazione', 'Mostrar informações de navegação', 'Показывать информацию навигации', 'ナビゲーション情報を表示', '显示导航信息'),
    'show_speed_info': ('Show speed', 'Pokazuj prędkość', 'Geschwindigkeit anzeigen', 'Mostrar velocidad', 'Afficher la vitesse', 'Mostra velocità', 'Mostrar velocidade', 'Показывать скорость', '速度を表示', '显示速度'),
    'show_controls_info': ('Show control hints', 'Pokazuj skróty sterowania', 'Steuerungshinweise anzeigen', 'Mostrar ayudas de control', 'Afficher les aides de commande', 'Mostra suggerimenti comandi', 'Mostrar dicas de controle', 'Показывать подсказки управления', '操作ヒントを表示', '显示控制提示'),
    'split_info_note': ('Split mode keeps speed at the top and control hints at the bottom.', 'Tryb dzielony zostawia prędkość u góry, a skróty sterowania na dole.', 'Geteilter Modus zeigt die Geschwindigkeit oben und Steuerungshinweise unten.', 'El modo dividido deja la velocidad arriba y los controles abajo.', 'Le mode partagé garde la vitesse en haut et les commandes en bas.', 'La modalità divisa mostra la velocità in alto e i comandi in basso.', 'O modo dividido mantém a velocidade em cima e os controles embaixo.', 'Раздельный режим показывает скорость сверху, а управление снизу.', '分割モードでは速度を上、操作ヒントを下に表示します。', '分割模式将速度显示在顶部，控制提示显示在底部。'),
    'header_preview': ('Preview', 'Podgląd', 'Vorschau', 'Vista previa', 'Aperçu', 'Anteprima', 'Prévia', 'Предпросмотр', 'プレビュー', '预览'),
    'hud_camera': ('Camera', 'Kamera', 'Camera', 'Camera', 'Camera', 'Camera', 'Camera', 'Camera', 'Camera', 'Camera'),
    'hud_fov': ('FOV', 'FOV', 'FOV', 'FOV', 'FOV', 'FOV', 'FOV', 'FOV', 'FOV', 'FOV'),
    'hud_opacity': ('HUD opacity', 'Krycie HUD', 'HUD-Deckkraft', 'Opacidad HUD', 'Opacité du HUD', 'Opacità HUD', 'Opacidade HUD', 'Прозрачность HUD', 'HUD 不透明度', 'HUD 不透明度'),
    'hud_ortho': ('Ortho', 'Ortho', 'Ortho', 'Ortho', 'Ortho', 'Ortho', 'Ortho', 'Ortho', 'Ortho', 'Ortho'),
    'hud_scale': ('HUD text size', 'Rozmiar tekstu HUD', 'HUD-Textgröße', 'Tamaño de texto HUD', 'Taille du texte HUD', 'Dimensione testo HUD', 'Tamanho do texto HUD', 'Размер текста HUD', 'HUD 文字サイズ', 'HUD 文字大小'),
    'hud_speed': ('Speed', 'Prędkość', 'Speed', 'Speed', 'Speed', 'Speed', 'Speed', 'Speed', 'Speed', 'Speed'),
    'hud_viewport': ('Viewport', 'Viewport', 'Viewport', 'Viewport', 'Viewport', 'Viewport', 'Viewport', 'Viewport', 'Viewport', 'Viewport'),
    'instant_stop': ('Stop immediately after releasing movement keys', 'Zatrzymuj natychmiast po puszczeniu klawiszy ruchu', 'Nach dem Loslassen der Bewegungstasten sofort stoppen', 'Detener inmediatamente al soltar las teclas de movimiento', 'Arrêter immédiatement au relâchement des touches de déplacement', 'Arresta subito quando rilasci i tasti di movimento', 'Parar imediatamente ao soltar as teclas de movimento', 'Останавливать сразу после отпускания клавиш движения', '移動キーを離したら即座に停止', '松开移动键后立即停止'),
    'invert_y': ('Invert Y axis', 'Odwróć oś Y', 'Y-Achse umkehren', 'Invertir eje Y', 'Inverser l’axe Y', 'Inverti asse Y', 'Inverter eixo Y', 'Инвертировать ось Y', 'Y 軸を反転', '反转 Y 轴'),
    'language': ('Interface language', 'Język interfejsu', 'Oberflächensprache', 'Idioma de la interfaz', 'Langue de l’interface', 'Lingua interfaccia', 'Idioma da interface', 'Язык интерфейса', 'インターフェース言語', '界面语言'),
    'left_key': ('Left', 'W lewo', 'Links', 'Izquierda', 'Gauche', 'Sinistra', 'Esquerda', 'Влево', '左', '左移'),
    'look_sensitivity': ('Mouse sensitivity', 'Czułość myszy', 'Mausempfindlichkeit', 'Sensibilidad del ratón', 'Sensibilité de la souris', 'Sensibilità mouse', 'Sensibilidade do mouse', 'Чувствительность мыши', 'マウス感度', '鼠标灵敏度'),
    'maximum_speed': ('Maximum speed', 'Maksymalna prędkość', 'Maximale Geschwindigkeit', 'Velocidad máxima', 'Vitesse maximale', 'Velocità massima', 'Velocidade máxima', 'Максимальная скорость', '最高速度', '最高速度'),
    'minimum_speed': ('Minimum speed', 'Minimalna prędkość', 'Minimale Geschwindigkeit', 'Velocidad mínima', 'Vitesse minimale', 'Velocità minima', 'Velocidade mínima', 'Минимальная скорость', '最低速度', '最低速度'),
    'modifier_roles': ('What each modifier does', 'Co robią modyfikatory', 'Funktion der Modifikatortasten', 'Función de cada modificador', 'Rôle de chaque modificateur', 'Funzione dei modificatori', 'Função de cada modificador', 'Назначение модификаторов', '修飾キーの役割', '修饰键的作用'),
    'more_settings': ('More settings are available in Add-on Preferences.', 'Więcej ustawień znajdziesz w preferencjach dodatku.', 'Weitere Einstellungen sind in den Add-on-Einstellungen verfügbar.', 'Hay más opciones en las preferencias del complemento.', 'D’autres réglages sont disponibles dans les préférences de l’extension.', 'Altre impostazioni sono disponibili nelle preferenze dell’add-on.', 'Mais opções estão disponíveis nas preferências do complemento.', 'Дополнительные параметры находятся в настройках дополнения.', '追加設定はアドオン設定にあります。', '更多设置位于插件首选项中。'),
    'motion': ('Motion', 'Ruch', 'Bewegung', 'Movimiento', 'Mouvement', 'Movimento', 'Movimento', 'Движение', 'モーション', '运动'),
    'motion_help': ('Tune how quickly movement accelerates. Keep Immediate Stop on for precise control.', 'Ustaw, jak szybko ruch się rozpędza. Zostaw natychmiastowe zatrzymanie dla precyzyjnego sterowania.', 'Stelle ein, wie schnell die Bewegung beschleunigt. Sofortiges Stoppen sorgt für präzise Kontrolle.', 'Ajusta la rapidez de aceleración. Mantén la parada inmediata para un control preciso.', 'Réglez la vitesse d’accélération. Gardez l’arrêt immédiat pour un contrôle précis.', 'Regola la rapidità dell’accelerazione. Mantieni l’arresto immediato per un controllo preciso.', 'Ajuste a rapidez da aceleração. Mantenha a parada imediata para controle preciso.', 'Настройте скорость разгона. Оставьте мгновенную остановку для точного управления.', '加速の速さを調整します。正確な操作には即時停止をオンのままにしてください。', '调整移动加速速度。保持“立即停止”开启可获得更精准的控制。'),
    'motion_short_note': ('Lower times react faster. Update Rate only changes sampling.', 'Krótszy czas daje szybszą reakcję. Update Rate zmienia tylko częstotliwość obliczeń.', 'Kürzere Zeiten reagieren schneller. Update Rate ändert nur die Abtastung.', 'Tiempos menores responden más rápido. Update Rate solo cambia el muestreo.', 'Des temps plus courts réagissent plus vite. Update Rate ne change que l’échantillonnage.', 'Tempi minori reagiscono più rapidamente. Update Rate cambia solo il campionamento.', 'Tempos menores respondem mais rápido. Update Rate só muda a amostragem.', 'Меньшее время даёт более быстрый отклик. Update Rate меняет только частоту расчёта.', '短い時間ほど反応が速くなります。Update Rate は計算頻度のみを変更します。', '时间越短，响应越快。Update Rate 只改变计算频率。'),
    'movement_mode': ('Forward/back movement', 'Ruch przód/tył', 'Vorwärts-/Rückwärtsbewegung', 'Movimiento adelante/atrás', 'Mouvement avant/arrière', 'Movimento avanti/indietro', 'Movimento frente/trás', 'Движение вперёд/назад', '前後移動', '前后移动'),
    'navigate_action': ('Navigate', 'Nawigacja', 'Navigation', 'Navegar', 'Navigation', 'Navigazione', 'Navegação', 'Навигация', 'ナビゲーション', '导航'),
    'navigate_during_tools': ('Navigate while using compatible tools', 'Nawigacja podczas używania zgodnych narzędzi', 'Bei kompatiblen Werkzeugen navigieren', 'Navegar con herramientas compatibles', 'Naviguer avec les outils compatibles', 'Naviga con strumenti compatibili', 'Navegar com ferramentas compatíveis', 'Навигация при совместимых инструментах', '対応ツール使用中もナビゲート', '使用兼容工具时仍可导航'),
    'navigation_keys': ('Movement layout', 'Układ ruchu', 'Bewegungslayout', 'Diseño de movimiento', 'Disposition des déplacements', 'Schema movimento', 'Layout de movimento', 'Схема движения', '移動レイアウト', '移动布局'),
    'navigation_modifier': ('Navigation modifier', 'Modyfikator nawigacji', 'Navigationsmodifikator', 'Modificador de navegación', 'Modificateur de navigation', 'Modificatore navigazione', 'Modificador de navegação', 'Модификатор навигации', 'ナビゲーション修飾キー', '导航修饰键'),
    'navigation_mouse': ('Navigation mouse button', 'Przycisk myszy nawigacji', 'Navigations-Maustaste', 'Botón de navegación', 'Bouton de navigation', 'Pulsante navigazione', 'Botão de navegação', 'Кнопка навигации', 'ナビゲーションマウスボタン', '导航鼠标键'),
    'navigation_preset': ('Navigation preset', 'Preset nawigacji', 'Navigationsprofil', 'Preajuste de navegación', 'Préréglage de navigation', 'Preset navigazione', 'Predefinição de navegação', 'Профиль навигации', 'ナビゲーションプリセット', '导航预设'),
    'no_preferences': ('Add-on preferences are unavailable', 'Brak dostępu do ustawień dodatku', 'Add-on-Einstellungen nicht verfügbar', 'Preferencias no disponibles', 'Préférences indisponibles', 'Preferenze non disponibili', 'Preferências indisponíveis', 'Настройки недоступны', 'アドオン設定を利用できません', '无法使用插件设置'),
    'none': ('None', 'Brak', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None'),
    'orbit_enable_short': ('Orbit selection', 'Orbita zaznaczenia', 'Auswahl-Orbit', 'Órbita de selección', 'Orbite sélection', 'Orbita selezione', 'Órbita da seleção', 'Орбита выделения', '選択オービット', '选择环绕'),
    'orbit_modifier': ('Orbit modifier', 'Modyfikator orbity', 'Orbit-Modifikator', 'Modificador de órbita', 'Modificateur d’orbite', 'Modificatore orbita', 'Modificador de órbita', 'Модификатор орбиты', 'オービット修飾キー', '环绕修饰键'),
    'orbit_mouse': ('Orbit mouse button', 'Przycisk myszy orbity', 'Orbit-Maustaste', 'Botón de órbita', 'Bouton d’orbite', 'Pulsante orbita', 'Botão de órbita', 'Кнопка орбиты', 'オービットマウスボタン', '环绕鼠标键'),
    'orbit_needs_selection': ('Select an object before using Orbit Around Selection', 'Zaznacz obiekt przed użyciem orbity', 'Select an object before using Orbit Around Selection', 'Select an object before using Orbit Around Selection', 'Select an object before using Orbit Around Selection', 'Select an object before using Orbit Around Selection', 'Select an object before using Orbit Around Selection', 'Select an object before using Orbit Around Selection', 'Select an object before using Orbit Around Selection', 'Select an object before using Orbit Around Selection'),
    'orbit_shortcut_label': ('Orbit selection', 'Orbita wokół zaznaczenia', 'Auswahl umkreisen', 'Orbitar selección', 'Orbite autour de la sélection', 'Orbita selezione', 'Órbita da seleção', 'Орбита вокруг выделения', '選択物を中心にオービット', '围绕选择环绕'),
    'precision_key': ('Precision key', 'Klawisz precyzji', 'Präzisionstaste', 'Tecla de precisión', 'Touche de précision', 'Tasto precisione', 'Tecla de precisão', 'Клавиша точности', '精密移動キー', '精细移动键'),
    'precision_multiplier': ('Precision multiplier', 'Mnożnik precyzji', 'Präzisions-Multiplikator', 'Multiplicador de precisión', 'Multiplicateur de précision', 'Moltiplicatore precisione', 'Multiplicador de precisão', 'Множитель точности', '精密移動倍率', '精细移动倍率'),
    'precision_role': ('{button}: precision movement ({multiplier}× speed)', '{button}: wolny ruch precyzyjny ({multiplier}× prędkości)', '{button}: präzise langsame Bewegung ({multiplier}× Tempo)', '{button}: movimiento de precisión ({multiplier}× velocidad)', '{button} : mouvement de précision ({multiplier}× vitesse)', '{button}: movimento preciso ({multiplier}× velocità)', '{button}: movimento de precisão ({multiplier}× velocidade)', '{button}: точное медленное движение ({multiplier}× скорость)', '{button}: 精密な低速移動（{multiplier}×）', '{button}：精细慢速移动（{multiplier}× 速度）'),
    'preferences_reset': ('Add-on settings restored to defaults', 'Przywrócono domyślne ustawienia dodatku', 'Add-on settings restored to defaults', 'Add-on settings restored to defaults', 'Add-on settings restored to defaults', 'Add-on settings restored to defaults', 'Add-on settings restored to defaults', 'Add-on settings restored to defaults', 'Add-on settings restored to defaults', 'Add-on settings restored to defaults'),
    'preferences_save_failed': ('Could not save Blender preferences: {error}', 'Nie udało się zapisać ustawień Blendera: {error}', 'Could not save Blender preferences: {error}', 'Could not save Blender preferences: {error}', 'Could not save Blender preferences: {error}', 'Could not save Blender preferences: {error}', 'Could not save Blender preferences: {error}', 'Could not save Blender preferences: {error}', 'Could not save Blender preferences: {error}', 'Could not save Blender preferences: {error}'),
    'preferences_saved': ('Blender preferences saved', 'Ustawienia Blendera zostały zapisane', 'Blender preferences saved', 'Blender preferences saved', 'Blender preferences saved', 'Blender preferences saved', 'Blender preferences saved', 'Blender preferences saved', 'Blender preferences saved', 'Blender preferences saved'),
    'preset_camera': ('Camera / orbit', 'Kamera / orbita', 'Kamera / Orbit', 'Cámara / órbita', 'Caméra / orbite', 'Camera / orbita', 'Câmera / órbita', 'Камера / орбита', 'カメラ / オービット', '相机 / 环绕'),
    'preset_motion': ('Motion', 'Ruch', 'Bewegung', 'Movimiento', 'Mouvement', 'Movimento', 'Movimento', 'Движение', 'モーション', '运动'),
    'preset_shortcuts': ('Shortcuts', 'Skróty', 'Tasten', 'Atajos', 'Raccourcis', 'Scorciatoie', 'Atalhos', 'Клавиши', 'ショートカット', '快捷键'),
    'project_page': ('Open project page', 'Otwórz stronę projektu', 'Projektseite öffnen', 'Abrir página del proyecto', 'Ouvrir la page du projet', 'Apri pagina progetto', 'Abrir página do projeto', 'Открыть страницу проекта', 'プロジェクトページを開く', '打开项目页面'),
    'protect_camera_orbit': ('Protect the active camera frame', 'Chroń kadr aktywnej kamery', 'Aktiven Kamerarahmen schützen', 'Proteger el encuadre de cámara', 'Protéger le cadrage de la caméra', 'Proteggi inquadratura camera', 'Proteger enquadramento da câmera', 'Защищать кадр камеры', 'アクティブカメラの構図を保護', '保护活动相机构图'),
    'quick_setup': ('Quick setup', 'Szybka konfiguracja', 'Schnelle Einrichtung', 'Configuración rápida', 'Configuration rapide', 'Configurazione rapida', 'Configuração rápida', 'Быстрая настройка', 'クイック設定', '快速设置'),
    'report_issue': ('Report an issue', 'Zgłoś błąd', 'Problem melden', 'Informar de un problema', 'Signaler un problème', 'Segnala un problema', 'Relatar problema', 'Сообщить о проблеме', '問題を報告', '报告问题'),
    'reset_preferences': ('Reset to Defaults', 'Przywróć domyślne', 'Standardwerte', 'Restablecer', 'Réinitialiser', 'Ripristina', 'Restaurar', 'Сбросить', '初期値に戻す', '恢复默认'),
    'restore_cursor': ('Restore cursor position on release', 'Przywróć pozycję kursora po puszczeniu', 'Cursorposition beim Loslassen wiederherstellen', 'Restaurar posición del cursor', 'Restaurer la position du curseur', 'Ripristina posizione cursore', 'Restaurar posição do cursor', 'Восстанавливать позицию курсора', '終了時にカーソル位置を復元', '松开后恢复光标位置'),
    'right_key': ('Right', 'W prawo', 'Rechts', 'Derecha', 'Droite', 'Destra', 'Direita', 'Вправо', '右', '右移'),
    'rmb_hold_duration': ('Hold delay', 'Opóźnienie przytrzymania', 'Halteverzögerung', 'Retardo de pulsación', 'Délai de maintien', 'Ritardo pressione', 'Atraso ao segurar', 'Задержка удержания', '長押し遅延', '按住延迟'),
    'save_preferences': ('Save on Disk', 'Zapisz na dysku', 'Speichern', 'Guardar', 'Enregistrer', 'Salva', 'Salvar', 'Сохранить', '保存', '保存'),
    'show_crosshair': ('Show crosshair', 'Pokaż celownik', 'Fadenkreuz anzeigen', 'Mostrar mira', 'Afficher le réticule', 'Mostra mirino', 'Mostrar mira', 'Показывать прицел', '照準を表示', '显示准星'),
    'show_header_speed': ('Show speed in viewport header', 'Pokazuj prędkość w nagłówku', 'Geschwindigkeit im Viewport-Kopf anzeigen', 'Mostrar velocidad en cabecera', 'Afficher la vitesse dans l’en-tête', 'Mostra velocità nell’intestazione', 'Mostrar velocidade no cabeçalho', 'Показывать скорость в заголовке', 'ヘッダーに速度を表示', '在标题栏显示速度'),
    'show_header_tutorial': ('Show controls in viewport header', 'Pokazuj sterowanie w nagłówku', 'Steuerung im Viewport-Kopf anzeigen', 'Mostrar controles en cabecera', 'Afficher les commandes dans l’en-tête', 'Mostra controlli nell’intestazione', 'Mostrar controles no cabeçalho', 'Показывать управление в заголовке', 'ヘッダーに操作を表示', '在标题栏显示控制提示'),
    'show_navigation_hud': ('Show compact navigation HUD', 'Pokaż kompaktowy HUD nawigacji', 'Kompaktes Navigations-HUD anzeigen', 'Mostrar HUD compacto', 'Afficher le HUD compact', 'Mostra HUD compatto', 'Mostrar HUD compacto', 'Показывать компактный HUD', 'コンパクトHUDを表示', '显示紧凑 HUD'),
    'smooth_motion': ('Smooth acceleration and braking', 'Płynne przyspieszanie i hamowanie', 'Sanftes Beschleunigen und Bremsen', 'Aceleración y frenado suaves', 'Accélération et freinage fluides', 'Accelerazione e frenata fluide', 'Aceleração e frenagem suaves', 'Плавный разгон и торможение', '滑らかな加速と減速', '平滑加速和刹车'),
    'speed_down_key': ('Decrease speed', 'Zmniejsz prędkość', 'Geschwindigkeit verringern', 'Reducir velocidad', 'Réduire la vitesse', 'Riduci velocità', 'Diminuir velocidade', 'Уменьшить скорость', '速度を下げる', '降低速度'),
    'speed_unit': ('Speed unit', 'Jednostka prędkości', 'Geschwindigkeitseinheit', 'Unidad de velocidad', 'Unité de vitesse', 'Unità di velocità', 'Unidade de velocidade', 'Единица скорости', '速度単位', '速度单位'),
    'speed_up_key': ('Increase speed', 'Zwiększ prędkość', 'Geschwindigkeit erhöhen', 'Aumentar velocidad', 'Augmenter la vitesse', 'Aumenta velocità', 'Aumentar velocidade', 'Увеличить скорость', '速度を上げる', '提高速度'),
    'sprint_key': ('Sprint key', 'Klawisz sprintu', 'Sprinttaste', 'Tecla de sprint', 'Touche de sprint', 'Tasto sprint', 'Tecla de sprint', 'Клавиша ускорения', 'スプリントキー', '加速键'),
    'sprint_multiplier': ('Sprint multiplier', 'Mnożnik sprintu', 'Sprint-Multiplikator', 'Multiplicador de sprint', 'Multiplicateur de sprint', 'Moltiplicatore sprint', 'Multiplicador de sprint', 'Множитель ускорения', 'スプリント倍率', '加速倍率'),
    'sprint_role': ('{button}: sprint while navigating ({multiplier}× speed)', '{button}: sprint podczas nawigacji ({multiplier}× prędkości)', '{button}: Sprint während der Navigation ({multiplier}× Tempo)', '{button}: sprint al navegar ({multiplier}× velocidad)', '{button} : sprint pendant la navigation ({multiplier}× vitesse)', '{button}: scatto durante la navigazione ({multiplier}× velocità)', '{button}: correr durante a navegação ({multiplier}× velocidade)', '{button}: ускорение при навигации ({multiplier}× скорость)', '{button}: ナビゲーション中の高速移動（{multiplier}×）', '{button}：导航时加速（{multiplier}× 速度）'),
    'stopped': ('Navigation stopped: {error}', 'Nawigacja zatrzymana: {error}', 'Navigation stopped: {error}', 'Navigation stopped: {error}', 'Navigation stopped: {error}', 'Navigation stopped: {error}', 'Navigation stopped: {error}', 'Navigation stopped: {error}', 'Navigation stopped: {error}', 'Navigation stopped: {error}'),
    'ui_expand_camera': ('ui_expand_camera', 'ui_expand_camera', 'ui_expand_camera', 'ui_expand_camera', 'ui_expand_camera', 'ui_expand_camera', 'ui_expand_camera', 'ui_expand_camera', 'ui_expand_camera', 'ui_expand_camera'),
    'ui_expand_controls': ('ui_expand_controls', 'ui_expand_controls', 'ui_expand_controls', 'ui_expand_controls', 'ui_expand_controls', 'ui_expand_controls', 'ui_expand_controls', 'ui_expand_controls', 'ui_expand_controls', 'ui_expand_controls'),
    'ui_expand_keybindings': ('ui_expand_keybindings', 'ui_expand_keybindings', 'ui_expand_keybindings', 'ui_expand_keybindings', 'ui_expand_keybindings', 'ui_expand_keybindings', 'ui_expand_keybindings', 'ui_expand_keybindings', 'ui_expand_keybindings', 'ui_expand_keybindings'),
    'ui_expand_diagnostics': ('ui_expand_diagnostics', 'ui_expand_diagnostics', 'ui_expand_diagnostics', 'ui_expand_diagnostics', 'ui_expand_diagnostics', 'ui_expand_diagnostics', 'ui_expand_diagnostics', 'ui_expand_diagnostics', 'ui_expand_diagnostics', 'ui_expand_diagnostics'),
    'ui_expand_display': ('ui_expand_display', 'ui_expand_display', 'ui_expand_display', 'ui_expand_display', 'ui_expand_display', 'ui_expand_display', 'ui_expand_display', 'ui_expand_display', 'ui_expand_display', 'ui_expand_display'),
    'ui_expand_motion': ('ui_expand_motion', 'ui_expand_motion', 'ui_expand_motion', 'ui_expand_motion', 'ui_expand_motion', 'ui_expand_motion', 'ui_expand_motion', 'ui_expand_motion', 'ui_expand_motion', 'ui_expand_motion'),
    'up_key': ('Up', 'W górę', 'Hoch', 'Arriba', 'Haut', 'Su', 'Cima', 'Вверх', '上', '上移'),
    'update_rate': ('Update rate', 'Częstotliwość odświeżania', 'Aktualisierungsrate', 'Frecuencia de actualización', 'Fréquence de mise à jour', 'Frequenza aggiornamento', 'Taxa de atualização', 'Частота обновления', '更新レート', '更新频率'),
    'update_rate_simple': ('60–120 Hz is recommended. Higher values only update motion more often.', 'Zalecane jest 60–120 Hz. Wyższa wartość tylko częściej aktualizuje ruch.', '60–120 Hz werden empfohlen. Höhere Werte aktualisieren die Bewegung nur häufiger.', 'Se recomiendan 60–120 Hz. Valores mayores solo actualizan el movimiento más a menudo.', '60–120 Hz sont recommandés. Une valeur supérieure met seulement le mouvement à jour plus souvent.', 'Sono consigliati 60–120 Hz. Valori maggiori aggiornano solo il movimento più spesso.', 'Recomenda-se 60–120 Hz. Valores maiores apenas atualizam o movimento com mais frequência.', 'Рекомендуется 60–120 Гц. Более высокое значение лишь чаще обновляет движение.', '60〜120 Hz を推奨します。高い値は移動の更新回数を増やすだけです。', '建议使用 60–120 Hz。更高的值只会更频繁地更新移动。'),
    'version': ('Version 1.5.5 — Matsm Studio', 'Wersja 1.5.5 — Matsm Studio', 'Version 1.5.5 — Matsm Studio', 'Versión 1.5.5 — Matsm Studio', 'Version 1.5.5 — Matsm Studio', 'Versione 1.5.5 — Matsm Studio', 'Versão 1.5.5 — Matsm Studio', 'Версия 1.5.5 — Matsm Studio', 'バージョン 1.5.5 — Matsm Studio', '版本 1.5.5 — Matsm Studio'),
    'wheel_multiplier': ('Speed-step multiplier', 'Mnożnik skoku prędkości', 'Geschwindigkeitsschritt', 'Paso de velocidad', 'Pas de vitesse', 'Passo velocità', 'Passo de velocidade', 'Шаг скорости', '速度ステップ', '速度步进'),
}
_EXTRA_TRANSLATIONS = {
    "UK": {
        "acceleration_time":"Час до повної швидкості", "advanced_and_tools":"Додатково та інструменти", "advanced_help":"Рідше потрібні параметри, межі швидкості, перевірка конфліктів і сервісні інструменти.",
        "backward_key":"Назад", "base_speed":"Швидкість руху", "camera_help":"У Camera View працює та сама навігація. Орбіта обертає вид навколо вибраного об’єкта.", "camera_orbit":"Камера та орбіта", "camera_orbit_protection_note":"У Camera View захист потребує вибраної цілі. Esc відновлює початковий кадр камери.", "camera_view_navigation":"Керувати активною камерою в Camera View",
        "check_conflicts":"Перевірити конфлікти", "conflicts_found":"Можливих конфліктів: {count}", "conflicts_none":"Прямих конфліктів в активних розкладках Blender і додатків не знайдено.", "conflicts_not_checked":"Не перевірено після останньої зміни скорочень.",
        "control_presets":"Профіль програми / рушія", "preset_help":"Виберіть програму, навігацію якої хочете наслідувати. Профіль налаштовує клавіші, рух і орбіту; ручна зміна клавіші перемикає на Власний.", "current_controls":"Поточне керування", "navigation_behavior_help":"Тут змінюється відчуття миші й поведінка руху. Усі клавіші призначаються в розділі «Клавіші».",
        "key_bindings":"Клавіші", "key_bindings_help":"Усі скорочення змінюються лише тут. Ручна зміна будь-якої клавіші автоматично перемикає профіль на Власний.", "navigation_trigger":"Запуск навігації", "movement_bindings":"Клавіші руху", "modifier_bindings":"Швидкий і точний рух", "speed_bindings":"Зміна швидкості", "orbit_bindings":"Клавіші орбіти", "current_layout":"Активна схема", "uses_key":"Клавіша: {button}", "edit_orbit_in_keys":"Це скорочення змінюється в розділі «Клавіші».",
        "crosshair_color":"Колір прицілу", "crosshair_gap":"Проміжок у центрі", "crosshair_size":"Розмір прицілу", "crosshair_style":"Стиль прицілу", "crosshair_thickness":"Товщина лінії", "deceleration_time":"Час гальмування", "display":"Відображення", "display_help":"Лише візуальні підказки — вони не змінюють навігацію.", "down_key":"Вниз",
        "enable_rmb_click_hold":"Зберігати звичайний клік ПКМ", "error_prefs":"Не вдалося прочитати налаштування додатка", "error_region":"Запускайте навігацію над основною областю 3D Viewport", "force_perspective":"Переходити в перспективу при старті навігації", "forward_key":"Вперед", "hide_cursor":"Приховувати системний курсор під час навігації", "how_to_use":"Як користуватися", "navigation_section":"Навігація", "speed_section":"Швидкість", "sprint_short":"Спринт", "precision_short":"Точність",
        "info_position":"Положення інформації", "show_navigation_info":"Показувати інформацію навігації", "show_speed_info":"Показувати швидкість", "show_controls_info":"Показувати підказки керування", "split_info_note":"У розділеному режимі швидкість зверху, а підказки керування знизу.", "hud_opacity":"Прозорість HUD", "hud_scale":"Розмір тексту HUD", "instant_stop":"Зупинятися одразу після відпускання клавіш руху", "invert_y":"Інвертувати вісь Y", "language":"Мова інтерфейсу", "left_key":"Ліворуч", "look_sensitivity":"Чутливість миші", "maximum_speed":"Максимальна швидкість", "minimum_speed":"Мінімальна швидкість", "more_settings":"Більше параметрів доступно в налаштуваннях додатка.",
        "motion":"Рух", "motion_help":"Налаштуйте, як швидко рух розганяється. Для точного керування залиште миттєву зупинку увімкненою.", "motion_short_note":"Менший час = швидша реакція. Частота оновлення змінює лише частоту розрахунку руху.", "movement_mode":"Напрямок руху вперед/назад", "navigate_action":"Навігація", "navigate_during_tools":"Дозволяти навігацію під час сумісних інструментів", "navigation_keys":"Схема клавіш руху", "navigation_modifier":"Додаткова клавіша навігації", "navigation_mouse":"Кнопка миші для навігації", "navigation_preset":"Профіль програми / рушія", "no_preferences":"Налаштування додатка недоступні", "none":"Немає",
        "orbit_enable_short":"Орбіта навколо вибраного", "orbit_modifier":"Додаткова клавіша орбіти", "orbit_mouse":"Кнопка миші орбіти", "orbit_needs_selection":"Перед орбітою виберіть об’єкт", "orbit_shortcut_label":"Орбіта вибраного", "precision_key":"Клавіша точного руху", "precision_multiplier":"Множник точності", "precision_role":"{button}: точний рух ({multiplier}× швидкості)", "preferences_reset":"Налаштування додатка відновлено", "preferences_saved":"Налаштування Blender збережено", "preset_camera":"Камера / орбіта", "preset_motion":"Рух", "preset_shortcuts":"Скорочення", "project_page":"Відкрити сторінку проєкту", "protect_camera_orbit":"Захищати кадр активної камери", "quick_setup":"Швидке налаштування", "report_issue":"Повідомити про проблему", "reset_preferences":"Скинути всі налаштування", "restore_cursor":"Повернути курсор після завершення", "right_key":"Праворуч", "rmb_hold_duration":"Час утримання перед навігацією", "save_preferences":"Зберегти на диск", "show_crosshair":"Показувати приціл", "smooth_motion":"Плавний розгін і гальмування", "speed_down_key":"Зменшити швидкість", "speed_unit":"Одиниця швидкості", "speed_up_key":"Збільшити швидкість", "sprint_key":"Клавіша швидкого руху (спринт)", "sprint_multiplier":"Множник спринту", "sprint_role":"{button}: спринт під час навігації ({multiplier}× швидкості)", "up_key":"Вгору", "update_rate":"Частота оновлення руху", "version":"Версія 1.5.5 — Matsm Studio", "wheel_multiplier":"Зміна швидкості за крок коліщатка"
    },
    "CS": {
        "acceleration_time":"Čas do plné rychlosti", "advanced_and_tools":"Pokročilé a nástroje", "advanced_help":"Méně používané chování, limity rychlosti, kontrola konfliktů a servisní nástroje.", "backward_key":"Dozadu", "base_speed":"Rychlost pohybu", "camera_help":"V Camera View funguje stejná navigace. Orbit obíhá kolem vybraného objektu.", "camera_orbit":"Kamera a orbit", "camera_view_navigation":"Ovládat aktivní kameru v Camera View", "check_conflicts":"Zkontrolovat konflikty", "conflicts_found":"Možné konflikty: {count}", "conflicts_none":"V aktivních klávesových mapách Blenderu a doplňků nebyly nalezeny přímé konflikty.", "conflicts_not_checked":"Po poslední změně zkratek nebylo zkontrolováno.",
        "control_presets":"Profil programu / enginu", "preset_help":"Vyberte program, jehož navigaci chcete napodobit. Profil nastaví klávesy, pohyb i orbit; ruční změna klávesy přepne na Vlastní.", "current_controls":"Aktuální ovládání", "navigation_behavior_help":"Zde se mění pocit z myši a chování pohybu. Všechny klávesy se nastavují v sekci Klávesy.", "key_bindings":"Klávesy", "key_bindings_help":"Všechny zkratky se upravují pouze zde. Ruční změna libovolné klávesy automaticky přepne profil na Vlastní.", "navigation_trigger":"Spuštění navigace", "movement_bindings":"Klávesy pohybu", "modifier_bindings":"Rychlý a přesný pohyb", "speed_bindings":"Změna rychlosti", "orbit_bindings":"Zkratka orbitu", "current_layout":"Aktivní rozložení", "uses_key":"Používá: {button}", "edit_orbit_in_keys":"Tuto zkratku změňte v sekci Klávesy.",
        "crosshair_color":"Barva zaměřovače", "crosshair_gap":"Mezera uprostřed", "crosshair_size":"Velikost zaměřovače", "crosshair_style":"Styl zaměřovače", "crosshair_thickness":"Tloušťka čáry", "deceleration_time":"Doba brzdění", "display":"Zobrazení", "display_help":"Pouze vizuální pomůcky; nemění chování navigace.", "down_key":"Dolů", "enable_rmb_click_hold":"Zachovat běžné kliknutí pravým tlačítkem", "force_perspective":"Při spuštění navigace přepnout do perspektivy", "forward_key":"Dopředu", "hide_cursor":"Při navigaci skrýt systémový kurzor", "how_to_use":"Jak používat", "navigation_section":"Navigace", "speed_section":"Rychlost", "sprint_short":"Sprint", "precision_short":"Přesnost",
        "info_position":"Umístění informací", "show_navigation_info":"Zobrazit informace o navigaci", "show_speed_info":"Zobrazit rychlost", "show_controls_info":"Zobrazit nápovědu ovládání", "split_info_note":"Rozdělený režim ponechá rychlost nahoře a nápovědu ovládání dole.", "hud_opacity":"Průhlednost HUD", "hud_scale":"Velikost textu HUD", "instant_stop":"Po uvolnění kláves pohybu okamžitě zastavit", "invert_y":"Invertovat osu Y", "language":"Jazyk rozhraní", "left_key":"Doleva", "look_sensitivity":"Citlivost myši", "maximum_speed":"Maximální rychlost", "minimum_speed":"Minimální rychlost", "more_settings":"Další možnosti jsou v nastavení doplňku.", "motion":"Pohyb", "motion_help":"Nastavte, jak rychle pohyb zrychluje. Pro přesné ovládání nechte okamžité zastavení zapnuté.", "motion_short_note":"Nižší časy reagují rychleji. Frekvence aktualizace mění pouze vzorkování pohybu.", "movement_mode":"Směr pohybu vpřed/vzad", "navigate_action":"Navigovat", "navigate_during_tools":"Povolit navigaci při používání kompatibilních nástrojů", "navigation_keys":"Rozložení kláves pohybu", "navigation_modifier":"Volitelná klávesa navigace", "navigation_mouse":"Tlačítko myši pro navigaci", "navigation_preset":"Profil programu / enginu", "no_preferences":"Nastavení doplňku není dostupné", "none":"Žádné",
        "orbit_enable_short":"Orbit kolem výběru", "orbit_modifier":"Volitelná klávesa orbitu", "orbit_mouse":"Tlačítko myši orbitu", "orbit_needs_selection":"Před použitím orbitu vyberte objekt", "orbit_shortcut_label":"Orbit výběru", "precision_key":"Klávesa přesného pohybu", "precision_multiplier":"Násobek přesnosti", "precision_role":"{button}: přesný pohyb ({multiplier}× rychlosti)", "preferences_reset":"Nastavení doplňku obnoveno", "preferences_saved":"Nastavení Blenderu uloženo", "preset_camera":"Kamera / orbit", "preset_motion":"Pohyb", "preset_shortcuts":"Zkratky", "project_page":"Otevřít stránku projektu", "protect_camera_orbit":"Chránit záběr aktivní kamery", "quick_setup":"Rychlé nastavení", "report_issue":"Nahlásit problém", "reset_preferences":"Obnovit všechna nastavení", "restore_cursor":"Po ukončení obnovit pozici kurzoru", "right_key":"Doprava", "rmb_hold_duration":"Doba podržení před navigací", "save_preferences":"Uložit na disk", "show_crosshair":"Zobrazit zaměřovač", "smooth_motion":"Plynulé zrychlení a brzdění", "speed_down_key":"Snížit rychlost", "speed_unit":"Jednotka rychlosti", "speed_up_key":"Zvýšit rychlost", "sprint_key":"Klávesa rychlého pohybu (Sprint)", "sprint_multiplier":"Násobek sprintu", "sprint_role":"{button}: sprint při navigaci ({multiplier}× rychlosti)", "up_key":"Nahoru", "update_rate":"Frekvence aktualizace pohybu", "version":"Verze 1.5.5 — Matsm Studio", "wheel_multiplier":"Změna rychlosti na krok kolečka"
    },
    "NL": {
        "acceleration_time":"Tijd tot volle snelheid", "advanced_and_tools":"Geavanceerd en hulpmiddelen", "advanced_help":"Minder gebruikte opties, snelheidslimieten, conflictcontrole en onderhoudshulpmiddelen.", "backward_key":"Achteruit", "base_speed":"Bewegingssnelheid", "camera_help":"Camera View gebruikt dezelfde navigatie. Orbit draait rond het geselecteerde object.", "camera_orbit":"Camera en orbit", "camera_view_navigation":"Actieve camera besturen in Camera View", "check_conflicts":"Conflicten controleren", "conflicts_found":"Mogelijke conflicten: {count}", "conflicts_none":"Geen directe conflicten gevonden in actieve Blender- en add-on-keymaps.", "conflicts_not_checked":"Niet gecontroleerd na de laatste wijziging van sneltoetsen.",
        "control_presets":"Programma-/engineprofiel", "preset_help":"Kies het programma waarvan je de navigatie wilt nabootsen. Het profiel stelt toetsen, beweging en orbit in; een handmatige toetswijziging schakelt naar Aangepast.", "current_controls":"Huidige bediening", "navigation_behavior_help":"Hier verander je het muisgevoel en bewegingsgedrag. Alle toetsen worden ingesteld in Toetsen.", "key_bindings":"Toetsen", "key_bindings_help":"Alle sneltoetsen worden alleen hier aangepast. Een handmatige wijziging schakelt het profiel automatisch naar Aangepast.", "navigation_trigger":"Navigatie starten", "movement_bindings":"Bewegingstoetsen", "modifier_bindings":"Snel en precies bewegen", "speed_bindings":"Snelheid aanpassen", "orbit_bindings":"Orbit-sneltoets", "current_layout":"Actieve indeling", "uses_key":"Gebruikt: {button}", "edit_orbit_in_keys":"Wijzig deze sneltoets in Toetsen.",
        "crosshair_color":"Kleur vizier", "crosshair_gap":"Opening in het midden", "crosshair_size":"Grootte vizier", "crosshair_style":"Stijl vizier", "crosshair_thickness":"Lijndikte", "deceleration_time":"Remtijd", "display":"Weergave", "display_help":"Alleen visuele hulpmiddelen; ze veranderen de navigatie niet.", "down_key":"Omlaag", "enable_rmb_click_hold":"Normale rechtermuisklik behouden", "force_perspective":"Bij start van navigatie naar perspectief schakelen", "forward_key":"Vooruit", "hide_cursor":"Systeemcursor verbergen tijdens navigatie", "how_to_use":"Gebruik", "navigation_section":"Navigatie", "speed_section":"Snelheid", "sprint_short":"Sprint", "precision_short":"Precisie",
        "info_position":"Positie van informatie", "show_navigation_info":"Navigatie-informatie tonen", "show_speed_info":"Snelheid tonen", "show_controls_info":"Bedieningstips tonen", "split_info_note":"Gesplitste modus houdt snelheid bovenaan en bedieningstips onderaan.", "hud_opacity":"HUD-dekking", "hud_scale":"HUD-tekstgrootte", "instant_stop":"Direct stoppen na loslaten van bewegingstoetsen", "invert_y":"Y-as omkeren", "language":"Interfacetaal", "left_key":"Links", "look_sensitivity":"Muisgevoeligheid", "maximum_speed":"Maximale snelheid", "minimum_speed":"Minimale snelheid", "more_settings":"Meer opties staan in de add-onvoorkeuren.", "motion":"Beweging", "motion_help":"Stel in hoe snel de beweging versnelt. Laat Direct stoppen aan voor nauwkeurige besturing.", "motion_short_note":"Lagere tijden reageren sneller. Updatefrequentie verandert alleen de bewegingssampling.", "movement_mode":"Richting vooruit/achteruit", "navigate_action":"Navigeren", "navigate_during_tools":"Navigatie toestaan tijdens compatibele tools", "navigation_keys":"Indeling bewegingstoetsen", "navigation_modifier":"Optionele navigatietoets", "navigation_mouse":"Muisknop voor navigatie", "navigation_preset":"Programma-/engineprofiel", "no_preferences":"Add-onvoorkeuren zijn niet beschikbaar", "none":"Geen",
        "orbit_enable_short":"Orbit rond selectie", "orbit_modifier":"Optionele orbittoets", "orbit_mouse":"Muisknop voor orbit", "orbit_needs_selection":"Selecteer een object voordat je Orbit rond selectie gebruikt", "orbit_shortcut_label":"Orbit selectie", "precision_key":"Toets voor precieze beweging", "precision_multiplier":"Precisiefactor", "precision_role":"{button}: precieze beweging ({multiplier}× snelheid)", "preferences_reset":"Add-oninstellingen hersteld", "preferences_saved":"Blender-voorkeuren opgeslagen", "preset_camera":"Camera / orbit", "preset_motion":"Beweging", "preset_shortcuts":"Sneltoetsen", "project_page":"Projectpagina openen", "protect_camera_orbit":"Actief camerakader beschermen", "quick_setup":"Snelle instelling", "report_issue":"Probleem melden", "reset_preferences":"Alle instellingen herstellen", "restore_cursor":"Cursorpositie herstellen bij loslaten", "right_key":"Rechts", "rmb_hold_duration":"Vasthoudtijd voor navigatie", "save_preferences":"Opslaan op schijf", "show_crosshair":"Vizier tonen", "smooth_motion":"Vloeiend versnellen en remmen", "speed_down_key":"Snelheid verlagen", "speed_unit":"Snelheidseenheid", "speed_up_key":"Snelheid verhogen", "sprint_key":"Toets voor snel bewegen (Sprint)", "sprint_multiplier":"Sprintfactor", "sprint_role":"{button}: sprint tijdens navigatie ({multiplier}× snelheid)", "up_key":"Omhoog", "update_rate":"Updatefrequentie beweging", "version":"Versie 1.5.5 — Matsm Studio", "wheel_multiplier":"Snelheidswijziging per wielstap"
    },
    "TR": {
        "acceleration_time":"Tam hıza ulaşma süresi", "advanced_and_tools":"Gelişmiş ve araçlar", "advanced_help":"Daha az kullanılan davranışlar, hız sınırları, çakışma kontrolü ve bakım araçları.", "backward_key":"Geri", "base_speed":"Hareket hızı", "camera_help":"Camera View aynı gezinmeyi kullanır. Yörünge seçili nesnenin etrafında döner.", "camera_orbit":"Kamera ve yörünge", "camera_view_navigation":"Camera View içinde etkin kamerayı kontrol et", "check_conflicts":"Çakışmaları kontrol et", "conflicts_found":"Olası çakışmalar: {count}", "conflicts_none":"Etkin Blender ve eklenti tuş haritalarında doğrudan çakışma bulunamadı.", "conflicts_not_checked":"Son kısayol değişikliğinden sonra kontrol edilmedi.",
        "control_presets":"Program / motor profili", "preset_help":"Gezinmesini taklit etmek istediğiniz programı seçin. Profil tuşları, hareketi ve yörüngeyi ayarlar; bir tuşu elle değiştirmek Özel profile geçirir.", "current_controls":"Geçerli kontroller", "navigation_behavior_help":"Burada fare hissi ve hareket davranışı değiştirilir. Tüm tuş atamaları Tuşlar bölümündedir.", "key_bindings":"Tuşlar", "key_bindings_help":"Tüm kısayollar yalnızca burada düzenlenir. Herhangi bir tuşu elle değiştirmek profili otomatik olarak Özel yapar.", "navigation_trigger":"Gezinmeyi başlat", "movement_bindings":"Hareket tuşları", "modifier_bindings":"Hızlı ve hassas hareket", "speed_bindings":"Hız ayarı", "orbit_bindings":"Yörünge kısayolu", "current_layout":"Etkin düzen", "uses_key":"Kullanır: {button}", "edit_orbit_in_keys":"Bu kısayolu Tuşlar bölümünde değiştirin.",
        "crosshair_color":"Nişangâh rengi", "crosshair_gap":"Merkez boşluğu", "crosshair_size":"Nişangâh boyutu", "crosshair_style":"Nişangâh stili", "crosshair_thickness":"Çizgi kalınlığı", "deceleration_time":"Frenleme süresi", "display":"Görünüm", "display_help":"Yalnızca görsel yardımcılar; gezinme davranışını değiştirmez.", "down_key":"Aşağı", "enable_rmb_click_hold":"Normal sağ tıklamayı koru", "force_perspective":"Gezinme başlayınca perspektife geç", "forward_key":"İleri", "hide_cursor":"Gezinirken sistem imlecini gizle", "how_to_use":"Nasıl kullanılır", "navigation_section":"Gezinme", "speed_section":"Hız", "sprint_short":"Sprint", "precision_short":"Hassas",
        "info_position":"Bilgi konumu", "show_navigation_info":"Gezinme bilgisini göster", "show_speed_info":"Hızı göster", "show_controls_info":"Kontrol ipuçlarını göster", "split_info_note":"Bölünmüş mod hızı üstte, kontrol ipuçlarını altta tutar.", "hud_opacity":"HUD saydamlığı", "hud_scale":"HUD metin boyutu", "instant_stop":"Hareket tuşları bırakılınca hemen dur", "invert_y":"Y eksenini ters çevir", "language":"Arayüz dili", "left_key":"Sol", "look_sensitivity":"Fare hassasiyeti", "maximum_speed":"Maksimum hız", "minimum_speed":"Minimum hız", "more_settings":"Daha fazla seçenek Eklenti Tercihleri'nde bulunur.", "motion":"Hareket", "motion_help":"Hareketin ne kadar hızlı ivmeleneceğini ayarlayın. Hassas kontrol için Anında Dur seçeneğini açık tutun.", "motion_short_note":"Daha düşük süreler daha hızlı tepki verir. Güncelleme hızı yalnızca hareket örneklemesini değiştirir.", "movement_mode":"İleri/geri hareket yönü", "navigate_action":"Gezin", "navigate_during_tools":"Uyumlu araçları kullanırken gezinmeye izin ver", "navigation_keys":"Hareket tuş düzeni", "navigation_modifier":"İsteğe bağlı gezinme tuşu", "navigation_mouse":"Gezinme fare düğmesi", "navigation_preset":"Program / motor profili", "no_preferences":"Eklenti tercihleri kullanılamıyor", "none":"Yok",
        "orbit_enable_short":"Seçim etrafında yörünge", "orbit_modifier":"İsteğe bağlı yörünge tuşu", "orbit_mouse":"Yörünge fare düğmesi", "orbit_needs_selection":"Yörüngeyi kullanmadan önce bir nesne seçin", "orbit_shortcut_label":"Seçim yörüngesi", "precision_key":"Hassas hareket tuşu", "precision_multiplier":"Hassasiyet çarpanı", "precision_role":"{button}: hassas hareket ({multiplier}× hız)", "preferences_reset":"Eklenti ayarları varsayılana döndürüldü", "preferences_saved":"Blender tercihleri kaydedildi", "preset_camera":"Kamera / yörünge", "preset_motion":"Hareket", "preset_shortcuts":"Kısayollar", "project_page":"Proje sayfasını aç", "protect_camera_orbit":"Etkin kamera karesini koru", "quick_setup":"Hızlı kurulum", "report_issue":"Sorun bildir", "reset_preferences":"Tüm ayarları sıfırla", "restore_cursor":"Bırakınca imleç konumunu geri yükle", "right_key":"Sağ", "rmb_hold_duration":"Gezinme başlamadan bekleme süresi", "save_preferences":"Diske kaydet", "show_crosshair":"Nişangâhı göster", "smooth_motion":"Yumuşak hızlanma ve frenleme", "speed_down_key":"Hızı azalt", "speed_unit":"Hız birimi", "speed_up_key":"Hızı artır", "sprint_key":"Hızlı hareket tuşu (Sprint)", "sprint_multiplier":"Sprint çarpanı", "sprint_role":"{button}: gezinirken sprint ({multiplier}× hız)", "up_key":"Yukarı", "update_rate":"Hareket güncelleme hızı", "version":"Sürüm 1.5.5 — Matsm Studio", "wheel_multiplier":"Tekerlek adımı başına hız değişimi"
    },
    "KO": {
        "acceleration_time":"최고 속도 도달 시간", "advanced_and_tools":"고급 및 도구", "advanced_help":"덜 자주 쓰는 동작, 속도 제한, 충돌 검사와 유지 관리 도구입니다.", "backward_key":"뒤로", "base_speed":"이동 속도", "camera_help":"Camera View에서도 같은 내비게이션을 사용합니다. 오빗은 선택한 오브젝트를 중심으로 회전합니다.", "camera_orbit":"카메라 및 오빗", "camera_view_navigation":"Camera View에서 활성 카메라 제어", "check_conflicts":"충돌 확인", "conflicts_found":"가능한 충돌: {count}", "conflicts_none":"활성 Blender 및 애드온 키맵에서 직접 충돌을 찾지 못했습니다.", "conflicts_not_checked":"마지막 단축키 변경 후 확인하지 않았습니다.",
        "control_presets":"프로그램 / 엔진 프로필", "preset_help":"내비게이션을 따라 할 프로그램을 선택하세요. 프로필은 키, 이동감과 오빗을 함께 설정하며 키를 직접 바꾸면 사용자 지정으로 전환됩니다.", "current_controls":"현재 조작", "navigation_behavior_help":"여기서는 마우스 감각과 이동 동작을 바꿉니다. 모든 키 지정은 키 설정 섹션에서 합니다.", "key_bindings":"키 설정", "key_bindings_help":"모든 단축키는 여기에서만 바꿉니다. 키를 직접 변경하면 프로필이 자동으로 사용자 지정으로 전환됩니다.", "navigation_trigger":"내비게이션 시작", "movement_bindings":"이동 키", "modifier_bindings":"빠른 / 정밀 이동", "speed_bindings":"속도 조절", "orbit_bindings":"오빗 단축키", "current_layout":"현재 배열", "uses_key":"사용 키: {button}", "edit_orbit_in_keys":"이 단축키는 키 설정에서 변경하세요.",
        "crosshair_color":"조준선 색상", "crosshair_gap":"중앙 간격", "crosshair_size":"조준선 크기", "crosshair_style":"조준선 스타일", "crosshair_thickness":"선 두께", "deceleration_time":"감속 시간", "display":"표시", "display_help":"시각적 도움말만 바꾸며 내비게이션 동작에는 영향을 주지 않습니다.", "down_key":"아래", "enable_rmb_click_hold":"짧은 우클릭 유지", "force_perspective":"내비게이션 시작 시 원근 보기로 전환", "forward_key":"앞으로", "hide_cursor":"내비게이션 중 시스템 커서 숨기기", "how_to_use":"사용 방법", "navigation_section":"내비게이션", "speed_section":"속도", "sprint_short":"스프린트", "precision_short":"정밀",
        "info_position":"정보 위치", "show_navigation_info":"내비게이션 정보 표시", "show_speed_info":"속도 표시", "show_controls_info":"조작 힌트 표시", "split_info_note":"분할 모드는 속도를 위에, 조작 힌트를 아래에 표시합니다.", "hud_opacity":"HUD 불투명도", "hud_scale":"HUD 글자 크기", "instant_stop":"이동 키를 놓으면 즉시 정지", "invert_y":"Y축 반전", "language":"인터페이스 언어", "left_key":"왼쪽", "look_sensitivity":"마우스 감도", "maximum_speed":"최대 속도", "minimum_speed":"최소 속도", "more_settings":"더 많은 옵션은 애드온 환경설정에서 사용할 수 있습니다.", "motion":"모션", "motion_help":"이동이 얼마나 빠르게 가속되는지 조절합니다. 정확한 조작에는 즉시 정지를 켜 두세요.", "motion_short_note":"시간이 짧을수록 빠르게 반응합니다. 업데이트 빈도는 모션 계산 빈도만 바꿉니다.", "movement_mode":"앞/뒤 이동 방향", "navigate_action":"내비게이션", "navigate_during_tools":"호환 도구 사용 중 내비게이션 허용", "navigation_keys":"이동 키 배열", "navigation_modifier":"선택 내비게이션 보조 키", "navigation_mouse":"내비게이션 마우스 버튼", "navigation_preset":"프로그램 / 엔진 프로필", "no_preferences":"애드온 환경설정을 사용할 수 없습니다", "none":"없음",
        "orbit_enable_short":"선택 항목 중심 오빗", "orbit_modifier":"선택 오빗 보조 키", "orbit_mouse":"오빗 마우스 버튼", "orbit_needs_selection":"오빗을 사용하기 전에 오브젝트를 선택하세요", "orbit_shortcut_label":"선택 오빗", "precision_key":"정밀 이동 키", "precision_multiplier":"정밀 이동 배율", "precision_role":"{button}: 정밀 이동 ({multiplier}× 속도)", "preferences_reset":"애드온 설정을 기본값으로 복원했습니다", "preferences_saved":"Blender 환경설정을 저장했습니다", "preset_camera":"카메라 / 오빗", "preset_motion":"모션", "preset_shortcuts":"단축키", "project_page":"프로젝트 페이지 열기", "protect_camera_orbit":"활성 카메라 프레임 보호", "quick_setup":"빠른 설정", "report_issue":"문제 신고", "reset_preferences":"모든 설정 초기화", "restore_cursor":"종료 시 커서 위치 복원", "right_key":"오른쪽", "rmb_hold_duration":"내비게이션 시작 전 누르기 시간", "save_preferences":"디스크에 저장", "show_crosshair":"조준선 표시", "smooth_motion":"부드러운 가속 및 감속", "speed_down_key":"속도 감소", "speed_unit":"속도 단위", "speed_up_key":"속도 증가", "sprint_key":"빠른 이동 키 (스프린트)", "sprint_multiplier":"스프린트 배율", "sprint_role":"{button}: 내비게이션 중 스프린트 ({multiplier}× 속도)", "up_key":"위", "update_rate":"모션 업데이트 빈도", "version":"버전 1.5.5 — Matsm Studio", "wheel_multiplier":"휠 한 단계당 속도 변경량"
    },
}

# Clearer names and short explanations for settings that were easy to misread.
_UI_OVERRIDES = {
    "EN": {
        "control_presets":"Program / engine profile", "navigation_preset":"Program / engine profile",
        "preset_help":"Choose the program whose navigation you want to mimic. The profile sets shortcuts, motion and orbit together. Editing a shortcut switches to Custom.",
        "navigation_mouse":"Navigation mouse button", "navigation_modifier":"Optional navigation key",
        "navigation_modifier_help":"None = the mouse button alone starts navigation. Shift/Ctrl/Alt = hold that key together with the navigation mouse button.",
        "navigation_keys":"Movement key layout", "movement_layout_help":"WASD and Arrow keys use ready layouts. Custom lets you assign every direction separately.",
        "sprint_key":"Fast movement key (Sprint)", "precision_key":"Slow movement key (Precision)",
        "orbit_modifier":"Optional orbit key", "orbit_mouse":"Orbit mouse button", "orbit_shortcut_help":"Default: Alt + RMB. Hold the shortcut and move the mouse to orbit around the selected object.",
        "enable_rmb_click_hold":"Keep normal RMB click on a quick press", "rmb_hold_duration":"Hold time before navigation starts",
        "navigate_during_tools":"Allow navigation while using compatible tools", "force_perspective":"Switch to perspective when navigation starts",
        "movement_mode":"Forward/back direction", "update_rate":"Motion update rate", "wheel_multiplier":"Speed change per wheel step",
        "reset_preferences":"Reset all add-on settings", "restore_default_keys":"Restore default keys", "default_keys_restored":"Default navigation keys restored",
        "always_actions_help":"These two actions are always available, even when the sections below are collapsed."
    },
    "PL": {
        "control_presets":"Preset programu / silnika", "navigation_preset":"Preset programu / silnika",
        "preset_help":"Wybierz program, którego sterowanie chcesz odwzorować. Preset ustawia skróty, ruch i orbitę razem. Ręczna zmiana skrótu przełącza na Własne.",
        "navigation_mouse":"Przycisk nawigacji (trzymaj)", "navigation_modifier":"Dodatkowy klawisz do nawigacji",
        "navigation_modifier_help":"Brak = wystarczy sam przycisk nawigacji. Shift/Ctrl/Alt = ten klawisz trzeba trzymać razem z przyciskiem nawigacji.",
        "navigation_keys":"Układ klawiszy ruchu", "movement_layout_help":"WASD i Strzałki to gotowe układy. Własne pozwala przypisać każdy kierunek osobno.",
        "sprint_key":"Klawisz szybkiego ruchu (Sprint)", "precision_key":"Klawisz wolnego ruchu (Precyzja)",
        "orbit_modifier":"Dodatkowy klawisz orbity", "orbit_mouse":"Przycisk myszy orbity", "orbit_shortcut_help":"Domyślnie: Alt + PPM. Przytrzymaj ten skrót i ruszaj myszą, aby orbitować wokół zaznaczonego obiektu.",
        "enable_rmb_click_hold":"Zachowaj zwykłe kliknięcie PPM przy krótkim kliknięciu", "rmb_hold_duration":"Czas przytrzymania przed startem nawigacji",
        "navigate_during_tools":"Pozwalaj na nawigację podczas używania zgodnych narzędzi", "force_perspective":"Przełącz na perspektywę po rozpoczęciu nawigacji",
        "movement_mode":"Kierunek ruchu przód/tył", "update_rate":"Częstotliwość aktualizacji ruchu", "wheel_multiplier":"Zmiana prędkości na jeden krok kółka",
        "reset_preferences":"Zresetuj wszystkie ustawienia dodatku", "restore_default_keys":"Przywróć domyślne klawisze", "default_keys_restored":"Przywrócono domyślne klawisze nawigacji",
        "always_actions_help":"Te dwa przyciski są zawsze widoczne, nawet gdy sekcje poniżej są zwinięte."
    },
}
_UI_OVERRIDES.update({
    "DE": {
        "navigation_mouse":"Navigationstaste der Maus", "navigation_modifier":"Optionale Navigationstaste", "navigation_modifier_help":"Keine = die Maustaste allein startet die Navigation. Shift/Strg/Alt = diese Taste zusammen mit der Navigationstaste halten.", "navigation_keys":"Bewegungstasten-Layout", "movement_layout_help":"WASD und Pfeiltasten sind fertige Layouts. Benutzerdefiniert erlaubt jede Richtung einzeln zuzuweisen.", "sprint_key":"Taste für schnelle Bewegung (Sprint)", "precision_key":"Taste für langsame Präzisionsbewegung", "orbit_modifier":"Optionale Orbit-Taste", "orbit_mouse":"Orbit-Maustaste", "orbit_shortcut_help":"Standard: Alt + rechte Maustaste. Diese Kombination halten und die Maus bewegen, um das ausgewählte Objekt zu umkreisen.", "restore_default_keys":"Standardtasten wiederherstellen", "default_keys_restored":"Standard-Navigationstasten wiederhergestellt"
    },
    "ES": {
        "navigation_mouse":"Botón del ratón para navegar", "navigation_modifier":"Tecla opcional de navegación", "navigation_modifier_help":"Ninguno = basta con el botón del ratón. Shift/Ctrl/Alt = mantén esa tecla junto con el botón de navegación.", "navigation_keys":"Distribución de teclas de movimiento", "movement_layout_help":"WASD y Flechas usan diseños preparados. Personalizado permite asignar cada dirección por separado.", "sprint_key":"Tecla de movimiento rápido (Sprint)", "precision_key":"Tecla de movimiento lento (Precisión)", "orbit_modifier":"Tecla opcional de órbita", "orbit_mouse":"Botón del ratón para órbita", "orbit_shortcut_help":"Predeterminado: Alt + botón derecho. Mantén este atajo y mueve el ratón para orbitar alrededor del objeto seleccionado.", "restore_default_keys":"Restaurar teclas predeterminadas", "default_keys_restored":"Teclas de navegación predeterminadas restauradas"
    },
    "FR": {
        "navigation_mouse":"Bouton souris de navigation", "navigation_modifier":"Touche de navigation optionnelle", "navigation_modifier_help":"Aucun = le bouton souris suffit. Maj/Ctrl/Alt = maintenez cette touche avec le bouton de navigation.", "navigation_keys":"Disposition des touches de déplacement", "movement_layout_help":"WASD et Flèches utilisent des dispositions prêtes. Personnalisé permet d’assigner chaque direction séparément.", "sprint_key":"Touche de déplacement rapide (Sprint)", "precision_key":"Touche de déplacement lent (Précision)", "orbit_modifier":"Touche d’orbite optionnelle", "orbit_mouse":"Bouton souris d’orbite", "orbit_shortcut_help":"Par défaut : Alt + clic droit. Maintenez ce raccourci et déplacez la souris pour tourner autour de l’objet sélectionné.", "restore_default_keys":"Restaurer les touches par défaut", "default_keys_restored":"Touches de navigation par défaut restaurées"
    },
    "IT": {
        "navigation_mouse":"Pulsante mouse per navigare", "navigation_modifier":"Tasto di navigazione opzionale", "navigation_modifier_help":"Nessuno = basta il pulsante del mouse. Shift/Ctrl/Alt = tieni premuto quel tasto insieme al pulsante di navigazione.", "navigation_keys":"Schema tasti di movimento", "movement_layout_help":"WASD e Frecce usano schemi pronti. Personalizzato permette di assegnare ogni direzione separatamente.", "sprint_key":"Tasto movimento veloce (Sprint)", "precision_key":"Tasto movimento lento (Precisione)", "orbit_modifier":"Tasto orbita opzionale", "orbit_mouse":"Pulsante mouse orbita", "orbit_shortcut_help":"Predefinito: Alt + tasto destro. Tieni premuta questa scorciatoia e muovi il mouse per orbitare attorno all’oggetto selezionato.", "restore_default_keys":"Ripristina tasti predefiniti", "default_keys_restored":"Tasti di navigazione predefiniti ripristinati"
    },
    "PT_BR": {
        "navigation_mouse":"Botão do mouse para navegar", "navigation_modifier":"Tecla opcional de navegação", "navigation_modifier_help":"Nenhum = só o botão do mouse inicia a navegação. Shift/Ctrl/Alt = segure essa tecla junto com o botão de navegação.", "navigation_keys":"Layout das teclas de movimento", "movement_layout_help":"WASD e Setas usam layouts prontos. Personalizado permite definir cada direção separadamente.", "sprint_key":"Tecla de movimento rápido (Sprint)", "precision_key":"Tecla de movimento lento (Precisão)", "orbit_modifier":"Tecla opcional de órbita", "orbit_mouse":"Botão do mouse para órbita", "orbit_shortcut_help":"Padrão: Alt + botão direito. Segure este atalho e mova o mouse para orbitar ao redor do objeto selecionado.", "restore_default_keys":"Restaurar teclas padrão", "default_keys_restored":"Teclas padrão de navegação restauradas"
    },
    "RU": {
        "navigation_mouse":"Кнопка мыши для навигации", "navigation_modifier":"Дополнительная клавиша навигации", "navigation_modifier_help":"Нет = достаточно кнопки мыши. Shift/Ctrl/Alt = удерживайте эту клавишу вместе с кнопкой навигации.", "navigation_keys":"Схема клавиш движения", "movement_layout_help":"WASD и стрелки — готовые схемы. Свои позволяют назначить каждое направление отдельно.", "sprint_key":"Клавиша быстрого движения (Спринт)", "precision_key":"Клавиша медленного точного движения", "orbit_modifier":"Дополнительная клавиша орбиты", "orbit_mouse":"Кнопка мыши для орбиты", "orbit_shortcut_help":"По умолчанию: Alt + ПКМ. Удерживайте это сочетание и двигайте мышь, чтобы вращаться вокруг выбранного объекта.", "restore_default_keys":"Вернуть стандартные клавиши", "default_keys_restored":"Стандартные клавиши навигации восстановлены"
    },
    "JA": {
        "navigation_mouse":"ナビゲーション用マウスボタン", "navigation_modifier":"追加ナビゲーションキー", "navigation_modifier_help":"なし = マウスボタンだけで開始します。Shift/Ctrl/Alt = ナビゲーションボタンと一緒に押します。", "navigation_keys":"移動キー配列", "movement_layout_help":"WASD と矢印キーは既定の配列です。カスタムでは各方向を個別に割り当てられます。", "sprint_key":"高速移動キー（スプリント）", "precision_key":"低速精密移動キー", "orbit_modifier":"追加オービットキー", "orbit_mouse":"オービット用マウスボタン", "orbit_shortcut_help":"既定: Alt + 右クリック。このショートカットを押しながらマウスを動かすと、選択オブジェクトを中心に回転します。", "restore_default_keys":"既定キーに戻す", "default_keys_restored":"既定のナビゲーションキーを復元しました"
    },
    "ZH_CN": {
        "navigation_mouse":"导航鼠标按钮", "navigation_modifier":"可选导航按键", "navigation_modifier_help":"无 = 只按鼠标按钮即可开始导航。Shift/Ctrl/Alt = 需要与导航鼠标按钮一起按住。", "navigation_keys":"移动按键布局", "movement_layout_help":"WASD 和方向键使用预设布局。自定义可分别设置每个方向。", "sprint_key":"快速移动键（冲刺）", "precision_key":"慢速精确移动键", "orbit_modifier":"可选环绕按键", "orbit_mouse":"环绕鼠标按钮", "orbit_shortcut_help":"默认：Alt + 鼠标右键。按住此快捷键并移动鼠标，即可围绕选中的对象旋转。", "restore_default_keys":"恢复默认按键", "default_keys_restored":"已恢复默认导航按键"
    },
    "UK": {
        "navigation_modifier_help":"Немає = достатньо самої кнопки миші. Shift/Ctrl/Alt = утримуйте цю клавішу разом із кнопкою навігації.", "movement_layout_help":"WASD і стрілки — готові схеми. Власний режим дозволяє призначити кожен напрямок окремо.", "orbit_shortcut_help":"За замовчуванням: Alt + ПКМ. Утримуйте це скорочення й рухайте мишу, щоб обертатися навколо вибраного об’єкта.", "restore_default_keys":"Відновити стандартні клавіші", "default_keys_restored":"Стандартні клавіші навігації відновлено"
    },
    "CS": {
        "navigation_modifier_help":"Žádné = stačí samotné tlačítko myši. Shift/Ctrl/Alt = držte tuto klávesu společně s tlačítkem navigace.", "movement_layout_help":"WASD a Šipky jsou hotová rozložení. Vlastní umožní přiřadit každý směr zvlášť.", "orbit_shortcut_help":"Výchozí: Alt + pravé tlačítko myši. Držte tuto zkratku a pohybujte myší pro obíhání kolem vybraného objektu.", "restore_default_keys":"Obnovit výchozí klávesy", "default_keys_restored":"Výchozí navigační klávesy obnoveny"
    },
    "NL": {
        "navigation_modifier_help":"Geen = alleen de muisknop start navigatie. Shift/Ctrl/Alt = houd die toets samen met de navigatiemuisknop ingedrukt.", "movement_layout_help":"WASD en Pijltjes zijn kant-en-klare indelingen. Aangepast laat elke richting afzonderlijk instellen.", "orbit_shortcut_help":"Standaard: Alt + rechtermuisknop. Houd deze sneltoets ingedrukt en beweeg de muis om rond het geselecteerde object te draaien.", "restore_default_keys":"Standaardtoetsen herstellen", "default_keys_restored":"Standaard navigatietoetsen hersteld"
    },
    "TR": {
        "navigation_modifier_help":"Yok = yalnızca fare düğmesi gezinmeyi başlatır. Shift/Ctrl/Alt = bu tuşu gezinme fare düğmesiyle birlikte basılı tutun.", "movement_layout_help":"WASD ve Yön tuşları hazır düzenlerdir. Özel modda her yönü ayrı atayabilirsiniz.", "orbit_shortcut_help":"Varsayılan: Alt + sağ fare düğmesi. Bu kısayolu basılı tutup fareyi hareket ettirerek seçili nesnenin etrafında dönün.", "restore_default_keys":"Varsayılan tuşları geri yükle", "default_keys_restored":"Varsayılan gezinme tuşları geri yüklendi"
    },
    "KO": {
        "navigation_modifier_help":"없음 = 마우스 버튼만으로 내비게이션을 시작합니다. Shift/Ctrl/Alt = 내비게이션 마우스 버튼과 함께 누릅니다.", "movement_layout_help":"WASD와 방향키는 준비된 배열입니다. 사용자 지정에서는 각 방향을 따로 지정할 수 있습니다.", "orbit_shortcut_help":"기본값: Alt + 마우스 오른쪽 버튼. 이 단축키를 누른 채 마우스를 움직이면 선택한 오브젝트 주위를 오빗합니다.", "restore_default_keys":"기본 키 복원", "default_keys_restored":"기본 내비게이션 키를 복원했습니다"
    },
})

_EN = {key: values[0] for key, values in _TR_ROWS.items()}
_EN.update(_UI_OVERRIDES["EN"])
_TEXT = {
    code: {key: values[index] for key, values in _TR_ROWS.items()}
    for index, code in enumerate(_BASE_LANG_CODES)
}
for _code in _BASE_LANG_CODES:
    _TEXT[_code].update(_UI_OVERRIDES.get(_code, {}))
for _code in ('UK', 'CS', 'NL', 'TR', 'KO'):
    _TEXT[_code] = dict(_EN)
    _TEXT[_code].update(_EXTRA_TRANSLATIONS[_code])
    _TEXT[_code].update(_UI_OVERRIDES.get(_code, {}))

_KEYBOARD_KEY_ITEMS = (
    ("A", "A", "A"), ("B", "B", "B"), ("C", "C", "C"), ("D", "D", "D"), ("E", "E", "E"), ("F", "F", "F"), ("G", "G", "G"), ("H", "H", "H"), ("I", "I", "I"), ("J", "J", "J"), ("K", "K", "K"), ("L", "L", "L"), ("M", "M", "M"), ("N", "N", "N"), ("O", "O", "O"), ("P", "P", "P"), ("Q", "Q", "Q"), ("R", "R", "R"), ("S", "S", "S"), ("T", "T", "T"), ("U", "U", "U"), ("V", "V", "V"), ("W", "W", "W"), ("X", "X", "X"), ("Y", "Y", "Y"), ("Z", "Z", "Z"),
    ("0", "0", "0"), ("1", "1", "1"), ("2", "2", "2"), ("3", "3", "3"), ("4", "4", "4"), ("5", "5", "5"), ("6", "6", "6"), ("7", "7", "7"), ("8", "8", "8"), ("9", "9", "9"),
    ("SPACE", "Space", "Space bar"), ("TAB", "Tab", "Tab"),
    ("UP_ARROW", "↑", "Up Arrow"), ("DOWN_ARROW", "↓", "Down Arrow"),
    ("LEFT_ARROW", "←", "Left Arrow"), ("RIGHT_ARROW", "→", "Right Arrow"),
    ("PAGE_UP", "Page Up", "Page Up"), ("PAGE_DOWN", "Page Down", "Page Down"),
    ("HOME", "Home", "Home"), ("END", "End", "End"),
    ("NUMPAD_8", "Numpad 8", "Numpad 8"), ("NUMPAD_2", "Numpad 2", "Numpad 2"),
    ("NUMPAD_4", "Numpad 4", "Numpad 4"), ("NUMPAD_6", "Numpad 6", "Numpad 6"),
    ("NUMPAD_9", "Numpad 9", "Numpad 9"), ("NUMPAD_7", "Numpad 7", "Numpad 7"),
    ("NUMPAD_5", "Numpad 5", "Numpad 5"), ("NUMPAD_1", "Numpad 1", "Numpad 1"),
    ("NUMPAD_3", "Numpad 3", "Numpad 3"),
)

_HOLD_KEY_ITEMS = (
    ("NONE", "None", "Disabled"), ("SHIFT", "Shift", "Either Shift key"),
    ("CTRL", "Ctrl", "Either Ctrl key"), ("ALT", "Alt", "Either Alt key"),
) + _KEYBOARD_KEY_ITEMS

_SPEED_KEY_ITEMS = (
    ("WHEELUPMOUSE", "Wheel Up", "Mouse wheel up"),
    ("WHEELDOWNMOUSE", "Wheel Down", "Mouse wheel down"),
    ("EQUAL", "+ / =", "Plus or equals key"),
    ("MINUS", "-", "Minus key"),
    ("NUMPAD_PLUS", "Numpad +", "Numpad plus"),
    ("NUMPAD_MINUS", "Numpad -", "Numpad minus"),
) + _KEYBOARD_KEY_ITEMS


_ENUM_PROPERTY_ITEMS = {
    "ui_language": _LANGUAGE_ITEMS,
    "navigation_preset": _NAVIGATION_PRESET_ITEMS,
    "navigation_mouse": _MOUSE_BUTTON_ITEMS,
    "navigation_modifier": _MODIFIER_ITEMS,
    "navigation_keys": _NAVIGATION_KEYS_ITEMS,
    "move_forward_key": _KEYBOARD_KEY_ITEMS,
    "move_backward_key": _KEYBOARD_KEY_ITEMS,
    "move_left_key": _KEYBOARD_KEY_ITEMS,
    "move_right_key": _KEYBOARD_KEY_ITEMS,
    "move_up_key": _KEYBOARD_KEY_ITEMS,
    "move_down_key": _KEYBOARD_KEY_ITEMS,
    "sprint_key": _HOLD_KEY_ITEMS,
    "precision_key": _HOLD_KEY_ITEMS,
    "speed_up_key": _SPEED_KEY_ITEMS,
    "speed_down_key": _SPEED_KEY_ITEMS,
    "speed_unit": _SPEED_UNIT_ITEMS,
    "movement_mode": _MOVEMENT_MODE_ITEMS,
    "orbit_mouse": _MOUSE_BUTTON_ITEMS,
    "orbit_modifier": _MODIFIER_ITEMS,
    "crosshair_style": _CROSSHAIR_STYLE_ITEMS,
    "info_position": _HUD_POSITION_ITEMS,
}

_ENUM_LABELS = {
    "EN": {
        "NONE":"None", "CUSTOM":"Custom", "ARROWS":"Arrow keys", "BOTH":"WASD + Arrow keys",
        "FREE":"Free flight", "LEVEL":"Level",
        "CROSS":"Cross", "CROSS_DOT":"Cross + dot", "DOT":"Dot", "CIRCLE":"Circle", "FILLED_CIRCLE":"Filled circle",
        "RIGHTMOUSE":"Right Mouse Button", "MIDDLEMOUSE":"Middle Mouse Button", "LEFTMOUSE":"Left Mouse Button",
        "BOTTOM_LEFT":"Bottom left", "BOTTOM_RIGHT":"Bottom right", "TOP_LEFT":"Top left", "TOP_RIGHT":"Top right",
        "WHEELUPMOUSE":"Wheel Up", "WHEELDOWNMOUSE":"Wheel Down", "SPACE":"Space", "PAGE_UP":"Page Up", "PAGE_DOWN":"Page Down",
        "NUMPAD_PLUS":"Numpad +", "NUMPAD_MINUS":"Numpad -",
    },
    "PL": {
        "NONE":"Brak", "CUSTOM":"Własne", "ARROWS":"Strzałki", "BOTH":"WASD + strzałki",
        "FREE":"Swobodny lot", "LEVEL":"Poziomo",
        "CROSS":"Krzyżyk", "CROSS_DOT":"Krzyżyk + kropka", "DOT":"Kropka", "CIRCLE":"Okrąg", "FILLED_CIRCLE":"Wypełnione kółko",
        "RIGHTMOUSE":"Prawy przycisk myszy", "MIDDLEMOUSE":"Środkowy przycisk myszy", "LEFTMOUSE":"Lewy przycisk myszy",
        "BOTTOM_LEFT":"Dół po lewej", "BOTTOM_RIGHT":"Dół po prawej", "TOP_LEFT":"Góra po lewej", "TOP_RIGHT":"Góra po prawej",
        "WHEELUPMOUSE":"Kółko w górę", "WHEELDOWNMOUSE":"Kółko w dół", "SPACE":"Spacja", "PAGE_UP":"Page Up", "PAGE_DOWN":"Page Down",
        "NUMPAD_PLUS":"Numpad +", "NUMPAD_MINUS":"Numpad -",
    },
    "DE": {"NONE":"Keine","CUSTOM":"Benutzerdefiniert","ARROWS":"Pfeiltasten","BOTH":"WASD + Pfeiltasten","FREE":"Freier Flug","LEVEL":"Horizontal","CROSS":"Kreuz","CROSS_DOT":"Kreuz + Punkt","DOT":"Punkt","CIRCLE":"Kreis","FILLED_CIRCLE":"Gefüllter Kreis","RIGHTMOUSE":"Rechte Maustaste","MIDDLEMOUSE":"Mittlere Maustaste","LEFTMOUSE":"Linke Maustaste","BOTTOM_LEFT":"Unten links","BOTTOM_RIGHT":"Unten rechts","TOP_LEFT":"Oben links","TOP_RIGHT":"Oben rechts","WHEELUPMOUSE":"Mausrad hoch","WHEELDOWNMOUSE":"Mausrad runter","SPACE":"Leertaste"},
    "ES": {"NONE":"Ninguno","CUSTOM":"Personalizado","ARROWS":"Flechas","BOTH":"WASD + flechas","FREE":"Vuelo libre","LEVEL":"Nivelado","CROSS":"Cruz","CROSS_DOT":"Cruz + punto","DOT":"Punto","CIRCLE":"Círculo","FILLED_CIRCLE":"Círculo relleno","RIGHTMOUSE":"Botón derecho","MIDDLEMOUSE":"Botón central","LEFTMOUSE":"Botón izquierdo","BOTTOM_LEFT":"Abajo izquierda","BOTTOM_RIGHT":"Abajo derecha","TOP_LEFT":"Arriba izquierda","TOP_RIGHT":"Arriba derecha","WHEELUPMOUSE":"Rueda arriba","WHEELDOWNMOUSE":"Rueda abajo","SPACE":"Espacio"},
    "FR": {"NONE":"Aucun","CUSTOM":"Personnalisé","ARROWS":"Flèches","BOTH":"WASD + flèches","FREE":"Vol libre","LEVEL":"Horizontal","CROSS":"Croix","CROSS_DOT":"Croix + point","DOT":"Point","CIRCLE":"Cercle","FILLED_CIRCLE":"Cercle plein","RIGHTMOUSE":"Bouton droit","MIDDLEMOUSE":"Bouton central","LEFTMOUSE":"Bouton gauche","BOTTOM_LEFT":"Bas gauche","BOTTOM_RIGHT":"Bas droite","TOP_LEFT":"Haut gauche","TOP_RIGHT":"Haut droite","WHEELUPMOUSE":"Molette haut","WHEELDOWNMOUSE":"Molette bas","SPACE":"Espace"},
    "IT": {"NONE":"Nessuno","CUSTOM":"Personalizzato","ARROWS":"Frecce","BOTH":"WASD + frecce","FREE":"Volo libero","LEVEL":"Livellato","CROSS":"Croce","CROSS_DOT":"Croce + punto","DOT":"Punto","CIRCLE":"Cerchio","FILLED_CIRCLE":"Cerchio pieno","RIGHTMOUSE":"Pulsante destro","MIDDLEMOUSE":"Pulsante centrale","LEFTMOUSE":"Pulsante sinistro","BOTTOM_LEFT":"Basso sinistra","BOTTOM_RIGHT":"Basso destra","TOP_LEFT":"Alto sinistra","TOP_RIGHT":"Alto destra","WHEELUPMOUSE":"Rotella su","WHEELDOWNMOUSE":"Rotella giù","SPACE":"Spazio"},
    "PT_BR": {"NONE":"Nenhum","CUSTOM":"Personalizado","ARROWS":"Setas","BOTH":"WASD + setas","FREE":"Voo livre","LEVEL":"Nivelado","CROSS":"Cruz","CROSS_DOT":"Cruz + ponto","DOT":"Ponto","CIRCLE":"Círculo","FILLED_CIRCLE":"Círculo preenchido","RIGHTMOUSE":"Botão direito","MIDDLEMOUSE":"Botão do meio","LEFTMOUSE":"Botão esquerdo","BOTTOM_LEFT":"Inferior esquerdo","BOTTOM_RIGHT":"Inferior direito","TOP_LEFT":"Superior esquerdo","TOP_RIGHT":"Superior direito","WHEELUPMOUSE":"Roda para cima","WHEELDOWNMOUSE":"Roda para baixo","SPACE":"Espaço"},
    "RU": {"NONE":"Нет","CUSTOM":"Свои","ARROWS":"Стрелки","BOTH":"WASD + стрелки","FREE":"Свободный полёт","LEVEL":"Горизонтально","CROSS":"Крест","CROSS_DOT":"Крест + точка","DOT":"Точка","CIRCLE":"Круг","FILLED_CIRCLE":"Заполненный круг","RIGHTMOUSE":"Правая кнопка мыши","MIDDLEMOUSE":"Средняя кнопка мыши","LEFTMOUSE":"Левая кнопка мыши","BOTTOM_LEFT":"Снизу слева","BOTTOM_RIGHT":"Снизу справа","TOP_LEFT":"Сверху слева","TOP_RIGHT":"Сверху справа","WHEELUPMOUSE":"Колесо вверх","WHEELDOWNMOUSE":"Колесо вниз","SPACE":"Пробел"},
    "JA": {"NONE":"なし","CUSTOM":"カスタム","ARROWS":"矢印キー","BOTH":"WASD + 矢印キー","FREE":"フリーフライト","LEVEL":"水平","CROSS":"十字","CROSS_DOT":"十字 + 点","DOT":"点","CIRCLE":"円","FILLED_CIRCLE":"塗りつぶし円","RIGHTMOUSE":"右マウスボタン","MIDDLEMOUSE":"中マウスボタン","LEFTMOUSE":"左マウスボタン","BOTTOM_LEFT":"左下","BOTTOM_RIGHT":"右下","TOP_LEFT":"左上","TOP_RIGHT":"右上","WHEELUPMOUSE":"ホイール上","WHEELDOWNMOUSE":"ホイール下","SPACE":"スペース"},
    "ZH_CN": {"NONE":"无","CUSTOM":"自定义","ARROWS":"方向键","BOTH":"WASD + 方向键","FREE":"自由飞行","LEVEL":"水平","CROSS":"十字","CROSS_DOT":"十字 + 点","DOT":"点","CIRCLE":"圆","FILLED_CIRCLE":"实心圆","RIGHTMOUSE":"鼠标右键","MIDDLEMOUSE":"鼠标中键","LEFTMOUSE":"鼠标左键","BOTTOM_LEFT":"左下","BOTTOM_RIGHT":"右下","TOP_LEFT":"左上","TOP_RIGHT":"右上","WHEELUPMOUSE":"滚轮向上","WHEELDOWNMOUSE":"滚轮向下","SPACE":"空格"},
}
_ENUM_LABELS.update({
    "UK": {"NONE":"Немає","CUSTOM":"Власний","ARROWS":"Стрілки","BOTH":"WASD + стрілки","FREE":"Вільний політ","LEVEL":"Горизонтально","CROSS":"Хрест","CROSS_DOT":"Хрест + точка","DOT":"Точка","CIRCLE":"Коло","FILLED_CIRCLE":"Заповнене коло","RIGHTMOUSE":"Права кнопка миші","MIDDLEMOUSE":"Середня кнопка миші","LEFTMOUSE":"Ліва кнопка миші","WHEELUPMOUSE":"Коліщатко вгору","WHEELDOWNMOUSE":"Коліщатко вниз","SPACE":"Пробіл","UNREAL":"Unreal Engine","BLENDER":"Blender","MAYA":"Maya","UNITY":"Unity","GODOT":"Godot"},
    "CS": {"NONE":"Žádné","CUSTOM":"Vlastní","ARROWS":"Šipky","BOTH":"WASD + šipky","FREE":"Volný let","LEVEL":"Vodorovně","CROSS":"Kříž","CROSS_DOT":"Kříž + tečka","DOT":"Tečka","CIRCLE":"Kruh","FILLED_CIRCLE":"Plný kruh","RIGHTMOUSE":"Pravé tlačítko myši","MIDDLEMOUSE":"Prostřední tlačítko myši","LEFTMOUSE":"Levé tlačítko myši","WHEELUPMOUSE":"Kolečko nahoru","WHEELDOWNMOUSE":"Kolečko dolů","SPACE":"Mezerník","UNREAL":"Unreal Engine","BLENDER":"Blender","MAYA":"Maya","UNITY":"Unity","GODOT":"Godot"},
    "NL": {"NONE":"Geen","CUSTOM":"Aangepast","ARROWS":"Pijltjestoetsen","BOTH":"WASD + pijltjestoetsen","FREE":"Vrije vlucht","LEVEL":"Horizontaal","CROSS":"Kruis","CROSS_DOT":"Kruis + punt","DOT":"Punt","CIRCLE":"Cirkel","FILLED_CIRCLE":"Gevulde cirkel","RIGHTMOUSE":"Rechtermuisknop","MIDDLEMOUSE":"Middelste muisknop","LEFTMOUSE":"Linkermuisknop","WHEELUPMOUSE":"Muiswiel omhoog","WHEELDOWNMOUSE":"Muiswiel omlaag","SPACE":"Spatie","UNREAL":"Unreal Engine","BLENDER":"Blender","MAYA":"Maya","UNITY":"Unity","GODOT":"Godot"},
    "TR": {"NONE":"Yok","CUSTOM":"Özel","ARROWS":"Yön tuşları","BOTH":"WASD + yön tuşları","FREE":"Serbest uçuş","LEVEL":"Yatay","CROSS":"Artı","CROSS_DOT":"Artı + nokta","DOT":"Nokta","CIRCLE":"Daire","FILLED_CIRCLE":"Dolu daire","RIGHTMOUSE":"Sağ fare düğmesi","MIDDLEMOUSE":"Orta fare düğmesi","LEFTMOUSE":"Sol fare düğmesi","WHEELUPMOUSE":"Tekerlek yukarı","WHEELDOWNMOUSE":"Tekerlek aşağı","SPACE":"Boşluk","UNREAL":"Unreal Engine","BLENDER":"Blender","MAYA":"Maya","UNITY":"Unity","GODOT":"Godot"},
    "KO": {"NONE":"없음","CUSTOM":"사용자 지정","ARROWS":"방향키","BOTH":"WASD + 방향키","FREE":"자유 비행","LEVEL":"수평","CROSS":"십자","CROSS_DOT":"십자 + 점","DOT":"점","CIRCLE":"원","FILLED_CIRCLE":"채운 원","RIGHTMOUSE":"마우스 오른쪽 버튼","MIDDLEMOUSE":"마우스 가운데 버튼","LEFTMOUSE":"마우스 왼쪽 버튼","WHEELUPMOUSE":"휠 위","WHEELDOWNMOUSE":"휠 아래","SPACE":"스페이스","UNREAL":"Unreal Engine","BLENDER":"Blender","MAYA":"Maya","UNITY":"Unity","GODOT":"Godot"},
})
# Extra labels for the new information-layout selector. Keeping these separate
# avoids duplicating the large enum translation table above.
_INFO_POSITION_LABELS = {
    "EN": {"HEADER":"Top - viewport header", "TOP_LEFT":"Top left", "TOP_RIGHT":"Top right", "BOTTOM_LEFT":"Bottom left", "BOTTOM_CENTER":"Bottom center", "BOTTOM_RIGHT":"Bottom right", "SPLIT":"Split top / bottom"},
    "PL": {"HEADER":"Góra - nagłówek viewportu", "TOP_LEFT":"Góra po lewej", "TOP_RIGHT":"Góra po prawej", "BOTTOM_LEFT":"Dół po lewej", "BOTTOM_CENTER":"Dół na środku", "BOTTOM_RIGHT":"Dół po prawej", "SPLIT":"Podział góra / dół"},
    "DE": {"HEADER":"Oben - Viewport-Kopf", "TOP_LEFT":"Oben links", "TOP_RIGHT":"Oben rechts", "BOTTOM_LEFT":"Unten links", "BOTTOM_CENTER":"Unten mittig", "BOTTOM_RIGHT":"Unten rechts", "SPLIT":"Oben / unten geteilt"},
    "ES": {"HEADER":"Arriba - cabecera", "TOP_LEFT":"Arriba izquierda", "TOP_RIGHT":"Arriba derecha", "BOTTOM_LEFT":"Abajo izquierda", "BOTTOM_CENTER":"Abajo centro", "BOTTOM_RIGHT":"Abajo derecha", "SPLIT":"Dividido arriba / abajo"},
    "FR": {"HEADER":"Haut - en-tête", "TOP_LEFT":"Haut gauche", "TOP_RIGHT":"Haut droite", "BOTTOM_LEFT":"Bas gauche", "BOTTOM_CENTER":"Bas centre", "BOTTOM_RIGHT":"Bas droite", "SPLIT":"Partagé haut / bas"},
    "IT": {"HEADER":"Alto - intestazione", "TOP_LEFT":"Alto sinistra", "TOP_RIGHT":"Alto destra", "BOTTOM_LEFT":"Basso sinistra", "BOTTOM_CENTER":"Basso centro", "BOTTOM_RIGHT":"Basso destra", "SPLIT":"Diviso alto / basso"},
    "PT_BR": {"HEADER":"Topo - cabeçalho", "TOP_LEFT":"Superior esquerdo", "TOP_RIGHT":"Superior direito", "BOTTOM_LEFT":"Inferior esquerdo", "BOTTOM_CENTER":"Inferior central", "BOTTOM_RIGHT":"Inferior direito", "SPLIT":"Dividido topo / baixo"},
    "RU": {"HEADER":"Сверху - заголовок", "TOP_LEFT":"Сверху слева", "TOP_RIGHT":"Сверху справа", "BOTTOM_LEFT":"Снизу слева", "BOTTOM_CENTER":"Снизу по центру", "BOTTOM_RIGHT":"Снизу справа", "SPLIT":"Раздельно сверху / снизу"},
    "JA": {"HEADER":"上 - ヘッダー", "TOP_LEFT":"左上", "TOP_RIGHT":"右上", "BOTTOM_LEFT":"左下", "BOTTOM_CENTER":"下中央", "BOTTOM_RIGHT":"右下", "SPLIT":"上 / 下に分割"},
    "ZH_CN": {"HEADER":"顶部 - 标题栏", "TOP_LEFT":"左上", "TOP_RIGHT":"右上", "BOTTOM_LEFT":"左下", "BOTTOM_CENTER":"底部居中", "BOTTOM_RIGHT":"右下", "SPLIT":"顶部 / 底部分离"},
    "UK": {"HEADER":"Вгорі - заголовок viewport", "TOP_LEFT":"Вгорі ліворуч", "TOP_RIGHT":"Вгорі праворуч", "BOTTOM_LEFT":"Внизу ліворуч", "BOTTOM_CENTER":"Внизу по центру", "BOTTOM_RIGHT":"Внизу праворуч", "SPLIT":"Розділити верх / низ"},
    "CS": {"HEADER":"Nahoře - záhlaví viewportu", "TOP_LEFT":"Vlevo nahoře", "TOP_RIGHT":"Vpravo nahoře", "BOTTOM_LEFT":"Vlevo dole", "BOTTOM_CENTER":"Dole uprostřed", "BOTTOM_RIGHT":"Vpravo dole", "SPLIT":"Rozdělit nahoře / dole"},
    "NL": {"HEADER":"Boven - viewportkop", "TOP_LEFT":"Linksboven", "TOP_RIGHT":"Rechtsboven", "BOTTOM_LEFT":"Linksonder", "BOTTOM_CENTER":"Midden onder", "BOTTOM_RIGHT":"Rechtsonder", "SPLIT":"Gesplitst boven / onder"},
    "TR": {"HEADER":"Üst - viewport başlığı", "TOP_LEFT":"Sol üst", "TOP_RIGHT":"Sağ üst", "BOTTOM_LEFT":"Sol alt", "BOTTOM_CENTER":"Alt orta", "BOTTOM_RIGHT":"Sağ alt", "SPLIT":"Üst / alt bölünmüş"},
    "KO": {"HEADER":"위 - 뷰포트 헤더", "TOP_LEFT":"왼쪽 위", "TOP_RIGHT":"오른쪽 위", "BOTTOM_LEFT":"왼쪽 아래", "BOTTOM_CENTER":"아래 중앙", "BOTTOM_RIGHT":"오른쪽 아래", "SPLIT":"위 / 아래 분할"},
}
for _lang_code, _labels in _INFO_POSITION_LABELS.items():
    _ENUM_LABELS.setdefault(_lang_code, {}).update(_labels)

_ENUM_ITEMS_CACHE = {}


def _enum_source_items(property_name):
    return _ENUM_PROPERTY_ITEMS.get(property_name, (("NONE", "None", "None"),))


def _enum_label(prefs, property_name, identifier):
    lang = _language(prefs)
    labels = _ENUM_LABELS.get(lang, _ENUM_LABELS["EN"])
    if identifier in labels:
        return labels[identifier]
    for item_identifier, label, _description in _enum_source_items(property_name):
        if item_identifier == identifier:
            return label
    return str(identifier).replace("_", " ").title()


def _enum_items_for_property(prefs, property_name):
    lang = _language(prefs)
    cache_key = (lang, property_name)
    cached = _ENUM_ITEMS_CACHE.get(cache_key)
    if cached is not None:
        return cached
    result = tuple(
        (identifier, _enum_label(prefs, property_name, identifier), _enum_label(prefs, property_name, identifier))
        for identifier, _label, _description in _enum_source_items(property_name)
    )
    _ENUM_ITEMS_CACHE[cache_key] = result
    return result


def _language(prefs):
    lang = getattr(prefs, "ui_language", "EN") if prefs is not None else "EN"
    return lang if lang in _TEXT else "EN"


def _tr(prefs, key, **kwargs):
    text = _TEXT[_language(prefs)].get(key, _EN.get(key, key))
    return text.format(**kwargs) if kwargs else text


# EnumProperty item lists are static constants above. Keeping them static avoids
# Blender registration failures and makes saved identifiers stable.

_SPEED_TO_METERS = {"M_S": 1.0, "CM_S": 0.01, "MM_S": 0.001, "KM_H": 1.0 / 3.6, "FT_S": 0.3048, "MPH": 0.44704}
_SPEED_SUFFIX = {"BU_S": "BU/s", "M_S": "m/s", "CM_S": "cm/s", "MM_S": "mm/s", "KM_H": "km/h", "FT_S": "ft/s", "MPH": "mph"}


def _clamp(value, minimum, maximum): return max(minimum, min(maximum, value))


def _scene_scale_length(context=None):
    context = context or bpy.context
    scene = getattr(context, "scene", None)
    if scene is None: return 1.0
    value = float(getattr(scene.unit_settings, "scale_length", 1.0))
    return value if value > 1.0e-12 else 1.0


def _speed_to_bu(value, unit, context=None):
    value = float(value)
    if unit == "BU_S": return value
    return (value * _SPEED_TO_METERS.get(unit, 1.0)) / _scene_scale_length(context)


def _speed_from_bu(value_bu, unit, context=None):
    value_bu = float(value_bu)
    if unit == "BU_S": return value_bu
    return (value_bu * _scene_scale_length(context)) / _SPEED_TO_METERS.get(unit, 1.0)


def _update_speed_unit(self, context):
    previous = getattr(self, "speed_unit_previous", "BU_S") or "BU_S"
    current = getattr(self, "speed_unit", "BU_S") or "BU_S"
    if previous != current:
        for name in ("move_speed", "minimum_speed", "maximum_speed"):
            value_bu = _speed_to_bu(float(getattr(self, name)), previous, context)
            setattr(self, name, _clamp(_speed_from_bu(value_bu, current, context), 1.0e-9, 1.0e12))
        self.speed_unit_previous = current


def _format_number(value):
    absolute = abs(value)
    if absolute >= 1000.0: return f"{value:,.1f}"
    if absolute >= 100.0: return f"{value:.1f}"
    if absolute >= 10.0: return f"{value:.2f}"
    if absolute >= 1.0: return f"{value:.2f}"
    if absolute >= 0.01: return f"{value:.3f}"
    return f"{value:.4g}"


def _format_speed(prefs):
    unit = getattr(prefs, "speed_unit", "BU_S")
    return f"{_format_number(float(prefs.move_speed))} {_SPEED_SUFFIX.get(unit, 'BU/s')}"


def _navigation_keys_mode(prefs):
    value = getattr(prefs, "navigation_keys", "WASD")
    return value if value in {"WASD", "ARROWS", "BOTH", "CUSTOM"} else "WASD"


def _modifier_event_set(value):
    known = {"SHIFT": set(_SHIFT_KEYS), "CTRL": set(_CTRL_KEYS), "ALT": set(_ALT_KEYS), "NONE": set()}
    return known[value] if value in known else ({value} if value else set())


def _modifier_is_held(value, event=None, pressed=None):
    if value == "NONE": return True
    pressed = pressed or set()
    if _modifier_event_set(value).intersection(pressed): return True
    if event is None: return False
    if value in {"SHIFT", "CTRL", "ALT"}:
        return bool(getattr(event, value.lower(), False))
    return getattr(event, "type", None) == value and getattr(event, "value", "PRESS") != "RELEASE"


def _hold_key_is_held(value, event=None, pressed=None):
    if value == "NONE":
        return False
    return _modifier_is_held(value, event=event, pressed=pressed)


def _key_label(value):
    mouse = {"RIGHTMOUSE": "RMB", "MIDDLEMOUSE": "MMB", "LEFTMOUSE": "LMB", "WHEELUPMOUSE": "Wheel Up", "WHEELDOWNMOUSE": "Wheel Down"}
    modifiers = {"SHIFT": "Shift", "CTRL": "Ctrl", "ALT": "Alt", "NONE": ""}
    if value in mouse: return mouse[value]
    if value in modifiers: return modifiers[value]
    return value.replace("_", " ").title()


def _shortcut_label(mouse, modifier="NONE", extra_modifier="NONE"):
    parts = []
    for value in (modifier, extra_modifier):
        label = _key_label(value)
        if label and label not in parts: parts.append(label)
    parts.append(_key_label(mouse))
    return "+".join(parts)


def _movement_action_map(prefs):
    mode = _navigation_keys_mode(prefs)
    if mode == "CUSTOM":
        return {
            "forward": {prefs.move_forward_key}, "backward": {prefs.move_backward_key},
            "left": {prefs.move_left_key}, "right": {prefs.move_right_key},
            "up": {prefs.move_up_key}, "down": {prefs.move_down_key},
        }
    actions = {"forward": set(), "backward": set(), "left": set(), "right": set(), "up": {"E"}, "down": {"Q"}}
    if mode in {"WASD", "BOTH"}:
        actions["forward"].add("W"); actions["backward"].add("S"); actions["left"].add("A"); actions["right"].add("D")
    if mode in {"ARROWS", "BOTH"}:
        actions["forward"].add("UP_ARROW"); actions["backward"].add("DOWN_ARROW"); actions["left"].add("LEFT_ARROW"); actions["right"].add("RIGHT_ARROW")
    return actions


def _all_action_keys(prefs):
    keys = set()
    for values in _movement_action_map(prefs).values(): keys.update(values)
    keys.update(_modifier_event_set(getattr(prefs, "sprint_key", "SHIFT")))
    keys.update(_modifier_event_set(getattr(prefs, "precision_key", "CTRL")))
    return keys


def _movement_keys_label(prefs):
    mode = _navigation_keys_mode(prefs)
    if mode == "CUSTOM":
        a = _movement_action_map(prefs)
        return f"{_key_label(next(iter(a['forward'])))} / {_key_label(next(iter(a['backward'])))} / {_key_label(next(iter(a['left'])))} / {_key_label(next(iter(a['right'])))}"
    return {"WASD": "WASD", "ARROWS": "Arrow keys", "BOTH": "WASD / Arrow keys"}.get(mode, "WASD")


def _orbit_shortcut(prefs, include_guard=False):
    # Camera protection is a setting, not a fragile three-button chord.
    return _shortcut_label(
        getattr(prefs, "orbit_mouse", "RIGHTMOUSE"),
        getattr(prefs, "orbit_modifier", "ALT"),
    )


def _controls_short(prefs):
    nav = _shortcut_label(getattr(prefs, "navigation_mouse", "RIGHTMOUSE"), getattr(prefs, "navigation_modifier", "NONE"))
    movement = _movement_keys_label(prefs)
    sprint = _key_label(getattr(prefs, "sprint_key", "SHIFT"))
    precision = _key_label(getattr(prefs, "precision_key", "CTRL"))
    parts = [f"{nav} + {movement}"]
    if getattr(prefs, "navigation_keys", "WASD") != "CUSTOM":
        parts.append("Q/E")
    if sprint:
        parts.append(f"{sprint}: {_tr(prefs, 'sprint_short')}")
    if precision:
        parts.append(f"{precision}: {_tr(prefs, 'precision_short')}")
    return " · ".join(parts)


def _header_text(prefs):
    parts = []
    if getattr(prefs, "show_header_speed", True):
        parts.append(f"UE NAV | {_format_speed(prefs)}")
    if getattr(prefs, "show_header_tutorial", True):
        parts.append(_controls_short(prefs))
    return " | ".join(parts) if parts else None

