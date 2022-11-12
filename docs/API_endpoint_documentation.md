# API Endpoint Documentation

## User routes:

---

* /user/
  * Methods: GET
  * Arguments: None
  * Description: Get all users' information
  * Authentication: @jwt_required
  * Authorization: Bearer token
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
  
    ![Get_all_users](Get_all_users.png)

* /user/<int:user_id>/
  * Methods: GET
  * Arguments: user_id
  * Description: Get information of the user with the specified user_id
  * Authentication: @jwt_required
  * Authorization: Bearer token
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
    ![Get_single_user](Get_single_user.png)

* /user/update/
  * Methods: PUT, PATCH
  * Arguments: None
  * Description: Update one user's information
  * Authentication: @jwt_required
  * Authorization: None
  * Request Body:
  
    ![Update_user_request](Update_user_request.png)
  * HTTP Code: 200
  * Response Body:
  
    ![Update_user_response](Update_user_response.png)

* /user/<int:user_id>/
  * Methods: DELETE
  * Arguments: user_id
  * Description: Delete the user with the specified user_id
  * Authentication: @jwt_required
  * Authorization: Bearer token
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
  
    ![Delete_user](Delete_user.png)

* /user/register/
  * Methods: POST
  * Arguments: None
  * Description: Register user
  * Authentication: None
  * Authorization: None
  * Request Body: 
  
    ![Register_user_request](Register_user_request.png)
  * HTTP Code: 201
  * Response Body:
  
    ![Register_user_response](Register_user_response.png)

* /user/login/
  * Methods: POST
  * Arguments: None
  * Description: User login
  * Authentication: None
  * Authorization: None
  * Request Body:
  
    ![User_login_request](User_login_request.png)
  * HTTP Code: 200
  * Response Body:
  
    ![User_login_response](User_login_response.png)

* /user/customer/
  * Methods: POST
  * Arguments: None
  * Description: Customer registration
  * Authentication: @jwt_required
  * Authorization: None
  * Request Body:
  
    ![Customer_registration_request](Customer_registration_request.png)
  * HTTP Code: 201
  * Response Body:
  
    ![Customer_registration_response](Customer_registration_response.png)

* /user/customer/
  * Methods: GET
  * Arguments: None
  * Description: Get all customers' information
  * Authentication: @jwt_required
  * Authorization: Bearer token
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
  
    ![Get_all_customers](Get_all_customers.png)

* /user/customer/<int:customer_id/>
  * Methods: GET
  * Arguments: customer_id
  * Description: Get single customer's information
  * Authentication: @jwt_required
  * Authorization: Bearer token
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
  
    ![Get_single_customer](Get_single_customer.png)

* /user/customer/update/phone/
  * Methods: PUT, PATCH
  * Arguments: None
  * Description: Update customer's phone number
  * Authentication: @jwt_required
  * Authorization: None
  * Request Body:
  
    ![Update_phone_request](Update_customer_phone_request.png)
  * HTTP Code: 200
  * Response Body:
  
    ![Update_phone_response](Update_customer_phone_response.png)

* /user/customer/update/address/
  * Methods: PUT, PATCH
  * Arguments: None
  * Description: Update customer's address
  * Authentication: @jwt_required
  * Authorization: None
  * Request Body:

    ![Update_address_request](Update_customer_address_request.png)
  * HTTP Code: 200
  * Response Body:
  
    ![Update_address_response](Update_customer_address_response.png)

* /user/customer/address/
  * Methods: GET
  * Arguments: None
  * Description: Get all addresses
  * Authentication: @jwt_required
  * Authorization: Bearer token
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
  
    ![Get_all_addresses](Get_all_addresses.png)
  
* /user/customer/address/
  * Methods: POST
  * Arguments: None
  * Description: Create a new address
  * Authentication: @jwt_required
  * Authorization: None
  * Request Body:
  
    ![Create_address_request](Create_address_request.png)
  * HTTP Code: 201
  * Response Body:
  
    ![Create_address_response](Create_address_response.png)


* /user/customer/address/<int:address_id>/
  * Methods: GET
  * Arguments: address_id
  * Description: Get information of an address
  * Authentication: @jwt_required
  * Authorization: Bearer token
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
  
    ![Get_single_address](Get_single_address.png)

