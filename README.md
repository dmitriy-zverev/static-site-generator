# Static Site Generator
Imagine that you just could write .md files and easily convert it to html + css sites. Yeah that's what this program is about.

## How to convert .md files to a static site
1. First of you need to get this repo to your computer.
2. You need to create as many .md files in the content folder. You can add subfolders too.
3. Run `./main.sh`. This will run the server that will convert all of the .md files into .html in docs folder.
4. If you want to specify another folder for .html files, just change the COPY_TO_DIR in src/consts.py.

Also if you want to publish this to your server, first change the second argument in build.sh to your base folder and then run `./build.sh` script. After that push all the files into your server. You're good to go.

## How does it look like
<img width="1298" height="1165" alt="Screenshot 2025-08-14 at 15 30 30" src="https://github.com/user-attachments/assets/0292bdb8-2fda-43fb-b8c8-b80dbdeb8968" />

But the cool thing is that you can write all of your blog posts into separate .md files and then build it and push to the server. Amazing.
<img width="1183" height="1226" alt="Screenshot 2025-08-14 at 15 30 46" src="https://github.com/user-attachments/assets/3e2f0ff5-81c6-4db5-bfad-55a5d4eab4e9" />

## Certificate for completion
<img width="915" height="558" alt="bootdev_certificate" src="https://github.com/user-attachments/assets/1fbffd98-0b0c-444b-94fb-995ea5e897b0" />
