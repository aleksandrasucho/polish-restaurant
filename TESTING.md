# Testing

## Manual Testing

Testing was done throughout site development, for each feature before it was merged into the master file.

Usability was tested with the below user acceptance testing, sent to new users to ensure testing from different users, on different devices and browsers to ensure issues were caught and where possible fixed during development.

|     | User Actions           | Expected Results | Y/N | Comments    |
|-------------|------------------------|------------------|------|-------------|
| Sign Up     | 
| 1           | Click on Sign Up button | Redirection to Sign Up page | Y |          |
| 2           | Click on the Login link in the form | Redirection to Login page | Y |          |
| 3           | Enter valid email | Field will only accept email address format | Y |          |
| 4           | Enter valid username | Field will only accept no more than 50 characters | Y |          |
| 5           | Enter valid Full Name | Field will only accept no more than 30 characters | Y |          |
| 6          | Enter valid password | Field will only accept secure passwords | Y |          |
| 7          | Enter valid password confirmation | Field will only accept the same password from the previous field | Y |          |
| 8          | Click on the Sign Up button | Takes user to the home page as a logged in user | Y |          |           |
| 9          | Click "Logout" | Takes user to log out page to confirm logout | Y |          |
| 10          | Click "Logout" button  in the center of the page| Redirects user to home page | Y |          |
| Log In      |                        |                  |      |             |
| 1           | Click on Login button | Redirection to Login page | Y |          |
| 2           | Click on the SignUp link in the form | Redirection to SignUp page | Y |          |
| 3           | Enter valid email or username | Field will only accept email address format | Y |          |
| 4           | Enter valid password | Field will only accept secure passwords | Y |          |
| 5           | Click on the Sign In button | Takes user to schedule page with pop-up confirming successful sign in. Get started button now missing in main nav, replaced by Menu | Y |          |
| 6           | Clicks "Forgot Password" instead of "Sign In" | Redirects user to forgot password page | Y |          |
| 7           | Click "Logout" | Takes user to log out page to confirm logout | Y |          |
| 8           | Click "Logout" button  in the center of the page| Redirects user to home page | Y |          |
| Menu        |                        |                  |      |             |
| 1           | Click on the "Menu" button | Redirection to Menu Page |
| 2           | Click on "Home" | Redirection to Home Page | Y | Available to everyone |
| 3           | Click on "Information" | Redirection to Information page | Y | Available only to bosses and sales managers |
| 4           | Click on "Book a Table" | Redirection to Make a Reservation page| Y | Available only to logged in users |
| 5           | Click on "Your Reservations" | Redirection to Reservation Details page | Y | Available only to logged in users with existing reservations |
| 6           | Click on "Logout" button in the center of the page | Takes user to log out page to confirm logout | Y | Available to everyone |
| Home       |                        |                  |      |             |
| 1           | Click on "Book a Table" | Redirection to Make a Reservation page | Y | Available to logged in users |
| 2           | Click on "Log in to Book a Table" | Redirection to Login page | Y | Available to everyone |
| 3           | Click on the "Menu" button | Redirection to Menu Page |
| 4           | Click on "Home" | Redirection to Home Page | Y | Available to everyone |
| 5           | Click on "Information" | Redirection to Information page | Y | Available only to bosses and sales managers |
| 6           | Click on "Book a Table" | Redirection to Make a Reservation page| Y | Available only to logged in users |
| 7           | Click on "Your Reservations" | Redirection to Reservation Details page | Y | Available only to logged in users with existing reservations |
| 8           | Click on "Logout" button in the center of the page | Takes user to log out page to confirm logout | Y | Available to logged in users|
| Information      |                        |                  |      |             |
| 1           | Click on the "Menu" button | Redirection to Menu Page |
| 2           | Click on "Home" | Redirection to Home Page | Y | Available to everyone |
| 3           | Click on "Information" | Redirection to Information page | Y | Available only to bosses and sales managers |
| 4           | Click on "Book a Table" | Redirection to Make a Reservation page| Y | Available only to logged in users |
| 5           | Click on "Your Reservations" | Redirection to Reservation Details page | Y | Available only to logged in users with existing reservations |
| 6           | Click on "Logout" button in the center of the page | Takes user to log out page to confirm logout | Y | Available to logged in users|
| Book a Table       |                        |                  |      |             |
| 1           | Click on the "Menu" button | Redirection to Menu Page |
| 2           | Click on "Home" | Redirection to Home Page | Y | Available to everyone |
| 3           | Click on "Information" | Redirection to Information page | Y | Available only to bosses and sales managers |
| 4           | Click on "Book a Table" | Redirection to Make a Reservation page| Y | Available only to logged in users |
| 5           | Click on "Your Reservations" | Redirection to Reservation Details page | Y | Available only to logged in users with existing reservations |
| 6           | Click on "Submit Reservation" | Redirection to Reservation Details page | Y | Available only to logged in users|
| 7           | Click on "Logout" button in the center of the page | Takes user to log out page to confirm logout | Y | Available to logged in users|
| Your Reservations       |                        |                  |      |             |
| 1           | Click on the "Menu" button | Redirection to Menu Page |
| 2           | Click on "Home" | Redirection to Home Page | Y | Available to everyone |
| 3           | Click on "Information" | Redirection to Information page | Y | Available only to bosses and sales managers |
| 4           | Click on "Book a Table" | Redirection to Make a Reservation page| Y | Available only to logged in users |
| 5           | Click on "Your Reservations" | Redirection to Reservation Details page | Y | Available only to logged in users with existing reservations |
| 6           | Click on "Logout" button in the center of the page | Takes user to log out page to confirm logout | Y | Available to logged in users|
| 7           | Click on "Edit" | Takes user to update his reservation | Y | Available to logged in users|
| 8           | Click on "Cancel" | Takes user to ucancel his reservation | Y | Available to logged in users|
| Update Profile |            |                  |      |             |
| 1           |  Change the form data for the first name, last name, time or date | Date in the form will be updated | Y | Available only when the user is logged in and has a reservation created  |
| 2           |  Click "update" button | Redirect back to user profile+data will be updated in the database | Y | Available only when the user is logged in and has a reservation created |
|Delete Profile |            |                  |      |             |
| 2           |  Click "cancel" button | Redirect back to user profile | Y | Available only when the user is logged in and has a reservation created  |
| 3           |  Click "delete" button | Redirect to home page | Y | Available only when the user is logged in and has a reservation created  |
| Reset Password |            |                  |      |             |
|1                | Enter valid email | Field will only accept valid email address | Y |  Available to everyone |
