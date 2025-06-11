Business Contract
=================
1. Obective 
  -> The Bill Management System is designed to streamline and automate bill tracking, payments, reminders, and reporting for Admins, Billers, and Customers. 
     It follows a Domain-Driven Design (DDD) and microservices architecture, emphasizing separation of concerns, clear ownership of business logic, 
      and modular growth.

2. Scope
  -> The Bill Management System covers the following business processes:
     - Bill creation, update, and deletion
     - Payment tracking
     - Bill reminders
     - Reporting and analytics
     - User authentication and authorization

3. Stakeholders/system Identities
  -> The primary stakeholders of the Bill Management System include:
     - Admin : is a user who has a privilege to create billers and customers.
             : Responsibilities
                  * Create billers and customers by assigning their roles.
                  * view a list of  all users by role.
                 -> Bill oversight
                      * view specific biller or customer profile.
                      * update specific biller or customer profile.
                      * delete specific biller or customer profile.
                      * can view all bills in the system by biller_id/customer_id/bill_status.
                 -> Reminder management
                      * can view all reminders scheduled/not scheduled/sent.
                 -> Reporting and analytics
                      * View over all bill reports issued by all billers. 
{
  "total_billers": 35,
  "total_customers": 240,
  "total_bills_systemwide": 1000,
  "total_amount_billed": 150000.00,
  "total_paid_amount": 130000.00,
  "total_outstanding_amount": 20000.00,
  "monthly_report": [
    {
      "month": "2025-05",
      "bills_created": 300,
      "amount_billed": 45000.00,
      "amount_paid": 39000.00,
      "new_billers": 3,
      "new_customers": 25
    },
    ...
  ],
  "top_billers": [
    {
      "biller_id": "b123",
      "biller_name": "Electricity Co",
      "bills_issued": 120,
      "amount_billed": 22000.00,
      "paid_ratio": 0.9
    },
    ...
  ],
  "top_debtors": [
    {
      "customer_id": "c456",
      "customer_name": "Jane Doe",
      "outstanding_amount": 1200.00,
      "overdue_bills": 3
    },
    ...
  ]
}

     - Billers : are responsible for issuing and managing bills for their customers
             : Responsibilities
                  * Create bills for their specific customer.
                  * Update bills status for their specific customer.
                  * View all bills issued to their specific customer.
                  * View all bills issued by all of their customers.
                  * View all reports of their bills
     {
  "total_bills_issued": 120,
  "total_amount_billed": 45000.00,
  "total_paid_amount": 37500.00,
  "total_outstanding_amount": 7500.00,
  "paid_bills_count": 90,
  "pending_bills_count": 25,
  "overdue_bills_count": 5,
  "bills_per_customer": [
    {
      "customer_id": "c123",
      "customer_name": "John Doe",
      "total_bills": 10,
      "paid": 8,
      "pending": 1,
      "overdue": 1,
      "total_billed": 3500.00,
      "total_paid": 2800.00
    },
    ...
  ],
  "monthly_aggregation": [
    {
      "month": "2025-05",
      "bills_issued": 30,
      "amount_billed": 11000.00,
      "amount_paid": 9000.00,
      "amount_outstanding": 2000.00
    },
    ...
  ]
}

     - Customers : are responsible for making payments for their bills and tracking their bills with their reminders.
                 :Responsibilities
                  * View all bills issued by filter bill status:pending/unpaid/overdue.
                  * View all reminders for their bills: this can be achieved either by the customer interface to fetch all its reminders or view on its email.
                  * view all their payments made for their bills.
                  * View all reports of their bills
     {
  "total_bills_received": 15,
  "total_amount_due": 5400.00,
  "total_paid": 4800.00,
  "outstanding_amount": 600.00,
  "paid_bills": 12,
  "pending_bills": 2,
  "overdue_bills": 1,
  "bills_by_biller": [
    {
      "biller_id": "b789",
      "biller_name": "Water Corp",
      "total_billed": 2000.00,
      "total_paid": 1600.00,
      "outstanding": 400.00
    },
    ...
  ],
  "payment_history": [
    {
      "bill_id": "bill001",
      "amount": 200.00,
      "paid_on": "2025-06-01",
      "status": "paid"
    },
    ...
  ]
}

