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
import re
import glob
import json
import shutil
import datetime
import hashlib

# Complete translation dictionary
TRANSLATIONS = {
    "en": {
        "app_name": "Community Layout Switcher",
        "window_title": "Community Layout Switcher",
        "layouts_tab": "Layouts",
        "effects_tab": "Effects",
        "themes_tab": "Themes",
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
        "effects_description": "Enhance your desktop with visual effects",
        "desktop_cube": "Desktop Cube",
        "desktop_cube_description": "Rotate your desktop on a 3D cube",
        "magic_lamp": "Magic Lamp",
        "magic_lamp_description": "Animated window minimizing effect",
        "windows_effects": "Windows Effects",
        "windows_effects_description": "Additional window animations",
        "desktop_icons": "Desktop Icons",
        "desktop_icons_description": "Add icons to your desktop",
        "extension_settings": "Extension Settings",
        "open_settings": "Open Settings",
        "not_installed": "Not installed",
        "install_extension": "Install Extension",
        "enable": "Enable",
        "disable": "Disable",
        "themes_description": "Customize your desktop appearance",
        "gtk_theme": "GTK Theme",
        "icon_theme": "Icon Theme",
        "shell_theme": "Shell Theme",
        "apply_theme": "Apply Theme",
        "no_themes_found": "No themes found",
        "license": "GPL-3.0 License",
        "gnome_only": "This feature is only available on GNOME",
        "user_theme_required": "User Themes extension is required to apply shell themes",
        "install_user_theme": "Install User Themes Extension",
        "theme_applied": "{theme_type} theme applied successfully",
        "error_applying_theme": "Error applying theme: {error}",
        "cancel": "Cancel",
        "applying_shell": "Applying shell theme {theme}...",
        "success_shell": "Successfully applied shell theme {theme}",
        "error_shell": "Error applying shell theme: {error}",
        "applying_gtk": "Applying GTK theme {theme}...",
        "success_gtk": "Successfully applied GTK theme {theme}",
        "error_gtk": "Error applying GTK theme: {error}",
        "applying_icons": "Applying icon theme {theme}...",
        "success_icons": "Successfully applied icon theme {theme}",
        "error_icons": "Error applying icon theme: {error}",
        "restart_required": "Restart may be required for changes to take effect",
        "shell_theme_restart": "Restart GNOME Shell to see the changes",
        "gtk_theme_restart": "Restart applications to see the changes",
        "icon_theme_restart": "Restart applications to see the changes",
        "about_title": "About Community Layout Switcher",
        "about_description": "Customize your GNOME desktop appearance",
        "quit_confirm": "Are you sure you want to quit?",
        "quit_confirm_title": "Quit Community Layout Switcher",
        "intro_title": "Welcome to Community Layout Switcher",
        "intro_message": "This tool allows you to customize your GNOME desktop with different layouts, effects, and themes. Before making changes, we recommend creating a backup of your current settings.",
        "intro_dont_show": "Don't show this again",
        "backup_created": "Backup created successfully",
        "backup_error": "Error creating backup: {error}",
        "backup_before_apply": "Create backup before applying layout?",
        "backup_restore": "Restore from backup",
        "backup_restore_title": "Restore Previous Settings",
        "backup_restore_message": "Are you sure you want to restore your previous settings? This will undo any changes made since the last backup.",
        "backup_restore_success": "Settings restored successfully",
        "backup_restore_error": "Error restoring backup: {error}",
        "test_layout": "Test Layout",
        "test_layout_title": "Test Layout",
        "test_layout_message": "Do you want to test this layout before applying it permanently? You can revert changes if needed.",
        "test_layout_keep": "Keep Changes",
        "test_layout_revert": "Revert Changes",
        "extensions_disabled": "GNOME Shell extensions are disabled",
        "extensions_enable_prompt": "Do you want to enable GNOME Shell extensions to apply this layout? Some layouts require extensions to function properly.",
        "extensions_enabled_success": "GNOME Shell extensions have been enabled. A restart of GNOME Shell may be required for changes to take effect.",
        "extensions_enable_error": "Error enabling GNOME Shell extensions: {error}"
    },
    "es": {
        "app_name": "Community Layout Switcher",
        "window_title": "Community Layout Switcher",
        "layouts_tab": "Diseños",
        "effects_tab": "Efectos",
        "themes_tab": "Temas",
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
        "effects_description": "Mejora tu escritorio con efectos visuales",
        "desktop_cube": "Cubo de Escritorio",
        "desktop_cube_description": "Rota tu escritorio en un cubo 3D",
        "magic_lamp": "Lámpara Mágica",
        "magic_lamp_description": "Efecto animado de minimización de ventanas",
        "windows_effects": "Efectos de Ventanas",
        "windows_effects_description": "Animaciones adicionales de ventanas",
        "desktop_icons": "Iconos del Escritorio",
        "desktop_icons_description": "Añade iconos a tu escritorio",
        "extension_settings": "Configuración de Extensiones",
        "open_settings": "Abrir Configuración",
        "not_installed": "No instalado",
        "install_extension": "Instalar Extensión",
        "enable": "Activar",
        "disable": "Desactivar",
        "themes_description": "Personaliza la apariencia de tu escritorio",
        "gtk_theme": "Tema GTK",
        "icon_theme": "Tema de Iconos",
        "shell_theme": "Tema del Shell",
        "apply_theme": "Aplicar Tema",
        "no_themes_found": "No se encontraron temas",
        "license": "Licencia GPL-3.0",
        "gnome_only": "Esta función solo está disponible en GNOME",
        "user_theme_required": "Se requiere la extensión User Themes para aplicar temas del shell",
        "install_user_theme": "Instalar Extensión User Themes",
        "theme_applied": "Tema {theme_type} aplicado con éxito",
        "error_applying_theme": "Error al aplicar el tema: {error}",
        "cancel": "Cancelar",
        "applying_shell": "Aplicando tema del shell {theme}...",
        "success_shell": "Tema del shell {theme} aplicado con éxito",
        "error_shell": "Error al aplicar el tema del shell: {error}",
        "applying_gtk": "Aplicando tema GTK {theme}...",
        "success_gtk": "Tema GTK {theme} aplicado con éxito",
        "error_gtk": "Error al aplicar el tema GTK: {error}",
        "applying_icons": "Aplicando tema de iconos {theme}...",
        "success_icons": "Tema de iconos {theme} aplicado con éxito",
        "error_icons": "Error al aplicar el tema de iconos: {error}",
        "restart_required": "Es posible que sea necesario reiniciar para que los cambios surtan efecto",
        "shell_theme_restart": "Reinicie GNOME Shell para ver los cambios",
        "gtk_theme_restart": "Reinicie las aplicaciones para ver los cambios",
        "icon_theme_restart": "Reinicie las aplicaciones para ver los cambios",
        "about_title": "Acerca de Community Layout Switcher",
        "about_description": "Personaliza la apariencia de tu escritorio GNOME",
        "quit_confirm": "¿Estás seguro de que quieres salir?",
        "quit_confirm_title": "Salir de Community Layout Switcher",
        "intro_title": "Bienvenido a Community Layout Switcher",
        "intro_message": "Esta herramienta te permite personalizar tu escritorio GNOME con diferentes diseños, efectos y temas. Antes de realizar cambios, te recomendamos crear una copia de seguridad de tu configuración actual.",
        "intro_dont_show": "No mostrar esto de nuevo",
        "backup_created": "Copia de seguridad creada exitosamente",
        "backup_error": "Error al crear copia de seguridad: {error}",
        "backup_before_apply": "¿Crear copia de seguridad antes de aplicar el diseño?",
        "backup_restore": "Restaurar desde copia de seguridad",
        "backup_restore_title": "Restaurar Configuración Anterior",
        "backup_restore_message": "¿Estás seguro de que quieres restaurar tu configuración anterior? Esto deshará cualquier cambio realizado desde la última copia de seguridad.",
        "backup_restore_success": "Configuración restaurada exitosamente",
        "backup_restore_error": "Error al restaurar copia de seguridad: {error}",
        "test_layout": "Probar Diseño",
        "test_layout_title": "Probar Diseño",
        "test_layout_message": "¿Quieres probar este diseño antes de aplicarlo permanentemente? Puedes revertir los cambios si es necesario.",
        "test_layout_keep": "Mantener Cambios",
        "test_layout_revert": "Revertir Cambios",
        "extensions_disabled": "Las extensiones de GNOME Shell están deshabilitadas",
        "extensions_enable_prompt": "¿Quieres habilitar las extensiones de GNOME Shell para aplicar este diseño? Algunos diseños requieren extensiones para funcionar correctamente.",
        "extensions_enabled_success": "Las extensiones de GNOME Shell han sido habilitadas. Es posible que sea necesario reiniciar GNOME Shell para que los cambios surtan efecto.",
        "extensions_enable_error": "Error al habilitar las extensiones de GNOME Shell: {error}"
    },
    "fr": {
        "app_name": "Community Layout Switcher",
        "window_title": "Community Layout Switcher",
        "layouts_tab": "Dispositions",
        "effects_tab": "Effets",
        "themes_tab": "Thèmes",
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
        "effects_description": "Améliorez votre bureau avec des effets visuels",
        "desktop_cube": "Cube de Bureau",
        "desktop_cube_description": "Faites pivoter votre bureau sur un cube 3D",
        "magic_lamp": "Lampe Magique",
        "magic_lamp_description": "Effet animé de réduction des fenêtres",
        "windows_effects": "Effets de Fenêtres",
        "windows_effects_description": "Animations de fenêtres supplémentaires",
        "desktop_icons": "Icônes du Bureau",
        "desktop_icons_description": "Ajoutez des icônes à votre bureau",
        "extension_settings": "Paramètres d'Extension",
        "open_settings": "Ouvrir les Paramètres",
        "not_installed": "Non installé",
        "install_extension": "Installer l'Extension",
        "enable": "Activer",
        "disable": "Désactiver",
        "themes_description": "Personnalisez l'apparence de votre bureau",
        "gtk_theme": "Thème GTK",
        "icon_theme": "Thème d'Icônes",
        "shell_theme": "Thème du Shell",
        "apply_theme": "Appliquer le Thème",
        "no_themes_found": "Aucun thème trouvé",
        "license": "Licence GPL-3.0",
        "gnome_only": "Cette fonctionnalité n'est disponible que sur GNOME",
        "user_theme_required": "L'extension User Themes est requise pour appliquer les thèmes du shell",
        "install_user_theme": "Installer l'extension User Themes",
        "theme_applied": "Thème {theme_type} appliqué avec succès",
        "error_applying_theme": "Erreur lors de l'application du thème: {error}",
        "cancel": "Annuler",
        "applying_shell": "Application du thème du shell {theme}...",
        "success_shell": "Thème du shell {theme} appliqué avec succès",
        "error_shell": "Erreur lors de l'application du thème du shell: {error}",
        "applying_gtk": "Application du thème GTK {theme}...",
        "success_gtk": "Thème GTK {theme} appliqué avec succès",
        "error_gtk": "Erreur lors de l'application du thème GTK: {error}",
        "applying_icons": "Application du thème d'icônes {theme}...",
        "success_icons": "Thème d'icônes {theme} appliqué avec succès",
        "error_icons": "Erreur lors de l'application du thème d'icônes: {error}",
        "restart_required": "Un redémarrage peut être nécessaire pour que les modifications prennent effet",
        "shell_theme_restart": "Redémarrez GNOME Shell pour voir les modifications",
        "gtk_theme_restart": "Redémarrez les applications pour voir les modifications",
        "icon_theme_restart": "Redémarrez les applications pour voir les modifications",
        "about_title": "À propos de Community Layout Switcher",
        "about_description": "Personnalisez l'apparence de votre bureau GNOME",
        "quit_confirm": "Êtes-vous sûr de vouloir quitter?",
        "quit_confirm_title": "Quitter Community Layout Switcher",
        "intro_title": "Bienvenue dans Community Layout Switcher",
        "intro_message": "Cet outil vous permet de personnaliser votre bureau GNOME avec différentes dispositions, effets et thèmes. Avant d'apporter des modifications, nous vous recommandons de créer une sauvegarde de vos paramètres actuels.",
        "intro_dont_show": "Ne plus afficher",
        "backup_created": "Sauvegarde créée avec succès",
        "backup_error": "Erreur lors de la création de la sauvegarde: {error}",
        "backup_before_apply": "Créer une sauvegarde avant d'appliquer la disposition?",
        "backup_restore": "Restaurer depuis la sauvegarde",
        "backup_restore_title": "Restaurer les paramètres précédents",
        "backup_restore_message": "Êtes-vous sûr de vouloir restaurer vos paramètres précédents? Cela annulera toutes les modifications apportées depuis la dernière sauvegarde.",
        "backup_restore_success": "Paramètres restaurés avec succès",
        "backup_restore_error": "Erreur lors de la restauration de la sauvegarde: {error}",
        "test_layout": "Tester la disposition",
        "test_layout_title": "Tester la disposition",
        "test_layout_message": "Voulez-vous tester cette disposition avant de l'appliquer de manière permanente? Vous pouvez annuler les modifications si nécessaire.",
        "test_layout_keep": "Garder les modifications",
        "test_layout_revert": "Annuler les modifications",
        "extensions_disabled": "Les extensions GNOME Shell sont désactivées",
        "extensions_enable_prompt": "Voulez-vous activer les extensions GNOME Shell pour appliquer cette disposition? Certaines dispositions nécessitent des extensions pour fonctionner correctement.",
        "extensions_enabled_success": "Les extensions GNOME Shell ont été activées. Un redémarrage de GNOME Shell peut être nécessaire pour que les modifications prennent effet.",
        "extensions_enable_error": "Erreur lors de l'activation des extensions GNOME Shell: {error}"
    },
    "de": {
        "app_name": "Community Layout Switcher",
        "window_title": "Community Layout Switcher",
        "layouts_tab": "Layouts",
        "effects_tab": "Effekte",
        "themes_tab": "Themen",
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
        "effects_description": "Verbessere deinen Desktop mit visuellen Effekten",
        "desktop_cube": "Desktop-Würfel",
        "desktop_cube_description": "Drehe deinen Desktop auf einem 3D-Würfel",
        "magic_lamp": "Magische Lampe",
        "magic_lamp_description": "Animierter Fensterminimierungseffekt",
        "windows_effects": "Fenstereffekte",
        "windows_effects_description": "Zusätzliche Fensteranimationen",
        "desktop_icons": "Desktop-Symbole",
        "desktop_icons_description": "Fügen Sie Symbole zu Ihrem Desktop hinzu",
        "extension_settings": "Erweiterungseinstellungen",
        "open_settings": "Einstellungen öffnen",
        "not_installed": "Nicht installiert",
        "install_extension": "Erweiterung installieren",
        "enable": "Aktivieren",
        "disable": "Deaktivieren",
        "themes_description": "Passe das Aussehen deines Desktops an",
        "gtk_theme": "GTK-Thema",
        "icon_theme": "Symbol-Thema",
        "shell_theme": "Shell-Thema",
        "apply_theme": "Thema anwenden",
        "no_themes_found": "Keine Themen gefunden",
        "license": "GPL-3.0 Lizenz",
        "gnome_only": "Diese Funktion ist nur unter GNOME verfügbar",
        "user_theme_required": "Die User Themes-Erweiterung ist erforderlich, um Shell-Themen anzuwenden",
        "install_user_theme": "User Themes-Erweiterung installieren",
        "theme_applied": "{theme_type}-Thema erfolgreich angewendet",
        "error_applying_theme": "Fehler beim Anwenden des Themas: {error}",
        "cancel": "Abbrechen",
        "applying_shell": "Wende Shell-Thema {theme} an...",
        "success_shell": "Shell-Thema {theme} erfolgreich angewendet",
        "error_shell": "Fehler beim Anwenden des Shell-Themas: {error}",
        "applying_gtk": "Wende GTK-Thema {theme} an...",
        "success_gtk": "GTK-Thema {theme} erfolgreich angewendet",
        "error_gtk": "Fehler beim Anwenden des GTK-Themas: {error}",
        "applying_icons": "Wende Symbol-Thema {theme} an...",
        "success_icons": "Symbol-Thema {theme} erfolgreich angewendet",
        "error_icons": "Fehler beim Anwenden des Symbol-Themas: {error}",
        "restart_required": "Ein Neustart kann erforderlich sein, damit die Änderungen wirksam werden",
        "shell_theme_restart": "Starten Sie GNOME Shell neu, um die Änderungen zu sehen",
        "gtk_theme_restart": "Starten Sie Anwendungen neu, um die Änderungen zu sehen",
        "icon_theme_restart": "Starten Sie Anwendungen neu, um die Änderungen zu sehen",
        "about_title": "Über Community Layout Switcher",
        "about_description": "Passen Sie die Erscheinung Ihres GNOME-Desktops an",
        "quit_confirm": "Sind Sie sicher, dass Sie beenden möchten?",
        "quit_confirm_title": "Community Layout Switcher beenden",
        "intro_title": "Willkommen bei Community Layout Switcher",
        "intro_message": "Dieses Tool ermöglicht es Ihnen, Ihren GNOME-Desktop mit verschiedenen Layouts, Effekten und Themen zu personalisieren. Bevor Sie Änderungen vornehmen, empfehlen wir Ihnen, eine Sicherungskopie Ihrer aktuellen Einstellungen zu erstellen.",
        "intro_dont_show": "Nicht mehr anzeigen",
        "backup_created": "Sicherung erfolgreich erstellt",
        "backup_error": "Fehler beim Erstellen der Sicherung: {error}",
        "backup_before_apply": "Sicherung vor dem Anwenden des Layouts erstellen?",
        "backup_restore": "Aus Sicherung wiederherstellen",
        "backup_restore_title": "Vorherige Einstellungen wiederherstellen",
        "backup_restore_message": "Sind Sie sicher, dass Sie Ihre vorherigen Einstellungen wiederherstellen möchten? Dies macht alle Änderungen rückgängig, die seit der letzten Sicherung vorgenommen wurden.",
        "backup_restore_success": "Einstellungen erfolgreich wiederhergestellt",
        "backup_restore_error": "Fehler beim Wiederherstellen der Sicherung: {error}",
        "test_layout": "Layout testen",
        "test_layout_title": "Layout testen",
        "test_layout_message": "Möchten Sie dieses Layout testen, bevor Sie es dauerhaft anwenden? Sie können die Änderungen bei Bedarf rückgängig machen.",
        "test_layout_keep": "Änderungen beibehalten",
        "test_layout_revert": "Änderungen rückgängig machen",
        "extensions_disabled": "GNOME Shell-Erweiterungen sind deaktiviert",
        "extensions_enable_prompt": "Möchten Sie GNOME Shell-Erweiterungen aktivieren, um dieses Layout anzuwenden? Einige Layouts erfordern Erweiterungen, um ordnungsgemäß zu funktionieren.",
        "extensions_enabled_success": "GNOME Shell-Erweiterungen wurden aktiviert. Ein Neustart von GNOME Shell kann erforderlich sein, damit die Änderungen wirksam werden.",
        "extensions_enable_error": "Fehler beim Aktivieren der GNOME Shell-Erweiterungen: {error}"
    },
    "pt_BR": {
        "app_name": "Community Layout Switcher",
        "window_title": "Community Layout Switcher",
        "layouts_tab": "Layouts",
        "effects_tab": "Efeitos",
        "themes_tab": "Temas",
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
        "effects_description": "Melhore sua área de trabalho com efeitos visuais",
        "desktop_cube": "Cubo da Área de Trabalho",
        "desktop_cube_description": "Gire sua área de trabalho em um cubo 3D",
        "magic_lamp": "Lâmpada Mágica",
        "magic_lamp_description": "Efeito animado de minimização de janelas",
        "windows_effects": "Efeitos de Janelas",
        "windows_effects_description": "Animações de janelas adicionais",
        "desktop_icons": "Ícones da Área de Trabalho",
        "desktop_icons_description": "Adicione ícones à sua área de trabalho",
        "extension_settings": "Configurações da Extensão",
        "open_settings": "Abrir Configurações",
        "not_installed": "Não instalado",
        "install_extension": "Instalar Extensão",
        "enable": "Ativar",
        "disable": "Desativar",
        "themes_description": "Personalize a aparência da sua área de trabalho",
        "gtk_theme": "Tema GTK",
        "icon_theme": "Tema de Ícones",
        "shell_theme": "Tema do Shell",
        "apply_theme": "Aplicar Tema",
        "no_themes_found": "Nenhum tema encontrado",
        "license": "Licença GPL-3.0",
        "gnome_only": "Este recurso está disponível apenas no GNOME",
        "user_theme_required": "A extensão User Themes é necessária para aplicar temas do shell",
        "install_user_theme": "Instalar Extensão User Themes",
        "theme_applied": "Tema {theme_type} aplicado com sucesso",
        "error_applying_theme": "Erro ao aplicar o tema: {error}",
        "cancel": "Cancelar",
        "applying_shell": "Aplicando tema do shell {theme}...",
        "success_shell": "Tema do shell {theme} aplicado com sucesso",
        "error_shell": "Erro ao aplicar o tema do shell: {error}",
        "applying_gtk": "Aplicando tema GTK {theme}...",
        "success_gtk": "Tema GTK {theme} aplicado com sucesso",
        "error_gtk": "Erro ao aplicar o tema GTK: {error}",
        "applying_icons": "Aplicando tema de ícones {theme}...",
        "success_icons": "Tema de ícones {theme} aplicado com sucesso",
        "error_icons": "Erro ao aplicar o tema de ícones: {error}",
        "restart_required": "Pode ser necessário reiniciar para que as alterações tenham efeito",
        "shell_theme_restart": "Reinicie o GNOME Shell para ver as alterações",
        "gtk_theme_restart": "Reinicie os aplicativos para ver as alterações",
        "icon_theme_restart": "Reinicie os aplicativos para ver as alterações",
        "about_title": "Sobre o Community Layout Switcher",
        "about_description": "Personalize a aparência da sua área de trabalho GNOME",
        "quit_confirm": "Tem certeza de que deseja sair?",
        "quit_confirm_title": "Sair do Community Layout Switcher",
        "intro_title": "Bem-vindo ao Community Layout Switcher",
        "intro_message": "Esta ferramenta permite personalizar sua área de trabalho GNOME com diferentes layouts, efeitos e temas. Antes de fazer alterações, recomendamos criar um backup das suas configurações atuais.",
        "intro_dont_show": "Não mostrar isso novamente",
        "backup_created": "Backup criado com sucesso",
        "backup_error": "Erro ao criar backup: {error}",
        "backup_before_apply": "Criar backup antes de aplicar o layout?",
        "backup_restore": "Restaurar do backup",
        "backup_restore_title": "Restaurar Configurações Anteriores",
        "backup_restore_message": "Tem certeza de que deseja restaurar suas configurações anteriores? Isso desfará quaisquer alterações feitas desde o último backup.",
        "backup_restore_success": "Configurações restauradas com sucesso",
        "backup_restore_error": "Erro ao restaurar backup: {error}",
        "test_layout": "Testar Layout",
        "test_layout_title": "Testar Layout",
        "test_layout_message": "Deseja testar este layout antes de aplicá-lo permanentemente? Você pode reverter as alterações se necessário.",
        "test_layout_keep": "Manter Alterações",
        "test_layout_revert": "Reverter Alterações",
        "extensions_disabled": "As extensões do GNOME Shell estão desativadas",
        "extensions_enable_prompt": "Você deseja ativar as extensões do GNOME Shell para aplicar este layout? Alguns layouts requerem extensões para funcionar corretamente.",
        "extensions_enabled_success": "As extensões do GNOME Shell foram ativadas. Pode ser necessário reiniciar o GNOME Shell para que as alterações tenham efeito.",
        "extensions_enable_error": "Erro ao ativar as extensões do GNOME Shell: {error}"
    },
    "pt_PT": {
        "app_name": "Community Layout Switcher",
        "window_title": "Community Layout Switcher",
        "layouts_tab": "Esquemas",
        "effects_tab": "Efeitos",
        "themes_tab": "Temas",
        "select_layout": "Selecionar Esquema",
        "applying": "A aplicar esquema {layout}...",
        "success": "Esquema {layout} aplicado com sucesso",
        "error_config": "Erro: Ficheiro de configuração não encontrado - {file}",
        "error_applying": "Erro ao aplicar o esquema: {error}",
        "error": "Erro: {error}",
        "apply": "Aplicar Esquema",
        "about": "Sobre",
        "quit": "Sair",
        "description_layout": "Aplica o esquema {layout} à sua área de trabalho.",
        "gnome": "GNOME",
        "effects_description": "Melhore a sua área de trabalho com efeitos visuais",
        "desktop_cube": "Cubo da Área de Trabalho",
        "desktop_cube_description": "Rode a sua área de trabalho num cubo 3D",
        "magic_lamp": "Lâmpada Mágica",
        "magic_lamp_description": "Efeito animado de minimização de janelas",
        "windows_effects": "Efeitos de Janelas",
        "windows_effects_description": "Animações de janelas adicionais",
        "desktop_icons": "Ícones da Área de Trabalho",
        "desktop_icons_description": "Adicione ícones à sua área de trabalho",
        "extension_settings": "Definições da Extensão",
        "open_settings": "Abrir Definições",
        "not_installed": "Não instalado",
        "install_extension": "Instalar Extensão",
        "enable": "Ativar",
        "disable": "Desativar",
        "themes_description": "Personalize a aparência da sua área de trabalho",
        "gtk_theme": "Tema GTK",
        "icon_theme": "Tema de Ícones",
        "shell_theme": "Tema do Shell",
        "apply_theme": "Aplicar Tema",
        "no_themes_found": "Nenhum tema encontrado",
        "license": "Licença GPL-3.0",
        "gnome_only": "Esta funcionalidade está apenas disponível no GNOME",
        "user_theme_required": "A extensão User Themes é necessária para aplicar temas do shell",
        "install_user_theme": "Instalar Extensão User Themes",
        "theme_applied": "Tema {theme_type} aplicado com sucesso",
        "error_applying_theme": "Erro ao aplicar o tema: {error}",
        "cancel": "Cancelar",
        "applying_shell": "A aplicar tema do shell {theme}...",
        "success_shell": "Tema do shell {theme} aplicado com sucesso",
        "error_shell": "Erro ao aplicar o tema do shell: {error}",
        "applying_gtk": "A aplicar tema GTK {theme}...",
        "success_gtk": "Tema GTK {theme} aplicado com sucesso",
        "error_gtk": "Erro ao aplicar o tema GTK: {error}",
        "applying_icons": "A aplicar tema de ícones {theme}...",
        "success_icons": "Tema de ícones {theme} aplicado com sucesso",
        "error_icons": "Erro ao aplicar o tema de ícones: {error}",
        "restart_required": "Pode ser necessário reiniciar para que as alterações tenham efeito",
        "shell_theme_restart": "Reinicie o GNOME Shell para ver as alterações",
        "gtk_theme_restart": "Reinicie as aplicações para ver as alterações",
        "icon_theme_restart": "Reinicie as aplicações para ver as alterações",
        "about_title": "Sobre o Community Layout Switcher",
        "about_description": "Personalize a aparência da sua área de trabalho GNOME",
        "quit_confirm": "Tem certeza de que deseja sair?",
        "quit_confirm_title": "Sair do Community Layout Switcher",
        "intro_title": "Bem-vindo ao Community Layout Switcher",
        "intro_message": "Esta ferramenta permite personalizar a sua área de trabalho GNOME com diferentes esquemas, efeitos e temas. Antes de fazer alterações, recomendamos criar uma cópia de segurança das suas configurações atuais.",
        "intro_dont_show": "Não mostrar isto novamente",
        "backup_created": "Cópia de segurança criada com sucesso",
        "backup_error": "Erro ao criar cópia de segurança: {error}",
        "backup_before_apply": "Criar cópia de segurança antes de aplicar o esquema?",
        "backup_restore": "Restaurar da cópia de segurança",
        "backup_restore_title": "Restaurar Configurações Anteriores",
        "backup_restore_message": "Tem certeza de que deseja restaurar as suas configurações anteriores? Isto irá desfazer quaisquer alterações feitas desde a última cópia de segurança.",
        "backup_restore_success": "Configurações restauradas com sucesso",
        "backup_restore_error": "Erro ao restaurar cópia de segurança: {error}",
        "test_layout": "Testar Esquema",
        "test_layout_title": "Testar Esquema",
        "test_layout_message": "Deseja testar este esquema antes de o aplicar permanentemente? Pode reverter as alterações se necessário.",
        "test_layout_keep": "Manter Alterações",
        "test_layout_revert": "Reverter Alterações",
        "extensions_disabled": "As extensões do GNOME Shell estão desativadas",
        "extensions_enable_prompt": "Deseja ativar as extensões do GNOME Shell para aplicar este esquema? Alguns esquemas requerem extensões para funcionar corretamente.",
        "extensions_enabled_success": "As extensões do GNOME Shell foram ativadas. Pode ser necessário reiniciar o GNOME Shell para que as alterações tenham efeito.",
        "extensions_enable_error": "Erro ao ativar as extensões do GNOME Shell: {error}"
    }
}

