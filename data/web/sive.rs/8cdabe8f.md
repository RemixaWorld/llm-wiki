---
domain: sive.rs
fetch_date: '2026-05-18T12:35:22.145112'
status: ok
url: https://sive.rs/ti
---

# Tech Independence

## Contents:

- What?
- Register a domain
- Change DNS nameservers
- Create storage
- Create an SSH key
- Create your server
- SSH into root
- Customize these instructions
- Use your storage
- Simple website
- File sharing in /pub/
- Check email
- SMTP server
- Your email on anything
- Email directly on your server
- Contacts and Calendar
- More indie tips
- More storage?
- Upkeep
- Certificate expired?
- Trouble? Start over
- Questions? Additions?

## What?

Tech independence is **not depending on any particular company or software**.

The only tools you need are the common open source basics built into any Linux or BSD operating system — **free public-domain tools that are not owned by anyone**, and can run on any computer.

**Learn a few of these basic tools**, and you can run your own private server on any computer forever, for the rest of your life.
Host your own website and email.
Keep your own contacts and calendars synced with your phone.
Back up and sync your photos, movies, and music to your own private storage.
No more subscriptions needed.

You can **ignore** all the companies offering “**solutions**”, even if they are free, because they take away **self-reliance**.
The point is to **know how to do it yourself**, not to have somebody do it for you.
It’s worth a little up-front work, like learning how to drive.

Below are **simple step-by-step instructions** that work.
Instead of drowning you in options, it uses an operating system called OpenBSD and a hosting company called Vultr because I’ve used them for years and I know they are good and trustworthy.
But you could do this same setup with **any free Linux or BSD operating system**, with **any hosting company** that gives you “root” access to your own private server.
You could even do it on **an old laptop in your closet**.

So if a company turns evil or goes out of business, no problem!
You can set up a new server anywhere else in an hour, point your domain name to the new IP address, and it’s done.
**That’s tech independence** — never dependent on any particular provider or software.
It’s very empowering.
The instructions below will show you how.

## Register a domain

- Go to Porkbun.com.
- Search for a domain name you like until you find one that’s available.
- Create a new account, and pay.
- Congratulations. You’ll use this domain name in many of the steps below.

## Change DNS nameservers to Vultr

- Wherever you registered your domain name, log in there to change your domain’s DNS nameservers.
- It’s usually set by default to the company where you registered. So for example a domain registered at GoDaddy will have default nameservers of something.godaddy.com, and Porkbun’s will be something.ns.porkbun.com.
**Replace**those defaults with these two:**ns1.vultr.com****ns2.vultr.com**


## Create storage

- Go to Vultr.com.
- Create an account and give it your credit card.
- Click here for the “Add Block Storage” page.
- Click “
**Block Storage (HDD)**”, which says “Globally Available” - Below that, a list of cities. Click the one closest to you.
- Below that, a slider lets you choose how much storage you need. If not sure, just leave it as $1 for 40 GB.
- Below that, in a subtle box that says “label”
**type the word**.`encrypted`

- Below that, click the “
**Add Block Storage**” button.

## Create an SSH key

**Open a terminal**.**Windows?**Start → Windows PowerShell → Windows PowerShell**Mac?**Applications → Utilities → Terminal

- Type

and hit [enter] or [return].**ssh-keygen -t ed25519** - When it says, “
`Enter file in which to save the key (/Users/yourname/.ssh/id_ed25519):`

”, hit [enter] or [return]. - When it says, “
`Enter passphrase (empty for no passphrase):`

”, hit [enter] or [return]. - When it says, “
`Enter same passphrase again:`

”, hit [enter] or [return]. - See the line that starts, “
`Your public key has been saved in`

” and ends in “`id_ed25519.pub`

”?**That’s the file you need**for the next step. **In a text editor, open “**.`id_ed25519.pub`

”**Windows?**Type**notepad .ssh/id_ed25519.pub****Mac?**Type**open -e .ssh/id_ed25519.pub**

- It should be a single line like this:
`ssh-ed25519 AAAAC3Nz5AAAAIPIXO5icj4LUpqa2baqYQRmCZ1+NV4sBDr you@computer`

