from typing import List
from aiohttp.web import Request
from aiohttp.web_response import Response
from aiohttp_rest_api import AioHTTPRestEndpoint
from aiohttp_rest_api.responses import respond_with_json
import logging
from models.posts import Posts
from api import to_dict

log = logging.getLogger(__name__)


class PostsEndpoint(AioHTTPRestEndpoint):

    def connected_routes(self) -> List[str]:
        """"""
        return [
            '/posts'
        ]

    async def get(self, request: Request) -> Response:
        """
        Получение списка данных новостей из БД.

        Поддерживает параметры:

        order = сортировка значений в определённом столбце, по умолчанию id
        sort = сортировка asc - возрастание/desc - убывание, по умолчанию desc
        limit = лимит данных, по умолчанию 5
        offset = смещение, по умолчанию 0

        :param
            * *request* (``Request``) -- запрос

        :rtype (``Response``)
        :return: список новостей
        """
        order = request.query.get('order')
        sort_type = request.query.get('sort', 'desc')
        limit = request.query.get('limit', '5')
        offset = request.query.get('offset', '0')
        if limit.isdigit():
            limit = abs(int(limit))
        if offset.isdigit():
            offset = abs(int(offset))

        db = request.app['db']
        query = db.session.query(Posts)
        if order:
            try:
                condition = getattr(Posts, order)
            except AttributeError as e:
                log.info(e)
                return respond_with_json(
                    {'error': f'Attribute {order} not found', 'status': 400}
                )
        else:
            condition = getattr(Posts, 'id')

        if sort_type == 'desc':
            condition = condition.desc()
        elif sort_type == 'asc':
            condition = condition.asc()
        else:
            return respond_with_json(
                {'error': f'Wrong parameter sort - {sort_type}', 'status': 400}
            )

        query = query.order_by(condition).limit(limit).offset(limit * offset)
        data = [to_dict(x) for x in query]
        return respond_with_json(data)
