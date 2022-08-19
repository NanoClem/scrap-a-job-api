from app.schemas import WebsiteNames


configs = {
    WebsiteNames.academicwork: {
        'base_url': 'https://jobs.academicwork.ch/advertsearch',
        'headers': {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'content-type': 'application/json',
            'requestverificationtoken': 'CfDJ8I3gK0kh2dFMhR7yPv-EDcRNDQjk6RhOzwN06mBMCrYjFwgKgSEr_P_hXGJVwZTy5saeuz5mNpMRHwr_XGACFabxDna5cMf0VM0lmwQdRdHzvRjhnaGTi92XFcd_SbRRBIaf9EsPaLZKtuMDGkuKc7c'
        },
        'body': {
            'SearchQueryItems': [
                {'type': 'Categories', 'value': 'IT', 'id': '20008319'},
                {'type': 'Locations', 'value': 'Genève', 'id': '20010605'},
                {'type': 'Locations', 'value': 'Lausanne', 'parent': 'Vaud', 'Id': "20010749"},
            ],
            'StartIndex': 0,
        },
        'raw_cookie': 'OptanonAlertBoxClosed=2022-07-05T23:50:05.399Z; _gcl_au=1.1.2071344892.1657065005; _ga=GA1.2.1193442835.1657065006; _hjid=18c34d47-16ac-4768-8553-748a3bc683e3; _hjSessionUser_682843=eyJpZCI6IjdiNzliNjg2LThiNGQtNTc2Ny05ZGEwLTc3YjE3Njc0MjBhZCIsImNyZWF0ZWQiOjE2NTcwNjUwMDYxNjEsImV4aXN0aW5nIjp0cnVlfQ==; _ccid=1633099688294q1z0krvy2; _gid=GA1.2.614028808.1658166817; _hjSession_682843=eyJpZCI6IjY2MzUwMWRkLWQ5MzctNGExMC05YzVlLWUxNGRmZWFhOTE1YiIsImNyZWF0ZWQiOjE2NTgxNjY4MTc1MDMsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; .AspNetCore.Antiforgery.-KRn_gW7bR0=CfDJ8I3gK0kh2dFMhR7yPv-EDcTdGJXgYz0xYgUD8ypbE10mZjAhgi57Z_-oxRavmpxlaVSFnd8DSuf7_Cwd7GzECvsmtj_SIQBQ9rNV234Y3-U-K7B7rviky4at2kaQ4DBiMtGhf1mzg4xPbLJpWiykmWQ; ARRAffinity=ec7e8bd19bfab2c59f807b76a164db45e22d9fa049dfa502c4ff57e79e9778a5; ARRAffinitySameSite=ec7e8bd19bfab2c59f807b76a164db45e22d9fa049dfa502c4ff57e79e9778a5; OptanonConsent=consentId=b7cec8f1-e58f-485f-9106-39450d01b175&datestamp=Mon+Jul+18+2022+19:59:24+GMT+0200+(heure+d’été+d’Europe+centrale)&version=6.25.0&interactionCount=1&isGpcEnabled=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001:1,C0003:1,C0002:1,C0004:1&geolocation=;&AwaitingReconsent=false'
    },
    WebsiteNames.jobup : {
        'base_url': 'https://www.jobup.ch/api/v1/public/search?location=Lausanne%20OR%20Gen%C3%A8ve&query=IT&rows=20',
        'headers': {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'content-type': 'application/json',
        },
    }
}