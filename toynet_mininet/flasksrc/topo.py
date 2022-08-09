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
from flask_apispec import MethodResource, use_kwargs
from util.error import XMLParseError, TypeCheckError
from toynet.toynet import ToyNet
from toynet.state import State


# Schema definitions
class MiniFlaskTopoPostReq(Schema):
    topology = fields.Str()


class MiniFlaskTopo(MethodResource):
    @use_kwargs(MiniFlaskTopoPostReq)
    def post(self, **kwargs):
        try:
            req = MiniFlaskTopoPostReq().load(kwargs)
        except ValidationError:
            abort(400, message='topology not provided')

        # Second validation after Marshmallow
        if 'topology' not in req:
            abort(400, message='topology not provided')

        try:
            if State.getInstance() is None:
                State.setInstance(ToyNet(filecontent=req['topology']))
                State.getInstance().start()
            else:
                State.getInstance().restart(new_topology=req['topology'])
        except (XMLParseError, TypeCheckError) as e:
            abort(400, message=f'failed to parse XML topology {State.getInstance()}; ' + str(e))

        return {
        }, 200
