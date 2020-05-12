# This is a simple Dockerfile to use while developing
# It's not suitable for production
#
# It allows you to run both flask and celery if you enabled it
# for flask: docker run --env-file=.flaskenv image flask run
# for celery: docker run --env-file=.flaskenv image celery worker -A myapi.celery_app:app
#
# note that celery will require a running broker and result backend
FROM python:3.8

RUN mkdir /code
WORKDIR /code

COPY requirements.txt setup.py tox.ini ./
RUN pip install -r requirements.txt
RUN pip install -e .

COPY covidapi covidapi/
COPY migrations migrations/

# Install the latest version of Firefox:
RUN export DEBIAN_FRONTEND=noninteractive \
  && apt-get update \
  && apt-get install --no-install-recommends --no-install-suggests -y \
     # Firefox dependencies:
     libavcodec-extra \
     libgtk-3-0 \
     libdbus-glib-1-2 \
     libx11-xcb1 \
     libxcb1 \
     bzip2 \
  && DL='https://download.mozilla.org/?product=firefox-latest-ssl&os=linux64' \
  && curl -sL "$DL" | tar -xj -C /opt \
  && ln -s /opt/firefox/firefox /usr/local/bin/ \
  # Remove obsolete files:
  && apt-get autoremove --purge -y \
     bzip2 \
  && apt-get clean \
  && rm -rf \
     /tmp/* \
     /usr/share/doc/* \
     /var/cache/* \
     /var/lib/apt/lists/* \
     /var/tmp/*


# Install the Geckodriver:
RUN BASE_URL=https://github.com/mozilla/geckodriver/releases/download \
  && VERSION="v0.26.0" \
  && curl -sL "$BASE_URL/$VERSION/geckodriver-$VERSION-linux64.tar.gz" | \
     tar -xz -C /usr/local/bin

EXPOSE 5000

