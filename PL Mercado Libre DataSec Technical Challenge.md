**Mercado Libre DataSec Technical**

**Challenge**

> **Instructions**

-   Create a separate file for each question.

-   Commit all the solutions to a single public GitHub repository.

-   Solve all the questions using python 3. Specify in the comments the
    > exact version of python you used.

**Assignments**

1.  **REST API: Highest International Students**

Use the HTTP GET method to retrieve information from a database of
universities across the globe. Query
https://jsonmock.hackerrank.com/api/universities to find all the
records. The query result is paginated and can be further accessed by
appending to the query string ?page=num where num is the page number.

The response is a JSON object with the following 5 fields:

-   page: The current page of the results. (Number)

-   per_page: The maximum number of results returned per page. (Number)

-   total: The total number of results. (Number)

-   total_pages: The total number of pages with results. (Number)

-   data: Either an empty array or an array with a single object that
    > contains the universities\' records.

Example of a data array object:

*\"university\": \"King\'s College London\",*

*\"rank_display\": \"35\",*

*\"score\": 82,*

*\"type\": \"Public\",*

*\"student_faculty_ratio\": 7,*

*\"international_students\": \"15,075\",*

*\"faculty_count\": \"4,216\",*

*\"location\": {*

> *\"city\": \"London\",*
>
> *\"country\": \"United Kingdom\",*
>
> *\"region\": \"Europe\"*

*}*

In data, each university has the following schema:

-   university: The name of the university (String)

-   rank_display: The rank of the university according to the 2022 QS
    > Rankings (String).

-   score: The score of the university according to the 2022 QS Rankings
    > (Number).

-   type: The type of university (String)

-   student_faculty_ratio: The ratio of number of students to the number
    > of faculty. (Number)

-   international_students: The number of international students
    > (String).

-   faculty_count: The number of faculty (String

-   location: An object containing the location details. The object has
    > the following schema:

-   city: (String)

-   country: (String)

-   region: (String)

Complete the highestInternationalStudents function were given the name
of two cities as parameters, return the name of the university with the
highest number of international students in the first city. If the first
city does not have a university within the data, return the university
with the highest number of international students in the second city.

**[Function Description]{.underline}**

Complete the function highestInternationalStudents.

-   **highestInternationalStudents** has the following parameters:

    -   string firstCity: name of the first city

    -   string secondCity: name of the second city

-   **Return:** string: the university with the highest number of
    > international students.

-   **Constraints:** There is always a university in one of the two
    > cities.

**[Sample Input]{.underline}**

-   *Pune*

-   *New Delhi*

**[Sample Output:]{.underline}**

-   *Indian Institute of Technology Delhi (IITD)*

**[Explanation:]{.underline}**

-   Since Pune does not have a university in the list, the university
    > with the highest international students in Delhi is printed.

2.  **SQL: Advertising System Failures Report**

As part of HackerAd\'s advertising system analytics, a team needs a list
of customers who have a maximum number of failure events (status =
\"failure\") in their campaigns.

For all customers with more than 3 events with status = \'failure\',
report the customer name and their number of failures.

The result should be in the following format: customer, failures.

-   customer is a candidate\'s full name, the first_name and last_name
    > separated by a single space.

-   The order of the output is not important.

**Schemas:** There are 3 tables:

  -----------------------------------------------------------------------
  **customers**                            
  ----------------- ---------------------- ------------------------------
  **name**          **type**               **description**

  id                SMALLINT               Customer ID

  first_name        VARCHAR(64)            Customer First Name

  last_name         VARCHAR(64)            Customer Last Name
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------
  **campaigns**                                
  -------------------- ----------------------- --------------------------
  **name**             **type**                **description**

  id                   SMALLINT                Campaign ID

  customer_id          SMALLINT                Customer ID

  name                 VARCHAR(64)             Campaign Name
  -----------------------------------------------------------------------

  ------------------------------------------------------------------------
  **events**                                    
  ------------------- ------------------------- --------------------------
  **name**            **type**                  **description**

  dt                  VARCHAR(19)               Event Timestamp

  campaign_id         SMALLINT                  Campaign ID

  status              VARCHAR(64)               Event Status
  ------------------------------------------------------------------------

  ------------------------------------------------------------------------
  **customers**                               
  --------------- --------------------------- ----------------------------
  **id**          **first_name**              **last_name**

  1               Whitney                     Ferrero

  2               Dickie                      Romera
  ------------------------------------------------------------------------

**[Sample Data:]{.underline}**

Replicate the following data in a local MySQL instance

  -----------------------------------------------------------------------------
  **campaigns**                        
  --------------- -------------------- ----------------------------------------
  **id**          **customer_id**      **name**

  1               1                    Upton Group

  2               1                    Roob, Hudson and Rippin

  3               1                    McCullough, Rempel and Larson

  4               1                    Lang and Sons

  5               2                    Ruecker, Hand and Haley
  -----------------------------------------------------------------------------

  ------------------------------------------------------------------------
  **events**                                          
  ----------------------------- --------------------- --------------------
  **dt**                        **campaign_id**       **status**

  2021-12-02 13:52:00           1                     failure

  2021-12-02 08:17:48           2                     failure

  2021-12-02 08:18:17           2                     failure

  2021-12-01 11:55:32           3                     failure

  2021-12-01 06:53:16           4                     failure

  2021-12-02 04:51:09           4                     failure

  2021-12-01 06:34:04           5                     failure

  2021-12-02 03:21:18           5                     failure

  2021-12-01 03:18:24           5                     failure

  2021-12-02 15:32:37           1                     success

  2021-12-01 04:23:20           1                     success

  2021-12-02 06:53:24           1                     success

  2021-12-02 08:01:02           2                     success

  2021-12-01 15:57:19           2                     success

  2021-12-02 16:14:34           3                     success

  2021-12-02 21:56:38           3                     success

  2021-12-01 05:54:43           4                     success

  2021-12-02 17:56:45           4                     success

  2021-12-02 11:56:50           4                     success

  2021-12-02 06:08:20           5                     success
  ------------------------------------------------------------------------

The expected output is:

  -----------------------------------------------------------------------
  **customer**                              **failures**
  ----------------------------------------- -----------------------------
  Whitney Ferrero                           6

  -----------------------------------------------------------------------
