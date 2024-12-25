Resource    |  URL     |    Parameter           |   Method |   Status Code
Register    | /register| username,pw            | Post     | 200,  301, 302
Add         | /Add     | username,pw,amount     | Post     | 200,   301, 302, 304
Transfer    | /transfer| username,pw,amount,to  | Post     | 200,   301, 302, 303, 304
CheckBalance| /balance | username,pw            | Post     | 200,   301, 302
TakeLoan    | /takeLoan| username,pw,amount     | Post     | 200,   301, 302, 304
PayLoan     | /payLoan | username,pw,amount     | Post     | 200,   301, 302, 304
debt        | /debt   | username,pw,amount     | Post     | 200,   301, 302, 304



status code description - 
200  - Ok
301  - Invalid username , user already exist