4. Constraints
  -> The Bill Management System should be secure, reliable, and scalable to handle large volumes of data and concurrent requests.

5. Dependencies
  -> The Bill Management System depends on:
     - A database (e.g., PostgreSQL)
     - A message queue (e.g., Redis)
     - A web server (e.g., FastAPI)

6. High-level Architecture
High level Architecture of the microservice
===========================================
Client (Frontend, Mobile, etc.)
     |
FastAPI route handlers ───►  routers/router.py
     |
Application Service Layer ─► handlers/user_handler.py or handlers/Bill_handler.py
     |
Domain / Business Logic ────► core/*.py
     |
Persistence Layer ──────────► fs/fs.py
     |
Database (PostgreSQL)
7. Project Structure and Description
*BillingManagerService
  -> app : The key objective is this folder is to define and start the FastAPI application with its required http server requirements
      -> __init__.py
      -> setup.py: This file sets up the necessary dependencies and configurations for the FastAPI application
  -> config
      -> __init__.py
      -> config.py
      ->.env
  -> fs
      -> __init__.py
      -> fs.py
  -> logic
      -> __init__.py
      -> Core
            -> Bill.py
            -> user.py
            -> __init__.py 
      -> DTO
            -> BillDto.py
            -> userDto.py
            -> __init__.py
      -> handlers
            -> __init__.py
            -> Bill_handler.py
            -> user_handler.py
      -> event_processor
            -> __init__.py
            -> Bill_reminder_event_processor.py
      -> utils   
  -> middlewares
      -> __init__.py
      -> auth_middleware.py
  -> routers
      -> __init__.py
      -> endpoint.py 
  -> tests
      -> __init__.py
      -> test_user_handler.py
      -> test_Bill_handler.py
  main.py

8. Domain Entinties: a data first approach to define the domains of the system
  -> The Bill Management System has the following key atomic data/physically existing entities:
     - Bills
          {
     -        id: int
     -        biller_id: int
     -        customer_id: int
     -        amount: float
     -        due_date: datetime
     -        status: str   /Pending/Paid/Overdue
     -        description: str
     -        created_at: datetime
     -        updated_at: datetime
     -    }
     - Users
            {
     -           id: int
     -           full_name: str
     -           username: str
     -           email: str
     -           password_hash: str
     -           role: str /Admin/Customer/Biller
     -           created_at: datetime
     -           updated_at: datetime
     - 
     -       }
       - And the system has also the following logical entities which are built on top of the atomic entities:
             PaymentHistory
                       {
                       -    id: int
                       -    bill_id: int
                            customer_id: int
                       -    amount_paid: float
                       -    paid_on: datetime
                            method:str  /cash/creditcard/mobile
                            created_at: datetime
                       }
             
            Fragmented data
               Reminders
                     {
                     -    id: int
                     -    bill_id: int
                     -    customer_id: int
                          reminder_type: str /email/sms/inApp
                          status: str /Pending/Sent/Failed
                          scheduled_on: datetime
                          sent_on: datetime
                          created_at: datetime
       - 
                     }
         9. API Specificaation
           -> The Bill Management System provides the following API endpoints:
             User: atomic data object of the system with all its actions/verbs
      
              - login 
                 Identity: Admin/Customer/Biller
                 Method: POST
                 URL:users/auth/api/v1/login
                 Description: Enables admin, customers, and billers to signin in to the system.
                 Logics:
                          step-1: Check if the user exists in the system
                          step-2: Check if the password is correct
                          step-3: prepare the payload stored in the JWT token {user_id, user_name,role}
                          step-4: Generate JWT token
                          step-5: Return JWT token
                          
                 Headers: None
                 req_body{
                             "username": "admin",
                             "password": "password"
                          }
                 resp{
                             "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
                             "token_type": "bearer"
                    
                      }
              - logout 
                 Identity: Admin/Customer/Biller
                 Method: POST
                 URL:users/auth/api/v1/logout
                 Description: Enables admin, customers, and billers to signout of the system.
                 Headers: Authorization: Bearer <access_token>
                 req_body: None
                 resp: None
                - refresh token
                   Identity: Admin/Customer/Biller
                   Method: POST
                   URL:users/auth/api/v1/refresh
                   Description: Enables admin, customers, and billers to refresh their access token.
                   logics:
                            Reads the refresh token from the HTTP-only secure cookie
                            Validates it (calls your auth.verify_refresh_token)
                            Extracts the payload (user info)
                            Generates a new access token and a new refresh token
                            Sets the new refresh token in the cookie
                            Returns the new access token in JSON
                 Headers: Authorization: Bearer <access_token>
                 req_body: None
                 resp: {
                             "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
                             "token_type": "bearer"
                      }
   
              - Register 
                 Identity: Admin
                 Method: POST
                 URL:users/api/v1/write_user
                 Description: Enables admin to register a new billers/customers.
                 Logics:
                          step-1: Parse and validate the incoming request body as RegisterUserDTO.
                          step-2: Check the current user’s role from the request state to ensure it’s "admin".
                          step-3: If not admin, return a custom error message with 403 Forbidden status.
                          step-4: Call the user model’s register method to create a new user with the DTO data.
                          step-5: Return the newly created user data serialized as UserResponseDTO.
            
                 Headers: Authorization: Bearer <access_token>
                 req_body: {
                             "full_name": "John Doe",
                             "username": "johndoe",
                             "email": "5r4wH@example.com",
                             "password": "password",
                             "role": "biller"
                    
                           }
                 resp: {
                             "id": 1,
                             "full_name": "John Doe",
                             "username": "johndoe",
                             "email": "5r4wH@example.com",
                             "role": "biller",
                             "created_at": "2021-01-01T00:00:00",
                             "updated_at": "2021-01-01T00:00:00"
                 }
                - view user profile
                   Identity: Admin/Customer/Biller
                   Method: GET
                   URL:users/api/v1/profile
                   Description: Enables admin, customers, and billers to view their profile.
                   Logics:
                           step-1: Extract the current user from the request state (populated by authentication middleware).
                           step-2: Fetch the full profile of the current user by their user ID.
                           step-3: Return the user profile serialized as UserResponseDTO.
                           step-4: No request body is expected
                           step-5: This endpoint is accessible by admin, customer, and biller (so no role-based restriction here).
                   Headers: Authorization: Bearer <access_token>
                   req_body: None
                   resp: {
                               "id": 1,
                               "full_name": "John Doe",
                               "username": "johndoe",
                               "email": "5r4wH@example.com",
                               "role": "biller",
                               "created_at": "2021-01-01T00:00:00",
                               "updated_at": "2021-01-01T00:00:00"
                           }  
                - Read user{biller/customer} by id
                   Identity: Admin
                   Method: GET
                   URL:users/api/v1/read_user/{user_id}
                   Description: Enables admin to read a specific biller/customer.
                   Logics:
                          step-1: Extract user_id from the request path parameters. 
                          Get the current user from request state. 
                          Check if current user’s role is "admin".
                          If not admin, return a "Not authorized" detail with status 403.
                          Fetch the user by user_id. 
                          If user not found, return a "User not found" detail with status 404.
                          Return the user serialized as UserResponseDTO.
                 Headers: Authorization: Bearer <access_token>
                 req_body: None
                 resp: {
                             "id": 1,
                             "full_name": "John Doe",
                             "username": "johndoe",
                             "email": "5r4wH@example.com",
                             "role": "biller",
                             "created_at": "2021-01-01T00:00:00",
                             "updated_at": "2021-01-01T00:00:00"
                 }
              - Update user{biller/customer} by id
                 Identity: Admin
                 Method: PUT
                 URL:users/api/v1/update_user/{user_id}
                 Description: Enables admin to update a specific biller/customer.
                 Headers: Authorization: Bearer <access_token>
                 req_body: {
                             "full_name": "John Doe",
                             "username": "johndoe",
                             "email": "5r4wH@example.com",
                             "role": "biller"
                           }
                 resp: {
                             "id": 1,
                             "full_name": "John Doe",
                             "username": "johndoe",
                             "email": "5r4wH@example.com",
                             "role": "biller",
                             "created_at": "2021-01-01T00:00:00",
                             "updated_at": "2021-01-01T00:00:00"
                 }
              - Remove user{biller/customer} by id
                 Identity: Admin
                 Method: DELETE
                 URL:users/api/v1/delete_user/{user_id}
                 Description: Enables admin to delete a specific biller/customer.
                 Headers: Authorization: Bearer <access_token>
                 req_body: None
                 resp: {
                             status_code: 204
                             "id": 1,
                        }
                - Read all users{biller/customer} by role
                   Identity: Admin
                   Method: GET
                   URL:users/api/v1/read_all_users/{role}
                   Description: Enables admin to read all billers/customers.
                   Headers: Authorization: Bearer <access_token>
                   req_body: None
                   resp: [
                               {
                                   "id": 1,
                                   "full_name": "John Doe",
                                   "username": "johndoe",
                                   "email": "5r4wH@example.com",
                                   "role": "biller",
                                   "created_at": "2021-01-01T00:00:00",
                                   "updated_at": "2021-01-01T00:00:00"
                               },
                               {
                                   "id": 2,
                                   "full_name": "Jane Doe",
                                   "username": "janedoe",
                                   "email": "Qb9l1@example.com",
                                   "role": "customer",
                                   "created_at": "2021-01-01T00:00:00",
                                   "updated_at": "2021-01-01T00:00:00"
                               }
                           ]
       
             Bills: atomic data object of the system
                - Create bill
                   Identity: Biller
                   Method: POST
                   URL:bills/api/v1/write_bill
                   Description: Enables biller to create a new bill.   
                   Headers: Authorization: Bearer <access_token>
                   req_body: {
                               "customer_id": 1,
                               "amount": 100.00,
                               "status": "pending"
                               "description": "This is a test bill"
                               "due_date": "2021-01-01T00:00:00"
                             }
                   resp: {
                               "id": 1,
                               "customer_id": 1,
                               "amount": 100.00,
                               "status": "pending",
                               "created_at": "2021-01-01T00:00:00",
                               "updated_at": "2021-01-01T00:00:00"
                           }
                - Read bill by id
                   Identity: Biller
                   Method: GET
                   URL:bills/api/v1/read_bill/{bill_id}
                   Description: Enables biller to read a specific bill.
                   Headers: Authorization: Bearer <access_token>
                   req_body: None
                   resp: {
                               "id": 1,
                               "customer_id": 1,
                               "amount": 100.00,
                               "status": "pending",
                               "created_at": "2021-01-01T00:00:00",
                               "updated_at": "2021-01-01T00:00:00"
                           }
                - Update bill by id
                   Identity: Biller
                   Method: PUT    
                   URL:bills/api/v1/update_bill/{bill_id}
                   Description: Enables biller to update a specific bill.
                   Headers: Authorization: Bearer <access_token>
                   req_body: {
                               "customer_id": 1,
                               "amount": 100.00,
                               "status": "pending"
                               "description": "This is a test bill"
                               "due_date": "2021-01-01T00:00:00"
                             }
                 
                   resp: {
                               "id": 1,
                               "customer_id": 1,
                               "amount": 100.00,
                               "status": "pending",
                         }
              
                - Read all bills by status
                   Identity: Biller/Admin/customers
                   Method: GET
                   URL:bills/api/v1/read_all_bills/{status}
                   Description: Enables billers and customers to read all bills by status but also admin could also use this api to read all bills maanged by different billers.
                   Headers: Authorization: Bearer <access_token>
                   req_body: None
                   resp: [
                               {
                                   "id": 1,
                                   "customer_id": 1,
                                   "amount": 100.00,
                                   "status": "pending",
                                   "created_at": "2021-01-01T00:00:00",
                                   "updated_at": "2021-01-01T00:00:00"
                               }, 
                               {
                                   "id": 2,
                                   "customer_id": 2,
                                   "amount": 200.00,
                                   "status": "pending",
                                   "created_at": "2021-01-01T00:00:00",
                                   "updated_at": "2021-01-01T00:00:00"    
                               }
                   ]
               - Remove bill by id
                  Identity: Biller/admin
                  Method: DELETE      
                  URL:bills/api/v1/delete_bill/{bill_id}
                  Description: Enables biller and admin to delete a specific bill by its id if the status is pending.   
                  Headers: Authorization: Bearer <access_token>
                  req_body: None
                  resp: {
                              status_code: 204
                  }
                 - List all bills created by a specific customer using customer id
                    Identity: Biller
                    Method: GET
                    URL:bills/api/v1/list_all_customer_bills/{customer_id}
                    Description: Enables biller to list all bills created by a specific customer.
                    Headers: Authorization: Bearer <access_token>
                    req_body: None
                    resp: [
                                {
                                    "id": 1,
                                    "customer_id": 1,   
                                    "amount": 100.00,
                                    "status": "pending",
                                    "created_at": "2021-01-01T00:00:00",    
                                    "updated_at": "2021-01-01T00:00:00"
                                },
                                {
                                    "id": 2,            
                                    "customer_id": 1,
                                    "amount": 200.00,
                                    "status": "pending",
                                    "created_at": "2021-01-01T00:00:00",
                                    "updated_at": "2021-01-01T00:00:00"
                            ]
                 - List all bills owned by a specific biller or customer
                    Identity: Biller/Customer
                    Method: GET
                    URL:bills/api/v1/list_all_biller_bills
                    Description: Enables biller or customer to list all bills owned by a specific biller or customer.
                    Headers: Authorization: Bearer <access_token>
                    req_body: None
                    resp: [
                                {
                                    "id": 1,
                                    "customer_id": 1,   
                                    "amount": 100.00,
                                    "status": "pending",
                                    "created_at": "2021-01-01T00:00:00",    
                                    "updated_at": "2021-01-01T00:00:00"
                                },
                                {
                                    "id": 2,            
                                    "customer_id": 1,
                                    "amount": 200.00,
                                    "status": "pending",
                                    "created_at": "2021-01-01T00:00:00",    
                                    "updated_at": "2021-01-01T00:00:00"
                                }
                                
                    ]
                 - List all bills created by all billers
                    Identity: Admin
                    Method: GET
                    URL:bills/api/v1/list_all_bills
                    Description: Enables admin to list all bills created by all billers.
                    Headers: Authorization: Bearer <access_token>
                    req_body: None
                    resp: [
                                {
                                    "id": 1,
                                    "customer_id": 1,
                                    "amount": 100.00,
                                    "status": "pending",
                                    "created_at": "2021-01-01T00:00:00",
                                    "updated_at": "2021-01-01T00:00:00"
                                }, 
                                {
                                    "id": 2,
                                    "customer_id": 2,
                                    "amount": 200.00,
                                    "status": "pending",
                                    "created_at": "2021-01-01T00:00:00",
                                    "updated_at": "2021-01-01T00:00:00"    
                                }         
                    ]
                   - List all bills created by a specific biller
                      Identity: Admin 
                      Method: GET                    
                      URL:bills/api/v1/list_all_bills/{biller_id}      
                      Description: Enables admin to list all bills created by a specific biller.
                      Headers: Authorization: Bearer <access_token>
                      req_body: None
                      resp: [
                                  {
                                      "id": 1,
                                      "customer_id": 1,
                                      "amount": 100.00,
                                      "status": "pending",
                                      "created_at": "2021-01-01T00:00:00",
                                      "updated_at": "2021-01-01T00:00:00"
                                  }, 
                                  {
                                      "id": 2,
                                      "customer_id": 2,
                                      "amount": 200.00,
                                      "status": "pending",
                                      "created_at": "2021-01-01T00:00:00",
                                      "updated_at": "2021-01-01T00:00:00"    
                                  }       
                      ]
                     - read report
                        Identity: Admin/biller/customer
                        Method: GET
                        URL:bills/api/v1/read_report  
                        Description: Enables admin to read report.
                        Headers: Authorization: Bearer <access_token>
                        req_body: None
                        resp: {
                                 if admin:
                                      admin_report
                                 else if biller:
                                      biller_report
                                 else if customer:
                                      customer_report
                     }
                
 ---
Bill data api's
===============
1. Create Bill — POST /api/v0.1/bills/


{
  "method": "POST",
  "url": "http://localhost:8000/api/v0.1/bills/",
  "headers": {
    "Authorization": "Bearer YOUR_JWT_TOKEN",
    "Content-Type": "application/json"
  },
  "body": {
    "biller_id": "uuid-string",
    "customer_id": "uuid-string",
    "amount": 123.45,
    "due_date": "2025-07-15T00:00:00Z",
    "status": "pending",
    "description": "Electricity bill for June"
  }
2. Read Bill by ID — GET /api/v0.1/bills/{bill_id}

{
  "method": "GET",
  "url": "http://localhost:8000/api/v0.1/bills/your-bill-uuid",
  "headers": {
    "Authorization": "Bearer YOUR_JWT_TOKEN"
  }
}
3. Update Bill by ID — PUT /api/v0.1/bills/{bill_id}
{
  "method": "PUT",
  "url": "http://localhost:8000/api/v0.1/bills/your-bill-uuid",
  "headers": {
    "Authorization": "Bearer YOUR_JWT_TOKEN",
    "Content-Type": "application/json"
  },
  "body": {
    "amount": 150.00,
    "status": "paid",
    "description": "Updated bill amount after adjustment"
  }
}
4. Delete Bill by ID — DELETE /api/v0.1/bills/{bill_id}
{
  "method": "DELETE",
  "url": "http://localhost:8000/api/v0.1/bills/your-bill-uuid",
  "headers": {
    "Authorization": "Bearer YOUR_JWT_TOKEN"
  }
}
5. Get Bills by Status — GET /api/v0.1/bills/status/{status}
{
  "method": "GET",
  "url": "http://localhost:8000/api/v0.1/bills/status/paid",
  "headers": {
    "Authorization": "Bearer YOUR_JWT_TOKEN"
  }
}
6. Get Bills by Customer ID — GET /api/v0.1/bills/customer/{customer_id}
{
  "method": "GET",
  "url": "http://localhost:8000/api/v0.1/bills/customer/customer-uuid",
  "headers": {
    "Authorization": "Bearer YOUR_JWT_TOKEN"
  }
}
7. Get Bills by Biller ID — GET /api/v0.1/bills/biller/{biller_id}
{
  "method": "GET",
  "url": "http://localhost:8000/api/v0.1/bills/biller/biller-uuid",
  "headers": {
    "Authorization": "Bearer YOUR_JWT_TOKEN"
  }
}
8.Get All Bills — GET /api/v0.1/bills/all
{
  "method": "GET",
  "url": "http://localhost:8000/api/v0.1/bills/all",
  "headers": {
    "Authorization": "Bearer YOUR_JWT_TOKEN"
  }
}
9.Get Own Bills — GET /api/v0.1/bills/my-bills
{
  "method": "GET",
  "url": "http://localhost:8000/api/v0.1/bills/my-bills",
  "headers": {
    "Authorization": "Bearer YOUR_JWT_TOKEN"
  }
}
10. Get Reports — GET /api/v0.1/bills/report
{
  "method": "GET",
  "url": "http://localhost:8000/api/v0.1/bills/report",
  "headers": {
    "Authorization": "Bearer YOUR_JWT_TOKEN"
  }
}


