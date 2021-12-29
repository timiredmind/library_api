from marshmallow import fields, Schema
from utils import generate_url_link


class PaginationSchema(Schema):
    class Meta:
        ordered = True

    links = fields.Method(serialize="generate_pagination_link")
    page = fields.Integer(dump_only=True)
    pages = fields.Integer(dump_only=True)
    per_page = fields.Integer(dump_only=True)
    total = fields.Integer(dump_only=True)

    def generate_pagination_link(self, paginated_object):
        generated_links = {
            "first": generate_url_link(page=1)
        }
        if paginated_object.pages == 0:
            generated_links["last"] = generate_url_link(page=1)
        else:
            generated_links["last"] = generate_url_link(page=paginated_object.pages)

        if paginated_object.has_next:
            generated_links["next"] = generate_url_link(page=paginated_object.next_num)

        if paginated_object.has_prev:
            generated_links["prev"] = generate_url_link(page=paginated_object.prev_num)

        return generated_links

