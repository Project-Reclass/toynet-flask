# This file is part of Toynet-Flask.
#
# Toynet-Flask is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Toynet-Flask is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Toynet-Flask.  If not, see <https://www.gnu.org/licenses/>.

from marshmallow import Schema, fields, ValidationError
from flask_restful import abort
from flask_apispec import marshal_with, MethodResource, use_kwargs
from toynet.state import State


# Schema definitions
class MiniFlaskTerminatePostReq(Schema):
    terminate = fields.Bool()


class MiniFlaskTerminatePostResp(Schema):
    terminated = fields.Bool()


class MiniFlaskTerminate(MethodResource):
    @use_kwargs(MiniFlaskTerminatePostReq)
    @marshal_with(MiniFlaskTerminatePostResp)
    def post(self, **kwargs):
        try:
            req = MiniFlaskTerminatePostReq().load(kwargs)
        except ValidationError:
            abort(400, message='invalid terminate request')

        # Second validation outside of Marshmallow
        if 'terminate' not in req:
            abort(400, message='invalid terminate request')

        res = False

        if req['terminate'] and State.getInstance() is not None:
            try:
                State.getInstance().stop()
                State.setInstance(None)
                res = True
            except Exception:
                abort(500, message='terminate request failed')

        return {
            'terminated': res
        }, 200
