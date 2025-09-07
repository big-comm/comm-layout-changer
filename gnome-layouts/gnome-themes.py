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
        "window_title": "Big Community Desktop Themes GUI",
        "select_layout": "Select Desktop Layout",
        "select_shell_theme": "Select Shell Theme",
        "select_gtk_theme": "Select GTK Theme",
        "applying": "Applying {layout} layout...",
        "applying_shell": "Applying {theme} shell theme...",
        "applying_gtk": "Applying {theme} GTK theme...",
        "success": "Successfully applied {layout} layout",
        "success_shell": "Successfully applied {theme} shell theme",
        "success_gtk": "Successfully applied {theme} GTK theme",
        "error_config": "Error: Config file not found - {file}",
        "error_applying": "Error applying layout: {error}",
        "error_shell": "Error applying shell theme: {error}",
        "error_gtk": "Error applying GTK theme: {error}",
        "error": "Error: {error}",
        "no_themes": "No themes found",
        "refresh": "Refresh",
        "apply": "Apply",
        "about": "About",
        "quit": "Quit",
        "description_layout": "Apply the {layout} layout to your desktop.",
        "description_shell": "Apply the {theme} theme to your desktop shell.",
        "description_gtk": "Apply the {theme} theme to your GTK applications.",
        "gnome": "GNOME",
        "cinnamon": "Cinnamon",
        "xfce": "XFCE"
    },
    "es": {
        "window_title": "GUI de Temas de Escritorio de Big Community",
        "select_layout": "Seleccionar Diseño de Escritorio",
        "select_shell_theme": "Seleccionar Tema del Shell",
        "select_gtk_theme": "Seleccionar Tema GTK",
        "applying": "Aplicando diseño {layout}...",
        "applying_shell": "Aplicando tema de shell {theme}...",
        "applying_gtk": "Aplicando tema GTK {theme}...",
        "success": "Diseño {layout} aplicado con éxito",
        "success_shell": "Tema de shell {theme} aplicado con éxito",
        "success_gtk": "Tema GTK {theme} aplicado con éxito",
        "error_config": "Error: Archivo de configuración no encontrado - {file}",
        "error_applying": "Error al aplicar el diseño: {error}",
        "error_shell": "Error al aplicar el tema del shell: {error}",
        "error_gtk": "Error al aplicar el tema GTK: {error}",
        "error": "Error: {error}",
        "no_themes": "No se encontraron temas",
        "refresh": "Actualizar",
        "apply": "Aplicar",
        "about": "Acerca de",
        "quit": "Salir",
        "description_layout": "Aplica el diseño {layout} a tu escritorio.",
        "description_shell": "Aplica el tema {theme} a tu shell de escritorio.",
        "description_gtk": "Aplica el tema {theme} a tus aplicaciones GTK.",
        "gnome": "GNOME",
        "cinnamon": "Cinnamon",
        "xfce": "XFCE"
    },
    "fr": {
        "window_title": "GUI de Thèmes de Bureau de Big Community",
        "select_layout": "Sélectionner la disposition du bureau",
        "select_shell_theme": "Sélectionner le thème du shell",
        "select_gtk_theme": "Sélectionner le thème GTK",
        "applying": "Application de la disposition {layout}...",
        "applying_shell": "Application du thème du shell {theme}...",
        "applying_gtk": "Application du thème GTK {theme}...",
        "success": "Disposition {layout} appliquée avec succès",
        "success_shell": "Thème du shell {theme} appliqué avec succès",
        "success_gtk": "Thème GTK {theme} appliqué avec succès",
        "error_config": "Erreur: Fichier de configuration non trouvé - {file}",
        "error_applying": "Erreur lors de l'application de la disposition: {error}",
        "error_shell": "Erreur lors de l'application du thème du shell: {error}",
        "error_gtk": "Erreur lors de l'application du thème GTK: {error}",
        "error": "Erreur: {error}",
        "no_themes": "Aucun thème trouvé",
        "refresh": "Actualiser",
        "apply": "Appliquer",
        "about": "À propos",
        "quit": "Quitter",
        "description_layout": "Applique la disposition {layout} à votre bureau.",
        "description_shell": "Applique le thème {theme} à votre shell de bureau.",
        "description_gtk": "Applique le thème {theme} à vos applications GTK.",
        "gnome": "GNOME",
        "cinnamon": "Cinnamon",
        "xfce": "XFCE"
    },
    "de": {
        "window_title": "Big Community Desktop-Themen GUI",
        "select_layout": "Desktop-Layout auswählen",
        "select_shell_theme": "Shell-Thema auswählen",
        "select_gtk_theme": "GTK-Thema auswählen",
        "applying": "Wende {layout} Layout an...",
        "applying_shell": "Wende {theme} Shell-Thema an...",
        "applying_gtk": "Wende {theme} GTK-Thema an...",
        "success": "{layout} Layout erfolgreich angewendet",
        "success_shell": "{theme} Shell-Thema erfolgreich angewendet",
        "success_gtk": "{theme} GTK-Thema erfolgreich angewendet",
        "error_config": "Fehler: Konfigurationsdatei nicht gefunden - {file}",
        "error_applying": "Fehler beim Anwenden des Layouts: {error}",
        "error_shell": "Fehler beim Anwenden des Shell-Themas: {error}",
        "error_gtk": "Fehler beim Anwenden des GTK-Themas: {error}",
        "error": "Fehler: {error}",
        "no_themes": "Keine Themen gefunden",
        "refresh": "Aktualisieren",
        "apply": "Anwenden",
        "about": "Über",
        "quit": "Beenden",
        "description_layout": "Wende das {layout} Layout auf deinen Desktop an.",
        "description_shell": "Wende das {theme} Thema auf deinen Shell-Desktop an.",
        "description_gtk": "Wende das {theme} Thema auf deine GTK-Anwendungen an.",
        "gnome": "GNOME",
        "cinnamon": "Cinnamon",
        "xfce": "XFCE"
    },
    "pt_BR": {
        "window_title": "GUI de Temas de Área de Trabalho da Big Community",
        "select_layout": "Selecionar Layout da Área de Trabalho",
        "select_shell_theme": "Selecionar Tema do Shell",
        "select_gtk_theme": "Selecionar Tema GTK",
        "applying": "Aplicando layout {layout}...",
        "applying_shell": "Aplicando tema do shell {theme}...",
        "applying_gtk": "Aplicando tema GTK {theme}...",
        "success": "Layout {layout} aplicado com sucesso",
        "success_shell": "Tema do shell {theme} aplicado com sucesso",
        "success_gtk": "Tema GTK {theme} aplicado com sucesso",
        "error_config": "Erro: Arquivo de configuração não encontrado - {file}",
        "error_applying": "Erro ao aplicar o layout: {error}",
        "error_shell": "Erro ao aplicar o tema do shell: {error}",
        "error_gtk": "Erro ao aplicar o tema GTK: {error}",
        "error": "Erro: {error}",
        "no_themes": "Nenhum tema encontrado",
        "refresh": "Atualizar",
        "apply": "Aplicar",
        "about": "Sobre",
        "quit": "Sair",
        "description_layout": "Aplica o layout {layout} à sua área de trabalho.",
        "description_shell": "Aplica o tema {theme} ao shell da sua área de trabalho.",
        "description_gtk": "Aplica o tema {theme} às suas aplicações GTK.",
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
        self.set_default_size(1366, 768)
        
        # Detect desktop environment
        self.desktop_env = detect_desktop_environment()
        print(f"Detected desktop environment: {self.desktop_env}")
        
        # Define layouts based on desktop environment
        self.define_layouts()
        
        # Initialize state variables
        self.selected_item = None
        self.selected_type = None
        self.applying = False  # Flag to prevent multiple simultaneous operations
        
        # Create UI components
        self.create_ui()
        
        # Load CSS
        self.load_css()
        
        # Initialize themes
        self.refresh_shell_themes()
        self.refresh_gtk_themes()
        
        # Select first layout by default
        if self.layouts:
            self.select_item((self.layouts[0][0], self.layouts[0][1]), "layout")
    
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
                ("Classic", "classic.txt", "cinnamon-classic.png", "view-continuous-symbolic"),
                ("Modern", "modern.txt", "cinnamon-modern.png", "view-grid-symbolic")
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
        
        # Main container with responsive paned layout
        main_paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        main_paned.set_position(450)
        main_paned.set_resize_start_child(True)
        main_paned.set_shrink_start_child(False)
        
        # Create sidebar
        sidebar = self.create_sidebar()
        main_paned.set_start_child(sidebar)
        
        # Create preview area
        preview = self.create_preview_area()
        main_paned.set_end_child(preview)
        
        # Set content to toolbar view
        toolbar_view.set_content(main_paned)
        
        # Set toolbar view as window content
        self.set_content(toolbar_view)
    
    def create_sidebar(self):
        """Create the sidebar with theme selection"""
        sidebar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        sidebar_box.set_size_request(400, -1)
        sidebar_box.set_margin_start(15)
        sidebar_box.set_margin_end(15)
        sidebar_box.set_margin_top(15)
        sidebar_box.set_margin_bottom(15)
        
        # Stack for different theme types
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_vexpand(True)
        
        # Stack switcher
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(self.stack)
        stack_switcher.set_halign(Gtk.Align.CENTER)
        stack_switcher.set_margin_top(10)
        stack_switcher.set_margin_bottom(10)
        
        # Create pages
        layout_page = self.create_layout_page()
        self.stack.add_titled(layout_page, "layout", _("select_layout"))
        
        shell_theme_page = self.create_shell_theme_page()
        self.stack.add_titled(shell_theme_page, "shell", _("select_shell_theme"))
        
        gtk_theme_page = self.create_gtk_theme_page()
        self.stack.add_titled(gtk_theme_page, "gtk", _("select_gtk_theme"))
        
        # Add components to sidebar
        sidebar_box.append(stack_switcher)
        sidebar_box.append(self.stack)
        
        return sidebar_box
    
    def create_preview_area(self):
        """Create the preview area"""
        preview_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        preview_container.set_margin_start(20)
        preview_container.set_margin_end(20)
        preview_container.set_margin_top(20)
        preview_container.set_margin_bottom(20)
        preview_container.set_hexpand(True)
        preview_container.set_vexpand(True)
        
        # Preview card
        preview_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        preview_card.add_css_class("card")
        preview_card.set_halign(Gtk.Align.CENTER)
        preview_card.set_valign(Gtk.Align.CENTER)
        preview_card.set_size_request(500, 600)
        
        # Preview title
        self.preview_title = Gtk.Label()
        self.preview_title.add_css_class("title-1")
        self.preview_title.set_margin_bottom(25)
        preview_card.append(self.preview_title)
        
        # Preview image container
        image_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        image_container.set_halign(Gtk.Align.CENTER)
        image_container.set_margin_bottom(25)
        
        # Preview image
        self.preview_image = Gtk.Picture()
        self.preview_image.set_size_request(450, 300)
        self.preview_image.set_content_fit(Gtk.ContentFit.CONTAIN)
        image_container.append(self.preview_image)
        preview_card.append(image_container)
        
        # Preview description
        self.preview_description = Gtk.Label()
        self.preview_description.set_wrap(True)
        self.preview_description.set_max_width_chars(70)
        self.preview_description.set_margin_bottom(30)
        self.preview_description.set_halign(Gtk.Align.CENTER)
        preview_card.append(self.preview_description)
        
        # Apply button with spinner
        self.apply_button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.apply_button_box.set_halign(Gtk.Align.CENTER)
        
        self.apply_button = Gtk.Button(label=_("apply"))
        self.apply_button.add_css_class("suggested-action")
        self.apply_button.add_css_class("pill")
        self.apply_button.set_size_request(200, 50)
        self.apply_button.set_margin_top(10)
        self.apply_button.connect("clicked", self.on_apply_clicked)
        self.apply_button_box.append(self.apply_button)
        
        # Spinner for loading state
        self.spinner = Gtk.Spinner()
        self.spinner.set_size_request(30, 30)
        self.spinner.set_margin_start(10)
        self.spinner.set_visible(False)
        self.apply_button_box.append(self.spinner)
        
        preview_card.append(self.apply_button_box)
        
        # Add preview card to container
        preview_container.append(preview_card)
        
        # Status bar
        status_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        status_container.set_halign(Gtk.Align.CENTER)
        status_container.set_margin_top(20)
        
        self.status_bar = Gtk.Label()
        status_container.append(self.status_bar)
        preview_container.append(status_container)
        
        return preview_container
    
    def create_layout_page(self):
        """Create the layout selection page"""
        page_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        # Layout grid
        self.layout_grid = Gtk.Grid()
        self.layout_grid.set_row_spacing(20)
        self.layout_grid.set_column_spacing(20)
        self.layout_grid.set_halign(Gtk.Align.CENTER)
        
        # Create layout buttons
        for i, (name, config_file, icon_file, fallback_icon) in enumerate(self.layouts):
            # Calculate row and column for 3 columns
            row = i // 3
            col = i % 3
            
            button = self.create_theme_button(
                name, icon_file, fallback_icon,
                lambda w, n=name, c=config_file: self.select_item((n, c), "layout")
            )
            
            # Add to grid
            self.layout_grid.attach(button, col, row, 1, 1)
        
        # Add grid to scrolled window
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_child(self.layout_grid)
        scrolled.set_vexpand(True)
        page_box.append(scrolled)
        
        return page_box
    
    def create_shell_theme_page(self):
        """Create the shell theme selection page"""
        page_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        # Refresh button
        refresh_button = Gtk.Button(label=_("refresh"))
        refresh_button.add_css_class("pill")
        refresh_button.set_margin_top(15)
        refresh_button.set_margin_bottom(15)
        refresh_button.set_size_request(120, 40)
        refresh_button.connect("clicked", lambda x: self.refresh_shell_themes())
        page_box.append(refresh_button)
        
        # Shell theme grid
        self.shell_theme_grid = Gtk.Grid()
        self.shell_theme_grid.set_row_spacing(20)
        self.shell_theme_grid.set_column_spacing(20)
        self.shell_theme_grid.set_halign(Gtk.Align.CENTER)
        
        # Add grid to scrolled window
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_child(self.shell_theme_grid)
        scrolled.set_vexpand(True)
        page_box.append(scrolled)
        
        return page_box
    
    def create_gtk_theme_page(self):
        """Create the GTK theme selection page"""
        page_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        # Refresh button
        refresh_button = Gtk.Button(label=_("refresh"))
        refresh_button.add_css_class("pill")
        refresh_button.set_margin_top(15)
        refresh_button.set_margin_bottom(15)
        refresh_button.set_size_request(120, 40)
        refresh_button.connect("clicked", lambda x: self.refresh_gtk_themes())
        page_box.append(refresh_button)
        
        # GTK theme grid
        self.gtk_theme_grid = Gtk.Grid()
        self.gtk_theme_grid.set_row_spacing(20)
        self.gtk_theme_grid.set_column_spacing(20)
        self.gtk_theme_grid.set_halign(Gtk.Align.CENTER)
        
        # Add grid to scrolled window
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_child(self.gtk_theme_grid)
        scrolled.set_vexpand(True)
        page_box.append(scrolled)
        
        return page_box
    
    def create_theme_button(self, name, icon_file, fallback_icon, callback):
        """Create a standardized theme button"""
        button = Gtk.Button()
        button.set_tooltip_text(name)
        button.add_css_class("card")
        button.add_css_class("theme-button")
        
        # Create button content
        button_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        
        # Create image
        image = Gtk.Picture()
        image.set_size_request(120, 100)
        image.set_content_fit(Gtk.ContentFit.CONTAIN)
        
        # Try to load custom icon if icon_file is provided
        if icon_file:
            icon_path = self.find_icon(icon_file)
            if icon_path:
                image.set_filename(icon_path)
            else:
                # Use fallback icon
                fallback_image = Gtk.Image.new_from_icon_name(fallback_icon)
                fallback_image.set_pixel_size(80)
                image.set_paintable(fallback_image.get_paintable())
        else:
            # For themes, try to find theme-specific icon first
            theme_icon_path = self.find_theme_icon(name, fallback_icon)
            if isinstance(theme_icon_path, str) and os.path.exists(theme_icon_path):
                image.set_filename(theme_icon_path)
            else:
                # Use fallback icon
                fallback_image = Gtk.Image.new_from_icon_name(fallback_icon)
                fallback_image.set_pixel_size(80)
                image.set_paintable(fallback_image.get_paintable())
        
        # Create label
        label = Gtk.Label(label=name)
        label.set_halign(Gtk.Align.CENTER)
        label.set_max_width_chars(12)
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.add_css_class("title-4")
        
        # Add to button box
        button_box.append(image)
        button_box.append(label)
        button.set_child(button_box)
        
        # Connect callback
        button.connect("clicked", callback)
        
        return button
    
    def select_item(self, item, item_type):
        """Select an item and update the preview"""
        self.selected_item = item
        self.selected_type = item_type
        
        # Clear previous selection
        self.clear_selection()
        
        # Update preview based on type
        if item_type == "layout":
            name, config_file = item
            self.update_preview(name, "layout")
            self.highlight_selected_button(self.layout_grid, name)
        
        elif item_type == "shell":
            theme_name = item
            self.update_preview(theme_name, "shell")
            self.highlight_selected_button(self.shell_theme_grid, theme_name)
        
        elif item_type == "gtk":
            theme_name = item
            self.update_preview(theme_name, "gtk")
            self.highlight_selected_button(self.gtk_theme_grid, theme_name)
    
    def update_preview(self, name, item_type):
        """Update the preview area"""
        self.preview_title.set_text(name)
        
        # Set description based on type
        if item_type == "layout":
            self.preview_description.set_text(_("description_layout").format(layout=name))
            icon_key = "layout"
        elif item_type == "shell":
            self.preview_description.set_text(_("description_shell").format(theme=name))
            icon_key = "shell"
        else:  # gtk
            self.preview_description.set_text(_("description_gtk").format(theme=name))
            icon_key = "gtk"
        
        # Try to load preview image
        icon_path = None
        
        if item_type == "layout":
            # For layouts, check our predefined icons
            for layout in self.layouts:
                if layout[0] == name:
                    icon_path = self.find_icon(layout[2])
                    break
        else:
            # For themes, check theme directories
            icon_path = self.find_theme_icon(name, icon_key)
        
        # Set image or fallback
        if icon_path and isinstance(icon_path, str) and os.path.exists(icon_path):
            self.preview_image.set_filename(icon_path)
        else:
            # Use fallback icon based on type
            fallback_icons = {
                "layout": "view-grid-symbolic",
                "shell": "desktop-wallpaper",
                "gtk": "preferences-desktop-theme"
            }
            fallback_image = Gtk.Image.new_from_icon_name(fallback_icons.get(icon_key, "image-missing"))
            fallback_image.set_pixel_size(150)
            self.preview_image.set_paintable(fallback_image.get_paintable())
    
    def highlight_selected_button(self, grid, name):
        """Highlight the selected button in a grid"""
        for child in grid:
            if isinstance(child, Gtk.Button):
                button_box = child.get_child()
                if isinstance(button_box, Gtk.Box):
                    label = button_box.get_last_child()
                    if isinstance(label, Gtk.Label) and label.get_text() == name:
                        child.add_css_class("selected")
    
    def clear_selection(self):
        """Clear selection from all buttons"""
        for grid in [self.layout_grid, self.shell_theme_grid, self.gtk_theme_grid]:
            for child in grid:
                if isinstance(child, Gtk.Button):
                    child.remove_css_class("selected")
    
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
            elif self.selected_type == "shell":
                self.apply_shell_theme()
            elif self.selected_type == "gtk":
                self.apply_gtk_theme()
        except Exception as e:
            # Update UI on main thread
            GLib.idle_add(self.update_status, _("error").format(error=str(e)))
        finally:
            # Always reset applying state
            GLib.idle_add(self.set_applying_state, False)
    
    def get_random_wallpaper(self):
        """Get a random wallpaper from /usr/share/wallpapers"""
        wallpapers = []
        wallpaper_dir = "/usr/share/wallpapers"
        
        # Check if wallpaper directory exists
        if not os.path.exists(wallpaper_dir):
            print(f"Wallpaper directory not found: {wallpaper_dir}")
            return None
            
        print(f"Scanning wallpaper directory: {wallpaper_dir}")
        
        # Walk through the wallpaper directory recursively
        try:
            for root, dirs, files in os.walk(wallpaper_dir):
                for file in files:
                    # Check for common image extensions including .avif
                    if file.lower().endswith(('.png', '.jpg', '.jpeg', '.svg', '.bmp', '.tiff', '.webp', '.avif')):
                        wallpaper_path = os.path.join(root, file)
                        wallpapers.append(wallpaper_path)
                        print(f"Found wallpaper: {wallpaper_path}")
        except Exception as e:
            print(f"Error scanning wallpaper directory: {e}")
            return None
        
        if not wallpapers:
            print("No wallpapers found in /usr/share/wallpapers")
            return None
        
        # Return a random wallpaper
        selected = random.choice(wallpapers)
        print(f"Selected wallpaper: {selected}")
        return selected
    
    def set_wallpaper(self, wallpaper_path):
        """Set the wallpaper using gsettings"""
        try:
            # Convert path to URI
            uri = f"file://{wallpaper_path}"
            print(f"Setting wallpaper to: {uri}")
            
            # Set for both light and dark modes
            subprocess.run(
                ["gsettings", "set", "org.gnome.desktop.background", "picture-uri", uri],
                check=True, timeout=10
            )
            subprocess.run(
                ["gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark", uri],
                check=True, timeout=10
            )
            
            print("Wallpaper set successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error setting wallpaper: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error setting wallpaper: {e}")
            return False
    
    def apply_layout(self):
        """Apply the selected layout and set a random wallpaper"""
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
            
            # Set a random wallpaper
            wallpaper = self.get_random_wallpaper()
            if wallpaper:
                success = self.set_wallpaper(wallpaper)
                if not success:
                    print("Failed to set wallpaper")
            else:
                print("No wallpaper available to set")
            
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
    
    def apply_shell_theme(self):
        """Apply the selected shell theme"""
        theme_name = self.selected_item
        GLib.idle_add(self.update_status, _("applying_shell").format(theme=theme_name))
        
        try:
            # Apply shell theme based on desktop environment
            if self.desktop_env == 'gnome':
                subprocess.run(
                    ["gsettings", "set", "org.gnome.shell.extensions.user-theme", "name", theme_name],
                    check=True,
                    timeout=10
                )
            elif self.desktop_env == 'cinnamon':
                subprocess.run(
                    ["gsettings", "set", "org.cinnamon.theme", "name", theme_name],
                    check=True,
                    timeout=10
                )
            elif self.desktop_env == 'xfce':
                subprocess.run(
                    ["xfconf-query", "-c", "xfwm4", "-p", "/general/theme", "-s", theme_name],
                    check=True,
                    timeout=10
                )
            
            # Give desktop time to apply changes
            time.sleep(0.5)
            
            GLib.idle_add(self.update_status, _("success_shell").format(theme=theme_name))
        except subprocess.TimeoutExpired:
            GLib.idle_add(self.update_status, _("error_shell").format(error="Operation timed out"))
        except subprocess.CalledProcessError as e:
            GLib.idle_add(self.update_status, _("error_shell").format(error=str(e)))
        except Exception as e:
            GLib.idle_add(self.update_status, _("error").format(error=str(e)))
    
    def apply_gtk_theme(self):
        """Apply the selected GTK theme"""
        theme_name = self.selected_item
        GLib.idle_add(self.update_status, _("applying_gtk").format(theme=theme_name))
        
        try:
            # Apply GTK theme using gsettings
            subprocess.run(
                ["gsettings", "set", "org.gnome.desktop.interface", "gtk-theme", theme_name],
                check=True,
                timeout=10
            )
            
            # Give GTK time to apply changes
            time.sleep(0.5)
            
            GLib.idle_add(self.update_status, _("success_gtk").format(theme=theme_name))
        except subprocess.TimeoutExpired:
            GLib.idle_add(self.update_status, _("error_gtk").format(error="Operation timed out"))
        except subprocess.CalledProcessError as e:
            GLib.idle_add(self.update_status, _("error_gtk").format(error=str(e)))
        except Exception as e:
            GLib.idle_add(self.update_status, _("error").format(error=str(e)))
    
    def update_status(self, message):
        """Update the status bar safely from any thread"""
        self.status_bar.set_label(message)
        return False  # Don't call again
    
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
    
    def find_theme_icon(self, theme_name, theme_type):
        """Search for theme icon in project's icons directory"""
        # For shell themes, look in the project's icons directory
        if theme_type == "shell":
            # Try to find icon with theme name in icons directory
            icon_name = f"{theme_name.lower().replace(' ', '-')}.png"
            icon_path = os.path.join(os.path.dirname(__file__), "icons", icon_name)
            
            if os.path.exists(icon_path):
                return icon_path
            
            # Try with different extensions
            base_name, _ = os.path.splitext(icon_name)
            for ext in ['.png', '.jpg', '.jpeg', '.svg']:
                test_path = os.path.join(os.path.dirname(__file__), "icons", f"{base_name}{ext}")
                if os.path.exists(test_path):
                    return test_path
            
            # Try common icon names for shell themes
            common_names = ["shell.png", "gnome-shell.png", "theme.png"]
            for name in common_names:
                icon_path = os.path.join(os.path.dirname(__file__), "icons", name)
                if os.path.exists(icon_path):
                    return icon_path
        
        # For GTK themes, look for thumbnail.png in the theme directory
        elif theme_type == "gtk":
            # Check user themes first
            user_theme_dir = os.path.expanduser(f"~/.themes/{theme_name}")
            system_theme_dir = f"/usr/share/themes/{theme_name}"
            
            for theme_dir in [user_theme_dir, system_theme_dir]:
                if os.path.exists(theme_dir):
                    # Look for thumbnail.png in gtk-3.0 subdirectory
                    thumbnail_path = os.path.join(theme_dir, "gtk-3.0", "thumbnail.png")
                    if os.path.exists(thumbnail_path):
                        return thumbnail_path
                    
                    # Also check for other common image names
                    for img_name in ["preview.png", "preview.jpg", "preview.svg"]:
                        preview_path = os.path.join(theme_dir, "gtk-3.0", img_name)
                        if os.path.exists(preview_path):
                            return preview_path
        
        # Return default icon based on theme type
        if theme_type == "gtk":
            return "preferences-desktop-theme"
        else:
            return "desktop-wallpaper"
    
    def get_themes(self, theme_type):
        """Get available themes of specified type"""
        themes = []
        
        # For shell themes, check based on desktop environment
        if theme_type == "shell":
            if self.desktop_env == 'gnome':
                theme_type = "gnome-shell"
            elif self.desktop_env == 'cinnamon':
                theme_type = "cinnamon"
            elif self.desktop_env == 'xfce':
                theme_type = "xfwm4"
        
        # Check user themes
        user_theme_dir = os.path.expanduser("~/.themes")
        if os.path.exists(user_theme_dir):
            for theme_name in os.listdir(user_theme_dir):
                theme_path = os.path.join(user_theme_dir, theme_name)
                if os.path.isdir(theme_path):
                    # Check for theme-specific directory
                    theme_subdir = os.path.join(theme_path, theme_type)
                    if os.path.exists(theme_subdir):
                        themes.append(theme_name)
        
        # Check system themes
        system_theme_dir = "/usr/share/themes"
        if os.path.exists(system_theme_dir):
            for theme_name in os.listdir(system_theme_dir):
                theme_path = os.path.join(system_theme_dir, theme_name)
                if os.path.isdir(theme_path):
                    # Check for theme-specific directory
                    theme_subdir = os.path.join(theme_path, theme_type)
                    if os.path.exists(theme_subdir):
                        themes.append(theme_name)
        
        # Remove duplicates and sort
        return sorted(list(set(themes)))
    
    def get_shell_themes(self):
        """Get available shell themes based on desktop environment"""
        return self.get_themes("shell")
    
    def get_gtk_themes(self):
        """Get available GTK themes"""
        return self.get_themes("gtk-3.0")
    
    def refresh_themes(self, theme_type, grid, callback):
        """Generic method to refresh themes"""
        # Clear existing widgets
        while grid.get_first_child():
            grid.remove(grid.get_first_child())
        
        # Get available themes
        themes = self.get_themes(theme_type)
        
        if not themes:
            no_themes_label = Gtk.Label(label=_("no_themes"))
            no_themes_label.set_halign(Gtk.Align.CENTER)
            grid.attach(no_themes_label, 0, 0, 1, 1)
            return
        
        # Create theme buttons
        for i, theme_name in enumerate(themes):
            row = i // 2
            col = i % 2
            
            button = self.create_theme_button(
                theme_name,
                None,  # No specific icon file for themes
                theme_type,  # Use theme type as fallback icon
                lambda w, t=theme_name: callback(t)
            )
            
            # Add to grid
            grid.attach(button, col, row, 1, 1)
    
    def refresh_shell_themes(self):
        """Refresh the list of available Shell themes"""
        self.refresh_themes("shell", self.shell_theme_grid, lambda t: self.select_item(t, "shell"))
    
    def refresh_gtk_themes(self):
        """Refresh the list of available GTK themes"""
        self.refresh_themes("gtk-3.0", self.gtk_theme_grid, lambda t: self.select_item(t, "gtk"))
    
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
        """Load and apply CSS styling"""
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
            .theme-button {
                background-color: @card_bg_color;
                border-radius: 12px;
                padding: 15px;
                margin: 8px;
                min-width: 140px;
                min-height: 140px;
                transition: all 200ms ease;
            }
            .theme-button:hover {
                background-color: shade(@card_bg_color, 1.1);
                transform: translateY(-2px);
            }
            .theme-button:active {
                background-color: shade(@card_bg_color, 0.9);
                transform: translateY(0);
            }
            .theme-button.selected {
                background-color: @accent_bg_color;
                color: @accent_fg_color;
            }
            .card {
                background-color: @card_bg_color;
                border-radius: 16px;
                padding: 30px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .title-1 {
                font-weight: 800;
                font-size: 24pt;
            }
            .title-3 {
                font-weight: 700;
                font-size: 18pt;
            }
            .title-4 {
                font-weight: 600;
                font-size: 14pt;
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
        win = LayoutSwitcher(self)
        win.present()
    
    def on_about(self, action, param):
        """Show about dialog"""
        about_dialog = Adw.AboutWindow()
        about_dialog.set_transient_for(self.get_active_window())
        about_dialog.set_application_name(_("window_title"))
        about_dialog.set_version("1.0")
        about_dialog.set_developer_name("Big Community")
        about_dialog.set_license_type(Gtk.License.GPL_3_0)
        about_dialog.set_comments(_("select_layout"))
        about_dialog.set_website("https://example.org")
        about_dialog.set_issue_url("https://example.org/issues")
        about_dialog.present()

if __name__ == "__main__":
    app = LayoutApp()
    app.run(sys.argv)
