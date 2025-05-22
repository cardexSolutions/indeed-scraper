import os
import json

def create_proxy_extension(proxy_host, proxy_port, proxy_user, proxy_pass, out_dir="proxy_ext"):
    os.makedirs(out_dir, exist_ok=True)

    # Manifest.json for Manifest V3
    manifest = {
        "name": "Chrome Proxy",
        "version": "1.0",
        "manifest_version": 3,
        "permissions": [
            "proxy",
            "storage",
            "webRequest",
            "webRequestAuthProvider",
            "declarativeNetRequestWithHostAccess"
        ],
        "host_permissions": ["<all_urls>"],
        "background": {
            "service_worker": "background.js"
        }
    }

    # Write manifest.json
    with open(os.path.join(out_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)

    # Background.js
    background_js = f"""
        chrome.runtime.onInstalled.addListener(() => {{
            const config = {{
                mode: "fixed_servers",
                rules: {{
                    singleProxy: {{
                        scheme: "http",
                        host: "{proxy_host}",
                        port: {int(proxy_port)}
                    }},
                    bypassList: ["localhost"]
                }}
            }};
            chrome.proxy.settings.set({{ value: config, scope: "regular" }}, function () {{}});
        }});

        chrome.webRequest.onAuthRequired.addListener(
            function(details) {{
                return {{
                    authCredentials: {{
                        username: "{proxy_user}",
                        password: "{proxy_pass}"
                    }}
                }};
            }},
            {{ urls: ["<all_urls>"] }},
            ["blocking"]
        );
    """

    # Write background.js
    with open(os.path.join(out_dir, "background.js"), "w") as f:
        f.write(background_js)

    return out_dir
