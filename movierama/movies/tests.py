from django.test import Client, TestCase

from movierama.users.models import User

from .models import Movie


class TestMovieViews(TestCase):
    """Example integration tests on the view functions of the movies app"""

    def setUp(self):
        # Add a user to the database
        self.user = User.objects.create_user(username="testuser", password="12345")
        # Add a movie to the database, from the user
        self.movie = Movie.objects.create(
            title="Test Movie", description="Test Movie Description", user=self.user
        )
        # Add a second user to the database, to login with.
        self.user2 = User.objects.create_user(username="testuser2", password="12345")
        # Create a test client to send requests to the view functions
        self.client2 = Client()
        # Login with the user2
        self.client2.login(username="testuser2", password="12345")

    def test_home_and_about_pages_return_ok(self):
        """Just a quick test to make sure the home and about pages return a 200"""
        # Get the home page for anonymous users
        response = self.client.get("/")
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the response is html.
        self.assertEqual(response["content-type"], "text/html; charset=utf-8")
        # Get the about page for anonymous users
        response = self.client.get("/about/")
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the response is html.
        self.assertEqual(response["content-type"], "text/html; charset=utf-8")

    def test_movies_list(self):
        # Get the movies list page for anonymous users
        response = self.client.get("/movies/")
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the response is html.
        self.assertEqual(response["content-type"], "text/html; charset=utf-8")
        # Check that the response contains the movie
        self.assertContains(response, "Test Movie")

    def test_my_movies(self):
        # Redirect to the login page for anonymous users
        response = self.client.get("/movies/my_movies/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/movies/my_movies/")

        # Use the user2 logged in
        response = self.client2.get("/movies/my_movies/")
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the response is html.
        self.assertEqual(response["content-type"], "text/html; charset=utf-8")

    def test_movies_create(self):
        # Redirect to the login page for anonymous users
        response = self.client.get("/movies/my_movies/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/movies/my_movies/")

        # Use logged in client to create a movie using the form
        response = self.client2.post(
            "/movies/new/",
            {
                "title": "Test Movie 2",
                "description": "Test Movie Description 2",
            },
            follow=True,
        )
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the response is html.
        self.assertEqual(response["content-type"], "text/html; charset=utf-8")
        # Check that the response contains the movie
        self.assertContains(response, "Test Movie 2")

    def test_movies_update(self):
        # Use logged in client to create a movie using the form
        response = self.client2.post(
            "/movies/new/",
            {
                "title": "Test Movie 2",
                "description": "Test Movie Description 2",
            },
            follow=True,
        )
        # Get movie id
        movie_id = Movie.objects.get(title="Test Movie 2").id
        # Edit the movie using the form
        response = self.client2.post(
            f"/movies/edit/{movie_id}/",
            {
                "title": "Test Movie 3",
                "description": "Test Movie Description 3",
            },
            follow=True,
        )
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the response is html.
        self.assertEqual(response["content-type"], "text/html; charset=utf-8")
        # Check that the response contains the movie
        self.assertContains(response, "Test Movie 3")

    def test_movies_delete(self):
        # Use logged in client to create a movie using the form
        response = self.client2.post(
            "/movies/new/",
            {
                "title": "Test Movie 2",
                "description": "Test Movie Description 2",
            },
            follow=True,
        )
        # Get movie id
        movie_id = Movie.objects.get(title="Test Movie 2").id
        # Delete the movie using the form
        response = self.client2.post(f"/movies/delete/{movie_id}/", follow=True)
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the response is html.
        self.assertEqual(response["content-type"], "text/html; charset=utf-8")
        # Check that the response does not contain the movie
        self.assertNotContains(response, "Test Movie 2")

    def test_movies_like_unlike_remove(self):
        # Use logged in client to vote for a movie
        response = self.client2.post(
            f"/movies/movie_vote/{self.movie.id}/",
            {
                "vote": "like",
            },
            follow=True,
        )
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the response is html.
        self.assertEqual(response["content-type"], "text/html; charset=utf-8")
        # Check that the response contains the movie
        self.assertContains(response, "Test Movie")
        # Check that the movie has 1 vote
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.num_vote_up, 1)
        self.assertEqual(self.movie.num_vote_down, 0)

        # Revote the movie, to show that has no effect.
        response = self.client2.post(
            f"/movies/movie_vote/{self.movie.id}/",
            {
                "vote": "like",
            },
            follow=True,
        )
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the movie has 1 vote
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.num_vote_up, 1)
        self.assertEqual(self.movie.num_vote_down, 0)

        # Downvote the movie
        response = self.client2.post(
            f"/movies/movie_vote/{self.movie.id}/",
            {
                "vote": "dislike",
            },
            follow=True,
        )
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the movie has 1 vote
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.num_vote_up, 0)
        self.assertEqual(self.movie.num_vote_down, 1)

        # Remove the vote altogether
        response = self.client2.post(
            f"/movies/movie_vote/{self.movie.id}/",
            {
                "vote": "remove",
            },
            follow=True,
        )
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the movie has 0 votes
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.num_vote_up, 0)
        self.assertEqual(self.movie.num_vote_down, 0)

    def test_user_cannot_vote_own_movies(self):
        # Use logged in cliet to create a movie
        response = self.client2.post(
            "/movies/new/",
            {
                "title": "Test Movie 2",
                "description": "Test Movie Description 2",
            },
            follow=True,
        )
        # Get movie id
        movie_id = Movie.objects.get(title="Test Movie 2").id
        # Use logged in client to vote for the movie
        response = self.client2.post(
            f"/movies/movie_vote/{movie_id}/",
            {
                "vote": "like",
            },
            follow=True,
        )
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check the movie has 0 votes
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.num_vote_up, 0)
        self.assertEqual(self.movie.num_vote_down, 0)

    def test_filter_movies_by_user(self):
        # Use logged client to get the list of movies for all users
        response = self.client2.get("/movies/movie_users/", follow=True)
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check the movie is in the response.
        self.assertContains(response, "Test Movie")

        # Get the id of user and user2
        user_id = User.objects.get(username="testuser").id
        user2_id = User.objects.get(username="testuser2").id

        # Get the user movies list for the firstr user
        response = self.client2.get(f"/movies/movie_users/?user={user_id}", follow=True)
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check the movie is in the response.
        self.assertContains(response, "Test Movie")

        # Get the user movies list for the second user
        response = self.client2.get(
            f"/movies/movie_users/?user={user2_id}", follow=True
        )
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check the movie is not in the response.
        self.assertNotContains(response, "Test Movie")