**Copy**(⌘-C or Ctrl-C)**the contents of “id_ed25519.pub” now**, since you will paste it in the next step.- In your Vultr.com account, “Account → SSH Keys”, click here to
**[Add SSH Key]** - In [Name], type
**mykey** - In the box below it,
**paste**(⌘-V or Ctrl-V)**the contents of “id_ed25519.pub” now**, so it says something like`ssh-ed25519 AAAAC3Nz5AAAAIPIXO5icj4LUpqa2baqYQRmCZ1+NV4sBDr you@computer`

- Below that, click the [Add SSH Key] button. It should say “SSH Key Added” and under “SSH Keys” you should see “mykey”.

## Create your server

- In your Vultr.com account:
- Click here for the “Deploy New Instance” page.
- Click “
**Cloud Compute - Shared CPU**” (NOT “Optimized Cloud Compute”) - Below that, Choose Location, IMPORTANT: click
**the same city**you chose for your encrypted storage in the previous step. - Below that, Choose Image, click “
**OpenBSD**” (the yellow blowfish) then inside its box, click “**7.7 x64**” - Below that, Choose Plan, click “
**Regular Cloud Compute**” on the right - When it pops-up “For only $$ more…” click “No Thanks”
- Click the
**top, cheapest option**: 25 GB SSD, 1 vCPU, 1 GB, 1 TB, $5/month - When again it pops-up “For only $$ more…” click “No Thanks”
- Below that, Additional Features, UN-check “Auto Backups”
- A scary pop-up says “Are you sure....”. Tick the box next to “I understand the risks”, then click the red button “Disable Auto Backups”.
- Next to that, UN-check “IPv6” because you won’t use it yet
- Under
**SSH Keys, choose “mykey”**(*very important!*) - Under “Server Hostname & Label”,
**type your domain name**in both “server hostname” and “server label”. - At the bottom, click the big blue button [“
**Deploy Now**”]. - Stretch your legs for a minute while waiting for your server status to change from “Installing” to “Running”.
**Copy and save**its**IP Address**on your computer.

## SSH into root, and get my script

- Copy (⌘-C or Ctrl-C) the
**IP Address**from the last step of Create Your Server. **Open your terminal**from the Create an SSH key section.- Whenever I say to type something into the terminal, hit your [return] or [enter] key afterwards.
**Type into the terminal:**. So for example:`ssh root@YOUR-IP-ADDRESS`

`ssh root@123.45.67.89`

- It should say something like:
The authenticity of host '123.45.67.78 (123.45.67.89)' can’t be established. ED25519 key fingerprint is SHA256:OyiqVsjRX8U2f0UTUY4D0erdl6855YNRXyQk2D. This key is not known by any other names Are you sure you want to continue connecting (yes/no/[fingerprint])?

**Type**`yes`

- It should say something like:
Warning: Permanently added '123.45.67.89' (ED25519) to the list of known hosts. OpenBSD 7.7 (GENERIC.MP) #0: Sun May 4 11:23:50 MDT 2025 Welcome to OpenBSD: The proactively secure Unix-like operating system.

- Congratulations! You’re inside a remote computer!
- Type
**ftp https://sive.rs/ti.sh** - Type
**sh ti.sh** - Watch it install, answer its questions, and do what it says.
- Be ready to open a
**new**terminal window, so you can leave this one logged-in. - See below for help with its prompts.

## Customize these instructions

Enter your domain name and the username that you create, below, and this will customize all following instructions for you.

Now when you see this button: **click it** to **copy that line** so you can **paste it into your terminal**, without error.

## Use your encrypted storage

The ti.sh script will eventually prompt you, “Now upload anything while I wait...”. Here’s how.

### Mac

