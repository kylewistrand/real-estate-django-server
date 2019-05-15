# real-estate-django-server
Final project for INFO 441 (Server-Side Development) built with Django

### ERD
<img src="Real Estate Server ERD.jpeg" alt="Real Estate Server ERD">

### Models
- Offer
- Coupon
- CouponType
- Property
- PropertyType
- UserDetail
- User_Role
- Role
- Ownership
- Cart
- Neighborhood
- Property_Photo
- Photo
- Property_Amenity
- Amenity

### Views

###### realestate/auth/register
- POST: Create a new user
- GET: Form
###### realestate/auth/sign-in
- POST: Login user
- GET: Form
###### realestate/users/<user_id> (admin authentication)
- GET: JSON of specified user
- PATCH: Edit user (role, description, etc)
- DELETE: Remove specific user
###### realestate/coupons (admin authentication)
- POST: Create a new coupon
- GET: List of all coupons or maybe a form if a user is logged in?
- DELETE: Delete all coupons
###### realestate/coupons/<coupon_id> (admin authentication)
- PATCH: Edit specified coupon
- DELETE: Remove specified coupon
- GET: Retrieve JSON of specified coupon
###### realestate/properties (seller authentication)
- POST: Create new property listing (amenity, neighborhood, etc)
- GET: List of all of seller’s properties or maybe a form?
- DELETE: Remove all of seller’s properties
###### realestate/properties/<property_id>
- GET: JSON of specified property
- POST: Add to specified cart
    - User authentication
- DELETE: Delete specified property
    - Seller authentication
###### realestate/checkout (User authentication)
- GET: List of properties in cart
- POST: Purchase properties
- DELETE: Remove specified property from cart
###### realestate/offers (User authentication)
- GET: List of all current and past offers
- POST: Make a new offer
- PATCH: Edit your own offer or create a counter offer
###### realestate/coupons/<coupon_id> (admin authentication)
PATCH: Edit specified coupon

DELETE: Remove specified coupon

GET: Retrieve JSON of specified coupon

###### realestate/auth/register 
POST: Create a new user

GET: Form

###### realestate/checkout (User authentication)
GET: List of properties in cart

POST: Purchase properties

DELETE: Remove specified property from cart



