# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/crawlib-project/crawlib/tests/dummy_site_crawler/sql_backend/s2_music/entity_music_sql_backend.py
# Compiled at: 2019-12-30 16:10:34
# Size of source mod 2**32: 6686 bytes
import typing, requests, sqlalchemy as sa
from crawlib import Status, ParseResult, resolve_arg, Relationship, RelationshipConfig
from crawlib.entity.sql import Base, SqlEntitySingleStatus
from ...music_url_builder import url_builder

class MusicPageBase(Base, SqlEntitySingleStatus):
    __abstract__ = True

    def build_request(self, url, **kwargs):
        request = url
        return request

    def send_request(self, request, **kwargs):
        return requests.get(request)


class MusicPage(MusicPageBase):
    __tablename__ = 'site_music_music'
    CONF_UPDATE_INTERVAL = 86400
    CONF_ONLY_FIELDS = ('id', )
    id = sa.Column((sa.Integer), primary_key=True)
    title = sa.Column(sa.String)
    artists = sa.Column(sa.PickleType)
    n_artist = sa.Column(sa.Integer)
    genres = sa.Column(sa.PickleType)
    n_genre = sa.Column(sa.Integer)

    @property
    def music_id(self):
        return self.id

    def build_url(self):
        return url_builder.url_music_detail(self.music_id)

    @resolve_arg()
    def parse_response(self, url, request, response=None, html=None, soup=None, **kwargs):
        div_detail = soup.find('div', id='detail')
        title = div_detail.find('div', class_='title').find('span').text
        artists = [int(a['href'].split('/')[(-1)]) for a in div_detail.find('div', class_='artists').find_all('a')]
        genres = [int(a['href'].split('/')[(-1)]) for a in div_detail.find('div', class_='genres').find_all('a')]
        entity_data = dict(title=title, artists=artists, genres=genres)
        children = list()
        for artist_id in artists:
            children.append(ArtistPage(id=artist_id))

        for genre_id in genres:
            children.append(GenrePage(id=genre_id))

        status = Status.S50_Finished.id
        pres = ParseResult(entity_data=entity_data,
          children=children,
          additional_data={},
          status=status)
        return pres


class ArtistPage(MusicPageBase):
    __tablename__ = 'site_music_artist'
    CONF_UPDATE_INTERVAL = 3600
    CONF_ONLY_FIELDS = ('id', )
    CONF_RELATIONSHIP = RelationshipConfig([
     Relationship(child_klass=MusicPage,
       relationship=(Relationship.Option.many),
       n_child_key='n_music',
       recursive=False)])
    id = sa.Column((sa.Integer), primary_key=True)
    musics = sa.Column(sa.PickleType)
    n_music = sa.Column(sa.Integer)

    @property
    def artist_id(self):
        return self.id

    def build_url(self):
        return url_builder.url_artist(self.artist_id)

    @resolve_arg()
    def parse_response(self, url, request, response, html=None, soup=None, **kwargs):
        div = soup.find('div', id='detail')
        musics = [int(a['href'].split('/')[(-1)]) for a in div.find_all('a')]
        entity_data = dict(musics=musics)
        children = list()
        for music_id in musics:
            music = MusicPage(id=music_id)
            children.append(music)

        status = Status.S50_Finished.id
        pres = ParseResult(entity_data=entity_data,
          children=children,
          additional_data={},
          status=status)
        return pres


class GenrePage(MusicPageBase):
    __tablename__ = 'site_music_genre'
    CONF_UPDATE_INTERVAL = 3600
    CONF_ONLY_FIELDS = ('id', )
    CONF_RELATIONSHIP = RelationshipConfig([
     Relationship(child_klass=MusicPage,
       relationship=(Relationship.Option.many),
       n_child_key='n_music',
       recursive=False)])
    id = sa.Column((sa.Integer), primary_key=True)
    musics = sa.Column(sa.PickleType)
    n_music = sa.Column(sa.Integer)

    @property
    def genre_id(self):
        return self.id

    def build_url(self):
        return url_builder.url_genre(self.genre_id)

    @resolve_arg()
    def parse_response(self, url, request, response, html=None, soup=None, **kwargs):
        div = soup.find('div', id='detail')
        musics = [int(a['href'].split('/')[(-1)]) for a in div.find_all('a')]
        entity_data = dict(musics=musics)
        children = list()
        for music_id in musics:
            music = MusicPage(id=music_id)
            children.append(music)

        status = Status.S50_Finished.id
        pres = ParseResult(entity_data=entity_data,
          children=children,
          additional_data={},
          status=status)
        return pres


class RandomMusicPage(MusicPageBase):
    __tablename__ = 'site_music_random_music'
    CONF_UPDATE_INTERVAL = 1
    CONF_ONLY_FIELDS = ('id', )
    CONF_RELATIONSHIP = RelationshipConfig([
     Relationship(child_klass=MusicPage,
       relationship=(Relationship.Option.many),
       n_child_key='n_music',
       recursive=True)])
    id = sa.Column((sa.Integer), primary_key=True)
    musics = sa.Column(sa.PickleType)
    n_music = sa.Column(sa.Integer)

    def build_url(self, **kwargs):
        return url_builder.url_random_music()

    @resolve_arg()
    def parse_response(self, url, request, response=None, html=None, soup=None, **kwargs):
        musics = [int(a['href'].split('/')[(-1)]) for a in soup.find_all('a')]
        entity_data = dict(musics=musics)
        children = list()
        for music_id in musics:
            music = MusicPage(id=music_id)
            children.append(music)

        status = Status.S50_Finished.id
        pres = ParseResult(entity_data=entity_data,
          children=children,
          additional_data={},
          status=status)
        return pres


MusicPage.CONF_RELATIONSHIP = RelationshipConfig([
 Relationship(child_klass=ArtistPage,
   relationship=(Relationship.Option.many),
   n_child_key='n_artist',
   recursive=True),
 Relationship(child_klass=GenrePage,
   relationship=(Relationship.Option.many),
   n_child_key='n_genre',
   recursive=True)])
MusicPage.validate_implementation()
ArtistPage.validate_implementation()
GenrePage.validate_implementation()
RandomMusicPage.validate_implementation()