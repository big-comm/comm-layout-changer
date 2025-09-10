#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, Adw, Gdk, Gio, GLib, Pango
import subprocess
import os
import sys
import locale
import threading
import time
import random
import xml.etree.ElementTree as ET

# Complete translation dictionary
TRANSLATIONS = {
    "en": {
        "window_title": "Big Community Desktop Layout Switcher",
        "select_layout": "Select Layout",
        "applying": "Applying {layout} layout...",
        "success": "Successfully applied {layout} layout",
        "error_config": "Error: Config file not found - {file}",
        "error_applying": "Error applying layout: {error}",
        "error": "Error: {error}",
        "apply": "Apply Layout",
        "about": "About",
        "quit": "Quit",
        "description_layout": "Apply the {layout} layout to your desktop.",
        "gnome": "GNOME",
        "cinnamon": "Cinnamon",
        "xfce": "XFCE"
    },
    "es": {
        "window_title": "Selector de Diseño de Escritorio de Big Community",
        "select_layout": "Seleccionar Diseño",
        "applying": "Aplicando diseño {layout}...",
        "success": "Diseño {layout} aplicado con éxito",
        "error_config": "Error: Archivo de configuración no encontrado - {file}",
        "error_applying": "Error al aplicar el diseño: {error}",
        "error": "Error: {error}",
        "apply": "Aplicar Diseño",
        "about": "Acerca de",
        "quit": "Salir",
        "description_layout": "Aplica el diseño {layout} a tu escritorio.",
        "gnome": "GNOME",
        "cinnamon": "Cinnamon",
        "xfce": "XFCE"
    },
    "fr": {
        "window_title": "Sélecteur de Disposition de Bureau de Big Community",
        "select_layout": "Sélectionner la disposition",
        "applying": "Application de la disposition {layout}...",
        "success": "Disposition {layout} appliquée avec succès",
        "error_config": "Erreur: Fichier de configuration non trouvé - {file}",
        "error_applying": "Erreur lors de l'application de la disposition: {error}",
        "error": "Erreur: {error}",
        "apply": "Appliquer la disposition",
        "about": "À propos",
        "quit": "Quitter",
        "description_layout": "Applique la disposition {layout} à votre bureau.",
        "gnome": "GNOME",
        "cinnamon": "Cinnamon",
        "xfce": "XFCE"
    },
    "de": {
        "window_title": "Big Community Desktop-Layout-Switcher",
        "select_layout": "Layout auswählen",
        "applying": "Wende {layout} Layout an...",
        "success": "{layout} Layout erfolgreich angewendet",
        "error_config": "Fehler: Konfigurationsdatei nicht gefunden - {file}",
        "error_applying": "Fehler beim Anwenden des Layouts: {error}",
        "error": "Fehler: {error}",
        "apply": "Layout anwenden",
        "about": "Über",
        "quit": "Beenden",
        "description_layout": "Wende das {layout} Layout auf deinen Desktop an.",
        "gnome": "GNOME",
        "cinnamon": "Cinnamon",
        "xfce": "XFCE"
    },
    "pt_BR": {
        "window_title": "Alternador de Layout de Área de Trabalho da Big Community",
        "select_layout": "Selecionar Layout",
        "applying": "Aplicando layout {layout}...",
        "success": "Layout {layout} aplicado com sucesso",
        "error_config": "Erro: Arquivo de configuração não encontrado - {file}",
        "error_applying": "Erro ao aplicar o layout: {error}",
        "error": "Erro: {error}",
        "apply": "Aplicar Layout",
        "about": "Sobre",
        "quit": "Sair",
        "description_layout": "Aplica o layout {layout} à sua área de trabalho.",
        "gnome": "GNOME",
        "cinnamon": "Cinnamon",
        "xfce": "XFCE"
    }
}

# Get system language
def get_system_language():
    try:
        lang = locale.getdefaultlocale()[0]
        if lang:
            # Check if we have a translation for the full locale
            if lang in TRANSLATIONS:
                return lang
            # Extract primary language code (e.g., 'pt' from 'pt_BR')
            primary_lang = lang.split('_')[0]
            # Check if we have a translation for the primary language
            if primary_lang in TRANSLATIONS:
                return primary_lang
    except:
        pass
    return "en"  # Default to English

# Translation function
def _(text):
    lang = get_system_language()
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(text, text)

