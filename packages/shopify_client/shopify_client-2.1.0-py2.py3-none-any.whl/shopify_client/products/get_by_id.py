from shopify_client.common.graphql_client import GraphqlClient


class ProductGetById(GraphqlClient):
    def get_query(self):
        return '''
            query GetProduct($id: ID!){   
                product(id: $id) {
                    id
                    title
                    handle
                    status
                    productType
                    tags
                    featuredImage {
                        url
                    }
                }
            }
        '''

    def get_variables(self, product_id):
        return {
            'id': product_id
        }

    def get_parsed_response(self, response):
        product = response['data']['product']

        return {
            'id': product['id'],
            'title': product['title'],
            'handle': product['handle'],
            'status': product['status'],
            'product_type': product['productType'],
            'tags': product['tags'],
            'image_url': (product['featuredImage'] or {}).get('url')
        }