- In a
**new terminal window on your Mac**, type: **rsync -avz Documents yourusername@yourdomain.name:/mnt/**- You should see it uploading your Documents folder to your private encrypted storage. Use this same format to upload any other folders, replacing “Documents” in the command.
- I
**highly recommend learning rsync**, since it can be used for so many things (even backing up to a USB storage). Search the web for “rsync tutorial” some day to know it better. Then you can skip over the next FreeFileSync section.

### FreeFileSync

For **Windows**, try **FreeFileSync**. Here’s how:

- Download FreeFileSync and please give an optional donation there if you can afford to. Donating also unlocks more features. Thanks to Jon Lis for the recommendation.
- Install and open FreeFileSync.
- Top-center: click the grey
**[Browse]**button and find the folder with the stuff you want to upload. - Top-far-right: click the white
**cloud icon**then**SFTP**at the top. - Server name or IP address: yourdomain.name
- Left side: click
**(*) Key File** - Username: yourusername
- Browse to find your
**private**key, called**id_ed25519**from the “Create an SSH key” section. (Not the file that ends in “.pub”, but the one next to it.) NOTE: Because the /Users/yourusername/.ssh directory is “hidden” by Windows and Mac by default, I find it easier to just type the path directly, like this:*The username, for this next line, should be your username on your home computer, not your remote server.***Windows?**Type**C:\Users\yourusername\.ssh\id_ed25519****Mac?**Type**/Users/yourusername/.ssh/id_ed25519**

**Directory on server**:**/mnt**- Click
**OK**to go back to the main screen. - Top-right: click the
**green gear wheel**. - Left button: click “
**MIRROR →**” - Click
**OK**to go back to the main screen. - Top-center: click “
**COMPARE**”, and make sure your files are there. - Top-right: click “
**SYNCHRONIZE Mirror →**” then**[Start]**

### Verify and unmount

- When it’s done uploading,
**log in to your server**again, from your terminal. - Type
**find /mnt** - You should see a long list of the files you uploaded.
- Type

to detach your encrypted storage.**m-x** - Type

again, and now you should see nothing there! Congratulations! You now see**find /mnt****how this will work in the future**:- Log in and type “

” to**m****attach**your encrypted storage. **Upload**your files with rsync or FreeFileSync.- Log in and type “

” to**m-x****detach**the storage, for security.

- Log in and type “

## Simple website

- On your home computer, in your main home directory,
**make a directory/folder called “htdocs”** - Download this file called “template.html” and save it in your “htdocs” directory.
- Download this file called “style.css” and also save it in your “htdocs” directory.
**Make a copy**of the “template.html” file, and**name the copy “index.html”**. This will be your home page.**Edit the index.html file**in a text editor (NotePad or TextEdit) and change my default text to whatever you want.- When you need to add a new page, just
**copy the template again**, call it “about.html” or whatever, and make a link to it from the home page. The header of each page will link back to index.html : your home page. - If you want to
**change the look**of your site, just edit the style.css file. Search the web for “CSS tutorial” if needed. **To upload it**to your public server, do one of the next two steps:- Apple Mac?
**Open a new terminal window**on your computer, type**rsync -avz htdocs yourusername@yourdomain.name:/var/www/** - Windows? FreeFileSync again, but now change the “
**Directory on server**” to**/var/www/**(you can find it by clicking [browse] or typing it directly) then upload this htdocs directory there. - Go to https://yourdomain.name in your web browser,
**refresh the page**, and you should see your updated website. - Any trouble, just know that the goal is to get that index.html file into this location on your server:

because that’s where the web server is expecting it to be. That’s where we put the original test file, so your new**/var/www/htdocs/index.html**`index.html`

file should replace that one. - If you want
**short URLs**, without the .html, you can (for everything except index.html) because I set the default type to be HTML. Just remove the “.html” from your HTML filenames, update your links, and voilà!

*many*pages, consider a more complicated solution.

## File sharing in /pub/

Your website is configured to list all files in the /pub/ directory of your website. So basically anything in /var/www/htdocs/pub/ is public. Upload any files you want to share.

It replaces Dropbox and similar services for sending big files. Just upload the file to /var/www/htdocs/pub/ then find it in your web browser, copy its URL, and send someone the URL.

