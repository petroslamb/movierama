.. MovieRama documentation master file, created by
   sphinx-quickstart.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to MovieRama's documentation!
======================================================================

The application is (yet another)
social sharing platform where users can share their favorite movies. 

Each movie has a title
and a small description as well as a date that corresponds to the date it was added to the
database. In addition it holds a reference to the user that submitted it. Users can also
express their opinion about a movie by either likes or hates.

When an unregistered user visits the homepage, they see the list of movies that have been
added to the system, as well as links for logging in or signing up. Each movie contains the
following information:

● Title

● Description

● Name of the user

● Date of publication

● Number of likes

● Number of hates

The name of the user is a link that, when clicked upon, filters the movies down to the items
that have been shared by this specific user. The list can also be sorted by the number of
likes, number of hates or the publication date.

In addition to the functionality described above, registered users are able to add their own
movies and express their opinion for other movies by either a like or a hate. Voting is
performed by clicking on the respective counters that are displayed for each movie.

● Users should be able to log into their account or sign up for a new one

● Users should be able to add movies by completing a form. Movies should be
persisted and reference the user that submitted them.

● Users should be able to express their opinion for any movie by either a like or a hate.
Users can vote only once for each movie and can change their vote at any time by
switching to the opposite vote or by retracting their vote altogether.

● Users should not be able to vote for the movies they have submitted.

● Users should be able to view the list of movies and sort them by number of likes,
number of hates or date added.

● Users should be able to view all movies submitted by a specific user.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   howto
   users



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
