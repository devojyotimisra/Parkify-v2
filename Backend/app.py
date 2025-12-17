from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from application.middlewares.init_db import initialize_database
from application.middlewares.init_cache import init_cache
from application.middlewares.init_jwt import init_jwt
from application.middlewares.init_bg_jobs import initialize_bg_jobs
from application.middlewares.init_app_context import init_app_context
from application.middlewares.init_config import init_config
from application.middlewares.init_token_refresh import init_token_refresh

from application.resources.general.login_resource import LoginResource
from application.resources.general.signup_resource import SignupResource
from application.resources.admin.admin_dashboard_resource import AdminDashboardResource
from application.resources.admin.admin_parking_lot_add_resource import AdminParkingLotAddResource
from application.resources.admin.admin_parking_lot_update_resource import AdminParkingLotUpdateResource
from application.resources.admin.admin_parking_lot_delete_resource import AdminParkingLotDeleteResource
from application.resources.admin.admin_parking_spots_details_resource import AdminParkingSpotsDetailsResource
from application.resources.admin.admin_parking_spot_details_resource import AdminParkingSpotDetailsResource
from application.resources.admin.admin_users_list_resource import AdminUsersListResource
from application.resources.admin.admin_search_resource import AdminSearchResource
from application.resources.admin.admin_history_resource import AdminHistoryResource
from application.resources.admin.admin_profile_fetch_resource import AdminProfileFetchResource
from application.resources.admin.admin_profile_update_resource import AdminProfileUpdateResource

from application.resources.user.user_dashboard_resource import UserDashboardResource
from application.resources.user.user_slot_select_resource import UserSlotSelectResource
from application.resources.user.user_slot_book_resource import UserSlotBookResource
from application.resources.user.user_slot_release_resource import UserSlotReleaseResource
from application.resources.user.user_search_resource import UserSearchResource
from application.resources.user.user_history_resource import UserHistoryResource
from application.resources.user.user_profile_fetch_resource import UserProfileFetchResource
from application.resources.user.user_profile_update_resource import UserProfileUpdateResource
from application.resources.user.user_account_delete_resource import UserAccountDeleteResource
from application.resources.user.user_export_csv_resource import UserExportCSVResource


app = Flask(__name__)
api = Api(app)
cors = CORS(app, expose_headers=["X-Refresh-Token"])

init_config(app)
initialize_database(app)
init_cache(app)
init_jwt(app)
initialize_bg_jobs(app)
init_app_context(app)
init_token_refresh(app)

celery = app.celery


api.add_resource(LoginResource, '/api/login')
api.add_resource(SignupResource, '/api/signup')

api.add_resource(AdminDashboardResource, '/api/admin/dash')
api.add_resource(AdminParkingLotAddResource, '/api/admin/add_lot')
api.add_resource(AdminParkingLotUpdateResource, '/api/admin/edit_lot/<int:lot_id>')
api.add_resource(AdminParkingLotDeleteResource, '/api/admin/delete_lot/<int:lot_id>')
api.add_resource(AdminParkingSpotsDetailsResource, '/api/admin/view_spots/<int:lot_id>')
api.add_resource(AdminParkingSpotDetailsResource, '/api/admin/spot_details/<int:spot_id>')
api.add_resource(AdminUsersListResource, '/api/admin/users')
api.add_resource(AdminSearchResource, '/api/admin/search')
api.add_resource(AdminHistoryResource, '/api/admin/history')
api.add_resource(AdminProfileFetchResource, '/api/admin/profile')
api.add_resource(AdminProfileUpdateResource, '/api/admin/edit_profile')

api.add_resource(UserDashboardResource, '/api/user/dash')
api.add_resource(UserSlotSelectResource, '/api/user/select_slot/<int:lot_id>')
api.add_resource(UserSlotBookResource, '/api/user/book_slot/<int:lot_id>')
api.add_resource(UserSlotReleaseResource, '/api/user/release_slot/<int:reservation_id>')
api.add_resource(UserSearchResource, '/api/user/search')
api.add_resource(UserHistoryResource, '/api/user/history')
api.add_resource(UserProfileFetchResource, '/api/user/profile')
api.add_resource(UserProfileUpdateResource, '/api/user/edit_profile')
api.add_resource(UserAccountDeleteResource, '/api/user/delete_account')
api.add_resource(UserExportCSVResource, '/api/user/export')


if __name__ == "__main__":
    app.run()
