| Column Name               | Description                                          | Value Type  | Valid Data Regex / Allowed Values                  |
|---------------------------|------------------------------------------------------|-------------|----------------------------------------------------|
| CustomerID                | Unique customer identifier                          | Categorical | `CUST\d{3}`                                        |
| Age                       | Age of the customer in years                        | Numerical   | `\d{1,3}`                                          |
| Gender                    | Gender of the customer                              | Categorical | Male, Female, Other                                |
| Income (Monthly)          | Monthly income of the customer                      | Numerical   | `\d+(\.\d+)?`                                      |
| Location                  | Customer's city location                            | Categorical | Berlin, Hamburg, Cologne, Frankfurt                |
| Purchase Frequency        | Number of purchases in a period                     | Numerical   | `\d+`                                              |
| Avg. Transaction Value    | Average value per transaction                       | Numerical   | `\d+(\.\d+)?`                                      |
| Loyalty Program Member    | Whether the customer is in loyalty program          | Categorical | Yes, No                                            |
| Tenure (Months)           | How long they've been a customer (in months)        | Numerical   | `\d+`                                              |
| Last Purchase Date        | Date of the last purchase                           | Date        | `\d{4}-\d{2}-\d{2}`     yyyy-mm-dd                           |
| Total Spend (6M)          | Total spending in last 6 months                     | Numerical   | `\d+(\.\d+)?`                                      |
| Visit Recency (Days)      | Days since last visit                               | Numerical   | `\d+`                                              |
| Preferred Category        | Product category most often purchased               | Categorical | Grocery, Home, Beauty, Electronics                 |
| Engagement Score          | Score representing user interaction                 | Numerical   | `\d+(\.\d+)?`                                      |
| Value Score               | Score indicating customer value                     | Numerical   | `\d+(\.\d+)?`                                      |
| Retention Risk Score      | Score estimating likelihood of customer churn       | Numerical   | `\d+(\.\d+)?`                                      |
| Overall Customer Index    | Composite score for customer performance            | Numerical   | `\d+(\.\d+)?`                                      |
