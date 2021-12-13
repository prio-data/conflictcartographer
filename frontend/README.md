
# Conflict Cartographer Frontend

This is the frontend component of Conflict Cartographer.  The frontend is
written in [Vue](https://vuejs.org/), an excellent frontend framework.  The
frontend is organized into views, which are presented via Vue router.

## Organization

The frontend code is organized into four folders:

* `./views`:      Pages shown to the user
* `./components`: Reusable components shared between views
* `./lib`:        (JavaScript) code used in views
* `./testing`:    Utility code for testing.

Each view is registered in the Vue Router, found in `./router.js`.
