class Config:
    SocialLoginInformation = {
        "google": {
            "name": "google",
            "logos": "configs/logos/google/",
            "valid_login_urls": ["accounts.google.com/"],
            "must_have_texts_in_valid_login_urls": ["client_id"]
        },
        "facebook": {
            "name": "facebook",
            "logos": "configs/logos/facebook/",
            "valid_login_urls": ["facebook.com/login", ".facebook.com/login"],
            "must_have_texts_in_valid_login_urls": ["client_id=", "app_id="]
        },
        "apple": {
            "name": "apple",
            "logos": "configs/logos/apple/",
            "valid_login_urls": ["appleid.apple.com/"],
            "must_have_texts_in_valid_login_urls": ["client_id"]
        }
    }
    AnalysisPaths = {
        "base": "./logo-recognition/analysis/"
    }
    SeleniumPaths = {
        "screenshots": "./logo-recognition/screenshots/",
        "extensions": "./logo-recognition/configs/driver/extensions/"
    }
