---
domain: medium.com
fetch_date: '2026-05-18T12:51:07.249647'
status: ok
url: https://medium.com/ai-simplified-in-plain-english/enter-2025-with-these-5-cool-python-libraries-9169b581efb1
---

# Enter 2025 with these 5 Cool Python Libraries

[ ![Manpreet Singh](https://miro.medium.com/v2/resize:fill:64:64/1*YaViKfuc2uAV4OhpLOsZXw.jpeg) ](</@singh.manpreet171900?source=post_page---byline--9169b581efb1--------------------------------------->)

[Manpreet Singh](</@singh.manpreet171900?source=post_page---byline--9169b581efb1--------------------------------------->)

7 min read

·

Dec 2, 2024

\--

\--

Listen

Share

More

![created bt me](https://miro.medium.com/v2/resize:fit:700/1*wdpcgEKYInz2FNoHWfwOqw.png)

Hey there!

Let me tell you about how I discovered five amazing Python libraries that totally changed how I code.

You know when I personally find something so helpful then I want to tell everyone about it?

Lets see all one by one.

## TQDM (From “Is It Working?” to “Almost Done!”)

Remember when you’d run a program and just… wait?

Like when you’re downloading 1000 photos and have no clue if it’s working or frozen?

Let me show you what I mean:

```python # Let me show you something I dealt with recently...import timedef old_way_photo_download(): print("Starting download...") for photo in range(100): # Download stuff... time.sleep(0.1) # The problems: # 1. No idea how much is done # 2. No clue if it's stuck # 3. Can't tell when it'll finish print("Done! ...I think?") ``` ```python # Then I found TQDM - watch this magic!from tqdm import tqdmdef new_way_photo_download(): # Look how simple and clear this is! for photo in tqdm(range(100), desc=" Downloading vacation photos", unit="photos"): time.sleep(0.1) # Now I can see: # - Exactly how many photos are done # - How fast they're downloading # - When it'll finish!# Even better - downloading files with size infodef download_with_progress(): total_size = 100 # MB with tqdm(total=total_size, unit='MB', unit_scale=True, desc=" Downloading holiday_pics.zip") as progress: downloaded = 0 while downloaded < total_size: # Download a chunk (pretend) chunk_size = 2 downloaded += chunk_size # Update our nice progress bar progress.update(chunk_size) progress.set_postfix({ 'speed': '2.5 MB/s', 'status': 'Looking good!' }) time.sleep(0.2) ```

Here’s what drove me crazy before TQDM:

* Starting big downloads and not knowing if they crashed
* Having to add print statements everywhere just to see progress
* Never knowing when something would finish

But with TQDM, it’s like having a smart progress bar for everything!

Just wrap your loop with `tqdm()` and suddenly you can see exactly what's happening.

No more guessing games!

Lets move on to next library.

## Rich (Making Your Code Talk in Color!)

Let me tell you about the time I spent hours trying to find a bug in my data.

It was like trying to find a typo in a really long text message.

Then I found Rich:

```python from rich import printfrom rich.console import Consolefrom rich.table import Tablefrom rich.traceback import install# Before Rich, debugging was like this:def old_way_debug(): # Imagine trying to spot the problem here! game_data = { "player": "Mario", "lives": -1, # Bug: Negative lives! "coins": 9999999, # Bug: Too many coins! "power_ups": ["mushroom", "star", None] # Bug: None snuck in! } print("DEBUG - Game State:", game_data)# With Rich, problems jump out at you!console = Console()def new_way_debug(): game_data = { "player": "Mario", "lives": -1, "coins": 9999999, "power_ups": ["mushroom", "star", None] } # Create a pretty game status display console.print("[bold red]🎮 Game Status Check[/bold red]") # Make a neat table table = Table(title="Super Mario Status") table.add_column("Item", style="cyan") table.add_column("Value", style="magenta") table.add_column("Status", style="green") for key, value in game_data.items(): status = "✅" if key == "lives" and value < 0: status = "Can't have negative lives!" elif key == "coins" and value > 999999: status = "Coin overflow!" elif key == "power_ups" and None in value: status = "Invalid power-up!" table.add_row(str(key), str(value), status) console.print(table) ```

The problems Rich fixed for me:

1. Finding bugs used to be like searching for a needle in a haystack
2. Error messages were confusing and hard to read
3. Important information got lost in walls of text
4. Debugging was just… not fun!

Now with Rich:

* Important stuff stands out in color
* Data is organized in nice tables
* Errors make sense
* Debugging actually became kind of fun!

Let’s talk about three more that totally changed how I code.

These aren’t just tools — they’re like having super helpful friends who make coding way easier!

Next.

## Pathlib (No More File Path Nightmares!)

Let me tell you about the time I spent THREE HOURS debugging a program just because Windows uses backslashes (`\`) and Linux uses forward slashes (`/`).

It was a mess! trust me

```python import os # The old wayfrom pathlib import Path # The better way!# The Old Way (So Many Problems!) 😫def old_way_file_handling(): # Problem 1: Different systems, different slashes data_folder = "data\\\user\\\photos" # Works on Windows # data_folder = "data/user/photos" # Works on Linux # Which one should we use? 😕 # Problem 2: Building paths is messy full_path = os.path.join(os.path.dirname(__file__), "data", "user", "photos", "vacation.jpg") # Problem 3: Checking files is complicated if os.path.exists(full_path) and os.path.isfile(full_path): if os.path.splitext(full_path)[1].lower() == '.jpg': print("Found a jpg file!")# The Pathlib Way (Super Easy!) 😊def new_way_file_handling(): # Works everywhere! Windows, Mac, Linux - no problem! photos = Path("data") / "user" / "photos" # Finding files is super easy for photo in photos.glob("*.jpg"): print(f"Found photo: {photo.name}") print(f"Size: {photo.stat().st_size / 1024:.2f} KB") print(f"Created: {photo.stat().st_ctime}") # Making new folders? Easy! backup_folder = photos / "backup" backup_folder.mkdir(exist_ok=True) # Moving files? No problem! for photo in photos.glob("*.jpg"): new_location = backup_folder / photo.name print(f"Moving {photo.name} to backup...") # photo.rename(new_location) # This would actually move the file# Let's see both in action!print("Old Way (lots of potential problems):")old_way_file_handling()print("
New Way (smooth and easy):")new_way_file_handling() ```

Here’s what drove me crazy before Pathlib:

* Programs breaking because of wrong slashes
* Having to write different code for Windows and Linux
* Complex path joining that was hard to read
* Never being sure if a file exists or not

But with Pathlib:

* Just use `/` everywhere - it works on all computers!
* Finding files is super easy with `.glob()`
* Creating and moving files just makes sense
* No more path headaches!

## Pydantic (Your Data’s Best Friend! )

Ever had your program crash because someone put text where a number should be?

Or spent hours debugging because data wasn’t in the right format?

That’s where Pydantic comes in!

```python from pydantic import BaseModel, Field, EmailStr, validatorfrom typing import List, Optionalfrom datetime import date# Before Pydantic - Lots of Manual Checkingdef old_way_user_registration(user_data): errors = [] # So much manual checking! if 'email' not in user_data: errors.append("Email is required") elif '@' not in user_data['email']: errors.append("Invalid email") if 'age' not in user_data: errors.append("Age is required") elif not isinstance(user_data['age'], int): errors.append("Age must be a number") elif user_data['age'] < 0: errors.append("Age can't be negative") if errors: raise ValueError(errors) return user_data# With Pydantic - Clean and Safe! class User(BaseModel): name: str = Field(..., min_length=2, max_length=50) email: EmailStr # Automatically checks email format! age: int = Field(..., ge=0, lt=150) hobbies: List[str] = [] premium_member: bool = False # Even custom checks are easy! @validator('name') def name_must_be_cool(cls, v): if v.lower() == 'admin': raise ValueError("'admin' is not allowed as a name!") return v.title() # Makes names look nice!# Let's try it out!def register_new_user(): try: # Good data works perfectly good_user = User( name="Alice", email="alice@example.com", age=25, hobbies=["coding", "reading"] ) print("✅ Valid user created:", good_user) # Bad data? Pydantic catches it! bad_user = User( name="a", # Too short! email="not-an-email", # Invalid email! age=-5, # Negative age! hobbies="reading" # Should be a list! ) except Exception as e: print("❌ Found problems:", str(e))# Try it out!print("Let's register some users!")register_new_user() ```

The problems Pydantic solved for me:

1. No more writing tons of if-statements to check data
2. Clear error messages when something’s wrong
3. Automatic conversion of data to the right type
4. Easy validation of complex data structures

Now lets finish with Ruff. It’s my favorite code cleanup tool

## Ruff (From Messy to Beautiful in Seconds!)

Let me tell you about the tool that basically became my code’s best friend — Ruff!

You know how sometimes your code works but looks messy?

Or maybe you’ve copied some code from different places and now it’s all in different styles?

That’s exactly what Ruff helps fix!

Let me show you what I mean with a real problem I had last week:

```python # This was my messy code before Ruff import pandas as pd;import numpy as np;from matplotlib import pyplot as pltfrom datetime import datetime,date,timedeltaimport json,os,sysclass userProfile: def __init__(self,name,age,email): self.name=name;self.age=age;self.email=email def check_age(self): if self.age<13:return 'Too young'; elif self.age<18:return 'Teen' else:return'Adult' def to_dict(self):return{'name':self.name,'age':self.age,'email':self.email}def process_data(data_list): results=[] for i in range(len(data_list)): item=data_list[i] if type(item)==str:item=int(item) results.append(item*2) return results# After Ruff worked its magic!import jsonimport osfrom datetime import date, datetime, timedeltaimport numpy as npimport pandas as pdfrom matplotlib import pyplot as pltclass UserProfile: """A class to manage user profiles and their attributes.""" def __init__(self, name: str, age: int, email: str): self.name = name self.age = age self.email = email def check_age(self) -> str: """Determine the age category of the user.""" if self.age < 13: return "Too young" elif self.age < 18: return "Teen" return "Adult" def to_dict(self) -> dict: """Convert user profile to dictionary format.""" return { "name": self.name, "age": self.age, "email": self.email, }def process_data(data_list: list) -> list: """Process a list of data items by converting to int and doubling.""" results = [] for item in data_list: if isinstance(item, str): item = int(item) results.append(item * 2) return results ```

Let me tell you what problems this fixed:

### Problem 1: Messy Imports

Before Ruff:

* Imports were all jumbled together
* Some had semicolons (which look ugly!)
* No organization at all

After Ruff:

* Imports are neatly organized
* Standard library imports come first
* Third-party imports (like pandas) come next
* Everything’s in alphabetical order!

### Problem 2: Class Names and Spacing

Before:

* Inconsistent naming (`userProfile` instead of `UserProfile`)
* No spaces around operators
* Everything squished together

After:

* Proper PascalCase for class names
* Nice spacing that makes code easy to read
* Clear separation between functions

### Problem 3: Missing Documentation

Before:

* No one knew what the code did
* Had to read through everything to understand it

After:

* Clear docstrings explaining what everything does
* Type hints showing what kind of data to use
* Comments that actually help!

Ruff is like having a friendly robot that cleans up your code while you work!

And the best part?

It’s super fast — way faster than other tools like Black or Flake8.

Just install Ruff:

```python pip install ruff ```

And that’s it!

You can now make your code beautiful anytime!

So, these five libraries will make your Python coding journey so much more enjoyable!

They’re like having a team of helpful assistants making your code better, safer and more beautiful.

> Remember, great developers aren’t just about writing code — they’re about using the right tools to make coding easier and more fun!

Give these libraries a try and I promise you’ll wonder how you ever coded without them!

Happy coding!
