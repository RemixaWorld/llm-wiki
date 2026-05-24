---
domain: intoai.pub
fetch_date: '2026-05-18T12:37:56.314369'
status: ok
url: https://intoai.pub/p/10-must-know-concepts-for-ai-engineers
---

# 10 Must-Know Concepts For AI Engineers To Build Better Systems

### CAP Theorem, Design Patterns, Big-O Notation, and more

AI engineers are in great demand today.

According to a McKinsey survey, 78 percent of respondents said that their organizations used AI in at least one business function in 2025, up from 72 percent in early 2024 and 55 percent a year earlier.

What makes a great AI engineer is someone who can think systematically and build reliable systems that can scale while being secure at the same time.

Yes, you do need to have the specialized knowledge for AI Engineering. Still, the fundamentals of Computer Science and Software Engineering must be at the core of your understanding and thinking process.

As mentioned by Anton Bacaj in the book “AI Engineering” by Chip Huyen:

“AI Engineering is just Software Engineering with AI models thrown in the stack.”


Here are 10 concepts that you must know as an AI/ML engineer for building better systems.

All the images used in this article are taken from my books:

*Let’s begin!*

### 1. CAP Theorem

To understand the CAP theorem, one must first understand these three terms in Distributed Computing:

**Consistency**: The system of all machines connected in a distributed manner sees the same data at the same time.**Availability**: The degree to which a system remains operational and responsive to requests.**Partition Tolerance:**The capability of a system to continue operating despite network failures between the connected machines.

The CAP theorem tells that in a distributed system, you can guarantee **at most two out of these three** properties (Consistency, Availability, and Partition tolerance) but **never all three simultaneously.**

### 2. Big-O Notation

The Big-O Notation is a mathematical way of describing the worst-case time or space complexity of an algorithm as the input size grows.

For example, the **Time complexity **of the self-attention mechanism of Transformers is `O(n²d)`

where `n`

is the sequence length and `d`

is the model dimension, making them quadratically expensive with longer sequences.

The **Space complexity** of self-attention is `O(n²)`

for storing the attention matrix plus `O(nd)`

for storing token representations and projections.

### 3. ACID vs. BASE Transactions

The acronym ACID stands for:

**Atomicity**: A transaction either completes entirely or fails completely, and no partial transactions occur.**Consistency**: A system remains in a valid state before and after each transaction, as per all rules and constraints.**Isolation**: Transactions running in parallel do so as if they’re the only ones executing. No two transactions interfere with each other’s intermediate states.**Durability**: Once a transaction is committed, its changes are permanently saved and will not be affected by system failures.

The acronym BASE stands for:

**Basically Available**: The system stays up and running even when parts of it fail, though some data may be temporarily inaccessible.**Soft State**: Data can be temporarily inconsistent across different parts of the system. These temporary inconsistencies are resolved at a later time.**Eventual Consistency**: Given enough time, all parts of the system will sync up and eventually converge to the same consistent state.

Relational databases (SQL databases) use ACID transactions to maintain strict data integrity and relationships.

NoSQL databases, on the other hand, use BASE transactions to achieve high scalability and performance by relaxing consistency requirements.

### 4. **Concurrency vs. Parallelism**

Many engineers confuse these terms, so it's important to understand their meanings clearly.

Parallelism means executing multiple tasks together, across different processor cores or machines, at the same time.

Concurrency means executing multiple tasks at the same time, either by running them in parallel or by rapidly switching between them on the same processor core.

Parallelism is a subset of Concurrency.

### 5. Horizontal vs. Vertical Scaling

Horizontal Scaling means adding more machines or servers to handle increased load by distributing work across them.

Horizontal Scaling means ‘Scaling out’ to different machines.


Vertical Scaling means increasing the power of existing machines by adding more CPU, RAM, or storage to handle increased load.

Vertical Scaling means ‘Scaling up’ existing machines.


### 6. SOLID Principles

SOLID is an acronym that gives the guidelines for writing clean and maintainable code that is easy to understand, test, and modify without breaking existing functionality.

Its components are:

**Single Responsibility**: One must not mix different responsibilities in the same class, and each class should do only one job.**Open/Closed**: One should be able to add new features without changing existing code that already works.**Liskov Substitution**: If one replaces a parent object with a child object, everything should still work the same way.**Interface Segregation**: One must not force classes to implement methods that they don’t need.**Dependency Inversion**: High-level code shouldn’t directly depend on low-level details, and abstractions must be used as a middle layer.

### 7. Latency & Throughput

Latency is the time it takes to complete a single request or task from start to finish.

Throughput is the number of requests or tasks a system can handle per unit of time.

### 8. Authentication & Authorization

Authentication is the process of verifying one’s identity through credentials like passwords, tokens, or biometrics.

Authorization is the process of determining what one is allowed to do by checking their permission to access specific resources or perform certain actions.

### 9. Monolith vs. Microservices

Monolith is a unified architecture where all components of an application are tightly integrated and deployed together as one unit.

With Microservices architecture, one breaks down an application into small, independent services that communicate over networks and can be developed, deployed, and scaled separately.

### 10. Design Patterns

Design patterns are reusable templates for solving common programming problems, which help make code easier to organize and maintain.

There are three main categories of design patterns that represent the three fundamental aspects of object-oriented programming:

**1. Creational design patterns**: Focus on how objects are created

**2. Structural design patterns**: Deal with how classes and objects are composed to form larger structures

**3. Behavioral design patterns**: Focus on communication and responsibility between objects

*Learn Systems Design and Computer Science visually! *

*Check out my visual tech guides using the links below and grab them at a special 20% discount using the coupon code “ BETTERENGINEER”.*

https://open.substack.com/pub/hamtechautomation/p/a-battle-tested-sredevops-engineers?r=64j4y5&utm_campaign=post&utm_medium=web
