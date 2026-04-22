"""
6. routers/junction.py

POST /junction/invite — business owner invites retailer (auth required)
PATCH /junction/{id}/accept — retailer accepts invite (auth required)
PATCH /junction/{id}/block — business owner blocks retailer (auth required)
GET /junction/my-retailers — business owner gets all their retailers (auth required)


7. routers/products.py

POST /products/create — create product (auth required)
GET /products — get all products for a business
GET /products/{id} — get single product
PATCH /products/{id} — update product (auth required)
PATCH /products/{id}/toggle — toggle active/inactive (auth required)


8. routers/orders.py

POST /orders/create — retailer places order (auth required)
GET /orders — get all orders (auth required)
GET /orders/{id} — get single order (auth required)
PATCH /orders/{id}/confirm — business owner confirms (auth required)
PATCH /orders/{id}/reject — business owner rejects (auth required)
PATCH /orders/{id}/dispatch — business owner dispatches (auth required)
PATCH /orders/{id}/deliver — mark as delivered (auth required)


9. routers/order_items.py

POST /order-items/create — add item to order (auth required)
GET /order-items/{order_id} — get all items for an order (auth required)


10. routers/payments.py

POST /payments/create — record payment (auth required)
GET /payments/{order_id} — get all payments for an order (auth required)


11. routers/invoices.py

GET /invoices/{order_id} — get invoice for an order (auth required)


12. routers/accounting_ledger.py

GET /ledger — get full ledger for a business (auth required)
GET /ledger/{retailer_id} — get ledger for specific retailer (auth required)


13. routers/conversations.py

POST /conversations/create — start a conversation (auth required)
GET /conversations — get all conversations (auth required)


14. routers/messages.py

POST /messages/create — send a message (auth required)
GET /messages/{conversation_id} — get all messages in a conversation (auth required)


15. routers/notifications.py

GET /notifications — get all notifications for current user (auth required)
PATCH /notifications/{id}/read — mark as read (auth required)


16. routers/reviews.py

POST /reviews/create — leave a review (auth required)
GET /reviews/{business_id} — get all reviews for a business


17. routers/sessions.py

GET /sessions — get all active sessions for current user (auth required)
DELETE /sessions/{id} — revoke a specific session (auth required)


18. routers/analytics_events.py

POST /analytics/log — log an event (auth required)
GET /analytics/dashboard/{business_id} — get dashboard data (auth required)
"""