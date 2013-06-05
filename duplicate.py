import sublime, sublime_plugin
import shopify
import os

theme_dirs = ['Layout', 'Templates', 'Templates/Customers', 'Snippets', 'Assets', 'Config']

class ExampleCommand(sublime_plugin.EventListener):

    def on_post_save(self, view):
        print view.file_name()
        print 'saved'

#window.run_command('theme', {'shop_url' : "heller-sawayn5574.myshopify.com", 'shop_token' : "xxxxxxxxxxxxxxxxxxxxxx"})
class ThemeCommand(sublime_plugin.WindowCommand):

    def run(self, shop_url = '', shop_token = ''):
        print 'importing theme...'

        session = shopify.Session(shop_url)
        session.token = shop_token
        shopify.ShopifyResource.activate_session(session)

        main_theme = next((theme for theme in shopify.Theme.find() if theme.role == 'main'), shopify.Theme.find()[0])
        assets = shopify.Asset.find(theme_id = main_theme.id)

        theme_path = os.path.join(os.path.expanduser('~'), 'shopify_themes', shop_url, main_theme.name)
        if not os.path.exists(theme_path):
            os.makedirs(theme_path)

        for dir_name in theme_dirs:
            theme_dir_path = os.path.join(theme_path, dir_name)
            if not os.path.exists(theme_dir_path):
                os.makedirs(theme_dir_path)

        for asset in assets:
            print 'importing ' + asset.id
            asset_resource = shopify.Asset.find(asset.id)
            if 'image' in asset_resource.content_type:
                continue

            asset_file_path = os.path.join(theme_path, asset.id)
            #if not os.path.exists(asset_file_path):
            #    os.makedirs(asset_file_path)

            asset_file = open(asset_file_path, 'w+')
            asset_file.write(asset_resource.value.encode('UTF-8'))
            asset_file.close()

        print 'Theme downloaded to: ' + theme_path