# Get system language
def get_system_language():
    try:
        # Try to get the language from the locale
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
    
    # Fallback to checking environment variables
    try:
        lang = os.environ.get('LANG', '').split('.')[0]
        if lang:
            # Check if we have a translation for the full locale
            if lang in TRANSLATIONS:
                return lang
            # Extract primary language code
            primary_lang = lang.split('_')[0]
            # Check if we have a translation for the primary language
            if primary_lang in TRANSLATIONS:
                return primary_lang
    except:
        pass
    
    # Fallback to checking LANGUAGE environment variable
    try:
        lang = os.environ.get('LANGUAGE', '').split(':')[0]
        if lang:
            # Check if we have a translation for the full locale
            if lang in TRANSLATIONS:
                return lang
            # Extract primary language code
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

# Backup utility functions
def create_backup_dir():
    """Create backup directory if it doesn't exist"""
    backup_dir = os.path.expanduser("~/.config/big-appearance/backups")
    os.makedirs(backup_dir, exist_ok=True)
    return backup_dir

def create_backup():
    """Create a backup of current dconf settings"""
    try:
        backup_dir = create_backup_dir()
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"backup_{timestamp}.dconf")
        
        # Create the backup
        with open(backup_file, 'w') as f:
            subprocess.run(["dconf", "dump", "/"], stdout=f, check=True)
        
        # Create a symlink to the latest backup
        latest_backup = os.path.join(backup_dir, "latest_backup.dconf")
        if os.path.exists(latest_backup):
            os.remove(latest_backup)
        os.symlink(backup_file, latest_backup)
        
        return backup_file
    except Exception as e:
        print(f"Backup error: {e}")
        return None

