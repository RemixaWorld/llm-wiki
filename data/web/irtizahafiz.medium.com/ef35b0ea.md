---
domain: irtizahafiz.medium.com
fetch_date: '2026-05-18T12:57:09.087102'
status: ok
url: https://irtizahafiz.medium.com/protecting-against-bot-attacks-using-nginx-rate-limits-12872fcbaafd
---

# Protecting Against Bot Attacks Using Nginx Rate Limits

## Implement custom rate limits per API endpoint.

I wasn’t surprised to see my website hit by **bot traffic** within a couple of weeks of *being live.*

Self-hosting all the systems powering my online presence in a single Digital Ocean server means when my machine is the victim of a **Distributed Denial-of-Service (DDoS)** attack, real users cannot access my site.

To prevent that, I had to quickly set up some basic rate limits. I needed to quickly put something together before I eventually moved to a more distributed system with a load balancer (coming up in the next few weeks).

Let’s start with defining the concept of “rate limit”.

**Rate Limiting** allows you to limit the amount of **HTTP requests** a user (or machine) can make in a given period. It stops your server from wasting valuable resources, and at worst, stops your servers from becoming overwhelmed and unresponsive.

I am hosting both my NextJS website and Python FastAPI API on Digital Ocean clusters with Nginx servers as gateways.

That’s why, the easiest solution was to implement a rate limit using Nginx. Luckily, Nginx provides a **comprehensive toolkit** to implement complex rate limit policies.

Now that you understand “rate limits”, let me walk you through the steps I took to protect my website against bot traffic.

**HTTP Routes to Rate Limit**

I primarily expose 2 HTTP routes to the public internet.

`GET https://irtizahafiz.com`

GET https://api.irtizahafiz.com/recommendations

The first route serves my website whenever someone goes to irtizahafiz.com.

The second is an API route used by my website to support **“smart search” **functionality.

If the first route is overwhelmed by bot traffic, people cannot access my site.

If the second route is overwhelmed by bot traffic, it could cost me $$$, because the /recommendations route uses OpenAI’s Embeddings API on the backend to fetch recommendations for the user.

Either way, it’s not good news!

So, let’s see how I quickly bootstrapped a rate limit system using Nginx. Surely, it’s not perfect, and it’s fairly easy to circumvent the rate limit. But, at least so far, it has prevented the early surge of bot traffic I was seeing.

In the future, I will move to a more distributed architecture, or use Cloudflare for stronger protection.

**Configuring Rate Limits Using Nginx**

First, let’s look at the Nginx config file.

`limit_req_zone $binary_remote_addr zone=mylimit:10m rate=10r/s;`

server {

listen 443 ssl;

server_name irtizahafiz.com;

location / {

limit_req zone=mylimit burst=20 nodelay;

limit_req_status 427;

proxy_pass http://127.0.0.1:3000;

}

ssl_certificate /etc/letsencrypt/live/irtizahafiz.com/fullchain.pem;

ssl_certificate_key /etc/letsencrypt/live/irtizahafiz.com/privkey.pem;

include /etc/letsencrypt/options-ssl-nginx.conf;

ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

}

There are 3 Nginx directives used to implement rate limit — `limit_req_zone`

, `limit_req`

, and `limit_req_status`

.

According to Nginx’s official documentation — the `limit_req_zone`

directive defines the parameters for rate limiting while `limit_req`

enables rate limiting within the context of where it appears (example — my route https://irtizahafiz.com/).

Zooming into the limit_req_zone directive:

`$binary_remote_addr`

— The characteristic or “key” against which the rate limit is implemented. In this case, I am using the binary representation of the user’s IP address. In other words, I am rate-limiting**by IP address.**`zone=mylimit:10m`

— We are allocating 10MB to store the IP address-related information needed to rate limit successfully.`rate=10r/s`

— Sets the maximum at**10 requests per second**.

Now, let’s look at the limit_req directive inside the location block:

`zone=mylimit`

— Uses the same shared memory defined in the top level.`burst=20`

— Allows bursty traffic by queueing up to 20 requests, before the server starts sending HTTP status code 427.

For both burst and `nodelay`

, the Nginx official documentation does a brilliant job explaining, so check that out if you want to learn more.

For the keen reader, you will have noticed that I haven’t talked about rate-limiting my API yet. That’s because it uses the same logic. Here’s what the nginx configuration looks like for my API server block.

`server {`

listen 443 ssl;

server_name api.irtizahafiz.com;

location /recommendations {

limit_req zone=mylimit burst=20 nodelay;

limit_req_status 427;

proxy_pass http://127.0.0.1:10000;

}

location / {

# Deny access to all other routes

return 404;

}

ssl_certificate /etc/letsencrypt/live/irtizahafiz.com/fullchain.pem;

ssl_certificate_key /etc/letsencrypt/live/irtizahafiz.com/privkey.pem;

include /etc/letsencrypt/options-ssl-nginx.conf;

ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

}

Once again, I am using the same 10 requests/second rate limit, allowing bursts of up to 20 requests without any delay in response.

Lastly, the limit_req_status tells Nginx to respond with HTTP status code 427 when rate-limiting users. Otherwise, Nginx defaults to 503s which can be difficult to interpret.

**Closing Thoughts**

If you have made it this far, I hope you found this valuable.

Here are a few ways you can do so: follow me on Medium, subscribe to my website, or follow me on YouTube.
