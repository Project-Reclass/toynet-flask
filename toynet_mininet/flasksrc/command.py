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
from toynet.toynet import ToyNet
from toynet.state import State

#Schema definitions
class MiniFlaskCommandPostReq(Schema):
    command = fields.String()


class MiniFlaskCommandPostResp(Schema):
    output = fields.String()


class MiniFlaskCommand(MethodResource):
    @use_kwargs(MiniFlaskCommandPostReq)
    @marshal_with(MiniFlaskCommandPostResp)
    def post(self, **kwargs):
        try:
            req = MiniFlaskCommandPostReq().load(kwargs)
        except ValidationError as e:
            abort(400, message='invalid command request')

        # Second validation outside of Marshmallow
        if 'command' not in req:
            abort(400, message='invalid command request')
        
        res = ''
        if State.getInstance() is not None:
            res = State.getInstance().cmd(req['command'])
        else:
            abort(500, message='No topology defined')

        return {
            'output': res,
            }, 200
