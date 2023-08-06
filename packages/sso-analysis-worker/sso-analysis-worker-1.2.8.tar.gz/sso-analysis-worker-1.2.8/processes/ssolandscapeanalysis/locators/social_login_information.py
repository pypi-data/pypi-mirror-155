SocialLoginInformation = {
    "Google": {
        "name": "Google",
        "valid_login_urls": ["https://accounts.google.com/"],
        "valid_login_urls_when_logged_in": ["https://accounts.google.com/"],
        "block_requests_if_logged_in": [],
        "must_have_texts_in_valid_login_urls": [["client_id"]],
        "exclude_url_starts_with": ["google.", "accounts.google.", "account.google.", "consent.google.",
                                    "developers.googleblog.com", "pki.goog", "support.google.", "patent.google.",
                                    "www.google.", "translate.google.", "maps.google.", "trends.google.",
                                    "adwords.google.", "picasa.google.", "books.google.", "edu.google.", "news.google.",
                                    "developers.google.", "mymaps.google.", "workspace.google.", "gsuite.google.",
                                    "mijnaccount.google.", "scholar.google.", "blog.google", "patents.google.",
                                    "googlegroups.", "myaccount.google.com"],
        "extra_texts": ["ورود با حساب گوگل"]
    },
    "Facebook": {
        "name": "Facebook",
        "valid_login_urls": ["https://m.facebook.com/login", "https://facebook.com/login",
                             "https://www.facebook.com/login", "https://www.facebook.com/dialog/oauth"],
        "valid_login_urls_when_logged_in": ["https://facebook.com", "https://www.facebook.com",
                                            "https://m.facebook.com"],
        "block_requests_if_logged_in": ["www.facebook.com/x/oauth/status", "facebook.com/x/oauth/status"],
        "must_have_texts_in_valid_login_urls": [["client_id=", "app_id="]],
        "exclude_url_starts_with": ["facebook.", "www.facebook.", "connect.facebook.", "developers.facebook."],
        "extra_texts": []
    },
    "Apple": {
        "name": "Apple",
        "valid_login_urls": ["https://appleid.apple.com/"],
        "valid_login_urls_when_logged_in": ["https://appleid.apple.com/"],
        "block_requests_if_logged_in": [],
        "must_have_texts_in_valid_login_urls": [["client_id"]],
        "exclude_url_starts_with": ["apple.", "appleid.apple.", "secure.apple.", "secure2.apple.",
                                    "secure2.store.apple.", "support.apple.", "music.apple.", "discussions.apple.",
                                    "www.apple.", "business.apple.", "itunes.apple."],
        "extra_texts": []
    }
}