# Detect desktop environment
def detect_desktop_environment():
    desktop = os.environ.get('XDG_CURRENT_DESKTOP', '').lower()
    if 'gnome' in desktop:
        return 'gnome'
    elif 'cinnamon' in desktop:
        return 'cinnamon'
    elif 'xfce' in desktop:
        return 'xfce'
    else:
        # Fallback to checking other environment variables
        if 'GNOME_DESKTOP_SESSION_ID' in os.environ:
            return 'gnome'
        elif 'CINNAMON_VERSION' in os.environ:
            return 'cinnamon'
        elif 'XFCE4_SESSION' in os.environ:
            return 'xfce'
        return 'gnome'  # Default to GNOME

class LayoutSwitcher(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title(_("window_title"))
        self.set_default_size(700, 450)
        self.set_size_request(600, 400)
        
        # Detect desktop environment
        self.desktop_env = detect_desktop_environment()
        print(f"Detected desktop environment: {self.desktop_env}")
        
        # Define layouts based on desktop environment
        self.define_layouts()
        
        # Initialize state variables
        self.selected_item = None
        self.selected_type = None
        self.applying = False
        self.updating_selection = False  # Flag to prevent selection loops
        
        # Create UI components
        self.create_ui()
        
        # Load minimal CSS for selection
        self.load_css()
        
        # Select first layout by default
        if self.layouts:
            self.select_item((self.layouts[0][0], self.layouts[0][1]), "layout")
        
        # Connect to resize event for responsive adjustments
        self.connect("notify::default-width", self.on_resize)
        self.connect("notify::default-height", self.on_resize)
    
    def define_layouts(self):
        """Define layouts based on desktop environment"""
        if self.desktop_env == 'gnome':
            self.layouts = [
                ("Classic", "classic.txt", "classic.png", "view-continuous-symbolic"),
                ("Vanilla", "vanilla.txt", "vanilla.png", "view-grid-symbolic"),
                ("G-Unity", "g-unity.txt", "g-unity.png", "view-app-grid-symbolic"),
                ("New", "new.txt", "new.png", "view-paged-symbolic"),
                ("Next-Gnome", "next-gnome.txt", "next-gnome.png", "view-paged-symbolic"),
                ("Modern", "modern.txt", "modern.png", "view-grid-symbolic")
            ]
        elif self.desktop_env == 'cinnamon':
            self.layouts = [
                ("Classic", "classic.txt", "classic.png", "view-continuous-symbolic"),
                ("Modern", "modern.txt", "modern.png", "view-grid-symbolic")
            ]
        elif self.desktop_env == 'xfce':
            self.layouts = [
                ("SUSE Way", "suse-way.txt", "suse-way.png", "view-continuous-symbolic"),
                ("XFCE-Like", "xfce-like.txt", "xfce-like.png", "view-grid-symbolic"),
                ("Big-like", "big-like.txt", "big-like.png", "view-app-grid-symbolic")
            ]
    
    def create_ui(self):
        """Create all UI components"""
        # Create toolbar view
        toolbar_view = Adw.ToolbarView()
        
        # Create header bar
        header_bar = Adw.HeaderBar()
        toolbar_view.add_top_bar(header_bar)
        
        # Add desktop environment label
        desktop_label = Gtk.Label()
        desktop_label.set_text(f"{_(self.desktop_env.capitalize())} Desktop")
        desktop_label.add_css_class("title-3")
        header_bar.set_title_widget(desktop_label)
        
        # Add menu button
        menu_button = Gtk.MenuButton()
        menu_button.set_icon_name("open-menu-symbolic")
        
        # Create menu model
        menu = Gio.Menu()
        menu.append(_("about"), "app.about")
        menu.append(_("quit"), "app.quit")
        
        # Set menu to button
        menu_button.set_menu_model(menu)
        header_bar.pack_end(menu_button)
        
        # Create paned widget for main layout
        self.paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        self.paned.set_position(500)
        self.paned.set_resize_start_child(True)
        self.paned.set_shrink_start_child(False)
        self.paned.set_resize_end_child(False)
        self.paned.set_shrink_end_child(False)
        
        # Create main content area
        main_content = self.create_main_content()
        self.paned.set_start_child(main_content)
        
        # Create sidebar
        sidebar = self.create_sidebar()
        self.paned.set_end_child(sidebar)
        
        # Set paned as content
        toolbar_view.set_content(self.paned)
        
        # Set toolbar view as window content
        self.set_content(toolbar_view)
    
    def create_main_content(self):
        """Create the main content area"""
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)
        
        # Welcome section
        welcome_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        welcome_box.set_margin_bottom(20)
        
        welcome_title = Gtk.Label()
        welcome_title.set_text(_("window_title"))
        welcome_title.add_css_class("title-1")
        welcome_title.set_margin_bottom(5)
        welcome_title.set_halign(Gtk.Align.START)
        welcome_box.append(welcome_title)
        
        welcome_subtitle = Gtk.Label()
        welcome_subtitle.set_text(_("select_layout"))
        welcome_subtitle.add_css_class("title-2")
        welcome_subtitle.set_halign(Gtk.Align.START)
        welcome_box.append(welcome_subtitle)
        
        main_box.append(welcome_box)
        
        # Preview area
        preview_area = self.create_preview_area()
        main_box.append(preview_area)
        
        return main_box
    
    def create_preview_area(self):
        """Create the preview area"""
        preview_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        preview_container.set_halign(Gtk.Align.CENTER)
        preview_container.set_valign(Gtk.Align.CENTER)
        preview_container.set_vexpand(True)
        
        # Preview card
        preview_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        preview_card.add_css_class("card")
        preview_card.set_size_request(400, 300)
        
        # Preview title
        self.preview_title = Gtk.Label()
        self.preview_title.add_css_class("title-2")
        self.preview_title.set_margin_bottom(15)
        self.preview_title.set_halign(Gtk.Align.CENTER)
        preview_card.append(self.preview_title)
        
        # Preview image with frame
        image_frame = Gtk.Box()
        image_frame.add_css_class("frame")
        image_frame.set_halign(Gtk.Align.CENTER)
        image_frame.set_size_request(350, 180)
        
        self.preview_image = Gtk.Picture()
        self.preview_image.set_size_request(330, 160)
        self.preview_image.set_content_fit(Gtk.ContentFit.CONTAIN)
        image_frame.append(self.preview_image)
        preview_card.append(image_frame)
        
        # Preview description
        self.preview_description = Gtk.Label()
        self.preview_description.set_margin_top(15)
        self.preview_description.set_margin_bottom(20)
        self.preview_description.set_halign(Gtk.Align.CENTER)
        self.preview_description.set_wrap(True)
        self.preview_description.set_max_width_chars(40)
        preview_card.append(self.preview_description)
        
        # Apply button
        self.apply_button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.apply_button_box.set_halign(Gtk.Align.CENTER)
        
        self.apply_button = Gtk.Button(label=_("apply"))
        self.apply_button.add_css_class("suggested-action")
        self.apply_button.add_css_class("pill")
        self.apply_button.set_size_request(150, 40)
        self.apply_button.set_margin_top(5)
        self.apply_button.connect("clicked", self.on_apply_clicked)
        self.apply_button_box.append(self.apply_button)
        
        # Spinner for loading state
        self.spinner = Gtk.Spinner()
        self.spinner.set_size_request(20, 20)
        self.spinner.set_margin_start(10)
        self.spinner.set_visible(False)
        self.apply_button_box.append(self.spinner)
        
        preview_card.append(self.apply_button_box)
        preview_container.append(preview_card)
        
        # Status bar
        status_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        status_container.set_halign(Gtk.Align.CENTER)
        status_container.set_margin_top(15)
        
        self.status_bar = Gtk.Label()
        self.status_bar.set_wrap(True)
        self.status_bar.set_max_width_chars(40)
        status_container.append(self.status_bar)
        preview_container.append(status_container)
        
        return preview_container
    
    def create_sidebar(self):
        """Create the sidebar for layout selection"""
        sidebar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        sidebar_box.set_size_request(200, -1)
        
        # Sidebar header
        sidebar_header = Gtk.Label()
        sidebar_header.set_text(_("select_layout"))
        sidebar_header.add_css_class("title-3")
        sidebar_header.set_margin_start(15)
        sidebar_header.set_margin_top(15)
        sidebar_header.set_margin_bottom(15)
        sidebar_header.set_halign(Gtk.Align.START)
        sidebar_box.append(sidebar_header)
        
        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_start(10)
        separator.set_margin_end(10)
        separator.set_margin_bottom(5)
        sidebar_box.append(separator)
        
        # Create scrolled window for layout list
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_vexpand(True)
        
        # Layout list box
        self.layout_list_box = Gtk.ListBox()
        self.layout_list_box.set_selection_mode(Gtk.SelectionMode.SINGLE)
        
        # Connect row-selected signal for single click selection
        self.layout_list_box.connect("row-selected", self.on_row_selected)
        
        # Create layout buttons
        self.layout_buttons = []
        for name, config_file, icon_file, fallback_icon in self.layouts:
            row = self.create_layout_row(name, icon_file, fallback_icon, config_file)
            self.layout_list_box.append(row)
            self.layout_buttons.append((row, name, config_file))
        
        scrolled_window.set_child(self.layout_list_box)
        sidebar_box.append(scrolled_window)
        
        return sidebar_box
    
    def create_layout_row(self, name, icon_file, fallback_icon, config_file):
        """Create a layout row for the sidebar with improved image sizing"""
        row = Gtk.ListBoxRow()
        row.add_css_class("layout-row")
        
        # Store the layout data in the row for easy access
        row.layout_name = name
        row.config_file = config_file
        
        # Row content with improved layout
        row_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        row_box.set_margin_start(12)
        row_box.set_margin_end(12)
        row_box.set_margin_top(10)
        row_box.set_margin_bottom(10)
        
        # Create icon container with consistent sizing
        icon_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        icon_container.set_size_request(60, 60)  # Fixed size for all icons
        icon_container.add_css_class("icon-container")
        
        # Icon frame with consistent styling
        icon_frame = Gtk.Box()
        icon_frame.set_size_request(48, 48)  # Fixed icon frame size
        icon_frame.add_css_class("icon-frame")
        icon_frame.set_halign(Gtk.Align.CENTER)
        icon_frame.set_valign(Gtk.Align.CENTER)
        
        # Create image with consistent sizing
        image = Gtk.Picture()
        image.set_size_request(40, 40)  # Fixed image size
        image.set_content_fit(Gtk.ContentFit.CONTAIN)
        image.set_halign(Gtk.Align.CENTER)
        image.set_valign(Gtk.Align.CENTER)
        
        # Try to load custom icon if icon_file is provided
        if icon_file:
            icon_path = self.find_icon(icon_file)
            if icon_path:
                image.set_filename(icon_path)
            else:
                # Use fallback icon
                fallback_image = Gtk.Image.new_from_icon_name(fallback_icon)
                fallback_image.set_pixel_size(32)  # Consistent fallback size
                image.set_paintable(fallback_image.get_paintable())
        else:
            # Use fallback icon
            fallback_image = Gtk.Image.new_from_icon_name(fallback_icon)
            fallback_image.set_pixel_size(32)  # Consistent fallback size
            image.set_paintable(fallback_image.get_paintable())
        
        icon_frame.append(image)
        icon_container.append(icon_frame)
        
        # Create label container
        label_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        label_container.set_halign(Gtk.Align.START)
        label_container.set_valign(Gtk.Align.CENTER)
        label_container.set_hexpand(True)
        
        # Create label with improved styling
        label = Gtk.Label(label=name)
        label.add_css_class("layout-label")
        label.set_halign(Gtk.Align.START)
        label.set_valign(Gtk.Align.CENTER)
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_max_width_chars(12)  # Consistent text width
        
        label_container.append(label)
        
        # Add to row box
        row_box.append(icon_container)
        row_box.append(label_container)
        row.set_child(row_box)
        
        return row
    
    def on_row_selected(self, list_box, row):
        """Handle row selection (single click)"""
        if self.updating_selection:
            return
            
        if row is None:
            return
            
        # Get the layout data directly from the row
        name = row.layout_name
        config_file = row.config_file
        
        # Select the item
        self.select_item((name, config_file), "layout")
    
    def select_item(self, item, item_type):
        """Select an item and update the preview"""
        self.selected_item = item
        self.selected_type = item_type
        
        # Clear previous selection
        self.clear_selection()
        
        # Update preview
        if item_type == "layout":
            name, config_file = item
            self.update_preview(name)
            self.highlight_selected_row(name)
    
    def update_preview(self, name):
        """Update the preview area"""
        self.preview_title.set_text(name)
        self.preview_description.set_text(_("description_layout").format(layout=name))
        
        # Try to load preview image
        icon_path = None
        for layout in self.layouts:
            if layout[0] == name:
                icon_path = self.find_icon(layout[2])
                break
        
        # Set image or fallback
        if icon_path and isinstance(icon_path, str) and os.path.exists(icon_path):
            self.preview_image.set_filename(icon_path)
        else:
            # Use fallback icon
            fallback_image = Gtk.Image.new_from_icon_name("view-grid-symbolic")
            fallback_image.set_pixel_size(80)
            self.preview_image.set_paintable(fallback_image.get_paintable())
    
    def highlight_selected_row(self, name):
        """Highlight the selected row in the list"""
        self.updating_selection = True
        
        for row, row_name, _ in self.layout_buttons:
            if row_name == name:
                row.add_css_class("selected")
                self.layout_list_box.select_row(row)
                break
        
        self.updating_selection = False
    
    def clear_selection(self):
        """Clear selection from all rows"""
        self.updating_selection = True
        
        for row, _, _ in self.layout_buttons:
            row.remove_css_class("selected")
        
        self.updating_selection = False
    
    def on_apply_clicked(self, widget):
        """Handle apply button click"""
        if self.applying or not self.selected_item or not self.selected_type:
            return
        
        # Disable button and show spinner
        self.set_applying_state(True)
        
        # Start applying in a separate thread
        threading.Thread(target=self.apply_selected_item, daemon=True).start()
    
    def set_applying_state(self, applying):
        """Set the applying state of the UI"""
        self.applying = applying
        self.apply_button.set_sensitive(not applying)
        
        if applying:
            self.spinner.set_visible(True)
            self.spinner.start()
        else:
            self.spinner.set_visible(False)
            self.spinner.stop()
    
    def apply_selected_item(self):
        """Apply the selected item in a separate thread"""
        try:
            if self.selected_type == "layout":
                self.apply_layout()
        except Exception as e:
            # Update UI on main thread
            GLib.idle_add(self.update_status, _("error").format(error=str(e)))
        finally:
            # Always reset applying state
            GLib.idle_add(self.set_applying_state, False)
    
    def apply_layout(self):
        """Apply the selected layout"""
        name, config_file = self.selected_item
        GLib.idle_add(self.update_status, _("applying").format(layout=name))
        
        # Find config file path based on desktop environment
        config_path = self.find_config_file(config_file)
        if not config_path:
            GLib.idle_add(self.update_status, _("error_config").format(file=config_file))
            return
        
        # Apply layout based on desktop environment
        try:
            if self.desktop_env == 'gnome':
                self.apply_gnome_layout(config_path)
            elif self.desktop_env == 'cinnamon':
                self.apply_cinnamon_layout(config_path)
            elif self.desktop_env == 'xfce':
                self.apply_xfce_layout(config_path)
            
            # Give desktop time to apply changes
            time.sleep(0.5)
            
            GLib.idle_add(self.update_status, _("success").format(layout=name))
        except subprocess.TimeoutExpired:
            GLib.idle_add(self.update_status, _("error_applying").format(error="Operation timed out"))
        except subprocess.CalledProcessError as e:
            GLib.idle_add(self.update_status, _("error_applying").format(error=str(e)))
        except Exception as e:
            GLib.idle_add(self.update_status, _("error").format(error=str(e)))
    
    def apply_gnome_layout(self, config_path):
        """Apply GNOME layout using dconf"""
        # Use a more robust approach to apply the layout
        with open(config_path, 'r') as f:
            config_data = f.read()
        
        # Write to a temporary file to avoid issues
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write(config_data)
            temp_file_path = temp_file.name
        
        try:
            # Apply the configuration
            subprocess.run(
                ["dconf", "load", "/org/gnome/shell/"],
                stdin=open(temp_file_path, 'r'),
                check=True,
                timeout=10
            )
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)
    
    def apply_cinnamon_layout(self, config_path):
        """Apply Cinnamon layout using dconf"""
        # Use a more robust approach to apply the layout
        with open(config_path, 'r') as f:
            config_data = f.read()
        
        # Write to a temporary file to avoid issues
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write(config_data)
            temp_file_path = temp_file.name
        
        try:
            # Apply the configuration
            subprocess.run(
                ["dconf", "load", "/org/cinnamon/"],
                stdin=open(temp_file_path, 'r'),
                check=True,
                timeout=10
            )
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)
    
    def apply_xfce_layout(self, config_path):
        """Apply XFCE layout using xfconf-query"""
        # Read the configuration file
        with open(config_path, 'r') as f:
            config_data = f.read()
        
        # Process each line in the configuration
        for line in config_data.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Split line into property and value
            parts = line.split(' ', 1)
            if len(parts) != 2:
                continue
            
            prop, val = parts
            
            # Apply the configuration using xfconf-query
            subprocess.run(
                ["xfconf-query", "-c", "xfce4-panel", "-p", prop, "-s", val],
                check=True,
                timeout=10
            )
    
    def update_status(self, message):
        """Update the status bar safely from any thread"""
        self.status_bar.set_label(message)
        return False  # Don't call again
    
    def on_resize(self, widget, param):
        """Handle window resize for responsive adjustments"""
        width = self.get_width()
        
        # Adjust paned position based on width
        if width < 700:  # Small screens
            self.paned.set_position(int(width * 0.6))
        else:  # Large screens
            self.paned.set_position(500)
        
        # Adjust preview image size
        if width < 700:
            self.preview_image.set_size_request(280, 140)
        else:
            self.preview_image.set_size_request(330, 160)
    
    def find_icon(self, icon_name):
        """Search for icon in common locations"""
        if not icon_name:
            return None
            
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "icons", icon_name),
            os.path.expanduser(f"~/.local/share/icons/{icon_name}"),
            f"/usr/share/icons/{icon_name}",
            f"/usr/local/share/icons/{icon_name}"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # Try with different extensions
        base_name, ext = os.path.splitext(icon_name)
        for ext in ['.png', '.jpg', '.jpeg', '.svg']:
            test_path = base_name + ext
            for path in possible_paths:
                test_path = os.path.join(os.path.dirname(path), os.path.basename(test_path))
                if os.path.exists(test_path):
                    return test_path
        
        return None
    
    def find_config_file(self, config_file):
        """Search for config file in common locations based on desktop environment"""
        # Determine the config directory based on desktop environment
        if self.desktop_env == 'gnome':
            config_dir = "gnome-layouts"
        elif self.desktop_env == 'cinnamon':
            config_dir = "cinnamon-layouts"
        elif self.desktop_env == 'xfce':
            config_dir = "xfce-layouts"
        else:
            config_dir = "gnome-layouts"  # Default to GNOME
        
        possible_paths = [
            os.path.join(os.path.dirname(__file__), config_dir, config_file),
            os.path.expanduser(f"~/.config/{config_dir}/{config_file}"),
            f"/usr/share/{config_dir}/{config_file}"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def load_css(self):
        """Load minimal CSS for selection highlighting and improved layout"""
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
            .layout-row {
                border-radius: 8px;
                margin: 4px;
                transition: all 200ms ease;
                min-height: 70px;
            }
            .layout-row:hover {
                background-color: alpha(@theme_fg_color, 0.1);
            }
            .layout-row.selected {
                background-color: @theme_selected_bg_color;
                color: @theme_selected_fg_color;
            }
            .icon-container {
                background-color: alpha(@theme_fg_color, 0.05);
                border-radius: 12px;
                padding: 6px;
            }
            .icon-frame {
                background-color: alpha(@theme_fg_color, 0.1);
                border-radius: 8px;
                padding: 4px;
            }
            .layout-label {
                font-weight: 500;
                font-size: 13pt;
            }
        """)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

class LayoutApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id='org.bigCommunity.comm-layout-switcher-gnome')
        self.connect('activate', self.on_activate)
        
        # Add actions
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.on_about)
        self.add_action(about_action)
        
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", lambda *args: self.quit())
        self.add_action(quit_action)
    
    def on_activate(self, app):
        win = LayoutSwitcher(app)
        win.present()
    
    def on_about(self, action, param):
        """Show about dialog"""
        about_dialog = Adw.AboutWindow()
        
        # Set transient parent
        active_window = self.get_active_window()
        if active_window:
            about_dialog.set_transient_for(active_window)
        
        # Set application information
        about_dialog.set_application_name(_("window_title"))
        about_dialog.set_version("1.0")
        about_dialog.set_developer_name("Big Community & Ari Novais")
        about_dialog.set_license_type(Gtk.License.GPL_3_0)
        about_dialog.set_comments(_("select_layout"))
        about_dialog.set_website("https://communitybig.org/")
        about_dialog.set_issue_url("https://github.com/big-comm/comm-layout-changer/issues")
        
        # Set logo icon using the correct method
        about_dialog.set_icon_name("org.bigCommunity-comm-layout-changer")
        
        # Add copyright information
        about_dialog.set_copyright("© 2022 - 2025 Big Community")
        
        # Show the about dialog
        about_dialog.present()

if __name__ == "__main__":
    app = LayoutApp()
    app.run(sys.argv)