def restore_backup(backup_file):
    """Restore settings from a backup file"""
    try:
        if not os.path.exists(backup_file):
            return False
        
        # Load the backup
        subprocess.run(["dconf", "load", "/"], stdin=open(backup_file, 'r'), check=True)
        return True
    except Exception as e:
        print(f"Restore error: {e}")
        return False

def get_latest_backup():
    """Get the path to the latest backup file"""
    backup_dir = create_backup_dir()
    latest_backup = os.path.join(backup_dir, "latest_backup.dconf")
    
    if os.path.exists(latest_backup):
        if os.path.islink(latest_backup):
            return os.path.realpath(latest_backup)
        return latest_backup
    
    # If no symlink, find the most recent backup
    backups = glob.glob(os.path.join(backup_dir, "backup_*.dconf"))
    if backups:
        return max(backups, key=os.path.getctime)
    
    return None

# Detect desktop environment
def detect_desktop_environment():
    desktop = os.environ.get('XDG_CURRENT_DESKTOP', '').lower()
    if 'gnome' in desktop:
        return 'gnome'
    else:
        # Fallback to checking other environment variables
        if 'GNOME_DESKTOP_SESSION_ID' in os.environ:
            return 'gnome'
        return 'gnome'  # Default to GNOME

# Extract color from theme name
def extract_color_from_theme_name(theme_name):
    color_map = {
        'blue': '#3584e4',
        'green': '#26a269',
        'yellow': '#cd9309',
        'orange': '#e66100',
        'red': '#c01c28',
        'purple': '#9141ac',
        'pink': '#d16d9e',
        'teal': '#2190a4',
        'grey': '#5e5c64',
        'gray': '#5e5c64',
        'black': '#241f31',
        'white': '#ffffff',
        'dark': '#241f31',
        'light': '#ffffff',
        'brown': '#865e3c',
        'cyan': '#00b4c8',
        'magenta': '#c061cb',
        'lime': '#2ec27e',
        'indigo': '#1c71d8'
    }
    
    theme_lower = theme_name.lower()
    for color_name, hex_code in color_map.items():
        if color_name in theme_lower:
            return hex_code
    
    # Default colors if no match
    if 'dark' in theme_lower:
        return '#241f31'
    if 'light' in theme_lower:
        return '#ffffff'
    
    # Generate a color based on the theme name hash
    hash_value = hash(theme_name)
    r = (hash_value & 0xFF0000) >> 16
    g = (hash_value & 0x00FF00) >> 8
    b = hash_value & 0x0000FF
    return f'#{r:02x}{g:02x}{b:02x}'

