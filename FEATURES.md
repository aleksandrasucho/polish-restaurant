# Polka Restaurant

## Features

Web application has the following pages:
- home page
- menu page
- information page
- login page
- signup page
- reset password page
- book a table page
- your reservations page
- edit your reservation page
- cancel your reservation page

### Access to pages according to the user role:

| Page Name                   | Customer | Admin   |
| --------------------------- | -------- | ------- |
| home page                   | Y        | Y       |
| menu page                   | Y        | Y       |
| information page            | Y        | Y       |
| login page                  | Y        | Y       |
| signup page                 | Y        | Y       |
| reset password page         | Y        | Y       |
| book a table page           | Y        | Y       |
| your reservations page      | Y        | Y       |
| edit your reservation page  | Y        | Y       |
| cancel your reservation page| Y        | Y       |

- Each page has a navbar and a footer

**Navbar**

![Navbar](documentation/features/navbar/navbar.png)

Navbar has the following links:
- home page
- ![home button](documentation/features/navbar/home-btn.png)
- menu page
- ![menu button](documentation/features/navbar/menu-btn.png)
- information page
- ![information button](documentation/features/navbar/information-btn.png)
- login page
- ![login button](documentation/features/navbar/login-btn.png)

The simplistic design of the navbar is based on the decision to make the use of the webapp easy for the user.

When the user is logged in, the navbar looks as follows.

- ![Navbar User logged in](documentation/features/navbar/navbar-loggedin.png)

It has an additional Book a Table page
- book a table
- ![book a table button](documentation/features/navbar/book-a-table-btn.png)

When the user is logged in and has existing reservations, the navbar looks as follows.

- ![Navbar User logged in](documentation/features/navbar/existing-reservations-navbar.png)

It has an additional Your Reservations page
- your reservations
- ![your reservations button](documentation/features/navbar/your-reservations-btn.png)
