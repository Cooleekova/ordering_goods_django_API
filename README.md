# API for automating purchases in retail network (Django)

**Users of the service:**
- the customer (purchase manager who orders goods for sale in the store)
- the supplier of goods

**What customer can do:**

- log in, register and recover password via API.
- make purchases according to the catalog, in which goods from several suppliers are presented 
  (in one order you can specify goods from different suppliers)

**What supplier can do:**

- inform the service about updating the price list through the API
- can enable and disable the acceptance of orders
- can receive a list of completed orders