class BigAppearanceWindow(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title(_("app_name"))
        self.set_default_size(900, 600)
        self.set_size_request(800, 500)
        
        # Detect desktop environment
        self.desktop_env = detect_desktop_environment()
        print(f"Detected desktop environment: {self.desktop_env}")
        print(f"System language: {get_system_language()}")
        
        # Initialize state variables
        self.applying = False
        self.updating_selection = False  # Flag to prevent selection loops
        self.selected_item = None
        self.selected_type = None
        self.test_mode = False
        self.backup_created = False
        
        # Load settings
        self.settings = self.load_settings()
        
        # Create UI components
        self.create_ui()
        
        # Load CSS for styling
        self.load_css()
        
        # Connect to resize event for responsive adjustments
        self.connect("notify::default-width", self.on_resize)
        self.connect("notify::default-height", self.on_resize)
        
        # Show intro dialog if needed
        if not self.settings.get("intro_shown", False):
            self.show_intro_dialog()
    
    def load_settings(self):
        """Load application settings"""
        settings_dir = os.path.expanduser("~/.config/big-appearance")
        settings_file = os.path.join(settings_dir, "settings.json")
        
        if not os.path.exists(settings_dir):
            os.makedirs(settings_dir, exist_ok=True)
        
        if os.path.exists(settings_file):
            try:
                with open(settings_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {"intro_shown": False}
    
    def save_settings(self):
        """Save application settings"""
        settings_dir = os.path.expanduser("~/.config/big-appearance")
        settings_file = os.path.join(settings_dir, "settings.json")
        
        try:
            with open(settings_file, 'w') as f:
                json.dump(self.settings, f)
        except:
            pass
    
    def show_intro_dialog(self):
        """Show introduction dialog"""
        dialog = Adw.MessageDialog(
            transient_for=self,
            heading=_("intro_title"),
            body=_("intro_message"),
        )
        
        dialog.add_response("close", _("close"))
        dialog.set_response_appearance("close", Adw.ResponseAppearance.SUGGESTED)
        
        # Add "Don't show again" checkbox
        dont_show_check = Gtk.CheckButton(label=_("intro_dont_show"))
        dont_show_check.set_margin_top(12)
        dont_show_check.set_halign(Gtk.Align.CENTER)
        dialog.set_extra_child(dont_show_check)
        
        dialog.connect("response", self.on_intro_dialog_response, dont_show_check)
        dialog.present()
    
    def on_intro_dialog_response(self, dialog, response, dont_show_check):
        """Handle response from intro dialog"""
        if dont_show_check.get_active():
            self.settings["intro_shown"] = True
            self.save_settings()
        
        dialog.destroy()
    
    def create_ui(self):
        """Create all UI components"""
        # Create toolbar view
        toolbar_view = Adw.ToolbarView()
        
        # Create header bar
        header_bar = Adw.HeaderBar()
        toolbar_view.add_top_bar(header_bar)
        
        # Add window title
        title_label = Gtk.Label()
        title_label.set_text(_("app_name"))
        title_label.add_css_class("title-3")
        header_bar.set_title_widget(title_label)
        
        # Add menu button
        menu_button = Gtk.MenuButton()
        menu_button.set_icon_name("open-menu-symbolic")
        
        # Create menu model
        menu = Gio.Menu()
        menu.append(_("backup_restore"), "app.restore_backup")
        menu.append(_("about"), "app.about")
        menu.append(_("quit"), "app.quit")
        
        # Set menu to button
        menu_button.set_menu_model(menu)
        header_bar.pack_end(menu_button)
        
        # Create tab view for the three main sections
        self.tab_view = Adw.TabView()
        self.tab_view.set_vexpand(True)
        
        # Create tabs
        self.layouts_tab = self.create_layouts_tab()
        self.effects_tab = self.create_effects_tab()
        self.themes_tab = self.create_themes_tab()
        
        # Add tabs to tab view
        layouts_page = self.tab_view.append(self.layouts_tab)
        layouts_page.set_title(_("layouts_tab"))
        
        effects_page = self.tab_view.append(self.effects_tab)
        effects_page.set_title(_("effects_tab"))
        
        themes_page = self.tab_view.append(self.themes_tab)
        themes_page.set_title(_("themes_tab"))
        
        # Create tab bar
        tab_bar = Adw.TabBar()
        tab_bar.set_view(self.tab_view)
        tab_bar.set_autohide(False)
        
        # Create main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.append(tab_bar)
        main_box.append(self.tab_view)
        
        # Set main content
        toolbar_view.set_content(main_box)
        
        # Set toolbar view as window content
        self.set_content(toolbar_view)
    
    def create_layouts_tab(self):
        """Create the Layouts tab"""
        # Define layouts for GNOME
        layouts = [
            ("Classic", "classic.txt", "classic.svg", "view-continuous-symbolic"),
            ("Vanilla", "vanilla.txt", "vanilla.svg", "view-grid-symbolic"),
            ("G-Unity", "g-unity.txt", "g-unity.svg", "view-app-grid-symbolic"),
            ("New", "new.txt", "new.svg", "view-paged-symbolic"),
            ("Next-Gnome", "next-gnome.txt", "next-gnome.svg", "view-paged-symbolic"),
            ("Modern", "modern.txt", "modern.svg", "view-grid-symbolic")
        ]
        
        # Create main container
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        container.set_margin_start(20)
        container.set_margin_end(20)
        container.set_margin_top(20)
        container.set_margin_bottom(20)
        
        # Title
        title = Gtk.Label()
        title.set_text(_("layouts_tab"))
        title.add_css_class("title-1")
        title.set_margin_bottom(20)
        title.set_halign(Gtk.Align.START)
        container.append(title)
        
        # Description
        description = Gtk.Label()
        description.set_text(_("select_layout"))
        description.add_css_class("body")
        description.set_margin_bottom(30)
        description.set_halign(Gtk.Align.START)
        container.append(description)
        
        # Create paned widget for main layout
        paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        paned.set_position(500)
        paned.set_resize_start_child(True)
        paned.set_shrink_start_child(False)
        paned.set_resize_end_child(False)
        paned.set_shrink_end_child(False)
        
        # Create preview area
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
        
        # Buttons container
        buttons_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        buttons_box.set_halign(Gtk.Align.CENTER)
        buttons_box.set_margin_top(5)
        buttons_box.set_spacing(10)
        
        # Test button
        self.test_button = Gtk.Button(label=_("test_layout"))
        self.test_button.add_css_class("pill")
        self.test_button.set_size_request(150, 40)
        self.test_button.connect("clicked", self.on_test_layout_clicked)
        buttons_box.append(self.test_button)
        
        # Apply button
        self.apply_button = Gtk.Button(label=_("apply"))
        self.apply_button.add_css_class("suggested-action")
        self.apply_button.add_css_class("pill")
        self.apply_button.set_size_request(150, 40)
        self.apply_button.connect("clicked", self.on_apply_layout_clicked)
        buttons_box.append(self.apply_button)
        
        # Spinner for loading state
        self.spinner = Gtk.Spinner()
        self.spinner.set_size_request(20, 20)
        self.spinner.set_margin_start(10)
        self.spinner.set_visible(False)
        buttons_box.append(self.spinner)
        
        preview_card.append(buttons_box)
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
        
        paned.set_start_child(preview_container)
        
        # Create sidebar
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
        self.layout_list_box.connect("row-selected", self.on_layout_row_selected)
        
        # Create layout buttons
        self.layout_buttons = []
        for name, config_file, icon_file, fallback_icon in layouts:
            row = self.create_layout_row(name, icon_file, fallback_icon, config_file)
            self.layout_list_box.append(row)
            self.layout_buttons.append((row, name, config_file))
        
        scrolled_window.set_child(self.layout_list_box)
        sidebar_box.append(scrolled_window)
        
        paned.set_end_child(sidebar_box)
        container.append(paned)
        
        # Store layouts for later use
        self.layouts = layouts
        
        # Select first layout by default
        if layouts:
            self.select_layout_item((layouts[0][0], layouts[0][1]))
        
        return container
    
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
    
    def on_layout_row_selected(self, list_box, row):
        """Handle row selection (single click)"""
        if self.updating_selection:
            return
            
        if row is None:
            return
            
        # Get the layout data directly from the row
        name = row.layout_name
        config_file = row.config_file
        
        # Select the item
        self.select_layout_item((name, config_file))
    
    def select_layout_item(self, item):
        """Select an item and update the preview"""
        self.selected_layout_item = item
        
        # Clear previous selection
        self.clear_layout_selection()
        
        # Update preview
        name, config_file = item
        self.update_layout_preview(name)
        self.highlight_selected_layout_row(name)
    
    def update_layout_preview(self, name):
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
    
    def highlight_selected_layout_row(self, name):
        """Highlight the selected row in the list"""
        self.updating_selection = True
        
        for row, row_name, _ in self.layout_buttons:
            if row_name == name:
                row.add_css_class("selected")
                self.layout_list_box.select_row(row)
                break
        
        self.updating_selection = False
    
    def clear_layout_selection(self):
        """Clear selection from all rows"""
        self.updating_selection = True
        
        for row, _, _ in self.layout_buttons:
            row.remove_css_class("selected")
        
        self.updating_selection = False
    
    def on_test_layout_clicked(self, widget):
        """Handle test button click"""
        if self.applying or not hasattr(self, 'selected_layout_item'):
            return
        
        # Ask user if they want to test the layout
        dialog = Adw.MessageDialog(
            transient_for=self,
            heading=_("test_layout_title"),
            body=_("test_layout_message"),
        )
        
        dialog.add_response("cancel", _("cancel"))
        dialog.add_response("test", _("test_layout"))
        dialog.set_response_appearance("test", Adw.ResponseAppearance.SUGGESTED)
        
        dialog.connect("response", self.on_test_dialog_response)
        dialog.present()
    
    def on_test_dialog_response(self, dialog, response):
        """Handle response from test dialog"""
        if response == "test":
            self.test_mode = True
            self.on_apply_layout_clicked(None)
        
        dialog.destroy()
    
    def on_apply_layout_clicked(self, widget):
        """Handle apply button click"""
        if self.applying or not hasattr(self, 'selected_layout_item'):
            return
        
        # Check if GNOME Shell extensions are enabled
        if not self.check_gnome_extensions_enabled():
            self.show_extensions_enable_dialog()
            return
        
        # If not in test mode, ask for backup confirmation
        if not self.test_mode and not self.backup_created:
            dialog = Adw.MessageDialog(
                transient_for=self,
                heading=_("backup_before_apply"),
                body=_("backup_before_apply"),
            )
            
            dialog.add_response("skip", _("skip"))
            dialog.add_response("backup", _("backup"))
            dialog.set_response_appearance("backup", Adw.ResponseAppearance.SUGGESTED)
            
            dialog.connect("response", self.on_backup_dialog_response)
            dialog.present()
            return
        
        # Disable button and show spinner
        self.set_applying_state(True)
        
        # Start applying in a separate thread
        threading.Thread(target=self.apply_selected_layout, daemon=True).start()
    
    def on_backup_dialog_response(self, dialog, response):
        """Handle response from backup dialog"""
        if response == "backup":
            # Create backup
            backup_file = create_backup()
            if backup_file:
                self.backup_created = True
                self.show_toast(_("backup_created"))
            else:
                self.show_toast(_("backup_error").format(error=_("unknown")))
        
        # Continue with applying layout
        self.on_apply_layout_clicked(None)
        dialog.destroy()
    
    def set_applying_state(self, applying):
        """Set the applying state of the UI"""
        self.applying = applying
        self.apply_button.set_sensitive(not applying)
        self.test_button.set_sensitive(not applying)
        
        if applying:
            self.spinner.set_visible(True)
            self.spinner.start()
        else:
            self.spinner.set_visible(False)
            self.spinner.stop()
    
    def apply_selected_layout(self):
        """Apply the selected layout in a separate thread"""
        try:
            name, config_file = self.selected_layout_item
            GLib.idle_add(self.update_status, _("applying").format(layout=name))
            
            # Find config file path
            config_path = self.find_config_file(config_file)
            if not config_path:
                GLib.idle_add(self.update_status, _("error_config").format(file=config_file))
                return
            
            # Apply GNOME layout
            self.apply_gnome_layout(config_path)
            
            # Give desktop time to apply changes
            time.sleep(0.5)
            
            GLib.idle_add(self.update_status, _("success").format(layout=name))
            
            # If in test mode, show dialog to keep or revert changes
            if self.test_mode:
                self.test_mode = False
                GLib.idle_add(self.show_test_result_dialog)
        except subprocess.TimeoutExpired:
            GLib.idle_add(self.update_status, _("error_applying").format(error="Operation timed out"))
        except subprocess.CalledProcessError as e:
            GLib.idle_add(self.update_status, _("error_applying").format(error=str(e)))
        except Exception as e:
            GLib.idle_add(self.update_status, _("error").format(error=str(e)))
        finally:
            # Always reset applying state
            GLib.idle_add(self.set_applying_state, False)
    
    def show_test_result_dialog(self):
        """Show dialog to keep or revert test changes"""
        dialog = Adw.MessageDialog(
            transient_for=self,
            heading=_("test_layout_title"),
            body=_("test_layout_message"),
        )
        
        dialog.add_response("revert", _("test_layout_revert"))
        dialog.add_response("keep", _("test_layout_keep"))
        dialog.set_response_appearance("keep", Adw.ResponseAppearance.SUGGESTED)
        
        dialog.connect("response", self.on_test_result_dialog_response)
        dialog.present()
    
    def on_test_result_dialog_response(self, dialog, response):
        """Handle response from test result dialog"""
        if response == "revert":
            # Restore from backup
            backup_file = get_latest_backup()
            if backup_file:
                if restore_backup(backup_file):
                    self.show_toast(_("backup_restore_success"))
                else:
                    self.show_toast(_("backup_restore_error").format(error=_("unknown")))
        
        dialog.destroy()
    
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
    
    def update_status(self, message):
        """Update the status bar safely from any thread"""
        self.status_bar.set_label(message)
        return False  # Don't call again
    
    def check_gnome_extensions_enabled(self):
        """Check if GNOME Shell extensions are enabled"""
        try:
            # Check if extensions are disabled
            result = subprocess.run(
                ["dconf", "read", "/org/gnome/shell/disable-extensions"],
                capture_output=True,
                text=True,
                check=True
            )
            # If the key is set to 'true', extensions are disabled
            return result.stdout.strip().lower() != "true"
        except subprocess.CalledProcessError as e:
            print(f"Error checking extensions status: {e}")
            # Assume extensions are enabled if we can't check
            return True
        except Exception as e:
            print(f"Unexpected error checking extensions status: {e}")
            return True
    
    def enable_gnome_extensions(self):
        """Enable GNOME Shell extensions"""
        try:
            subprocess.run(
                ["dconf", "write", "/org/gnome/shell/disable-extensions", "false"],
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error enabling extensions: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error enabling extensions: {e}")
            return False
    
    def show_extensions_enable_dialog(self):
        """Show dialog to enable GNOME Shell extensions"""
        dialog = Adw.MessageDialog(
            transient_for=self,
            heading=_("extensions_disabled"),
            body=_("extensions_enable_prompt"),
        )
        
        dialog.add_response("cancel", _("cancel"))
        dialog.add_response("enable", _("enable"))
        dialog.set_response_appearance("enable", Adw.ResponseAppearance.SUGGESTED)
        
        dialog.connect("response", self.on_extensions_enable_dialog_response)
        dialog.present()
    
    def on_extensions_enable_dialog_response(self, dialog, response):
        """Handle response from extensions enable dialog"""
        if response == "enable":
            if self.enable_gnome_extensions():
                self.show_toast(_("extensions_enabled_success"))
                # Now, try to apply the layout again
                self.on_apply_layout_clicked(None)
            else:
                self.show_toast(_("extensions_enable_error").format(error=_("unknown")))
        
        dialog.destroy()
    
    def create_effects_tab(self):
        """Create the Effects tab"""
        # Create main container
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        container.set_margin_start(20)
        container.set_margin_end(20)
        container.set_margin_top(20)
        container.set_margin_bottom(20)
        
        # Title
        title = Gtk.Label()
        title.set_text(_("effects_tab"))
        title.add_css_class("title-1")
        title.set_margin_bottom(20)
        title.set_halign(Gtk.Align.START)
        container.append(title)
        
        # Description
        description = Gtk.Label()
        description.set_text(_("effects_description"))
        description.add_css_class("body")
        description.set_margin_bottom(30)
        description.set_halign(Gtk.Align.START)
        container.append(description)
        
        # Check if running on GNOME
        if self.desktop_env != 'gnome':
            # Show message that effects are only available on GNOME
            info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            info_box.set_halign(Gtk.Align.CENTER)
            info_box.set_valign(Gtk.Align.CENTER)
            info_box.set_vexpand(True)
            
            info_icon = Gtk.Image.new_from_icon_name("dialog-information-symbolic")
            info_icon.set_pixel_size(64)
            info_icon.set_margin_bottom(20)
            info_box.append(info_icon)
            
            info_label = Gtk.Label()
            info_label.set_text(_("gnome_only"))
            info_label.add_css_class("title-3")
            info_label.set_wrap(True)
            info_label.set_max_width_chars(30)
            info_box.append(info_label)
            
            container.append(info_box)
            return container
        
        # Create effects grid
        effects_grid = Gtk.Grid()
        effects_grid.set_row_spacing(20)
        effects_grid.set_column_spacing(20)
        effects_grid.set_halign(Gtk.Align.CENTER)
        effects_grid.set_valign(Gtk.Align.CENTER)
        effects_grid.set_vexpand(True)
        
        # Define effects with updated URLs
        effects = [
            {
                "name": _("desktop_cube"),
                "description": _("desktop_cube_description"),
                "uuid": "desktop-cube@schneegans.github.com",
                "url": "https://extensions.gnome.org/extension/4648/desktop-cube/"
            },
            {
                "name": _("magic_lamp"),
                "description": _("magic_lamp_description"),
                "uuid": "compiz-alike-magic-lamp-effect@hermes83.github.com",
                "url": "https://extensions.gnome.org/extension/3740/compiz-alike-magic-lamp-effect/"
            },
            {
                "name": _("windows_effects"),
                "description": _("windows_effects_description"),
                "uuid": "compiz-windows-effect@hermes83.github.com",
                "url": "https://extensions.gnome.org/extension/3210/compiz-windows-effect/"
            },
            {
                "name": _("desktop_icons"),
                "description": _("desktop_icons_description"),
                "uuid": "ding@rastersoft.com",
                "url": "https://extensions.gnome.org/extension/2087/desktop-icons-ng-ding/",
                "has_settings": True
            }
        ]
        
        # Create effect cards
        for i, effect in enumerate(effects):
            # Effect card
            effect_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            effect_card.add_css_class("card")
            effect_card.set_size_request(250, 220)
            
            # Effect icon
            effect_icon = Gtk.Image.new_from_icon_name("applications-graphics-symbolic")
            effect_icon.set_pixel_size(48)
            effect_icon.set_margin_top(20)
            effect_icon.set_halign(Gtk.Align.CENTER)
            effect_card.append(effect_icon)
            
            # Effect name
            effect_name = Gtk.Label()
            effect_name.set_text(effect["name"])
            effect_name.add_css_class("title-3")
            effect_name.set_margin_top(10)
            effect_name.set_halign(Gtk.Align.CENTER)
            effect_card.append(effect_name)
            
            # Effect description
            effect_description = Gtk.Label()
            effect_description.set_text(effect["description"])
            effect_description.add_css_class("body")
            effect_description.set_margin_top(5)
            effect_description.set_margin_bottom(15)
            effect_description.set_halign(Gtk.Align.CENTER)
            effect_description.set_wrap(True)
            effect_description.set_max_width_chars(20)
            effect_card.append(effect_description)
            
            # Check if extension is installed
            installed = self.check_extension_installed(effect["uuid"])
            
            if installed:
                # Check if extension is enabled
                enabled = self.check_extension_enabled(effect["uuid"])
                
                # Create toggle switch
                toggle = Gtk.Switch()
                toggle.set_active(enabled)
                toggle.set_halign(Gtk.Align.CENTER)
                toggle.set_margin_bottom(10)
                toggle.connect("notify::active", lambda switch, _, uuid=effect["uuid"]: self.toggle_extension(uuid, switch.get_active()))
                effect_card.append(toggle)
                
                # Status label
                status_label = Gtk.Label()
                status_label.set_text(_("enable") if not enabled else _("disable"))
                status_label.add_css_class("body")
                status_label.set_halign(Gtk.Align.CENTER)
                status_label.set_margin_bottom(10)
                effect_card.append(status_label)
                
                # Add settings button if extension has settings and is enabled
                if effect.get("has_settings", False) and enabled:
                    settings_button = Gtk.Button()
                    settings_button.set_icon_name("settings-symbolic")
                    settings_button.set_tooltip_text(_("extension_settings"))
                    settings_button.set_halign(Gtk.Align.CENTER)
                    settings_button.set_margin_bottom(10)
                    settings_button.connect("clicked", lambda btn, uuid=effect["uuid"]: self.open_extension_settings(uuid))
                    effect_card.append(settings_button)
            else:
                # Install button
                install_button = Gtk.Button(label=_("install_extension"))
                install_button.add_css_class("pill")
                install_button.set_margin_bottom(20)
                install_button.connect("clicked", lambda btn, url=effect["url"]: self.open_url(url))
                effect_card.append(install_button)
            
            # Add to grid
            effects_grid.attach(effect_card, i % 3, i // 3, 1, 1)
        
        container.append(effects_grid)
        
        return container
    
    def check_extension_installed(self, uuid):
        """Check if a GNOME extension is installed"""
        user_extensions = os.path.expanduser("~/.local/share/gnome-shell/extensions")
        system_extensions = "/usr/share/gnome-shell/extensions"
        
        # Check user extensions
        if os.path.exists(os.path.join(user_extensions, uuid)):
            return True
        
        # Check system extensions
        if os.path.exists(os.path.join(system_extensions, uuid)):
            return True
        
        return False
    
    def check_extension_enabled(self, uuid):
        """Check if a GNOME extension is enabled"""
        try:
            # Get list of enabled extensions
            result = subprocess.run(
                ["gsettings", "get", "org.gnome.shell", "enabled-extensions"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse the list
            enabled_extensions = result.stdout.strip().strip("[]").replace("'", "").split(", ")
            
            # Check if our extension is in the list
            return uuid in enabled_extensions
        except:
            return False
    
    def toggle_extension(self, uuid, enable):
        """Enable or disable a GNOME extension"""
        try:
            # Get current list of enabled extensions
            result = subprocess.run(
                ["gsettings", "get", "org.gnome.shell", "enabled-extensions"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse the list
            enabled_extensions = result.stdout.strip().strip("[]").replace("'", "").split(", ")
            
            if enable:
                # Add extension to list if not already there
                if uuid not in enabled_extensions:
                    enabled_extensions.append(uuid)
            else:
                # Remove extension from list
                if uuid in enabled_extensions:
                    enabled_extensions.remove(uuid)
            
            # Set the new list
            new_list = "@as [" + ", ".join([f"'{ext}'" for ext in enabled_extensions if ext]) + "]"
            subprocess.run(
                ["gsettings", "set", "org.gnome.shell", "enabled-extensions", new_list],
                check=True
            )
            
            # Show notification
            self.show_toast(f"{uuid} {'enabled' if enable else 'disabled'}")
            
        except subprocess.CalledProcessError as e:
            self.show_toast(f"Error toggling extension: {str(e)}")
    
    def open_extension_settings(self, uuid):
        """Open the settings for a GNOME extension"""
        try:
            # Try to open the extension settings directly
            subprocess.run(["gnome-extensions-app", "prefs", uuid], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Fallback to opening the extensions app
            try:
                subprocess.run(["gnome-extensions-app"], check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Last resort: open extensions.gnome.org
                self.open_url(f"https://extensions.gnome.org/extension/{uuid.split('@')[0]}/")
    
    def open_url(self, url):
        """Open a URL in the default browser"""
        subprocess.run(["xdg-open", url], check=True)
    
    def create_themes_tab(self):
        """Create the Themes tab"""
        # Create main container
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        container.set_margin_start(20)
        container.set_margin_end(20)
        container.set_margin_top(20)
        container.set_margin_bottom(20)
        
        # Title
        title = Gtk.Label()
        title.set_text(_("themes_tab"))
        title.add_css_class("title-1")
        title.set_margin_bottom(20)
        title.set_halign(Gtk.Align.START)
        container.append(title)
        
        # Description
        description = Gtk.Label()
        description.set_text(_("themes_description"))
        description.add_css_class("body")
        description.set_margin_bottom(30)
        description.set_halign(Gtk.Align.START)
        container.append(description)
        
        # Create theme categories
        theme_notebook = Gtk.Notebook()
        theme_notebook.set_vexpand(True)
        
        # GTK Themes
        gtk_themes_page = self.create_theme_page("gtk")
        gtk_themes_label = Gtk.Label(label=_("gtk_theme"))
        theme_notebook.append_page(gtk_themes_page, gtk_themes_label)
        
        # Icon Themes
        icon_themes_page = self.create_theme_page("icons")
        icon_themes_label = Gtk.Label(label=_("icon_theme"))
        theme_notebook.append_page(icon_themes_page, icon_themes_label)
        
        # Shell Themes
        shell_themes_page = self.create_theme_page("shell")
        shell_themes_label = Gtk.Label(label=_("shell_theme"))
        theme_notebook.append_page(shell_themes_page, shell_themes_label)
        
        container.append(theme_notebook)
        
        return container
    
    def create_theme_page(self, theme_type):
        """Create a theme page for a specific type"""
        # Create scrolled window
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_vexpand(True)
        
        # Create flow box for themes
        flow_box = Gtk.FlowBox()
        flow_box.set_selection_mode(Gtk.SelectionMode.SINGLE)
        flow_box.set_max_children_per_line(4)
        flow_box.set_min_children_per_line(2)
        flow_box.set_halign(Gtk.Align.CENTER)
        flow_box.set_valign(Gtk.Align.START)
        flow_box.set_row_spacing(20)
        flow_box.set_column_spacing(20)
        
        # Get themes based on type
        themes = self.get_themes(theme_type)
        
        if not themes:
            # No themes found message
            no_themes_label = Gtk.Label()
            no_themes_label.set_text(_("no_themes_found"))
            no_themes_label.add_css_class("title-3")
            no_themes_label.set_margin_top(50)
            no_themes_label.set_halign(Gtk.Align.CENTER)
            flow_box.append(no_themes_label)
        else:
            # Create theme cards
            for theme_name, theme_path in themes:
                theme_card = self.create_theme_card(theme_name, theme_path, theme_type)
                flow_box.append(theme_card)
        
        scrolled_window.set_child(flow_box)
        return scrolled_window
    
    def create_theme_card(self, theme_name, theme_path, theme_type):
        """Create a theme card"""
        # Create card container
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        card.add_css_class("card")
        card.set_size_request(200, 200)
        card.set_margin_start(10)
        card.set_margin_end(10)
        card.set_margin_top(10)
        card.set_margin_bottom(10)
        
        # Extract color from theme name
        color = extract_color_from_theme_name(theme_name)
        
        # Create color circle
        color_circle = Gtk.DrawingArea()
        color_circle.set_size_request(80, 80)
        color_circle.set_halign(Gtk.Align.CENTER)
        color_circle.set_margin_top(20)
        color_circle.set_draw_func(self.draw_color_circle, color)
        card.append(color_circle)
        
        # Theme name
        name_label = Gtk.Label()
        name_label.set_text(theme_name)
        name_label.add_css_class("title-4")
        name_label.set_margin_top(15)
        name_label.set_halign(Gtk.Align.CENTER)
        name_label.set_ellipsize(Pango.EllipsizeMode.END)
        name_label.set_max_width_chars(15)
        card.append(name_label)
        
        # Apply button
        apply_button = Gtk.Button(label=_("apply_theme"))
        apply_button.add_css_class("pill")
        apply_button.set_margin_top(15)
        apply_button.set_margin_bottom(20)
        apply_button.set_halign(Gtk.Align.CENTER)
        apply_button.connect("clicked", lambda btn: self.apply_theme(theme_name, theme_type))
        card.append(apply_button)
        
        return card
    
    def draw_color_circle(self, drawing_area, ctx, width, height, color):
        """Draw a color circle"""
        # Set background color
        ctx.set_source_rgb(int(color[1:3], 16)/255, int(color[3:5], 16)/255, int(color[5:7], 16)/255)
        
        # Draw circle
        ctx.arc(width/2, height/2, min(width, height)/2 - 5, 0, 2 * 3.14159)
        ctx.fill()
    
    def get_themes(self, theme_type):
        """Get available themes of a specific type"""
        themes = []
        
        # Define search paths based on theme type
        if theme_type == "gtk" or theme_type == "shell":
            search_paths = [
                os.path.expanduser("~/.themes"),
                "/usr/local/share/themes",
                "/usr/share/themes"
            ]
        elif theme_type == "icons":
            search_paths = [
                os.path.expanduser("~/.icons"),
                "/usr/local/share/icons",
                "/usr/share/icons"
            ]
        else:
            return themes
        
        # Check all search paths
        for search_path in search_paths:
            if not os.path.exists(search_path):
                continue
                
            # Get all theme directories
            for theme_dir in os.listdir(search_path):
                theme_path = os.path.join(search_path, theme_dir)
                
                # Skip if not a directory
                if not os.path.isdir(theme_path):
                    continue
                
                # Check based on theme type
                if theme_type == "gtk":
                    # Check for gtk-3.0 or gtk-2.0 directory
                    if os.path.exists(os.path.join(theme_path, "gtk-3.0")) or \
                       os.path.exists(os.path.join(theme_path, "gtk-2.0")):
                        themes.append((theme_dir, theme_path))
                
                elif theme_type == "icons":
                    # Check for index.theme file
                    if os.path.exists(os.path.join(theme_path, "index.theme")):
                        themes.append((theme_dir, theme_path))
                
                elif theme_type == "shell":
                    # Check for gnome-shell directory
                    shell_dir = os.path.join(theme_path, "gnome-shell")
                    if os.path.exists(shell_dir):
                        # Check for required files
                        if (os.path.exists(os.path.join(shell_dir, "gnome-shell.css")) or
                            os.path.exists(os.path.join(shell_dir, "gnome-shell.gresource"))):
                            themes.append((theme_dir, theme_path))
        
        # Remove duplicates and sort
        themes = list(set(themes))
        themes.sort(key=lambda x: x[0].lower())
        
        return themes
    
    def apply_theme(self, theme_name, theme_type):
        """Apply a theme using gsettings"""
        # Set the selected item and type for compatibility with the provided code
        self.selected_item = theme_name
        self.selected_type = theme_type
        
        # Start applying in a separate thread
        threading.Thread(target=self._apply_theme_thread, daemon=True).start()
    
    def _apply_theme_thread(self):
        """Apply the selected theme in a separate thread"""
        try:
            if self.selected_type == "shell":
                theme_name = self.selected_item
                print(f"Applying shell theme: {theme_name}")
                GLib.idle_add(self.update_status, _("applying_shell").format(theme=theme_name))
                
                # Check if User Themes extension is installed and enabled
                user_theme_uuid = "user-theme@gnome-shell-extensions.gcampax.github.com"
                
                if not self.check_extension_installed(user_theme_uuid):
                    print("User Themes extension is not installed")
                    GLib.idle_add(self.show_user_theme_dialog)
                    return
                
                if not self.check_extension_enabled(user_theme_uuid):
                    print("User Themes extension is not enabled")
                    GLib.idle_add(self.show_user_theme_dialog)
                    return
                
                # Apply shell theme using dconf
                try:
                    print(f"Running: dconf write /org/gnome/shell/extensions/user-theme/name '{theme_name}'")
                    subprocess.run(
                        ["dconf", "write", "/org/gnome/shell/extensions/user-theme/name", f"'{theme_name}'"],
                        check=True
                    )
                    print("Command completed successfully")
                    
                    # Verify the setting
                    result = subprocess.run(
                        ["dconf", "read", "/org/gnome/shell/extensions/user-theme/name"],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    current_theme = result.stdout.strip().strip("'").strip('"')
                    print(f"Current shell theme after setting: {current_theme}")
                    
                    if current_theme == theme_name:
                        GLib.idle_add(self.update_status, _("success_shell").format(theme=theme_name))
                        GLib.idle_add(self.show_toast, _("shell_theme_restart"))
                    else:
                        GLib.idle_add(self.update_status, _("error_shell").format(error=f"Theme not set. Current: {current_theme}"))
                except subprocess.CalledProcessError as e:
                    print(f"Error applying shell theme: {e}")
                    GLib.idle_add(self.update_status, _("error_shell").format(error=str(e)))
                except Exception as e:
                    print(f"Unexpected error applying shell theme: {e}")
                    GLib.idle_add(self.update_status, _("error").format(error=str(e)))
            
            elif self.selected_type == "gtk":
                theme_name = self.selected_item
                GLib.idle_add(self.update_status, _("applying_gtk").format(theme=theme_name))
                
                # Apply GTK theme using dconf
                try:
                    print(f"Running: dconf write /org/gnome/desktop/interface/gtk-theme '{theme_name}'")
                    subprocess.run(
                        ["dconf", "write", "/org/gnome/desktop/interface/gtk-theme", f"'{theme_name}'"],
                        check=True
                    )
                    
                    # Verify the setting
                    result = subprocess.run(
                        ["dconf", "read", "/org/gnome/desktop/interface/gtk-theme"],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    current_theme = result.stdout.strip().strip("'").strip('"')
                    print(f"Current GTK theme after setting: {current_theme}")
                    
                    if current_theme == theme_name:
                        GLib.idle_add(self.update_status, _("success_gtk").format(theme=theme_name))
                        GLib.idle_add(self.show_toast, _("gtk_theme_restart"))
                    else:
                        GLib.idle_add(self.update_status, _("error_gtk").format(error=f"Theme not set. Current: {current_theme}"))
                except subprocess.CalledProcessError as e:
                    GLib.idle_add(self.update_status, _("error_gtk").format(error=str(e)))
                except Exception as e:
                    GLib.idle_add(self.update_status, _("error").format(error=str(e)))
            
            elif self.selected_type == "icons":
                theme_name = self.selected_item
                GLib.idle_add(self.update_status, _("applying_icons").format(theme=theme_name))
                
                # Apply icon theme using dconf
                try:
                    print(f"Running: dconf write /org/gnome/desktop/interface/icon-theme '{theme_name}'")
                    subprocess.run(
                        ["dconf", "write", "/org/gnome/desktop/interface/icon-theme", f"'{theme_name}'"],
                        check=True
                    )
                    
                    # Verify the setting
                    result = subprocess.run(
                        ["dconf", "read", "/org/gnome/desktop/interface/icon-theme"],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    current_theme = result.stdout.strip().strip("'").strip('"')
                    print(f"Current icon theme after setting: {current_theme}")
                    
                    if current_theme == theme_name:
                        GLib.idle_add(self.update_status, _("success_icons").format(theme=theme_name))
                        GLib.idle_add(self.show_toast, _("icon_theme_restart"))
                    else:
                        GLib.idle_add(self.update_status, _("error_icons").format(error=f"Theme not set. Current: {current_theme}"))
                except subprocess.CalledProcessError as e:
                    GLib.idle_add(self.update_status, _("error_icons").format(error=str(e)))
                except Exception as e:
                    GLib.idle_add(self.update_status, _("error").format(error=str(e)))
            
        except Exception as e:
            GLib.idle_add(self.update_status, _("error").format(error=str(e)))
    
    def show_user_theme_dialog(self):
        """Show dialog to install User Themes extension"""
        dialog = Adw.MessageDialog(
            transient_for=self,
            heading=_("user_theme_required"),
            body=_("user_theme_required"),
        )
        
        dialog.add_response("cancel", _("cancel"))
        dialog.add_response("install", _("install_user_theme"))
        dialog.set_response_appearance("install", Adw.ResponseAppearance.SUGGESTED)
        
        dialog.connect("response", self.on_user_theme_dialog_response)
        dialog.present()
    
    def on_user_theme_dialog_response(self, dialog, response):
        """Handle response from User Themes dialog"""
        if response == "install":
            # Open extensions.gnome.org for User Themes extension
            self.open_url("https://extensions.gnome.org/extension/19/user-themes/")
        
        dialog.destroy()
    
    def show_toast(self, message):
        """Show a toast notification"""
        toast = Adw.Toast.new(message)
        toast.set_timeout(3)
        
        # Get the toast overlay from the main window
        if hasattr(self, 'toast_overlay'):
            self.toast_overlay.add_toast(toast)
    
    def on_resize(self, widget, param):
        """Handle window resize for responsive adjustments"""
        width = self.get_width()
        
        # Adjust preview image size if in layouts tab
        if hasattr(self, 'preview_image'):
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
        """Search for config file in common locations"""
        config_dir = "layouts"  # Changed from "gnome-layouts" to "layouts"
        
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
        """Load CSS for styling"""
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
            .success {
                color: #26a269;
                font-weight: bold;
            }
            .theme-card {
                transition: all 200ms ease;
            }
            .theme-card:hover {
                transform: translateY(-5px);
            }
        """)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

class BigAppearanceApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id='org.bigappearance.app')
        self.connect('activate', self.on_activate)
        
        # Add actions
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.on_about)
        self.add_action(about_action)
        
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit)
        self.add_action(quit_action)
        
        restore_action = Gio.SimpleAction.new("restore_backup", None)
        restore_action.connect("activate", self.on_restore_backup)
        self.add_action(restore_action)
    
    def on_activate(self, app):
        win = BigAppearanceWindow(app)
        win.present()
    
    def on_about(self, action, param):
        """Show about dialog"""
        about_dialog = Adw.AboutWindow()
        
        # Set transient parent
        active_window = self.get_active_window()
        if active_window:
            about_dialog.set_transient_for(active_window)
        
        # Set application information
        about_dialog.set_application_name(_("app_name"))
        about_dialog.set_version("1.0")
        about_dialog.set_developer_name("Big Community & Ari Novais")
        about_dialog.set_license_type(Gtk.License.GPL_3_0)
        about_dialog.set_license(_("license"))
        about_dialog.set_comments(_("about_description"))
        about_dialog.set_website("https://communitybig.org/")
        about_dialog.set_issue_url("https://github.com/big-comm/comm-layout-changer/issues")
        
        # Set logo icon using the correct method
        about_dialog.set_icon_name("org.bigappearance.app")
        
        # Add copyright information
        about_dialog.set_copyright("© 2022 - 2025 Big Community")
        
        # Show the about dialog
        about_dialog.present()
    
    def on_quit(self, action, param):
        """Handle quit action with confirmation dialog"""
        dialog = Adw.MessageDialog(
            transient_for=self.get_active_window(),
            heading=_("quit_confirm_title"),
            body=_("quit_confirm"),
        )
        
        dialog.add_response("cancel", _("cancel"))
        dialog.add_response("quit", _("quit"))
        dialog.set_response_appearance("quit", Adw.ResponseAppearance.DESTRUCTIVE)
        
        dialog.connect("response", self.on_quit_dialog_response)
        dialog.present()
    
    def on_quit_dialog_response(self, dialog, response):
        """Handle response from quit confirmation dialog"""
        if response == "quit":
            self.quit()
        
        dialog.destroy()
    
    def on_restore_backup(self, action, param):
        """Handle restore backup action"""
        active_window = self.get_active_window()
        backup_file = get_latest_backup()
        
        if not backup_file:
            active_window.show_toast(_("backup_restore_error").format(error=_("No backup found")))
            return
        
        dialog = Adw.MessageDialog(
            transient_for=active_window,
            heading=_("backup_restore_title"),
            body=_("backup_restore_message"),
        )
        
        dialog.add_response("cancel", _("cancel"))
        dialog.add_response("restore", _("backup_restore"))
        dialog.set_response_appearance("restore", Adw.ResponseAppearance.SUGGESTED)
        
        dialog.connect("response", self.on_restore_dialog_response, backup_file)
        dialog.present()
    
    def on_restore_dialog_response(self, dialog, response, backup_file):
        """Handle response from restore dialog"""
        if response == "restore":
            if restore_backup(backup_file):
                self.get_active_window().show_toast(_("backup_restore_success"))
            else:
                self.get_active_window().show_toast(_("backup_restore_error").format(error=_("unknown")))
        
        dialog.destroy()

if __name__ == "__main__":
    app = BigAppearanceApp()
    app.run(sys.argv)
