import xbmc
import xbmcaddon
import xbmcgui
import os
import json
import xbmcvrapi

# Get the list of installed add-ons
def get_installed_addons():
    addon_paths = []
    # Get the Kodi addon manager
    addon_manager = xbmcvrapi.AddonManager()
    # Get a list of all installed addons
    installed_addons = addon_manager.get_addons()
    for addon in installed_addons:
        addon_path = addon.getAddonPath()
        addon_paths.append(addon_path)
    return addon_paths

# Function to search addon settings
def search_addon_settings(addon_id):
    settings = xbmcaddon.Addon(id=addon_id)
    # Let's list settings as key-value pairs
    settings_data = {}
    for setting in settings.getSettingIds():
        settings_data[setting] = settings.getSetting(setting)
    return settings_data

# Create a search interface in Kodi
def create_search_interface():
    # Create the dialog for entering a search query
    dialog = xbmcgui.Dialog()
    query = dialog.input("Enter search term")
    if query:
        search_results = search_addons(query)
        display_search_results(search_results)

def search_addons(query):
    results = []
    installed_addons = get_installed_addons()

    # Search through each add-on's settings for a match
    for addon in installed_addons:
        settings_data = search_addon_settings(addon)
        for setting, value in settings_data.items():
            if query.lower() in setting.lower() or query.lower() in str(value).lower():
                results.append((addon, setting, value))
    return results

def display_search_results(results):
    dialog = xbmcgui.Dialog()
    message = ""
    for result in results:
        addon, setting, value = result
        message += f"Addon: {addon}\nSetting: {setting}\nValue: {value}\n\n"
    dialog.ok("Search Results", message)

# Main execution
if __name__ == '__main__':
    create_search_interface()