* /user/customer/address/postcode/
  * Methods: GET
  * Arguments: None
  * Description: Get all postcodes' information
  * Authentication: @jwt_required
  * Authorization: Bearer token
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
  
  ![Get_all_postcodes](Get_all_postcodes.png)


* /user/customer/address/postcode/<int:postcode_id>/
  * Methods: GET
  * Arguments: postcode_id
  * Description: Get information of a postcode
  * Authentication: @jwt_required
  * Authorization: Bearer token
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
  
    ![Get_single_postcode](Get_single_postcode.png)


* /user/customer/address/postcode/
  * Methods: POST
  * Arguments: None
  * Description: Create a new postcode
  * Authentication: @jwt_required
  * Authorization: Bearer token
  * Request Body:
  
    ![Create_postcode_request](Create_postcode_request.png)
  * HTTP Code: 201
  * Response Body:
  
    ![Create_postcode_response](Create_postcode_response.png)

* /user/customer/payment_account/
  * Methods: GET
  * Arguments: None
  * Description: Get all payment_account fot the customer
  * Authentication: @jwt_required
  * Authorization: None
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
  
    ![Get_all_paymentaccounts](Get_all_paymentaccounts.png)

* /user/customer/payment_account/<int:payment_account_id>/
  * Methods: GET
  * Arguments: payment_account_id
  * Description: Get a particular payment_account
  * Authentication: @jwt_required
  * Authorization: None
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
  
    ![Get_single_paymentaccount](Get_single_paymentaccount.png)

* /user/customer/payment_account/
  * Methods: POST
  * Arguments: None
  * Description: Create a new payment_account
  * Authentication: @jwt_required
  * Authorization: None
  * Request Body:
  
    ![Create_paymentaccount_request](Create_paymentaccount_request.png)
  * HTTP Code: 200
  * Response Body:
  
    ![Create_paymentaccount_response](Create_paymentaccount_response.png)

* /user/customer/payment_account/<int:payment_account_id>/
  * Methods: DELETE
  * Arguments: payment_account_id
  * Description: Delete a payment_account
  * Authentication: @jwt_required
  * Authorization: Bearer token
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
  
    ![Delete_paymentaccount](Delete_paymentaccount.png)

## Order routes:


* /order/
  * Methods: GET
  * Arguments: None
  * Description: Get all orders' information
  * Authentication: @jwt_required
  * Authorization: Bearer token
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
  
    ![Get_all_orders_1](Get_all_orders_1.png)
    ![Get_all_orders_2](Get_all_orders_2.png)
    ![Get_all_orders_3](Get_all_orders_3.png)

* /order/<int:order_id>/
  * Methods: GET
  * Arguments: order_id
  * Description: Get a single order's information
  * Authentication: @jwt_required
  * Authorization: Bearer token
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
  
    ![Get_single_order](Get_single_order.png)

* /order/customer/
  * Methods: GET
  * Arguments: None
  * Description: Get orders for a customer
  * Authentication: @jwt_required
  * Authorization: None
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
  
    ![Get_order_for_a_customer_1](Get_order_for_a_customer_1.png)
    ![Get_order_for_a_customer_2](Get_order_for_a_customer_2.png)

* /order/customer/
  * Methods: POST
  * Arguments: None
  * Description: Create a new order
  * Authentication: @jwt_required
  * Authorization: None
  * Request Body:
  
    ![Create_order_request](Create_order_request.png)
  * HTTP Code: 201
  * Response Body:
  
    ![Create_order_response](Create_order_response.png)

* /order/detail/
  * Methods: POST
  * Arguments: None
  * Description: Create a new orderdetail
  * Authentication: @jwt_required
  * Authorization: None
  * Request Body:
  
    ![Create_orderdetail_request](Create_orderdetail_request.png)
  * HTTP Code: 201
  * Response Body:
  
    ![Create_orderdetail_response](Create_orderdetail_response.png)

* /order/detail/
  * Methods: GET
  * Arguments: None
  * Description: Get all orderdetails' information
  * Authentication: @jwt_required
  * Authorization: Bearer token
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
  
    ![Get_all_orderdetails](Get_all_orderdetails.png)

