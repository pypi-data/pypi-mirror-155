import json
import logging
import os
import uuid
from urllib.parse import unquote as urlunquote
from urllib.parse import urlsplit, urlunsplit

from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
from markdown.util import AMP_SUBSTITUTE
from mkdocs import utils
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin

log = logging.getLogger(__name__)
base_path = os.path.dirname(os.path.abspath(__file__))


class SwaggerUIPlugin(BasePlugin):
    """ Create Swagger UI with swagger-ui tag """

    config_scheme = (
        ("background", config_options.Type(str, default="")),
    )

    def on_pre_page(self, page, config, files, **kwargs):
        """ Add files for validate swagger-ui tag src """

        self.files = files
        return page

    def path_to_url(self, page_file, url):
        """ Validate swagger-ui tag src and parse url """

        scheme, netloc, path, query, fragment = urlsplit(url)

        if (scheme or netloc or not path or url.startswith('/') or url.startswith('\\')
                or AMP_SUBSTITUTE in url or '.' not in os.path.split(path)[-1]):
            # Ignore URLs unless they are a relative link to a source file.
            # AMP_SUBSTITUTE is used internally by Markdown only for email.
            # No '.' in the last part of a path indicates path does not point to a file.
            return url

        # Determine the filepath of the target.
        target_path = os.path.join(os.path.dirname(
            page_file.src_path), urlunquote(path))
        target_path = os.path.normpath(target_path).lstrip(os.sep)

        # Validate that the target exists in files collection.
        if target_path not in self.files:
            log.warning(
                f"Documentation file '{page_file.src_path}' contains Swagger UI scr to "
                f"'{target_path}' which is not found in the documentation files."
            )
            return url

        target_file = self.files.get_file_from_path(target_path)
        path = target_file.url_relative_to(page_file)
        components = (scheme, netloc, path, query, fragment)
        return urlunsplit(components)

    def on_post_page(self, output, page, config, **kwargs):
        """ Replace swagger-ui tag with iframe
            Add javascript code to update iframe height
            Create a html with Swagger UI for iframe
        """

        soup = BeautifulSoup(output, "html.parser")
        swagger_ui_list = soup.find_all("swagger-ui")
        iframe_id_list = []
        for swagger_ui_ele in swagger_ui_list:
            css_dir = utils.get_relative_url(
                utils.normalize_url("assets/stylesheets/"),
                page.url
            )
            js_dir = utils.get_relative_url(
                utils.normalize_url("assets/javascripts/"),
                page.url
            )

            cur_id = str(uuid.uuid4())[:8]
            iframe_filename = f"swagger-{cur_id}.html"
            iframe_id_list.append(cur_id)

            env = Environment(loader=FileSystemLoader(
                os.path.join(base_path, "swagger-ui")))
            template = env.get_template('swagger.html')
            openapi_spec_url = self.path_to_url(
                page.file, swagger_ui_ele.get('src', ""))
            output_from_parsed_template = template.render(
                css_dir=css_dir, js_dir=js_dir, background=self.config['background'], id=cur_id, openapi_spec_url=openapi_spec_url)

            page_dir = os.path.join(config['site_dir'], page.url)
            if not os.path.exists(page_dir):
                os.makedirs(page_dir)

            with open(os.path.join(page_dir, iframe_filename), 'w') as f:
                f.write(output_from_parsed_template)

            iframe = soup.new_tag("iframe")
            iframe['id'] = cur_id
            iframe['src'] = iframe_filename
            iframe['frameborder'] = "0"
            iframe['style'] = "overflow:hidden;width:100%;"
            iframe['width'] = "100%"
            swagger_ui_ele.replaceWith(iframe)
        if swagger_ui_list:
            js_code = soup.new_tag("script")
            js_code["type"] = "text/javascript"
            js_code.string = """
                update_swagger_ui_iframe_height = function (id) {
                    var iFrameID = document.getElementById(id);
                    if (iFrameID) {
                        full_height = (iFrameID.contentWindow.document.body.scrollHeight + 80) + "px";
                        iFrameID.height = full_height;
                        iFrameID.style.height = full_height;
                    }
                }
                var scheme = document.body.getAttribute("data-md-color-scheme")
                const options = {
                    childList: true,
                    attributes: true,
                    characterData: false,
                    subtree: false,
                    attributeFilter: ['data-md-color-scheme'],
                    attributeOldValue: false,
                    characterDataOldValue: false
                };
            """
            js_code.string += f"""
                const iframe_id_list = {json.dumps(iframe_id_list)}
            """
            js_code.string += """
                function color_scheme_callback(mutations) {
                    for (let mutation of mutations) {
                        if (mutation.attributeName === "data-md-color-scheme") {
                            scheme = document.body.getAttribute("data-md-color-scheme")
                            iframe_id_list.forEach((id) => {
                                var ele = document.getElementById(id);
                                if (ele) {
                                    if (scheme === "slate") {
                                        ele.contentWindow.enable_dark_mode();
                                    } else {
                                        ele.contentWindow.disable_dark_mode();
                                    }
                                }
                            })
                        }
                    }
                }
                observer = new MutationObserver(color_scheme_callback);
                observer.observe(document.body, options);
            """
            soup.body.append(js_code)

        return str(soup)

    def on_post_build(self, config, **kwargs):
        """ Copy Swagger UI css and js files to assets directory """

        output_base_path = os.path.join(config["site_dir"], "assets")
        css_path = os.path.join(output_base_path, "stylesheets")
        for file_name in os.listdir(os.path.join(base_path, "swagger-ui", "stylesheets")):
            utils.copy_file(os.path.join(base_path, "swagger-ui", "stylesheets", file_name), os.path.join(
                css_path, file_name))

        js_path = os.path.join(output_base_path, "javascripts")
        for file_name in os.listdir(os.path.join(base_path, "swagger-ui", "javascripts")):
            utils.copy_file(os.path.join(base_path, "swagger-ui", "javascripts", file_name), os.path.join(
                js_path, file_name))
