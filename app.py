from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

POSTS_FILE = 'posts.json'

def load_posts():
    """
    Loads blog posts from the JSON file. Initializes the file if it is empty or faulty.

    Returns:
        list: A list of blog posts as dictionaries.
    """
    try:
        if not os.path.exists(POSTS_FILE):
            # File does not exist – create empty file
            with open(POSTS_FILE, 'w', encoding='utf-8') as file:
                json.dump([], file)
            return []

        with open(POSTS_FILE, 'r+', encoding='utf-8') as file:
            content = file.read().strip()
            if not content:
                # File is empty – initialize with empty list
                file.seek(0)
                json.dump([], file)
                file.truncate()
                return []
            file.seek(0)
            return json.load(file)

    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading the file: {e}")
        try:
            # On JSON error – overwrite file with empty list
            with open(POSTS_FILE, 'w', encoding='utf-8') as file:
                json.dump([], file)
        except IOError as write_error:
            print(f"Error resetting the file: {write_error}")
        return []

def save_posts(posts):
    """
    Saves blog posts to the JSON file.

    Args:
        posts (list): A list of blog post dictionaries.
    """
    try:
        with open(POSTS_FILE, 'w', encoding='utf-8') as file:
            json.dump(posts, file, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Error saving the file: {e}")

@app.route('/')
def index():
    """
    Homepage displaying all blog posts.

    Returns:
        HTML page with a list of all blog entries.
    -> Renders index.html with all posts
    """
    posts = load_posts()
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Shows the form to add a new blog post (GET) or processes the entered data (POST).

    Returns:
        - GET: HTML form page
        - POST: Redirects to homepage after successful save
    -> Renders add.html or saves new post and redirects
    """
    if request.method == 'POST':
        try:
            author = request.form.get('author', '').strip()
            title = request.form.get('title', '').strip()
            content = request.form.get('content', '').strip()

            # Check if all fields are filled
            if not (author and title and content):
                raise ValueError("All fields must be filled.")

            posts = load_posts()

            # Assign new ID: max ID + 1 or 1 if empty
            new_id = max([post['id'] for post in posts], default=0) + 1

            new_post = {
                'id': new_id,
                'author': author,
                'title': title,
                'content': content
            }

            posts.append(new_post)
            save_posts(posts)

            return redirect(url_for('index'))
        except Exception as e:
            print(f"Error adding a post: {e}")
            return "An error occurred while saving the blog post.", 500

    # On GET: show empty form
    return render_template('add.html')

@app.route('/delete/<int:post_id>')
def delete(post_id):
    """
    Deletes a blog post by the given ID.

    Args:
        post_id (int): The ID of the blog post to delete.

    Returns:
        Redirects to homepage after deletion.
    -> Removes entry from JSON file and redirects to homepage
    """
    try:
        posts = load_posts()

        # Filter all posts except the one with the matching ID
        filtered_posts = [post for post in posts if post['id'] != post_id]

        if len(filtered_posts) == len(posts):
            # No change → ID not found
            raise ValueError(f"No post found with ID {post_id}.")

        save_posts(filtered_posts)

        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error deleting the post with ID {post_id}: {e}")
        return "An error occurred while deleting the blog post.", 500

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Edits an existing blog post.

    Args:
        post_id (int): The ID of the blog post to edit.

    Returns:
        - GET: Shows form with pre-filled values
        - POST: Saves changed data and redirects to homepage
    -> Allows updating author, title, and content
    """
    try:
        posts = load_posts()
        post = next((p for p in posts if p['id'] == post_id), None)

        if not post:
            return f"Post with ID {post_id} not found.", 404

        if request.method == 'POST':
            # Read new data from the form
            post['author'] = request.form.get('author', '').strip()
            post['title'] = request.form.get('title', '').strip()
            post['content'] = request.form.get('content', '').strip()

            # Validation
            if not (post['author'] and post['title'] and post['content']):
                raise ValueError("All fields must be filled.")

            save_posts(posts)
            return redirect(url_for('index'))

        return render_template('update.html', post=post)

    except Exception as e:
        print(f"Error editing the post with ID {post_id}: {e}")
        return "An error occurred while updating the blog post.", 500

if __name__ == '__main__':
    # Start the Flask application in debug mode
    app.run(host='0.0.0.0', port=5000, debug=True)