* /order/detail/<int:order_detail_id>/
  * Methods: GET
  * Arguments: order_detail_id
  * Description: Get a single orderdetail's information
  * Authentication: @jwt_required
  * Authorization: Bearer token
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
  
    ![Get_single_orderdetail](Get_single_orderdetail.png)

* /order/status/
  * Methods: GET
  * Arguments: None
  * Description: Get all order status
  * Authentication: @jwt_required
  * Authorization: Bearer token
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
  
    ![Get_all_orderstatus](Get_all_orderstatus.png)

* /order/status/<int:order_status_id>/
  * Methods: GET
  * Arguments: None
  * Description: Get a single order status
  * Authentication: @jwt_required
  * Authorization: Bearer token
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
  
    ![Get_single_orderstatus](Get_single_orderstatus.png)

* /order/status/
  * Methods: POST
  * Arguments: None
  * Description: Create a new order status
  * Authentication: @jwt_required
  * Authorization: Bearer token
  * Request Body:
  
    ![Create_orderstatus_request](Create_orderstatus_request.png)
  * HTTP Code: 201
  * Response Body:
  
    ![Create_orderstatus_response](Create_orderstatus_response.png)

* /order//status/<int:order_status_id>/
  * Methods: PUT, PATCH
  * Arguments: order_status_id
  * Description: Update a order status
  * Authentication: @jwt_required
  * Authorization: Bearer token
  * Request Body:
  
    ![Update_orderstatus_request](Update_orderstatus_request.png)
  * HTTP Code: 200
  * Response Body:
  
    ![Update_orderstatus_response](Update_orderstatus_response.png)

* /order/status/<int:order_status_id>/
  * Methods: DELETE
  * Arguments: order_status_id
  * Description: Delete a order status
  * Authentication: @jwt_required
  * Authorization: Bearer token
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
  
    ![Delete_orderstatus](Delete_orderstatus.png)

* /order//shipping/
  * Methods: GET
  * Arguments: None
  * Description: Get all shippingmethods' information
  * Authentication: @jwt_required
  * Authorization: Bearer token
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
  
    ![Get_all_shippingmethods](Get_all_shippingmethods.png)

* /order/shipping/<int:shipping_method_id>/
  * Methods: GET
  * Arguments: shipping_method_id
  * Description: Get information of a shipping method
  * Authentication: @jwt_required
  * Authorization: Bearer token
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
  
    ![Get_single_shippingmethod](Get_single_shippingmethod.png)

* /order/shipping/
  * Methods: POST
  * Arguments: None
  * Description: Create a new shipping method
  * Authentication: @jwt_required
  * Authorization: Bearer token
  * Request Body:
  
    ![Create_shippingmethod_request](Create_shippingmethod_request.png)
  * HTTP Code: 201
  * Response Body:
  
    ![Create_shippingmethod_response](Create_shippingmethod_response.png)

* /order/shipping/<int:shipping_method_id>/
  * Methods: PUT, PATCH
  * Arguments: shipping_method_id
  * Description: Update a shipping method
  * Authentication: @jwt_required
  * Authorization: Bearer token
  * Request Body:
  
    ![Update_shippingmethod_request](Update_shippingmethod_request.png)
  * HTTP Code: 200
  * Response Body:
  
    ![Update_shippingmethod_response](Update_shippingmethod_response.png)

* /order/shipping/<int:shipping_method_id>/
  * Methods: DELETE
  * Arguments: shipping_method_id
  * Description: Delete a shipping method
  * Authentication: @jwt_required
  * Authorization: Bearer token
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
  
    ![Delete_shippingmethod](Delete_shippingmethod.png)

## Product routes:

* /product/
  * Methods: GET
  * Arguments: None
  * Description: Get all products' information
  * Authentication: @jwt_required
  * Authorization: None
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
  
    ![Get_all_products](Get_all_products.png)

* /product/<int:product_id>/
  * Methods: GET
  * Arguments: product_id
  * Description: Get a single product's information
  * Authentication: @jwt_required
  * Authorization: None
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
  
    ![Get_single_product](Get_single_product.png)