If the files you want to share are already on your computer, then just **make a pub/ directory inside htdocs/** (so, **htdocs/pub/**), put your files in there, then use FreeFileSync or rsync to upload them as you did in the previous section called “Simple website”.
Consider them part of your website.

Or if you have a URL from somewhere else online that you want to download to your server, just do it as we did in the numbered steps above. Then use FreeFileSync or rsync to download from your server to your computer first, before your next upload sync.

## Check email on your server

- From your existing (gmail, etc) email account,
**send two or three “hello me!” emails to yourusername@yourdomain.name** - ssh in to your server, then
**type**`mutt`

- You should see the emails you sent. If not, wait a minute.
**Type**to go down and up the list of emails.`j`

and`k`

a few times- To
**read an email, hit [enter] or [return]**when it is highlighted. - To go
**back to the list, type**(for “index”)`i`

- To
**delete it, type**(but don’t delete them all yet because you need one for a future step)`d`

- Type
.`q`

to quit

## SMTP server

If it weren’t for thieves, we wouldn’t need locks. If it weren’t for spammers, you could send email directly from your server. But noooooo, hosting companies got burned by spammers, so now they block outgoing emails even for nice people like you. That’s why you need to use a special external email-sending service. SMTP is the name of the standard protocol for sending emails.

- Go to
**smtp2go.com**and click**[Try SMTP2GO Free]**. - Under “Start your free account”, when it asks your “Work email”,
**give your new yourusername@yourdomain.name** - Click [Continue] then give your name, and make up a password just for your account there. (You won’t need that password anywhere else.)
- After that, it should say “Check your inbox!”
**Finish the remaining steps on your server**, by running “`ti.sh`

”. My ti.sh script receives their email, shows you the link, gets the API key from you, then takes care of everything else so that you can send emails.- When done, your smtp2go.com account has
**your SMTP User settings**(the things you enter in your email app) on the left-hand menu under**“Sending” → “SMTP Users”**.

## Your email on anything

To do email from your phone, computer, or anywhere else, you now have an IMAP server, called Dovecot.
So on any device, you can **add a new IMAP Mail account**, with these settings:

- Account type: IMAP
- Email address: yourusername@yourdomain.name
- Username: yourusername
- Password: the password you made for your username on your server
- Incoming mail server: yourdomain.name
- Outgoing mail server: yourdomain.name
- Connection security: SSL
- Authentication type: Basic authentication

If you have any problem sending email that way, use the smtp2go.com settings for the Outgoing mail server, saved under “Sending → SMTP Users” in your smtp2go.com account.

## Email directly on your server

- ssh in to your server, then
**type**`mutt`

**Type**to get to an email you want to reply to.`j`

and`k`

**To reply, hit**then:`r`

- It shows “
`To:`

” so you can edit or add recipients.**Hit [enter] or [return]**to leave it. - It shows “
`Subject:`

” so you can edit the subject.**Hit [enter] or [return]**to leave it. - It asks “
`Include message in reply? ([yes]/no/?):`

”.**Hit [enter] or [return]**for the usual norm of echoing someone’s email back at them below your reply. Or`n`

for not. - Now you are inside the
**vi**text editor which is not self-explanatory, so I’ll walk you through a simple reply: - Hit

(no [return] or [enter]) to go into “insert mode” and**i****type your message**. You’ll notice it’s on the same line as some other text, so you might want to start by hitting [return] or [enter] a few times, then**up-arrow**to go back to the first line again. - When done typing your message,
**hit your [esc] key**in the very top-left corner of your keyboard. Nothing will change on the screen, yet. - Type

(the “:” at the beginning is important) then [enter] or [return].**:wq** - Then you’ll see the “Compose Menu” which I think of as the “last chance before sending” screen.
**Hit**.`y`

to send it

- It shows “
- To
**send a new email**, hit

then repeat those steps like you did for a reply, except now the “**m**`To:`

” and “`Subject:`

” are blank and waiting for you to create. (For “`To:`

”, type the email address of the person you’re emailing.) - To
**quit**, hit**q**

Mutt is a great program for reading and sending email on the command line. It’s been my email client for 20 years. Read its manual here if you want to go deeper. It does everything.

The vi text editor is a useful tool to edit text on a server. It takes a few minutes to learn, but it’s worth learning because it’s installed by default on every Linux/BSD server.

## Contacts and Calendar

Your phone currently keeps its contacts and calendars with Google or Apple. Now you can get them off the cloud and keep them privately on your own server.

My ti.sh setup script installs a CardDAV server for contacts, and CalDAV server for calendars.

Here’s how to connect your phone.

### Android phone

You need an app called “**DAVx⁵**”, so install it first. Then…

- Open the
**DAVx⁵**app - Click the orange (+) in the bottom-right
- Click (·) “Login with URL and user name”
- Base URL:
**https://dav.yourdomain.name/** - User name: yourusername
- Password: the “easy to type on your phone” password you made
- Click “LOGIN” in the bottom-right corner.
- It should work and bring you to the “Create account” page, where “Account name” will be yourusername. Leave everything as-is and
**click “CREATE ACCOUNT”**in the bottom-right corner. - It brings you to the “CARDDAV” header.
**Tick the toggle to turn on**next to your domain name. - Click the ♻ arrows in the bottom-right corner to synchronize your contacts.
- Click the “CALDAV” header up top.
**Tick the toggle to turn on**next to your domain name. - Click the ♻ arrows in the bottom-right corner to synchronize your calendar.
**Go to your Calendar app**, and in the top-right corner, click the round icon there. (Might be your face or a letter.) Then**change it to the one with yourusername**. After changing it, click the X in the top-left corner.- To add a new Event,
**Click [+] in the bottom-right corner**, and choose “**Event**” from the popup menu. - There might be a warning, “Switch to a Google Account to take advantage blah blah…”.
**Click “dismiss”**. - Title this event something like “Test Delete”, and notice it should be saving to the calendar with your domain name and username.
**Click (Save)**in the top-right corner. - Check the terminal window where it should say “Calendar entry added!”
**Go to your Contacts app**, and in the bottom-right corner,**click “Fix & manage”**.- Click “
**Settings**” - Near the bottom, click “
**Default account for new contacts**”, and change it to the DAVx⁵ Address book with your domain name. **Click “< Settings”**in the top-left corner.- In the top-right corner, click the round icon there. (Might be your face or a letter.) Then
**change it to the DAVx⁵ Address book**with your domain name. Then click X in the top-left corner. - Click “
**Contacts**” in the bottom-left corner. It should say “No contacts in this account”. - Click
**+**in the bottom-right corner to Create contact. Top of the next page should say “Save to” then your domain name. - Add a New Contact with a name like “Test Delete”. Then
**click “Save”**in the top-right corner. - Check the terminal window where it should say “Contact added! Both work. Congratulations.”

### Apple iPhone

**Settings → Contacts → Accounts → Add Account → Other →**(under “CONTACTS”:)**Add CardDAV Account**- Server:
**dav.yourdomain.name** - User Name: yourusername
- Password: the “easy to type on your phone” password you made
- Click “next” in the top right corner, and it should bring you to your “Accounts” page, where you see it listed, saying “Contacts” underneath.
- Click
**Add Account → Other →**(under “CALENDARS”:)**Add CalDAV Account** - Server:
**dav.yourdomain.name** - User Name: yourusername
- Password: the “easy to type on your phone” password you made
- Click “next” in the top right corner, and it should bring you to a “CalDAV” page, showing Calendars and Reminders.
**Un-tick Reminders**. - Click “save” in the top right corner, and it should bring you to your “Accounts” page, where you see it listed, saying “Calendars” underneath.
**Click “< Contacts”**in the top-left corner, to go back to settings for your Contacts app.- At the bottom
**change Default Account**to the one with yourdomain.name. **Click “< Contacts”**then “**< Settings**”, both in the top-left corner, then**scroll down to Calendar settings**and click it.- In Calendar settings, 2nd from the bottom should say “
**Default Calendar**”. Tap to**change it**to the one with yourdomain.name. - Go to your
**Calendar**app and click the**+**in the top-right corner. - Add a New Event with a Title like “Test Delete”. Then
**click “Add”**in the top-right corner. - Check the terminal window where it should say “Calendar entry added!”
- Go to your
**Contacts**app and click the**+**in the top-right corner. - Add a New Contact with a name like “Test Delete”. Then
**click “Done”**in the top-right corner. - Check the terminal window where it should say “Contact added! Both work. Congratulations.”

## More indie tips

- Use Firefox.
- Install uBlock Origin in Firefox and Chrome.
- In Firefox settings, under “Privacy and Security”, choose “[X] Delete cookies and site data when Firefox is closed”, then close Firefox often to erase all your cookies and logins. Browse the web anonymously, not logged-in.
- Replace Google Authenticator with 2FAS.
- If you use Windows, replace it with Ubuntu Linux. (Use both at first, then slowly transition.)
- Keep your new email address as a private email account that you only give to those few people who you really want to hear from. Then your old gmail/yahoo/outlook/etc address can be just low-priority junk, and your new private email account won’t need spam protection.
- Or if you don’t want to run your own email server, use Mailbox.org or Fastmail but
**only**by using your own domain name. Be yourusername@yourdomain.name from now on. Don’t depend on anyone else’s domain for your email or you’ll be stuck with them.

## More storage?

If you need hundreds of gigabytes, or even terabytes of storage, I recommend Hetzner’s “Storage Box”. It’s the best storage value I’ve found. Also consider Backblaze Personal Backup.

I personally use Vultr’s storage (as described above) for sensitive information I definitely want completely encrypted. Then I use Hetzner’s Storage Box for all my photos, videos, music, and other big files that don’t absolutely need to be encrypted.

## Upkeep

You honestly don’t have to do anything to maintain your server. It will just work as-is for decades! But if you like to keep it up-to-date, it only takes a minute, so run these next steps any time.

**Log in to your server**, if you are not already.- Type
**doas su** - Type
**syspatch** - Type
**fw_update** - Type
**pkg_add -u** - Type
**sysupgrade** - Type

to log out.**exit; exit**

If that last “`sysupgrade`

” step did **not** give an “Error retrieving … 404 Not Found” error, that means your OpenBSD operating system is upgrading itself. They release an upgrade every 6 months. In that case, go to this OpenBSD page and follow the link at the top that says “**Upgrading to** (7.6, etc)” to see if there’s anything else you should know.

If the “`sysupgrade`

” step updated your operating system and your server rebooted, then there is just one more step:

**Log in to your server**, if you are not already.- Type
**doas su** - Type
**sysmerge** - Follow any instructions. Don’t worry about messing up because you can always start over, as described below.
- Re-do the
`syspatch ; fw_update ; pkg_add -u`

steps, above. - Type

to log out.**exit; exit**

## Secure certificate expired?

**Log in to your server**, if you are not already.- Type
**doas su** - Type
**domain=yourdomain.name** - Type
**acme-client -v $domain** - Type
**rcctl restart relayd** - That should fix it. Confirm it in your web browser. Let me know if not.
- IMPORTANT: Copy-paste this next line to make it renew automatically from now on:
**(crontab -l 2>/dev/null; echo "11\t3\t*\t*\t5\tacme-client $domain && rcctl reload relayd") | crontab -**- Hit [enter]. Type

to log out.**exit; exit** - Let me know if it happens again. (It shouldn’t.)

## Trouble? Start over

I’ve tested the steps above very carefully and repeatedly. They work. So if you hit a major problem, something not happening like it says it should, please do this:

- Type “

” in any terminals you still have open, until they are all closed.**cd ; m-x ; exit** - Go to your Vultr account.
- See your server instance? See to the far right, a subtle
**···**? Click that. - From its pop-up menu, click the last option: “
**Server Destroy**”. **Tick the box**next to “[X] Yes, destroy this server.”- Click the big red
**[Destroy Server]**button. - This will not destroy your encrypted storage. That’s another reason we kept it separate from the start. So
**if**you already uploaded a bunch of your files and want to save them, they should still be there. - On your own computer,
**in the terminal, type:**`rm .ssh/known_hosts`

- Go back to the section called “Create your server” and try again.

## Questions? Additions?

**To learn more** about your new server, just **log in** and type: **help**

It will teach you the basics.
Then for each command or file you want to know more about, type

followed by the command or filename.
So for example, log in and type…**man**

Hit your [space] bar to scroll the page, then

to quit.
**q**

It’s one of the most wonderful things about OpenBSD: **everything you need to know is in those man pages!**
No need for YouTube, Google, ChatGPT, or any other advertising-driven sources of information.

I will constantly improve this page, so get on my private email list for updates.

Until then, ask any questions.
If something went wrong, please give me a **very specific** description of exactly what went wrong at what step, what it was supposed to do, and what exactly it actually did.
Click here to email me.

Requests for what to add? Again, just email me.
