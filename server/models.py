from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    #customer_reviews
    customer_reviews = db.relationship('Review', back_populates='customer')
    items = association_proxy('customer_reviews', 'item')

    # to test serialize_rules...POSTMAN (you'll have to write routes)
    # or in flask shell -> customer_instance.to_dict()
    serialize_rules = ('-customer_reviews.customer', )

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'
    
    """
    customer: {
        id,
        name,
        customer_reviews: [{
            id, 
            comment,
            customer: {
                id,
                name,
                customer_reviews: [{
                    id,
                    comment,
                    customer...
                }]
            },
            item: {}
        }, ...],
        items: [{
            id,
            name,
            price,
            reviews: []
        }, ...]
    }
    """
    


class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    #item_reviews
    item_reviews = db.relationship('Review', back_populates='item')

    serialize_rules = ('-item_reviews.item', )
    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'
    
class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)

    comment = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    #refers to customer_reviews
    customer = db.relationship('Customer', back_populates='customer_reviews')
    #refers to item_reviews
    item = db.relationship('Item', back_populates='item_reviews')



    serialize_rules = ('-customer.customer_reviews', '-item.item_reviews')