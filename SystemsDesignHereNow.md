
# Systems Design: Here Now

 ### [View in Markdown Editor](https://goo.gl/dftdyx)

*An important aspect of being a software engineer is creating design documents for large projects. A design document is a way to solidify your thoughts and allow your co-workers to understand the project. It also allows them to make helpful comments to improve the final design. Design docs are rarely perfect, and this one's purpose is to serve as a solid point for a discussion if you come into our offices for an interview.*

Write a one-page design doc describing a service that keeps track of Foursquare users as they check in at different venues. In particular, this service will get informed of each check-in in real time (a user/venue pair) and must be able to answer the following queries in real time: 
1. Where is user A right now?
2. What users are at venue X right now?

The following business rules apply:
1. A user can only be at one venue at a time. If user A checks
in at venue X and then at venue Y, they are no longer at venue X.
2. A check-in only “lasts” for at most 3 hours. If user A checks
in at venue X and then does nothing for 3 hours, they are no
longer at venue X.

The service should have durable enough storage that you can
restart it without losing all of your data. It should not
store everything in memory.


## Functional Requirements
1. Service can determine a user's current venue.
2. Service can determine a venue's current users.



## Nonfunctional Requirements
1. Service should be highly available.
2. Service should be reliable and fault tolerant. Can restart it without losing all data.
3. Service should process data in real time with minimum latency.
4. Service should support a heavy read load.

CAP theorem states that in a distributed system, you can only prioritize two of three options:
* **Consistency** - All nodes see the same data at the same time
* **Availability** - Every request gets a response on success/failure
* **Fault Tolerance** - The system continues to work despite message loss or partial failure

This service will prioritize **availability and fault tolerance**. This is because the service should be durable enough that it
can be restarted without losing data. The real time requirement allows for eventual consistency where data is replicated asynchronously.

## Capacity Estimation
Foursquare claims there are about [50 million monthly unique users from both City Guide and Swarm][1].

As of 1.5 years ago there were roughly [8 million check-ins per day][2].

8 million / 3600 seconds = 92.59 check-ins per second

## Entity Relationships

These diagrams define and illustrate the relationship between a user, venue, and check-in. They are assumed to already exist elsewhere in the overall system. The service is a component of this system that gets informed of the UserID and VenueID on each check-in in real time.

![Diagram](https://i.imgur.com/vtfhX72.png)

![ERD](https://i.imgur.com/Jm1jyIs.png)


## Service Overview

The service will only handle processing of UserIDs and VenueIDs to determine the answers to the 2 queries.

The service must generate a VenueID for any given UserID and a list of UserIDs for any given VenueID as UserID / VenueID pairs are streamed in real time. It should also allow for expiration of the data that has reached the 3 hour time limit.

##### System APIs

getUserVenue(apiKey, userID)

Returns: venueID

getUsersAtVenue(apiKey, venueID)

Returns: list of userIDs

##### Messaging - Apache Kafka
In order to process the data from check-ins in real time, the service should make use of a stream processing platform. Because of the need for availability, reliability, and durability, Apache Kafka is the recommendation for the technology of choice to handle the check-in streams. Kafka does publish-subscribe messaging and acts as a broker between producers and consumers of message streams.

In the event of failure, it automatically balances consumers which makes it a better choice when compared to similar messaging services. It can scale quickly without incurring downtime, delivers high throughput, and provides intra-cluster replication by keeping messages on disks.



##### Database - Distributed Key-Value Store
For the persistence layer, a simple NoSQL Key-Value store could be maintained. NoSQL is better for this use case because the service can allow for eventual consistency. This will also help the service in terms of the data intensive workload, high throughput, and horizontal scalability.

A Distributed Fault-Tolerant Key-Value Store can be built using a database such as Apache Cassandra or Amazon DynamoDB.

When the user/venue pair is received for a check-in, two separate tables can be utilized for insertion.  The first table will be used to find where a certain user is and the other table can be used to determine what users are currently at a venue.

In order to support the expiration of check-in data after 3 hours, Cassandra and DynamoDB offer an automatic data expiration feature. The time to live value or TTL can be specified in seconds during insert and update statements. The exact duration in which a particular item gets deleted after expiration is specific to the nature of the workload and the size of the table. Deleting the expired entries can be achieved efficiently by having one bucket for interval of time.


##### Scaling

Caching and load balancing can be added to the service once there are multiple servers and to handle scaling issues if there were suddenly 100x more requests.

An in memory caching solution such as Redis or Memcached can be introduced in front of the persistence layer. Application logic can quickly check if the cache has any venueID or list of userIDs before touching the backend database.

A load balancing layer can be added either before the application logic, between the application servers and database, or in both places. Initially, a basic round robin approach would suffice but eventually a more advanced load balancer would be necessary that occasionally sends queries about load and adjusts traffic.


[1]: https://foursquare.com/about
[2]: https://www.wired.com/story/foursquare-may-have-grown-up-but-the-check-in-still-matters/
