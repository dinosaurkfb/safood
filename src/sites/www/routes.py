from handlers import *

handlers = [
    (r"/", HomeHandler),
    (r"/register", RegisterHandler),
    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),
    (r"/about", AboutHandler),

#    (r"/local", LocalHandler),
#    (r"/remote/jsonp/flightResult", JsonpHandler),

    (r"/additive/upload", AdditiveUploadHandler),
    (r"/additive", AdditiveHandler),
    (r"/additive/([0-9]+)/delete", AdditiveDeleteHandler),
    (r"/additive/([0-9]+)/update", AdditiveUpdateHandler),
    (r"/additive/([0-9]+)/via/user", AdditiveUserHandler),
    (r"/additive/([0-9]+)/via/hot", AdditiveHotHandler),
    (r"/additive/([0-9]+)/via/mine", AdditiveMineHandler),
    (r"/additive/([0-9]+)", AdditiveHandler),
    (r"/additive/search", AdditiveSearchHandler),
    (r"/additives/hot", HotAdditivesHandler),
    (r"/additives/latest", LatestAdditivesHandler),

    (r"/food", FoodHandler),
    (r"/food/([0-9]+)", FoodHandler),
    (r"/food/search", FoodSearchHandler),
    (r"/foods/hot", HotFoodsHandler),
    (r"/foods/latest", LatestFoodsHandler),

    (r"/api/additives/hot", HotAdditivesApiHandler),
    (r"/api/additives/latest", LatestAdditivesApiHandler),
    (r"/api/additive/([0-9]+)", AdditiveApiHandler),
    (r"/api/additive/search", AdditiveSearchApiHandler),
    (r"/api/additive", AdditiveApiHandler),

    (r"/api/foods/hot", HotFoodsApiHandler),
    (r"/api/foods/latest", LatestFoodsApiHandler),
    (r"/api/food/([0-9]+)", FoodApiHandler),
    (r"/api/food/search", FoodSearchApiHandler),
    (r"/api/food", FoodApiHandler),


    (r"/user/([a-zA-Z\-\_0-9]+)", UserHandler),
    (r"/user/([a-zA-Z\-\_0-9]+)/additives", UserAdditivesHandler),

    (r"/mine/additives", MineAdditivesHandler),

    (r"/settings", SettingsHandler),
    (r"/settings/profile", SettingsProfileHandler),
    (r"/settings/link", SettingsLinkHandler),
    (r"/settings/avatar", SettingsAvatarHandler),
    (r"/settings/password", SettingsPasswordHandler),
]
