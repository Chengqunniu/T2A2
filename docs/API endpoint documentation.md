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
  * HTTP Code: 200
  * Response Body:
    ![Create_postcode_response](Create_postcode_response.png)


## Error handling

* 400
* Key Error
* DataError
* 404
* 401
* Validation Error