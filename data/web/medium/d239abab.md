---
domain: levelup.gitconnected.com
fetch_date: '2026-05-18T12:45:25.774563'
status: ok
url: https://levelup.gitconnected.com/build-a-personal-ai-tech-news-agent-94e7a2e508fe
---

# Build a Personal AI Tech News Agent

## NATURAL LANGUAGE PROCESSING IN APPLICATIONs

# Build a Personal AI Tech News Agent

## That will crawl tech sites and summarize key trends based on your preferences

[ ![Ida Silfverskiöld](https://miro.medium.com/v2/resize:fill:64:64/1*-PJYZEnMvuSpoVNkHyVeZg.png) ](<https://medium.com/@ilsilfverskiold?source=post_page---byline--94e7a2e508fe--------------------------------------->)

[Ida Silfverskiöld](<https://medium.com/@ilsilfverskiold?source=post_page---byline--94e7a2e508fe--------------------------------------->)

14 min read

·

Feb 22, 2024

\--

Listen

Share

More

Press enter or click to view image in full size

Get the trending keywords and sources → make an LLM summarize for you

_If you’re not a member but want to read this article, see this friend link_[ _here._](</build-a-personal-ai-tech-news-agent-94e7a2e508fe?sk=f4c3a49ec3b10d38c1c0f5deafa19990>)

You’d think that building something like this in the era of AI would be easy. However, just because we have access to high-performing LLMs doesn’t mean that it doesn’t need structured data to perform.

What we’re trying to build here is a personalized tech report bot that will **run daily and weekly** and that will **summarize tech trends and news based on what the tech community is sharing and talking about.**

It should be built with **your personal preferences** in mind so we can decide how condensed the summaries should be and what it should focus on.

The data we’re using to help it perform is an API that crawls tech sites, extracts keywords, and aggregates them to help us see what is trending within various categories.

Press enter or click to view image in full size

Simplified API process for the reversed keyword search bot

The idea is to query the API and programmatically set up the sources that should be fed into an LLM, based on the trending metrics and our preferences, helping it summarize the correct data.

Press enter or click to view image in full size

Every keywords has ids attached to it so we can get the search content for it

If you’re keen to create a search API like this, check out this previous post [here](<https://medium.com/gitconnected/predicting-tech-trends-with-natural-language-processing-9d9ce1c082d3>). This goes into a bit more detail on how it’s created.

In that article, I talk about using open-source NLPs to extract keywords and categorize them to analyze and link back to thousands of texts. I’ve also talked about fine-tuning your own NLP models [here](<https://medium.com/gitconnected/fine-tune-smaller-nlp-models-with-hugging-face-for-specific-use-cases-1745813471dc>) and have open-sourced the model that helped build the API [here](<https://huggingface.co/ilsilfverskiold/tech-keywords-extractor>).

However, to follow along you don’t need to create this one from scratch.

I’m more interested in the end result that will build on this API and that can create a news report that will look something like this.

Press enter or click to view image in full size

The report is a short snippet of what we receive back. There are up to ten categories to choose from, and obviously, there are endless keywords to pick for what you want the tech bot to look out for on a daily or weekly basis.

You can find a full-length example of a report [here](<https://github.com/ilsilfverskiold/ai-tech-news-bot/blob/main/example_email.md>). You can tweak it to have it look like you want it though. It can only focus on one category or only a few keywords.

Remember, this is an LLM doing the work for us, summarizing the sources it will be given with the data within each category, so there is no human curating this newsletter or report. It’s data and then there is the LLM.

Except for the architecture. That’s all us.

## Introduction

We’re not using low-code tools here, so it might be a stretch for some folks who are completely new to coding to understand this. However, the code itself will be prepared for you, and all you will need to do is tweak the configuration with your preferences. You do, though, need a free[ AWS account](<https://aws.amazon.com/>).

The full tutorial will take about 5 to 10 minutes. The only costs associated with this are the OpenAI tokens.

You’ll find the repository we’ll be using [here](<https://github.com/ilsilfverskiold/ai-tech-news-bot>).

I’ll go through a brief introduction as well as the architecture of the bot, then we’ll start building it.

### Some Q&A

**How technical do you have to be for this?** Not very technical, although we’re using the Serverless Framework to deploy to AWS, so it’s good for you to have an AWS account set up from the start.

**How much does it cost?** We’re not exceeding the AWS free tier for this, so the cost will be for the LLM tokens — in this case, GPT-3.5. One report usually costs $0.05 or less, depending on the number of categories and keywords I’m asking it to scout for per day.

**What’s the time investment?** Not very large, as I’ve already prepared the code for myself, and you can grab it as is. You may want to tweak it to your preferences, though.

### Infrastructure

The majority of the work has been done before I got to this point, building the API itself. Now, we’re just taking advantage of this data that we have.

To build this tech bot, though, we’ll use **AWS Lambda** for the function and **AWS EventBridge** to run it on a schedule, every weekday at 10 UTC. We’ll use the **Serverless Framework to deploy to AWS** , as it simplifies the process.

Our language of choice is **python** for this one.

Press enter or click to view image in full size

We deploy our python code via the Serverless framework to AWS

To send emails, we’ll use **AWS Simple Email Service** , but you can naturally use your medium of choice.

If you want updates in Slack or via WhatsApp, tweak the code to send you info there instead. However, I’m only showing you how to send emails for this tutorial.

**What about the API for the data?** The API that gets us data you can read more about [here](<https://medium.com/gitconnected/predicting-tech-trends-with-natural-language-processing-9d9ce1c082d3>), where you can create one on your own. For this, though, you can use the one I use, as it’s free and costs me minimally to keep, thanks to using small, fine-tuned NLP models.

I’ve previously open-sourced the [NLP model](<https://huggingface.co/ilsilfverskiold/tech-keywords-extractor>) that extracts the keywords, so it’s fully possible to create your own as well.

To see the data we have to work with you can do a quick API call for the table endpoint.

```bash curl -X GET \ "https://safron.io/api/table?period=daily&sort=trending" ```

This should get you the amount of keywords the NLP models picked up yesterday from various tech websites, and sort the trending keywords first.

To get search results for specific **keywords** or **row_ids** you’ll use the sources endpoint.

```bash curl -X POST \ -H "Content-Type: application/json" \ -d '{"keywords": ["ChatGPT", "AI"]}' \ "https://safron.io/api/sources" ```

This would get you sources or search results from the last 6 days based on the keywords ‘AI’ and ‘ChatGPT.’ You have the ability to control for dates and sources as well here.

In this application though, to build these newsletters, we’re using ids rather than keywords in the JSON body of the request. You can peak into the code in the [repository](<https://github.com/ilsilfverskiold/ai-tech-news-bot/blob/main/helper_functions.py>) to see how it is done.

**What about the larger LLM?** Lastly, we’re incorporating a larger LLM that we’re feeding data to, which is up to you if you’d like to use an open-source one. However, for simplicity, I’m using the new GPT-3.5-turbo-1205 model that OpenAI just released.

You would, though, need a large enough model to perform well for this part so I would suggest you start with GPT-3.5, Claude Haiku or Mistral Medium. You’ll need a large context window of at least 16k.

## Technical Bits

To build this, we’ll need a few things.

You’ll need an AWS account. If you don’t already have one, go ahead and create one. You won’t exceed the free tier for this project, but setting up billing alerts is good practice.

Make sure you have NodeJS, npm, and Python installed locally. Also having Postman is good for testing the API, but not essential.

The steps to complete this application are as follows.

1. Configure an **IAM user** in AWS
2. Obtain an **OpenAI API key**
3. Set up a **local environment**
4. Test the**data** from the **API**
5. Set up **personal preferences** for the bot
6. Set up **AWS SES** for emails
7. **Deploy** the application to run on a schedule

### AWS Configuration

First we need to set up an IAM user in the AWS Console.

Navigate to **IAM.** Create a new user and name it whatever you’d like. It will **not** need access to the management console.

Under permissions, you are looking for `attach policies directly` and then create policy.

Press enter or click to view image in full size

Under specify permissions choose JSON and paste in the permissions below.

```json { "Version": "2012-10-17", "Statement": [ { "Sid": "VisualEditor0", "Effect": "Allow", "Action": [ "iam:GetRole", "events:DescribeRule", "apigateway:*", "s3:*", "logs:*", "events:PutRule", "events:RemoveTargets", "events:PutTargets", "events:DeleteRule", "iam:CreateRole", "cloudformation:*", "iam:AttachRolePolicy", "iam:PutRolePolicy", "events:PutTargets", "iam:PassRole", "lambda:*", "iam:TagRole", "iam:UntagRole" ], "Resource": "*" } ]} ```

This involves a broad set of permissions, which you should always cautious of. However, Serverless will need quite a few permissions for everything to go smoothly. You can try to look through the Serverless documentation to see if it’s possible to set a more granular set of permissions; otherwise, we’ll continue.

Name the policy something meaningful and click ‘Save’. I named mine `serverless`.

You may need to recreate the IAM user to see the policy, but it should appear if you reload the page.

Press enter or click to view image in full size

Create the user, then click on it to find where you can generate an access key.

Choose **‘Local Code’** when asked what you are intending to use it for, and download the .csv file. We’ll need these credentials later for Serverless to create our application.

I usually revoke these rights from this user after I’ve deployed it, but I’m naturally paranoid. But let’s wait until we have deployed the application first.

### Getting an OpenAI API Key

Go to [platform.openai.com](<http://platform.openai.com>) and create a new account or log in. Navigate to ‘API keys’.

Get a new API key and save it somewhere safe.

You’re correct in thinking you’ll need to have tokens or a debit card added. This is the only expense associated with this application. I’m guessing most of us have an account by now, though.

### Setup a Local Environment

Ensure you have NodeJS, npm, and Python installed for this.

You can check if Node.js and npm are installed by running `node -v` and `npm -v` in your terminal. If they are not installed, you'll need to install Node.js (npm comes bundled with Node.js). To install Node.js and npm, visit the Node.js [website](<https://nodejs.org>) and download the installer locally.

Also check that you have Python installed and which version.

``` python --version ```

If I run this I get back **‘Python 3.11.5.’**

If you have another version be sure to either upgrade or change the runtime in the serverless.yml file.

```yaml provider: name: aws runtime: python3.11 ```

I also have Docker running on my laptop if you do not have docker running change the serverless.yml file to false when asked to package the dependencies with docker.

```yaml custom: pythonRequirements: dockerizePip: false ```

I don’t think we need docker for this so it shouldn’t be an issue to leave this out.

Once you’re confident everything is set up correctly, we can proceed by setting up a new folder locally.

```bash mkdir tech-botcd tech-bot ```

Make sure you install the serverless framework globally.

```bash npm install -g serverless ```

Then clone the repository we’ll be working with like so.

``` git clone https://github.com/ilsilfverskiold/ai-tech-news-bot.gitcd ai-tech-news-bot ```

Set up a virtual environment and activate it.

``` python -m venv venvsource venv/bin/activate # On Windows use `venv\Scripts\activate` ```

Install a serverless plugin, that will allow us to install the dependencies.

``` serverless plugin install -n serverless-python-requirements ```

Install the required dependencies that we have stored in the `requirements.txt` file.

```python pip install -r requirements.txt ```

The last thing we will need is to add the AWS credentials we downloaded before, when we created an IAM user in AWS.

Set them up like so.

``` serverless config credentials --provider aws --key YOUR_AWS_ACCESS_KEY --secret YOUR_AWS_SECRET_KEY ```

This will allow us to deploy our application to AWS.

### Testing the API

Let’s test the data we’re soon feeding into this LLM to see what it will get us.

Go to the browser and paste this into the search bar.

``` https://www.safron.io/api/table?period=daily&sort=trending ```

What we’ll get back are results like these.

``` {update_date: "2024-02-19",rows: 2983,results: [ { keyword: "AWS", date: "2024-02-19T00:00:00.000Z", count: 72, category: "Platforms & Search Engines", row_ids: [], sentiment: {}, yesterday_count: 34, sentiment_previous: {}, countChange: 111.76470588235294, trending: true }, { keyword: "Security", date: "2024-02-19T00:00:00.000Z", count: 40, category: "Subjects", row_ids: [], sentiment: {}, yesterday_count: 27, sentiment_previous: {}, countChange: 48.148148148148145, trending: true } ...] ```

As you can see, we can now programmatically filter objects based on whether they are ‘trending’, whether it’s a specific keyword, or whether the keyword falls under a specific category.

> I’m using a bit of a strange algorithm here to check if something is trending; it looks at count, sentiment, and then the overall count in various places. It’s a bit of a work in progress but, as of now, it’s right 80% of the time. Sometimes, things are just trending because it’s random, which is hard to control for.

Once filtered, we can then use the `row_ids` in the sources endpoint to fetch the sources for these keywords.

``` https://safron.io/api/sources ```

This endpoint requires a POST request so I’ll be using Postman to test it.

Press enter or click to view image in full size

You can feed it **‘keywords’** or **‘ids’** in the JSON body for the sources endpoint. Here, I am using **‘ids’** that you can get from the table endpoint under `row_ids`. This is what we'll do in the application as well.

The idea is to first query the table API to get the `row_ids` of the specific keywords, and then use these **‘ids’** in another request to this sources/search endpoint to get the correct sources and URLs.

Don’t worry, you don’t have to set up the code for this, but this is how it works.

### Set Preferences & Personalize It

Open up your code locally for the repository you’ve cloned. I usually do this with a simple shortcut for VSCode

``` .code ```

You’ll need to set up this shortcut, so if it is easier, just open the directory with the code manually in the code editor of your choice.

Navigate to `config.py` to configure your preferences.

Press enter or click to view image in full size

We’re setting quite a few things here — make sure you set the things that will be interesting to you.

You have three choices here:

* You can set the category limits for the trending keywords that have been found.
* You can set the keywords of interest. These keywords should always be scouted for, regardless if they are trending or not.
* You can set categories to be scouted and the amount of keywords within each category.

You can play around with these a bit or leave it as is. I have a temporary [frontend](<https://www.safron.io/>) set up where you can go and scout the different keywords to see what’s there.

### Setting Up AWS SES for Email Notifications

We need to also send the email that the LLM is producing for us.

I have already set up an email template in the helper_functions.py for the **generate_html_report** function.

Go to the code base and find the generate_html function to tweak the email layout if you want. This is optional.

Press enter or click to view image in full size

Go to your code base and find the generate html function to tweak the email layout

If it look alright to you, we can move on from this.

The most important thing to do though is to set validated to and from addresses in AWS SES.

So navigate back to the AWS console. Find Simple Email Service.

You need to add an email address where you can send emails to. You’ll also have to confirm it before being allowed to send emails to it.

Press enter or click to view image in full size

Create an identity of the email address where you would like your newsletters sent to. I have a domain called safron.io so I simply added that in to send from, but you should use your own private email address.

Make sure you also set the correct region, to and from addresses in the code under **config.py**.

Press enter or click to view image in full size

The last thing before we test this locally though you need to also grant your **IAM user SES access**.

To do this, we’ll go back to IAM, find the user you created previously, click **Add Permissions** and then find **AmazonSESFullAccess** and add it to your IAM user.

Press enter or click to view image in full size

Now the application will be able to send emails.

If you go, well I want to send these emails to random people too! Well then you’ll need a domain name and then confirmation from AWS to move out of your sandbox environment which is a bit of a lengthier process.

Technically you can use another medium here such as Slack, Whatsapp or set up MailChimp in that case.

### Deploy to AWS

Last part is now to test it out and then push it to AWS.

I would personally give this a go locally first. Maybe you want to work a bit on the newsletter templates and so on and want to see what the newsletter looks like.

So run this via your terminal.

``` serverless invoke local --function newsletterTrigger ```

What should happen when you run it locally? See my code run below.

Press enter or click to view image in full size

So what happens once the email has been sent? You’ll end up with something like this in your email inbox.

Press enter or click to view image in full size

Depending on your preferences, system templates and choice of LLM it will look different.

I have already set up the EventBrige schedules in the **serverless.yml** file, so they are triggered **at 10 AM UTC on weekdays.** If you’d like to change what time the reports should go out you can do so there.

If you’re happy, then push it to AWS.

``` serverless deploy ```

### End Result

Now you’ve got a personal tech newsletter that should run automatically at 10 AM UTC every day, and for the weekly newsletter it will run on Fridays. It should be based on what you are specifically interested in.

### Some Notes

I would say that some keywords you might want to scout for on a weekly basis only, and some on a daily basis only. ‘**AI’** is better to have as daily as it has a huge amount of sources whereas if you’re checking ‘**Mistral’** and other low count keywords then it’s better to get data for 6 days so you get more data to summarize.

The LLMs only has a very short context window, so it will only be able to process up to 150 sources per keyword and summary.

**Was it worth it?**

It’s a cool project, it get’s me what I want but it is still a work in progress.

> Doing this though, I wonder if this means that we won’t need humanly curated newsletters in the future? We might just need to set up the correct architecture for an LLM to perform for us. Based on our unique preferences. The key is good data though.

**What’s next with this?**

It might be interesting to apply more ML processes to this data to get better trending metrics; the algo I’m using right now is a bit shaky. It might also be interesting to build a better UI to get reports based on the keyword you’re searching for.

Additionally, it might be good to feed it more data from areas outside of tech, so you can understand what people are talking about in various fields.

We’ll see.

I hope you either managed to set up a useful tech bot and/or that it sparked some imagination.

❤
