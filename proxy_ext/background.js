
        chrome.runtime.onInstalled.addListener(() => {
            const config = {
                mode: "fixed_servers",
                rules: {
                    singleProxy: {
                        scheme: "http",
                        host: "geo.iproyal.com",
                        port: 12321
                    },
                    bypassList: ["localhost"]
                }
            };
            chrome.proxy.settings.set({ value: config, scope: "regular" }, function () {});
        });

        chrome.webRequest.onAuthRequired.addListener(
            function(details) {
                return {
                    authCredentials: {
                        username: "6Bk04u9eWn8IH8Ug",
                        password: "rOQtoGgpyHhSDEn3"
                    }
                };
            },
            { urls: ["<all_urls>"] },
            ["blocking"]
        );
    