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
 
FROM python:3.8-slim-buster

ARG FLASK_APP
ARG FLASK_ENV
ARG TOYNET_IMAGE_TAG
ARG MINI_FLASK_PORT
ARG COMPOSE_NETWORK

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP ${FLASK_APP}
ENV FLASK_ENV ${FLASK_ENV}
ENV TOYNET_IMAGE_TAG ${TOYNET_IMAGE_TAG}
ENV MINI_FLASK_PORT ${MINI_FLASK_PORT}
ENV COMPOSE_NETWORK ${COMPOSE_NETWORK}

EXPOSE 5000

ENTRYPOINT /app/entrypoint.sh