* /product/
  * Methods: POST
  * Arguments: None
  * Description: Create a new product
  * Authentication: @jwt_required
  * Authorization: Bearer token
  * Request Body:
  
    ![Create_product_request](Create_product_request.png)
  * HTTP Code: 201
  * Response Body:
  
    ![Create_product_response](Create_product_response.png)

* /product/<int:product_id>/
  * Methods: PUT, PATCH
  * Arguments: product_id
  * Description: Update a product
  * Authentication: @jwt_required
  * Authorization: Bearer token
  * Request Body:
  
    ![Update_product_request](Update_product_request.png)
  * HTTP Code: 200
  * Response Body:
  
    ![Update_product_response](Update_product_response.png)

* /product/<int:product_id>/
  * Methods: DELETE
  * Arguments: product_id
  * Description: Delete a product
  * Authentication: @jwt_required
  * Authorization: Bearer token
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
  
    ![Delete_product](Delete_product.png)

* /product/category/
  * Methods: GET
  * Arguments: None
  * Description: Get all categories' information
  * Authentication: @jwt_required
  * Authorization: None
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
  
    ![Get_all_categories](Get_all_categories.png)

* /product/category/<int:category_id>/
  * Methods: GET
  * Arguments: category_id
  * Description: Get a category's information
  * Authentication: @jwt_required
  * Authorization: None
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
  
    ![Get_single_category](Get_single_category.png)

* /product/category/
  * Methods: POST
  * Arguments: None
  * Description: Create a category
  * Authentication: @jwt_required
  * Authorization: Bearer token
  * Request Body:
  
    ![Create_category_request](Create_category_request.png)
  * HTTP Code: 201
  * Response Body:
  
    ![Create_category_response](Create_category_response.png)

* /product/category/<int:category_id>/
  * Methods: PUT, PATCH
  * Arguments: category_id
  * Description: Update a category
  * Authentication: @jwt_required
  * Authorization: Bearer token
  * Request Body:
  
  ![Update_category_request](Update_category_request.png)
  * HTTP Code: 200
  * Response Body:
  
    ![Update_category_response](Update_category_response.png)

* /product/category/<int:category_id>/
  * Methods: DELETE
  * Arguments: category_id
  * Description: Delete a category
  * Authentication: @jwt_required
  * Authorization: Bearer token
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
  
    ![Delete_category](Delete_category.png)

* /product/<int:product_id_entered>/review/
  * Methods: GET
  * Arguments: product_id_entered
  * Description: Get all reviews of a product
  * Authentication: @jwt_required
  * Authorization: None
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
  
    ![Get_all_reviews](Get_all_reviews.png)

* /product/<int:product_id_entered>/review/<int:review_id>/
  * Methods: GET
  * Arguments: product_id_entered, review_id
  * Description: Get a particular review of a product
  * Authentication: @jwt_required
  * Authorization: None
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
  
    ![Get_single_review](Get_single_review.png)

* /product/<int:product_id_entered>/review/
  * Methods: POST
  * Arguments: product_id_entered
  * Description: Create a reivew for the product
  * Authentication: @jwt_required
  * Authorization: None
  * Request Body:
  
    ![Create_review_request](Create_review_request.png)
  * HTTP Code: 201
  * Response Body:
  
    ![Create_review_response](Create_review_response.png)

* /product/<int:product_id_entered>/review/<int:review_id>/
  * Methods: DELETE
  * Arguments: product_id_entered, review_id
  * Description: Delete a review of a product
  * Authentication: @jwt_required
  * Authorization: None
  * Request Body: None
  * HTTP Code: 200
  * Response Body:
  
    ![Delete_review](Delete_review.png)

## Error handling

* 400 - Bad request

Raise error with wrong syntax

![400](400.png)
  
* Key Error

Raise error if missing required fields, such as foreign keys

![KeyError](KeyError.png)

* DataError

Raise error if data entered does not follow the data type and constraints

![DataError](DataError.png)

* 404
  
Raise error when data not found

![404](404.png)

* 401

Raise error when user are not authorized to perform the operation

![401](401.png)

* Validation Error

Raise error when data validation fails

![ValidationError](ValidationError.png)